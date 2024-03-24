import pandas as pd
import csv

# Open the CSV file
csv_file_path = "data.csv"

# Read the CSV file into a pandas DataFrame
data = pd.read_csv(csv_file_path)

for index, row in data.iterrows():
    print(row['join_cols'], type(row['join_cols']))
    print(list(row['join_cols']))

