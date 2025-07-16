import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load the data
df = pd.read_excel('scraped_data.xlsx')

# Check the column names
print("Columns in the dataset:", df.columns)

# Clean the data
if 'Current Price' in df.columns and 'Original Price' in df.columns:
    df['Current Price'] = df['Current Price'].replace('[\₹,Rs.\s]', '', regex=True).astype(float)
    df['Original Price'] = df['Original Price'].replace('[\₹,Rs.\s]', '', regex=True).astype(float)
else:
    print("Error: 'Current Price' or 'Original Price' column not found in the dataset.")
    exit()

# Remove rows with missing values and duplicates
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

# Transform the data
df['discount_percentage'] = (df['Original Price'] - df['Current Price']) / df['Original Price'] * 100
df['price_difference'] = df['Original Price'] - df['Current Price']

# Placeholder for date transformation if date column is available
df['date'] = pd.to_datetime('2023-01-01')  # Placeholder date, you need to update this accordingly
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

# Descriptive Statistics
print(df.describe())

# Visualization: Price Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['Current Price'], bins=30)
plt.title('Distribution of Current Prices')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()

# Correlation Analysis
numeric_df = df[['Current Price', 'Original Price', 'discount_percentage', 'price_difference']]
corr_matrix = numeric_df.corr()
plt.figure(figsize=(10, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Predictive Modeling
features = ['Original Price', 'discount_percentage']
X = df[features]
y = df['Current Price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, predictions)
print(f'Mean Squared Error: {mse}')

# Save cleaned and transformed data to a new Excel file
df.to_excel('transformed_data.xlsx', index=False)

print("Data transformation, analysis, and saving completed.")

