from dash import Dash, html, dcc
from dash import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
app = Dash(__name__)

data = {
    "shoe_price" : [100, 150, 300, 550],
    "coolness" : [80, 85, 70, 15],
    "female_attention" : [10, 30, 10, 5],
    "year" : [2000, 2005, 2010, 2015]
}

# fig = px.line(data, x = 'shoe_price', y = 'coolness')

# app.layout = html.Div(
#     children = [
#         html.H1(children = 'Hello World!'),
#         html.Div(children = 'Some description'),

#         dcc.Graph(
#             id = 'graph',
#             figure = fig
#         )
#     ]
# )

app.layout = html.Div([
    dcc.Graph(id = 'scatter_plot'),
    dcc.Slider(
        min(data['year']),
        max(data['year']),
        step = None,
        value = min(data['year']),
        marks = {str(year): str(year) for year in np.unique(data['year'])},
        id = 'slider'
    ),
])

@app.callback(
    Output('scatter_plot', 'figure'),
    Input('slider', 'value')
)
def update_figure(input_year):
    filter_df = data[data['year'] == input_year]

    fig = px.scatter(filter_df, x = 'shoe_price', y = 'coolness',
                     size = 'female_attention')

    return fig

if __name__ == "__main__":
    app.run_server(debug = True)