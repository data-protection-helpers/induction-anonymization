import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash
import dash_table
import json

import pandas as pd

from components.sidebar import sidebar_div
from app import app

df = pd.read_csv("../data/statistical-generative-modeling-sample.csv.bz2")
df = df[:500]

div1 = html.Div(
    [
        html.H3("Select columns you want to keep", id="guideline", style={"textAlign": "center"}),
        dash_table.DataTable(
            id="initial_table",
            columns=[
                {
                    "name": i, "id": i, "selectable": True
                } for i in df.columns
            ],
            data=df.to_dict("records"),
            column_selectable="multi",
            selected_columns=[],
            virtualization=True,
            style_table={"height": "350px",  "marginLeft": 50, "width":"90%", "overflowY": "auto", "overflowX": "auto"},
            style_cell_conditional=[
                {
                    "if": {"column_id": c},
                    "textAlign": "left"
                } for c in ["Date", "Region"]
            ],
            style_data_conditional=[
                {
                    "if": {"row_index": "odd"},
                    "backgroundColor": "rgb(248, 248, 248)"
                }
            ],
            style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"}
        ),
        dbc.Button(id="validate_columns", n_clicks=0, children="Submit", color="secondary"),

        html.Div(id="storage_reduced_table", style={"display": "none"}),

    ], style={"marginTop": 10, "marginLeft": 300,  "width": "80%", "height": "550px", "padding":
        "2rem", "display": "flex", "flex-direction": "column", "align-items": "center", "background-color":
                  "#f8f9fa"}, id="div1",
)

div2 = html.Div(
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
                html.Div([
                            html.H3("Select columns you want to synthesize", style={"text-align": "left"}),
                            dcc.Dropdown(
                                id="synth_dropdown",
                                multi=True,
                                placeholder="Select the type of anonymisation you want to perform",
                            ),

                         ], style={"marginTop": 50, "marginBottom": 50}
                ),
                html.Div([
                            dbc.Button(id="validate_anonymisation", n_clicks=0, children="Submit", color="secondary"),
                        ], style={"display": "flex", "flex-direction": "column", "align-items": "center"}
                )

            ], id="div2", style={"display": "none"}
        ),
    ], id="div2_container", style={"marginTop": 30, "marginLeft": 300, "width": "100%", "height": "650px", "padding":
        "1rem 1rem", "flex-direction": "column",
                                   "background-color": "#f8f9fa", "display": "flex"}

)

layout = html.Div([
    #sidebar_div,
    html.Div([
        div1,
        div2
    ], style={"display": "flex", "align-items": "flex-start", "flex-direction": "column"}
    )
], style={"display": "flex", "align-items": "flex-start"}, id="homepage_layout"
)


@app.callback(
    Output('storage_layout', 'data'),
    [Input("homepage_layout", "children")],
)
def store_layout(children):
    return children


@app.callback(
    Output("storage_reduced_table", "children"),
    [Input("initial_table", "selected_columns"),
     Input("validate_columns", "n_clicks")]
)
def store_reduced_df_to_json(selected_columns, n_clicks):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if "validate_columns" in changed_id:
        df_sample = df[selected_columns]
        return df_sample.to_json(date_format="iso", orient="split")


@app.callback(
    # Output("div1", "children"),
    [Output("homepage_layout", "children"),
     Output("synth_dropdown", "options")],
    [Input("storage_reduced_table", "children")]
)
def update_reduced_table(jsonified_cleaned_data):
    df_sample = pd.read_json(jsonified_cleaned_data, orient="split")
    new_div = html.Div([
        html.H3(
            "Categorize each column",
            style={"textAlign": "center"}
        ),
        dash_table.DataTable(
            id="initial_table2",
            columns=[{"name": i, "id": i, "selectable": True} for i in df_sample],
            data=df.to_dict("records"),
            column_selectable="single",
            editable=True,
            selected_columns=[],
            virtualization=True,
            style_table={"height": "350px", "width": 1200, "overflowY": "auto", "overflowX": "auto",
                         "margin": 20},
            style_cell_conditional=[
                {
                    "if": {"column_id": c},
                    "textAlign": "left"
                } for c in ["Date", "Region"]
            ],
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
            style_header={
                "backgroundColor": "rgb(230, 230, 230)",
                "fontWeight": "bold"
            }
        )

    ], style={ "marginLeft": 300, "width": "100%", "height": "550px", "display": "flex", "padding": "2rem",
              "flex-direction": "column", "align-items": "center", "background-color":
                  "#f8f9fa"})

    return html.Div([
        #sidebar_div,
        html.Div([
            new_div,
            div2
        ], style={"display": "flex", "align-items": "flex-start", "flex-direction": "column"}
        )
    ], style={"display": "flex", "align-items": "flex-start"}, id="homepage_layout"
    ), [{"label": i, "value": i} for i in df_sample]


@app.callback(
    [Output("guideline2", "children"),
     Output("type_dropdown", "disabled"),
     Output("anony_dropdown", "disabled"),
     Output("div2", "style")],
    [Input("initial_table2", "selected_columns")]
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
     Input("initial_table2", "selected_columns"),
     Input("initial_table2", "columns")]
)
def store_attribute_types(value, selected_columns, columns):
    if len(selected_columns) > 0:
        col = []
        for i in columns:
            if i["name"] != selected_columns[0]:
                col.append(i)
            else:
                col.append({"name": selected_columns[0], "id": selected_columns[0], "type": value, "selectable": True})
        return json.dumps(col)


@app.callback(
    Output("initial_table2", "columns"),
    [Input("intermediate-value2", "children")]
)
def update_attribute_colors(jsonified_cleaned_data):
    col = json.loads(jsonified_cleaned_data)
    return col


if __name__ == "__main__":
    app.run_server(debug=True)
