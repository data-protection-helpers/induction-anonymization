import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from apps import homepage, synthetic_data , results, classification, visualization
from app import app
from components import sidebar
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
                dcc.Store(id="storage_button_sample_df", storage_type="local", clear_data=True),

                # from classification
                dcc.Store(id="storage_updated_columns", storage_type="local", clear_data=True),
                dcc.Store(id="storage_selected_columns", storage_type="local", clear_data=True),
                dcc.Store(id="storage_synth_attributes", storage_type="local", clear_data=True),
                dcc.Store(id="storage_swap_attributes", storage_type="local", clear_data=True),
                dcc.Store(id="storage_mask_attributes", storage_type="local", clear_data=True),
                dcc.Store(id="storage_types", storage_type="local", clear_data=True),
                dcc.Store(id="storage_techniques", storage_type="local", clear_data=True),
                dcc.Store(id="storage_glob_sample_df", storage_type="local", clear_data=True),
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


            ],
            id="hidden_data",
            style={"display": "none"},
        ),


    ],  style={"display": "flex", "align-items": "flex-start"}
)


@app.callback(
    [Output(f"app_link", "active"),
     Output(f"results_link", "active"),
     Output(f"classification_link", "active"),
     Output(f"visualization_link", "active")],
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
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )


if __name__ == "__main__":
    app.run_server(debug=True)
