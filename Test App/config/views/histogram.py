import numpy as np
from dash import dcc, html
import plotly.graph_objects as go

class Histogram(html.Div):
    def __init__(self, name, feature_x, feature_y, df, type):
        self.html_id = name.lower().replace(" ","-")
        self.df = df
        self.feature_x = feature_x
        self.feature_y = feature_y
        self.type = type

        super().__init__(
            className = "graph_card",
            children = [
                html.H6(name),
                dcc.Graph(id = self.html_id)
            ],
        )

    def update(self, selected_data):
        if self.type == 'input':
            width = 10
            height =  10
        elif self.type == 'output':
            width = 1000
            height = 400
        else:
            raise ValueError('Parameter: "type" is invalid or inexecutable.')
            
        self.fig = go.Figure()
        x_values = self.df[self.feature_x]

        self.fig.add_trace(go.Histogram(
            x = x_values,
            xbins = dict(start = np.min(x_values), size = 10, end = np.max(x_values)),
            marker = dict(color = 'rgb(0, 0, 80)')
        ))

        self.fig.update_traces(marker = dict(color = 'rgb(0, 0, 80)'))
        self.fig.update_layout(autosize = False, width = width, height = height)
        self.fig.update_xaxes(fixedrange = True)
        self.fig.update_yaxes(fixedrange = True)

        self.fig.update_layout(
            xaxis_title = self.feature_x,
            yaxis_title = self.feature_y,
        )


        return self.fig