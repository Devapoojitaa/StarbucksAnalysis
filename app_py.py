import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load Data
directory = pd.read_csv("directory.csv")
menu = pd.read_csv("starbucks-menu-nutrition-drinks.csv")
portfolio = pd.read_csv("portfolio.csv")

# Preprocess data
directory['latitude'].fillna(directory['latitude'].mean(), inplace=True)
directory['longitude'].fillna(directory['longitude'].mean(), inplace=True)
menu['Calories'] = pd.to_numeric(menu['Calories'], errors='coerce')
menu['Calories'].fillna(0, inplace=True)

# Initialize the app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Starbucks Dashboard", style={'text-align': 'center'}),
    dcc.Tabs([
        # Tab 1: Customer Segmentation
        dcc.Tab(label='Customer Segmentation', children=[
            html.H2("Customer Segmentation Analysis"),
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
            html.H2("Menu Optimization Insights"),
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
            html.H2("Store Location Insights"),
            html.Button("Update Heatmap", id="update-heatmap-btn"),
            dcc.Graph(id='location-heatmap'),
        ]),
    ])
])

# Callbacks
@app.callback(
    Output('segmentation-scatter', 'figure'),
    [Input('cluster-dropdown', 'value')]
)
def update_segmentation_scatter(selected_cluster):
    filtered_data = portfolio[portfolio['cluster'] == selected_cluster]
    fig = px.scatter(filtered_data, x='reward', y='difficulty', color='cluster', size='duration',
                     title="Customer Segmentation Scatter Plot")
    return fig

@app.callback(
    Output('calorie-distribution', 'figure'),
    [Input('calorie-slider', 'value')]
)
def update_calorie_distribution(calorie_range):
    filtered_data = menu[(menu['Calories'] >= calorie_range[0]) & (menu['Calories'] <= calorie_range[1])]
    fig = px.histogram(filtered_data, x='Calories', nbins=20, title="Calorie Distribution")
    return fig

@app.callback(
    Output('location-heatmap', 'figure'),
    Input('update-heatmap-btn', 'n_clicks'),
)
def update_location_heatmap(n_clicks):
    """Callback to render a global heatmap."""
    print("Heatmap callback triggered")
    fig = px.density_mapbox(
        directory,
        lat='latitude',
        lon='longitude',
        radius=10,
        mapbox_style="carto-positron",  # Use a clean map style
        title="Store Location Heatmap",
        center={"lat": 0, "lon": 0},  # Center at the equator
        zoom=3,  # Zoom out for a global view
        height=600,  # Adjust height for better visibility
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
