import numpy as np


def swap(df, attributes):
    for attribute in attributes:
        swap = df[attribute].copy()
        np.random.shuffle(swap.to_numpy())
        df[attribute] = swap
    return df
