import dash
from dash import html, dcc, callback, Input, Output, State, dash_table
import dash_daq as daq
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import reverberation_calc


if not os.environ.get("SPHINX_BUILD"):
    dash.register_page(__name__, path="/", name="Home", title="Reverbation | Home")


# Load material database
try:
    df_materials = pd.read_csv("materials.csv")
except FileNotFoundError:
    df_materials = pd.DataFrame()

# Define Dropdown Data
df_room_usage = pd.DataFrame(
    {"options": ["no requirements", "A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3", "B4", "B5"]}
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
        dcc.Store(id='active-row-index-store'),
        dbc.Row(
            [
                dbc.Col([html.H1("RoomAcousticWizard", className="app-brand")]),
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
                            placeholder="3",
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
                        html.Label(["Relative Humidity","\u00A0", "%"]),
                        html.Br(),
                        dcc.Input(
                            type="number",
                            placeholder="50",
                            id="input_room_humidity",
                            min=0,
                            className="custom-input",  # Use custom style class
                        ),
                        html.Br(),
                        html.Label(["Air Pressure", "\u00A0", "hPa"]),
                        html.Br(),
                        dcc.Input(
                            type="number",
                            placeholder="1013.5",
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
                            value="no requirements",
                            id="dropdown_room_usage",
                            clearable=False,
                            searchable=False,
                            className="custom-dropdown", # Use custom style class
                        ),
                        html.Div(
                            [
                                html.Br(),
                                html.Label("Activate Air Damp"),
                                html.Div(
                                    [
                                        html.Span("Off"),
                                        daq.ToggleSwitch(
                                            id="my-toggle-switch",
                                            value=False,
                                            color="#3DED97",
                                            size=40,
                                            theme={"dark": True},
                                        ),
                                        html.Span("On"),
                                    ],
                                    style={
                                        "display": "flex",
                                        "align-items": "center",
                                        "gap": "10px",
                                    },
                                ),
                            ],
                            style={"textAlign": "left"},
                        ),
                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                        dcc.Loading(
                            id="reverberation-graph",
                            type="circle",
                            children=dcc.Graph(
                                id="fig-transformed",
                                className="my-graph",
                                style={'height': '600px'}
                            ),
                        )
                    ],
                    width=9,
                    className="multi-graph",
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Br(),
                        html.H5(children="Definition of Room Surfaces"),
                        dash_table.DataTable(
                            id="area-table",
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
                                'whiteSpace': 'normal',
                                'height': 'auto',
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
                            id="add-row-button",
                            n_clicks=0,
                            className="my-button",
                            style={"marginTop": "10px"},
                        ),
                    ]
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Br(),
                        html.H5(children="Report Generation"),
                        html.Button(
                            "Export PDF",
                            id="export",
                            n_clicks=0,
                            title="The grid search may take several minutes",
                            className="my-button",
                        ),
                    ],
                    width=8,
                    style={"text-align": "left", "margin": "5px 1px 1px 1px"},
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
            size="xl",
        ),
    ]
)


# Page Callbacks

