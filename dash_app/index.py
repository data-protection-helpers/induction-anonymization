import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from apps import homepage, synthetic_data, results, classification
from app import app
from components import sidebar
import dash


app.layout = html.Div(
    [
        sidebar.sidebar_div,
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content" ),
        html.Div(
            [
                dcc.Store(id="storage_button_sample_df", storage_type="local", clear_data=True),
                dcc.Store(id="storage_button_anonymisation", storage_type="local", clear_data=True),
                dcc.Store(id="storage_synth_col", storage_type="local", clear_data=True),
                dcc.Store(id="storage_types", storage_type="local", clear_data=True),
                dcc.Store(id="storage_sample_df", storage_type="local", clear_data=True),
                dcc.Store(id="storage_pearson_graph_gen", storage_type="local", clear_data=True),
                dcc.Store(id="storage_pearson_graph_init", storage_type="local", clear_data=True),
                dcc.Store(id="storage_generated_table", storage_type="local", clear_data=True),
            ],
            id="hidden_data",
            style={"display": "none"},
        ),

    ],  style={"display": "flex", "align-items": "flex-start"}
)



@app.callback(
    Output("url", "pathname"),
    [Input("storage_button_anonymisation", "data"), Input("storage_button_sample_df", "data")]
)
def redirect_data_page(data1, data2):
    if data1 != 0 and data1 is not None:
        return "/synthetic_data"
    elif data2 != 0 and data2 is not None:
        return "/classification"
    return "/"


@app.callback(
    [Output(f"synthetic_data_link", "active"), Output(f"app_link", "active"), Output(f"results_link", "active"), Output(f"classification_link", "active")],
    [Input("url", "pathname")]
)
def toggle_active_links(pathname):
    if pathname == "/":
        return False, True, False, False
    elif pathname == "/synthetic_data":
        return True, False, False, False
    elif pathname == "/results":
        return False, False, True, False
    return False, False, False, True


@app.callback(
    Output("page-content", "children"), [Input("url", "pathname")],
)
def render_page_content(pathname):
    if pathname == "/":
        return homepage.layout

    elif pathname == "/results":
        return results.layout

    elif pathname == "/synthetic_data":
        return synthetic_data.layout

    elif pathname == "/classification":
        return classification.layout

    else:
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )


if __name__ == "__main__":
    app.run_server(debug=True)
