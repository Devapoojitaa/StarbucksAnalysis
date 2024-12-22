import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import os

# Load and validate data
def load_data(file_path, required_columns=None):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: {file_path} not found. Please upload the file.")
    
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Error loading {file_path}: {e}")

    # Validate required columns
    if required_columns:
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise KeyError(f"Missing required columns in {file_path}: {missing_columns}")

    return df

# Load datasets with validation
menu = load_data(
    "starbucks-menu-nutrition-drinks.csv",
    required_columns=["Calories"]
)
directory = load_data(
    "directory.csv",
    required_columns=["latitude", "longitude"]
)
portfolio = load_data(
    "portfolio.csv",
    required_columns=["cluster", "reward", "difficulty", "duration"]
)

# Preprocess and clean data
def preprocess_data():
    # Clean 'directory' dataset
    directory['latitude'] = pd.to_numeric(directory['latitude'], errors='coerce')
    directory['longitude'] = pd.to_numeric(directory['longitude'], errors='coerce')
    directory['latitude'].fillna(directory['latitude'].mean(), inplace=True)
    directory['longitude'].fillna(directory['longitude'].mean(), inplace=True)

    # Clean 'menu' dataset
    menu['Calories'] = pd.to_numeric(menu['Calories'], errors='coerce').fillna(0)

preprocess_data()

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server  # For deployment platforms like Render or Heroku

# App Layout
app.layout = html.Div([
    html.H1("Starbucks Dashboard", style={"textAlign": "center"}),

    dcc.Tabs([
        # Tab 1: Customer Segmentation
        dcc.Tab(label='Customer Segmentation', children=[
            html.H2("Customer Segmentation Analysis", style={"textAlign": "center"}),
            dcc.Graph(id='segmentation-scatter'),
            html.P("Filter by Cluster:"),
            dcc.Dropdown(
                id='cluster-dropdown',
                options=[{'label': f'Cluster {i}', 'value': i} for i in portfolio['cluster'].unique()],
                value=portfolio['cluster'].unique()[0]
            ),
        ]),

        # Tab 2: Menu Optimization
        dcc.Tab(label='Menu Optimization', children=[
            html.H2("Menu Optimization Insights", style={"textAlign": "center"}),
            dcc.Graph(id='calorie-distribution'),
            html.P("Filter by Calorie Level:"),
            dcc.RangeSlider(
                id='calorie-slider',
                min=menu['Calories'].min(),
                max=menu['Calories'].max(),
                step=10,
                marks={i: str(i) for i in range(0, int(menu['Calories'].max()) + 1, 100)},
                value=[menu['Calories'].min(), menu['Calories'].mean()]
            ),
        ]),

        # Tab 3: Store Location Optimization
        dcc.Tab(label='Store Location Optimization', children=[
            html.H2("Store Location Insights", style={"textAlign": "center"}),
            html.Button("Update Heatmap", id="update-heatmap", n_clicks=0),
            dcc.Graph(id='location-heatmap'),
        ]),
    ])
])

# Callbacks

# Customer Segmentation Scatter Plot
@app.callback(
    Output('segmentation-scatter', 'figure'),
    [Input('cluster-dropdown', 'value')]
)
def update_segmentation_scatter(selected_cluster):
    filtered_data = portfolio[portfolio['cluster'] == selected_cluster]
    fig = px.scatter(
        filtered_data, x='reward', y='difficulty', color='cluster', size='duration',
        title="Customer Segmentation Scatter Plot"
    )
    return fig

# Menu Optimization Calorie Distribution
@app.callback(
    Output('calorie-distribution', 'figure'),
    [Input('calorie-slider', 'value')]
)
def update_calorie_distribution(calorie_range):
    filtered_data = menu[(menu['Calories'] >= calorie_range[0]) & (menu['Calories'] <= calorie_range[1])]
    fig = px.histogram(
        filtered_data, x='Calories', nbins=20, title="Calorie Distribution",
        labels={'Calories': 'Calorie Levels'}
    )
    return fig

# Store Location Heatmap
@app.callback(
    Output('location-heatmap', 'figure'),
    [Input('update-heatmap', 'n_clicks')]
)
def update_location_heatmap(n_clicks):
    fig = px.density_mapbox(
        directory,
        lat='latitude',
        lon='longitude',
        radius=10,
        mapbox_style="stamen-terrain",
        center={"lat": directory['latitude'].mean(), "lon": directory['longitude'].mean()},
        zoom=2,
        title="Store Location Heatmap"
    )
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
