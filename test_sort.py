import os

print(os.path.split(__file__))

dict_list =\
    {"plane":[["Lesson", "2017-01-03T11:00:00-05:00"],
            ["Lesson", "2017-12-30T13:00:00-05:00"],
            ["Repair", "2017-01-15T00:00:00-05:00"]]}

for key, value in dict_list.items():
    # sort
    list1 = sorted(value, key=lambda x: x[1])

    list2 = []
    for row in list1:
         list2.append(row[1:])
     # finally replace the list in dict
    dict_list[key] = list2



print(dict_list)