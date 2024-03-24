
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

print(merged_df)

len_merged_df = len(merged_df.columns)
len_df= len(df1.columns) -1  # value lenth only

for i in range(1, len_df + 1):  # loops 1~
    # Apply the comparison function to each row and create a new column
    newColNm = f'{df1.columns[i]}_Match'
    merged_df[newColNm] = merged_df.apply(lambda row: row.iloc[i] == row.iloc[i + len_df], axis=1)


print(len(merged_df), merged_df)

#pick only
merged_df1=pd.DataFrame()
idx = 0
for col, series in merged_df.items() :
    # print ("key" , key )
    if idx == 0:
        merged_df1[col] = merged_df[col]

    if idx >= 2 * len_df + 1:
        merged_df1[col] = merged_df[col]

    idx += 1

#why above took 30 min ?

merged_df1.reset_index()
print(len(merged_df1), merged_df1)