# Callback for adding a row
@callback(
    Output('area-table', 'data', allow_duplicate=True), # allow_duplicate needed if another callback modifies data
    Input('add-row-button', 'n_clicks'),
    State('area-table', 'data'),
    prevent_initial_call=True
)
def add_row_to_surface_table(n_clicks, rows):
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
    Output('area-table', 'data', allow_duplicate=True), # Keep allow_duplicate if other callbacks modify data
    Output('active-row-index-store', 'data'),
    Input("area-table", "active_cell"),
    Input("close-details-modal-button", "n_clicks"),
    State("details-modal", "is_open"),
    State("area-table", "data"), 
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
    stored_row_index = dash.no_update

    if triggered_id == "close-details-modal-button":
        new_modal_state = False
        return new_modal_state, new_modal_content, new_table_data, stored_row_index

    if active_cell and table_data:
        row_index = active_cell["row"]
        col_id = active_cell["column_id"]

        if row_index < len(table_data):
            # Click action on DB icon in the main table
            if col_id == "col-3":
                stored_row_index = row_index
                if not df_materials.empty:
                    modal_table_component = dash_table.DataTable(
                        id='material-selection-table',
                        columns=[{"name": i, "id": i} for i in df_materials.columns],
                        data=df_materials.to_dict('records'),
                        style_table={'overflowY': 'auto', 'height': '400px', 'overflowX': 'auto', 'minWidth': '100%'},
                        style_cell={
                            'textAlign': 'left',
                            'padding': '5px',
                            'color': 'black',
                            'border': '1px solid black',
                            'whiteSpace': 'normal',
                            'height': 'auto'
                        },
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'color': 'black',
                            'fontWeight': 'bold',
                            'border': '1px solid black'
                        },
                    )
                    new_modal_content = html.Div(
                        modal_table_component, 
                        className='material-table-container'
                    )
                else:
                    new_modal_content = html.Div("Material database (materials.csv) not found.")
                
                new_modal_state = True
            
            elif col_id == "col-delete": # Click on Delete icon in the main table
                updated_rows = [row for i, row in enumerate(table_data) if i != row_index]
                new_table_data = updated_rows
                new_modal_state = False 
                return new_modal_state, new_modal_content, new_table_data, stored_row_index
        
    return new_modal_state, new_modal_content, new_table_data, stored_row_index


# Callback to update area-table with selected material
@callback(
    Output('area-table', 'data', allow_duplicate=True),
    Output('details-modal', 'is_open', allow_duplicate=True),
    Input('material-selection-table', 'active_cell'),
    State('material-selection-table', 'data'),
    State('active-row-index-store', 'data'),
    State('area-table', 'data'),
    prevent_initial_call=True
)
def update_area_table_with_material(active_cell, material_data, active_row_index, area_table_data):
    if not active_cell or active_row_index is None:
        return dash.no_update, dash.no_update

    selected_material_row_index = active_cell['row']
    selected_material = material_data[selected_material_row_index]

    # The row from area-table to be updated
    target_row = area_table_data[active_row_index]

    # Update the values
    target_row['col-4'] = selected_material['name']
    target_row['col-5'] = selected_material['63']
    target_row['col-6'] = selected_material['125']
    target_row['col-7'] = selected_material['250']
    target_row['col-8'] = selected_material['500']
    target_row['col-9'] = selected_material['1000']
    target_row['col-10'] = selected_material['2000']
    target_row['col-11'] = selected_material['4000']
    target_row['col-12'] = selected_material['8000']

    # Close modal
    return area_table_data, False


