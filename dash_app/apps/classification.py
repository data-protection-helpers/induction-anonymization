import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash
import dash_table
import json
from app import app

import pandas as pd

matching_types = {"numeric": "Numerical", "text": "Categorical", "datetime": "Text"}

div_sample_df = html.Div(
    [
        html.Div(
            [
                html.H3("Classify each column", style={"textAlign": "center"}),
            ],
            style={"display": "flex", "flex-direction": "column", "align-items": "center"}
        ),
        html.Div(
            [
                dcc.Checklist(
                    id="select_all_sample_df",
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
                    column_selectable="multi",
                    editable=True,
                    selected_columns=[],
                    virtualization=True,
                    style_table={"height": "350px", "marginLeft": 70, "marginRight": 70, "width": 1500,
                                 "overflowY": "auto", "overflowX": "auto"},
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
                    style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold", 'padding-left': '20px'}
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
                html.H4("Type of attribute:", style={"text-align": "left"}),
                dcc.Dropdown(
                    id="type_dropdown",
                    options=[
                        {"label": "Numerical", "value": "numeric"},
                        {"label": "Categorical", "value": "text"},
                        {"label": "Text", "value": "datetime"}
                    ],
                    placeholder="Select the type of the attribute",
                ),

                html.H4("Anonymisation technique:", style={"text-align": "left"}),
                dcc.Dropdown(
                    id="anony_dropdown",
                    options=[
                        {"label": "Synthesization", "value": "synth"},
                        {"label": "Total masking", "value": "mask"},
                        {"label": "Swapping", "value": "swap"},
                        {"label": "Text generation", "value": "text_gen"}
                    ],
                    placeholder="Select the type of anonymization you want to perform",
                ),

            ],

            style={"display": "flex", "flex-direction": "column", "justify-content": "space-around"}
        ),

        html.Div(
            [
                dbc.Button(id="validate_partial_classification", n_clicks=0, children="Validate", color="secondary"),
            ], style={"display": "flex", "flex-direction": "column", "align-items": "start"}
        ),

        html.Div(
            [
                dbc.Button(id="validate_total_classification", n_clicks=0, children="Submit", color="secondary"),
            ], style={"display": "flex", "flex-direction": "column", "align-items": "center"}
        ),
    ],
    style={"marginTop": 10, "marginLeft": 300, "width": "78%", "height": "350px", "padding": "2rem", "display": "flex",
           "flex-direction": "column", "justify-content": "space-around", "background-color": "#f8f9fa"}

)

layout = html.Div(
    [
        div_sample_df,
        div_classification
    ],
    style={"display": "flex", "flex-direction": "column"}
)


# sets data for sample df display
@app.callback(
    Output("df_sample", "data"),
    [Input("storage_sample_df", "data")]
)
def init_sample_data(jsonified_sample_df):
    if jsonified_sample_df is not None:
        df = pd.read_json(jsonified_sample_df, orient="split")
        return df[:100].to_dict('records')
    return None


# sets anonymization techniques according to attribute type selected by the user
@app.callback(
    Output("anony_dropdown", "options"),
    [Input("type_dropdown", "value")]
)
def sets_techniques(value):
    # if value is datetime (which corresponds to textual in reality), choices for techniques are reduced
    if value == "datetime":
        return [{"label": "Total masking", "value": "mask"},
                {"label": "Text generation", "value": "text_gen"}]
    return [{"label": "Synthesization", "value": "synth"},
            {"label": "Total masking", "value": "mask"},
            {"label": "Swapping", "value": "swap"},
            {"label": "Text generation", "value": "text_gen"}]


# sets page to which the final classification will redirect
@app.callback(
    Output("validate_total_classification", "href"),
    [Input("storage_synth_attributes", "data")]
)
def redirects_main_button(synth_attributes):
    # if no attributes are selected for synthesization, the user is redirected to results page
    if synth_attributes is None or len(synth_attributes) == 0:
        return "/results"
    # else the user is redirected to the synthetic data visualization page
    else:
        return "/visualization"


# enables the partial classification button to save partial choices for attributes classification
@app.callback(
    Output("validate_partial_classification", "disabled"),
    [Input("type_dropdown", "value"),
     Input("anony_dropdown", "value")]
)
def enables_partial_classification_button(value_type, value_technique):
    # if the user has selected a type and a technique, the button is enabled
    if value_type != "Select the type of the attribute" and value_technique != "Select the type of anonymization you " \
                                                                               "want to perform":
        return False
    return True


# enables the main classification button to save final choices for attributes classification
@app.callback(
    Output("validate_total_classification", "disabled"),
    [Input("storage_types", "data"),
     Input("storage_techniques", "data"),
     Input("df_sample", "columns")]
)
def enables_total_classification_button(df_sample_types, df_sample_techniques, columns):
    if columns is None:
        return True
    else:
        # if not every attribute from the sample data-frame has been classified, the button remains disabled
        disable = False
        for column in columns:
            if column["name"] not in df_sample_types or column["name"] not in df_sample_techniques:
                disable = True
        return disable


# resets select all checkbox to empty after every partial classification
@app.callback(
    Output("select_all_sample_df", "value"),
    [Input("validate_partial_classification", "n_clicks")],
)
def empties_select_all_button(n_clicks):
    return []


# updates guideline for classification of selected columns and enables type and anonymization dropdowns
@app.callback(
    [Output("guideline_selected_columns", "children"),
     Output("type_dropdown", "disabled"),
     Output("anony_dropdown", "disabled")],
    [Input("df_sample", "selected_columns")]
)
def updates_guideline(selected_columns):

    # if no columns are selected nothing is displayed and dropdowns remain disabled
    if selected_columns is None or len(selected_columns) == 0:
        new_guideline = "Selected columns:"
        return new_guideline, True, True

    # else we print which columns have been selected and enable the dropdowns
    else:
        new_guideline = "Selected columns: " + ", ".join(selected_columns)
    return new_guideline, False, False


# stores techniques chosen by classification
@app.callback(
    [Output("storage_synth_attributes", "data"),
     Output("storage_swap_attributes", "data"),
     Output("storage_mask_attributes", "data"),
     Output("storage_text_gen_attributes", "data")],
    [Input("storage_techniques", "data")],
)
def stores_anonymization_techniques(df_sample_techniques):
    if df_sample_techniques is not None:
        synthesization_attributes = []
        swapping_attributes = []
        masking_attributes = []
        text_gen_attributes = []

        # attributes are stored according to their anonymization technique
        for key in df_sample_techniques:
            if df_sample_techniques[key] == "synth":
                synthesization_attributes.append(key)
            elif df_sample_techniques[key] == "swap":
                swapping_attributes.append(key)
            elif df_sample_techniques[key] == "mask":
                masking_attributes.append(key)
            elif df_sample_techniques[key] == "text_gen":
                text_gen_attributes.append(key)
        return synthesization_attributes, swapping_attributes, masking_attributes, text_gen_attributes

    return None, None, None, None


# stores information from partial classification
@app.callback(
    [Output("storage_types", "data"),
     Output("storage_techniques", "data")],
    [Input("validate_partial_classification", "n_clicks")],
    [State("df_sample", "selected_columns"),
     State("storage_types", "data"),
     State("storage_techniques", "data"),
     State("type_dropdown", "value"),
     State("anony_dropdown", "value"),
     State("df_sample", "columns")]
)
def stores_partial_classification(n_clicks, selected_columns, df_sample_types, df_sample_techniques, value_type,
                                  value_technique, columns):

    # initialization of storage components for selected types and techniques
    if columns is None:
        return {}, {}
    else:
        for column in columns:

            # we update the types and techniques for selected columns, other columns are left as they are
            if column["name"] in selected_columns:
                df_sample_types[column["name"]] = matching_types[value_type]
                df_sample_techniques[column["name"]] = value_technique

        return df_sample_types, df_sample_techniques


# initializes and updates classification page depending on partial classification
@app.callback(
    [Output("df_sample", "columns"),
     Output("df_sample", "selected_columns"),
     Output("type_dropdown", "value"),
     Output("anony_dropdown", "value")],
    [Input("storage_sample_df", "data"),
     Input("validate_partial_classification", "n_clicks"),
     Input("select_all_sample_df", "value")],
    [State("df_sample", "selected_columns"),
     State("df_sample", "columns"),
     State("type_dropdown", "value"),
     State("anony_dropdown", "value")]
)
def updates_classification_page(jsonified_df_sample, n_clicks, select_all, selected_columns, columns, value_type,
                                value_technique):

    if jsonified_df_sample is not None:
        df_sample = pd.read_json(jsonified_df_sample, orient="split")

        # initialization of dataframe and dropdowns
        if columns is None:
            return [{"name": i, "id": i, "selectable": True} for i in df_sample.columns], [], "Select the type of the "\
                                                                                              "attribute", \
                   "Select the type of anonymization you want to perform"

        # once the dataframe and dropdowns have been initialized
        else:

            # if the user has selected a value and a technique:
            if value_type != "Select the type of the attribute" and value_technique != "Select the type of " \
                                                                                       "anonymization you want to " \
                                                                                       "perform":
                col = columns
                for i, name in enumerate(df_sample.columns):
                    # we add a type for selected columns, other columns are left as they are
                    if name in selected_columns:
                        col[i] = {"name": name, "id": name, "type": value_type, "selectable": True}

                return col, [], "Select the type of the attribute", "Select the type of anonymization you want to " \
                                                                    "perform"

            # if the select all checkbox has been selected, all the columns are returned as selected columns
            if len(select_all) >= 1 and select_all[0] == "select_all":
                return columns, [i for i in df_sample.columns], "Select the type of the attribute", "Select the type " \
                                                                                                    "of anonymization" \
                                                                                                    " you want to " \
                                                                                                    "perform"
    return None, None, None, None


# stores information about main classification button
@app.callback(
    Output("storage_main_classification_button", "data"),
    [Input("validate_total_classification", "n_clicks")]
)
def stores_validation_classification(n_clicks):
    return n_clicks


