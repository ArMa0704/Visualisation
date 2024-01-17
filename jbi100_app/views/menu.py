from dash import dcc, html
from ..config import color_list1, color_list2

import pandas as pd

from .scatterplot import Scatterplot



# Testing df for left column input graphs
data = {
    "shoe_price" : [100, 150, 300, 550],
    "coolness" : [80, 85, 70, 15]
}

df_test = pd.DataFrame(data)

scatterplotdf = Scatterplot("df", 'shoe_price', 'coolness', df_test)


def generate_description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("StandIn Name Dashboard"),
            html.Div(
                id="intro",
                children="JBL100 Template, Spaghetti.",
            ),
        ],
    )


def generate_control_card():
    """

    :return: A Collapsible Div containing controls for graphs.
    """
    return html.Details([
        html.Summary("Settings"),
        html.Div(
        id="control-card",
        children=[
            html.Label("Graph background color"),
            dcc.Dropdown(
                id="select-color-scatter-1",
                options=[{"label": i, "value": i} for i in color_list1],
                value=color_list1[0],
            ),
            html.Br(),
            html.Label("Color scatterplot 2"),
            dcc.Dropdown(
                id="select-color-scatter-2",
                options=[{"label": i, "value": i} for i in color_list2],
                value=color_list2[0],
            ),
        ], style={"textAlign": "float-left"}
        )
    ])

def generate_input_graphs():
    """
    :return a Div containing graphs showing the client's submitted info
    """
    return html.Div(
        id = "input-card",
        children = scatterplotdf
    )

def make_menu_layout():
    return [generate_description_card(), generate_control_card(), generate_input_graphs()]
