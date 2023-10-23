# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import visualize

# Incorporate data
zni_df = pd.read_csv('datasets/Energia_en_ZNI.csv')

zni_df = zni_df.rename(columns={'ID DEPATAMENTO':'PROVINCE_ID', 'DEPARTAMENTO':'PROVINCE','ID MUNICIPIO':'CITY_ID','MUNICIPIO':'CITY','ID LOCALIDAD':'ZONE_ID','LOCALIDAD':'ZONE','AÑO SERVICIO':'SERVICE_YEAR', 
                                    'MES SERVICIO':'SERVICE_MONTH','ENERGÍA ACTIVA':'ACTIVE_POWER','ENERGÍA REACTIVA':'REACTIVE_POWER','POTENCIA MÁXIMA':'MAX_POWER',
                                    'DÍA DE DEMANDA MÁXIMA':'MAX_DEMAND_DAY','FECHA DE DEMANDA MÁXIMA':'MAX_DEMAND_DATE','PROMEDIO DIARIO EN HORAS':'DAILY_MEAN_HOURS'})
    

# Initialize the app - incorporate css
external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/litera/bootstrap.min.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H1("Dashboard of the Non-Interconnected Areas in Colombia", className="title",style={'color':'#008080','textAlign': 'center'}),  # Set the title
    # Add a blank space using CSS style
    html.Div(style={'margin-top': '20px'}),
    html.H4("Energy consumption analysis for the non-interconnected areas of Colombia", className="alert-heading", style={'textAlign': 'center'}),
                html.A("The non-interconnected zones (ZNI) are regions that do not receive public electricity service through the national grid, also known as the national interconnected system (SIN)", className="alert-link", href="#", style={'textAlign': 'center'}),
    html.Div(children = '''
            Dataset: 
    ''',style={'margin-left': '20px', 'margin-right': '20px','textAlign': 'center'}),

    html.Div(style={'margin-top': '20px'}),

    html.Div(className='row', children=[
        html.Div(style={'margin-left': '100px', 'margin-right': '20px','width': '85%', 'height': 'auto'},className='six columns', children=[
            dash_table.DataTable(data=zni_df.to_dict('records'), page_size=11, style_table={'overflowX': 'auto'})
        ])
    ]),

    html.H2("Active power peak value by location", className="subtitle",style={'color':'#008080','textAlign': 'center'}),
    html.Div(style={'margin-top': '20px'}),
    html.Div(children = '''
            Choose a type of location to display:
    ''',style={'margin-left': '20px', 'margin-right': '20px','textAlign': 'center'}),
    html.Div(style={'margin-top': '20px'}),
    # Create a new row for the RadioItems
    html.Div(style={'margin-left': '20px'},className='row', children=[
        html.Div(className='six columns', children=[
            dcc.RadioItems(
                options=['ZONE', 'CITY', 'PROVINCE'],
                value='ZONE',
                inline=True,
                id='my-radio-buttons-final',
                labelStyle={'display': 'block', 'margin-bottom': '10px'}
                
            )
        ])
    ]),
    
    # Create a new row for the last two graphs (placed in the same row)
    html.Div(style={'margin-left': '20px', 'margin-right': '20px'},className='row', children=[
        html.Div(className='six columns', children=[
            dcc.Graph(figure={}, id='bar-chart-high-act-en')
        ]),
        html.Div(className='six columns2', children=[
            dcc.Graph(figure={}, id='bar-chart-low-act-en')
        ])
    ]),

    
    html.H2("Active energy analysis", className="subtitle",style={'color':'#008080','textAlign': 'center'}),
    html.Div(style={'margin-top': '20px'}),
    html.H3("Mean active energy", className="subtitle",style={'textAlign': 'center'}),
    # Create a new row for the last two graphs (placed in the same row)
    
    html.Div(className='row', children=[
        html.Div(className='twelve columns', children=[
            
            dcc.Graph(figure={}, id='mean-act-e')  # Display the Plotly figure in this new row
        ]),
        html.Div(className='twelve columns', children=[
            
            dcc.Graph(figure={}, id='mean-act-p-prov')  # Display the Plotly figure in this new row
        ])
    ]),

    html.Div(style={'margin-top': '20px'}),
    html.H3("Hours of power demanded", className="subtitle",style={'textAlign': 'center'}),
    html.Div(style={'margin-top': '20px'}),
    html.Div(className='row', children=[
        html.Div(className='twenty-four columns', children=[
            
            dcc.Graph(figure={}, id='mean-h')  # Display the Plotly figure in this new row
        ]),
        html.Div(className='twenty-four columns', children=[
            
            dcc.Graph(figure={}, id='mean-h-z')  # Display the Plotly figure in this new row
        ])
    ]),

    html.Div(style={'margin-top': '20px'}),
    html.H3("Power Factor", className="subtitle",style={'textAlign': 'center'}),
    html.Div(style={'margin-top': '20px'}),
    html.Div(className='row', children=[
        html.Div(style={'display': 'flex', 'justify-content': 'center'},className='twenty-four columns', children=[
            
            dcc.Graph(figure={}, id='h_power-factor')  # Display the Plotly figure in this new row
        ]),
        html.Div(style={'display': 'flex', 'justify-content': 'center'},className='twenty-four columns', children=[
            
            dcc.Graph(figure={}, id='l_power-factor')  # Display the Plotly figure in this new row
        ])
    ]),
    
    html.Div(style={'margin-top': '20px'}),
    html.H2("Wind Power", className="subtitle",style={'textAlign': 'center'}),
    html.Img(src="assets\powerdensityimg.jpg", style={'width': '95%', 'height': 'auto','textAlign': 'center'}),
    

    html.Div(style={'margin-top': '20px'}),
    html.H2("Solar Atlas", className="subtitle",style={'width': '95%', 'height': 'auto','textAlign': 'center'}),
    html.Div(style={'margin-top': '20px'}),
    html.Div(className='row', children=[
        html.Div(style={'margin-left': '400px', 'margin-right': '20px'},className='twenty-four columns', children=[
            
            dcc.Graph(figure={}, id='solar_atlas')  # Display the Plotly figure in this new row
        ]),
        #html.Div(className='twenty-four columns', children=[
            
        #    dcc.Graph(figure={}, id='solar_atlas2')  # Display the Plotly figure in this new row
        #]),
        
    ]),
])



