import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import pandas as pd
from app import app
from smote import treatment
import plotly.graph_objects as go
import dash



df = pd.read_csv("../data/statistical-generative-modeling-sample.csv.bz2")
df = df[:500]

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
                                dbc.Button(id="smote_button", n_clicks=0, children="Synthesize", color="secondary", href="/results"),
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
           "-direction": "column", "background-color": "#f8f9fa", "display": "flex"}
)



@app.callback(
    [Output("storage_pearson_graph_gen", "data"),
     Output("storage_pearson_graph_init", "data"),
     Output("storage_generated_table", "data")],
    [Input("smote_button", "n_clicks"),
     Input("storage_synth_col", "data"),
     Input("storage_types", "data"),
     Input("storage_sample_df", "data")]
)
def store_generated_df_information(n_clicks, data, types, jsonified_cleaned_data):
    if n_clicks != 0:
        df_sample = pd.read_json(jsonified_cleaned_data, orient="split")

        categorical_columns = []
        for col in data:
            if types[col] == "Categorical":
                categorical_columns.append(col)
        fig_gen, fig_init, df_gen = treatment(df_sample[data], categorical_columns)

        return fig_gen, fig_init, df_gen.to_json(date_format="iso", orient="split")
    return None, None, None



