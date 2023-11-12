import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score


class BaseRegression():
    """Calss for refactoring the common functionality"""
    
    def __init__(self, df_values, split_ratio):
        """Constructor for Base Class. Will receive the parameters I pass
        in the child classes"""
        self.df_values = df_values
        self.split_ratio = split_ratio
        
    
    def split_data(self):
        """For spliting the dataset into train and test set"""
        df_values = np.array(self.df_values)
        X = df_values[:, :-1]
        y = df_values[:, -1]
        return train_test_split(X, y, 
                                test_size=float(self.split_ratio), 
                                random_state=0,
                               )
        
    def evaluate_model_r2_score(self, y_test, y_pred):
        """Evaluation model performance using R2 score method"""
        return r2_score(y_test, y_pred)



class LinearRegressionClass(BaseRegression):
    """Class for performing linear regression"""
        
    def perform_regression(self):
        """Perform the linear regression operation"""
        try:
            X_train, X_test, y_train, y_test = self.split_data()
            
            # applying linear regression
            from sklearn.linear_model import LinearRegression
            # default parameters
            regressor = LinearRegression()
            regressor.fit(X_train, y_train)
            y_pred = regressor.predict(X_test)
            
            #r2 score metrics
            """Pass parameter (test data, predicted data)"""
            model_r2_score = self.evaluate_model_r2_score(y_test, y_pred)
            return model_r2_score
            
        except Exception as e:
            print(f"Error in Linear {e}")
            return None
        


class SupportVectorRegressorClass(BaseRegression):
    """Class for performing Support Vector Regression"""
        
    def perform_regression(self):
        """Perform the SVR operation"""
        try:
            X_train, X_test, y_train, y_test = self.split_data()
            from sklearn.svm import SVR
            #using radial basis function(rbf) kernel
            regressor = SVR(kernel='rbf')
            regressor.fit(X_train, y_train)
            
            y_pred = regressor.predict(X_test)
            
            # evaluation model performance
            """Pass parameter (test data, predicted data)"""
            model_r2_score = self.evaluate_model_r2_score(y_test, y_pred)
            return model_r2_score
        
        except Exception as e:
            print(f"Error in SVR {e}")
            return None
        
        

class DecisionTreeRegressorClass(BaseRegression):
    """Class For DecitionTree Regression"""
    
    def perform_regression(self):
        """ Performing Regresseion """
        try:
             X_train, X_test, y_train, y_test = self.split_data()
             from sklearn.tree import DecisionTreeRegressor
             regressor = DecisionTreeRegressor(random_state=0)
             regressor.fit(X_train, y_train)
             
             y_pred = regressor.predict(X_test)
             
             """Pass parameter (test data, predicted data)"""
             model_r2_socre = self.evaluate_model_r2_score(y_test, y_pred)
             return model_r2_socre
            
        except Exception as e:
            print(f"Error in Decition Tree Regressor {e}")
            return None
        
        
class RandomForestRegressorClass(BaseRegression):
    
    def perform_regression(self):
        """performing Random Forest Regression"""
        try:
             X_train, X_test, y_train, y_test = self.split_data()
             from sklearn.ensemble import RandomForestRegressor
             
             # number of trees 15
             regressor = RandomForestRegressor(n_estimators=15, random_state=0)
             regressor.fit(X_train, y_train)
             
             #predict the X_test result
             y_pred = regressor.predict(X_test)
             
             """Pass parameter (test data, predicted data)"""
             model_r2_socre = self.evaluate_model_r2_score(y_test, y_pred)
             return model_r2_socre
         
        except Exception as e:
             print(f"Error in Random Forest {e}")
             return None