import streamlit as st
st.set_page_config(
     page_title="Yara Visulizations App",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
    #  menu_items={
    #      'Get Help': 'https://www.extremelycoolapp.com/help',
    #      'Report a bug': "https://www.extremelycoolapp.com/bug",
    #      'About': "# This is a header. This is an *extremely* cool app!"
    #  }
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
        st.title('')
        st.title('')
        def min_max_values(col):
            top = df[col].idxmax()
            top_obs = pd.DataFrame(df.loc[top])
            
            bottom = df[col].idxmin()
            bot_obs = pd.DataFrame(df.loc[bottom])
            
            min_max_obs = pd.concat([top_obs, bot_obs], axis = 1)
        
            return min_max_obs
        st.subheader(f'The Min and Max values for {x_axis} are as under:')    
        min_max = min_max_values(x_axis)
        st.write(min_max)
    
    
    
    else:
        st.write('choose the Feature to view')
    
    col41, col42, col43, col44, col45, col46 = st.columns(6)
    
    
    
    if col42.button('close'):
        col41.button('show heat map')
    elif col41.button('show heat map'):
        fig3, ax = plt.subplots()
        heat_map = sns.heatmap(df.corr(),
            cmap = 'viridis', vmax = 1.0, vmin = -1.0, linewidths = 0.1,
            annot = True, square = True )
    
        st.pyplot(fig3)
     




   
    st.write('Total Nan Values', df.isna().sum())

    st.write('Q1 = df.quantile(0.25)')
    st.write('Q3 = df.quantile(0.75)')
    st.write('IQR = Q3 - Q1')
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1

    st.write('Identifying Outliers with Interquartile Range (IQR)')
    iqr_values = (df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))
    st.write('Total number of outliers in each columns are \n', iqr_values[iqr_values == True].sum())

    
    # Outliers in Column Ammonia tons/hr
    
    ammonia_outlier = iqr_values.index[iqr_values['Ammonia tons/hr'] == True].tolist()
    df.at[ammonia_outlier, 'Ammonia tons/hr'] = None

    # Outliers in Column Steam tons/hr

    steam_outlier = iqr_values.index[iqr_values['Steam tons/hr'] == True].tolist()
    df.at[steam_outlier, 'Steam tons/hr'] = None

    # Outliers in Column Humidity %
    humidity_outlier = iqr_values.index[iqr_values['Humidity %'] == True].tolist()
    df.at[humidity_outlier, 'Humidity %'] = None

    # Outliers in Column Pressure in mbara
    pressure_outlier = iqr_values.index[iqr_values['Pressure in mbara'] == True].tolist()
    df.at[pressure_outlier, 'Pressure in mbara'] = None

    # Outliers in Column Temp °C
    temp_outlier = iqr_values.index[iqr_values['Temp °C'] == True].tolist()
    df.at[temp_outlier, 'Temp °C'] = None

    # Outliers in Column Speed of compressor rpms
    speed_outlier = iqr_values.index[iqr_values['Speed of compressor rpms'] == True].tolist()
    df.at[speed_outlier, 'Speed of compressor rpms'] = None

    st.write('Total None Values after changing None to the outliers \n', df.isnull().sum())


    st.write('📢 Shape of the Dateframe',df.shape)

    def delete_outliers(df,x_percent):
        if x_percent != 0:
            trim = int((x_percent) * (df.shape[0]) / 100.0)
            df = df[trim:-trim]
            return df
        else:
            return df
    col71,col72 = st.columns(2)
    number = col71.slider('choose percentage to trim', 0 , 50, 10)
    df = delete_outliers(df, number)
    st.write(f'The shape of Dataframe after trimming  {number}% is', df.shape)

    def impute_missing_values(df, method):
        if method == 'mean':
            df = df.fillna(df.mean())
        elif method == 'median':
            df = df.fillna(df.median())
        elif method == 'mode':
            df = df.fillna(df.median())
        else:
            method == 'interpolate'
            df = df.interpolate()
        return df

    col81, col82,col83 = st.columns(3)
    option = col81.selectbox('How would you like to be impute?',('Mean', 'Median', 'Mode', 'interpolate'))
   
    df = impute_missing_values(df, option) 
    st.write('Total None Values after imputing',df.isna().sum())
    
    
    
    
    
    
    
    
    
    
    
    
    
    st.title('--------------------------------------------------------------------------------')
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

        
        st.header('Baseline Graphs')
        df_describe = df.describe()
        df_describe = df_describe.drop(['count'], axis = 0)
        # col91, col92, col93, col94, col95, col96, col97 = st.columns(7)
        # t25 = col91.number_input('25%',0 )
        # t50 = col92.number_input('50%',0 )
        # t75 = col93.number_input('75%',0 )
        # max = col94.number_input('max',0 )
        # mean = col95.number_input('mean',0 )
        # min = col96.number_input('min',0 )
        # std = col97.number_input('std',0 )
        # pd.dataframe 
        selected_columns_st_3 = df_describe.columns.tolist() 
        selected_columns_3 = st.multiselect('', selected_columns_st_3, key='baselinegraphs')
        st.dataframe(df_describe[selected_columns_3])
        st.line_chart(data = df_describe[selected_columns_3])
       


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