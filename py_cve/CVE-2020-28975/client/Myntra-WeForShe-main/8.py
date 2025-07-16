import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error

# Load the cleaned data
df = pd.read_excel('cleaned_data.xlsx')

# Placeholder for date transformation if date column is available
df['date'] = pd.to_datetime('2023-01-01')  # Placeholder date, you need to update this accordingly
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

# Time series analysis
# Convert the date column to datetime format and set as index
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Set the frequency of the datetime index explicitly
df.index = pd.date_range(start=df.index[0], periods=len(df), freq='D')

# Plot the price trend over time
plt.figure(figsize=(14, 7))
plt.plot(df.index, df['Current Price'], label='Current Price', color='b')
plt.title('Price Trend Over Time')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

# Decompose the time series with a period of 7 days
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

# Split data into training and testing sets
train_size = int(len(df) * 0.8)
train, test = df['Current Price'][:train_size], df['Current Price'][train_size:]

# Fit the ARIMA model
model = ARIMA(train, order=(5, 1, 0))
model_fit = model.fit()
print(model_fit.summary())

# Forecast
forecast = model_fit.forecast(steps=len(test))

# Create a datetime index for the forecasted values
forecast_index = pd.date_range(start=df.index[train_size], periods=len(test), freq='D')

# Plot the results
plt.figure(figsize=(14, 7))
plt.plot(train.index, train, label='Training Data')
plt.plot(test.index, test, label='Actual Prices')
plt.plot(forecast_index, forecast, label='Forecasted Prices', color='r')
plt.title('ARIMA Forecast')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

# Calculate mean squared error
mse = mean_squared_error(test, forecast)
print(f"Mean Squared Error: {mse}")

# Derive insights and recommendations
if decomposition.trend.mean() > 0:
    print("There is an upward trend in prices. Consider adjusting pricing strategies.")
else:
    print("Prices show no significant trend. Focus on optimizing inventory management.")

# Check if the last forecasted price is higher than the first using `iloc`
if forecast.iloc[-1] > forecast.iloc[0]:
    print("Forecasted prices are increasing. Plan promotional campaigns to capitalize on this trend.")
else:
    print("Forecasted prices are stable or decreasing. Consider maintaining current pricing strategies.")

# Save insights to a report or log file
with open('analysis_insights.txt', 'w') as file:
    file.write(f"Mean Squared Error: {mse}\n")
    file.write(f"Trend Analysis: {decomposition.trend.mean()}\n")
    file.write(f"Forecast: {forecast.iloc[-1]}\n")

print("Data interpretation and insights completed.")

# Define features and target variable for machine learning models
X = df[['year', 'month']]
y = df['Current Price']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize models
models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(),
    'Gradient Boosting': GradientBoostingRegressor(),
    'XGBoost': XGBRegressor()
}

# Train and evaluate models
for name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"{name} Mean Squared Error: {mse}")

# Hyperparameter Tuning for Random Forest
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, 30],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(estimator=RandomForestRegressor(), param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

print(f"Best parameters: {grid_search.best_params_}")

best_rf_model = grid_search.best_estimator_
rf_predictions = best_rf_model.predict(X_test)
mse = mean_squared_error(y_test, rf_predictions)
print(f"Random Forest Best Model Mean Squared Error: {mse}")

# Cross-Validation for the best model
rf_model = RandomForestRegressor(n_estimators=grid_search.best_params_['n_estimators'],
                                 max_depth=grid_search.best_params_['max_depth'],
                                 min_samples_split=grid_search.best_params_['min_samples_split'])
cv_scores = cross_val_score(rf_model, X, y, cv=5, scoring='neg_mean_squared_error')
cv_scores = -cv_scores  # convert to positive MSE scores

print(f"Cross-Validation Scores: {cv_scores}")
print(f"Mean CV Score: {cv_scores.mean()}")

