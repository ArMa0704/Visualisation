import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import scipy.stats as stats
from collections import Counter
from data import load_data

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

# Example static dataset
df = load_data()

# Function to create a sample chart
def create_chart(title : str, plotType : str, var : str):
    if plotType == 'bar':
        # Calculate Frq. Dist.
        freqDist = Counter(df[var])
        x = list(freqDist.keys())
        y = list(freqDist.values())

        fig =  px.bar(df, x = x, y = y , title = title)
    elif plotType == 'line':
        fig = px.line()
        
    fig.update_layout(**chart_theme_style)  # Apply dark theme styles to chart
    return fig

# Creating bar and line charts using Plotly
# bar_chart = px.bar(df, x="Month", y="Value", title="Bar Chart")
# line_chart = px.line(df, x="Month", y="Value", title="Line Chart")

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(
    style = dark_theme_style,
    children = [
    html.Div([
        html.H3("Applicant Information", style = {'color' : 'white'}),
        html.Div([html.P("Monthly Inhand Salary:"), dcc.Input(id = 'monthly-input', type = 'number')]),
        html.Div([html.P("Outstanding Debt:"), dcc.Input(id = 'outstanding-input', type = 'number')]),
        html.Div([html.P("Interest Rate:"), dcc.Input(id = 'int-rate-input', type = 'number')]),
        html.Div([html.P("Number of Loans:"), dcc.Input(id = 'num-loans-input', type = 'number')]),
        html.Div([html.P("Number of Credit Inquiries:"), dcc.Input(id = 'num-inquiries-input', type = 'number')]),
        html.Div([html.P("Credit Mix:"), dcc.Input(id = 'credit-mix-input', type = 'number')]),
        html.Div([html.P("Credit Utilisation Ratio:"), dcc.Input(id = 'CUR-input', type = 'number')]),
        html.Div([html.P("Total EMI per Month:"), dcc.Input(id = 'EMI-input', type = 'number')])
    ], style = {'width': '15%', 'display': 'inline-block', 'verticalAlign': 'top'}),

    html.Div([
        # First row of graphs
        html.Div([
            html.Div(dcc.Graph(figure = create_chart('Delay from Due Date', 'bar', 'Delay_from_due_date'), style = {'width' : '400px', 'height' : '350px'})),
            html.Div(dcc.Graph(figure = create_chart("Chart 2"), style = {'width' : '400px', 'height' : '350px'})),
            html.Div(dcc.Graph(figure = create_chart("Chart 3"), style = {'width' : '400px', 'height' : '350px'})),
        ], style = {'display': 'flex', 'justifyContent': 'space-between'}),

        # Second row of graphs
        html.Div([
            html.Div(dcc.Graph(figure = create_chart("Chart 4"), style = {'width' : '400px', 'height' : '350px'})),
            html.Div(dcc.Graph(figure = create_chart("Chart 5"), style = {'width' : '400px', 'height' : '350px'})),
            html.Div(dcc.Graph(figure = create_chart("Chart 6"), style = {'width' : '400px', 'height' : '350px'})),
        ], style = {'display': 'flex', 'justifyContent': 'space-between'}),
    ], style = {'width': '85%', 'display': 'inline-block'})
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)