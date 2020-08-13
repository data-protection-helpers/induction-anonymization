import numpy as np
import string
import random
import pandas as pd


# complete masking
def complete_masking(df, attributes):
    df_masked = df.copy()

    for row in df_masked.itertuples():
        for attribute in attributes:
            masked_val = []
            val = str(getattr(row, attribute))
            for i in range(len(val)):
                masked_val.append("#")
            processed = "".join(masked_val)
            df_masked.loc[row.Index, attribute] = processed
    return df_masked


# swapping
def swap(df, attributes):
    for attribute in attributes:
        swap = df[attribute].copy()
        np.random.shuffle(swap.to_numpy())
        df[attribute] = swap
    return df


# text generation
def generates_text(df, attributes):
    df_masked = df.copy()

    for row in df_masked.itertuples():
        for attribute in attributes:
            generated_text_list = []
            val = str(getattr(row, attribute))
            for i, c in enumerate(val):
                if c.isnumeric():
                    generated_text_list.append(str(random.randint(0, 9)))
                elif c == " ":
                    generated_text_list.append(" ")
                else:
                    generated_text_list.append(random.choice(string.ascii_letters).upper())

            generated_text = "".join(generated_text_list)
            df_masked.loc[row.Index, attribute] = generated_text

    return df_masked


# generalization
def generalization(df, attributes, intervals):
    df_generalized = df.copy()

    for i, attribute in enumerate(attributes):
        test = []
        minimal_value = min(df[attribute])
        maximal_value = max(df[attribute])
        c = minimal_value
        while c < maximal_value:
            test.append(c)
            c += intervals[i]
        df_generalized[attribute] = pd.cut(x=df_generalized[attribute], bins=test)

    return df_generalized