# Add controls to build the interaction
@callback(
    Output(component_id='bar-chart-high-act-en', component_property='figure'),
    Input(component_id='my-radio-buttons-final', component_property='value')
)
def update_high_bar_chart(location):
    fig = visualize.max_power(location)
    return fig


@callback(

    Output(component_id='bar-chart-low-act-en', component_property='figure'),
    Input(component_id='my-radio-buttons-final', component_property='value')
)
def update_low_bar_chart(location):
    fig2 = visualize.max_power(location, range='min')
    return fig2

@callback(

    Output(component_id='mean-act-e', component_property='figure'),
    Input(component_id='my-radio-buttons-final', component_property='value')
)
def mean_act_chart(location):
    fig2 = visualize.mean_act_energy_year()
    return fig2

@callback(

    Output(component_id='mean-act-p-prov', component_property='figure'),
    Input(component_id='my-radio-buttons-final', component_property='value')
)
def mean_zone_act_chart(location):
    fig2 = visualize.mean_act_power_province()
    return fig2

@callback(

    Output(component_id='mean-h', component_property='figure'),
    Input(component_id='my-radio-buttons-final', component_property='value')
)
def mean_h(location):
    fig2 = visualize.mean_hours()
    return fig2

@callback(

    Output(component_id='mean-h-z', component_property='figure'),
    Input(component_id='my-radio-buttons-final', component_property='value')
)
def mean_h_z(location):
    fig2 = visualize.mean_hours_zones()
    return fig2

@callback(

    Output(component_id='l_power-factor', component_property='figure'),
    Input(component_id='my-radio-buttons-final', component_property='value')
)
def h_power_factor(location):
    fig2 = visualize.power_factor(location)
    return fig2
@callback(

    Output(component_id='h_power-factor', component_property='figure'),
    Input(component_id='my-radio-buttons-final', component_property='value')
)
def l_power_factor(location):
    fig2 = visualize.power_factor(location,range='min')
    return fig2

@callback(

    Output(component_id='solar_atlas', component_property='figure'),
    Input(component_id='my-radio-buttons-final', component_property='value')
)
def solar_atlas(location):
    fig2 = visualize.solar_map()
    return fig2

'''@callback(

    Output(component_id='solar_atlas2', component_property='figure'),
    Input(component_id='my-radio-buttons-final', component_property='value')
)
def solar_atlas(location):
    fig2 = visualize.solar_map2()
    return fig2
'''
# Run the app
if __name__ == '__main__':
    app.run(debug=True)
