

import json
import plotly.express as px
import plotly
import chart_studio.plotly as py
import plotly.graph_objs as go
import numpy as np
import pandas as pd

def plotly_global_timeseries():

    fig = go.Figure(
        data = go.Bar(
            x = ['January', 'July', 'November'],
            y = [20114754920.56, 15519797242.32 ,12596653961.11]))

    fig.update_layout(
        title="Total Volume Over Time",
        xaxis_title="Month",
        yaxis_title="Volume",
        legend_title="Legend Title",
        font=dict(
            size=18,
            color="grey"
        )
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON



def plotly_net_income_loss():

    fig = go.Figure(go.Scatter(
    x = ['January', 'July', 'November'],
    y = [-7934818.780000001, 19395713.42 ,7885372.56]))

    fig.update_layout(
        title="Net Income/Loss (ITC) Over Time",
        xaxis_title="Month",
        yaxis_title="Net Income/Loss (ITC)",
        legend_title="Legend Title",
        font=dict(
            size=18,
            color="grey"
        )
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON