import statsmodels.api as sm
import pandas as pd

# Data Loading
data_paris = pd.read_csv("C:/Users/17789/Python-Project/data_paris.csv")
data_yelp = pd.read_csv("C:/Users/17789/Python-Project/yelp_results.csv", encoding='latin-1')

# Merging the datasets on a common attribute, e.g., 'location_id'
merged_data = pd.merge(data_paris, data_yelp, on=['Latitude', 'Longitude'], how='right')

# Assuming 'rating' is the column name for store ratings in data3 and 'num_bikes' for number of bicycles in data1
y = merged_data['Number_of_Bikes']
X = merged_data[['Review Count', 'Rating']]

# Adding a constant to the model (it's a best practice!)
X = sm.add_constant(X)

# Building the model
model = sm.OLS(y, X).fit()

# Getting the summary of the regression
print(model.summary())