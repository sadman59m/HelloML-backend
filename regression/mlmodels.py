import pandas as pd
import numpy as np


class LinearRegression():
    
    def __init__(self, df_values, split_ratio):
        """Coustructor for Linear Regression Model"""
        self.df_values = df_values
        self.split_ratio = split_ratio
        
        
    def perform_regression(self):
        df_values = np.array(self.df_values)
        X = df_values[:, :-1]
        y = df_values[:, -1]
        # print(X)
        # print(y)
        # # trains test split
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=float(self.split_ratio), random_state=0)
        print(len(X_train))
        print(len(X_test))
        
        # applying linear regression
        from sklearn.linear_model import LinearRegression
        # default parameters
        regressor = LinearRegression()
        regressor.fit(X_train, y_train)
        y_pred = regressor.predict(X_test)
        
        #r2 score metrics
        from sklearn.metrics import r2_score
        r2_score_value = r2_score(y_test, y_pred)
        print(r2_score_value)
        
    