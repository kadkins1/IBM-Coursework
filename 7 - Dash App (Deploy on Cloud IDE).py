# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create options lists for dropdown
launch_options = [{'label': 'All Sites', 'value': 'ALL'}]
for i in spacex_df['Launch Site'].unique():
    launch_options.append({'label': i, 'value': i})

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id ='site-dropdown', options= launch_options, value = 'ALL', 
                                placeholder='Select a Site', searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(0, 10000, 1000, value= [min_payload, max_payload], id='payload-slider'),  

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(
    Output(component_id = 'success-pie-chart', component_property = 'figure'),
    Input(component_id = 'site-dropdown', component_property = 'value'))
    
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df[spacex_df['class']==1], values='class', names='Launch Site', title='Succesful Launches by Site')
        return fig
    else:
        filtered_df = spacex_df.loc[spacex_df['Launch Site'] == entered_site,:]
        fig = px.pie(data_frame = filtered_df, names = 'class', title=f'Launch Outcomes for Site {entered_site}')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
    Input(component_id = 'payload-slider', component_property = 'value'),
    Input(component_id = 'site-dropdown', component_property = 'value'))

def get_scatter(payload_slider, site_dropdown):
    if site_dropdown == 'ALL':
        scatter_all_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_slider[0]) & (spacex_df['Payload Mass (kg)'] <= payload_slider[1])]
        fig = px.scatter(data_frame = scatter_all_df, x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category', title = 'Correlation between Payload Weight and Launch Success for All Sites') 
        return fig
    else:
        filtered_df = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown,:]
        scatter_some_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_slider[0]) & (filtered_df['Payload Mass (kg)'] <= payload_slider[1])]
        fig = px.scatter(data_frame = scatter_some_df, x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category', title = f'Correlation between Payload Weight and Launch Success for {site_dropdown}') 
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
