import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go 
import plotly.figure_factory as ff # for plot heatmap
from plotly.offline import init_notebook_mode
init_notebook_mode(connected=True)
import warnings
warnings.filterwarnings('ignore')

import rasterio as rio

from matplotlib.colors import LightSource

# Tips data available in the plotly express module
df_tips=px.data.tips()
# Gapminder data available in the plotly express module
population= px.data.gapminder()



zni_df = pd.read_csv('datasets/Energia_en_ZNI.csv')

zni_df = zni_df.rename(columns={'ID DEPATAMENTO':'PROVINCE_ID', 'DEPARTAMENTO':'PROVINCE','ID MUNICIPIO':'CITY_ID','MUNICIPIO':'CITY','ID LOCALIDAD':'ZONE_ID','LOCALIDAD':'ZONE','AÑO SERVICIO':'SERVICE_YEAR', 
                                    'MES SERVICIO':'SERVICE_MONTH','ENERGÍA ACTIVA':'ACTIVE_POWER','ENERGÍA REACTIVA':'REACTIVE_POWER','POTENCIA MÁXIMA':'MAX_POWER',
                                    'DÍA DE DEMANDA MÁXIMA':'MAX_DEMAND_DAY','FECHA DE DEMANDA MÁXIMA':'MAX_DEMAND_DATE','PROMEDIO DIARIO EN HORAS':'DAILY_MEAN_HOURS'})




#Show first 5 zones with lowest and highest 'max power' values
def max_power(location, range='max'):
    max_power = zni_df.groupby(location).MAX_POWER.max().sort_values(ascending=False)
    max_power = pd.DataFrame(max_power).reset_index()

    # Remove parentheses and their contents for visualization purposes
    max_power[location] = max_power[location].str.replace(r'\s*\(.*\)', '', regex=True)

    if range == 'max':
        # Create bar chart
        fig=px.bar(max_power[:5],x=location,y="MAX_POWER",title="Highest 'Maximum power' service daily sample")
    else: 
        # Create bar chart
        fig=px.bar(max_power[-5:],x=location,y="MAX_POWER",title="Lowest 'Maximum power' service daily sample")
    
    # Update marker color
    fig.update_traces(marker=dict(color='#008080'))

    # Set automargin for x-axis tick labels to True
    fig.update_xaxes(automargin=True)

    return fig
    
def mean_act_energy_year():
    
    years = [2020, 2021,2022,2023]
    result = pd.DataFrame(columns=years)
    
    for year in years:
        power = zni_df.loc[zni_df['SERVICE_YEAR'] == year]
        power = power.groupby('SERVICE_MONTH').ACTIVE_POWER.mean()
        result[year] = power
    
    total_act_energy = zni_df.groupby('SERVICE_MONTH').ACTIVE_POWER.mean()
    result['TOTAL'] = total_act_energy
    
    mean_act_energy_year = result
    mean_act_energy_year = mean_act_energy_year.reset_index()

    # Create a figure object for which we can later add the plots
    fig = go.Figure()

    # pass the graph objects to the add trace method, assign a series to x and y parameters of graph objects.
    fig.add_trace(go.Scatter(x=mean_act_energy_year['SERVICE_MONTH'], y=mean_act_energy_year[2020], mode='lines',line_color='#AF4343' ,name='2020'))
    fig.add_trace(go.Scatter(x=mean_act_energy_year['SERVICE_MONTH'], y=mean_act_energy_year[2021], mode='lines+markers',line_color='#fcbca2' ,name='2021'))

    # Customizing a particular line
    fig.add_trace(go.Scatter(x=mean_act_energy_year['SERVICE_MONTH'], y=mean_act_energy_year[2022], 
                            mode='lines+markers', name='2022',line_color='red'  ,                   
                            line=dict(color='darkgreen', dash='dot')))

    fig.add_trace(go.Scatter(x=mean_act_energy_year['SERVICE_MONTH'], y=mean_act_energy_year[2023], mode='lines+markers',line_color='#6A5ACD' ,name='2023'))
    # Further style the figure

    temp = dict(layout=go.Layout(font=dict(family="Franklin Gothic", size=12)))
    fig.update_traces(marker=dict(line=dict(width=1, color='#000000')))
    fig.update_layout(title="Mean demand per month (All zones)", showlegend=True, template=temp, 
                    legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=.97),
                    barmode='group', bargap=.15)

    return fig

