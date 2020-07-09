import numpy as np
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt
from common_structure import Model


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

        # displaying the results
        fig, ax = plt.subplots(1, 2, figsize=(10, 10))
        ax[0] = self.set_ax_heatmap(ax[0], hmap1, absc1, ordo1, "Initial pairwise Pearson correlations")
        ax[1] = self.set_ax_heatmap(ax[1], hmap2, absc2, ordo2, "Generated pairwise Pearson correlations")
        fig.tight_layout()
        ax[0].imshow(hmap1, cmap=plt.cm.pink, alpha=0.9)
        ax[1].imshow(hmap2, cmap=plt.cm.pink, alpha=0.9)

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

    def compare_distributions(self):

        """
        Plots for each attribute histograms of initial data and generated data for visual comparison
        """

        Mod = Model(self.initial_df)
        Mod_gen = Model(self.generated_df)

        Mod.compute_distributions(display_results=False)
        Mod_gen.compute_distributions(display_results=False)

        for attribute in self.initial_df:
            fig, ax = plt.subplots()
            Mod_gen.distributions[attribute].plot(Mod_gen.df[attribute], attribute, ax, fitted_distr=False,
                                                  lab="Generated data")
            Mod.distributions[attribute].plot(Mod.df[attribute], attribute, ax, fitted_distr=False, lab="Initial data")
            plt.show()
