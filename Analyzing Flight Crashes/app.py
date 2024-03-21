#import libraries
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc 
import dash_html_components as html
import plotly.graph_objects as go
# import dash_ag_grid as dag

#incorporate dataa
df = pd.read_csv('AbdessamadTzn_flightCrashes_cleanedData.csv', encoding='ISO-8859-1')

#intialise app
app = dash.Dash(__name__)

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
fig = px.scatter_geo(Frequent_5_locations, 
                        lat='Latitude', 
                        lon='Longitude', 
                        color="Location",
                        size='count',
                        hover_name='Location', 
                        animation_frame="Year",
                        projection="natural earth")
#TODO: in callbacks...flexible year choosing for animation

# locations="iso_alpha", color="continent",
#                      hover_name="country", size="pop",
#                      animation_frame="year",
#                      projection="natural earth")



app.layout = html.Div([
    html.Div(children=html.H1('Flight Crashes Dashboard', 
                                        style={'textAlign':'center'}
                                        )),
    html.H2('Frequent 5 locations of crashes in 1908'),
    
    dcc.Graph(figure=fig, id='graph1')
                            



                    ])
#Layout ends

#Controls for building the interactiont



if __name__ == '__main__':
    app.run_server(debug=True)