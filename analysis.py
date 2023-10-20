import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
import plotly.figure_factory as ff # for plot heatmap
from plotly.offline import init_notebook_mode
init_notebook_mode(connected=True)
import warnings
warnings.filterwarnings('ignore')

# helpful modules
import fuzzywuzzy
from fuzzywuzzy import process
import charset_normalizer

# Tips data available in the plotly express module
df_tips=px.data.tips()
# Gapminder data available in the plotly express module
population= px.data.gapminder()



zni_df = pd.read_csv('datasets/Energia_en_ZNI.csv')

zni_df = zni_df.rename(columns={'ID DEPATAMENTO':'PROVINCE_ID', 'DEPARTAMENTO':'PROVINCE','ID MUNICIPIO':'CITY_ID','MUNICIPIO':'CITY','ID LOCALIDAD':'ZONE_ID','LOCALIDAD':'ZONE','AÑO SERVICIO':'SERVICE_YEAR', 
                                    'MES SERVICIO':'SERVICE_MONTH','ENERGÍA ACTIVA':'ACTIVE_POWER','ENERGÍA REACTIVA':'REACTIVE_POWER','POTENCIA MÁXIMA':'MAX_POWER',
                                    'DÍA DE DEMANDA MÁXIMA':'MAX_DEMAND_DAY','FECHA DE DEMANDA MÁXIMA':'MAX_DEMAND_DATE','PROMEDIO DIARIO EN HORAS':'DAILY_MEAN_HOURS'})




#Show first 5 zones with lowest and highest 'max power' values
def show_max_power(location):
    max_power = zni_df.groupby(location).MAX_POWER.max().sort_values(ascending=False)
    max_power = pd.DataFrame(max_power).reset_index()

    # Remove parentheses and their contents for visualization purposes
    max_power[location] = max_power[location].str.replace(r'\s*\(.*\)', '', regex=True)

    #print(max_power)

    # Create bar chart
    fig=px.bar(max_power[:5],x=location,y="MAX_POWER",title="Highest 'Maximum power' service daily sample")
    # Update marker color
    fig.update_traces(marker=dict(color='#008080'))

    # Set automargin for x-axis tick labels to True
    fig.update_xaxes(automargin=True)

    # Show the plot
    fig.show()

    # Create bar chart
    fig=px.bar(max_power[-5:],x=location,y="MAX_POWER",title="Lowest 'Maximum power' service daily sample")
    # Update marker color
    fig.update_traces(marker=dict(color='#008080'))

    # Set automargin for x-axis tick labels to True
    fig.update_xaxes(automargin=True)

    # Show the plot
    st.plotly_chart(fig, use_container_width=True, sharing='streamlit')