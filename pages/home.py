import dash
from dash import html, dcc, callback, Input, Output
import dash_daq as daq
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/", name="Home", title="Reverbation | Home")

# Content Data
df = pd.DataFrame(
    {"options": ["A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3", "B4", "B5"]}
)

# Page Layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Reverberation Optimization", className="app-brand")
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.H3(children="Raumcharakteristiken"),
            html.Label(["Raumvolumen in m", html.Sup(3)]),
            dcc.Input(
                type="number",
                placeholder="30",
                id="input_room_volume",
                min=0,
            ),
            html.Div([
                daq.ToggleSwitch(id="my-toggle-switch", value=False),
                html.Div(id="my-toggle-switch-output"),
            ],style={"align": "left"}),
            
            html.Br(),
            html.Label("Temperatur [°C]"),
            html.Br(),
            dash.dcc.Input(
                type="number",
                placeholder="20",
                id="input_room_temperature",
                min=0,
            ),
            
            html.Br(),
            html.Label("Raumhöhe [m]"),
            html.Br(),
            dash.dcc.Input(
                type="number",
                placeholder="20",
                id="input_room_height",
                min=0,
            ),
            html.Br(),
            html.Label("Raumnutzungsart"),
            html.Br(),
            dash.dcc.Dropdown(
                options=[{"label": i, "value": i} for i in df["options"]],
                value="A1",
                id="dropdown_room_usage",
            ),
            html.Br(),
            html.Label("Nachhallzeitdiagramm"),
            dash.dcc.Graph(id="graph-content"),
        ]),
        dbc.Col([
            dcc.Loading(id='p2-2-loading', type='circle', children=dcc.Graph(id='fig-transformed', className='my-graph'))
        ], width=6, className='multi-graph'),
    ]),
    dbc.Col([], width=2),
])


# Page Callbacks
@callback(
    Output("graph-content", "figure"),
    Output("my-toggle-switch-output", "children"),
    Input("dropdown_room_usage", "value"),
    Input("my-toggle-switch", "value"),
    Input("input_room_volume", "value"),
    Input("input_room_temperature", "value"),
    Input("input_room_height", "value"),
)
def update_graph(value):
    # dff = df[df.country==value]
    # return px.line(dff, x='year', y='pop')
    # Placeholder for graph update logic
    return px.line(x=[0, 1], y=[0, 1], title=f"Graph for {value}")


def update_output(value):
    return f"The switch is {value}."
