from django.conf import settings
import pandas as pd
import numpy as np
import os

class DatasetPreprocessor():
    def __init__(self, file_path, file_name):
        self.file_path = file_path
        self.file_name = file_name
        
    def drop_blank_category_rows(self, df, cols):
        return df.dropna(subset = cols)
    
    def mean_missing_numerical_rows(self, df_values, col_indexs):
        from sklearn.impute import SimpleImputer
        imputer = SimpleImputer(missing_values = np.nan, strategy = 'mean')
        imputer.fit(df_values[:, col_indexs])
        df_values[:, col_indexs] = imputer.transform(df_values[:, col_indexs])
        return df_values
        
        
    def categorical_value_encoder(self, df_values, cols_indexs):
        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import OneHotEncoder
        
        ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), cols_indexs)], remainder='passthrough')
        df_values = np.array(ct.fit_transform(df_values))
        return df_values
    
    
    def target_value_label_encoder(self, df_values):
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        df_values[:, -1] = le.fit_transform(df_values[:, -1])
        return df_values
    
    
    def clean_file(self):
      df = pd.read_csv(self.file_path)
      categorical_columns = []
      categorical_column_indexes = []
      numerical_columns = []
      numerical_column_indexs = []
      
      for col in df.columns:
          if df[col].dtype == 'object':
              categorical_columns.append(col)
              categorical_column_indexes.append(df.columns.get_loc(col))
          elif df[col].dtype == int or df[col].dtype == float:
              numerical_columns.append(col)
              numerical_column_indexs.append(df.columns.get_loc(col))
              
      """para-metes are dataframe, array of categorial_colum_names"""
      category_cleaned_df = self.drop_blank_category_rows(df, categorical_columns)
      category_cleaned_df_values = category_cleaned_df.values
      cleaned_processed_df_values = self.mean_missing_numerical_rows(category_cleaned_df_values, numerical_column_indexs)
    #   print(cat_num_cleaned_df_values)
    
      if len(categorical_column_indexes) > 0:
        if df[df.columns[-1]].dtype == 'object':
            categorical_column_indexes = categorical_column_indexes[:-1]
        cleaned_processed_df_values = self.categorical_value_encoder(cleaned_processed_df_values, categorical_column_indexes)
     
      if df[df.columns[-1]].dtype == 'object':
        cleaned_processed_df_values = self.target_value_label_encoder(cleaned_processed_df_values)
      
      cleaned_preprocessed_df = pd.DataFrame(cleaned_processed_df_values)
      target_folder = os.path.join(settings.BASE_DIR, 'files', 'preprocessed')
      os.makedirs(target_folder, exist_ok=True)
      file_name = f"preprocessed_{self.file_name}"
      cleaned_file_path = os.path.join(target_folder, file_name)
      print(cleaned_preprocessed_df)
      print(cleaned_file_path)
      cleaned_preprocessed_df.to_csv(cleaned_file_path, index=False)
      preprocessed_file_dict = {}
      preprocessed_file_dict["filePath"] = cleaned_file_path
      preprocessed_file_dict["fileName"] = file_name
      return preprocessed_file_dict
        
      
      
      
      
      