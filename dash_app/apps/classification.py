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
df = df[:500]


matching_types = {"numeric": "Numerical", "text": "Categorical", "datetime": "Other"}
df_sample_types = {}


div_sample_df = html.Div(
    [
        html.H3(
            "Categorize each column",
            style={"textAlign": "center"}
        ),
        dash_table.DataTable(
            id="df_sample",
            data=df.to_dict("records"),
            column_selectable="single",
            editable=True,
            selected_columns=[],
            virtualization=True,
            style_table={"height": "350px",  "marginLeft": 70, "marginRight": 70, "width":1500, "overflowY": "auto",
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
    style={"marginTop": 10, "marginLeft": 300,  "width": "78%", "height": "550px", "padding": "2rem",
                              "display": "flex", "flex-direction": "column", "align-items": "center", "background-color"
                              : "#f8f9fa"}
)


div_classification = html.Div(
    [
        html.Div(
            [
                html.H3("", id="guideline2", style={"text-align": "left"}),
            ]
        ),
        html.Div(
            [
                html.H4("Attribute type", style={"text-align": "left"}),
                dcc.Dropdown(
                    id="type_dropdown",
                    options=[
                        {"label": "Numerical", "value": "numeric"},
                        {"label": "Categorical", "value": "text"},
                        {"label": "Other", "value": "datetime"}
                    ],
                    placeholder="Select the type of the attribute",
                ),
                html.H4("Anonymisation technique", style={"text-align": "left"}),
                dcc.Dropdown(
                    id="anony_dropdown",
                    options=[
                        {"label": "Masking", "value": "mask"},
                        {"label": "Swapping", "value": "swap"},
                        {"label": "Aggregation", "value": "aggreg"},
                    ],
                    placeholder="Select the type of anonymisation you want to perform",
                ),
                html.Div(id="none_output", style={"display": "none"}),
                html.Div(id="intermediate-value2", style={"display": "none"}),
                html.Div(
                    [
                        html.H3("Select columns you want to synthesize", style={"text-align": "left"}),
                        dcc.Dropdown(
                            id="synth_dropdown",
                            multi=True,
                            placeholder="Select the type of anonymisation you want to perform",
                        ),
                    ],
                    style={"marginTop": 50, "marginBottom": 50}
                ),
                html.Div(
                    [
                        dbc.Button(id="validate_anonymisation", n_clicks=0, children="Submit", color="secondary"),
                    ], style={"display": "flex", "flex-direction": "column", "align-items": "center"}
                )
            ],
            id="div2",
            style={"display": "none"}
        ),
    ],
    style={"marginTop": 10, "marginLeft": 300,  "width": "78%", "height": "550px", "padding": "2rem", "display": "flex",
           "flex-direction": "column", "background-color": "#f8f9fa"}

)

layout = html.Div(
    [
        div_sample_df,
        div_classification
    ],
    style={"display": "flex", "flex-direction": "column"}
)


@app.callback(
    Output("df_sample", "columns"),
    [Input("storage_sample_df", "data"), Input("intermediate-value2", "children")]
)
def update_sample_df(jsonified_cleaned_data1, jsonified_cleaned_data2):
    if jsonified_cleaned_data2 != None:
        col = json.loads(jsonified_cleaned_data2)
        return col
    df_sample = pd.read_json(jsonified_cleaned_data1, orient="split")
    col = [{"name": i, "id": i, "selectable": True} for i in df_sample],
    return col[0]


@app.callback(
    [Output("storage_button_anonymisation", "data"),
     Output("storage_synth_col", "data"),
     Output("storage_types", "data")],
    [Input("validate_anonymisation", "n_clicks"), Input("synth_dropdown", "value")],
)
def store_anonymisation_information(n_clicks, content):
    if n_clicks != 0:
        return n_clicks, content, df_sample_types

@app.callback(
    Output("synth_dropdown", "options"),
    [Input("storage_sample_df", "data")]
)
def update_synthesization_dropdown(jsonified_cleaned_data):
    df_sample = pd.read_json(jsonified_cleaned_data, orient="split")
    return [{"label": i, "value": i} for i in df_sample]

@app.callback(
    [Output("guideline2", "children"),
     Output("type_dropdown", "disabled"),
     Output("anony_dropdown", "disabled"),
     Output("div2", "style")],
    [Input("df_sample", "selected_columns")]
)
def print_new_guideline(selected_columns):
    if len(selected_columns) == 0:
        new_guideline2 = "Selected column:"
        return new_guideline2, True, True, {}
    else:
        new_guideline2 = "Selected column: " + str(selected_columns[0])
    return new_guideline2, False, False, {}


@app.callback(
    Output("intermediate-value2", "children"),
    [Input("type_dropdown", "value"),
     Input("df_sample", "selected_columns"),
     Input("df_sample", "columns")]
)
def store_attribute_types(value, selected_columns, columns):
    if len(selected_columns) > 0:
        col = []
        for i in columns:
            if i["name"] != selected_columns[0]:
                col.append(i)
            else:
                col.append({"name": selected_columns[0], "id": selected_columns[0], "type": value, "selectable": True})
                df_sample_types[selected_columns[0]] = matching_types[value]

        return json.dumps(col)


