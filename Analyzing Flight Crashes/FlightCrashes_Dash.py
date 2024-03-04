import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc 
import dash_html_components as html

flightCrashes_data = pd.read_csv('AbdessamadTzn_flightCrashes_cleanedData.csv', encoding='ISO-8859-1')

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1(children='Flight Crashes Visualization', style={'textAlign':'center'}),
        html.Div('Data Visualization of Cleaned flight crashes dataset ')
    ]
)
#contnue setting up...

if __name__ == '__main__':
    app.run_server()