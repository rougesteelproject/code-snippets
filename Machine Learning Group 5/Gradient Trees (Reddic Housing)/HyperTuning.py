import altair as alt
import pandas as pd
import numpy as np
import sklearn as sk

from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 1000)
# allows graph to work despite large data set
alt.data_transformers.disable_max_rows()

Data = pd.read_csv('https://raw.githubusercontent.com/byui-cse/cse450-course/master/data/housing.csv')

Model_Data = Data
#Model_Data['date'] = Model_Data['date'].dt.strftime('%Y-%m-%d')
Model_Data['bedrooms'] = Model_Data['bedrooms'].astype('int64')
Model_Data['bathrooms'] = Model_Data['bathrooms'].astype('float')
Model_Data['sqft_living'] = Model_Data['sqft_living'].astype('int64')
Model_Data['waterfront'] = Model_Data['waterfront'].astype('category')
Model_Data['view'] = Model_Data['view'].astype('category')
Model_Data['condition'] = Model_Data['condition'].astype('category')
Model_Data['grade'] = Model_Data['grade'].astype('int64')
Model_Data['zipcode'] = Model_Data['zipcode'].astype('category')

from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor

param_grid ={
    'max_depth':                [5], #5
    'min_child_weight':         [5], #5
    'subsample':                [1], #1
    'colsample_bytree':          [1], #1
    'eta':                       [.3],  #0.3 #alias "learning_rate"
    
}

X = pd.get_dummies(Model_Data, drop_first=True).drop(columns = ['price','date','id'], errors = "ignore")
y = Model_Data['price']

X_train, X_other, y_train, y_other = train_test_split(X, y, test_size=0.30, random_state = 42)
X_test, X_val, y_test, y_val = train_test_split(X_other, y_other, test_size=0.50, random_state = 42)

grid_search = GridSearchCV(XGBRegressor(), param_grid, refit = True, verbose = 3,n_jobs=-1)

grid_search.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_val, y_val)])

print("Tuned Parameters: {}".format(grid_search.best_params_))
print("Best score is {}".format(grid_search.best_score_))