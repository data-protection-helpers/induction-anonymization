import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc


sidebar_div = html.Div(
    [
        html.H2("Menu", className="display-4"),
        html.Hr(),
        html.P(
            "Anonymization tool: protect your data", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", id="app_link"),
                dbc.NavLink("Classification", href="/classification", id="classification_link"),
                dbc.NavLink("Visualization", href="/visualization", id="visualization_link"),
                dbc.NavLink("Results", href="/results", id="results_link"),

            ],
            vertical=True,
            pills=True,
        ),

    ],
    style={"position": "fixed", "top": 0, "left": 0, "bottom": 0, "width": "18rem", "padding": "2rem 1rem",
           "background-color": "#f8f9fa"}
)

