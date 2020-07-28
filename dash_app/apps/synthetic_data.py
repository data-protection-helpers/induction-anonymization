import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import pandas as pd
from app import app
from smote import treatment, numerical_data
from swapping import swap
from masking import complete_masking
import plotly.graph_objects as go
import dash

df = pd.read_csv("../data/statistical-generative-modeling-sample.csv.bz2")
df = df[:100]

div_content_synth = html.Div(
    [
        html.H3("Select the synthesization technique:", id="titre1", style={"textAlign": "center"}),
        html.Div(
            [
                html.Div(
                    [
                        html.H2("SMOTE", style={"textAlign": "center"}),
                        html.P(
                            """Donec id elit non mi porta gravida at eget metus.Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentumnibh, ut fermentum massa justo sit amet risus. Etiam porta semmalesuada magna mollis euismod. Donec sed odio dui. Donec id elit nonmi porta gravida at eget metus. Fusce dapibus, tellus ac cursuscommodo, tortor mauris condimentum nibh, ut fermentum massa justo sitamet risus. Etiam porta sem malesuada magna mollis euismod. Donec sedodio dui."""),
                        html.Div(
                            [
                                dbc.Button(id="smote_button", n_clicks=0, children="Synthesize", color="secondary",
                                           href="/results"),
                            ],
                            style={"display": "flex", "flex-direction": "column", "align-items": "center"}
                        ),
                    ],
                    style={"display": "flex", "flex-direction": "column", "width": 650}),

                html.Div(
                    [
                        html.H2("Statistical generative model", style={"textAlign": "center"}),
                        html.P(
                            """Donec id elit non mi porta gravida at eget metus.Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentumnibh, ut fermentum massa justo sit amet risus. Etiam porta semmalesuada magna mollis euismod. Donec sed odio dui. Donec id elit nonmi porta gravida at eget metus. Fusce dapibus, tellus ac cursuscommodo, tortor mauris condimentum nibh, ut fermentum massa justo sitamet risus. Etiam porta sem malesuada magna mollis euismod. Donec sedodio dui."""),
                    ],
                    style={"display": "flex", "flex-direction": "column", "width": 650}),
            ],
            style={"display": "flex", "flex-direction": "row", "justify-content": "space-around"}),
    ],
    style={"display": "flex", "flex-direction": "column"}
)

layout = html.Div(
    [
        html.H3("", id="titre", style={"textAlign": "center"}),
        div_content_synth,
    ],
    style={"marginTop": 30, "marginLeft": 300, "width": "100%", "height": "100%", "padding": "1rem 1rem", "flex"
                                                                                                          "-direction":
           "column", "background-color": "#f8f9fa", "display": "flex"})


@app.callback(
    [Output("storage_pearson_graph_gen", "data"),
     Output("storage_pearson_graph_init", "data"),
     Output("storage_synthetic_table_cat", "data"),
     Output("storage_synthetic_table_num", "data"),
     Output("storage_sample_synth_df_num", "data"),
     Output("storage_whole_generated_table", "data")],
    [Input("smote_button", "n_clicks")],
    [State("storage_swap_attributes", "data"),
     State("storage_mask_attributes", "data"),
     State("storage_synth_attributes", "data"),
     State("storage_types", "data"),
     State("storage_sample_df", "data")]
)
def stores_generated_df_information(n_clicks, swap_attributes, mask_attributes, synth_attributes, types,
                                    jsonified_df_sample):
    
    if jsonified_df_sample is not None and synth_attributes is not None and types is not None:
        df_sample = pd.read_json(jsonified_df_sample, orient="split")
        categorical_columns = []

        # synthesization: pearson plots and a synthetic dataframe are created
        for col in synth_attributes:
            if types[col] == "Categorical":
                categorical_columns.append(col)

        df_gen_synth_num, df_sample_synth_num, transitional_dfs = numerical_data(df_sample[synth_attributes],
                                                                                 categorical_columns)
        pearson_synth_gen, pearson_synth_init, df_gen_synth_cat = treatment(df_gen_synth_num, df_sample_synth_num,
                                                                            transitional_dfs, categorical_columns)

        # we add initial columns for swapping and masking attributes to the synthetic generated dataframe
        table = df_gen_synth_cat.copy()
        for attribute in swap_attributes + mask_attributes:
            table[attribute] = df_sample[attribute]

        # swapping: attributes with swapping technique are shuffled randomly
        table_swapped = swap(table, swap_attributes)

        # complete masking: each row of the attributes with masking technique is completely masked
        whole_table = complete_masking(table_swapped, mask_attributes)

        return pearson_synth_gen, pearson_synth_init, df_gen_synth_cat.to_json(date_format="iso", orient="split"), \
            df_gen_synth_num.to_json(date_format="iso", orient="split"), df_sample_synth_num.to_json(
            date_format="iso", orient="split"), whole_table.to_json(date_format="iso", orient="split")

    return None, None, None, None, None, None
