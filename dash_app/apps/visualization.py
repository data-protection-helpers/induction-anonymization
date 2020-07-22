import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash
import dash_table
import json
from app import app

import pandas as pd


div_graph1 = html.Div(
    [
        html.H2("Pearson Plot"),
        html.Div(
            [
                dcc.Graph(
                    id="pearson_init",
                    style={"textAlign": "center"},
                    figure={'data': [], 'layout': {'title': 'Initial dataframe'}}
                ),
                dcc.Graph(
                    id="pearson_gen",
                    style={"textAlign": "center"}
                )
            ],
            style={"display": "flex", "flex-direction": "row"}

        )

    ],
    style={"marginLeft": 300, "marginTop": 10, "width": "90%", "height": "550px", "display": "flex", "padding": "2rem",
           "flex-direction": "column", "align-items": "center", "background-color": "#f8f9fa"}
)

layout = html.Div(
    [
        div_graph1,

    ],
    style={"display": "flex", "flex-direction": "column"},
    id="results_layout"
)


@app.callback(
    Output("pearson_gen", "figure"),
    [Input("storage_pearson_graph_gen", "data")]
)
def store_generated_pearson_plot(data):
    if data is not None:
        return data
    return {'data': [], 'layout': {'title': 'Initial dataframe'}}

@app.callback(
    Output("pearson_init", "figure"),
    [Input("storage_pearson_graph_init", "data")]
)
def store_initial_pearson_plot(data):
    if data is not None:
        return data
    return {'data': [], 'layout': {'title': 'Initial dataframe'}}

