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