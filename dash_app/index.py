import numpy as np
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import sys
sys.path.append("apps/")
sys.path.append("components/")
import homepage
import results
import classification
import visualization
#from apps import homepage, results, classification, visualization
from app import app
import sidebar
import dash_table



app.layout = html.Div(
    [
        sidebar.sidebar_div,
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content"),
        html.Div(
            [
                # from homepage
                dcc.Store(id="storage_sample_df", storage_type="local", clear_data=True),
                dcc.Store(id="storage_initial_df", storage_type="local", clear_data=True),

                # from classification
                dcc.Store(id="storage_updated_columns", storage_type="local", clear_data=True),
                dcc.Store(id="storage_selected_columns", storage_type="local", clear_data=True),
                dcc.Store(id="storage_synth_attributes", storage_type="local", clear_data=True),
                dcc.Store(id="storage_swap_attributes", storage_type="local", clear_data=True),
                dcc.Store(id="storage_mask_attributes", storage_type="local", clear_data=True),
                dcc.Store(id="storage_text_gen_attributes", storage_type="local", clear_data=True),
                dcc.Store(id="storage_types", storage_type="local", clear_data=True),
                dcc.Store(id="storage_techniques", storage_type="local", clear_data=True),
                dcc.Store(id="storage_main_classification_button", storage_type="local", clear_data=True),

                # from synthetic_data
                dcc.Store(id="storage_pearson_gen_SMOTE", storage_type="local", clear_data=True),
                dcc.Store(id="storage_pearson_gen_STAT", storage_type="local", clear_data=True),
                dcc.Store(id="storage_pearson_init", storage_type="local", clear_data=True),
                dcc.Store(id="storage_synthetic_table_cat_SMOTE", storage_type="local", clear_data=True),
                dcc.Store(id="storage_synthetic_table_num_SMOTE", storage_type="local", clear_data=True),
                dcc.Store(id="storage_synthetic_table_cat_STAT", storage_type="local", clear_data=True),
                dcc.Store(id="storage_synthetic_table_num_STAT", storage_type="local", clear_data=True),
                dcc.Store(id="storage_sample_synth_df_num", storage_type="local", clear_data=True),
                dcc.Store(id="storage_whole_generated_table_SMOTE", storage_type="local", clear_data=True),
                dcc.Store(id="storage_whole_generated_table_STAT", storage_type="local", clear_data=True),
                dcc.Store(id="storage_whole_generated_table", storage_type="local", clear_data=True),


            ],
            id="hidden_data",
            style={"display": "none"},
        ),


    ],  style={"display": "flex", "align-items": "flex-start"}
)


@app.callback(
    [Output("app_link", "active"),
     Output("results_link", "active"),
     Output("classification_link", "active"),
     Output("visualization_link", "active")],
    [Input("url", "pathname")]
)
def toggle_active_links(pathname):
    if pathname == "/":
        return True, False, False, False
    elif pathname == "/results":
        return False, True, False, False
    elif pathname == "/classification":
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

    elif pathname == "/classification":
        return classification.layout

    elif pathname == "/visualization":
        return visualization.layout

    else:
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P("The pathname {pathname} was not recognised..."),
            ]
        )


if __name__ == "__main__":
    #app.run_server(debug=True)
    app.run_server(host='0.0.0.0', debug=True)
#    usageStr = "That script launches a Dash application (Flask server)"
#    (verboseFlag, dashPort) = dc.handle_opt(usageStr)

 #   app.run_server (host = '0.0.0.0', port = dashPort, debug = verboseFlag)

