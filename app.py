from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot

import pandas as pd
from dash import html, dcc
import plotly.express as px
from dash.dependencies import Input, Output


if __name__ == '__main__':
    # Create data
    df = px.data.iris()

    # Instantiate custom views
    scatterplot1 = Scatterplot("Scatterplot 1", 'sepal_length', 'sepal_width', df)
    scatterplot2 = Scatterplot("Scatterplot 2", 'petal_length', 'petal_width', df)


    app.layout = html.Div(
        id="app-container",
        children=[

            # # Collapsible Menu in left column
            # dcc.RadioItems(
            #     id = 'toggle',
            #     options = [{'label' : 'Toggle Settings', 'value' : i} for i in ['Show', 'Hide']],
            #     value = 'Show'
            # ),



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
                    scatterplot2
                ],
            ),
        ],
    )


    # Define interactions

    # Color updater scatterplot1
    @app.callback(
        Output(scatterplot1.html_id, "figure"), [
        Input("select-color-scatter-1", "value"),
        Input(scatterplot2.html_id, 'selectedData')
    ])
    def update_scatter_1(selected_color, selected_data):
        return scatterplot1.update(selected_color, selected_data)

    # Color updater scatterplot2
    @app.callback(
        Output(scatterplot2.html_id, "figure"), [
        Input("select-color-scatter-2", "value"),
        Input(scatterplot1.html_id, 'selectedData')
    ])
    def update_scatter_2(selected_color, selected_data):
        return scatterplot2.update(selected_color, selected_data)


    app.run_server(debug=False, dev_tools_ui=False)