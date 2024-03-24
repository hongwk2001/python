import pandas as pd

# Create a sample CSV file
with open('data.csv', 'w') as file:
    file.write('name,age,country\n')
    file.write('Alice,25,USA\n')
    file.write('Bob,30,Canada\n')
    file.write('Charlie,35,Australia\n')
    file.write('David,40,USA\n')
    file.write('Eva,45,Canada\n')

# Read the CSV file and use the first row as column names
df = pd.read_csv('data.csv', header=0)

print(df.name)

# Print the DataFrame
print(df)