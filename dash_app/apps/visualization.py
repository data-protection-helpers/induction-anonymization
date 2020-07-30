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
from statistical_generation import treatment_statistical
from smote import treatment, numerical_data
from swapping import swap
from masking import complete_masking
import pandas as pd


div_graph1_smote = html.Div(
    [
        html.H2("Pearson Plot"),
        html.Div(
            [
                dcc.Graph(
                    id="pearson_init_SMOTE",
                    style={"textAlign": "center"},
                ),
                dcc.Graph(
                    id="pearson_gen_SMOTE",
                    style={"textAlign": "center"}
                )
            ],
            style={"display": "flex", "flex-direction": "row"}
        ),
    ],
    style={"display": "none"},
    id="div_graph1_SMOTE"
)

div_graph1_stat = html.Div(
    [
        html.H2("Pearson Plot"),
        html.Div(
            [
                dcc.Graph(
                    id="pearson_init_STAT",
                    style={"textAlign": "center"},
                ),
                dcc.Graph(
                    id="pearson_gen_STAT",
                    style={"textAlign": "center"}
                )
            ],
            style={"display": "flex", "flex-direction": "row"}
        ),
    ],
    style={"display": "none"},
    id="div_graph1_STAT"
)


div_graph2_smote = html.Div(
    [
        html.H2("Scatter plots"),
        dash_table.DataTable(
            id="df_columns_scatter_SMOTE",
            column_selectable="multi",
            selected_columns=[],
            virtualization=True,
            style_table={"overflowX": "auto", "width": 700},

            style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold", 'padding-left': '20px', 'padding-right': '20px'}
        ),
        html.Div(
            [
                dcc.Graph(
                    id="scatter_graph_init_SMOTE",
                    style={"textAlign": "center"},
                ),
                dcc.Graph(
                    id="scatter_graph_gen_SMOTE",
                    style={"textAlign": "center"}
                )
            ],
            style={"display": "flex", "flex-direction": "row"}
        )
    ],
    style={"display": "none"},
    id="div_graph2_SMOTE"
)

div_graph2_stat = html.Div(
    [
        html.H2("Scatter plots"),
        dash_table.DataTable(
            id="df_columns_scatter_STAT",
            column_selectable="multi",
            selected_columns=[],
            virtualization=True,
            style_table={"overflowX": "auto", "width": 700},

            style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold", 'padding-left': '20px', 'padding-right': '20px'}
        ),
        html.Div(
            [
                dcc.Graph(
                    id="scatter_graph_init_STAT",
                    style={"textAlign": "center"},
                ),
                dcc.Graph(
                    id="scatter_graph_gen_STAT",
                    style={"textAlign": "center"}
                )
            ],
            style={"display": "flex", "flex-direction": "row"}
        )
    ],
    style={"display": "none"},
    id="div_graph2_STAT"
)


div_graph3_smote = html.Div(
    [
        html.H2("Distributions plot"),
        dash_table.DataTable(
            id="df_columns_distribution_SMOTE",
            column_selectable="single",
            selected_columns=[],
            virtualization=True,
            style_table={"overflowX": "auto", "width": 700},

            style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold", 'padding-left': '20px'}
        ),
        dcc.Graph(
            id="distr_graph_SMOTE",
            style={"textAlign": "center"},
        ),
    ],
    style={"display": "none"},
    id="div_graph3_SMOTE"
)

div_graph3_stat = html.Div(
    [
        html.H2("Distributions plot"),
        dash_table.DataTable(
            id="df_columns_distribution_STAT",
            column_selectable="single",
            selected_columns=[],
            virtualization=True,
            style_table={"overflowX": "auto", "width": 700},

            style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold", 'padding-left': '20px'}
        ),
        dcc.Graph(
            id="distr_graph_STAT",
            style={"textAlign": "center"},
        ),
    ],
    style={"display": "none"},
    id="div_graph3_STAT"
)

