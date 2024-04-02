#Import libraries
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output
'''
import plotly.graph_objects as go
import dash_ag_grid as dag
'''
import datetime as dt

# Incorporate data
df = pd.read_csv('Data/cleaned_data.csv', encoding='ISO-8859-1')



# Intialize app
app = dash.Dash(__name__, assets_folder='assets', title='Flight Crashes')

# Layout Section of Dash

max_rows=10 #TODO: user define it...

''' 
From data analysis
A bubble map with animation for most 5 locations where crashes happened
'''

locations_data = {
    'Location': ['Moscow, Russia', 'Manila, Philippines', 'New York, New York', 'Cairo, Egypt', 'Sao Paulo, Brazil'],
    'count': [21, 15, 14, 13, 13],
    'Latitude': [55.7558, 14.5995, 40.7128, 30.0444, -23.5505],
    'Longitude': [37.6176, 120.9842, -74.0060, 31.2357, -46.6333],
}

Frequent_5_locations = pd.DataFrame(locations_data)

# Plot the static fig
fig2 = px.scatter_geo(Frequent_5_locations, 
                        lat='Latitude', 
                        lon='Longitude', 
                        color="Location",
                        size='count',
                        hover_name='Location', 
                        #animation_frame="Year",
                        projection="natural earth")
''' 
TODO
Pie chart, shows for every year, total numbers of ftalities,
fatalitites passengers, 
fatalities crew,
ground..
depends on user pereference
'''

unique_routes = df['Route'].unique()
contact_me = html.Div([
            "by  ",
           html.A("Abdessamad Touzani", href="https://www.linkedin.com/in/abdessamadtouzani",
                target="_blank",)
            
],style={"display": "inline-block", "margin-left": "10px"})

app.layout = html.Div([
    # First division for the title and info
    html.Div([
        html.Div(children=html.H1('Analytic App - Flight Crashes', style={'textAlign':'center'})),
        html.Div([
            html.H4("This analytic app is under development", style={'textAlign': 'center', 'color':'red'}),  
            html.A("Source Code Github && Analysis Process", href="https://github.com/AbdessamadTzn/Self-Taught-Data-Scientist/tree/main/Analyzing%20Flight%20Crashes",
                target="_blank",
            ),
            contact_me,
        ], style={'marginTop': 10, 'textAlign':'center'}),  
    ]),

    # Second division for the dropdown && 2 graphs
    html.Div([
        # 1.1 graph
        html.Div([
            html.H2('Select Year', style={'margin-right': '2rem'}),
            dcc.Dropdown(options=[{'label': year, 'value': year} for year in df['Year'].unique()], value=2002, id='year'),
            dcc.Graph(id='plot1')
        ], style={'width': '49%', 'float': 'left', 'display': 'inline-block'}),
        
        # 1.2 graph
        html.Div([
            html.H2('Most 5 frequent countries with Fatalities since 1908', style={'margin-right': '2rem'}),
            dcc.Graph(figure=fig2)
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block', 'textAlign':'center'})
    ]),
    # Third Division
    html.Div([
        # 2.1 graph
        html.Div([
        html.H2('Select a Route', style={'text-align': 'center'}),
        dcc.Dropdown(id='route',value='Test flight', options=[{'label': route, 'value': route} for route in unique_routes ]),
        dcc.Graph(id='plot2')
        ]
        #style={'width': '49%', 'float': 'right', 'display': 'inline-block', 'textAlign':'center'}
        )
        # 2.2 graph
    ])

])

# Layout ends

# Controls for building the interactions

# First Division
@app.callback(
    Output(component_id='plot1', component_property='figure'),  # Update 'figure' property
    Input(component_id='year', component_property='value')
)
def pie_year(input_year):
    selected_year_data = df[df['Year'] == input_year]
    total_fatalities = selected_year_data['Fatalities'].sum()
    survivors = selected_year_data['Aboard'].sum() - total_fatalities #calculate survivors

    if input_year is None:
        return {}
    else:
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

# Second Division
@app.callback(
    Output(component_id='plot2', component_property='figure'),
    Input(component_id='route', component_property='value')
)
def routes_crashes(input_route):
    if input_route is None:
        return {}
    
    # Filter the DataFrame based on the selected route
    filtered_df = df[df['Route'] == input_route]
    
    # Group by year and count the number of crashes
    yearly_crashes_counts = filtered_df.groupby(filtered_df['Year']).size()    
    # Create the plot
    fig = px.line(x=yearly_crashes_counts.index, y=yearly_crashes_counts,
                  title=f'Distribution of Flight Crashes Over the Years for Route {input_route}',
                  labels=[{'x' : 'Years', 'y':'Crashes'}])
    fig.update_xaxes(title_text='Year')
    fig.update_yaxes(title_text='Number of Crashes')
    
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)