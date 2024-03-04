import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc 
import dash_html_components as html

flightCrashes_data = pd.read_csv('AbdessamadTzn_flightCrashes_cleanedData.csv', encoding='ISO-8859-1')

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('Flight Crashes Visualization', 
                                        style={'textAlign':'center'}
                                        ),
                                dcc.Dropdown(id='years-dropdown',
                                options=[{'label':'All years', 'value':'All'}],
                                value = "ALL",
                                placeholder = "Select a year",
                                searchable=True
                                )


                    ])



if __name__ == '__main__':
    app.run_server()