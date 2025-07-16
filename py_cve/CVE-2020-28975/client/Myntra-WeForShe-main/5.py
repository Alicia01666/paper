import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.seasonal import seasonal_decompose

# Load the data
df = pd.read_excel('scraped_data.xlsx')

# Clean the data
def clean_price_column(df, column_name):
    if column_name in df.columns:
        df[column_name] = df[column_name].replace('[\₹,Rs.\s]', '', regex=True).astype(float)
    else:
        print(f"Error: '{column_name}' column not found in the dataset.")
        exit()

clean_price_column(df, 'Current Price')
clean_price_column(df, 'Original Price')

df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

# Generate synthetic date data for demonstration
df['Date'] = pd.date_range(start='2023-01-01', periods=len(df), freq='D')  # Daily frequency starting from Jan 1, 2023

# Set 'Date' column as index for time series analysis
df.set_index('Date', inplace=True)

# Descriptive Statistics
print(df.describe())

# Visualization: Price Trend Over Time
plt.figure(figsize=(14, 7))
plt.plot(df.index, df['Current Price'], label='Current Price', color='b')
plt.title('Price Trend Over Time')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

# Time Series Decomposition
decomposition = seasonal_decompose(df['Current Price'], model='multiplicative', period=7)

# Plot the decomposed components
plt.figure(figsize=(14, 10))
plt.subplot(411)
plt.plot(decomposition.observed, label='Observed')
plt.legend(loc='upper left')
plt.subplot(412)
plt.plot(decomposition.trend, label='Trend')
plt.legend(loc='upper left')
plt.subplot(413)
plt.plot(decomposition.seasonal, label='Seasonality')
plt.legend(loc='upper left')
plt.subplot(414)
plt.plot(decomposition.resid, label='Residuals')
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()

# Correlation Analysis
numeric_df = df[['Current Price', 'Original Price']]
corr_matrix = numeric_df.corr()
plt.figure(figsize=(10, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Predictive Modeling
X = df[['Original Price']]
y = df['Current Price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, predictions)
print(f'Mean Squared Error: {mse}')

# Save cleaned data to a new Excel file
df.reset_index(inplace=True)  # Reset index to save date as a column again
df.to_excel('cleaned_data_with_time_series.xlsx', index=False)

print("Data cleaning, analysis, and saving completed.")

