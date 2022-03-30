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
        # try:
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
                print("File is not in a .csv format")
        # except:
        else:
            print('File does not exist')

    @classmethod
    def replace_outliers_none(cls):

        Q1 = cls.df.quantile(0.25)
        Q3 = cls.df.quantile(0.75)
        IQR = Q3 - Q1

        # Identifying Outliers with Interquartile Range (IQR)
        iqr_values = (cls.df < (Q1 - 1.5 * IQR)) | (cls.df > (Q3 + 1.5 * IQR))
        print('Total number of outliers in each columns are \n', iqr_values[iqr_values == True].sum())

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

        print('Total None Values \n', cls.df.isnull().sum())

    @classmethod
    def delete_outliers(cls, x_percent):
        print(cls.df.shape)
        trim = int((x_percent) * (cls.df.shape[0]) / 100.0)
        cls.df = cls.df[trim:-trim]
        print(cls.df.shape)

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
            sns.boxplot(x=cls.df[column])
            plt.title(f'{column}')
            plt.show()
            sns.displot(cls.df[column])
            plt.title(f'{column}')
            plt.show()

        sns.heatmap(cls.df.corr(),
                    cmap='viridis', vmax=1.0,
                    vmin=-1.0, linewidths=0.1,
                    annot=True, square=True)
        plt.show()

    @staticmethod
    def read_baseline(baseline):
        column_stats = {}

        for column, stats in baseline.items():
            column_stat = ColumnStatics(stats['average'], stats['std'], stats['min'], stats['max'])
            column_stats[column] = column_stat
        return column_stats

    @classmethod
    def calculate_internal_baseline(cls):
        baseline = {}
        column_stats = {}
        df_describe = cls.df.describe()
        df_describe.drop(['count', '25%', '50%', '75%'], inplace=True, axis=0)
        for i in df_describe.columns:
            baseline[i] = df_describe[i]
            column_stat = ColumnStatics(baseline[i]['mean'], baseline[i]['std'], baseline[i]['min'], baseline[i]['max'])
            column_stats[i] = column_stat
        return column_stats

    @staticmethod
    def compare_to_baseline(baseline, external_baseline):
        p_threshold = 0.6
        n_threshold = -0.6
        cols = {}
        for column in baseline.keys():
            column_baseline = baseline[column].__dict__
            v ={column:column_baseline}
            cols.update(v)
        base_df = pd.DataFrame(cols)   
        test_col = {}
        for row_ in external_baseline.keys():
            for column_ in external_baseline:
                external_column_baseline = external_baseline[column_].__dict__
                y = {row_:external_column_baseline}
                test_col.update(y)
        test_df = pd.DataFrame(test_col)
        new_base_df = base_df[test_df.columns.to_list()] 
        new_base_df = new_base_df.T
        test_df = test_df.T
        compare_df = pd.concat([new_base_df, test_df], axis = 1)
        if new_base_df.equals(test_df):
            print('The column data is similar to the baseline')
        else:
            compare_df['correlation'] = new_base_df.corrwith(test_df, axis=1)
            for index, i in enumerate(compare_df['correlation']):
                if n_threshold < i < p_threshold:
                    print(f'Warning: The statistics of the column data do not agree with the baseline for {compare_df.T.keys()[index]}')
        print(compare_df)
        for i in test_df.T.columns:
            sns.lineplot(x= test_df.T.index, y =i, data = test_df.T)
            sns.lineplot(x= new_base_df.T.index, y =i, data = new_base_df.T)
            plt.title('Comparing the Statistics')
            plt.legend(['External Baseline','Internal Baseline'])
            plt.show()








data_cleaner = DataCleaning()
data_cleaner.read_data('data_challenge.csv')
# data_cleaner.replace_outliers_none()
# data_cleaner.delete_outliers(10)
# print(data_cleaner.df.shape)
data_cleaner.impute_missing_values('mean')
# print(data_cleaner.df.isna().sum())
# data_cleaner.calculate_statics()
external_baseline = DataCleaning.read_baseline({'Ammonia tons/hr': {'average': 5, 'std': 0.2, 'min': 6, 'max': 12}})
baseline = DataCleaning.calculate_internal_baseline()
# print(baseline)
DataCleaning.compare_to_baseline(baseline, external_baseline)

