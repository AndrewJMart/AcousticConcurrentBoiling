from dash import Dash, html, dcc, callback, Output, Input, State
import dash 
import plotly.graph_objs as go
import pandas as pd
import os

SOURCEFILE = './SortedData/'
FINALDESTINATION = './HandLabeledData/'

FolderDropDownOptions = os.listdir(SOURCEFILE)

app = Dash()

app.layout = html.Div(
    style={
        'fontFamily': 'Arial, sans-serif',
        'padding': '40px',
        'backgroundColor': '#f9f9f9',
        'borderRadius': '10px',
        'boxShadow': '0 0 10px rgba(0,0,0,0.1)',
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'height': '100vh'
    },
    children=[
        html.H2("File Selection and Graph Plotter", style={'textAlign': 'center', 'color': '#333'}),

        html.Div([ 
            html.Label("Select Folder:", style={'marginBottom': '8px', 'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='Folder-Dropdown',
                options=[{'label': folder, 'value': folder} for folder in FolderDropDownOptions],
                placeholder="Choose a folder",
                style={'marginBottom': '20px', 'width': '100%'}
            ),
        ], style={'width': '300px', 'marginBottom': '20px'}),

        html.Div([
            html.Label("Select File:", style={'marginBottom': '8px', 'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='File-Dropdown',
                placeholder="Select a file after choosing folder",
                style={'marginBottom': '20px', 'width': '100%'}
            ),
        ], style={'width': '300px', 'marginBottom': '20px'}),

        html.Div([
            html.Label("Select Rhythm Type:", style={'marginBottom': '8px', 'fontWeight': 'bold'}),
            dcc.RadioItems(
                id='rhythm-selector',
                options=[
                    {'label': 'Rhythm 1', 'value': 'Rhythm 1'},
                    {'label': 'Rhythm 2', 'value': 'Rhythm 2'}
                ],
                value='Rhythm 1',
                style={'marginBottom': '20px'}
            ),
        ], style={'width': '300px', 'marginBottom': '20px'}),

        html.Div([
            dcc.Graph(
                id='Interactive-Plot',
                config={
                    'modeBarButtonsToRemove': [],
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToAdd': [],
                    'scrollZoom': True
                },
                style={'height': '70vh', 'width': '90%', 'maxWidth': '1200px'}
            )
        ], style={'width': '100%', 'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'marginTop': '30px'}),

        dcc.Store(id='peak-store', data=[]),
        
        dcc.Store(id='zoom-store', data={}),
        
        dcc.Store(id='dragmode-store', data={'dragmode': 'zoom'}),

        html.Div([
            html.Button("Save Peaks as CSV", id='save-button', n_clicks=0, style={
                'marginRight': '10px', 'padding': '10px 20px', 'fontWeight': 'bold'
            }),
            html.Button("Reset Peaks", id='reset-button', n_clicks=0, style={
                'padding': '10px 20px', 'fontWeight': 'bold', 'backgroundColor': '#e74c3c', 'color': 'white'
            }),
        ], style={'marginTop': '20px'}),

        html.Div(id='save-status', style={'marginTop': '10px', 'color': 'green'})
    ]
)

@app.callback(
    Output('File-Dropdown', 'options'),
    Output('peak-store', 'data', allow_duplicate=True),
    Output('zoom-store', 'data', allow_duplicate=True),
    Output('dragmode-store', 'data', allow_duplicate=True),
    Input('Folder-Dropdown', 'value'),
    prevent_initial_call=True 
)
def update_file_dropdown_and_reset_peaks(folder):
    if folder is None:
        return [], [], {}, {'dragmode': 'zoom'}
    file_path = os.path.join(SOURCEFILE, folder)
    files = os.listdir(file_path)

    return [{'label': file, 'value': file} for file in files], [], {}, {'dragmode': 'zoom'}

@app.callback(
    Output('peak-store', 'data', allow_duplicate=True),
    Output('zoom-store', 'data', allow_duplicate=True),
    Output('dragmode-store', 'data', allow_duplicate=True),
    Input('File-Dropdown', 'value'),
    prevent_initial_call=True
)
def reset_peaks_on_file_change(file):
    if file:
        return [], {}, {'dragmode': 'zoom'}
    return dash.no_update, dash.no_update, dash.no_update

@app.callback(
    Output('peak-store', 'data', allow_duplicate=True),
    Output('zoom-store', 'data', allow_duplicate=True),
    Output('dragmode-store', 'data', allow_duplicate=True),
    Input('Interactive-Plot', 'clickData'),
    Input('reset-button', 'n_clicks'),
    Input('Interactive-Plot', 'relayoutData'),
    State('peak-store', 'data'),
    State('rhythm-selector', 'value'),
    State('zoom-store', 'data'),
    State('dragmode-store', 'data'),
    prevent_initial_call=True
)
def handle_peaks_and_zoom(clickData, reset_clicks, relayoutData, current_peaks, rhythm_type, zoom_data, dragmode_data):
    ctx = dash.callback_context

    if ctx.triggered and ctx.triggered[0]['prop_id'] == 'reset-button.n_clicks':
        return [], zoom_data, dragmode_data

    if relayoutData:
        if 'dragmode' in relayoutData:
            dragmode_data['dragmode'] = relayoutData['dragmode']
        
        if 'xaxis.autorange' in relayoutData or 'yaxis.autorange' in relayoutData:
            zoom_data = {}
        elif any(key in relayoutData for key in ['xaxis.range[0]', 'xaxis.range[1]', 'yaxis.range[0]', 'yaxis.range[1]']):
            zoom_data.update(relayoutData)

    if not clickData:
        return current_peaks, zoom_data, dragmode_data

    point = clickData['points'][0]
    time_val = point['x']
    y_val = point['y']
    new_peak = {'Time': time_val, 'Value': y_val, 'Rhythm': rhythm_type}

    if not any(peak['Time'] == time_val and peak['Rhythm'] == rhythm_type for peak in current_peaks):
        current_peaks.append(new_peak)

    return current_peaks, zoom_data, dragmode_data

@app.callback(
    Output('Interactive-Plot', 'figure'),
    Input('Folder-Dropdown', 'value'),
    Input('File-Dropdown', 'value'),
    Input('peak-store', 'data'),
    State('zoom-store', 'data'),
    State('dragmode-store', 'data')
)
def update_plot(folder, file, peak_data, zoom_data, dragmode_data):
    if not folder or not file:
        return go.Figure()

    path = os.path.join(SOURCEFILE, folder, file)
    df = pd.read_csv(path)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Time"], y=df["0"], mode='lines', name='Signal'))

    if peak_data:
        peak_df = pd.DataFrame(peak_data)
        
        rhythm1_peaks = peak_df[peak_df['Rhythm'] == 'Rhythm 1']
        rhythm2_peaks = peak_df[peak_df['Rhythm'] == 'Rhythm 2']
        
        if not rhythm1_peaks.empty:
            fig.add_trace(go.Scatter(
                x=rhythm1_peaks['Time'],
                y=rhythm1_peaks['Value'],
                mode='markers',
                marker=dict(color='red', size=10),
                name='Rhythm 1 Peaks'
            ))
        
        if not rhythm2_peaks.empty:
            fig.add_trace(go.Scatter(
                x=rhythm2_peaks['Time'],
                y=rhythm2_peaks['Value'],
                mode='markers',
                marker=dict(color='blue', size=10),
                name='Rhythm 2 Peaks'
            ))

    dragmode = dragmode_data.get('dragmode', 'zoom')
    fig.update_layout(
        title=f"Acceleration Over Time for {file}",
        dragmode=dragmode
    )
    
    if zoom_data and any(key in zoom_data for key in ['xaxis.range[0]', 'xaxis.range[1]', 'yaxis.range[0]', 'yaxis.range[1]']):
        layout_updates = {}
        if 'xaxis.range[0]' in zoom_data and 'xaxis.range[1]' in zoom_data:
            layout_updates['xaxis'] = {'range': [zoom_data['xaxis.range[0]'], zoom_data['xaxis.range[1]']]}
        if 'yaxis.range[0]' in zoom_data and 'yaxis.range[1]' in zoom_data:
            layout_updates['yaxis'] = {'range': [zoom_data['yaxis.range[0]'], zoom_data['yaxis.range[1]']]}
        
        if layout_updates:
            fig.update_layout(**layout_updates)
    
    return fig

@app.callback(
    Output('save-status', 'children'),
    Input('save-button', 'n_clicks'),
    State('Folder-Dropdown', 'value'),
    State('File-Dropdown', 'value'),
    State('peak-store', 'data'),
    prevent_initial_call=True
)
def save_peaks(n_clicks, folder, file, peaks):
    if not (folder and file and peaks):
        return "Missing information or no peaks to save."

    save_folder = os.path.join(FINALDESTINATION, folder)
    os.makedirs(save_folder, exist_ok=True)

    peak_df = pd.DataFrame(peaks)
    base_filename = os.path.splitext(file)[0]
    save_path = os.path.join(save_folder, base_filename + "_peaks.csv")
    peak_df.to_csv(save_path, index=False)

    rhythm1_count = len(peak_df[peak_df['Rhythm'] == 'Rhythm 1'])
    rhythm2_count = len(peak_df[peak_df['Rhythm'] == 'Rhythm 2'])

    return f"Saved {len(peaks)} peaks to: {save_path} (Rhythm 1: {rhythm1_count}, Rhythm 2: {rhythm2_count})"

if __name__ == '__main__':
    app.run(debug=True)