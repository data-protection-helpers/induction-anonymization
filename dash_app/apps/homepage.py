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

df = pd.read_csv("../data/statistical-generative-modeling-sample.csv.bz2")
df = df[:100]

matching_types = {"numeric": "Numerical", "text": "Categorical", "datetime": "Other"}
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
            # Allow multiple files to be uploaded
            multiple=False
        ),

        html.Div(
            [
                html.H3("Select columns you want to keep", id="guideline", style={"textAlign": "center"}),


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


                dash_table.DataTable(
                    id="initial_table",
                    #columns=[{"name": i, "id": i, "selectable": True} for i in df.columns],
                    #data=df.to_dict("records"),
                    column_selectable="multi",
                    selected_columns=[],
                    virtualization=True,
                    style_table={"height": "350px", "marginLeft": 75, "width": "90%", "overflowY": "auto",
                                 "overflowX": "auto"},
                    style_cell_conditional=[
                        {"if": {"column_id": c}, "textAlign": "left"} for c in ["Date", "Region"]],
                    style_data_conditional=[
                        {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
                    ],
                    style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"}
                ),
                dbc.Button(id="validate_columns", n_clicks=0, children="Submit", color="secondary",
                           href="/classification"),


            ],
            id="div_initial_table",
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

@app.callback(
    Output("initial_table", "selected_columns"),
    [Input("select_all_init", "value")]
)
def select_all_columns(value):
    if len(value) >=1 and value[0] == "select_all":
        return [i for i in df.columns]
    return []


@app.callback(
    Output("storage_sample_df", "data"),
    [Input("validate_columns", "n_clicks")],
    [State("initial_table", "selected_columns")]
)
def store_reduced_data_information( n_clicks, selected_columns,):
    df_sample = df[selected_columns]
    return df_sample.to_json(date_format="iso", orient="split")


def parse_contents(contents, filename, date):
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

    return df[:100].to_dict('records'), [{'name': i, 'id': i, 'selectable': True} for i in df[:100].columns]


@app.callback([Output("div_initial_table", "style"),
              Output('initial_table', 'data'),
              Output('initial_table', 'columns')],
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        data, columns = parse_contents(list_of_contents, list_of_names, list_of_dates)
        return {"display": "flex", "flex-direction": "column", "align-items": "center"}, data, columns
    return {"display": "none"}, None, None


if __name__ == "__main__":
    app.run_server(debug=True)
