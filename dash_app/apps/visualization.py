import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash
import dash_table
import json
from app import app
import plotly.graph_objects as go
import plotly.express as px

import pandas as pd


df = pd.read_csv("../data/statistical-generative-modeling-sample.csv.bz2")
df = df[:100]

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
    style={"marginLeft": 300, "marginTop": 10, "width": "78%", "height": "550px", "display": "flex", "padding": "2rem",
           "flex-direction": "column", "align-items": "center", "background-color": "#f8f9fa"}
)

div_graph2 = html.Div(
    [
        html.H2("Scatter plots"),
        dash_table.DataTable(
            id="df_columns_scatter",
            column_selectable="multi",
            selected_columns=[],
            virtualization=True,
            style_table={"overflowX": "auto", "width": 700},

            style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"}
        ),

        html.Div(
            [
                dcc.Graph(
                    id="plot_graph_init",
                    style={"textAlign": "center"},
                ),
                dcc.Graph(
                    id="plot_graph_gen",
                    style={"textAlign": "center"}
                )
            ],
            style={"display": "flex", "flex-direction": "row"}

        )

    ],
    style={"marginLeft": 300, "marginTop": 10, "width": "78%", "height": "750px", "display": "flex", "padding": "2rem",
           "flex-direction": "column", "justify-content": "space-evenly", "align-items": "center", "background-color": "#f8f9fa"}
)


div_graph3 = html.Div(
    [
        html.H2("Distributions plot"),
        dash_table.DataTable(
            id="df_columns_distribution",
            column_selectable="single",
            selected_columns=[],
            virtualization=True,
            style_table={"overflowX": "auto", "width": 700},

            style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"}
        ),


        dcc.Graph(
            id="distr_graph",
            style={"textAlign": "center"},
        ),



    ],
    style={"marginLeft": 300, "marginTop": 10, "width": "78%", "height": "750px", "display": "flex", "padding": "2rem",
           "flex-direction": "column", "justify-content": "space-evenly", "align-items": "center", "background-color": "#f8f9fa"}
)



layout = html.Div(
    [
        div_graph1,
        div_graph2,
        div_graph3
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



@app.callback(
    [Output("df_columns_scatter", "columns"),
     Output("df_columns_distribution", "columns")],
    [Input("storage_sample_df", "data"),
     Input("storage_synth_attributes", "data")
    ]
)
def update_initial_table(jsonified_data, synth_attributes):
    if jsonified_data is not None:
        df_synth = pd.read_json(jsonified_data, orient="split")
        col_synth = [{"name": i, "id": i, "selectable": True} for i in df_synth.columns if i in synth_attributes],
        return col_synth[0], col_synth[0]
    return None, None

@app.callback(
    [Output("plot_graph_init", "figure"),
     Output("plot_graph_gen", "figure")],
    [Input("df_columns_scatter", "selected_columns"),
     Input("storage_generated_table_num", "data"),
     Input("storage_sample_df_num", "data"),
     Input("storage_types", "data"),]
)
def renders_plot(selected_columns, jsonified_data1, jsonified_data2, types):
    if jsonified_data1 is not None and jsonified_data2 is not None and selected_columns !=[]:
        df_gen_num = pd.read_json(jsonified_data1, orient="split")
        df_sample_num = pd.read_json(jsonified_data2, orient="split")

        if len(selected_columns) == 2:
            if types[selected_columns[0]] == "Categorical":
                attribute1 = selected_columns[0] + "_NUM"
            else:
                attribute1 = selected_columns[0]

            if types[selected_columns[1]] == "Categorical":
                attribute2 = selected_columns[1] + "_NUM"
            else:
                attribute2 = selected_columns[1]

            fig_init = px.scatter(df_sample_num, x=attribute1, y=attribute2, title="Initial dataframe")
            fig_gen = px.scatter(df_gen_num, x=attribute1, y=attribute2, title="Generated dataframe")

            return fig_init, fig_gen
    return {'data': [], 'layout': {}}, {'data': [], 'layout': {}}


@app.callback(
    Output("distr_graph", "figure"),
    [Input("df_columns_distribution", "selected_columns"),
     Input("storage_generated_table_num", "data"),
     Input("storage_sample_df_num", "data"),
     Input("storage_types", "data"),]
)
def renders_plot(selected_columns, jsonified_data1, jsonified_data2, types):
    if jsonified_data1 is not None and jsonified_data2 is not None and selected_columns !=[]:
        df_gen_num = pd.read_json(jsonified_data1, orient="split")
        df_sample_num = pd.read_json(jsonified_data2, orient="split")

        if types[selected_columns[0]] == "Categorical":
            attribute = selected_columns[0] + "_NUM"
        else:
            attribute = selected_columns[0]

        fig = go.Figure()
        fig.add_trace(go.Histogram(x=df_gen_num[attribute], name="Generated dataframe") )
        fig.add_trace(go.Histogram(x=df_sample_num[attribute], name="Initial dataframe"))

        fig.update_layout(barmode='overlay')

        fig.update_traces(opacity=0.75)

        return fig

    return {'data': [], 'layout': {}}


