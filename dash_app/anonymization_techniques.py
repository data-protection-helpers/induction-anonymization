import numpy as np
import string
import random


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

