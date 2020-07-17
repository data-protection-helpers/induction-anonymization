
import dash_html_components as html
import dash_bootstrap_components as dbc
from components.sidebar import sidebar_div


header = html.H3(
    'Select the synthesization technique:',
    style={'textAlign': 'center', 'marginBottom': 60, 'marginTop': 60}
)


body = dbc.Container(
    [
       dbc.Row(
           [
               dbc.Col(
                  [

                     html.H2("SMOTE"),
                     html.P(
                         """\
Donec id elit non mi porta gravida at eget metus.Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentumnibh, ut fermentum massa justo sit amet risus. Etiam porta semmalesuada magna mollis euismod. Donec sed odio dui. Donec id elit nonmi porta gravida at eget metus. Fusce dapibus, tellus ac cursuscommodo, tortor mauris condimentum nibh, ut fermentum massa justo sitamet risus. Etiam porta sem malesuada magna mollis euismod. Donec sedodio dui."""
                           ),
                      dbc.Button("Synthesize", color="secondary"),
                      html.Div(
                          id="output2"

                      ),
                   ],
                  md=6,
               ),
               dbc.Col(
                   [
                       html.H2("Statistical generative model"),
                       html.P(
                           """\
  Donec id elit non mi porta gravida at eget metus.Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentumnibh, ut fermentum massa justo sit amet risus. Etiam porta semmalesuada magna mollis euismod. Donec sed odio dui. Donec id elit nonmi porta gravida at eget metus. Fusce dapibus, tellus ac cursuscommodo, tortor mauris condimentum nibh, ut fermentum massa justo sitamet risus. Etiam porta sem malesuada magna mollis euismod. Donec sedodio dui."""
                       ),
                       dbc.Button("Synthesize", color="secondary"),
                   ],
                   md=6,
               )
            ]
        )


    ]

)


layout = html.Div([
    #sidebar_div,
    header,
    body,
])