# Connect all inputs to the calculation module and update the graph
@callback(
    Output('fig-transformed', 'figure'),
    [
        Input('area-table', 'data'),
        Input("input_room_volume", "value"),
        Input("input_room_height", "value"),
        Input("input_room_temperature", "value"),
        Input("input_room_humidity", "value"),
        Input("input_room_pressure", "value"),
        Input("dropdown_room_usage", "value"),
        Input("my-toggle-switch", "value"),
    ]
)
def update_graph_with_calculation(table_data, volume, height, temp, humidity, pressure, room_usage, air_damp_activated):
    """
    Update the graph based on all user inputs by calling the calculation module.

    Parameters
    ----------
    table_data : list of dicts
        Data from the surface definition table.
    volume : float
        Room volume in cubic meters.
    height : float, optional
        Room height in meters.
    temp : float
        Room temperature in degrees Celsius.
    humidity : float
        Relative humidity in percent.
    pressure : float
        Air pressure in hPa.
    room_usage : str
        Selected room usage type.
    air_damp_activated : bool
        State of the air dampening toggle switch.

    Returns
    -------
    fig : plotly.graph_objects.Figure
        Updated figure with calculated reverberation time.
    """
    # Default values for numeric inputs
    volume = float(volume) if volume is not None else 30
    height = float(height) if height is not None else None
    temp = float(temp) if temp is not None else 20
    humidity = float(humidity) if humidity is not None else 50
    pressure = float(pressure) if pressure is not None else 1013.25 # hPa

    # Standard octave bands for the x-axis
    frequency_bands = [63, 125, 250, 500, 1000, 2000, 4000, 8000]

    # Create a default empty figure and pre-format the axes
    fig = go.Figure()
    fig.update_layout(
        title_text="Please provide room volume and surface data for calculation",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#f6f6f6",
        xaxis=dict(
            type='log',
            tickvals=frequency_bands,
            ticktext=[str(f) for f in frequency_bands],
            title_text="Frequency in Hz",
            range=[np.log10(50), np.log10(10000)]  # Set a fixed range for log axis
        ),
        yaxis_title="Reverberation Time in s"
    )

    if not volume or not table_data:
        return fig

    try:
        # Create Room Object
        calc_room = reverberation_calc.room(volume)
        if height:
            calc_room.set_height(height)
        calc_room.set_temperature(temp)
        calc_room.set_rel_humidity(humidity)
        calc_room.set_pressure(pressure / 10) # Convert hPa to kPa

        # Create Surface Objects
        surfaces = []
        for row in table_data:
            try:
                # Use a helper to safely convert values to float, defaulting to np.nan for empty strings
                def safe_float(val):
                    try:
                        # Return NaN if the value is an empty string or cannot be converted
                        if val == '':
                            return np.nan
                        return float(val)
                    except (ValueError, TypeError):
                        return np.nan

                area = safe_float(row.get('col-2'))
                if area > 0 and not np.isnan(area):
                    absorb_coeffs = [
                        safe_float(row.get('col-5')),
                        safe_float(row.get('col-6')),
                        safe_float(row.get('col-7')),
                        safe_float(row.get('col-8')),
                        safe_float(row.get('col-9')),
                        safe_float(row.get('col-10')),
                        safe_float(row.get('col-11')),
                        safe_float(row.get('col-12'))
                    ]
                    mat_name = row.get('col-4') or "Unnamed Material"
                    surface_name = row.get('col-1') or "Unnamed Surface"
                    
                    material = reverberation_calc.material(mat_name, absorb_coeffs)
                    surface = reverberation_calc.surface(surface_name, area, material)
                    surfaces.append(surface)
            except (ValueError, TypeError):
                # This will now primarily catch issues if the row structure is unexpected
                continue

        if not surfaces:
            fig.update_layout(title_text="Valid surface data is required for calculation.")
            return fig

        # Calculate reverberation time
        reverb_obj = reverberation_calc.reverberation_time(calc_room, surfaces, air_damp_calc=air_damp_activated)
        df_reverb = pd.DataFrame({
            'Frequency': reverb_obj.frequency_bands,
            'Reverberation Time': reverb_obj.reverberation_time
        })

        # Get target reverberation time range
        if room_usage != "no requirements":
            limits = reverberation_calc.DIN_18041_limits(calc_room, room_usage)
            df_target = pd.DataFrame({
                'Frequency': reverb_obj.frequency_bands,
                'T_max': limits.T_upper_limit,
                'T_min': limits.T_lower_limit
            })
        else:
            df_target = pd.DataFrame()


        # Plotting
        fig.add_trace(go.Scatter(
            x=df_reverb['Frequency'], 
            y=df_reverb['Reverberation Time'],
            mode='lines+markers',
            name='Reverberation Time (T)',
            line=dict(color='#3DED97', width=3)
        ))
        
        if not df_target.empty:
            fig.add_trace(go.Scatter(
                x=df_target['Frequency'],
                y=df_target['T_max'],
                fill=None,
                mode='lines',
                line_color='rgba(255,107,107,0.5)',
                name='Target Range (Upper)'
            ))
            fig.add_trace(go.Scatter(
                x=df_target['Frequency'],
                y=df_target['T_min'],
                fill='tonexty', # fill area between trace0 and trace1
                mode='lines',
                line_color='rgba(255,107,107,0.5)',
                name='Target Range (Lower)'
            ))

        fig.update_layout(
            title_text="Reverberation Time Calculation with DIN 18041 requirements",
            xaxis_title="Frequency (Hz)",
            yaxis_title="Reverberation Time (s)",
            xaxis=dict(
                type='log',
                tickvals=frequency_bands,
                ticktext=[str(f) for f in frequency_bands],
                range=[np.log10(50), np.log10(10000)]  # Also set range here for consistency
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

    except Exception as e:
        fig.update_layout(title_text=f"An error occurred: {e}")

    return fig