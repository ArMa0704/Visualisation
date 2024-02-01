import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

# Example static dataset
df = pd.DataFrame({
    "Month": ["January", "February", "March", "April", "May", "June"],
    "Value": [65, 59, 80, 81, 56, 55]
})

dark_theme_style = {
    'backgroundColor': '#121212',  # Dark background color
    'color': '#E1E1E1',            # Light text color
    'padding': '10px',
    'margin': '10px'
}

chart_theme_style = {
    'plot_bgcolor': '#121212',
    'paper_bgcolor': '#121212',
    'font': {
        'color': '#E1E1E1'
    }
}

# Initialize the Dash app
app = dash.Dash(__name__)

# Function to create a sample chart with dark theme styling
def create_chart(title):
    fig = px.bar(df, x="Month", y="Value", title=title)
    fig.update_layout(**chart_theme_style)  # Apply dark theme styles to chart
    return fig

# Define the layout of the app
app.layout = html.Div(style=dark_theme_style, children=[
    html.Div([
        html.H3("Input Values", style={'color': 'white'}),
        html.Div([html.P("Value 1:", style={'color': 'white'}), dcc.Input(id='input-1', type='number', style={'backgroundColor': '#333', 'color': 'white'})]),
        # Add more inputs as needed
    ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top'}),

    html.Div([
        dcc.Graph(figure=create_chart("Chart 1")),
        dcc.Graph(figure=create_chart("Chart 2")),
        # Add more graphs as needed
    ], style={'width': '75%', 'display': 'inline-block'})
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