div_tab = html.Div(
    [
        dcc.Tabs(
            [
                dcc.Tab(
                    label='Statistical technique',
                    value='stat_tech',
                    children=html.Div(
                        [
                            div_graph1_stat,
                            div_graph2_stat,
                            div_graph3_stat
                        ],
                        className='control-tab',
                    )
                ),
                dcc.Tab(
                    label='Smote',
                    value='smote_tech',
                    children=html.Div(
                        [
                            div_graph1_smote,
                            div_graph2_smote,
                            div_graph3_smote
                        ],
                        className='control-tab',
                    ),
                    style={"width": 300}
                ),
            ],
            value='stat_tech',
            style={"width": 500, "marginLeft": 10}

        )
    ],
    id="div_graph1"
)


layout = html.Div(
    [
        div_tab,
    ],
    style={"display": "flex", "flex-direction": "column", "marginLeft": 300, "marginTop": 10},
    id="viz_layout"
)

# displays pearson plot of generated data
@app.callback(
    Output("pearson_gen_SMOTE", "figure"),
    [Input("storage_pearson_gen_SMOTE", "data")]
)
def displays_generated_pearson_plot(data):
    if data is not None:
        return data
    return {'data': [], 'layout': {'title': 'Generated dataframe'}}

@app.callback(
    Output("pearson_gen_STAT", "figure"),
    [Input("storage_pearson_gen_STAT", "data")]
)
def displays_generated_pearson_plot(data):
    if data is not None:
        return data
    return {'data': [], 'layout': {'title': 'Generated dataframe'}}


# displays pearson plot of initial data
@app.callback(
    [Output("pearson_init_SMOTE", "figure"),
     Output("pearson_init_STAT", "figure")],
    [Input("storage_pearson_init", "data")]
)
def displays_initial_pearson_plot(data):
    if data is not None:
        return data, data
    return {'data': [], 'layout': {'title': 'Initial dataframe'}}, {'data': [], 'layout': {'title': 'Initial dataframe'}}



@app.callback(
    [Output("div_graph1_SMOTE", "style"),
     Output("div_graph2_SMOTE", "style"),
     Output("div_graph3_SMOTE", "style")],
    [Input("storage_synth_attributes", "data")]
)
def undisplays_graphs1(synth_attributes):

    if synth_attributes is None or len(synth_attributes) == 0:
        return {"display": "none"}, {"display": "none"}, {"display": "none"}

    elif len(synth_attributes) == 1:
        return {"display": "none"}, {"display": "none"}, {"height": "550px", "display": "flex",
                                                          "flex-direction": "column", "justify-content": "space-evenly",
                                                          "align-items": "center", "border-radius": "5px",
                                                          "background-color": "#f9f9f9", "margin": "10px", "padding":
                                                          "15px", "box-shadow": "2px 2px 2px lightgrey"}

    else:
        return {"height": "550px", "display": "flex", "flex-direction": "column", "justify-content": "space-evenly",
                "align-items": "center", "border-radius": "5px", "background-color": "#f9f9f9", "margin": "10px",
                "padding": "15px", "box-shadow": "2px 2px 2px lightgrey"}, \
               {"height": "550px", "display": "flex", "flex-direction": "column", "justify-content": "space-evenly",
                "align-items": "center", "border-radius": "5px", "background-color": "#f9f9f9", "margin": "10px",
                "padding": "15px", "box-shadow": "2px 2px 2px lightgrey"}, \
               {"height": "550px", "display": "flex", "flex-direction": "column", "justify-content": "space-evenly",
                "align-items": "center", "border-radius": "5px", "background-color": "#f9f9f9", "margin": "10px",
                "padding": "15px", "box-shadow": "2px 2px 2px lightgrey"}, \



