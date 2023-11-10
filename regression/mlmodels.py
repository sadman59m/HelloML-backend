import pandas as pd
import numpy as np


class LinearRegression():
    
    def __init__(self, file_path, split_ratio):
        """Coustructor for Linear Regression Model"""
        self.file_path = file_path
        self.split_ratio = split_ratio
        
        
    def get_dataset(self):
        """Get the preprocessed dataset and convert it to pandas dataframe"""
        return pd.read_csv(self.file_path)
        
    def perform_regression(self):
        df = self.get_dataset()
        X = df.iloc[:, :-1].values
        y = df.iloc[:, -1].values
        # print(X)
        # print(y)
        
    