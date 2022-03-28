import numpy as np
import pandas as pd
import os



class DataCleaning:


    df = None
    
    @classmethod
    def read_data(cls, file_name):           
        if os.path.isfile(file_name) and os.access(file_name, os.R_OK): #Reading the file path          
            if file_name.endswith('.csv'):  # Checking the extension
                cls.df = pd.read_csv(file_name) 
                #Renaming the columns
                cls.df.rename(columns = {
                        '01FI1101E/PV.CV'    : 'Ammonia tons/hr',
                        '01AI1923/AI1/PV.CV' : 'Humidity %',        
                        '01FI1103/AI1/PV.CV' : 'Steam tons/hr',
                        '60PI0496/AI1/PV.CV' : 'Pressure in mbara',
                        '01TI1538/AI1/PV.CV' : 'Temp °C',
                        '01HC1955/PID1/PV.CV': 'Speed of compressor rpms'                      
                        }, inplace = True, errors = 'raise')
                cls.df= cls.df.drop(['Unnamed: 0', 'utctimestamp'], axis = 1)
                                    
            else:
                return "File is not in a .csv format"         
        else:    
            return "Either the file is missing or not readable"

    @classmethod
    def delete_outliers(cls, x_percent):
        
       
       
       print('Total None Values \n', cls.df.isnull().sum())
      
       Q1 = cls.df.quantile(0.25)
       Q3 = cls.df.quantile(0.75)
       IQR = Q3 - Q1
       
       #Identifying Outliers with Interquartile Range (IQR)
       iqr_values =(cls.df<(Q1- 1.5 * IQR )) | (cls.df > (Q3 + 1.5 * IQR))
       print('Total number of outliers in each columns are \n', iqr_values[iqr_values == True].sum())

       # Outliers in Column Ammonia tons/hr
       ammonia_outlier = iqr_values.index[iqr_values['Ammonia tons/hr'] == True].tolist()
       cls.df.at[ammonia_outlier,'Ammonia tons/hr'] =  None

       # Outliers in Column Steam tons/hr
       steam_outlier = iqr_values.index[iqr_values['Steam tons/hr'] == True].tolist()
       cls.df.at[steam_outlier,'Steam tons/hr'] =  None

       # Outliers in Column Humidity %
       humidity_outlier = iqr_values.index[iqr_values['Humidity %'] == True].tolist()
       cls.df.at[humidity_outlier,'Humidity %'] =  None

       # Outliers in Column Pressure in mbara
       pressure_outlier = iqr_values.index[iqr_values['Pressure in mbara'] == True].tolist()
       cls.df.at[pressure_outlier,'Pressure in mbara'] =  None

       # Outliers in Column Temp °C
       temp_outlier = iqr_values.index[iqr_values['Temp °C'] == True].tolist()
       cls.df.at[temp_outlier,'Temp °C'] =  None    

       # Outliers in Column Speed of compressor rpms
       speed_outlier = iqr_values.index[iqr_values['Speed of compressor rpms'] == True].tolist()
       cls.df.at[speed_outlier,'Speed of compressor rpms'] =  None 

       print('Total None Values \n',cls.df.isnull().sum())



    def trimmed_mean(self, df, percent):

        trim = int((percent)*(df.shape[0])/100.0)
        return df[trim:-trim]


    @staticmethod
    def impute_missing_values(df, method = ['mode', 'median', 'mean', 'interpolate']):
        if method == 'mean':
            df.fillna(df.mean())
        elif method == 'median':
            df.fillna(df.median())
        elif method == 'mode':
            df.fillna(df.median())
        elif method == 'interpolate':
            df = df.interpolate()
        else:
            print(' Please choose between Mean, mode, median or interpolate')

data_cleaner = DataCleaning()
df = data_cleaner.read_data('data_challenge.csv')
print(df)

# print(data_cleaning.delete_outliers())

# print(DataCleaning.delete_outliers(10, 'data_challenge.csv'))

