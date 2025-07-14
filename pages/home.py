"""
This module defines the layout and callbacks for the home page of the reverberation
optimization application. It includes components for inputting room parameters,
defining room surfaces, and visualizing the calculated reverberation time.
"""
import dash
from dash import html, dcc, callback, Input, Output, State, dash_table, clientside_callback
import dash_daq as daq
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from src import reverberation_calc


if not os.environ.get("SPHINX_BUILD"):
    try:
        dash.register_page(__name__, path="/", name="Home", title="Reverbation | Home")
    except dash.exceptions.PageError:
        # This error is expected when the module is imported during test collection
        # before the app is instantiated.
        pass


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
                            className="custom-input",  # Use custom style class
                        ),
                        html.Br(),
                        html.Label(["Room Height", "\u00A0", "m"]),
                        html.Br(),
                        dcc.Input(
                            type="number",
                            # placeholder="3",
                            id="input_room_height",
                            className="custom-input",  # Use custom style class
                        ),
                        html.Br(),
                        html.Label(["Temperature", "\u00A0", "°C"]),
                        html.Br(),
                        dcc.Input(
                            type="number",
                            placeholder="20",
                            id="input_room_temperature",
                            className="custom-input",  # Use custom style class
                        ),
                        html.Br(),
                        html.Label(["Relative Humidity","\u00A0", "%"]),
                        html.Br(),
                        dcc.Input(
                            type="number",
                            placeholder="50",
                            id="input_room_humidity",
                            className="custom-input",  # Use custom style class
                        ),
                        html.Br(),
                        html.Label(["Air Pressure", "\u00A0", "hPa"]),
                        html.Br(),
                        dcc.Input(
                            type="number",
                            placeholder="1013.5",
                            id="input_room_pressure",
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
                            className="my-button no-print",
                        ),
                        html.Div(id="placeholder"),
                    ]
                ),
            ],
            className="no-print",
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
    """Add a new row to the surface definition table.

    This callback is triggered when the "Add Row" button is clicked. It appends a new,
    empty row to the `area-table` DataTable, allowing users to define another room surface.

    Parameters
    ----------
    n_clicks : int
        The number of times the 'add-row-button' has been clicked.
    rows : list
        The existing data in the 'area-table'.

    Returns
    -------
    list
        The updated data for the 'area-table' with the new row added.
    """
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
    """Handle interactions with the main table.

    This callback manages two user interactions:
    1. Opens a material selection modal when the database icon ('💾') is clicked.
    2. Deletes a row from the table when the delete icon ('🗑️') is clicked.

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
    tuple
        A tuple containing the updated modal state, new modal content,
        updated table data, and the stored active row index.
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
                        data=df_materials.to_dict('records'), # type: ignore
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
    """Update the area table with data from the selected material of the material database.

    This callback is triggered when a cell in the material selection modal table is clicked.
    It takes the absorption coefficient data from the selected material and populates the
    corresponding row in the main 'area-table'.

    Parameters
    ----------
    active_cell : dict
        The activated cell in the 'material-selection-table'.
    material_data : list
        The data from the 'material-selection-table'.
    active_row_index : int
        The index of the row in 'area-table' to be updated.
    area_table_data : list
        The current data in the 'area-table'.

    Returns
    -------
    tuple
        A tuple containing the updated 'area-table' data and a boolean to close the modal.
    """
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


@callback(
    Output('input_room_volume', 'value'),
    Input('input_room_volume', 'n_blur'),
    State('input_room_volume', 'value')
)
def round_room_volume(n_blur, value):
    if value is None:
        return None
    try:
        return round(float(value), 2)
    except (ValueError, TypeError):
        return None

@callback(
    Output('input_room_height', 'value'),
    Input('input_room_height', 'n_blur'),
    State('input_room_height', 'value')
)
def round_room_height(n_blur, value):
    if value is None:
        return None
    try:
        return round(float(value), 2)
    except (ValueError, TypeError):
        return None

@callback(
    Output('input_room_temperature', 'value'),
    Input('input_room_temperature', 'n_blur'),
    State('input_room_temperature', 'value')
)
def round_room_temperature(n_blur, value):
    if value is None:
        return None
    try:
        return round(float(value), 2)
    except (ValueError, TypeError):
        return None

@callback(
    Output('input_room_humidity', 'value'),
    Input('input_room_humidity', 'n_blur'),
    State('input_room_humidity', 'value')
)
def round_room_humidity(n_blur, value):
    if value is None:
        return None
    try:
        return round(float(value), 2)
    except (ValueError, TypeError):
        return None

@callback(
    Output('input_room_pressure', 'value'),
    Input('input_room_pressure', 'n_blur'),
    State('input_room_pressure', 'value')
)
def round_room_pressure(n_blur, value):
    if value is None:
        return None
    try:
        return round(float(value), 2)
    except (ValueError, TypeError):
        return None


@callback(
    Output('area-table', 'data', allow_duplicate=True),
    Input('area-table', 'data_timestamp'),
    State('area-table', 'data'),
    State('area-table', 'data_previous'),
    prevent_initial_call=True
)
def validate_and_format_table_data(timestamp, data, data_previous):
    """
    Validate and format the data in the area-table.
    Ensures that area and alpha values are numeric and rounded to two decimal places.
    Reverts invalid inputs to their previous state.
    """
    if data is None or data_previous is None:
        raise dash.exceptions.PreventUpdate

    # If a row was added or deleted, the lengths will be different.
    # In this case, we don't want to validate, so we allow the update to proceed
    # without modification from this callback.
    if len(data) != len(data_previous):
        return data

    # Find the changed cell
    changed_row_idx, changed_col_id = -1, ''
    for i in range(len(data)):
        # Using .get() to avoid KeyErrors if a column was somehow removed
        diff_keys = [key for key in data[i] if data[i].get(key) != data_previous[i].get(key)]
        if diff_keys:
            changed_row_idx = i
            changed_col_id = diff_keys[0]
            break

    if changed_row_idx == -1:
        raise dash.exceptions.PreventUpdate

    # List of columns to validate
    editable_numeric_cols = [f'col-{i}' for i in range(2, 13) if i not in [3, 4]]

    if changed_col_id in editable_numeric_cols:
        value = data[changed_row_idx][changed_col_id]
        prev_value = data_previous[changed_row_idx][changed_col_id]

        if isinstance(value, str):
            cleaned_value = value.replace(',', '.').strip()
            if cleaned_value == '':
                # Allow user to clear the cell
                return data

            # Check for valid float format
            if cleaned_value.count('.') <= 1 and (cleaned_value.replace('.', '', 1).isdigit() or (cleaned_value.startswith('-') and cleaned_value[1:].replace('.', '', 1).isdigit())):
                try:
                    num_value = float(cleaned_value)
                    data[changed_row_idx][changed_col_id] = round(num_value, 2)
                except (ValueError, TypeError):
                    # Revert if conversion fails
                    data[changed_row_idx][changed_col_id] = prev_value
            else:
                # Revert if format is invalid
                data[changed_row_idx][changed_col_id] = prev_value
        elif isinstance(value, (int, float)):
            data[changed_row_idx][changed_col_id] = round(value, 2)
        # If value is None or other type, and it's a change, revert it.
        elif value != prev_value:
             data[changed_row_idx][changed_col_id] = prev_value


    return data


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
    """Update the graph based on all user inputs by calling the calculation module.

    This callback gathers all room parameters and surface definitions from the user interface,
    passes them to the `reverberation_calc` module for calculation, and plots the resulting
    reverberation time on the graph. It also plots target reverberation time ranges based on
    DIN 18041 if a room usage type is selected.

    Parameters
    ----------
    table_data : list[dict]
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
        Selected room usage type from the dropdown.
    air_damp_activated : bool
        State of the air dampening toggle switch.

    Returns
    -------
    plotly.graph_objects.Figure
        An updated Plotly figure with the calculated reverberation time.
    """
    # Helper to convert input to float, handling commas.
    def to_float(value, default):
        if value is None or value == '':
            return default
        try:
            return float(str(value).replace(',', '.'))
        except (ValueError, TypeError):
            return default

    # Default values for numeric inputs
    volume = to_float(volume, 30)
    height = to_float(height, None)
    temp = to_float(temp, 20)
    humidity = to_float(humidity, 50)
    pressure = to_float(pressure, 1013.25) # hPa

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
        yaxis_title="Reverberation Time in s",
        yaxis=dict(range=[0, None]),
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
                    # The validation callback should have already formatted the numbers,
                    # but this is a safeguard.
                    if isinstance(val, str):
                        val = val.replace(',', '.').strip()
                    try:
                        # Return NaN if the value is an empty string or cannot be converted
                        if val == '' or val is None:
                            return np.nan
                        return float(val)
                    except (ValueError, TypeError):
                        return np.nan

                area = safe_float(row.get('col-2'))
                if area is not None and area > 0 and not np.isnan(area):
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
            
        if not df_target.empty and (df_target['T_max'] > 0).any() and room_usage.startswith('B'):
            # Find the first and last indices where T_max is greater than 0
            non_zero_indices = df_target.index[df_target['T_max'] > 0]
            first_index = non_zero_indices[0]
            last_index = non_zero_indices[-1]

            # Get the corresponding frequencies
            first_freq = df_target.loc[first_index, 'Frequency']
            last_freq = df_target.loc[last_index, 'Frequency']

            # Create new rows to form a rectangle
            start_rect_row = pd.DataFrame([{'Frequency': first_freq, 'T_max': 0, 'T_min': 0}])
            end_rect_row = pd.DataFrame([{'Frequency': last_freq, 'T_max': 0, 'T_min': 0}])

            # Insert the new rows into the DataFrame
            df_target = pd.concat([
                df_target.iloc[:first_index],
                start_rect_row,
                df_target.iloc[first_index:last_index + 1],
                end_rect_row,
                df_target.iloc[last_index + 1:]
            ]).reset_index(drop=True)


        # Plotting
        fig.add_trace(go.Scatter(
            x=df_reverb['Frequency'], 
            y=df_reverb['Reverberation Time'],
            mode='lines+markers',
            name='Reverberation Time',
            line=dict(color='#3DED97', width=3)
        ))
        
        if not df_target.empty:
            fig.add_trace(go.Scatter(
                x=df_target['Frequency'],
                y=df_target['T_max'],
                fill=None,
                mode='lines',
                line_color='rgba(255,107,107,0.5)',
                showlegend=False
            ))
            fig.add_trace(go.Scatter(
                x=df_target['Frequency'],
                y=df_target['T_min'],
                fill='tonexty', # fill area between trace0 and trace1
                mode='lines',
                line_color='rgba(255,107,107,0.5)',
                name='Tolerance Range',
            ))

        fig.update_layout(
            title_text="Reverberation Time Calculation with DIN 18041 requirements",
            xaxis_title="Frequency in Hz",
            yaxis_title="Reverberation Time in s",
            yaxis=dict(range=[0, None]),
            xaxis=dict(
                type='log',
                tickvals=frequency_bands,
                ticktext=[str(f) for f in frequency_bands],
                range=[np.log10(50), np.log10(10000)]  # Also set range here for consistency
            ),
            legend=dict(
                orientation="h", 
                yanchor="bottom", 
                y=1.02, 
                xanchor="right", 
                x=1,
                itemclick=False,
                itemdoubleclick=False
                )
        )

    except Exception as e:
        fig.update_layout(title_text=f"An error occurred: {e}")

    return fig


# Clientside callback to trigger browser print
clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks > 0) {
            window.print();
        }
        return '';
    }
    """,
    Output('placeholder', 'children'),
    Input('export', 'n_clicks'),
    prevent_initial_call=True
)