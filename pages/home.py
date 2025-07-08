import dash
from dash import html, dcc, callback, Input, Output, State, dash_table
import dash_daq as daq
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px
import os


if not os.environ.get("SPHINX_BUILD"):
    dash.register_page(__name__, path="/", name="Home", title="Reverbation | Home")


# Define Dropdown Data
df_room_usage = pd.DataFrame(
    {"options": ["A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3", "B4", "B5"]}
)

# Define table columns
column_definitions = []
column_definitions.append({"name": "Surface Label", "id": "col-1", "editable": True})
column_definitions.append({"name": "Area m²", "id": "col-2", "editable": True})
column_definitions.append({"name": "DB", "id": "col-3", "editable": False})
column_definitions.append({"name": "Sound absorber", "id": "col-4", "editable": True})
column_definitions.append({"name": "α₆₃", "id": "col-5", "editable": True})
column_definitions.append({"name": "α₁₂₅", "id": "col-6", "editable": True})
column_definitions.append({"name": "α₂₅₀", "id": "col-7", "editable": True})
column_definitions.append({"name": "α₅₀₀", "id": "col-8", "editable": True})
column_definitions.append({"name": "α₁₀₀₀", "id": "col-9", "editable": True})
column_definitions.append({"name": "α₂₀₀₀", "id": "col-10", "editable": True})
column_definitions.append({"name": "α₄₀₀₀", "id": "col-11", "editable": True})
column_definitions.append({"name": "α₈₀₀₀", "id": "col-12", "editable": True}) 

# Add the delete column as the last one
column_definitions.append({"name": "", "id": "col-delete", "editable": False})
table_columns = column_definitions

# Define the initial empty row with icons
initial_empty_row = {f"col-{i+1}": "💾" if f"col-{i+1}" == "col-3" else "" for i in range(12)}
initial_empty_row["col-3"] = "💾" 
initial_empty_row["col-delete"] = "🗑️"


