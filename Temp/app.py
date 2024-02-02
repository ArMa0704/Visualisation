import dash
from dash.dependencies import ALL
from dash.exceptions import PreventUpdate
from dash import html, dcc, Input, Output, State
import json
import plotly.express as px
import pandas as pd
import numpy as np
import scipy.stats as stats
from collections import Counter
from data import load_data
import dash_bootstrap_components as dbc

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
df = pd.read_csv('Data/Cleaned/cleaned_data.csv')

# Function to create a sample chart
def create_chart(title : str, plotType : str, var : str):
    if plotType == 'bar':
        # Calculate Frq. Dist.
        freqDist = Counter(df[var])
        x = list(freqDist.keys())
        y = list(freqDist.values())

        fig =  px.bar(df, x = x, y = y,
                        labels = {
                           'x' : var.replace('_', ' '),
                           'y' : 'Frequency'
                        },
                        title = title)
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
        html.Div([html.P("Credit Mix:"), dcc.Input(id = 'credit-mix-input', type = 'text')]),
        html.Div([html.P("Credit Utilisation Ratio:"), dcc.Input(id = 'CUR-input', type = 'number')]),
        html.Div([html.P("Total EMI per Month:"), dcc.Input(id = 'EMI-input', type = 'number')]),
        html.Div([dbc.Button('Refresh', id = 'refresh-button', n_clicks = 0)])
    ], style = {'width': '15%', 'display': 'inline-block', 'verticalAlign': 'top'}),

    html.Div([
        html.H3("Financials of Applicant's Peers (TBD)", style = {'color' : 'white'}),
        # First row of graphs
        html.Div([
            html.Div(dcc.Graph(figure = create_chart('Delay from Due Date', 'bar', 'Delay_from_due_date'), style = {'width' : '600px', 'height' : '350px'})),
            html.Div(dcc.Graph(figure = create_chart('Number of Delayed Payments', 'bar', 'Num_of_Delayed_Payment'), style = {'width' : '600px', 'height' : '350px'})),
        ], style = {'display': 'flex', 'justifyContent': 'space-between'}),

        # Second row of graphs
        html.Div([
            html.Div(dcc.Graph(figure = create_chart('Payment Behaviour', 'bar', 'Payment_Behaviour'), style = {'width' : '600px', 'height' : '350px'})),
            html.Div(dcc.Graph(figure = create_chart('Credit Score', 'bar', 'Credit_Score'), style = {'width' : '600px', 'height' : '350px'})),
        ], style = {'display': 'flex', 'justifyContent': 'space-between'}),
    ], style = {'width': '85%', 'display': 'inline-block'},
    id = 'output-tab')
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


# @app.callback(
#     Output('output-tab', 'children'),
#     [Input({'type': 'dynamic-input', 'index': ALL}, 'value')],
#     prevent_initial_call=True
# )
# def restrict_dataset(values):

#     column_index = {1 : 'Monthly_Inhand_Salary',
#                     2 : 'Outstanding_Debt',
#                     3 : 'Interest_Rate',
#                     4: 'Num_of_Loan',
#                     5 : 'Num_Credit_Inquiries',
#                     6 : 'Credit_Mix',
#                     7 : 'Credit_Utilization_Ratio',
#                     8 : 'Total_EMI_per_month'}

#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return dash.no_update
#     else:
#         # Gets the id and value of the input component that triggered the callback
#         trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
#         trigger_value = ctx.triggered[0]['value']
        
#         # Extracts the 'index' from the trigger_id to know which input it came from
#         input_index = json.loads(trigger_id)['index']
#         input_column = column_index[input_index]

#         std = np.std(df[input_column])

#         df = df[(trigger_value - std) < input_column < (trigger_value + std)]

@app.callback(
    Output('output-tab', 'children'),
    [Input('refresh-button', 'n_clicks')],
    [State({'type': 'dynamic-input', 'index': ALL}, 'value')]
)
def update_graphs(n_clicks, values):
    if n_clicks == 0:
        # Prevents update before any interaction
        raise PreventUpdate

    # Load or update the DataFrame inside the function to ensure it's up-to-date
    df = pd.read_csv('Data/Cleaned/cleaned_data.csv')
    
    # Container for dynamically generated graphs
    graphs = []

    column_index = {0 : 'Monthly_Inhand_Salary',
                    1 : 'Outstanding_Debt',
                    2 : 'Interest_Rate',
                    3: 'Num_of_Loan',
                    4 : 'Num_Credit_Inquiries',
                    5 : 'Credit_Mix',
                    6 : 'Credit_Utilization_Ratio',
                    7 : 'Total_EMI_per_month'}

    # Assuming column_index maps input indices to df column names
    for i, val in enumerate(values):
        if val is not None:  # Check to ensure the input is not empty
            column_name = column_index[i]  # Adjust index as necessary
            std = np.std(df[column_name])
            mean = np.mean(df[column_name])

            # Filter the DataFrame based on input value and standard deviation
            filtered_df = df[(df[column_name] > (val - std)) & (df[column_name] < (val + std))]

            # Generate a chart for this filtered DataFrame
            fig = create_chart(filtered_df, f"Filtered on {column_name}", 'bar', column_name)
            graphs.append(dcc.Graph(figure=fig))

    return graphs
