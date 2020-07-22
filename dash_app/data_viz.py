import numpy as np
from scipy.stats.stats import pearsonr
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
from common_structure import Model
import sys
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

SAVE_PATH = Path('/static/images')
class Closeness:
    """
    Graphical display of closeness between original and generated data-frames
    """

    def __init__(self, init, gen):
        self.initial_df = init
        self.generated_df = gen
        self.correlations = {}

    def computes_correlations(self):

        """
        Computes in numpy arrays pairwise Pearson correlation coefficients for initial and generated data
        """

        self.correlations["initial"] = np.zeros((len(self.initial_df.columns), len(self.initial_df.columns)))
        self.correlations["generated"] = np.zeros((len(self.generated_df.columns), len(self.generated_df.columns)))

        # pairwise coefficients for initial data
        for index1, col1 in enumerate(self.initial_df.columns):
            for index2, col2 in enumerate(self.initial_df.columns):
                self.correlations["initial"][index1, index2] = \
                pearsonr(self.initial_df[col1].to_numpy(), self.initial_df[col2].to_numpy())[0]

        # pariwise coefficients for generated data
        for index1, col1 in enumerate(self.generated_df.columns):
            for index2, col2 in enumerate(self.generated_df.columns):
                self.correlations["generated"][index1, index2] = \
                pearsonr(self.generated_df[col1].to_numpy(), self.generated_df[col2].to_numpy())[0]

    def set_ax_heatmap(self, ax, hmap, absc, ordo, title):

        """
        Sets ax in order to compute 2D heatmap
        :param ax: matplotlib ax for display
        :param hmap: 2D numpy array of pariwise pearson correlation coefficients
        :param absc, ordo: list of strings (column names)
        :param title: string (title of ax for display)
        :return: matplotlib ax with adjustments for display
        """

        ax.set_xticks(np.arange(len(absc)))
        ax.set_yticks(np.arange(len(ordo)))

        # labels
        ax.set_xticklabels(absc)
        ax.set_yticklabels(ordo)

        # Rotation and alignment of xlabels
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        # displaying actual values
        for i in range(len(absc)):
            for j in range(len(ordo)):
                text = ax.text(j, i, np.round(hmap[i, j], 2), ha="center", va="center", color="w")

        # title
        ax.set_title(title)

        return ax

    def pearson_plot(self):

        """
        Computes a 2D heatmap of pairwise Pearson correlations
        """

        # computing correlation matrices
        self.computes_correlations()

        # labels for axes
        absc1, absc2 = self.initial_df.columns, self.generated_df.columns
        ordo1, ordo2 = self.initial_df.columns, self.generated_df.columns

        # computing heatmaps
        hmap1, hmap2 = self.correlations["initial"], self.correlations["generated"]

        fig_init = go.Figure(
            {
                "data": [go.Heatmap(x=absc1, y=ordo1, z=hmap1, colorscale='RdBu', zmid=0)],
                "layout": go.Layout(title=go.layout.Title(text="Initial dataframe")),
            }
        )

        fig_gen = go.Figure(
            {
                "data": [go.Heatmap(x=absc2, y=ordo2, z=hmap2, colorscale='RdBu', zmid=0)],
                "layout": go.Layout(title=go.layout.Title(text="Generated dataframe")),
            }
        )
        fig_gen.update_yaxes(automargin=True)
        fig_init.update_yaxes(automargin=True)

        return fig_gen, fig_init

    def variables_scatter_plot(self):

        """
        Computes scatter plots between first attribute and all of the others for initial and generated sets
        """

        ref_col1 = self.initial_df.columns[0]
        ref_col2 = self.generated_df.columns[0]
        fig, axes = plt.subplots(len(self.initial_df.columns) - 1, 2, figsize=(8, 8))

        # scatter plots for intial data
        for index, col in enumerate(self.initial_df.columns[1:]):
            axes[index][0].scatter(self.initial_df[ref_col1], self.initial_df[col])
            axes[index][0].set_ylabel(col)

        # scatter plots for generated data
        for index, col in enumerate(self.generated_df.columns[1:]):
            axes[index][1].scatter(self.generated_df[ref_col2], self.generated_df[col])

        # common abscissa axis label (first attribute)
        plt.setp(axes[-1, :], xlabel=ref_col1)

        # column titles
        for ax, col in zip(axes[0], ["Original", "Generated"]):
            ax.set_title(col)

        fig.tight_layout()
        fig.savefig(SAVE_PATH / "scatter.png")

    def compare_distributions(self):

        """
        Plots for each attribute histograms of initial data and generated data for visual comparison
        """

        Mod = Model(self.initial_df)
        Mod_gen = Model(self.generated_df)

        Mod.compute_distributions(display_results=False)
        Mod_gen.compute_distributions(display_results=False)

        fig, axes = plt.subplots(1, len(self.initial_df.columns))
        for i, attribute in enumerate(self.initial_df):

            axes[i] = Mod_gen.distributions[attribute].plot(Mod_gen.df[attribute], attribute, axes[i], fitted_distr=False,
                                                  lab="Generated data")
            axes[i] = Mod.distributions[attribute].plot(Mod.df[attribute], attribute, axes[i], fitted_distr=False, lab="Initial data")


        fig.savefig(SAVE_PATH / "distr.png")
