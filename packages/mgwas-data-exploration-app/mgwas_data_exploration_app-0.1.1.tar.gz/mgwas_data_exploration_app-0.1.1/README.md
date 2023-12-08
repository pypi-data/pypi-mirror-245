# mGWAS data exploration app

> [!NOTE]
> This tool was built for [Scoary2](https://github.com/MrTomRod/scoary-2)!

## Description

This is a simple, static HTML/JS data exploration that allows you to explore the results of mGWAS software, particularly large phenotypic datasets.

## Output

The app produces two types of HTML files that can be opened in any browser:

- `overview.html`: A simple overview of all traits in the dataset.
- `trait.html`: A more detailed view of a single trait.

The usage of this app is described on the Scoary2 [wiki](https://github.com/MrTomRod/scoary-2/wiki/App).

## Installation

1) Using pip: `pip install mgwas-data-exploration-app`
2) Using docker: `docker pull troder/scoary-2`

## How to prepare your data

### Expected folder structure

The app expects the following folder structure:

```
.
└── workdir
    ├── summary.tsv
    ├── traits.tsv
    ├── tree.nwk
    ├── isolate_info.tsv (optional)
    └── traits
        ├── trait1
        │   ├── coverage-matrix.tsv
        │   ├── meta.json
        │   ├── result.tsv
        │   └── values.tsv
        ├── trait2
        │   └── ...
        └── ...
```

### Input arguments

- `summary_df`: A table with the results of the mGWAS analysis. Rows: traits; columns: genes. (Separator: tab)
- `traits_df`: A table with the metadata of the traits. Rows: traits; columns: metadata. (Separator: tab)
- `workdir`: Folder where the mGWAS output must be located, exepect to find a folder 'traits' with subfolders for each trait.
- `is_numeric`: Whether the data is numeric or binary.
- `app_config`: A JSON file that overwrites the default app config. See the default [config.json](mgwas_data_exploration_app/templates/config.json). (Optional)
- `distance_metric`: The distance metric for the clustering of binary data. See the [scipy documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html).
  (Binary data only; default: jaccard)
- `linkage_method`: The linkage method for the clustering. One of [single, complete, average, weighted, ward, centroid, median]. (Default: ward)
- `optimal_ordering`: Whether to use optimal ordering. See [scipy.cluster.hierarchy.linkage](https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html) (Default: True)
- `corr_scale`: Whether to scale numeric data before clustering. (Numeric data only; default: True)
- `corr_method`: The correlation method for numeric data. One of [pearson, kendall, spearman]. (Numeric data only; default: pearson)
- `dendrogram_x_scale`: The x-axis scale for the dendrogram. One of [linear, squareroot, log, symlog, logit]. (Default: linear)
- `scores_x_scale`: The x-axis scale for the scores plot. One of [linear, manhattan]. (Default: linear)

### Usage

Get help with `mgwas-data-exploration-app --help` or reading the docstring of [main.py](mgwas_data_exploration_app/main.py).

**Python**

<details>

  <summary>Click here to expand.</summary>

```python
from mgwas_data_exploration_app.main import mgwas_app

mgwas_app(
    summary_df="summary.tsv",  # or a pandas.DataFrame
    traits_df="traits.tsv",  # or a pandas.DataFrame
    workdir="out",
    is_numeric=False,
    app_config="app_config.json",  # or dict
    distance_metric="jaccard",
    linkage_method="ward",
    optimal_ordering=True,
    corr_scale=True,
    corr_method="pearson",
    dendrogram_x_scale="linear",
    scores_x_scale="linear",
)
```

</details>

**Command line**

<details>

  <summary>Click here to expand.</summary>

```shell
mgwas-data-exploration-app \
    --summary summary.tsv \
    --traits traits.tsv \
    --workdir out \
    --is-numeric False \
    --app-config None \
    --distance-metric jaccard \
    --linkage-method ward \
    --optimal-ordering True \
    --corr-scale True \
    --corr-method pearson \
    --dendrogram-x-scale linear \
    --scores-x-scale linear
```

</details>

# Credits

This project is built using the following libraries:

- [PapaParse](https://www.papaparse.com/) for parsing the CSV files
- [Bootstrap](https://getbootstrap.com/) for the layout
- [SlimSelect](https://slimselectjs.com/) for the dropdowns
- [DataTables](https://datatables.net/) and [jQuery](https://jquery.com/) for the tables
- [Plotly](https://plotly.com/javascript/) for the plots
- [Phylocanvas](https://phylocanvas.org/) for the phylogenetic trees
- [Chroma.js](https://gka.github.io/chroma.js/) for the color scales
- [Popper.js](https://popper.js.org/) for the tooltips
