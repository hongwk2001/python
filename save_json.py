import json

# Dictionary to be saved
data = {
    'name': 'John Doe',
    'age': 30,
    'city': 'New York'
}

# Path to the JSON file
file_path = 'data.json'

# Save the dictionary to JSON
with open(file_path, 'w') as json_file:
    json.dump(data, json_file)