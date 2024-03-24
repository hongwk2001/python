import pandas as pd

# Sample dataframes with same column names
df1 = pd.DataFrame({'join_column': [1, 2, 3],
                    'col1': ['A', 'B', 'C'],
                    'col2': ['1', '2', '3']})

df2 = pd.DataFrame({'join_column': [2, 3, 4],
                    'col1': ['B', 'Y', 'Z'],
                    'col2': ['2', None, '']})

# Perform outer join on the join_column and specify suffixes for overlapping columns
merged_df = pd.merge(df1, df2, on='join_column', how='outer', suffixes=('_df1', '_df2'))

# Create new columns for comparing values between the two dataframes
len_df = len(df1.columns) - 1
for i in range(1, len_df + 1):
    new_col_name = f'{df1.columns[i]}_Match'
    merged_df[new_col_name] = merged_df.iloc[:, i] == merged_df.iloc[:, i + len_df]

# Select desired columns from the merged dataframe
merged_df1 = merged_df.iloc[:, [0] + list(range(2 * len_df + 1, len(merged_df.columns)))].copy()

merged_df1.reset_index(inplace=True)
print(len(merged_df1), merged_df1)