@app.callback(
    [Output("div_graph1_STAT", "style"),
     Output("div_graph2_STAT", "style"),
     Output("div_graph3_STAT", "style")],
    [Input("storage_synth_attributes", "data")]
)
def undisplays_graphs2(synth_attributes):
    if synth_attributes is None or len(synth_attributes) == 0:
        return {"display": "none"}, {"display": "none"}, {"display": "none"}
    elif len(synth_attributes) == 1:
        return {"display": "none"}, {"display": "none"}, {"height": "550px", "display": "flex",
                                                          "flex-direction": "column", "justify-content": "space-evenly",
                                                          "align-items": "center", "border-radius": "5px",
                                                          "background-color": "#f9f9f9", "margin": "10px", "padding":
                                                              "15px", "box-shadow": "2px 2px 2px lightgrey"}
    else:
        return {"height": "550px", "display": "flex", "flex-direction": "column", "justify-content": "space-evenly",
                "align-items": "center", "border-radius": "5px", "background-color": "#f9f9f9", "margin": "10px",
                "padding": "15px", "box-shadow": "2px 2px 2px lightgrey"}, \
               {"height": "550px", "display": "flex", "flex-direction": "column", "justify-content": "space-evenly",
                "align-items": "center", "border-radius": "5px", "background-color": "#f9f9f9", "margin": "10px",
                "padding": "15px", "box-shadow": "2px 2px 2px lightgrey"}, \
               {"height": "550px", "display": "flex", "flex-direction": "column", "justify-content": "space-evenly",
                "align-items": "center", "border-radius": "5px", "background-color": "#f9f9f9", "margin": "10px",
                "padding": "15px", "box-shadow": "2px 2px 2px lightgrey"}, \


