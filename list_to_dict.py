import pickle

def save_dictionary_to_file(dictionary, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(dictionary, file)

# Example dictionary
my_dictionary = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}

# Saving the dictionary to a file
save_dictionary_to_file(my_dictionary, 'dictionary.pickle')