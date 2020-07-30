import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash
import dash_table
import json
from app import app

import pandas as pd


# initial sample table
# smote tab
div_initial_smote = html.Div(
    [
        html.H3(
            "Initial dataframe",
            style={"textAlign": "center"}
        ),
        dash_table.DataTable(
            id="div_initial_SMOTE",
            virtualization=True,
            style_table={"height": "350px", "marginLeft": 70, "marginRight": 70, "width": 1500, "overflowY": "auto",
                         "overflowX": "auto"},
            style_data_conditional=[
                {
                    "if": {"row_index": "odd"},
                    "backgroundColor": "rgb(248, 248, 248)"},
                {"if": {"column_type": "numeric"},
                 "background_color": "#D2F3FF",
                 },
                {"if": {"column_type": "text"},
                 "background_color": "#d0f0c0",
                 },
                {"if": {"column_type": "datetime"},
                 "background_color": "#EAD8D7",
                 },
            ],
            style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"}
        )
    ],
    style={"height": "550px", "width": "90%","display": "flex",
           "flex-direction": "column", "justify-content": "space-evenly", "align-items": "center", "border-radius":
               "5px", "background-color": "#f9f9f9", "margin": "10px", "padding": "15px", "box-shadow": "2px 2px 2px "
                                                                                                        "lightgrey"},

)


# statistical tab
div_initial_stat = html.Div(
    [
        html.H3(
            "Initial dataframe",
            style={"textAlign": "center"}
        ),
        dash_table.DataTable(
            id="div_initial_STAT",
            virtualization=True,
            style_table={"height": "350px", "marginLeft": 70, "marginRight": 70, "width": 1500, "overflowY": "auto",
                         "overflowX": "auto"},
            style_data_conditional=[
                {
                    "if": {"row_index": "odd"},
                    "backgroundColor": "rgb(248, 248, 248)"},
                {"if": {"column_type": "numeric"},
                 "background_color": "#D2F3FF",
                 },
                {"if": {"column_type": "text"},
                 "background_color": "#d0f0c0",
                 },
                {"if": {"column_type": "datetime"},
                 "background_color": "#EAD8D7",
                 },
            ],
            style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"}
        )
    ],
    style={"height": "550px", "width": "90%", "display": "flex",
           "flex-direction": "column", "justify-content": "space-evenly", "align-items": "center", "border-radius":
               "5px", "background-color": "#f9f9f9", "margin": "10px", "padding": "15px", "box-shadow": "2px 2px 2px "
                                                                                                        "lightgrey"},
)


# generated sample table
# smote tab
div_generated_smote = html.Div(
    [
        html.H3(
            "Generated dataframe",
            style={"textAlign": "center"}
        ),

        dash_table.DataTable(
            id="generated_SMOTE",
            virtualization=True,
            style_table={"height": "350px", "marginLeft": 70, "marginRight": 70, "width": 1500, "overflowY": "auto",
                         "overflowX": "auto"},
            style_data_conditional=[
                {
                    "if": {"row_index": "odd"},
                    "backgroundColor": "rgb(248, 248, 248)"},
                {"if": {"column_type": "numeric"},
                 "background_color": "#D2F3FF",
                 },
                {"if": {"column_type": "text"},
                 "background_color": "#d0f0c0",
                 },
                {"if": {"column_type": "datetime"},
                 "background_color": "#EAD8D7",
                 },
            ],
            style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"}
        )
    ],
    style={"height": "550px", "width": "90%", "display": "flex", "flex-direction": "column", "justify-content":
           "space-evenly", "align-items": "center", "border-radius": "5px", "background-color": "#f9f9f9", "margin":
           "10px", "padding": "15px", "box-shadow": "2px 2px 2px lightgrey"},
)


# statistical tab
div_generated_stat = html.Div(
    [
        html.H3(
            "Generated dataframe",
            style={"textAlign": "center"}
        ),
        dash_table.DataTable(
            id="generated_STAT",
            virtualization=True,
            style_table={"height": "350px", "marginLeft": 70, "marginRight": 70, "width": 1500, "overflowY": "auto",
                         "overflowX": "auto"},
            style_data_conditional=[
                {
                    "if": {"row_index": "odd"},
                    "backgroundColor": "rgb(248, 248, 248)"},
                {"if": {"column_type": "numeric"},
                 "background_color": "#D2F3FF",
                 },
                {"if": {"column_type": "text"},
                 "background_color": "#d0f0c0",
                 },
                {"if": {"column_type": "datetime"},
                 "background_color": "#EAD8D7",
                 },

            ],
            style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"}
        )
    ],
    style={"height": "550px", "width": "90%", "display": "flex",
           "flex-direction": "column", "justify-content": "space-evenly", "align-items": "center", "border-radius":
               "5px", "background-color": "#f9f9f9", "margin": "10px", "padding": "15px", "box-shadow": "2px 2px 2px "
                                                                                                        "lightgrey"}
)


# tab to display results from the two techniques in parallel
div_tab = html.Div(
    [
        dcc.Tabs(
            [
                dcc.Tab(
                    [
                        div_initial_stat,
                        div_generated_stat
                    ],
                    label='Statistical anonymization',
                    value='stat_tech',

                ),
                dcc.Tab(
                    [
                        div_initial_smote,
                        div_generated_smote
                    ],
                    label='Smote anonymization',
                    value='smote_tech',
                ),

            ],
            value='stat_tech',
            style={"width": 500, "marginLeft": 10}
        )
    ],
    id="div_graph1"
)