# Page Layout
layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col([html.H1("Reverberation Optimization", className="app-brand")]),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5(children="Room parameters"),
                        html.Label(["Room Volume", "\u00A0", "m", html.Sup("3")]),
                        html.Br(),
                        dcc.Input(
                            type="number",
                            placeholder="30",
                            id="input_room_volume",
                            min=0,
                            className="custom-input",  # Use custom style class
                        ),
                        html.Br(),
                        html.Label(["Room Height", "\u00A0", "m"]),
                        html.Br(),
                        dcc.Input(
                            type="number",
                            placeholder="20",
                            id="input_room_height",
                            min=0,
                            className="custom-input",  # Use custom style class
                        ),
                        html.Br(),
                        html.Label(["Temperature", "\u00A0", "°C"]),
                        html.Br(),
                        dcc.Input(
                            type="number",
                            placeholder="20",
                            id="input_room_temperature",
                            min=0,
                            className="custom-input",  # Use custom style class
                        ),
                        html.Br(),
                        html.Label("Relative Humidity\u00A0%"),
                        html.Br(),
                        dcc.Input(
                            type="number",
                            placeholder="50",
                            id="input_room_humidity",
                            min=0,
                            className="custom-input",  # Use custom style class
                        ),
                        html.Br(),
                        html.Label("Air Pressure\u00A0hPa"),
                        html.Br(),
                        dcc.Input(
                            type="number",
                            placeholder="101.35",
                            id="input_room_pressure",
                            min=0,
                            className="custom-input",  # Use custom style class
                        ),
                        html.Br(),
                        html.Label("Room Usage Type"),
                        html.Br(),
                        dcc.Dropdown(
                            options=[
                                {"label": i, "value": i}
                                for i in df_room_usage["options"]
                            ],
                            value="A1",
                            id="dropdown_room_usage",
                            className="custom-dropdown", # Use custom style class
                        ),
                        html.Div(
                            [
                                daq.ToggleSwitch(
                                    id="my-toggle-switch",
                                    value=False,
                                    color="#3DED97",
                                    size=40,
                                    theme={"dark": True},
                                )
                            ],
                            style={"textAlign": "left"},
                        ),
                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                        dcc.Loading(
                            id="nachhallzeit-graph",
                            type="circle",
                            children=dcc.Graph(
                                id="fig-transformed", className="my-graph"
                            ),
                        )
                    ],
                    width=6,
                    className="multi-graph",
                ),
                dbc.Col(
                    [
                        html.H5(children="Report Generation"),
                        html.Button(
                            "Export PDF",
                            id="export",
                            n_clicks=0,
                            title="The grid search may take several minutes",
                            className="my-button",
                        ),
                    ],
                    width=2,
                    style={"text-align": "left", "margin": "5px 1px 1px 1px"},
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5(children="Definition of Room Surfaces"),
                        dash_table.DataTable(
                            id="flächen-tabelle",
                            columns=table_columns,
                            data=[initial_empty_row],
                            editable=True,
                            row_deletable=False,  # MODIFIED: Disable default delete
                            style_table={"overflowX": "auto", "minWidth": "100%"},
                            style_cell={
                                "textAlign": "left",
                                "padding": "5px",
                                "backgroundColor": "#0e2a2e",
                                "color": "#f6f6f6",
                                "border": "1px solid #042f33",
                            },
                            style_header={
                                "backgroundColor": "#042f33",
                                "fontWeight": "bold",
                                "color": "#f6f6f6",
                                "border": "1px solid #3DED97",
                            },
                            style_data_conditional=[
                                {
                                    "if": {"row_index": "odd"},
                                    "backgroundColor": "#0c262a",
                                },
                                {
                                    # DB Icon
                                    "if": {"column_id": "col-3"},
                                    "textAlign": "center",
                                    "cursor": "pointer",
                                    "fontWeight": "bold",
                                    # "color": "#3DED97",
                                },
                                {
                                    # Delete Icon
                                    "if": {"column_id": "col-delete"},
                                    "textAlign": "center",
                                    "cursor": "pointer",
                                    "fontWeight": "bold",
                                    # "color": "#FF6B6B",
                                },
                            ],
                        ),
                        html.Button(
                            "Add Row",
                            id="add-fläche-row-button",
                            n_clicks=0,
                            className="my-button",
                            style={"marginTop": "10px"},
                        ),
                    ]
                ),
            ]
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle("Material selection"), 
                    close_button=True, 
                    style={"backgroundColor": "white", "color": "black"}
                ),
                dbc.ModalBody(id="details-modal-body-content"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id="close-details-modal-button",
                        className="ml-auto my-button",
                        n_clicks=0,
                    )
                ),
            ],
            id="details-modal",
            centered=True,
            is_open=False,
        ),
    ]
)


# Page Callbacks

# Callback for adding a row
@callback(
    Output('flächen-tabelle', 'data', allow_duplicate=True), # allow_duplicate needed if another callback modifies data
    Input('add-fläche-row-button', 'n_clicks'),
    State('flächen-tabelle', 'data'),
    prevent_initial_call=True
)
def add_row_to_flächen_tabelle(n_clicks, rows):
    if rows is None:
        rows = []
    new_row_data = {f"col-{i+1}": "💾" if f"col-{i+1}" == "col-3" else "" for i in range(12)}
    new_row_data["col-delete"] = "🗑️" # Add delete icon to new rows
    rows.append(new_row_data)
    return rows

