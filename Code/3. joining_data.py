# 1. Import necessary libraries

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# 2. Data Loading

data_paris = pd.read_csv("C:/Users/17789/Python-Project/data_paris.csv")
data_yelp = pd.read_csv("C:/Users/17789/Python-Project/yelp_results.csv", encoding='latin-1')
data_foursquare = pd.read_csv("C:/Users/17789/Python-Project/foursquare_results.csv", encoding='latin-1')

# 3. Joining Data

# Merge data_paris, data_yelp
merged_paris_yelp_data = pd.merge(data_paris, data_yelp, how="cross")
# Merge data_paris, data_foursquare
merged_paris_foursquare_data = pd.merge(data_paris, data_foursquare, how="cross")

# 4. Data Cleaning

# Identify and display the number of NaNs in each column for the merged datasets

print("NaN values in merged_paris_yelp_data:")
print(merged_paris_yelp_data.isnull().sum())
print("\nNaN values in merged_paris_foursquare_data:")
print(merged_paris_foursquare_data.isnull().sum())

# Remove duplicate rows from merged_paris_yelp_data and merged_paris_foursquare_data
merged_paris_yelp_data = merged_paris_yelp_data.drop_duplicates()
merged_paris_foursquare_data = merged_paris_foursquare_data.drop_duplicates()

# 5. Data Visualization

# Scatter plot for data_part1
plt.figure(figsize=(10, 6))
plt.scatter(merged_paris_foursquare_data['Longitude'], merged_paris_foursquare_data['Latitude'], c=merged_paris_foursquare_data['Number_of_Bikes'], cmap='viridis', s=50)
plt.colorbar(label='Number of Bikes')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Distribution of Bikes in Paris')
plt.show()

# Pair plot for data_part2
sns.pairplot(merged_paris_yelp_data[['Review Count', 'Rating', 'Number_of_Bikes']], diag_kind='kde')
plt.suptitle('Pair Plot for Data Part 2', y=1.02)
plt.show()

# # Bar plot for data_part3
plt.figure(figsize=(12, 6))
sns.countplot(data=merged_paris_yelp_data, y='Category', order=merged_paris_yelp_data['Category'].value_counts().index, palette='viridis')
plt.xlabel('Count')
plt.ylabel('Category')
plt.title('Distribution of Categories in Paris')
plt.xticks(rotation=45)
plt.show()

# 6. Creating an SQLite Database

# Connect to the SQLite database
connection = sqlite3.connect("Python-Project/data/mydatabase.sqlite")
cursor = connection.cursor()

# Create the table for ParisBikes
cursor.execute("CREATE TABLE IF NOT EXISTS ParisBikes (Latitude REAL, Longitude REAL, Bikes INTEGER)")

# Create the table for FourSquare
cursor.execute("CREATE TABLE IF NOT EXISTS FourSquare (Name TEXT, Latitude REAL, Longitude REAL, Category TEXT)")

# Create the table for Yelp
cursor.execute("CREATE TABLE IF NOT EXISTS Yelp (Name TEXT, Latitude REAL, Longitude REAL, ReviewCount INTEGER, Rating REAL, Category TEXT)")

# Create the table for cross join on ParisBikes and FourSquare
cursor.execute("CREATE TABLE IF NOT EXISTS ParisBikesFourSquare (Latitude REAL, Longitude REAL, Bikes INTEGER, Name TEXT, Category TEXT)")

# Create the table for cross join on ParisBikes and Yelp
cursor.execute("CREATE TABLE IF NOT EXISTS ParisBikesYelp (Latitude REAL, Longitude REAL, Bikes INTEGER, Name TEXT, ReviewCount INTEGER, Rating REAL, Category TEXT)")

data_paris.to_sql("ParisBikes", connection, if_exists="replace", index=False)
data_foursquare.to_sql("FourSquare", connection, if_exists="replace", index=False)
data_yelp.to_sql("Yelp", connection, if_exists="replace", index=False)
merged_paris_foursquare_data.to_sql("ParisBikesFourSquare", connection, if_exists="replace", index=False)
merged_paris_yelp_data.to_sql("ParisBikesYelp", connection, if_exists="replace", index=False)

connection.commit()

# 7. Data Validation

#Query the first few rows from the database to validate
cursor.execute("SELECT * FROM ParisBikes LIMIT 5;")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.execute("SELECT * FROM FourSquare LIMIT 5;")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.execute("SELECT * FROM Yelp LIMIT 5;")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.execute("SELECT * FROM ParisBikesFourSquare LIMIT 10;")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.execute("SELECT * FROM ParisBikesYelp LIMIT 10;")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the database connection
connection.close()