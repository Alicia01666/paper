import pandas as pd

# Function to convert Excel file to CSV
def convert_excel_to_csv(excel_file, csv_file):
    # Read the Excel file
    df = pd.read_excel(excel_file)
    # Save the dataframe to a CSV file
    df.to_csv(csv_file, index=False)
    print(f"Excel file '{excel_file}' has been converted to CSV file '{csv_file}'.")

# Convert 'cleaned_data.xlsx' to 'cleaned_data.csv'
convert_excel_to_csv('cleaned_data.xlsx', 'cleaned_data.csv')

# Convert 'scraped_data.xlsx' to 'scraped_data.csv'
convert_excel_to_csv('scraped_data.xlsx', 'scraped_data.csv')
