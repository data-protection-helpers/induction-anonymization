import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash
import dash_table
import json
from app import app

import base64
import datetime
import io

import pandas as pd


matching_types = {"numeric": "Numerical", "text": "Categorical", "datetime": "Text"}
df_sample_types = {}

div_initial_df = html.Div(
    [
        dcc.Upload(
            id='upload-data',
            children=html.Div(['Drag and Drop or ', html.A('Select a file')]),
            style={
                'width': '100%',
                'height': '250px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        ),


        html.Div(
            [
                html.Div(
                    [
                        html.H3("Select columns you want to keep", id="guideline", style={"textAlign": "center"}),
                    ],
                    style={"display": "flex", "flex-direction": "column", "align-items": "center"}
                ),
                html.Div(
                    [
                        dcc.Checklist(
                            id="select_all_init",
                            options=[{'label': 'Select all', 'value': 'select_all'}],
                            value=[],
                            style={"fontWeight": "bold", "display": "flex", "flex-direction": "column",
                                   "align-items": "left"}
                        ),
                    ],
                    style={"display": "flex", "flex-direction": "column", "align-items": "left"}
                ),
                html.Div(
                    [
                        dash_table.DataTable(
                            id="initial_df",
                            # columns=[{"name": i, "id": i, "selectable": True} for i in df.columns],
                            column_selectable="multi",
                            selected_columns=[],
                            virtualization=True,
                            style_table={"height": "350px", "marginLeft": 70, "marginRight": 70, "width": 1500,
                                         "overflowY":
                                             "auto", "overflowX": "auto"},

                            style_data_conditional=[
                                {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
                            ],
                            style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold",
                                          'padding-left': '20px'}
                        ),
                        dbc.Button(id="validate_columns", n_clicks=0, children="Submit", color="secondary", href=
                                   "/classification"),

                    ],
                    style={"display": "flex", "flex-direction": "column", "align-items": "center"}
                )
            ],
            id="div_initial_df",
            style={"display": "none"}
        ),
    ],
    id="div_initial_df",
    style={"marginTop": 10, "marginLeft": 300, "width": 1570, "height": 900, "padding": "2rem", "display": "flex",
           "flex-direction": "column", "background-color": "#f8f9fa", "justify-content": "space-around"}

)


layout = html.Div(
    [
        div_initial_df,
    ],
    id="homepage_layout",
    style={"display": "flex", "flex-direction": "column"},
)


# returns all columns as selected columns if the select all checkbox is selected
@app.callback(
    Output("initial_df", "selected_columns"),
    [Input("select_all_init", "value"),
     Input("initial_df", "columns")]
)
def selects_all_columns(value, columns):
    if len(value) >= 1 and value[0] == "select_all":
        selection = []
        for column in columns:
            selection.append(column["name"])
        return selection
    return []


# stores the sample df
@app.callback(
    Output("storage_sample_df", "data"),
    [Input("validate_columns", "n_clicks")],
    [State("initial_df", "selected_columns"),
     State("storage_initial_df", "data")]
)
def stores_sample_df_information(n_clicks, selected_columns, jsonified_initial_df):
    if jsonified_initial_df is not None:
        df = pd.read_json(jsonified_initial_df, orient="split")
        df_sample = df[selected_columns]
        return df_sample.to_json(date_format="iso", orient="split")
    return None


# used for upload data
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # if the user uploads a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # if the user uploads an excel file: to try
            df = pd.read_excel(io.BytesIO(decoded))

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df[:100].to_dict('records'), [{'name': i, 'id': i, 'selectable': True} for i in df[:100].columns], df[:100]


# initial data upload
@app.callback([Output("div_initial_df", "style"),
              Output('initial_df', 'data'),
              Output('initial_df', 'columns'),
               Output('storage_initial_df', 'data')],
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')]
)
def updates_page(list_of_contents, list_of_names):
    if list_of_contents is not None:
        data, columns, df = parse_contents(list_of_contents, list_of_names)
        return {"display": "flex", "flex-direction": "column"}, data, columns, df.to_json(date_format="iso", orient="split")
    return {"display": "none"}, None, None, None


