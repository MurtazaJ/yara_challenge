import numpy as np
import pandas as pd
import os



class DataCleaning:

    def __init__(self, file_name):
        self.file_name = file_name

    
    def read_data(self):           
        if os.path.isfile(self.file_name) and os.access(self.file_name, os.R_OK):           
            if self.file_name.endswith('.csv'):
                df = pd.read_csv(self.file_name)
                df.rename(columns = {
                        '01FI1101E/PV.CV'    : 'Ammonia tons/hr',
                        '01AI1923/AI1/PV.CV' : 'Humidity %',
                        '01FI1103/AI1/PV.CV' : 'Steam tons/hr',
                        '60PI0496/AI1/PV.CV' : 'Pressure in mbara',
                        '01TI1538/AI1/PV.CV' : 'Temp °C',
                        '01HC1955/PID1/PV.CV': 'Speed of compressor rpms'                      
                        }, inplace = True, errors = 'raise')
                return df              
            else:
                return "File is not in a .csv format"         
        else:    
            return "Either the file is missing or not readable"

    def delete_outliers(x_percent):




data_cleaning = DataCleaning('data_challenge.csv')
print(data_cleaning.read_data())


