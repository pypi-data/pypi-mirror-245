from dash import Dash, html, Input, Output, State, ALL
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import random
import sys
from amplabs.components import navbar, graph, selectionBar

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


def start_dash_server():
    global dash_server_running
    app.run_server(debug=True)


def plot(data_list=[], data_names=[], color_list=[]):
    # try:
    #     # Check if data frame and data frame name array are empty
    #     if len(df) == 0 and len(df_names) == 0:
    #         raise ValueError("Both data frame name and data frame are not found.")

    #     # Check if data frame is empty
    #     if len(df) == 0:
    #         raise ValueError("Data frame is empty.")

    #     # Check if data frame name array is empty
    #     if len(df_names) == 0:
    #         raise ValueError("Data frame name array is empty.")

    #     # Check if the length of data frame name array is not equal to the number of data frames
    #     if len(df_names) != len(df):
    #         raise ValueError(
    #             "Number of data frame names is not equal to the number of data frames."
    #         )

    # except ValueError as ve:
    #     print(f"Error: {ve}")
    #     sys.exit(1)
    try:
        # list_of_dfs = data_list

        list_of_headers = []
        for dataFrame in data_list:
            list_of_headers.append(dataFrame.columns.tolist())


        # add callback for toggling the collapse on small screens
        @app.callback(
            Output("navbar-collapse", "is_open"),
            [Input("navbar-toggler", "n_clicks")],
            [State("navbar-collapse", "is_open")],
        )
        def toggle_navbar_collapse(n, is_open):
            if n:
                return not is_open
            return is_open

        app.layout = html.Div(
            [
                navbar.HTML_NAVBAR,
                selectionBar.htmlSelectionBar(data_names, list_of_headers),
                graph.HTML_GRAPH,
            ],
            style={"fontSize": "14px"},
        )

        @app.callback(
            Output("graph", "figure"),
            [Input({"type": "add-x", "index": ALL}, "value")],
            [Input({"type": "add-y", "index": ALL}, "value")],
        )
        def update_line_chart(x_axes, y_axes_values):
            fig = go.Figure()

            # Create y-axes for the selected traces
            for i, y_values in enumerate(y_axes_values):
                axis_num = i + 1
                df = data_list[i]
                if i == 0:
                    for j, y_axis in enumerate(y_values):
                        if j >= len(color_list):
                            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
                            color_list.append(color)
                        else:
                            color = color_list[j]

                        y_df = [float(temp) for temp in df[y_axis]]

                        fig.add_trace(
                            go.Scatter(
                                x=df[x_axes[i]],
                                y=y_df,
                                name=y_axis,
                                line=dict(color=color),
                            )
                        )
                    fig.update_layout(
                        yaxis=dict(
                            # title="y1",
                            titlefont=dict(color="#ff7f0e"),
                            tickfont=dict(color="#ff7f0e"),
                            ticks="outside",
                            range=[25, 50],
                        )
                    )
                else:
                    for j, y_axis in enumerate(y_values):
                        if j >= len(color_list):
                            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
                            color_list.append(color)
                        else:
                            color = color_list[j]
                        y_df = [float(temp) for temp in df[y_axis]]
                        fig.add_trace(
                            go.Scatter(
                                x=df[x_axes[i]],
                                y=y_df,
                                # name=y_axis,
                                yaxis=f"y{axis_num}",
                                line=dict(color=color),
                            )
                        )
                        fig.update_layout(
                            **{
                                f"yaxis{axis_num}": dict(
                                    # title=f"y{i}",
                                    overlaying="y",
                                    side="right",
                                    titlefont=dict(color="#ff7f0e"),
                                    tickfont=dict(color="#ff7f0e"),
                                    autoshift=True,
                                    # anchor="free",
                                    ticks="outside",
                                    shift=20 * (i - 1),
                                )
                            }
                        )
            fig.update_layout(
                dict(
                    legend={"x": 1.05, "y": 0.9},
                ),
                width=1200,
                height=600,
                # xaxis_title=x_axes[0],
            )
            fig.update_xaxes(
                showline=True,
                linewidth=1,
                linecolor="black",
                mirror=True,
                ticks="outside",
            )
            fig.update_yaxes(
                showline=True,
                linewidth=1,
                linecolor="black",
                mirror=True,
                # ticks="outside",
            )
            return fig

    except Exception as ve:
        print(f"Error: {ve}")
        sys.exit(1)

    start_dash_server()
