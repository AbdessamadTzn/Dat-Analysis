import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, callback, Output, Input
from dash import html

flightCrashes_data = pd.read_csv('AbdessamadTzn_flightCrashes_cleanedData.csv', encoding='ISO-8859-1')

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1(children='Flight Crashes Visualization', style={'textAlign':'center'}),
    ]
)
#TODO...