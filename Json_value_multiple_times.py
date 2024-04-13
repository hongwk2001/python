import json

def search_json(data, key):
  """
  Searches for a key in a JSON structure and returns all corresponding values.
  """
  results = []
  if isinstance(data, dict):
    for k, v in data.items():
      if k == key:
        results.append(v)
      results.extend(search_json(v, key))  # Recursively search nested structures
  elif isinstance(data, list):
    for item in data:
      results.extend(search_json(item, key))
  return results

# Example usage
json_data = '''{
  "name": "Shopping List",
  "items": [
    "Milk",
    "Bread",
    "Eggs",
    {
      "name": "Fruits",
      "subitems": ["Apples", "Bananas", "Oranges"]
    },
    {
      "name": null,
      "items": ["letters", "tomato", "radish"]
    }
  ]
}'''

data = json.loads(json_data)
key_to_find = "name"
all_values = search_json(data, key_to_find)
print(all_values)  # Output: ["tennis"]

key_to_find = "items"
all_values = search_json(data, key_to_find)
print(all_values)  # Output: ["tennis"]