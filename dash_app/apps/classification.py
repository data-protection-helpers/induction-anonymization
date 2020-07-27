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
#df_sample_types = {}
#df_sample_techniques = {}
#global glob_sample_df
#glob_sample_df = []


div_sample_df = html.Div(
    [
        html.Div(
            [
                html.H3("Categorize each column",style={"textAlign": "center"}),

            ],
            style={"marginTop": 10, "marginLeft": 300, "width": "78%", "height": "550px", "padding": "2rem", "display": "flex",
           "flex-direction": "column", "align-items": "center", "background-color": "#f8f9fa"}
        ),


        html.Div(
            [
                dcc.Checklist(
                    id="select_all_sample",
                    options=[{'label': 'Select all', 'value': 'select_all'}],
                    value=[],
                    style={"fontWeight": "bold"}
                ),
            ],
            style={"display": "flex", "flex-direction": "column", "align-items": "left"}
        ),

        html.Div(
            [
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
            style={"display": "flex", "flex-direction": "column", "align-items": "center"}

        )


    ],
    style={"marginTop": 10, "marginLeft": 300, "width": "78%", "height": "550px", "padding": "2rem", "display": "flex",
           "flex-direction": "column", "background-color": "#f8f9fa"}
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
                        {"label": "Synthesization", "value": "synth"},
                    ],
                    placeholder="Select the type of anonymisation you want to perform",
                ),
                dbc.Button(id="validate_anony", n_clicks=0, children="Validate", color="secondary"),


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


@app.callback(
    Output("validate_anony", "disabled"),
    [Input("type_dropdown", "value"),
     Input("anony_dropdown", "value")]
)
def disable_validate_button(value_type, value_technique):
    if value_type != "Select the type of the attribute" and value_technique !="Select the type of anonymisation you want to perform":
        return False
    return True


# sets synthesization dropdown options and global sample dataframe based on selected columns from homepage
@app.callback(
    [Output("df_sample", "columns"),
     Output("df_sample", "selected_columns"),
     Output("type_dropdown", "value"),
     Output("anony_dropdown", "value"),

     ],
    [Input("storage_sample_df", "data"),
     Input("validate_anony", "n_clicks"),
     Input("select_all_sample", "value")],
    [State("df_sample", "selected_columns"),
     State("df_sample", "columns"),
     State("type_dropdown", "value"),
     State("anony_dropdown", "value"),

     ]

)
def classification_page_initialization(jsonified_df_sample,  n_clicks, select_all, selected_columns, columns, value_type, value_technique):
    if jsonified_df_sample is not None:
        df_sample = pd.read_json(jsonified_df_sample, orient="split")
        if columns is None:
            return [{"name": i, "id": i, "selectable": True} for i in df_sample.columns], [], "Select the type of the attribute", "Select the type of anonymisation you want to perform"

        else:

            if value_type != "Select the type of the attribute" and value_technique != "Select the type of anonymisation you want to perform":
                col = columns
                for i, name in enumerate(df_sample.columns):
                    # we add a type for selected columns
                    # other columns are left as they are
                    if name in selected_columns:

                        col[i] = {"name": name, "id": name, "type": value_type,
                                  "selectable": True}
                return col, [], "Select the type of the attribute", "Select the type of anonymisation you want to perform"
            if len(select_all) >= 1 and select_all[0] == "select_all":

                return columns, [i for i in df_sample.columns], "Select the type of the attribute", "Select the type of anonymisation you want to perform"



@app.callback(
    [ Output("storage_types", "data"),
     Output("storage_techniques", "data")],
    [Input("validate_anony", "n_clicks"),
     ],
    [State("df_sample", "selected_columns"),
     State("storage_types", "data"),
     State("storage_techniques", "data"),
     State("type_dropdown", "value"),
     State("anony_dropdown", "value"),
     State("df_sample", "columns")]
)
def updates_info(n_clicks, selected_columns, df_sample_types, df_sample_techniques, value_type, value_technique, columns):
    if columns is None:

        return {}, {}
    else:

        for column in columns:
            # we add a type for selected columns
            # other columns are left as they are
            if column["name"] in selected_columns:
                df_sample_types[column["name"]] = matching_types[value_type]
                df_sample_techniques[column["name"]] = value_technique
        return df_sample_types, df_sample_techniques

@app.callback(
    Output("select_all_sample", "value"),
    [Input("validate_anony", "n_clicks")],
)
def untick_select_all(n_clicks):
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
    Output("storage_synth_col", "data"),
    [Input("validate_anonymisation", "n_clicks")],
     [State("storage_techniques", "data")],

)
def store_anonymisation_information(data, df_sample_techniques):
    if df_sample_techniques is not None:
        synthesization_columns = []
        for key in df_sample_techniques:
            if df_sample_techniques[key] == "synth":
                synthesization_columns.append(key)
        return synthesization_columns
