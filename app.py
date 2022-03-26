from asyncio.windows_events import NULL
import streamlit as st
st.set_page_config(
     page_title="Yara Visulizations App",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
 )


#importing the libraries
import numpy as np
import pandas as pd
import seaborn as sns
import altair as alt
import matplotlib.pyplot as plt
from io import BytesIO

st.title('Check Visualisations')


#Uploading a file
uploaded_file = st.file_uploader("Choose a csv file")
if uploaded_file is not None:
    df= pd.read_csv(uploaded_file)
    df.rename(columns = {
                        '01FI1101E/PV.CV'    : 'Ammonia tons/hr',
                        '01AI1923/AI1/PV.CV' : 'Humidity %',
                        '01FI1103/AI1/PV.CV' : 'Steam tons/hr',
                        '60PI0496/AI1/PV.CV' : 'Pressure in mbara',
                        '01TI1538/AI1/PV.CV' : 'Temp °C',
                        '01HC1955/PID1/PV.CV': 'Speed of compressor rpms'                      
                        }, inplace = True, errors = 'raise')
    st.write('file loading sucessful...')
    df = df.drop(['Unnamed: 0', 'utctimestamp'], axis = 1)

    # Viewing the desired columns
    selected_columns = df.columns.tolist()  
    st.subheader('Select the features to view the dataframe')
    selected_columns_st = st.multiselect('', selected_columns,selected_columns)
    if not len(selected_columns_st) == 0:
        df_altered = df[(selected_columns_st)]
        st.dataframe(df_altered.head(5))
        st.header('')

        # Boxplots
        plt.title('Scatter Plots')
        fig1, ax = plt.subplots(figsize=(15, 5))
        sns.boxplot(data=df_altered)

        st.write(fig1)

        # Distplots
        plt.title('Distplots')
        fig2, ax = plt.subplots(figsize=(15, 5))
        sns.distplot(df_altered, bins=20)
        st.write(fig2)
        st.title('')



        # Subheader for defining the height and width of the graphs
        st.header('Lets look at the scatter plots')
        col3 , col4 = st.columns(2)
        col3.subheader('Size of the plots 👇')
        col1 , col2, col5, col6 = st.columns(4)
        width = col1.slider("Plot width", 4., 9., 8., key='width_slider' )
        height = col2.slider("Plot height", 4., 9., 4., key='height_slider') 


        # Scatter Plots
        col4.subheader('Select your features 👇')
        x_axis = col5.selectbox('Choose X-axis to plot from the features' ,(df.columns))
        y_axis = col6.selectbox('Choose Y-axis to plot from the features' ,(df.columns))
        x_axis_df = df[(x_axis)]
        y_axis_df = df[(y_axis)]
        fig, ax = plt.subplots(figsize=(width, height))
        scatter = ax.scatter(x_axis_df, y_axis_df)
        plt.xlabel(x_axis_df.name)
        plt.ylabel(y_axis_df.name)
        plt.legend(*scatter.legend_elements())
        plt.title('Scatter Plots')
        buf = BytesIO()
        fig.savefig(buf, format="png")
        st.image(buf)

        
    
    
    
    else:
        st.write('choose the Feature to view')
    st.title('--------------------------------------------------------------------------------')

    st.write('📢Looking at scatter plots and box plot we find out that for column ammonia all the values below 300 must be trimmed')
    #remove outliers in ammonia
    remove_outlier_ammonia = df[df['Ammonia tons/hr']<300].index
    df.drop(remove_outlier_ammonia, inplace=True, axis = 0)
    
    st.write('📢Looking at scatter plots and box plot we find out that for column Humidity all the values below 42 must be trimmed')
    # Remove outlier in Humidity
    remove_outlier_humidity = df[df['Humidity %']<42].index
    df.drop(remove_outlier_humidity, inplace=True, axis = 0)
    
    st.write('📢Looking at scatter plots and box plot we find out that for column Humidity all the values below 0 must be trimmed')
    #Remove outlier in Steam
    remove_outlier_steam = df[df['Steam tons/hr']<0].index
    df.drop(remove_outlier_steam, inplace=True, axis = 0)
    
    st.write('📢Looking at scatter plots and box plot we find out that for column Humidity all the values below 3906 must be trimmed')
    # Remove outlier of speed
    remove_outlier_speed= df[df['Speed of compressor rpms']<3906].index
    df.drop(remove_outlier_speed, inplace=True, axis = 0)

    st.write('📢 Shape of the Dateframe',df.shape)

    
    
    
    selected_columns_2 = df.columns.tolist()  
    st.subheader('Select the features to view the dataframe')
    selected_columns_st_2 = st.multiselect('', selected_columns_2)
    if not len(selected_columns_st_2) == 0:
        df_altered = df[(selected_columns_st_2)]
        st.dataframe(df_altered.head(5))
        st.header('')

        # Boxplots
        plt.title('Scatter Plots')
        fig1, ax = plt.subplots(figsize=(15, 5))
        sns.boxplot(data=df_altered)

        st.write(fig1)

        # Distplots
        plt.title('Distplots')
        fig2, ax = plt.subplots(figsize=(15, 5))
        sns.distplot(df_altered, bins=20)
        st.write(fig2)
        st.title('')



        # Subheader for defining the height and width of the graphs
        st.header('Lets look at the scatter plots')
        col11 , col12 = st.columns(2)
        col11.subheader('Size of the plots 👇')
        col13 , col14, col15, col16 = st.columns(4)
        width = col13.slider("Plot width", 4., 9., 8., key='width_slider1' )
        height = col14.slider("Plot height", 4., 9., 4., key='height_slider1') 


        # Scatter Plots
        col12.subheader('Select your features 👇')
        x_axis = col15.selectbox('Choose X-axis to plot from the features' ,(df.columns), key='1')
        y_axis = col16.selectbox('Choose Y-axis to plot from the features' ,(df.columns), key='1')
        x_axis_df = df[(x_axis)]
        y_axis_df = df[(y_axis)]
        fig, ax = plt.subplots(figsize=(width, height))
        scatter = ax.scatter(x_axis_df, y_axis_df)
        plt.xlabel(x_axis_df.name)
        plt.ylabel(y_axis_df.name)
        plt.legend(*scatter.legend_elements())
        plt.title('Scatter Plots')
        buf = BytesIO()
        fig.savefig(buf, format="png")
        st.image(buf)
      
    else:
        st.write('choose the Feature to view')