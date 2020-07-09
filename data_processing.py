from tools import gauss_truncated


def categorical_to_numerical(df, categorical_fields):
    """
    Converts categorical data attributes to numerical
    :param df: initial pandas data-frame
    :param categorical_fields: list of strings (attributes names that will be converted from categorical
    to numerical
    :return:  dictionary where keys are names of numerical fields computed from categorical, and values are
    pandas data-frames with sorted categorical values and corresponding intervals
    """

    transitional_dfs = {}
    df_categorical = df.copy()

    for categorical_field in categorical_fields:

        assert (categorical_field in df), "This field doesn't exist in the database"

        # adding empty column for new numerical field
        df_categorical[categorical_field + "_NUM"] = 0

        # data-frame of unique discrete values from categorical field and associated proportions (decreasing order)
        unique_values_df = df[categorical_field \
            ].value_counts(normalize=True).rename_axis('unique_values').reset_index(name='counts')

        # building the intervals
        unique_values_df["interval_down"] = ""
        unique_values_df["interval_up"] = ""
        for index, row in unique_values_df.iterrows():
            if index == 0:
                unique_values_df.loc[index, "interval_down"] = 0
                unique_values_df.loc[index, "interval_up"] = row["counts"]
            else:
                unique_values_df.loc[index, "interval_down"] = \
                    unique_values_df[index - 1:index]["interval_up"].item()
                unique_values_df.loc[index, "interval_up"] = \
                    unique_values_df[index - 1:index]["interval_up"].item() + row["counts"]

        transitional_dfs[categorical_field + "_NUM"] = unique_values_df

        # filling new numerical column
        for index, row in df.iterrows():
            value = row[categorical_field]
            i = unique_values_df[unique_values_df["unique_values"] == value].index.tolist()[0]

            # drawing value from truncated gaussian distribution
            a = unique_values_df[i:i + 1]["interval_down"].item()
            b = unique_values_df[i:i + 1]["interval_up"].item()
            mu = a + (b - a) / 2
            sigma = (b - a) / 6
            x = gauss_truncated(a, b, mu, sigma)
            df_categorical.loc[index, categorical_field + "_NUM"] = x
        df_categorical = df_categorical.drop(categorical_field, axis=1)

    return df_categorical, transitional_dfs


def numerical_to_categorical(df, categorical_fields, transitional_dfs):
    """
    Converts numerical data back to categorical
    :param df: original data-frame with numerical data
    :param categorical_fields: list of strings (attribute names that have to be converted from numerical
    to categorical)
    :param transitional_dfs: dictionary returned by categorical_to_numerical function
    :return: new data-frame where requested numerical fields have been turned to categorical
    """

    df_final = df.copy()
    for categorical_field in categorical_fields:
        for index, row in df.iterrows():
            discrete_value = 0

            # searching for the corresponding interval
            for index2, row2 in transitional_dfs[categorical_field].iterrows():
                if row2["interval_down"] <= df[categorical_field][index] <= row2["interval_up"]:
                    discrete_value = row2["unique_values"]
            df_final.loc[index, categorical_field] = discrete_value

    return df_final