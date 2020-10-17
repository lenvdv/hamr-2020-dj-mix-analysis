import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
colorscale = px.colors.sequential.Inferno

import numpy as np

def plot_loudness(df,
                  outpath):
    print("Plotting Loudness...")
    scaled_x = df.index/df.shape[0]
    loudness = df.Loudness

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=scaled_x, y=loudness,
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color=colorscale[5]),
        stackgroup='one', # define stack group,
        name="Loudness"
    ))

    fig.update_layout(title='Loudness',
                      xaxis_title="Time",
                      yaxis_title="Loudness")


    with open (outpath, 'w+') as f:
        f.write(fig.to_html(full_html=False))
    print("Done! Result saved into file {}".format(outpath))


def plot_spectral_comp(df, outpath):
    print("Plotting specral complexity...")
    scaled_x = df.index/df.shape[0]
    spectral_comp = y=df["Sprectral Complexity"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=scaled_x, y=spectral_comp,
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color=colorscale[5]),
        stackgroup='one', # define stack group,
        name="Spectral Complexity"
    ))
    import ipdb; ipdb.set_trace()

    fig.update_layout(title='Spectral Complexity',
                      xaxis_title="Time",
                      yaxis_title="Specral Complexity",
                      yaxis_range=(0, 150))

    with open (outpath, 'w+') as f:
        f.write(fig.to_html(full_html=False))
    print("Done! Result saved into file {}".format(outpath))


def plot_energy_band(df,
              outpath):

    print("Plotting energy Band....")
    fig = go.Figure()

    scaled_x = df.index/df.shape[0]
    for i, (key, descr) in enumerate(df.iteritems()):
        fig.add_trace(go.Scatter(
            x=scaled_x, y=descr,
            hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5, color=colorscale[i]),
            stackgroup='one', # define stack group,
            name="Energy Band Level {}".format(i)
        ))

    legend_title="Legend Title",
    fig.update_layout(title='Energy Band Level',
                      xaxis_title="Time",
                      yaxis_title="Energy Balance")

    fig.update_layout(yaxis_range=(0, 1))

    with open (outpath, 'w+') as f:
        f.write(fig.to_html(full_html=False))
    print("Done! Result saved into file {}".format(outpath))