def loc_m_act_energy_year(location):

    years = [2020, 2021,2022,2023]
    result = pd.DataFrame(columns=years)

    for year in years:
        hours = zni_df.loc[zni_df['SERVICE_YEAR'] == year]
        total_hours = hours.groupby(location).ACTIVE_POWER.mean()
        result[year] = total_hours

    total_hours = zni_df.groupby(location).ACTIVE_POWER.mean()
    result['TOTAL'] = total_hours
    result = result.reset_index()
    
    return result



def mean_act_power_province():
    pal = sns.color_palette("mako", 5).as_hex()
    province_m_act_energy = loc_m_act_energy_year('PROVINCE')
    province_m_act_energy = province_m_act_energy.reset_index()

    fig = px.pie(province_m_act_energy, values='TOTAL', names='PROVINCE', title='Mean active power by province',color_discrete_sequence=pal)

    #fig.update_traces(hoverinfo='label+percent', textfont_size=15, 
    #                  textinfo="label+percent ", pull=[0.05, 0, 0, 0, 0],
    #                  marker_line=dict(color="#FFFFFF", width=2))

    temp = dict(layout=go.Layout(font=dict(family="Franklin Gothic", size=12)))
    fig.update_layout(template=temp, title='Mean active power by province', 
                    uniformtext_minsize=15, uniformtext_mode='hide',width=800)
    return fig

def sum_h_year(location):
    
    years = [2020, 2021,2022,2023]
    result = pd.DataFrame(columns=years)
    
    for year in years:
        hours = zni_df.loc[zni_df['SERVICE_YEAR'] == year]
        total_hours = hours.groupby(location).DAILY_MEAN_HOURS.mean()
        result[year] = total_hours
    
    total_hours = zni_df.groupby(location).DAILY_MEAN_HOURS.mean()
    result['TOTAL'] = total_hours
    return result

def mean_hours():

    province_hours = sum_h_year('PROVINCE')
    pal = sns.color_palette("mako", 5).as_hex()
    province_hours = province_hours.reset_index()

    fig = px.pie(province_hours, values='TOTAL', names='PROVINCE', title='Mean service hours by province',color_discrete_sequence=pal)

    #fig.update_traces(hoverinfo='label+percent', textfont_size=15, 
    #                  textinfo="label+percent ", pull=[0.05, 0, 0, 0, 0],
    #                  marker_line=dict(color="#FFFFFF", width=2))

    temp = dict(layout=go.Layout(font=dict(family="Franklin Gothic", size=12)))
    fig.update_layout(template=temp, title='Mean service hours by province', 
                    uniformtext_minsize=15, uniformtext_mode='hide',width=800)
    return fig

def mean_hours_zones():
    names_24to18,names_17to12,names_11to6,names_5to0 = [], [], [], []
    n_24to18,n_17to12,n_11to6,n_5to0= 0,0,0,0

    zone_hours = sum_h_year('ZONE')

    for i in range(0,102):
        if zone_hours['TOTAL'].iloc[i] >17:
            
            n_24to18 += 1
            names_24to18.append(zone_hours['TOTAL'].index[i])

        elif zone_hours['TOTAL'].iloc[i] <= 17 and zone_hours['TOTAL'].iloc[i] >=12:

            n_17to12 += 1
            names_17to12.append(zone_hours['TOTAL'].index[i])
            
        elif zone_hours['TOTAL'].iloc[i] <= 11 and zone_hours['TOTAL'].iloc[i] >=6:

            n_11to6 += 1
            names_11to6.append(zone_hours['TOTAL'].index[i])
        
        else:

            n_5to0 += 1
            names_5to0.append(zone_hours['TOTAL'].index[i])

    pal = sns.color_palette("mako", 5).as_hex()

    dic = {'Number of hours':['24 to 18','17 to 12', '11 to 6','5 to 0'],
        'Value':[n_24to18,n_17to12,n_11to6,n_5to0]}

    n_hours_per_zone = pd.DataFrame(dic)

    fig = px.pie(n_hours_per_zone, values='Value', names='Number of hours', title='Zones divided by amount of mean daily hours of power consumption',color_discrete_sequence=pal)

    fig.update_traces(hoverinfo='label+percent', textfont_size=15, 
                    textinfo="label+percent ", pull=[0.05, 0, 0, 0, 0],
                    marker_line=dict(color="#FFFFFF", width=2))

    temp = dict(layout=go.Layout(font=dict(family="Franklin Gothic", size=12)))
    fig.update_layout(template=temp, title='Hours of power consumption', 
                    uniformtext_minsize=15, uniformtext_mode='hide',width=800)
    
    return fig

