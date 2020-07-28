import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash
import dash_table
import json
from app import app

import pandas as pd


df = pd.read_csv("../data/statistical-generative-modeling-sample.csv.bz2")
df = df[:100]


div_initial = html.Div(
    [
        html.H3(
            "Initial dataframe",
            style={"textAlign": "center"}
        ),

        dash_table.DataTable(
            id="initial_table_res",
            data=df.to_dict("records"),
            virtualization=True,
            style_table={"height": "350px", "marginLeft": 70, "marginRight": 70, "width": 1500, "overflowY": "auto",
                         "overflowX": "auto"},
            style_cell_conditional=[{"if": {"column_id": c}, "textAlign": "left"} for c in ["Date", "Region"]],
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
    style={"marginTop": 10, "marginLeft": 300,  "width": "78%", "height": "550px", "padding": "2rem", "display": "flex",
           "flex-direction": "column", "align-items": "center", "background-color": "#f8f9fa"}

)


div_generated = html.Div(
    [
        html.H3(
            "Generated dataframe",
            style={"textAlign": "center"}
        ),

        dash_table.DataTable(
            id="generated_table_res",

            virtualization=True,
            style_table={"height": "350px", "marginLeft": 70, "marginRight": 70, "width": 1500, "overflowY": "auto",
                         "overflowX": "auto"},
            style_cell_conditional=[{"if": {"column_id": c}, "textAlign": "left"} for c in ["Date", "Region"]],
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
    style={"marginLeft": 300, "marginTop": 10, "width": "78%", "height": "550px", "display": "flex", "padding": "2rem",
           "flex-direction": "column", "align-items": "center", "background-color": "#f8f9fa"}

)

layout = html.Div(
    [
        div_initial,
        div_generated,

    ],
    style={"display": "flex", "flex-direction": "column"},
    id="results_layout"
)



@app.callback(
    [Output("generated_table_res", "columns"),
     Output("generated_table_res", "data")],
    [Input("storage_whole_generated_table", "data")]
)
def update_initial_table(jsonified_data):
    if jsonified_data is not None:
        df_gen = pd.read_json(jsonified_data, orient="split")
        col_gen = [{"name": i, "id": i, "selectable": True} for i in df_gen.columns],
        return col_gen[0], df_gen.to_dict("records")
    return None, None

@app.callback(
    Output("initial_table_res", "columns"),
    [Input("storage_sample_df", "data")]
)
def update_reduced_table(jsonified_sample_df):
    if jsonified_sample_df is not None:
        df_sample = pd.read_json(jsonified_sample_df, orient="split")
        col = [{"name": i, "id": i, "selectable": True} for i in df_sample],
        return col[0]
    return None

