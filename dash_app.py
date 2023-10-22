# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Incorporate data
zni_df = pd.read_csv('datasets/Energia_en_ZNI.csv')

zni_df = zni_df.rename(columns={'ID DEPATAMENTO':'PROVINCE_ID', 'DEPARTAMENTO':'PROVINCE','ID MUNICIPIO':'CITY_ID','MUNICIPIO':'CITY','ID LOCALIDAD':'ZONE_ID','LOCALIDAD':'ZONE','AÑO SERVICIO':'SERVICE_YEAR', 
                                    'MES SERVICIO':'SERVICE_MONTH','ENERGÍA ACTIVA':'ACTIVE_POWER','ENERGÍA REACTIVA':'REACTIVE_POWER','POTENCIA MÁXIMA':'MAX_POWER',
                                    'DÍA DE DEMANDA MÁXIMA':'MAX_DEMAND_DAY','FECHA DE DEMANDA MÁXIMA':'MAX_DEMAND_DATE','PROMEDIO DIARIO EN HORAS':'DAILY_MEAN_HOURS'})
    

# Initialize the app - incorporate css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

# App layout
app.layout = html.Div([
    html.Div(className='row', children='Dashboard of the Non-Interconnected Areas in Colombia',
             style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),

    html.Div(className='row', children=[
        dcc.RadioItems(options=['ZONE', 'CITY', 'PROVINCE'],
                       value='ZONE',
                       inline=True,
                       id='my-radio-buttons-final')
    ]),

    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dash_table.DataTable(data=zni_df.to_dict('records'), page_size=11, style_table={'overflowX': 'auto'})
        ]),
        html.Div(className='six columns', children=[
            dcc.Graph(figure={}, id='bar-chart-high-act-en')

        ]),
        html.Div(className='six columns', children=[
            dcc.Graph(figure={}, id='bar-chart-low-act-en')

        ])
    ])
])

# Add controls to build the interaction
@callback(
    Output(component_id='bar-chart-high-act-en', component_property='figure'),
    Input(component_id='my-radio-buttons-final', component_property='value')
)
def update_graph(location):
    
    max_power = zni_df.groupby(location).MAX_POWER.max().sort_values(ascending=False)
    max_power = pd.DataFrame(max_power).reset_index()

    # Remove parentheses and their contents for visualization purposes
    max_power[location] = max_power[location].str.replace(r'\s*\(.*\)', '', regex=True)

    #print(max_power)

    # Create bar chart
    fig1=px.bar(max_power[:5],x=location,y="MAX_POWER",title="Highest 'Maximum power' service daily sample")
    # Update marker color
    fig1.update_traces(marker=dict(color='#008080'))

    # Set automargin for x-axis tick labels to True
    fig1.update_xaxes(automargin=True)

    return fig1


@callback(

    Output(component_id='bar-chart-low-act-en', component_property='figure'),
    Input(component_id='my-radio-buttons-final', component_property='value')
)
def update_graph(location):
    
    max_power = zni_df.groupby(location).MAX_POWER.max().sort_values(ascending=False)
    max_power = pd.DataFrame(max_power).reset_index()

    # Remove parentheses and their contents for visualization purposes
    max_power[location] = max_power[location].str.replace(r'\s*\(.*\)', '', regex=True)

    #print(max_power)

    # Create bar chart
    fig2=px.bar(max_power[-5:],x=location,y="MAX_POWER",title="Lowest 'Maximum power' service daily sample")
    # Update marker color
    fig2.update_traces(marker=dict(color='#008080'))

    # Set automargin for x-axis tick labels to True
    fig2.update_xaxes(automargin=True)

    return fig2


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
