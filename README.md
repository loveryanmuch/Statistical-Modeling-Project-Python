# Final-Project-Statistical-Modelling-with-Python

## Project/Goals
This project is to develop a robust regression model that can accurately estimate the number of bicycles available in the city of Paris. Additionally, this project seeks to delve into the characteristics and features of cafes and bars within the city. Through comprehensive data analysis and modeling, it aims to uncover valuable insights that can inform decision-making and urban planning related to both bike-sharing programs and the food and beverage industry in Paris.

## Process
### Step 1: CityBikes API Exploration
    1) Get familiar with the CityBikes API structure and data.
    2) Choose a city from the API's coverage and collect information about its bike stations, including their locations and available bikes.
    3) Convert this data into a user-friendly Pandas dataframe.

### Step 2: Foursquare and Yelp API Connection
    1) Establish connections to both the Foursquare and Yelp APIs.
    2) For each bike station identified in Part 1, query both APIs to retrieve details about nearby restaurants, bars, and other points of interest (POIs).
    3) Organize the obtained data into separate dataframes for Yelp and Foursquare results.
    4) Assess and compare data quality between the two APIs.

### Step 3: Data Integration and Visualization
    1) Merge the data from Part 1 (bike stations) with Part 2 (POI data) to create a comprehensive dataset.
    2) Employ data visualization techniques to gain insights from the combined data.
    3) Establish an SQLite database to store the POI data systematically, ensuring proper structure.
    4) Verify the integrity of the database to maintain data quality.
    
### Step 4: Regression Modeling and Analysis
    1) Build a regression model using Python's statsmodels module to uncover relationships between bike quantities and POI attributes.
    2) Interpret the model's findings, extracting meaningful insights.
    3) Optionally, explore how to transform this regression problem into a classification task.

## Results
The data from Parisian stores (including cafes and bars) revealed no discernible correlation with City bikes(bicycle) in terms of categories, ratings, or the number of reviews. Additionally, there doesn't seem to be any relationship between store ratings, review counts, and the distribution of bicycles in the city. It may be worth considering a re-analysis using different variables.

## Challenges 
API Rate Limiting: Both Foursquare and Yelp APIs have request limits for free tiers, which slowed down the data collection process and the availability of bikes changes throughout the day, making it a dynamic feature. The static nature of the dataset made it challenging to capture this dynamism adequately.

## Future Goals
As there are many bicycle stations, we should try to visualize cleaner data by checking how it affects not only cafes and bars but also other factors.
