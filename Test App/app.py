import pandas as pd
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output

from config.data import load_data
from config.main import app
from config.config import background_colors, plot_colors
from config.config import Scatterplot
from config.config import Histogram

if __name__ == '__main__':

    # Load dataset
    df = load_data()

    # Create Input plots
    fig_monthly_salary = Histogram('Monthly Inhand Salary Distribution', 'Monthly_Inhand_Salary', ' Monthly_Inhand_Salary', df, input)

    app.layout = html.Div(
        id = 'app-container',
        children = [

            # Left Menu Column
            html.Div(
                id = 'left-column',
                className = 'four-columns',
                children = [

                    # Description Card
                    html.Div(
                        id = 'description-card',
                        children = [
                            html.H5(
                                "StandIn Name Dashboard"
                            ),
                            html.Div(
                                id = 'intro',
                                children = [
                                    'Enter financial parameters below.'
                                ]
                            )
                        ]
                    ),

                    # Collapsible Settings Menu
                    html.Details([
                        html.Summary("Settings"),
                        html.Div(
                            id = 'settins-card',
                            children = [
                                html.Label("Graph background color"),
                                dcc.Dropdown(
                                    id = "select-background-color",
                                    options = [{"label": i, "value": i} for i in background_colors],
                                    value = background_colors[0],
                                ),
                                html.Br(),
                                html.Label("Graph plot color"),
                                dcc.Dropdown(
                                    id = 'select-plot-color',
                                    options = [{"label": i, "value": i} for i in plot_colors],
                                    value = plot_colors[0],
                                )
                            ],
                            # style = {'textAlign' : 'float-left'}
                        )
                    ]),

                    # Monthly Salary Card
                    html.Div(
                        id = 'monthly-salary-card',
                        children = [

                            dcc.Input(
                                id = 'salary-input',
                                value = None,
                                type = 'text'
                            )
                        ]
                    )
                ]
            ),
        

            html.Div(
                id = 'right-column',
                className = 'eight-columns',
                children = [
                    html.Div(
                        id = 'right-side',
                        className = 'four-columns',
                        children = [

                        ]
                    ),
                    html.Div(
                        id = 'left-side',
                        className = 'four-columns',
                        children = [

                        ]
                    )
                ]
            )
        ]
    )

    # TODO : insert app.callback's for every reactive graph and input Div

    app.run_server(debug = True, dev_tools_ui = True)