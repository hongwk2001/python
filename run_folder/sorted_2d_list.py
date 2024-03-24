# Create a 2D list
list_2d = [[3, 4], [1, 2], [5, 6]]

# Sort the list by the first element in each row
sorted_list_2d = sorted(list_2d, key=lambda x: x[0])

# Print the sorted list
print(sorted_list_2d)