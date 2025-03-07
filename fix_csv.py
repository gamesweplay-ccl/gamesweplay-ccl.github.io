import pandas as pd

# Read the CSV file
df = pd.read_csv('gamesweplay.csv')

# Select and clean the required columns
df = df[['Game Name', 'Game Format', 'Minimum Age', 'Number of Players']]

# Clean up any whitespace
for col in df.columns:
    df[col] = df[col].str.strip()

# Write the cleaned data back to CSV
df.to_csv('gamesweplay.csv', index=False)
