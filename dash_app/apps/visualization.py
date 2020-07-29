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

                ),
                dcc.Graph(
                    id="pearson_gen",
                    style={"textAlign": "center"}
                )
            ],
            style={"display": "flex", "flex-direction": "row"}
        )
    ],
    style={"height": "550px", "display": "flex", "flex-direction": "column", "align-items": "center", "border-radius":
           "5px", "background-color": "#f9f9f9", "margin": "10px", "padding": "15px", "box-shadow": "2px 2px 2px "
                                                                                                    "lightgrey"},
    id="div_graph1"
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

            style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold", 'padding-left': '20px'}
        ),
        html.Div(
            [
                dcc.Graph(
                    id="scatter_graph_init",
                    style={"textAlign": "center"},
                ),
                dcc.Graph(
                    id="scatter_graph_gen",
                    style={"textAlign": "center"}
                )
            ],
            style={"display": "flex", "flex-direction": "row"}
        )
    ],
    style={"height": "750px", "display": "flex", "flex-direction": "column", "justify-content": "space-evenly",
           "align-items": "center", "border-radius": "5px", "background-color": "#f9f9f9", "margin": "10px", "padding":
           "15px", "box-shadow": "2px 2px 2px lightgrey"},
    id="div_graph2"
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

            style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold", 'padding-left': '20px'}
        ),
        dcc.Graph(
            id="distr_graph",
            style={"textAlign": "center"},
        ),
    ],
    style={"height": "750px", "display": "flex",
           "flex-direction": "column", "justify-content": "space-evenly", "align-items": "center", "border-radius":
               "5px", "background-color": "#f9f9f9", "margin": "10px", "padding": "15px", "box-shadow": "2px 2px 2px "
                                                                                                        "lightgrey"},
    id="div_graph3"
)


layout = html.Div(
    [
        div_graph1,
        div_graph2,
        div_graph3
    ],
    style={"display": "flex", "flex-direction": "column", "marginLeft": 300, "marginTop": 10,},
    id="results_layout"
)

# displays pearson plot of generated data
@app.callback(
    Output("pearson_gen", "figure"),
    [Input("storage_pearson_graph_gen", "data")]
)
def displays_generated_pearson_plot(data):
    if data is not None:
        return data
    return {'data': [], 'layout': {'title': 'Initial dataframe'}}


# displays pearson plot of initial data
@app.callback(
    Output("pearson_init", "figure"),
    [Input("storage_pearson_graph_init", "data")]
)
def displays_initial_pearson_plot(data):
    if data is not None:
        return data
    return {'data': [], 'layout': {'title': 'Initial dataframe'}}



@app.callback(
    [Output("div_graph1", "style"),
     Output("div_graph2", "style"),
     Output("div_graph3", "style")],
    [Input("storage_synth_attributes", "data")]
)
def undisplays_graphs(synth_attributes):
    if len(synth_attributes) == 1:
        return {"display": "none"}, {"display": "none"}, {"height": "750px", "display": "flex",
           "flex-direction": "column", "justify-content": "space-evenly", "align-items": "center", "border-radius":
               "5px", "background-color": "#f9f9f9", "margin": "10px", "padding": "15px", "box-shadow": "2px 2px 2px "
                                                                                                        "lightgrey"}
    elif len(synth_attributes) == 0:
        return {"display": "none"}, {"display": "none"}, {"display": "none"}

    return {"height": "550px", "display": "flex", "flex-direction": "column", "align-items": "center", "border-radius":
            "5px", "background-color": "#f9f9f9", "margin": "10px", "padding": "15px", "box-shadow": "2px 2px 2px "
            "lightgrey"},\
           {"height": "750px", "display": "flex", "flex-direction": "column", "justify-content": "space-evenly",
            "align-items": "center", "border-radius": "5px", "background-color": "#f9f9f9", "margin": "10px", "padding":
            "15px", "box-shadow": "2px 2px 2px lightgrey"}, \
           {"height": "750px", "display": "flex", "flex-direction": "column", "justify-content": "space-evenly",
            "align-items": "center", "border-radius": "5px", "background-color": "#f9f9f9", "margin": "10px", "padding":
            "15px", "box-shadow": "2px 2px 2px lightgrey"}



