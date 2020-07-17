import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from apps import homepage, synthetic_data
from app import app
from components import sidebar
import dash


app.layout = html.Div([
    sidebar.sidebar_div,
    dcc.Location(id="url", refresh=False),
    html.Div(id='page-content' ),
    html.Div([
            dcc.Store(id='storage_layout')
        ],
                id="hiddendata",
                style={"display": "none"},
        ),
    html.Div([
                dcc.Store(id='storage_button', storage_type="local", clear_data=True)
            ],

    ),

],  style={"display": "flex", "align-items": "flex-start"}
)

@app.callback(
    Output("url", "pathname"),
    [Input("storage_button", "data")]
)
def redirect_synthetic_data_page(data):
    if data != 0 and data is not None:
        return "/synthetic_data"
    return "/"


@app.callback(
    Output("storage_button", "data"),
    [Input("validate_anonymisation", "n_clicks")],
)
def store_button(n_clicks):
    if n_clicks != 0:
        return n_clicks


@app.callback(
    [Output(f"synthetic_data_link", "active"), Output(f"app_link", "active")],
    [Input("url", "pathname")]
)
def toggle_active_links(pathname):
    if pathname == "/":
        return False, True
    return True, False


@app.callback(
    Output("page-content", "children"), [Input("url", "pathname"), Input("storage_layout", "data")],
)
def render_page_content(pathname, children):

    if pathname == "/":
        if children is None:
            return homepage.layout
        else:
            return children

    elif pathname == "/synthetic_data":
        return html.Div([
            synthetic_data.layout
        ], style={"position": "fixed", "top": 20, "left": 300, "bottom": 0, "width": "83.5%", "height": "550px", "padding":
              "1rem 1rem", "display": "flex", "flex-direction": "column", "align-items": "center", "background-color":
              "#f8f9fa"}
        )

    else:
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )


if __name__ == '__main__':
    app.run_server(debug=True)
