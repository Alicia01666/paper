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

# Initial data check
print(f"Initial data size: {df.shape}")

# Clean the data
if 'Current Price' in df.columns:
    df['Current Price'] = df['Current Price'].replace('[\₹,Rs.\s]', '', regex=True).astype(float)
else:
    print("Error: 'Current Price' column not found in the dataset.")
    exit()

if 'Original Price' in df.columns:
    df['Original Price'] = df['Original Price'].replace('[\₹,Rs.\s]', '', regex=True).astype(float)

# Check for missing values before dropping
missing_values = df.isnull().sum()
print(f"Missing values before cleaning:\n{missing_values}")

# Remove any rows with missing values and duplicates
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

# Check data size after cleaning
print(f"Data size after cleaning: {df.shape}")

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
# Selecting only numeric columns for correlation analysis
numeric_columns = ['Current Price', 'Original Price']
numeric_df = df[numeric_columns].dropna()  # Drop any rows with missing numeric values
corr_matrix = numeric_df.corr()
plt.figure(figsize=(10, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Predictive Modeling (Optional)
# For demonstration, using 'Original Price' as a feature if it exists
features = []
if 'Original Price' in df.columns:
    features.append('Original Price')

if features:
    X = df[features]
    y = df['Current Price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, predictions)
    print(f'Mean Squared Error: {mse}')
else:
    print("Not enough numeric features for predictive modeling.")

# Save cleaned data to a new Excel file
df.to_excel('cleaned_data.xlsx', index=False)

print("Data cleaning, analysis, and saving completed.")
