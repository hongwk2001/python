data = [
    ['TAIL NO', 'IN DATE', 'OUT DATE', 'DESCRIPTION'],
    ['133CZ', '1/5/2017', '1/7/2017', '100 hour inspection'],
    ['134CZ', '3/24/2017', '3/27/2017', '100 hour inspection'],
    ['134CZ', '4/16/2017', '4/19/2017', 'annual inspection'],
    ['131CZ', '1/28/2017', '1/30/2017', '100 hour inspection'],
    ['135CZ', '2/17/2017', '2/19/2017', '100 hour inspection'],
    ['133CZ', '3/4/2017', '3/7/2017', '100 hour inspection'],
    ['135CZ', '4/19/2017', '4/22/2017', 'minor repair'],
    ['136CZ', '5/4/2017', '5/7/2017', '100 hour inspection']
]

keys = data[0]  # Get the first row as keys

dict_list = {}
for row in data[1:]:
    #dictionary = dict(zip(keys, row))
    tail_no = row[0]
    if tail_no not in dict_list:
        dict_list[tail_no] = []
    dict_list[tail_no].append(row)

print('all',dict_list)
print(dict_list['136CZ'])


# each will whole list per plane
for key, value in dict_list.items() :
    print(value, type(value))
    new_list = sorted(value, key=lambda x:x[1])
    dict_list[key] = new_list

print (dict_list)