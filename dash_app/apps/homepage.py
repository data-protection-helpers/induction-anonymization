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

matching_types = {"numeric": "Numerical", "text": "Categorical", "datetime": "Other"}
df_sample_types = {}

div_initial_df = html.Div(
    [
        html.H3("Select columns you want to keep", id="guideline", style={"textAlign": "center"}),
        dash_table.DataTable(
            id="initial_table",
            columns=[
                {"name": i, "id": i, "selectable": True} for i in df.columns],
            data=df.to_dict("records"),
            column_selectable="multi",
            selected_columns=[],
            virtualization=True,
            style_table={"height": "350px", "marginLeft": 50, "width": "90%", "overflowY": "auto", "overflowX": "auto"},
            style_cell_conditional=[
                {"if": {"column_id": c}, "textAlign": "left"} for c in ["Date", "Region"]],
            style_data_conditional=[
                {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
            ],
            style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"}
        ),
        dbc.Button(id="validate_columns", n_clicks=0, children="Submit", color="secondary", href="/classification"),

    ],
    id="div_initial_df",
    style={"marginTop": 10, "marginLeft": 300, "width": "78%", "height": "550px", "padding": "2rem", "display": "flex",
           "flex-direction": "column", "align-items": "center", "background-color": "#f8f9fa"}
)




layout = html.Div(
    [
        div_initial_df,
    ],
    id="homepage_layout",
    style={"display": "flex", "flex-direction": "column"},
)


@app.callback(
    Output("storage_sample_df", "data"),
    [Input("initial_table", "selected_columns"),
     Input("validate_columns", "n_clicks")]
)
def store_reduced_data_information(selected_columns, n_clicks):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if "validate_columns" in changed_id:
        df_sample = df[selected_columns]
        return df_sample.to_json(date_format="iso", orient="split")
    return None



if __name__ == "__main__":
    app.run_server(debug=True)
