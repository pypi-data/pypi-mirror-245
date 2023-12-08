import matplotlib.pyplot as plt
import matplotlib.scale as mscale
import matplotlib.transforms as mtransforms
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import uniform, randint


class MinusLog10Scale(mscale.ScaleBase):
    """
    ScaleBase class for generating -log10 scale. (Manhattan plot)
    """

    name = '-log10'

    def __init__(self, axis, **kwargs):
        mscale.ScaleBase.__init__(self, axis)

    def set_default_locators_and_formatters(self, axis):
        axis.set_major_locator(ticker.AutoLocator())
        axis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'-log10({x:.0e})'))
        axis.set_minor_locator(ticker.NullLocator())
        axis.set_minor_formatter(ticker.NullFormatter())

    def limit_range_for_scale(self, vmin, vmax, minpos):
        return max(0., vmin), vmax

    class MinusLog10Transform(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def transform_non_affine(self, a):
            a = np.array(a)
            r = -np.log10(a)
            r: np.ndarray
            if np.isnan(r).any():
                print(a)
                np.nan_to_num(r, copy=False, nan=10.0)
                # r = -np.log10(np.abs(a))
            return r

        def inverted(self):
            return MinusLog10Scale.InvertedMinusLog10Transform()

    class InvertedMinusLog10Transform(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def transform(self, a):
            return 10 ** -np.array(a)

        def inverted(self):
            return MinusLog10Scale.MinusLog10Transform()

    def get_transform(self):
        return self.MinusLog10Transform()


mscale.register_scale(MinusLog10Scale)

df = pd.DataFrame({'gene': ['gene-%i' % i for i in np.arange(10000)],
                'pvalue': uniform.rvs(size=10000),
                'chromosome': ['ch-%i' % i for i in randint.rvs(0, 12, size=10000)]})

# -log_10(pvalue)

df.chromosome = df.chromosome.astype('category')
df.chromosome = df.chromosome.cat.set_categories(['ch-%i' % i for i in range(12)], ordered=True)
df = df.sort_values('chromosome')

# How to plot gene vs. -log10(pvalue) and colour it by chromosome?
df['ind'] = range(len(df))
df_grouped = df.groupby(('chromosome'))

fig = plt.figure()
ax = fig.add_subplot(111)
colors = ['red', 'green', 'blue', 'yellow']
x_labels = []
x_labels_pos = []
for num, (name, group) in enumerate(df_grouped):
    group.plot(kind='scatter', x='ind', y='pvalue', color=colors[num % len(colors)], ax=ax)
    x_labels.append(name)
    x_labels_pos.append((group['ind'].iloc[-1] - (group['ind'].iloc[-1] - group['ind'].iloc[0]) / 2))
ax.set_xticks(x_labels_pos)
ax.set_xticklabels(x_labels)
ax.set_yscale('-log10')
ax.set_xlim([0, len(df)])
# ax.set_ylim([0, 3.5])
ax.set_xlabel('Chromosome')
plt.show()


exit(0)
# Simulate DataFrame
df = pd.DataFrame({
    'rsid': [f'rs{i}' for i in np.arange(10000)],  # Reference SNP cluster ID (not strictly required)
    'chrom': [i for i in randint.rvs(1, 23 + 1, size=10000)],
    'pos': [i for i in randint.rvs(0, 10 ** 5, size=10000)],
    'pval': uniform.rvs(size=10000)})
df = df.sort_values(['chrom', 'pos'])
df.reset_index(inplace=True, drop=True)
df['i'] = df.index


def plot_old(df):
    df['-logp'] = -np.log10(df.pval)

    # Generate Manhattan plot: (#optional tweaks for relplot: linewidth=0, s=9)
    plot = sns.relplot(
        data=df, x='i', y='-logp', aspect=3.7,
        hue='chrom', palette='bright', legend=None
    )
    chrom_df = df.groupby('chrom')['i'].median()
    plot.ax.set_xlabel('chrom')
    plot.ax.set_xticks(chrom_df)
    plot.ax.set_xticklabels(chrom_df.index)
    plot.fig.suptitle('Manhattan plot')

    plt.show()


def plot_new(df):
    plot = sns.relplot(
        data=df, x='i', y='pval',
        hue='chrom', palette='bright', legend=None
    )
    # plot.ax.set_ylim(top=0)

    chrom_df = df.groupby('chrom')['i'].median()
    # plot.ax.set_xlabel('chrom')
    # plot.ax.set_xticks(chrom_df)
    # plot.ax.set_xticklabels(chrom_df.index)
    plot.fig.suptitle('Manhattan plot')
    # plot.ax.tick_params(
    #     axis='both', which='both',
    #     bottom=False, top=False, left=False, right=False,
    #     labelbottom=False
    # )
    plt.grid(False)
    plt.axis('off')

    plot.ax.set_yscale('-log10')

    plt.show()


# plot_old(df.copy(deep=True))
plot_new(df.copy(deep=True))
