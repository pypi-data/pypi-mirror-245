from dash import Dash, html, Input, Output, State, ALL
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import random
import sys
from amplabs.components import navbar, graph, selectionBar



app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])



class plot:
    instances = []
    def __init__(self, df, df_name):
        self.df = df
        self.df_name = df_name
        self.headers = self.df.columns.tolist()
        plot.instances.append(self)

    def set_color(self, colors):
        self.colors = colors
    
    def set_xrange(self, ranges):
        self.xrange = ranges

    def set_yrange(self,ranges): 
        self.yrange = ranges

    def set_xintervals(self, intervals):    
        self.xinterval = intervals
    
    def set_yintervals(self, intervals):    
        self.yinterval = intervals



    @classmethod
    def show(cls):
        color_list = []
        data_list = []
        data_names = []
        list_of_headers = []
        x_ranges = []
        y_ranges = []
        x_interval = []
        y_interval = []

        for instance in cls.instances:
            data_list.append(instance.df)
            data_names.append(instance.df_name)
            list_of_headers.append(instance.headers)
            if hasattr(instance, 'colors'):
                color_list.append(instance.colors)
            else:
                color_list.append([])
            if hasattr(instance, 'xrange'):
                x_ranges.append(instance.xrange) 
            else:
                x_ranges.append([]) 
            if hasattr(instance, 'yrange'):
                y_ranges.append(instance.yrange) 
            else:
                y_ranges.append([]) 
            if hasattr(instance, 'xinterval'):
                x_interval.append(instance.xinterval)
            else:
                x_interval.append([])
            if hasattr(instance, 'yinterval'):
                y_interval.append(instance.yinterval) 
            else:
                y_interval.append([]) 
        print(color_list)        
        try:

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
                                color_list[i].append(color)
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
                                color_list[i].append(color)
                            else:
                                color = color_list[i][j]
                                print(color)
                            y_df = [float(temp) for temp in df[y_axis]]
                            x_df = [float(temp) for temp in df[x_axes[i]]]
                            fig.add_trace(
                                go.Scatter(
                                    x=x_df,
                                    y=y_df,
                                    name=y_axis, 
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
                                        anchor="free",
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
                    x_ranges,
                ):
                    if len(x_range) == 0:
                        continue
                    x_axis_name = "xaxis"  # Generate unique x-axis identifier
                    x_num = i + 1
                    if x_num != 1:
                        x_axis_name = x_axis_name + str(x_num)
                    fig.update_layout(**{x_axis_name: dict(range=x_range, dtick=8)})

                for i, y_range in enumerate(
                    y_ranges,
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
                            )
                        }
                    )

                for i, y_tick in enumerate(
                    y_interval,
                ):
                    if isinstance(y_tick, (int, float)) is False:
                        continue
                    y_axis_name = "yaxis"
                    y_num = i + 1
                    tick_num = y_tick
                    if y_num != 1:
                        y_axis_name = y_axis_name + str(y_num)
                    fig.update_layout(
                        **{
                            y_axis_name: dict(
                                dtick=tick_num,
                            )
                        }
                    )

                for i, x_tick in enumerate(
                    x_interval,
                ):
                    if isinstance(x_tick, (int, float)) is False:
                        continue
                    x_axis_name = "yaxis"
                    x_num = i + 1
                    tick_num = x_tick
                    if x_num != 1:
                        x_axis_name = x_axis_name + str(x_num)
                    fig.update_layout(
                        **{
                            x_axis_name: dict(
                                dtick=tick_num,
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

        start_dash_server()


def start_dash_server():
    global dash_server_running
    app.run_server(debug=True)