# Callback to open/close modal AND handle custom row deletion
@callback(
    Output("details-modal", "is_open"),
    Output("details-modal-body-content", "children"),
    Output('flächen-tabelle', 'data', allow_duplicate=True), # Keep allow_duplicate if other callbacks modify data
    Input("flächen-tabelle", "active_cell"),
    Input("close-details-modal-button", "n_clicks"),
    State("details-modal", "is_open"),
    State("flächen-tabelle", "data"), 
    prevent_initial_call=True
)
def handle_table_interactions(active_cell, close_clicks, modal_is_open, table_data):
    """
    Handle interactions with the main table, including opening the modal and deleting rows.

    Parameters
    ----------
    active_cell : dict
        The currently active cell in the table.
    close_clicks : int
        Number of clicks on the close button.
    modal_is_open : bool
        Current state of the modal.
    table_data : list
        Current data in the table.

    Returns
    -------
    new_modal_state : bool
        Updated state of the modal.
    new_modal_content : dash_html_components.Component
        Content to display in the modal.
    new_table_data : list
        Updated data for the table after deletion.
    """
    
    
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    new_modal_state = modal_is_open
    new_modal_content = dash.no_update
    new_table_data = dash.no_update 

    if triggered_id == "close-details-modal-button":
        new_modal_state = False
        return new_modal_state, new_modal_content, new_table_data

    if active_cell and table_data:
        row_index = active_cell["row"]
        col_id = active_cell["column_id"]

        if row_index < len(table_data):
            # Click action on DB icon in the main table
            if col_id == "col-3":
                selected_row_data = table_data[row_index]

                # Prepare columns for the modal table:
                # table_columns is defined globally
                modal_table_display_columns = []
                for col_def in table_columns:
                    if col_def['id'] not in ['col-3', 'col-delete']: # Exclude DB and Delete columns
                        modal_col = col_def.copy()
                        modal_col['editable'] = False # Make all columns non-editable in the modal
                        modal_table_display_columns.append(modal_col)
                
                # The data for the modal table is the single selected row, wrapped in a list
                modal_table_display_data = [selected_row_data]
                
                # Modal style_data_conditional
                modal_s_d_c = []

                modal_table_component = dash_table.DataTable(
                    id='modal-detail-display-table', 
                    columns=modal_table_display_columns,
                    data=modal_table_display_data,
                    style_table={'overflowX': 'auto', 'minWidth': '100%'},
                    style_cell={ 
                        'textAlign': 'left',
                        'padding': '5px',
                        'color': 'black',
                        'border': '1px solid black'
                    },
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'color': 'black',
                        'fontWeight': 'bold',
                        'border': '1px solid black'
                    },
                    style_data_conditional=modal_s_d_c,
                )
                
                new_modal_content = modal_table_component
                new_modal_state = True
            
            elif col_id == "col-delete": # Click on Delete icon in the main table
                updated_rows = [row for i, row in enumerate(table_data) if i != row_index]
                new_table_data = updated_rows
                new_modal_state = False 
                return new_modal_state, new_modal_content, new_table_data
        
    return new_modal_state, new_modal_content, new_table_data


# Existing Callbacks
@callback(
    Output('fig-transformed', 'figure'),
    Input("dropdown_room_usage", "value"),
    Input("my-toggle-switch", "value"),
    Input("input_room_volume", "value"),
    Input("input_room_temperature", "value"),
    Input("input_room_height", "value"),
)
def update_graph(room_usage, switch_value, volume, temp, height):
    """
    Update the graph based on user inputs.

    Parameters
    ----------
    room_usage : str
        Selected room usage type.
    switch_value : bool
        State of the toggle switch.
    volume : float
        Room volume in cubic meters.
    temp : float
        Room temperature in degrees Celsius.
    height : float
        Room height in meters.

    Returns
    -------
    fig : plotly.graph_objects.Figure
        Updated figure with new data.
    """
    
    title = (
        f"Usage Type: {room_usage}, Switch: {switch_value}, "
        f"Vol: {volume}, Temp: {temp}, Height: {height}"
    )
    y_values = [
        float(volume) if volume not in [None, ""] else 0,
        float(temp) if temp not in [None, ""] else 0,
        float(height) if height not in [None, ""] else 0
    ]
    fig = px.line(x=[0, 1, 2], y=y_values, title=title)
    return fig