import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats


def remove_ticks(ax):
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')


def remove_splines(ax, spl):
    for s in spl:
        ax.spines[s].set_visible(False)


def modify_splines(ax, lwd, col):
    for s in ['bottom', 'left', 'top', 'right']:
        ax.spines[s].set_linewidth(lwd)
        ax.spines[s].set_color(col)


class Distribution(object):
    """
    Given an initial set of data, computes the best fitted distribution and corresponding parameters
    from predefined list of known distributions
    """

    def __init__(self, distr_names_list=["norm", "lognorm", "expon", "uniform", "truncnorm", "exponweib", "weibull_max",
                                         "weibull_min", "pareto", "genextreme"]):
        self.distr_names = distr_names_list
        self.distr_results = []
        self.params = {}
        self.distribution_name = ""
        self.pvalue = 0
        self.param = None
        self.is_fitted = False

    def fit(self, initial_data):

        """
        :param initial_data: pandas series of initial data that has to be fitted
        :return: name of the distribution that fits the best and associated p value (computed by ks test)
        """

        # going through all distributions
        for distr_name in self.distr_names:
            # best parameters for this distribution
            distr = getattr(stats, distr_name)
            param = distr.fit(initial_data)
            self.params[distr_name] = param

            # Kolmogorov-Smirnov test for these parameters
            D, p = stats.kstest(initial_data, distr_name, args=param)
            self.distr_results.append((distr_name, p))

        # select the best fitted distribution
        best_distr, best_p = (max(self.distr_results, key=lambda tup: tup[1]))

        # store the name of the best fit and its p value and parameters
        self.distribution_name = best_distr
        self.pvalue = best_p
        self.param = self.params[best_distr]
        self.is_fitted = True

        return self.distribution_name, self.pvalue

    def random(self, n=1):

        """
        :param n: int, number of samples that will be drawn according to the best fitted distribution
        :return: array of samples drawn according to the best fitted distribution
        """

        if self.is_fitted:
            param = self.params[self.distribution_name]
            distr = getattr(stats, self.distribution_name)
            return distr.rvs(*param[:-2], loc=param[-2], scale=param[-1], size=n)
        else:
            raise ValueError('Must first run the fit method.')

    def plot(self, initial_data, name, ax, fitted_distr=True, lab="Actual"):

        """
        :param initial_data: pandas series of initial data that has to be fitted
        :param name: string of the name of the attribute that is being fitted
        :pram ax: matplotlib ax for display
        :param fitted_distr: bool (indicates is fitted distribution is plotted on top of initial distribution)
        :param lab: string, label for initial data
        """

        # for graphic view
        remove_ticks(ax)
        modify_splines(ax, lwd=0.75, col='0.8')
        remove_splines(ax, ['top', 'right'])
        ax.patch.set_facecolor('0.93')
        ax.grid(True, 'major', color='0.98', linestyle='-', linewidth=1.0)
        ax.set_axisbelow(True)

        x = self.random(n=len(initial_data))
        if fitted_distr:
            ax.hist(x, bins=30, alpha=0.4, label='Fitted', density=True, ec="k", histtype='stepfilled')
        ax.hist(initial_data, bins=30, alpha=0.4, label=lab, density=True, ec="k", histtype='stepfilled')
        ax.set_title(name)
        ax.legend(loc='upper right')

        return ax


class Model:
    """
    Computes the generative model from an initial data-frame
    """

    def __init__(self, dataframe):
        self.df = dataframe
        self.df_normed = pd.DataFrame(columns=self.df.columns)
        self.distributions = {}
        self.distr_computed = False


    def compute_distributions(self, display_results=True):

        """
        Computes the best fitted distribution for each attribute and prints its name, associated p value
        (computed from ks test), and parameters
        :param display_results: bool that indicates whether information on the fitted distribution will be printed
        """

        for attribute in self.df:
            distr = Distribution()
            distr.fit(self.df[attribute])
            self.distributions[attribute] = distr
            self.distr_computed = True
            if display_results:
                print("The distribution that fits the best attribute " + attribute + " is " + distr.distribution_name)
                print("The pvalue is", distr.pvalue, " with the following parametrers:", distr.param)
                print("\n")

    def plot_distributions(self, fitted_distr=True, lab="Actual"):

        """
        Plots the distribution of each attribute of the main data-frame
        :param fitted_distr: bool (indicates is fitted distributions will be plotted on top of
        initial distributions)
        :param lab: string, label for initial data
        """

        if self.distr_computed:
            for attribute in self.df:
                fig, ax = plt.subplots()
                self.distributions[attribute].plot(self.df[attribute], attribute, ax, fitted_distr, lab)
                plt.show()
        else:
            raise ValueError('Must compute the distributions first.')