# used to have synthetic attributes names as headers of dataframes to be selected for plot display
@app.callback(
    [Output("df_columns_scatter", "columns"),
     Output("df_columns_distribution", "columns"),
     Output("df_columns_scatter", "selected_columns"),
     Output("df_columns_distribution", "selected_columns")],
    [Input("storage_sample_df", "data"),
     Input("storage_synth_attributes", "data")]
)
def updates_headers(jsonified_df_sample, synth_attributes):
    if jsonified_df_sample is not None:
        df_sample = pd.read_json(jsonified_df_sample, orient="split")
        col_synth = [{"name": i, "id": i, "selectable": True} for i in df_sample.columns if i in synth_attributes]
        if len(col_synth) >= 2:
            return col_synth, col_synth, [col_synth[0]["name"], col_synth[1]["name"]], [col_synth[0]["name"]]
        elif len(col_synth) == 1:
            return col_synth, col_synth, [], [col_synth[0]["name"]]
        else:
            return col_synth, col_synth, None, None
    return None, None, None, None


# computes scatter plots
@app.callback(
    [Output("scatter_graph_init", "figure"),
     Output("scatter_graph_gen", "figure")],
    [Input("df_columns_scatter", "selected_columns"),
     Input("storage_synthetic_table_num", "data"),
     Input("storage_sample_synth_df_num", "data"),
     Input("storage_types", "data")]
)
def renders_plot(selected_columns, jsonified_gen_synth_num, jsonified_sample_synth_num, types):
    if jsonified_gen_synth_num is not None and jsonified_sample_synth_num is not None and selected_columns !=[]:
        df_gen_synth_num = pd.read_json(jsonified_gen_synth_num, orient="split")
        df_sample_synth_num = pd.read_json(jsonified_sample_synth_num, orient="split")

        if len(selected_columns) == 2:
            if types[selected_columns[0]] == "Categorical":
                attribute1 = selected_columns[0] + "_NUM"
            else:
                attribute1 = selected_columns[0]

            if types[selected_columns[1]] == "Categorical":
                attribute2 = selected_columns[1] + "_NUM"
            else:
                attribute2 = selected_columns[1]

            fig_init = px.scatter(df_sample_synth_num, x=attribute1, y=attribute2, title="Initial dataframe")
            fig_gen = px.scatter(df_gen_synth_num, x=attribute1, y=attribute2, title="Generated dataframe")

            return fig_init, fig_gen
    return {'data': [], 'layout': {}}, {'data': [], 'layout': {}}


# computes distribution plot
@app.callback(
    Output("distr_graph", "figure"),
    [Input("df_columns_distribution", "selected_columns"),
     Input("storage_synthetic_table_num", "data"),
     Input("storage_sample_synth_df_num", "data"),
     Input("storage_types", "data")]
)
def renders_plot(selected_columns, jsonified_gen_synth_num, jsonified_sample_synth_num, types):
    if jsonified_gen_synth_num is not None and jsonified_sample_synth_num is not None and selected_columns != []:
        df_gen_synth_num = pd.read_json(jsonified_gen_synth_num, orient="split")
        df_sample_synth_num = pd.read_json(jsonified_sample_synth_num, orient="split")

        if types[selected_columns[0]] == "Categorical":
            attribute = selected_columns[0] + "_NUM"
        else:
            attribute = selected_columns[0]

        fig = go.Figure()
        fig.add_trace(go.Histogram(x=df_gen_synth_num[attribute], name="Generated dataframe") )
        fig.add_trace(go.Histogram(x=df_sample_synth_num[attribute], name="Initial dataframe"))

        fig.update_layout(barmode='overlay')
        fig.update_traces(opacity=0.75)

        return fig

    return {'data': [], 'layout': {}}


