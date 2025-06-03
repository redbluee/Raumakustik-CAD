import dash
import dash_bootstrap_components as dbc
from dash import Dash, html

import numpy as np




# Import shared components
from assets.footer import _footer
# from assets.nav import _nav


app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
	   suppress_callback_exceptions=True, prevent_initial_callbacks=True)
server = app.server

# App Layout
app.layout = dbc.Container([
	
	dbc.Row([
        # dbc.Col([_nav], width = 2),
        dbc.Col([], width = 2),
        dbc.Col([
            dbc.Row([dash.page_container])
	    ], width = 10),
    ]),
    dbc.Row([
        dbc.Col([], width = 2),
        dbc.Col([
            dbc.Row([_footer])
	    ], width = 10),
    ]),
    dash.dcc.Store(id='browser-memo', data=dict(), storage_type='session')
], fluid=True)

# Run App
if __name__ == '__main__':
    app.run(debug=True)
