from dash import Dash, html, Input, Output, State, ALL
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import random
import sys
from amplabs.components import navbar, graph, selectionBar
from amplabs.utils import check_list_type

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

y_axis_ranges=[]

def set_color(colors):
    list_type = check_list_type(colors)
    global color_list
    if list_type == "list":
        color_list = [colors]
    else:
        color_list = colors


def set_x_axis_range(ranges):
    list_type = check_list_type(ranges)
    global x_axis_ranges
    if list_type == "list":
        x_axis_ranges = [ranges]
    else:
        x_axis_ranges = ranges


def set_y_axis_range(ranges):
    list_type = check_list_type(ranges)
    global y_axis_ranges
    if list_type == "list":
        y_axis_ranges = [ranges]
    else:
        y_axis_ranges = ranges


def start_dash_server():
    global dash_server_running
    app.run_server(debug=True)


def set_x_axis_tick_intervals(intervals):
    list_type = check_list_type(intervals)
    global x_axis_intervals 
    if list_type == "list":
        x_axis_intervals = [intervals]
    else:
        x_axis_intervals = intervals


def plot(data_list=[], data_names=[]):
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
                if i >= len(color_list):
                    color_list.append([])
                if i == 0:
                    for j, y_axis in enumerate(y_values):
                        if j >= len(color_list[i]):
                            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
                            color_list.append(color)
                        else:
                            color = color_list[i][j]

                        y_df = [float(temp) for temp in df[y_axis]]
                        x_df = [float(temp) for temp in df[x_axes[i]]]
                        fig.add_trace(
                            go.Scatter(
                                x=x_df,
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
                            # range=[25, 50],
                        )
                    )
                else:
                    for j, y_axis in enumerate(y_values):
                        if j >= len(color_list[i]):
                            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
                            color_list.append(color)
                        else:
                            color = color_list[i][j]
                        y_df = [float(temp) for temp in df[y_axis]]
                        x_df = [float(temp) for temp in df[x_axes[i]]]
                        fig.add_trace(
                            go.Scatter(
                                x=x_df,
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

            for i, x_range in enumerate(
                x_axis_ranges,
            ):
                if len(x_range) == 0:
                    continue
                x_axis_name = "xaxis"  # Generate unique x-axis identifier
                x_num = i + 1
                if x_num != 1:
                    x_axis_name = x_axis_name + str(x_num)
                fig.update_layout(
                    **{
                        x_axis_name: dict(
                            range=x_range,
                            dtick=8
                        )
                    }
                )

            for i, y_range in enumerate(
                y_axis_ranges,
            ):
                if len(y_range) == 0:
                    continue
                y_axis_name = "yaxis"
                y_num = i + 1
                if y_num != 1:
                    y_axis_name = y_axis_name + str(y_num)
                fig.update_layout(
                    **{
                        y_axis_name: dict(
                            range=y_range,
                            # anchor="",
                            # overlaying=f"yaxis{i-1}" if i > 1 else None,
                        )
                    }
                )

            # Update layout with dynamically generated x-axes
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
