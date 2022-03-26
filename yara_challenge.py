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
                return df              
            else:
                return "File is not in a .csv format"         
        else:    
            return "Either the file is missing or not readable"

    # def delete_outliers(x_percent):




data_cleaning = DataCleaning('data_challenge.csv')
print(data_cleaning.read_data())


