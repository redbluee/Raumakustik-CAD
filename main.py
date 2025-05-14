from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import dash_daq as daq


df = pd.DataFrame({'options': ['A1', 'A2','A3','A4','A5', 'B1', 'B2','B3','B4','B5']}) # Create a DataFrame with a column named 'options'

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = [
    html.H1(children="Reverberation Optimization", style={"textAlign": "left"}),
    dcc.Dropdown(
        options=[{"label": i, "value": i} for i in df["options"]],
        value="A1",
        id="dropdown-selection",
    ),
    dcc.Input(
        id="input_1",
        type="number",
        placeholder="input type {}".format("number"),
    ),
    html.Div(
        [
            daq.ToggleSwitch(id="my-toggle-switch", value=False),
            html.Div(id="my-toggle-switch-output"),
        ]
    ),
    dcc.Input(
        id="input_2",
        type="number",
        placeholder="input type {}".format("number"),
    ),
    dcc.Input(
        id="input_3",
        type="number",
        placeholder="input type {}".format("number"),
    ),
    dcc.Graph(id="graph-content"),
]


@callback(
    Output('graph-content', 'figure'),
    Output('my-toggle-switch-output', 'children'),
    Input('dropdown-selection', 'value'),
    Input('my-toggle-switch', 'value'),
    Input('input_1', 'value'),
    Input('input_2', 'value'),
    Input('input_3', 'value'),
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
