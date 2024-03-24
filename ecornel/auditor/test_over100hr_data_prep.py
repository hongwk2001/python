# See: https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time
import json
import utils
import inspections
import os

def strtime_to_isoformat(str):
    return utils.str_to_time(str, "America/New_York").isoformat()

def over100hr_data_prep(lessons, repairs):
    """
    As a hint, we recommend creating a dictionary to track the hours flown for each plane.
    Then combine the lessons and repairs together and sort them by date.
 {“133sz”:[[repair, 2017,2017 ], [lesson, 2017, 2018], [lesson,2017, 2017]],
  “122XF”:[[lesson, 2017,2017 ], [repair, 2017, 2018], [lesson,2017, 2017]],
    lessons, repairs not sorted, different columns
    """
    #
    # AIRPLANE	TAKEOFF	                    LANDING
    # 133CZ	    2017-01-02T09:00:00-05:00	2017-01-02T11:00:00-05:00
    # 134CZ	    2017-01-02T09:00:00-05:00	2017-01-02T11:00:00-05:00

    lessons.pop(0)
    lesson1 = []
    for row in lessons:
        nrow = [row[1], 'Lesson', strtime_to_isoformat(row[3]), strtime_to_isoformat(row[4])]
        lesson1.append(nrow)

    # now  yet mixed order
    # 133CZ	Lesson   2017-01-02T09:00:00-05:00	2017-01-02T11:00:00-05:00
    # 134CZ	Lesson   2017-01-02T09:00:00-05:00	2017-01-02T11:00:00-05:00
    # 133CZ	Lesson   2017-01-02T09:00:00-05:00	2017-01-02T11:00:00-05:00

    repairs.pop(0)
    repairs1 = []
    for row in repairs:
        nrow = [row[0], 'Repair', strtime_to_isoformat(row[1]), strtime_to_isoformat(row[2])]
        repairs1.append(nrow)
    """
    133CZ Repair  str1/5/2017	1/7/2017
    133CZ Repair  str1/28/2017	1/30/2017
    """
    # combine list
    combined_list = lesson1 + repairs1

    # sort list by plane , yet know only one column sort
    sorted_cbnd_list = sorted(combined_list, key=lambda x: x[0])

    # New dic with Plane as key
    # add lists
    dict_list = {}
    for row in sorted_cbnd_list:
        tail_no = row[0]
        if tail_no not in dict_list:
            dict_list[tail_no] = []
        dict_list[tail_no].append(row)

    #print('dict_list 100:', str(dict_list)[:100])

    # sort list inside by Takeoff:In_time ?  or landing:out_time ?
    # should be mutually exclusive but is it?
    # each will whole list per plane
    for key, value in dict_list.items():

        # sort tail_no, Lesson/Repair, from_date
        list1 = sorted(value, key=lambda x: x[2])

        # remove Tail_no in the list itself
        list2 = []
        for row in list1:
            list2.append(row[1:])

        # finally replace the list in dict
        dict_list[key] = list2

    """
    for key, value in dict_list.items():
        print('key----------------', key)
        print('value==============', value) """

    return dict_list

#current dir
parent = os.path.split(__file__)[0]

# Load in all the files
lessons = utils.read_csv(os.path.join(parent, 'tests/test_lessons.csv'))
repairs = utils.read_csv(os.path.join(parent, 'tests/test_repairs.csv'))

#test_dict_over100hr_src = inspections.over100hr_data_prep(lessons, repairs)

test_dict_over100hr_src = over100hr_data_prep(lessons, repairs)

print(test_dict_over100hr_src)

# Save the dictionary to JSON
with open("test_dict_over100hr_src.json", "w") as outfile:
    json.dump(test_dict_over100hr_src, outfile)