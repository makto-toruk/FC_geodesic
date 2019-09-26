import numpy as np
import pickle

# visualizations with plotly
from _plotly_future_ import v4_subplots
import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
import plotly.subplots as tls
import plotly.figure_factory as ff
import plotly.io as pio
pio.templates.default = 'plotly_white'

'''
when using LR from condition 1 as test, and RL from condition 2 as train
matrix transpose (by symmetry) also provides distance matrix for
RL from condition 2 as test and LR from condition 1 as test
- reduces computation by half
'''

class FC_plotter(object):
    def __init__(self, DIR):
        self.PARCEL_DIR = DIR + '/data/schaefer_parcel'

    def get_fig(self, FC):
        kROI = FC.shape[0]
        nw_path = self.PARCEL_DIR + '/7Networks_%d.pkl' %(kROI)
        with open(nw_path, 'rb') as f:
            networks = pickle.load(f)

        fig = go.Figure()
        edge = [0]
        for ii, nw in enumerate(networks):
            if ii < len(networks)-1:
                i = networks[nw][-1]
                edge.append(i)
                # add 0.5 for heatmaps
                line = go.Scatter(x=[i+0.5, i+0.5],
                                y=[0-0.5, kROI-0.5],
                                mode='lines',
                                line=dict(color='black', width=0.7))
                fig.add_trace(line)
                line = go.Scatter(x=[0-0.5, kROI-0.5],
                                y=[i+0.5, i+0.5],
                                mode='lines',
                                line=dict(color='black', width=0.7))
                fig.add_trace(line)
            else:
                i = networks[nw][-1]
                edge.append(i)
                
        heatmap = go.Heatmap(z=FC,
                            zmin=-0.5,
                            zmax=0.9,
                            colorscale="RdBu",
                            reversescale=True,
                            colorbar = dict(x=0.95, len=0.95,
                                            thickness=20))
        fig.add_trace(heatmap)

        tickvals = []
        for ii in range(len(edge)-1):
            tickvals.append((edge[ii] + edge[ii+1])/2)
            
        fig.update_yaxes(autorange='reversed',
                        showgrid=False, 
                        zeroline=False,
                        ticks='inside',
                        tickvals=tickvals,
                        ticktext=[nw + ' ' for nw in networks],
                        tickangle=-30,
                        ticklen=10)
        fig.update_xaxes(showgrid=False, 
                        zeroline=False,
                        ticks='inside',
                        tickvals=tickvals,
                        ticktext=[nw for nw in networks],
                        tickangle=-30,
                        ticklen=10,
                        automargin=True)
        fig.update_layout(height=500,
                        width=480,
                        showlegend=False,
                        font=dict(family='helvetica'))

        fig.update_yaxes(scaleanchor='x')

        return fig

    def get_minimal_fig(self, FC):
        kROI = FC.shape[0]
        
        fig = go.Figure()
                
        heatmap = go.Heatmap(z=FC,
                            zmin=-0.5,
                            zmax=0.9,
                            colorscale="RdBu",
                            reversescale=True,
                            showscale=False)
        fig.add_trace(heatmap)
    
        fig.update_yaxes(autorange='reversed',
                        showgrid=False, 
                        zeroline=False,
                        showticklabels=False,
                        ticks='')
        fig.update_xaxes(showgrid=False, 
                        zeroline=False,
                        showticklabels=False,
                        ticks='')
        fig.update_layout(height=500,
                        width=480,
                        showlegend=False)

        fig.update_yaxes(scaleanchor='x')

        return fig