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
global glob_sample_df
glob_sample_df = []


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
        )

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
                )
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
    Output("synth_dropdown", "options"),
    [Input("storage_sample_df", "data")]
)
def classification_page_initialization(jsonified_df_sample):
    df_sample = pd.read_json(jsonified_df_sample, orient="split")

    # builds global sample dataframe
    for i in df_sample:
        glob_sample_df.append({"name": i, "id": i, "selectable": True})

    # returns options for synthesization dropdown
    return [{"label": i, "value": i} for i in df_sample]


# updates the sample df
@app.callback(
    [Output("type_dropdown", "value"),
     Output("df_sample", "selected_columns"),
     Output("df_sample", "columns")],
    [Input("storage_updated_columns", "data"), Input("storage_selected_columns", "data")]
)
def update_sample_df(jsonified_updated_columns, selected_columns):
    # if no columns have been selected yet
    if selected_columns is None:
        return None, [], glob_sample_df

    # if columns have been selected but their type has not yet been assessed
    elif jsonified_updated_columns is None:
        return None, selected_columns, glob_sample_df

    # if columns have been selected and assessed
    else:
        col = json.loads(jsonified_updated_columns)
        return None, [], col


# stores anonymisation information
@app.callback(
    [Output("storage_synth_col", "data"),
     Output("storage_types", "data")],
    [Input("validate_anonymisation", "n_clicks"), Input("synth_dropdown", "value")],
)
def store_anonymisation_information(n_clicks, content):
    if n_clicks != 0:
        return content, df_sample_types
    return None, None


# stores selected columns
@app.callback(
    Output("storage_selected_columns", "data"),
    [Input("df_sample", "selected_columns")]
)
def store_selected_columns(children):
    return children


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


# stores updated global sample df with added types from actual selected columns type values (according to type dropdown)
@app.callback(
    Output("storage_updated_columns", "data"),
    [Input("type_dropdown", "value"),
     Input("df_sample", "selected_columns")]
)
def store_attribute_types(value, selected_columns):
    if selected_columns is not None and len(selected_columns) > 0 and value is not None:
        for i, column in enumerate(glob_sample_df):

            # we add a type for selected columns
            # other columns are left as they are
            if column["name"] in selected_columns:
                df_sample_types[column["name"]] = matching_types[value]
                glob_sample_df[i] = {"name": column["name"], "id": column["name"], "type": value, "selectable": True}

        return json.dumps(glob_sample_df)

    return None


