import pandas as pd
import numpy as np
import scipy.stats as stats
from math import sqrt
import sys
sys.path.insert(1, '../../')

from data_processing import categorical_to_numerical
from data_processing import numerical_to_categorical
from common_structure import Model, Distribution
from data_viz import Closeness
import math

def is_symmetric(M, rtol=1e-05, atol=1e-08):
    return np.allclose(M, M.T, rtol=rtol, atol=atol)

def is_pos_def(M):
    return np.all(np.linalg.eigvals(M) > 0)


def cholesky(M):
    """
    Performs Cholesky decomposition of a matrix
    :param M: symmetric and positive definite matrix
    :return: lower triangular matrix L from the decomposition
    """

    assert is_symmetric(M), "The matrix for Cholesky decomposition is not symmetric"
    assert is_pos_def(M), "The matrix for Cholesky decomposition is not positive definite"

    n = len(M)
    L = np.zeros((n, n))

    # performs the Cholesky decomposition
    for i in range(n):
        for k in range(i + 1):
            tmp_sum = sum(L[i][j] * L[k][j] for j in range(k))

            if (i == k):
                L[i][k] = sqrt(M[i][i] - tmp_sum)
            else:
                L[i][k] = (1.0 / L[k][k] * (M[i][k] - tmp_sum))
    return L


class Statistical_generative_model(Model):
    """
    Implements statistical generative model
    """

    def __init__(self, dataframe):
        super(Statistical_generative_model, self).__init__(dataframe)
        self.computed_copulas = False

    def gaussian_copula(self):

        """
        Converts all column distributions to standard normal
        """

        if self.distr_computed:

            # going through the rows
            for index, row in self.df.iterrows():
                values = {}
                initial_vect = np.array(row)
                transformed_vect = np.zeros(len(initial_vect))

                # going through the columns
                for i, attribute in enumerate(self.df):
                    # getting distribution of the column
                    distr = getattr(stats, self.distributions[attribute].distribution_name)
                    param = self.distributions[attribute].param
                    norm = getattr(stats, "norm")

                    # converting value to get standard normal distribution
                    transformed_vect[i] = norm.ppf(distr.cdf(initial_vect[i], *param[:-2], loc=param[-2], scale=param[-1]))

                    values[attribute] = transformed_vect[i]

                # adding normed results to a new data-frame
                new_row = pd.Series(values, name="new row")
                self.df_normed = self.df_normed.append(new_row, ignore_index=True)

            self.computed_copulas = True

            with pd.option_context('mode.use_inf_as_null', True):
                self.df_normed = self.df_normed.dropna()



        else:
            raise ValueError('Must compute the distributions first.')

    def sample(self):

        """
        :return: generated_row, numpy array (data-frame row) computed as a sample of the modeled distribution
        """

        if self.computed_copulas:

            # computing covariance matrix for the normed data-frame
            cov_matrix = self.df_normed.cov()
            cov_matrix = np.array(cov_matrix)
            nb_col = self.df_normed.shape[1]

            # computing cholesky decomposition
            L = cholesky(cov_matrix)

            mean = np.zeros(nb_col)
            cov = np.eye(nb_col)

            # generating new vector according to formula
            V = np.random.multivariate_normal(mean, cov)
            #U = L @ V
            U = np.matmul(L, V)
            generated_row = np.zeros(nb_col)
            for i, attribute in enumerate(self.df):
                distr = getattr(stats, self.distributions[attribute].distribution_name)
                param = self.distributions[attribute].param
                norm = getattr(stats, "norm")
                generated_row[i] = distr.ppf(norm.cdf(U[i]), *param[:-2], loc=param[-2], scale=param[-1])

            return generated_row

        else:
            raise ValueError("Must run gaussian_copula method first.")

    def generate_data(self, size):

        """
        Generates a data-frame of required size
        :param size: int, number of rows that will be generated
        :return: pandas data-frame with generated values
        """

        df_gen = pd.DataFrame(columns=self.df.columns)
        for index in range(size):
            values = {}
            row = self.sample()
            for i, attribute in enumerate(df_gen):
                values[attribute] = row[i]
            new_row = pd.Series(values, name="new row")
            df_gen = df_gen.append(new_row, ignore_index=True)
        return df_gen


def treatment_statistical(df_sample, categorical_fields):
    df_sample_num, transitional_dfs = categorical_to_numerical(df_sample, categorical_fields)
    Mod = Statistical_generative_model(df_sample_num)
    Mod.compute_distributions(display_results=False)
    Mod.gaussian_copula()
    size_of_generation = 100
    df_gen_num = Mod.generate_data(size_of_generation)

    df_gen_cat = numerical_to_categorical(df_gen_num, categorical_fields, transitional_dfs)

    res = Closeness(df_sample_num, df_gen_num)
    fig_pearson_gen, fig_pearson_init = res.pearson_plot()

    return fig_pearson_gen, fig_pearson_init, df_gen_cat, df_gen_num, df_sample_num
