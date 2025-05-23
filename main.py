from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import dash_daq as daq


df = pd.DataFrame({'options': ['A1', 'A2','A3','A4','A5', 'B1', 'B2','B3','B4','B5']}) # Create a DataFrame with a column named 'options'

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = html.Div([
    html.H1(children="Reverberation Optimization", style={"textAlign": "left"}),
    html.Div(children=[
        html.Div(children=[
            html.H3(children="Raumcharakteristiken", style={"textAlign": "left"}),
            
            html.Br(),
            html.Label('Raumvolumen in m<sup>3</sup>'),
            html.Br(),
            dcc.Input(
            type="number",
            placeholder="30",
            id="input_room_volume",
            min=0,
        ),
            
            html.Div([
                daq.ToggleSwitch(id="my-toggle-switch", value=False),
                html.Div(id="my-toggle-switch-output"),
            ], style={'align': 'left'}),

            html.Br(),
            html.Label('Temperatur [°C]'),
            html.Br(),
            dcc.Input(
            type="number",
            placeholder="20",
            id="input_room_temperature",
            min=0,
        ),
            html.Br(),
            html.Label('Raumhöhe [m]'),
            html.Br(),
            dcc.Input(
            type="number",
            placeholder="20",
            id="input_room_height",
            min=0,
        ),

            html.Br(),
            html.Label('Raumnutzungsart'),
            html.Br(),
            dcc.Dropdown(
            options=[{"label": i, "value": i} for i in df["options"]],
            value="A1",
            id="dropdown_room_usage",
        ),
            
            html.Br(),
            html.Label('Nachhallzeitdiagramm'),
            dcc.Graph(id="graph-content"),        
        ], style={'padding': 10, 'flex': 1}),

        html.Div(children=[
            html.Label('Placeholder for Graphs'),
            dcc.Graph(id="graph-content"),
            
            html.Br(),
            html.Label('Placeholder for Graphs'),
            dcc.Graph(id="graph-content"),   

        ], style={'padding': 10, 'flex': 1})
    ], style={'display': 'flex', 'flexDirection': 'row'}),
], )#style={'display': 'flex', 'flexDirection': 'row'})

# if __name__ == '__main__':
#     app.run(debug=True)


# app.layout = [
#     html.H1(children="Reverberation Optimization", style={"textAlign": "left"}),
#     dcc.Dropdown(
#         options=[{"label": i, "value": i} for i in df["options"]],
#         value="A1",
#         id="dropdown-selection",
#     ),
#     dcc.Input(
#         id="input_1",
#         type="number",
#         placeholder="Raumvolumen in m^3",
#     ),
#     html.Div(
#         [
#             daq.ToggleSwitch(id="my-toggle-switch", value=False),
#             html.Div(id="my-toggle-switch-output"),
#         ]
#     ),
#     dcc.Input(
#         type="number",
#         placeholder="input type {}".format("number"),
#         id="input_temperature",
#     ),
#     dcc.Input(
#         id="input_3",
#         type="number",
#         placeholder="input type {}".format("number"),
#     ),
#     dcc.Graph(id="graph-content"),
# ]


@callback(
    Output('graph-content', 'figure'),
    Output('my-toggle-switch-output', 'children'),
    Input('dropdown_room_usage', 'value'),
    Input('my-toggle-switch', 'value'),
    Input('input_room_volume', 'value'),
    Input('input_room_temperature', 'value'),
    Input('input_room_height', 'value'),
)

def update_graph(value):
    # dff = df[df.country==value]
    # return px.line(dff, x='year', y='pop')
    # Placeholder for graph update logic
    return px.line(x=[0, 1], y=[0, 1], title=f"Graph for {value}")

def update_output(value):
    return f'The switch is {value}.'

# app.layout = html.Div([
#     daq.ToggleSwitch(
#         id='my-toggle-switch',
#         value=False
#     ),
#     html.Div(id='my-toggle-switch-output')
# ])


# @callback(
#     Output('my-toggle-switch-output', 'children'),
#     Input('my-toggle-switch', 'value')
# )
# def update_output(value):
#     return f'The switch is {value}.'


if __name__ == '__main__':
    app.run(debug=True)
