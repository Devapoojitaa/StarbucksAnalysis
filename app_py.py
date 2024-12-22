import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load and validate data
try:
    menu = pd.read_csv("starbucks-menu-nutrition-drinks.csv")
    directory = pd.read_csv("directory.csv")
    portfolio = pd.read_csv("portfolio.csv")
except FileNotFoundError as e:
    raise FileNotFoundError(f"Error: {e}. Ensure all files are correctly uploaded.") from e

# Validate required columns in the datasets
required_directory_columns = ['latitude', 'longitude']
required_portfolio_columns = ['cluster', 'reward', 'difficulty', 'duration']
required_menu_columns = ['Calories']

for col in required_directory_columns:
    if col not in directory.columns:
        raise KeyError(f"Missing required column '{col}' in 'directory.csv'.")

for col in required_portfolio_columns:
    if col not in portfolio.columns:
        raise KeyError(f"Missing required column '{col}' in 'portfolio.csv'.")

for col in required_menu_columns:
    if col not in menu.columns:
        raise KeyError(f"Missing required column '{col}' in 'starbucks-menu-nutrition-drinks.csv'.")

# Clean and preprocess data
directory['latitude'] = pd.to_numeric(directory['latitude'], errors='coerce')
directory['longitude'] = pd.to_numeric(directory['longitude'], errors='coerce')
directory['latitude'].fillna(directory['latitude'].mean(), inplace=True)
directory['longitude'].fillna(directory['longitude'].mean(), inplace=True)

menu['Calories'] = pd.to_numeric(menu['Calories'], errors='coerce').fillna(0)

# Initialize Dash app
app = dash.Dash(__name__)

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
