#import libraries
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

import plotly.graph_objects as go
import dash_ag_grid as dag
import datetime as dt

#incorporate data
df = pd.read_csv('AbdessamadTzn_flightCrashes_cleanedData.csv', encoding='ISO-8859-1')

#Extract year and month from the date column
df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
df['Year'] = pd.to_datetime(df['Date']).dt.year

#intialise app
app = dash.Dash(__name__, assets_folder='assets')

#Layout Section of Dash
max_rows=10 #TODO: user define it...

''' From data analysis
A bubble map with animation for most 5 locations where crashes happened
'''

locations_data = {
    'Location': ['Moscow, Russia', 'Manila, Philippines', 'New York, New York', 'Cairo, Egypt', 'Sao Paulo, Brazil'],
    'count': [21, 15, 14, 13, 13],
    'Latitude': [55.7558, 14.5995, 40.7128, 30.0444, -23.5505],
    'Longitude': [37.6176, 120.9842, -74.0060, 31.2357, -46.6333],
    'Year': [1908, 1908, 1908, 1908, 1908]
}

Frequent_5_locations = pd.DataFrame(locations_data)

#Plot the fig
fig1 = px.scatter_geo(Frequent_5_locations, 
                        lat='Latitude', 
                        lon='Longitude', 
                        color="Location",
                        size='count',
                        hover_name='Location', 
                        animation_frame="Year",
                        projection="natural earth")
''' 
TODO
Pie chart, shows for every year, totala numbers of ftalities,
fatalitites passengers, 
fatalities crew,
ground..
depends on user pereference
'''

# locations="iso_alpha", color="continent",
#                      hover_name="country", size="pop",
#                      animation_frame="year",
#                      projection="natural earth")



app.layout = html.Div([
    html.Div([

        html.Div(children=html.H1('Analytic App - Flight Crashes', 
                                            style={'textAlign':'center'}
                                            )),
    html.Div([
            html.H4("This analytic app is under development",
                style={'textAlign': 'center', 'color':'red'}  
            ),
            html.A("Source Code Github", href="https://github.com/AbdessamadTzn/Self-Taught-Data-Scientist/tree/main/Analyzing%20Flight%20Crashes",
                target="_blank",
            ),
    ],
        style={'marginTop': 10, 'textAlign':'center'}  
    ),

        html.Div([
            html.H2('Select Year', style={'margin-right': '2rem'}),
            dcc.Dropdown(df.Year.unique(), value=2002, id='year'),
        dcc.Graph(id='plot1')
        ],
        style={'width': '49%','float': 'left', 'display': 'inline-block'})
                ]),
        html.Div([
            html.H2('Most 5 frequent countries with Fatalities', style={'margin-right': '2rem'}),
            dcc.Graph(figure=fig1)
        ],
        style={'width': '49%', 'float': 'right', 'display': 'inline-block', 'textAlign':'center'}
        )

])
    # #Layout ends

#Controls for building the interactiont
@app.callback(
    Output(component_id='plot1', component_property='figure'),  # Update 'figure' property
    Input(component_id='year', component_property='value')
)
def pie_year(input_year):
    selected_year_data = df[df['Year'] == input_year]
    total_fatalities = selected_year_data['Fatalities'].sum()
    survivors = selected_year_data['Aboard'].sum() - total_fatalities #calculate survivors

    fig = px.pie(
        selected_year_data,
        values=[total_fatalities, survivors],
        names=['Fatalities', 'Survivors'],  # Explicit labels for hover text
        hole=0.3,  # Donut effect
        color_discrete_sequence=px.colors.sequential.Plasma,
        title=f'Total Fatalities for Year {input_year}'
    )
    fig.update_traces(textposition='inside', textinfo='percent', textfont_size=12)  # Percentages inside

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)