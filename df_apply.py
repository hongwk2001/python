import pandas as pd

# Define a function that takes a row as input and returns the sum of the 'a' and 'b' columns
def sum_a_b(row):
    print(row)
    return row['a'] + row['b']

# Create a sample DataFrame
data = {'a': [1, 2, 3, 4],
        'b': [5, 6, 7, 8]}
df = pd.DataFrame(data)

# Apply the sum_a_b function to each row of the DataFrame
#df['sum'] = df.apply(sum_a_b, axis=1)

df['sum1']=df.apply(lambda row: row.a + row.b , axis = 1)

# Print the DataFrame with the new 'sum' column
print(df)