# initial sample df if no synthesization
div_initial_simple = html.Div(
    [
        html.H3(
            "Initial dataframe",
            style={"textAlign": "center"}
        ),

        dash_table.DataTable(
            id="div_initial_simple",
            virtualization=True,
            style_table={"height": "350px", "marginLeft": 70, "marginRight": 70, "width": 1500, "overflowY": "auto",
                         "overflowX": "auto"},
            style_data_conditional=[
                {
                    "if": {"row_index": "odd"},
                    "backgroundColor": "rgb(248, 248, 248)"},
                {"if": {"column_type": "numeric"},
                 "background_color": "#D2F3FF",
                 },
                {"if": {"column_type": "text"},
                 "background_color": "#d0f0c0",
                 },
                {"if": {"column_type": "datetime"},
                 "background_color": "#EAD8D7",
                 },
            ],
            style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"}
        )
    ],
    style={"height": "550px", "width": "90%","display": "flex",
           "flex-direction": "column", "justify-content": "space-evenly", "align-items": "center", "border-radius":
               "5px", "background-color": "#f9f9f9", "margin": "10px", "padding": "15px", "box-shadow": "2px 2px 2px "
                                                                                                        "lightgrey"},
)

# generated sample df if no synthesization
div_generated_simple = html.Div(
    [
        html.H3(
            "Generated dataframe",
            style={"textAlign": "center"}
        ),
        dash_table.DataTable(
            id="div_generated_simple",

            virtualization=True,
            style_table={"height": "350px", "marginLeft": 70, "marginRight": 70, "width": 1500, "overflowY": "auto",
                         "overflowX": "auto"},
            style_data_conditional=[
                {
                    "if": {"row_index": "odd"},
                    "backgroundColor": "rgb(248, 248, 248)"},
                {"if": {"column_type": "numeric"},
                 "background_color": "#D2F3FF",
                 },
                {"if": {"column_type": "text"},
                 "background_color": "#d0f0c0",
                 },
                {"if": {"column_type": "datetime"},
                 "background_color": "#EAD8D7",
                 },

            ],
            style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"}
        )
    ],
    style={"height": "550px", "width": "90%", "display": "flex",
           "flex-direction": "column", "justify-content": "space-evenly", "align-items": "center", "border-radius":
               "5px", "background-color": "#f9f9f9", "margin": "10px", "padding": "15px", "box-shadow": "2px 2px 2px "
                                                                                                        "lightgrey"},
)

layout = html.Div(
    [
        div_tab
    ],
    style={"display": "flex", "flex-direction": "column", "marginLeft": 300, "marginTop": 10},
    id="results_layout"
)




# returns initial sample dataframe
# both smote and statistical tabs
@app.callback(
    [Output("div_initial_SMOTE", "columns"),
     Output("div_initial_SMOTE", "data"),
     Output("div_initial_STAT", "columns"),
     Output("div_initial_STAT", "data")],
    [Input("storage_sample_df", "data")]
)
def update_reduced_table(jsonified_sample_df):
    if jsonified_sample_df is not None:
        df_sample = pd.read_json(jsonified_sample_df, orient="split")
        col = [{"name": i, "id": i, "selectable": True} for i in df_sample]
        return col, df_sample[:100].to_dict('records'), col, df_sample[:100].to_dict('records')
    return None, None, None, None


# displays generated dataframe
# smote tab
@app.callback(
    [Output("generated_SMOTE", "columns"),
     Output("generated_SMOTE", "data")],
    [Input("storage_whole_generated_table_SMOTE", "data")]
)
def displays_generated_table_smote(jsonified_whole_df):
    if jsonified_whole_df is not None:
        df_gen = pd.read_json(jsonified_whole_df, orient="split")
        col_gen = [{"name": i, "id": i, "selectable": True} for i in df_gen.columns]
        return col_gen, df_gen.to_dict("records")
    return None, None

# statistical tab
@app.callback(
    [Output("generated_STAT", "columns"),
     Output("generated_STAT", "data")],
    [Input("storage_whole_generated_table_STAT", "data")]
)
def update_initial_table(jsonified_whole_df):
    if jsonified_whole_df is not None:
        df_gen = pd.read_json(jsonified_whole_df, orient="split")
        col_gen = [{"name": i, "id": i, "selectable": True} for i in df_gen.columns]
        return col_gen, df_gen.to_dict("records")
    return None, None





@app.callback(
    [Output("div_generated_simple", "columns"),
     Output("div_generated_simple", "data")],
    [Input("storage_whole_generated_table", "data")]
)
def displays_results_no_synthesization(jsonified_data):
    if jsonified_data is not None:
        df_gen = pd.read_json(jsonified_data, orient="split")
        col_gen = [{"name": i, "id": i, "selectable": True} for i in df_gen.columns]
        return col_gen, df_gen.to_dict("records")

@app.callback(
    [Output("div_initial_simple", "columns"),
     Output("div_initial_simple", "data")],
    [Input("storage_sample_df", "data")]
)
def displays_results_no_synthesization(jsonified_sample_df):
    if jsonified_sample_df is not None:
        df_sample_df = pd.read_json(jsonified_sample_df, orient="split")
        col_gen = [{"name": i, "id": i, "selectable": True} for i in df_sample_df.columns]
        return col_gen, df_sample_df.to_dict("records")

@app.callback(
     Output("results_layout", "children"),
    [Input("storage_whole_generated_table", "data")]
)
def displays_results_no_synthesization(jsonified_data):
    if jsonified_data is not None:
        return html.Div(
            [
                div_initial_simple,
                div_generated_simple
            ],
            style={"display": "flex", "flex-direction": "column", "marginLeft": 10, "marginTop": 10},
            id="results_layout_simple"
        )
    return div_tab



