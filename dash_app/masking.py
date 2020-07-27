def complete_masking(df, attributes):
    df_masked = df.copy()
    for index, row in df.iterrows():
        for attribute in attributes:
            masked_val = []
            val = str(row[attribute])
            for i in range(len(val)):
                masked_val.append("#")
            processed = "".join(masked_val)
            df_masked.loc[index, attribute] = processed
    return df_masked