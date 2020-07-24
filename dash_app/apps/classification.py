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
#global glob_sample_df
#glob_sample_df = []


div_sample_df = html.Div(
    [
        html.H3(
            "Categorize each column",
            style={"textAlign": "center"}
        ),
        dash_table.DataTable(
            id="df_sample",
            data=df.to_dict("records"),
            column_selectable="multi",
            editable=True,
            selected_columns=[],
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
        ),




    ],
    style={"marginTop": 10, "marginLeft": 300, "width": "78%", "height": "550px", "padding": "2rem", "display": "flex",
           "flex-direction": "column", "align-items": "center", "background-color": "#f8f9fa"}
)

div_classification = html.Div(
    [
        html.Div(
            [
                html.H3("", id="guideline_selected_columns", style={"text-align": "left"}),
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

                html.Div(
                    [
                        html.H3("Select columns you want to synthesize", style={"text-align": "left"}),
                        dcc.Dropdown(
                            id="synth_dropdown",
                            multi=True,
                            options=[],
                            placeholder="Select the type of anonymisation you want to perform",
                        ),
                    ],
                    style={"marginTop": 50, "marginBottom": 50}
                ),
                html.Div(
                    [
                        dbc.Button(id="validate_anonymisation", n_clicks=0, children="Submit", color="secondary",
                                   href="/synthetic_data"),
                    ], style={"display": "flex", "flex-direction": "column", "align-items": "center"}
                ),


            ],
            id="div2",


        ),
    ],
    style={"marginTop": 10, "marginLeft": 300, "width": "78%", "height": "550px", "padding": "2rem", "display": "flex",
           "flex-direction": "column", "background-color": "#f8f9fa"}

)

layout = html.Div(
    [
        div_sample_df,
        div_classification
    ],
    style={"display": "flex", "flex-direction": "column"}
)

# sets synthesization dropdown options and global sample dataframe based on selected columns from homepage
@app.callback(
    [Output("df_sample", "columns"),
     Output("df_sample", "selected_columns")],
    [Input("storage_sample_df", "data"),
     Input("type_dropdown", "value")],
    [State("df_sample", "selected_columns"),
     State("df_sample", "columns")]

)
def classification_page_initialization(jsonified_df_sample, value, selected_columns, columns):
    if jsonified_df_sample is not None:
        if columns is None:
            df_sample = pd.read_json(jsonified_df_sample, orient="split")
            return [{"name": i, "id": i, "selectable": True} for i in df_sample.columns], []
        else:
            if value is not None:
                df_sample = pd.read_json(jsonified_df_sample, orient="split")
                col = columns
                for i, name in enumerate(df_sample.columns):
                    # we add a type for selected columns
                    # other columns are left as they are
                    if name in selected_columns:
                        df_sample_types[name] = matching_types[value]
                        col[i] = {"name": name, "id": name, "type": value,
                                  "selectable": True}
                return col, []
    return None, []


@app.callback(
    Output("synth_dropdown", "options"),
    [Input("storage_sample_df", "data")]
)
def set_synth_dropdown(jsonified_df_sample):
    if jsonified_df_sample is not None:
        df_sample = pd.read_json(jsonified_df_sample, orient="split")
        return [{"label": i, "value": i} for i in df_sample]
    return []


# updates guideline for selected columns based on selected columns
# enables type and anonymisation dropdowns
@app.callback(
    [Output("guideline_selected_columns", "children"),
     Output("type_dropdown", "disabled"),
     Output("anony_dropdown", "disabled")],
    [Input("df_sample", "selected_columns")]
)
def update_guideline(selected_columns):
    # if no columns are selected nothing is displayed and dropdowns remain disabled
    if selected_columns is None or len(selected_columns) == 0:
        new_guideline = "Selected columns:"
        return new_guideline, True, True

    # else we print which columns have been selected and enable the dropdowns
    else:
        new_guideline = "Selected columns: " + ", ".join(selected_columns)
    return new_guideline, False, False


# stores anonymisation information
@app.callback(
    [Output("storage_synth_col", "data"),
     Output("storage_types", "data")],
    [Input("synth_dropdown", "value")],
)
def store_anonymisation_information(content):
    return content, df_sample_types