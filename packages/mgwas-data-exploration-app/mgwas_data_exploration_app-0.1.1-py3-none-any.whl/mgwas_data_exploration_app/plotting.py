import logging

import matplotlib as mpl
import numpy as np
import pandas as pd
from scipy.cluster import hierarchy

mpl.use('SVG')
# The SVG backend avoids this error message:
# ValueError: Image size of 700x165660 pixels is too large. It must be less than 2^16 in each direction.
# This allows for dendrograms with at least 20'000 traits

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.collections import PatchCollection, QuadMesh
from matplotlib.patches import Rectangle

from .utils import RecursionLimit

logger = logging.getLogger('mgwas_data_exploration_app.plotting')


def plot_dendrogram(
        linkage_matrix: np.ndarray,
        labels: [str],
        ax: Axes,
        xscale: str = 'linear'
) -> {}:
    if xscale != 'linear':
        ax.set_xscale(xscale)

    with RecursionLimit(max(1000, len(linkage_matrix))):  # empirically tested for up to 20'000 traits
        dendrogram_params = hierarchy.dendrogram(
            linkage_matrix,
            orientation='left',
            labels=labels,
            no_labels=True,
            ax=ax,
            color_threshold=0, above_threshold_color='k'  # greyscale
        )

    ax.tick_params(
        axis='both', which='both',
        bottom=True, top=False, left=False, right=False,
        labelleft=False,
    )
    return dendrogram_params


def plot_scores_linear(
        scores: pd.DataFrame,
        fig: Figure,
        ax: Axes,
        scores_config: {str: dict}
) -> [QuadMesh]:
    # determine y intervals: [0, 10, 20, ...]
    y = np.arange(start=5, stop=len(scores.index) * 10, step=10)

    for i, (col, def_) in enumerate(scores_config.items()):
        if col not in scores.columns:
            continue

        ax.scatter(
            scores[col], y,
            marker=def_['marker-matplotlib'],
            color=def_['color']
        )

    # add y ticks and labels (trait names)
    ax.yaxis.tick_right()
    ytick_locations = np.arange(start=5, stop=len(scores) * 10, step=10)
    ax.set_yticks(ytick_locations, scores.index)
    ax.tick_params(
        axis='y', which='both',
        bottom=False, top=False, left=False, right=False,
        labelbottom=False
    )

    # add grid
    ax.set_axisbelow(True)
    ax.grid(visible=True, which='major', axis='x', linestyle='solid')
    ax.grid(visible=True, which='minor', axis='x', linestyle='dashed')

    # add shape on top and ticks that can be made clickable
    add_clickable_patches(scores.index, fig, ax)


def plot_scores_manhattan(
        scores: pd.DataFrame,
        fig: Figure,
        ax: Axes,
        scores_config: {str: dict}
) -> [QuadMesh]:
    # determine y intervals: [0, 10, 20, ...]
    y = np.arange(start=5, stop=len(scores.index) * 10, step=10)

    ax.set_xlim(left=0)  # corresponds to q = 1; q-values cannot be greater than 1

    x_max = 1.  # minimum width of plot
    for i, (col, def_) in enumerate(scores_config.items()):
        if col not in scores.columns:
            continue

        # transform q-values to -log10(q-value)
        x = -np.log10(scores[col])

        x_max = max(x_max, x.max())

        ax.scatter(
            x, y,
            marker=def_['marker-matplotlib'],
            color=def_['color']
        )

    # add y ticks and labels (trait names)
    ax.yaxis.tick_right()
    ytick_locations = np.arange(start=5, stop=len(scores) * 10, step=10)
    ax.set_yticks(ytick_locations, scores.index)

    # add x ticks (q-values)
    ax.set_xticks(ticks=np.arange(0, x_max + 1, 1), minor=False)

    ax.tick_params(
        axis='both', which='both',
        bottom=False, top=False, left=False, right=False,
        labelbottom=False
    )

    # add grid
    ax.set_axisbelow(True)
    ax.grid(visible=True, which='both', axis='x', linestyle='dashed')

    # add shape on top and ticks that can be made clickable
    add_clickable_patches(scores.index, fig, ax)


def add_clickable_patches(
        patch_names: [str],
        fig: Figure,
        ax: Axes
):
    x_start, x_end = sorted(ax.get_xlim())
    x_width = (x_end - x_start) * 5

    patches = [
        Rectangle(xy=(x_start, i * 10), width=x_width, height=10)
        for i in range(len(patch_names))
    ]

    # Create patch collection with specified colour/alpha
    pc = PatchCollection(
        patches,
        facecolors='white', alpha=1e-6,  # will result in 'opacity: 0'
        gid='clickable-patches',
        transform=ax.transData, figure=fig
    )

    # add urls -> this doesn't work
    # pc.set_urls([f'overview.html?trait={n}' for n in patch_names])

    fig.add_artist(pc)


def final_plot(
        linkage_matrix,
        labels,
        summary_df,
        scores_config: dict,
        workdir,
        dendrogram_x_scale: str = 'linear',
        scores_x_scale: str = 'manhattan'
):
    # calculate plot proportions
    content_height = max(3., len(labels) / 6)  # height dependent on number of compounds
    whitespace_abs = 0.6  # absolute amount of whitespace
    total_height = content_height + whitespace_abs  # total plot height
    whitespace_rel = whitespace_abs / 3 / total_height  # relative amount of whitespace

    # create matplotlib figure
    plt.close()
    fig = plt.figure(figsize=(8, total_height))  # dpi irrelevant if mpl.use('SVG')
    gs = fig.add_gridspec(
        nrows=1, ncols=2, width_ratios=(2, 1),
        left=0.05, right=0.6, bottom=whitespace_rel * 2, top=1 - whitespace_rel,
        wspace=0, hspace=0
    )

    # get axes objects with shared y-axis
    ax_dendrogram = fig.add_subplot(gs[0, 0])
    ax_colorbar = fig.add_subplot(gs[0, 1], sharey=ax_dendrogram)

    logger.info('Plotting dendrogram...')
    # plot dendrogram
    dendrogram_params = plot_dendrogram(linkage_matrix, labels=labels, ax=ax_dendrogram, xscale=dendrogram_x_scale)

    # reindex summary_df according to order in dendrogram
    summary_df = summary_df.reindex(dendrogram_params['ivl'])

    cols = [col for col in scores_config.keys() if col in summary_df.columns]
    if len(cols) != len(scores_config):
        logger.warning(f'The following columns from app_config are missing: {set(scores_config.keys()) - set(cols)}')
    scores_df = summary_df[cols]

    if scores_x_scale == 'linear':
        plot_scores_linear(scores=scores_df, fig=fig, ax=ax_colorbar, scores_config=scores_config)
    elif scores_x_scale == 'manhattan':
        plot_scores_manhattan(scores=scores_df, fig=fig, ax=ax_colorbar, scores_config=scores_config)
    else:
        raise ValueError(f'Unknown {scores_x_scale=}; must be one of ["linear", "manhattan"]')

    # save plot
    plt.savefig(f'{workdir}/overview_plot.svg', format='svg')
    plt.close()
    return summary_df
