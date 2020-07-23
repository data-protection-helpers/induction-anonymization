import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from apps import homepage, synthetic_data, results, classification, visualization
from app import app
from components import sidebar
import dash







app.layout = html.Div(
    [
        sidebar.sidebar_div,
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content"),
        html.Div(
            [
                # from homepage
                dcc.Store(id="storage_sample_df", storage_type="local", clear_data=True),
                dcc.Store(id="storage_button_sample_df", storage_type="local", clear_data=True),

                # from classification
                dcc.Store(id="storage_updated_columns", storage_type="local", clear_data=True),
                dcc.Store(id="storage_selected_columns", storage_type="local", clear_data=True),
                dcc.Store(id="storage_synth_col", storage_type="local", clear_data=True),
                dcc.Store(id="storage_types", storage_type="local", clear_data=True),

                # from synthetic_data
                dcc.Store(id="storage_pearson_graph_gen", storage_type="local", clear_data=True),
                dcc.Store(id="storage_pearson_graph_init", storage_type="local", clear_data=True),
                dcc.Store(id="storage_generated_table_cat", storage_type="local", clear_data=True),
                dcc.Store(id="storage_generated_table_num", storage_type="local", clear_data=True),
                dcc.Store(id="storage_sample_df_num", storage_type="local", clear_data=True),


            ],
            id="hidden_data",
            style={"display": "none"},
        ),
        dbc.Button(id="smote_button", n_clicks=0, children="Synthesize", color="secondary", href="/results", style={"display": "none"})


    ],  style={"display": "flex", "align-items": "flex-start"}
)


@app.callback(
    [Output(f"synthetic_data_link", "active"),
     Output(f"app_link", "active"),
     Output(f"results_link", "active"),
     Output(f"classification_link", "active"),
     Output(f"visualization_link", "active")],
    [Input("url", "pathname")]
)
def toggle_active_links(pathname):
    if pathname == "/":
        return False, True, False, False, False
    elif pathname == "/synthetic_data":
        return True, False, False, False, False
    elif pathname == "/results":
        return False, False, True, False, False
    elif pathname == "/classification":
        return False, False, False, True, False
    return False, False, False, False, True


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

    elif pathname == "/visualization":
        return visualization.layout

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
