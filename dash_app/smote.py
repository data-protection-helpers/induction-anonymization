from __future__ import division

import pandas as pd
import matplotlib.pyplot as plt

from numpy.random import seed
import numpy as np
import time
import sys
sys.path.insert(1, '../../')

from data_processing import categorical_to_numerical, numerical_to_categorical
from common_structure import Model, Distribution
from data_viz import Closeness


def computes_KNN(elem, target_list, k):
    """
    Computes k nearest neighbors of an element
    :param elem: numpy array of the element we consider
    :param target_list: numpy array of elements from which we will compute the neighbors
    :param k: int, number of neighbors in KNN
    :return: list of k nearest neighbors
    """

    # list of neighours: associated length and indexes
    distances_neighbors = []
    for i in range(len(target_list)):
        distances_neighbors.append([np.linalg.norm(target_list[i] - elem), i])
    distances_neighbors = sorted(distances_neighbors, key=lambda x: x[0])

    # we keep the k neighbors with smallest length
    closets_distances_neighbors = distances_neighbors[:k]

    # we compute the neighbors according to the indexes
    nearest_neighbors = []
    for i in range(k):
        nearest_neighbors.append(target_list[closets_distances_neighbors[i][1]])

    return nearest_neighbors


def standardize_data(X):
    """
    Returns reduced and centered data
    :param X: numpy array of initial data
    return: numpy array where columns have been standardized (zero mean and unit standard deviation)
    """

    X2 = X.copy()
    X2 = np.array(X2, dtype=float)
    for j in range(len(X2[0])):
        X2[:, j] = X2[:, j] - np.mean(X2[:, j])

        X2[:, j] = X2[:, j] / np.std(X2[:, j]) + 1 * 10 ** -16

    return X2


def destandardize_data(X, mean, std):
    """
    Destandardizes reduced and centered data
    :param X: array of initial reduced and centered data
    :param mean: float, wanted mean
    :param std: float, wanted standard deviation
    :return: numpy array where columns have been destandardized (have wanted mean and standard deviation)
    """

    X2 = X.copy()
    X2 = np.array(X2, dtype=float)
    for j in range(len(X2[0])):
        X2[:, j] = X2[:, j] * std[j]
        X2[:, j] = X2[:, j] + mean[j]

    return X2




class smote_model(Model):
    """
    Implements smote technique
    """

    def generate_data(self, k, n, visualization_2D=False):

        """
        Generates new data using smote
        :param k: int, number of neighbors that will be used for KNN
        :param n: int, number of elements that will be generated
        """

        if visualization_2D:
            fig, ax = plt.subplots()
            fig.canvas.draw()

        # new empty data-frame for generated data
        self.df_gen = np.zeros((n, self.df.shape[1]))

        # standardizing data
        self.df_norm = standardize_data(self.df.to_numpy())
        self.df_norm = pd.DataFrame(self.df_norm)

        c = 0
        for i in range(n // self.df.shape[0] + self.df.shape[0]):

            # going through each row
            for index, row in self.df_norm.iterrows():
                if c < n:
                    row = row.to_numpy()
                    target_rows = np.delete(self.df_norm.to_numpy(), index, axis=0)

                    # computing k nearest neighbors
                    neigh = computes_KNN(row, target_rows, k)

                    # selecting randomly one of them
                    seed()
                    rand = np.random.randint(k - 1)
                    selected_neigh = neigh[rand]

                    # creating new point between initial point and selected neighbor
                    new_point = row + np.random.rand(1)[0] * (selected_neigh - row)
                    self.df_gen[index] = new_point
                    c += 1

                    if visualization_2D:
                        stop_time = 1
                        plt.ion()
                        ax.clear()
                        ax.scatter(target_rows[:, 0], target_rows[:, 1], label="Initial data")
                        ax.scatter(row[0], row[1], c="r", label="Considered element")
                        time.sleep(stop_time)
                        fig.canvas.draw()
                        ax.scatter(np.array(neigh)[:, 0], np.array(neigh)[:, 1], c="cyan", label="Neighbors")
                        time.sleep(stop_time)
                        fig.canvas.draw()
                        ax.scatter(new_point[0], new_point[1], c="y", label="New point")
                        time.sleep(stop_time)
                        fig.canvas.draw()
                        fig.legend()

        if visualization_2D:
            plt.ioff()
            plt.close()

        self.df_gen = destandardize_data(self.df_gen, self.df.mean(), self.df.std())
        self.df_gen = pd.DataFrame(data=self.df_gen, columns=self.df.columns)

        return self.df_gen


def numerical_data(df_sample, categorical_fields, size):
    df_sample_num, transitional_dfs = categorical_to_numerical(df_sample, categorical_fields)

    print("nul", df_sample_num)

    Mod = smote_model(df_sample_num)

    # number of neighbors
    k = 5
    df_gen_num = Mod.generate_data(k, size)

    #print(df_gen_num)

    return df_gen_num, df_sample_num, transitional_dfs


def treatment_smote(df_gen_num, df_sample_num, transitional_dfs, categorical_fields):

    df_gen_cat = numerical_to_categorical(df_gen_num, categorical_fields, transitional_dfs)
    res = Closeness(df_sample_num, df_gen_num)
    fig_pearson_gen, fig_pearson_init = res.pearson_plot()

    return fig_pearson_gen, fig_pearson_init, df_gen_cat




