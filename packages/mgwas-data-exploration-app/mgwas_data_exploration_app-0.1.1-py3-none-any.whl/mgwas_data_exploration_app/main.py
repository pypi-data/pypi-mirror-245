import os
import json
import logging
from shutil import copy as shutil_copy
import numpy as np
import pandas as pd
from scipy.cluster import hierarchy
from scipy.spatial.distance import cdist, squareform
from sklearn.preprocessing import scale as sklearn_scale
from .utils import ROOT_DIR
from .plotting import final_plot

logger = logging.getLogger('mgwas_data_exploration_app.main')


def mgwas_app(
        summary_df: str | pd.DataFrame,
        traits_df: str | pd.DataFrame,
        workdir: str,
        is_numeric: bool,
        app_config: str | dict = {},
        symmetric: bool = True,
        distance_metric: str = 'jaccard',
        linkage_method: str = 'ward',
        optimal_ordering: bool = True,
        corr_scale: bool = True,
        corr_method: str = 'pearson',
        dendrogram_x_scale: str = 'linear',
        scores_x_scale: str = 'manhattan',
):
    """
    Create dendrogram and scores plot, and copy data exploration app.

    :param summary_df: path to summary.tsv
    :param traits_df: path to traits_df.tsv
    :param workdir: Folder where the mGWAS output must be located, exepect to find a folder 'traits' with subfolders for each trait
    :param is_numeric: whether the data is numeric or binary
    :param app_config: path to json file to overwrite the default app config
    :param symmetric: if True, correlated and anti-correlated traits will cluster together
    :param distance_metric: distance metric (binary data only); See metric in https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html
    :param linkage_method: linkage method for clustering [single, complete, average, weighted, ward, centroid, median]
    :param optimal_ordering: whether to use optimal ordering; See scipy.cluster.hierarchy.linkage.
    :param corr_scale: whether to scale numeric data
    :param corr_method: correlation method (numeric data only) [pearson, kendall, spearman]
    :param dendrogram_x_scale: x-axis scale for dendrogram [linear, squareroot, log, symlog, logit]
    :param scores_x_scale: x-axis scale for scores plot [linear, manhattan]
    """
    assert os.path.isdir(f'{workdir}/traits'), f'{workdir}/traits does not exist'

    if type(summary_df) is str:
        summary_df = pd.read_csv(summary_df, sep='\t', index_col=0)

    if type(traits_df) is str:
        traits_df = pd.read_csv(traits_df, sep='\t', index_col=0)

    # load app config
    if type(app_config) is str:
        with open(app_config) as f:
            app_config = json.load(f)
    app_config['legend_info'] = 'The plot is log<sub>10</sub>-scaled.' if scores_x_scale == 'manhattan' else ''

    if len(summary_df) == 0:
        raise ValueError('summary_df is empty!')

    # copy files from exploration app
    logger.info('Copying exploration app...')
    app_config = copy_app(workdir, config=app_config)

    if len(summary_df) == 1:
        logger.warning('Only one trait, skipping dendrogram...')
        return

    # calculate linkage matrix
    if is_numeric:
        logger.info(f'Calculating dendrogram based on correlation of numeric features...')
        linkage_matrix, labels = calculate_linkage_matrix_from_numeric(
            summary_df, traits_df, symmetric, corr_scale, corr_method, linkage_method, optimal_ordering)
    else:
        logger.info(f'Calculating dendrogram based on binary data using {distance_metric} distances...')
        linkage_matrix, labels = calculate_linkage_matrix_from_binary(
            summary_df, traits_df, symmetric, distance_metric, linkage_method, optimal_ordering)

    # plot dendrogram
    logger.info('Calculating dendrogram plot...')
    summary_df = final_plot(linkage_matrix, labels, summary_df, app_config['scores'], workdir, dendrogram_x_scale, scores_x_scale)

    # save summary_df, ensure order matches plot
    logger.info('Saving sorted summary.tsv...')
    summary_df.index.name = 'Trait'
    summary_df.to_csv(f'{workdir}/summary.tsv', sep='\t')


def copy_app(workdir: str, config: dict) -> dict:
    if os.environ.get('MGWAS_LINK_ONLY', 'false').lower() in 'true':
        copy_fn = os.symlink
    else:
        copy_fn = shutil_copy

    # copy files
    for file in ['overview.html', 'trait.html']:
        copy_fn(src=f'{ROOT_DIR}/templates/{file}', dst=f'{workdir}/{file}')
    os.makedirs(f'{workdir}/app', exist_ok=True)
    for file in ['trait.js', 'trait.css', 'overview.js', 'overview.css', 'favicon.svg']:
        copy_fn(src=f'{ROOT_DIR}/templates/{file}', dst=f'{workdir}/app/{file}')

    # load base config
    with open(f'{ROOT_DIR}/templates/config.json') as f:
        app_config = json.load(f)

    # update config
    app_config.update(config)

    # write config
    with open(f'{workdir}/app/config.json', 'w') as f:
        json.dump(app_config, f, indent=4)

    return app_config


def calculate_linkage_matrix_from_binary(
        summary_df: pd.DataFrame,
        traits_df: pd.DataFrame,
        symmetric: bool = True,
        distance_metric: str = 'jaccard',
        linkage_method: str = 'ward',
        optimal_ordering: bool = True,
):
    # prepare data: False -> -1, NAN -> 0, True -> 1
    pre_distance = traits_df[summary_df.index].astype('float').T  # False -> 0; NAN -> NAN, True -> 1
    pre_distance = ((pre_distance.fillna(0.5) * 2) - 1).astype('int')

    if symmetric:
        # make symmetric: correlated and anti-correlated traits should cluster together.
        # whether class=0 or class=1 is arbitrary. Calculate both possibilities, take minimum
        d1 = cdist(pre_distance, pre_distance, metric=distance_metric)
        d2 = cdist(pre_distance, 0 - pre_distance, metric=distance_metric)
        distance_matrix = np.minimum(d1, d2) * 2  # multiply by 2 to make maximal distance 1 again
        del d1, d2
    else:
        distance_matrix = cdist(pre_distance, pre_distance, metric=distance_metric)

    distance_matrix = pd.DataFrame(distance_matrix, columns=pre_distance.index, index=pre_distance.index)

    # create linkage matrix for scipy.cluster.hierarchy.dendrogram
    linkage_matrix = hierarchy.linkage(
        squareform(distance_matrix),
        method=linkage_method,
        optimal_ordering=optimal_ordering
    )
    return linkage_matrix, distance_matrix.columns.values


def calculate_linkage_matrix_from_numeric(
        summary_df: pd.DataFrame,
        traits_df: pd.DataFrame,
        symmetric: bool = True,
        scale: bool = True,
        corr_method: str = 'pearson',
        linkage_method: str = 'ward',
        optimal_ordering: bool = True,
):
    pre_corr = traits_df[summary_df.index].astype('float')

    if scale:
        # scale the phenotypes to mean=0 and std=1
        pre_corr = pd.DataFrame(sklearn_scale(pre_corr), index=pre_corr.index, columns=pre_corr.columns)

    correlation_matrix = pre_corr.corr(method=corr_method)
    if symmetric:
        # make symmetric: correlated and anti-correlated traits should cluster together.
        correlation_matrix = correlation_matrix.abs()

    linkage_matrix = hierarchy.linkage(
        correlation_matrix.values,
        method=linkage_method,
        optimal_ordering=optimal_ordering
    )

    return linkage_matrix, correlation_matrix.index.values


def __main__():
    import fire
    fire.Fire(mgwas_app)
