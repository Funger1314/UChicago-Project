# UChicago MSADS -Project
This project performs an exploratory data analysis (EDA) on Chicago real estate data using Python. It demonstrates practical data-cleaning, feature-engineering, and visualization techniques that are commonly used in data science and analytics.

Dataset

This project uses the Chicago House Price dataset from Kaggle:
https://www.kaggle.com/datasets/tawfikelmetwally/chicago-house-price. The CSV was downloaded locally and referenced as real_estate_data_chicago.csv. Please follow Kaggle’s dataset terms if you redistribute or publish derived data.

1. Import Libraries

Essential Python libraries are imported for data handling and visualization:
pandas, numpy, and matplotlib.pyplot.

2. Import Data from CSV File

The dataset is loaded from a local CSV file using pd.read_csv().
A helper function automatically detects common column names like price, sqft, date, and zip.

3. Manage Different Data Types

The script automatically:
Converts date strings into datetime objects.
Converts numeric columns (price, area, etc.) into floating-point numbers.
Casts categorical variables (like neighborhood or property type) to category dtype.

4. Data Processing

Before analysis, the dataset is cleaned and preprocessed:
Removes missing or invalid values.
Filters unrealistic data (e.g., prices ≤ 1 or area ≤ 50).
Calculates a new variable price_per_sqft.
Clip extreme outliers to improve statistical robustness.

5. Write My Own Function for Data Analysis

A custom analysis function named analyze_metric() is written to compute descriptive statistics such as:
Count, mean, median, and standard deviation
25th and 75th percentiles
Optional grouping by a categorical column (e.g., neighborhood or property type)
This function demonstrates how to encapsulate reusable analytical logic for different metrics.

6. Use My Function for Analysis

The function is called to summarize variables like price_per_sqft_clipped or price, providing quick insight into market trends and data spread.



7. Data Visualization

The distribution of key metrics (such as price per square foot) is visualized with a histogram using matplotlib.
This helps identify skewness, spread, and potential outliers in property prices.