# Calculate the Power Factor for each row
def calculate_power_factor(row):
    if row['ACTIVE_POWER'] !=0 and row['REACTIVE_POWER'] !=0:
        return row['ACTIVE_POWER'] / math.sqrt(row['ACTIVE_POWER']**2 + row['REACTIVE_POWER']**2)
    else:
        return 0
    
zni_df['POWER_FACTOR'] =  zni_df.apply(calculate_power_factor, axis=1)
zni_df['POWER_FACTOR']

#Show first 5 zones with lowest and highest 'max power' values
def power_factor(location,range='max'):
    power_factor = zni_df.groupby(location).POWER_FACTOR.mean().sort_values(ascending=False)
    power_factor = pd.DataFrame(power_factor).reset_index()

    # Remove parentheses and their contents for visualization purposes
    power_factor[location] = power_factor[location].str.replace(r'\s*\(.*\)', '', regex=True)

    if range == 'max':
        # Create bar chart
        fig=px.bar(power_factor[:5],x=location,y="POWER_FACTOR",title="Highest 'POWER_FACTOR'")
    else:
        # Create bar chart
        fig=px.bar(power_factor[-5:],x=location,y="POWER_FACTOR",title="Lowest 'POWER_FACTOR'")
    
    # Update marker color
    fig.update_traces(marker=dict(color='#008080'))

    # Set automargin for x-axis tick labels to True
    fig.update_xaxes(automargin=True)

    return fig


def solar_map():
    # Create the choropleth map
    with rio.open('datasets\Colombia_GISdata_LTAy_YearlyMonthlyTotals_GlobalSolarAtlas-v2_GEOTIFF\PVOUT.tif') as src:  
        solar_data = src.read(1)
    fig= px.imshow(solar_data)
    
    my_layout= dict(title_text='Photovoltaic power potential [kWh/kWp] in Colombia', title_x=0.5, width =700, height=500, template='none', 
                  coloraxis_colorbar=dict(len=0.75, thickness=25))

    fig.update_traces(customdata=solar_data, hovertemplate='PVOUT [kWh/kWp]: %{customdata}<extra></extra>')
    fig.update_layout(**my_layout)

    return fig

def solar_map2():
    # Create the choropleth map
    with rio.open('datasets\Colombia_GISdata_LTAy_YearlyMonthlyTotals_GlobalSolarAtlas-v2_GEOTIFF\GHI.tif') as src:  
        solar_data = src.read(1)
    fig= px.imshow(solar_data)
    
    my_layout= dict(title_text='Global horizontal irradiation [kWh/m2] in Colombia', title_x=0.5, width =700, height=500, template='none', 
                  coloraxis_colorbar=dict(len=0.75, thickness=25))

    fig.update_traces(customdata=solar_data, hovertemplate='GHI [kWh/m2]: %{customdata}<extra></extra>')
    fig.update_layout(**my_layout)

    return fig

#def wind_map():
    # Create the choropleth map
    with rio.open('datasets\COL_power_density\COL_power-density_100m.tif') as src:  
        solar_data = src.read(1)
    fig= px.imshow(solar_data)
    
    my_layout= dict(title_text='Wind power in Colombia', title_x=0.5, width =700, height=500, template='none', 
                  coloraxis_colorbar=dict(len=0.75, thickness=25))

    fig.update_traces(customdata=solar_data, hovertemplate='Wind power: %{customdata}<extra></extra>')
    fig.update_layout(**my_layout)

    return fig

    
