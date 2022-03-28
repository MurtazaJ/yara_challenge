import statistics
import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from columnstatics import ColumnStatics

class DataCleaning:

    df = None

    @classmethod
    def read_data(cls, file_name):
        try:
            if os.path.isfile(file_name) and os.access(file_name, os.R_OK):  # Reading the file path
                if file_name.endswith('.csv'):  # Checking the extension
                    cls.df = pd.read_csv(file_name)
                    # Renaming the columns
                    cls.df.rename(columns={
                        '01FI1101E/PV.CV': 'Ammonia tons/hr',
                        '01AI1923/AI1/PV.CV': 'Humidity %',
                        '01FI1103/AI1/PV.CV': 'Steam tons/hr',
                        '60PI0496/AI1/PV.CV': 'Pressure in mbara',
                        '01TI1538/AI1/PV.CV': 'Temp °C',
                        '01HC1955/PID1/PV.CV': 'Speed of compressor rpms'
                    }, inplace=True, errors='raise')
                    cls.df = cls.df.drop(['Unnamed: 0', 'utctimestamp'], axis=1)
                else:
                    return "File is not in a .csv format"
        except Exception as e:
            raise e

    @classmethod
    def delete_outliers(cls, x_percent):

        # print('Total None Values \n', cls.df.isnull().sum())

        Q1 = cls.df.quantile(0.25)
        Q3 = cls.df.quantile(0.75)
        IQR = Q3 - Q1

        # Identifying Outliers with Interquartile Range (IQR)
        iqr_values = (cls.df < (Q1 - 1.5 * IQR)) | (cls.df > (Q3 + 1.5 * IQR))
        # print('Total number of outliers in each columns are \n', iqr_values[iqr_values == True].sum())

        # Outliers in Column Ammonia tons/hr
        ammonia_outlier = iqr_values.index[iqr_values['Ammonia tons/hr'] == True].tolist()
        cls.df.at[ammonia_outlier, 'Ammonia tons/hr'] = None

        # Outliers in Column Steam tons/hr
        steam_outlier = iqr_values.index[iqr_values['Steam tons/hr'] == True].tolist()
        cls.df.at[steam_outlier, 'Steam tons/hr'] = None

        # Outliers in Column Humidity %
        humidity_outlier = iqr_values.index[iqr_values['Humidity %'] == True].tolist()
        cls.df.at[humidity_outlier, 'Humidity %'] = None

        # Outliers in Column Pressure in mbara
        pressure_outlier = iqr_values.index[iqr_values['Pressure in mbara'] == True].tolist()
        cls.df.at[pressure_outlier, 'Pressure in mbara'] = None

        # Outliers in Column Temp °C
        temp_outlier = iqr_values.index[iqr_values['Temp °C'] == True].tolist()
        cls.df.at[temp_outlier, 'Temp °C'] = None

        # Outliers in Column Speed of compressor rpms
        speed_outlier = iqr_values.index[iqr_values['Speed of compressor rpms'] == True].tolist()
        cls.df.at[speed_outlier, 'Speed of compressor rpms'] = None

        # print('Total None Values \n', cls.df.isnull().sum())
        trim = int((x_percent) * (cls.df.shape[0]) / 100.0)
        cls.df = cls.df[trim:-trim]
        


    @classmethod
    def impute_missing_values(cls, method):
        if method == 'mean':
            cls.df = cls.df.fillna(cls.df.mean())
        elif method == 'median':
            cls.df = cls.df.fillna(cls.df.median())
        elif method == 'mode':
            cls.df = cls.df.fillna(cls.df.median())
        elif method == 'interpolate':
            cls.df = cls.df.interpolate()
        else:
            print(' Please choose between Mean, mode, median or interpolate')
        
    @classmethod
    def calculate_statics(cls):
        print(cls.df.describe())

        def min_max_values(col):
            top = cls.df[col].idxmax()
            top_obs = pd.DataFrame(cls.df.loc[top])           
            bottom = cls.df[col].idxmin()
            bot_obs = pd.DataFrame(cls.df.loc[bottom])          
            min_max_obs = pd.concat([top_obs, bot_obs], axis = 1)         
            return min_max_obs

        for column in cls.df.columns:
            print(f"The Skewnes in {column} is ", cls.df[column].skew())
            print(f'The Max and Min value for {column} is \n', min_max_values(column))
            sns.boxplot(x= cls.df[column])
            plt.title(f'{column}')
            plt.show()
            sns.histplot(cls.df[column])
            plt.title(f'{column}')
            plt.show()

        sns.heatmap(cls.df.corr(),
                    cmap = 'viridis', vmax = 1.0, 
                    vmin = -1.0, linewidths = 0.1,
                    annot = True, square = True )
        plt.show()



    @classmethod
    def read_baseline(cls, baseline):
        column_stats = {}

        for column, stats in baseline.items():        
            column_stat = ColumnStatics( stats['average'], stats['min'],stats['max'], stats['std'] )
            column_stats[column] = column_stat



data_cleaner = DataCleaning()
data_cleaner.read_data('data_challenge.csv')
# data_cleaner.delete_outliers(10)

# print(data_cleaner.df.shape)
# data_cleaner.impute_missing_values('mean')
# print(data_cleaner.df)
# data_cleaner.calculate_statics()
data_cleaner.read_baseline({'col_xyz': {'average': 5, 'min': 2, 'max': 6, 'std': 0.2}})