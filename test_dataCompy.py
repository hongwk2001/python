import pandas as pd
from datacompy import Compare

# Create two sample DataFrames
df1 = pd.DataFrame({'ID': [1, 2, 3], 'Name': ['John', 'Alice', 'Bob']})
df2 = pd.DataFrame({'ID': [1, 2, 4], 'Name': ['John', 'Alice', 'Charlie']})

# Perform the comparison
compare = Compare(df1, df2, join_columns='ID')
result = compare.report()

# Print the comparison report
print(result)