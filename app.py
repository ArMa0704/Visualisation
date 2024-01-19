from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.views.histogram import Histogram
from jbi100_app.config import color_list1, color_list2

import pandas as pd
from dash import html, dcc
import plotly.express as px
from dash.dependencies import Input, Output

def load_data():
    df = pd.read_csv("Data/Raw/all_data.csv")
    return df

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
            ], 
            style={"textAlign": "float-left"}
        )
    ])

def generate_input_graphs():
    """
    :return a Div containing graphs showing the client's submitted info
    """

    fig_salary = Histogram(
        'Monthly Inhand Salary', 
        'Monthly_Inhand_Salary',
        'Annual_Income', 
        df,)
    fig_interest = None
    fig_loans = None
    fig_debt = None
    fig_cr_inq = None
    fig_cr_mix = None
    fig_CUR = None
    fig_EMI = None

    return html.Div(
        id = "input-card",
        children = [
            html.Div(
                id = "monthly-inhand",
                children = [
                    "Monthly Inhand Salary: ",
                    fig_salary,
                    html.Div([
                        dcc.Input(
                            id = 'salary-input', 
                            value = None, type = 'text'
                        )
                    ])
                ]
            )
        ]
    )

def make_menu_layout():
    return [generate_description_card(), generate_control_card(), generate_input_graphs()]

if __name__ == '__main__':
    # Create data
    df_template = px.data.iris()

    df = load_data()

    # Instantiate custom views
    scatterplot1 = Scatterplot("Scatterplot 1", 'sepal_length', 'sepal_width', df_template)
    scatterplot2 = Scatterplot("Scatterplot 2", 'petal_length', 'petal_width', df_template)

    app.layout = html.Div(
        id="app-container",
        children=[

            # Left column
            html.Div(
                id="left-column",
                className="three columns",
                children = make_menu_layout()
            ),

            # Right column
            html.Div(
                id="right-column",
                className="nine columns",
                children=[
                    scatterplot1,
                    scatterplot2,
                ],
            ),
        ],
    )


    # Define interactions
    # Update Monthly Salary figure
    @app.callback(
        Output(fig_salary.html_id, 'figure'), [
            Input('salary-input', 'value'),
        ]
    )
    def update_histogram_1(selected_data):
        return fig_salary.update(selected_data)

    # Color updater scatterplot1
    @app.callback(
        Output(scatterplot1.html_id, "figure"), [
        Input("select-color-scatter-1", "value"),
        Input(scatterplot1.html_id, 'selectedData')
    ])
    def update_scatter_1(selected_color, selected_data):
        return scatterplot1.update(selected_color, selected_data)

    # Color updater scatterplot2
    @app.callback(
        Output(scatterplot2.html_id, "figure"), [
        Input("select-color-scatter-2", "value"),
        Input(scatterplot2.html_id, 'selectedData')
    ])
    def update_scatter_2(selected_color, selected_data):
        return scatterplot2.update(selected_color, selected_data)


    app.run_server(debug=True, dev_tools_ui=True)