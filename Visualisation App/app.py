import dash
from dash.dependencies import ALL
from dash.exceptions import PreventUpdate
from dash import html, dcc, Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np
from collections import Counter
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

df = pd.read_csv('Data/Cleaned/cleaned_data.csv')


def create_chart(filtered_df, title: str, plotType: str, var: str):
    if plotType == 'bar':
        freqDist = Counter(filtered_df[var])
        x = list(freqDist.keys())
        y = list(freqDist.values())

        fig = px.bar(x=x, y=y, labels={'x': var.replace('_', ' '), 'y': 'Frequency'}, title=title)
    elif plotType == 'line':
        # Line plot section, functionality not pursued
        fig = px.line()
        
    fig.update_layout(**chart_theme_style)  # Apply dark theme styles to chart
    return fig

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    style=dark_theme_style,
    children=[
        html.Div([
            html.H3("Applicant Information", style={'color': 'white'}),
            html.Div([html.P("Monthly Inhand Salary:"), dcc.Input(id={'type': 'dynamic-input', 'index': 1}, type='number')]),
            html.Div([html.P("Outstanding Debt:"), dcc.Input(id={'type': 'dynamic-input', 'index': 2}, type='number')]),
            html.Div([html.P("Interest Rate:"), dcc.Input(id={'type': 'dynamic-input', 'index': 3}, type='number')]),
            html.Div([html.P("Number of Loans:"), dcc.Slider(0, 10, 1, id={'type': 'dynamic-input', 'index': 4})]),
            html.Div([html.P("Number of Credit Inquiries:"), dcc.Input(id={'type': 'dynamic-input', 'index': 5}, type='number')]),
            html.Div([
                html.P("Credit Mix:"),
                dbc.ButtonGroup([
                    dbc.Button("Bad", id='credit-mix-bad', n_clicks=0, className="mr-1"),
                    dbc.Button("Standard", id='credit-mix-standard', n_clicks=0, className="mr-1"),
                    dbc.Button("Good", id='credit-mix-good', n_clicks=0),
                ], className = 'mb-3'),
                dcc.Store(id='credit-mix-store'),  # Component to  store the credit mix value

            ]),
            html.Div([html.P("Credit Utilisation Ratio:"), dcc.Input(id={'type': 'dynamic-input', 'index': 6}, type='number')]),
            html.Div([html.P("Total EMI per Month:"), dcc.Input(id={'type': 'dynamic-input', 'index': 7}, type='number')]),
            html.Div([dbc.Button('Refresh', id='refresh-button', n_clicks=0)])
        ], style={'width': '15%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        html.Div(id='output-tab', style={'width': '85%', 'display': 'inline-block'})
    ]
)

@app.callback(
    Output('credit-mix-store', 'data'),
    [Input('credit-mix-bad', 'n_clicks'),
     Input('credit-mix-standard', 'n_clicks'),
     Input('credit-mix-good', 'n_clicks')],
    prevent_initial_call=True
)
def update_credit_mix_store(bad_clicks, standard_clicks, good_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'credit-mix-bad':
            return {'credit_mix': 'Bad'}
        elif button_id == 'credit-mix-standard':
            return {'credit_mix': 'Standard'}
        elif button_id == 'credit-mix-good':
            return {'credit_mix': 'Good'}


# Callback for updating graphs based on inputs and refresh button click
@app.callback(
    Output('output-tab', 'children'),
    [Input('refresh-button', 'n_clicks')],
    [State({'type': 'dynamic-input', 'index': ALL}, 'value'),
     State('credit-mix-store', 'data')]
)

def update_graphs(n_clicks, values, credit_mix_data):
    if n_clicks == 0:
        raise PreventUpdate

    df = pd.read_csv('Data/Cleaned/cleaned_data.csv')  # Reload to ensure the data is fresh each time
    graphs = []

    # Mapping from input index to DataFrame column name
    column_index = {
        1: 'Monthly_Inhand_Salary',
        2: 'Outstanding_Debt',
        3: 'Interest_Rate',
        4: 'Num_of_Loan',
        5: 'Num_Credit_Inquiries',
        6: 'Credit_Mix',
        7: 'Credit_Utilization_Ratio',
        8: 'Total_EMI_per_month'
    }

    # Retrieve the credit mix value from the store
    credit_mix_value = credit_mix_data.get('credit_mix') if credit_mix_data else None

    if credit_mix_data:
        credit_mix_value = credit_mix_data.get('credit_mix')
        df = df[df['Credit_Mix'] == credit_mix_value]

    # Compensate for the absence of the categorical variable Credit_Mix later
    values.insert(5, None)

    for i, val in enumerate(values):
        if val is not None and val != "":  # Check for valid numeric input
            column_name = column_index[i + 1]  # Map index to column name
            
            if column_name == 'Credit_Mix':
                continue

            if val != None:
                val = float(val)  # Ensure input is treated as numeric
                std = np.std(df[column_name])
                df = df[(df[column_name] < val + 1*std) & (df[column_name] > val - 1*std)]

    if df.empty:
        div = [
            html.H2('Insufficient Comparison Data Available', style = {'color' : 'white'})
        ]
        return div

    plots = [['Delay_from_due_date', 'bar'], ['Num_of_Delayed_Payment', 'bar'], ['Payment_Behaviour', 'bar'], ['Credit_Score', 'bar']]

    for i in plots:
        plot_title = i[0].replace('_', ' ')
        type = i[1]
        variable = i[0]

        # Generate chart with filtered data
        fig = create_chart(df, title = plot_title, plotType = type, var = variable)
        graphs.append(dcc.Graph(figure=fig))

    div = [
        html.H3("Financials of Applicant's Peers (TBD)", style = {'color' : 'white'}),
        # First row of graphs
        html.Div([
            html.Div(dcc.Graph(figure = create_chart(df, 'Delay from Due Date', 'bar', 'Delay_from_due_date'), style = {'width' : '600px', 'height' : '350px'})),
            html.Div(dcc.Graph(figure = create_chart(df, 'Number of Delayed Payments', 'bar', 'Num_of_Delayed_Payment'), style = {'width' : '600px', 'height' : '350px'})),
        ], style = {'display': 'flex', 'justifyContent': 'space-between'}),

        # Second row of graphs
        html.Div([
            html.Div(dcc.Graph(figure = create_chart(df, 'Payment Behaviour', 'bar', 'Payment_Behaviour'), style = {'width' : '600px', 'height' : '350px'})),
            html.Div(dcc.Graph(figure = create_chart(df, 'Credit Score', 'bar', 'Credit_Score'), style = {'width' : '600px', 'height' : '350px'})),
        ], style = {'display': 'flex', 'justifyContent': 'space-between'}),
    ]

    return div

if __name__ == '__main__':
    app.run_server(debug=True)
