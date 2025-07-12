"""
Main application file for the Dash app.

This file initializes the Dash application, registers pages, defines the overall layout,
and runs the server.
"""

import dash
import dash_bootstrap_components as dbc
from dash import Dash, html


# Import shared components
from assets.footer import _footer
# from assets.nav import _nav


app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
	   suppress_callback_exceptions=True, prevent_initial_callbacks=True)
server = app.server

# App Layout
app.layout = dbc.Container([
	
	dbc.Row([
        dbc.Col([dash.page_container])
	]),
    dbc.Row([
        dbc.Col([_footer])
    ]),
    dash.dcc.Store(id='browser-memo2', data=dict(), storage_type='session')
], fluid=True)

# Run App
if __name__ == '__main__':
    app.run(debug=True)