# used to have synthetic attributes names as headers of dataframes to be selected for plot display
@app.callback(
    [Output("df_columns_scatter_SMOTE", "columns"),
     Output("df_columns_distribution_SMOTE", "columns"),
     Output("df_columns_scatter_SMOTE", "selected_columns"),
     Output("df_columns_distribution_SMOTE", "selected_columns")],
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

@app.callback(
    [Output("df_columns_scatter_STAT", "columns"),
     Output("df_columns_distribution_STAT", "columns"),
     Output("df_columns_scatter_STAT", "selected_columns"),
     Output("df_columns_distribution_STAT", "selected_columns")],
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
    [Output("scatter_graph_init_SMOTE", "figure"),
     Output("scatter_graph_gen_SMOTE", "figure")],
    [Input("df_columns_scatter_SMOTE", "selected_columns"),
     Input("storage_synthetic_table_num_SMOTE", "data"),
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

@app.callback(
    [Output("scatter_graph_init_STAT", "figure"),
     Output("scatter_graph_gen_STAT", "figure")],
    [Input("df_columns_scatter_STAT", "selected_columns"),
     Input("storage_synthetic_table_num_STAT", "data"),
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
    Output("distr_graph_SMOTE", "figure"),
    [Input("df_columns_distribution_SMOTE", "selected_columns"),
     Input("storage_synthetic_table_num_SMOTE", "data"),
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

@app.callback(
    Output("distr_graph_STAT", "figure"),
    [Input("df_columns_distribution_STAT", "selected_columns"),
     Input("storage_synthetic_table_num_STAT", "data"),
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



@app.callback(
    [Output("storage_pearson_gen_SMOTE", "data"),
     Output("storage_pearson_init", "data"),
     Output("storage_synthetic_table_cat_SMOTE", "data"),
     Output("storage_synthetic_table_num_SMOTE", "data"),
     Output("storage_sample_synth_df_num", "data")],
    [Input("storage_main_classification_button", "data")],
    [State("storage_synth_attributes", "data"),
     State("storage_types", "data"),
     State("storage_sample_df", "data")]
)
def stores_generated_df_information(data, synth_attributes, types, jsonified_df_sample):
    if jsonified_df_sample is not None and synth_attributes is not None and len(synth_attributes) > 0 and types is not None and types != {}:
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


        return pearson_synth_gen, pearson_synth_init, df_gen_synth_cat.to_json(date_format="iso", orient="split"), \
            df_gen_synth_num.to_json(date_format="iso", orient="split"), df_sample_synth_num.to_json(
            date_format="iso", orient="split")

    return None, None, None, None, None


@app.callback(
    [Output("storage_pearson_gen_STAT", "data"),
     Output("storage_synthetic_table_cat_STAT", "data"),
     Output("storage_synthetic_table_num_STAT", "data")],
    [Input("storage_main_classification_button", "data")],
    [State("storage_synth_attributes", "data"),
     State("storage_types", "data"),
     State("storage_sample_df", "data")]
)
def stores_generated_df_information(data, synth_attributes, types, jsonified_df_sample):
    if jsonified_df_sample is not None and synth_attributes is not None and len(synth_attributes) > 0 and types is not None and types != {}:
        df_sample = pd.read_json(jsonified_df_sample, orient="split")
        categorical_columns = []

        # synthesization: pearson plots and a synthetic dataframe are created
        for col in synth_attributes:
            if types[col] == "Categorical":
                categorical_columns.append(col)

        pearson_synth_gen, pearson_synth_init, df_gen_synth_cat, df_gen_synth_num, df_sample_synth_num = \
            treatment_statistical(df_sample[synth_attributes], categorical_columns)


        return pearson_synth_gen,  df_gen_synth_cat.to_json(date_format="iso", orient="split"), df_gen_synth_num.to_json(date_format="iso", orient="split")


    return None, None, None


@app.callback(
    [Output("storage_whole_generated_table_SMOTE", "data"),
     Output("storage_whole_generated_table_STAT", "data"),
     Output("storage_whole_generated_table", "data")],
    [Input("storage_synthetic_table_cat_SMOTE", "data"),
     Input("storage_synthetic_table_cat_STAT", "data")],
    [State("storage_swap_attributes", "data"),
     State("storage_mask_attributes", "data"),
     State("storage_sample_df", "data")]
)
def builds_final_dataframes(jsonified_df_gen_synth_cat_SMOTE, jsonified_df_gen_synth_cat_STAT, swap_attributes,
                            mask_attributes, jsonified_df_sample):
    if jsonified_df_sample is not None:

        df_sample = pd.read_json(jsonified_df_sample, orient="split")

        if jsonified_df_gen_synth_cat_SMOTE is not None and jsonified_df_gen_synth_cat_STAT is not None:

            df_gen_synth_cat_SMOTE = pd.read_json(jsonified_df_gen_synth_cat_SMOTE, orient="split")
            df_gen_synth_cat_STAT = pd.read_json(jsonified_df_gen_synth_cat_STAT, orient="split")
            # we add initial columns for swapping and masking attributes to the synthetic generated dataframe
            table = pd.DataFrame()

            for attribute in swap_attributes + mask_attributes:
                table[attribute] = df_sample[attribute]

            # swapping: attributes with swapping technique are shuffled randomly
            table_swapped = swap(table, swap_attributes)

            # complete masking: each row of the attributes with masking technique is completely masked
            table_swapped_masked = complete_masking(table_swapped, mask_attributes)

            whole_table_SMOTE = pd.concat([df_gen_synth_cat_SMOTE, table_swapped_masked], axis=1)
            whole_table_STAT = pd.concat([df_gen_synth_cat_STAT, table_swapped_masked], axis=1)

            return whole_table_SMOTE.to_json(date_format="iso", orient="split"), whole_table_STAT.to_json(date_format=
                                                                                                          "iso", orient=
                                                                                                          "split"), None
        else:

            table = pd.DataFrame()

            for attribute in swap_attributes + mask_attributes:
                table[attribute] = df_sample[attribute]

            # swapping: attributes with swapping technique are shuffled randomly
            table_swapped = swap(table, swap_attributes)

            # complete masking: each row of the attributes with masking technique is completely masked
            table_swapped_masked = complete_masking(table_swapped, mask_attributes)
            return None, None, table_swapped_masked.to_json(date_format="iso", orient="split")
    return None, None, None
