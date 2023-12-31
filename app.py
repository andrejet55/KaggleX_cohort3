import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
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
import analysis

#App's primary structure
def estructure():
        
    # App title
    st.markdown("<h1 style='text-align: center;'>EDA for Non-Interconnected Areas in Colombia</h1>", unsafe_allow_html=True)
    st.sidebar.image("zni.jpeg")
    
        # Info
    with st.sidebar:
        selected = option_menu(
        menu_title = "ZNI Colombia",
        options = ["EDA"],
        icons = ["book"],
        menu_icon = "globe-americas",
        default_index = 0,)

    # More info
    if selected=="EDA":
        
        st.sidebar.subheader("ZNI in Colombia")
        #description of the model
        st.sidebar.write("The non-interconnected zones (ZNI) are regions that do not receive public electricity service through the national grid, also known as the national interconnected system (SIN)")

     # Create tabs
    tabs = st.tabs(["Pandas", "Sweetviz"])

    return(tabs)

#number of zones with complete data and more tha half of the data
def complete_Data(zni_df):
    n_complete = 0
    names_complete = []
    names_half = []
    n_half = 0

    for i in range(0,134):
        if int(zni_df.ZONE.value_counts().iloc[i]) == 42:
            
            n_complete += 1
            names_complete.append(zni_df.ZONE.value_counts().index[i])

        if int(zni_df.ZONE.value_counts().iloc[i]) >= 21:

            n_half += 1
            names_half.append(zni_df.ZONE.value_counts().index[i])

    print(f'Zones with complete data: {n_complete} \nZones with more than half of data: {n_half}')
    print(f'Zones with complete data: {names_complete}')
    
    n_half = n_half -n_complete
    less_than_half = len(zni_df.ZONE.value_counts()) - n_half

    labels = ['Complete data', 'Half data', 'Less than half']
    sizes = [n_complete, n_half, less_than_half]
    
    # Create the pie chart
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that the pie chart is circular.
    
    return fig

#Show first 5 zones with lowest and highest 'max power' values
def show_max_power(location,zni_df):
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

    st.plotly_chart(fig, use_container_width=True, sharing='streamlit')

    # Create bar chart
    fig=px.bar(max_power[-5:],x=location,y="MAX_POWER",title="Lowest 'Maximum power' service daily sample")
    # Update marker color
    fig.update_traces(marker=dict(color='#008080'))

    # Set automargin for x-axis tick labels to True
    fig.update_xaxes(automargin=True)

    # Show the plot
    st.plotly_chart(fig, use_container_width=True, sharing='streamlit')

#EDA with pandas
def pd_visualization():

    zni_df = pd.read_csv('datasets/Energia_en_ZNI.csv')

    zni_df = zni_df.rename(columns={'ID DEPATAMENTO':'PROVINCE_ID', 'DEPARTAMENTO':'PROVINCE','ID MUNICIPIO':'CITY_ID','MUNICIPIO':'CITY','ID LOCALIDAD':'ZONE_ID','LOCALIDAD':'ZONE','AÑO SERVICIO':'SERVICE_YEAR', 
                                    'MES SERVICIO':'SERVICE_MONTH','ENERGÍA ACTIVA':'ACTIVE_POWER','ENERGÍA REACTIVA':'REACTIVE_POWER','POTENCIA MÁXIMA':'MAX_POWER',
                                    'DÍA DE DEMANDA MÁXIMA':'MAX_DEMAND_DAY','FECHA DE DEMANDA MÁXIMA':'MAX_DEMAND_DATE','PROMEDIO DIARIO EN HORAS':'DAILY_MEAN_HOURS'})
    st.write("First 5 rows of data")
    st.dataframe(zni_df.head())

    st.write("Dataset shape")
    st.write(zni_df.shape)

    st.subheader("Number of complete/half samples")
    st.write("The dataset contains data from January of 2020 to June of 2023. Unfortunately not every zone has "+
             "a complete number of samples as we can see:")
    pie_chart1=complete_Data(zni_df)
    st.pyplot(pie_chart1)

    st.write("First 5 zones with the greatest power demand")
    max_power = zni_df.groupby('ZONE').MAX_POWER.max().sort_values(ascending=False)
    st.line_chart(max_power[:6])
    print(max_power[:6])

    st.write("First 5 zones with the greatest power demand")
    #analysis.show_max_power('ZONE')
    show_max_power('ZONE',zni_df)

#clasiffication using the model
def LinkScribe(tabs):
    label=[]
    #"APP" tab content
    with tabs[0]:
        
        # Subpage content
        st.markdown("<h1 style='text-align:;'>Exploratory Data Analysis using pandas</h1>", unsafe_allow_html=True)
        
        #  Submit
        visualization_button = st.button("Show visualization")

        #Check the input
        if visualization_button:
            pd_visualization()

#Communication with the database to fetch for data
def sweetviz_tab(tabs):
     with tabs[1]:
        
        st.write("code for sweetviz")

        zones = ['Business/Corporate', 'Computers and Technology',
        'E-Commerce', 'Education', 'Food', 'Forums', 'Games']

        # Sidebar para la búsqueda por categoría
        st.header("Filter by Zone")
        zone_filter = st.multiselect("Select zone", zones)

def run():
    tabs = estructure()
    LinkScribe(tabs)
    sweetviz_tab(tabs)

run()
