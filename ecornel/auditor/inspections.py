"""
Module to check inspection violations for a flight lesson (OPTIONAL)

There are three kinds of inspection violations. (1) A plane has gone more than
a year since its annual inspection. (2) A plane has accrued 100 hours of flight
time since its last regular inspection. (3) A plane is used for a lesson despite
the repair logs claiming that it is in the shop for maintenance.

This module is MUCH more difficult than the others.  In the other modules, we
provided specifications for all of the helper functions, to make the main
function (listing all violations) easier.  We do not do that at all here.
You have one specification for one function.  Any additional functions (which
we do recommend) are up to you.

The other tricky part is keeping track of the hours since the last inspection
for each plane.  It is possible to do this with a nested loop, but the result
will be very slow (the application will take several minutes to complete).
To speed it up, you have to figure out how to "interleave" lessons with repairs.
This is a very advanced programming problem.

To implement this module, you need to familiarize yourself with two files
beyond what you have used already.

First of all, recall that fleet.csv is a CSV file with the following header:

    TAILNO  TYPE  CAPABILITY  ADVANCED  MULTIENGINE ANNUAL  HOURS

This lists the planes at the flight school.  For this module you need the
last two columns, which are strings representing a date and an number,
respectively.  The date is the last annual inspection for that plane as of
the beginning of the year (e.g. the start of the audit).  The number is
the number of hours since the last 100 hour inspection.

In addition, repairs.csv is a CSV file with the following header:

    TAILNO  IN-DATE  OUT-DATE  DESCRIPTION

The first column is the string identifying the plane.  The next two columns are
strings representing dates, for when the plane enters and leaves the shop (so
it should not fly during this time).  The last column is the type of repair.
A plane must be inspected/repaired every 100 hours.  In addition, it must have
an annual inspection once a year.  Other repairs happen as needed.  ANY repair
resets the number of hours on the plane.

The preconditions for many of these functions are quite messy.  While this
makes writing the functions simpler (because the preconditions ensure we have
less to worry about), enforcing these preconditions can be quite hard. That is
why it is not necessary to enforce any of the preconditions in this module.

Author: YOUR NAME HERE
Date: THE DATE HERE
"""
import os.path
import datetime
import utils
import json

# FILENAMES
# Sunrise and sunset (mainly useful for timezones, since repairs do not have them)
DAYCYCLE = 'daycycle.json'
# The list of all take-offs (and landings)
LESSONS = 'lessons.csv'
# The list of all planes in the flight school
PLANES = 'fleet.csv'
# The list of all repairs made to planes over the past year
REPAIRS = 'repairs.csv'


def strtime_to_isoformat(str):
    return utils.str_to_time(str, "America/New_York").isoformat()

# (1) a plane has gone MORE than a year since its annual inspection
def is_annual_insp_violation(takeoff, plane, repairs_by_plane):
    annual = utils.str_to_time(plane[5], "America/New_York")

    for repair in repairs_by_plane :
        in_time = utils.str_to_time(repair[1], "America/New_York")

        # check up to take off, irrelevant!
        if  in_time > takeoff: break
        # get lastest annual insp
        if repair[3] =='annual inspection':
            if in_time > annual : annual = in_time

    if annual + datetime.timedelta(days=365) < takeoff :
#        print('annual violation', takeoff, plane[0], annual, )
        return True

    return False

def under_maintenance_violation(takeoff, repairs_by_plane):
    for repair in repairs_by_plane:
        in_time = utils.str_to_time(repair[1], "America/New_York")
        out_time = utils.str_to_time(repair[2], "America/New_York")
        if in_time < takeoff < out_time:
            return True
    return False


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


# (2) a plane has accrued OVER 100 hours of flight time
# since its last repair or inspection
# over100hr_data list by plane 
def over100hours_violation(takeoff, plane, over100hr_data):
    """ When you loop through the combined list, 
    you increment the hours if the next element is a lesson flight and 
    reset hours to 0 if it is a repair. 
    [   [Repair, 2017,2017 ], 
        [Lesson, 2017, 2018], 
        [Lesson,2017, 2017]]  ]
        takeoff : time newyork 
    """

    """For example, if fleet.csv claims that Cessna 133CZ starts with 88 hours, 
    then there should only be 12 hours’ worth of lessons 
    before the next inspection in repairs.csv"""
    annual = utils.str_to_time(plane[5], "America/New_York")
    # get hours from plane first after annual
    hours = datetime.timedelta(hours=int(plane[6]))

    flight_time_after_repair = datetime.timedelta(hours=0)

    # add valid time
    for row in over100hr_data:
        from_dt = utils.str_to_time(row[1], "America/New_York")
        to_dt = utils.str_to_time(row[2], "America/New_York")
        assert isinstance(from_dt, datetime.datetime)
        assert isinstance(to_dt, datetime.datetime)

        repair_end_dt = None

        #if plane[0] == '684TM' and takeoff == utils.str_to_time('2017-02-26T14:00:00-05:00', "America/New_York"):
        #    print(plane[0],takeoff, row, ' flight time :' , flight_time_after_repair.total_seconds() / 3600 )

        # no more counts
        if from_dt > takeoff :
            break

        # reset if Repair  billy and  begin date changes.
        if row[0] == 'Repair':
            flight_time_after_repair = datetime.timedelta(hours=0)
            repair_end_dt = utils.str_to_time(row[2] ,"America/New_York")
            continue

        # Not count before annual
        try:
            if from_dt < annual or (repair_end_dt is not None and to_dt <= repair_end_dt):
                continue
        except TypeError:
            print ('from_dt:', from_dt, ' annual:', annual, ' plane[5]', plane[5] , ' repair end dt:',repair_end_dt )
            raise

        # add Flight time
        assert isinstance(to_dt - from_dt, datetime.timedelta)
        time_delta = (to_dt - from_dt)
        flight_time_after_repair =  datetime.timedelta(hours=(flight_time_after_repair.total_seconds()/3600 + time_delta.total_seconds()/3600))
        assert isinstance(flight_time_after_repair, datetime.timedelta)

        #if plane[0] == '684TM' and takeoff == utils.str_to_time('2017-02-26T14:00:00-05:00', "America/New_York"):
        #    print(plane[0],takeoff, row, ' delta:', time_delta , ' flight time :' , flight_time_after_repair.total_seconds() / 3600 )

    #if takeoff == utils.str_to_time('2017-02-26T14:00:00-05:00')  and plane[5] == '684TM':
    #if plane[0] == '684TM' and takeoff < utils.str_to_time('2017-03-01', "America/New_York"):
    #    print(plane[0],  takeoff, ' flight time :' , flight_time_after_repair.seconds / 3600 )

    return flight_time_after_repair > datetime.timedelta(hours=100)


def repairs_2_dict(repairs):

    repairs.pop(0)
    repairs1 = []
    for row in repairs:
        new_r = [row[0], 'Repair', strtime_to_isoformat(row[1]), strtime_to_isoformat(row[2])]
        repairs1.append(new_r)

    # New dic with Plane as key
    # add lists
    dict_list = {}
    for row in repairs:
        tail_no = row[0]
        if tail_no not in dict_list:
            dict_list[tail_no] = []
        dict_list[tail_no].append(row)

    return dict_list


# (3) a plane is used for a lesson despite the repair logs
# claiming that it is in the shop for maintenance.
# gets dict  param takeoff time newyork
def under_maintenance_violation(takeoff, repairs_by_plane):
    for repair in repairs_by_plane:
        in_time = utils.str_to_time(repair[1], "America/New_York")
        out_time = utils.str_to_time(repair[2], "America/New_York")
        if in_time < takeoff < out_time:
            return True
    return False


def get_name_of_violation(annual_vio, over100_vio, under_main_vio):

    name_of_violation = ''
    cnt = 0

    if annual_vio :
        name_of_violation = 'Annual'
        cnt +=1
    if over100_vio :
        name_of_violation = 'Inspection'
        cnt +=1
    if under_main_vio :
        name_of_violation = 'Grounded'
        cnt +=1

    # multiple problems should be remained
    if cnt > 1: name_of_violation = 'Maintenance'
    return name_of_violation

def list_inspection_violations(directory):
    """
    Returns the (annotated) list of flight lessons that violate inspection
    or repair requirements.
    
    This function reads the data files in the given directory (the data files
    are all identified by the constants defined above in this module).  It loops
    through the list of flight lessons (in lessons.csv), identifying those
    takeoffs for which (1) a plane has gone MORE than a year since its annual
    inspection, (2) a plane has accrued OVER 100 hours of flight time since its
    last repair or inspection, and (3) a plane is used for a lesson despite
    the repair logs claiming that it is in the shop for maintenance.
    
    Note that a plane landing with exactly 100 hours used is not a violation.
    Nor is a plane that has flown with 365 days since its last inspection. This
    school likes to cut things close to safe money, but these are technically
    not violations.
    
    This function returns a list that contains a copy of each violating lesson,
    together with the violation appended to the lesson.  Violation of type (1)
    is annotated 'Annual'.  Violation of type (2) is annotated 'Inspection'.
    Violations of type (3) is annotated 'Grounded'.  If more than one is
    violated, it should be annotated 'Maintenance'.
    
    Example: Suppose that the lessons
    
        S00898  811AX  I072  2017-01-27T13:00:00-05:00  2017-01-27T15:00:00-05:00  VFR  Pattern
        S00681  684TM  I072  2017-02-26T14:00:00-05:00  2017-02-26T17:00:00-05:00  VFR  Practice Area
        S01031  738GG  I010  2017-03-19T13:00:00-04:00  2017-03-19T15:00:00-04:00  VFR  Pattern
    
    violate for reasons of 'Annual', 'Inspection', and 'Grounded', respectively
    (and are the only violations).  Then this function will return the 2d list
    
        [['S00898', '811AX', 'I072', '2017-01-27T13:00:00-05:00', '2017-01-27T15:00:00-05:00', 'VFR', 'Pattern', 'Annual'],
         ['S00681', '684TM', 'I072', '2017-02-26T14:00:00-05:00', '2017-02-26T17:00:00-05:00', 'VFR', 'Practice Area', 'Inspection'],
         ['S01031', '738GG', 'I010', '2017-03-19T13:00:00-04:00', '2017-03-19T15:00:00-04:00', 'VFR', 'Pattern', 'Grounded']]
    
    Parameter directory: The directory of files to audit
    Precondition: directory is the name of a directory containing the files
    'daycycle.json', 'fleet.csv', 'repairs.csv' and 'lessons.csv'
    """

    # Load in all the files
    lessons = utils.read_csv(os.path.join(directory, 'lessons.csv'))
    repairs = utils.read_csv(os.path.join(directory, 'repairs.csv'))
    fleet = utils.read_csv(os.path.join(directory, 'fleet.csv'))

    dict_over100hr_src = over100hr_data_prep(lessons, repairs)
    # Save the dictionary to JSON
    with open("dict_over100hr_src.json", "w") as outfile:
        json.dump(dict_over100hr_src, outfile)

    repair_dict = repairs_2_dict(repairs)
    # Save the dictionary to JSON
    with open("repair_dict.json", "w") as outfile:
        json.dump(repair_dict, outfile)

    list_violation = []
    list_violation_debug =[]
    # For each of the lessons
    # It loops through the list of flight lessons (in lessons.csv),
    lessons.pop(0)
    for lesson in lessons:
        # Get the takeoff time
        takeoff = utils.str_to_time(lesson[3], "America/New_York")
        plane = utils.get_for_id(lesson[1], fleet)

        # (1) a plane has gone MORE than a year since its annual inspection, is that all?
        annual_vio = True if is_annual_insp_violation(takeoff, plane, repair_dict[lesson[1]]) else False
        # (2) a plane has accrued OVER 100 hours of flight time
        # since its last repair or inspection
        over100_vio = True if over100hours_violation(takeoff, plane, dict_over100hr_src[lesson[1]]) else False
        # (3) a plane is used for a lesson despite the repair logs
        # claiming that it is in the shop for maintenance.
        under_main_vio = True if under_maintenance_violation(takeoff, repair_dict[lesson[1]]) else False

        #if lesson[0] == 'S00930' and lesson[1] == '811AX' :
        #    print ( lesson, 'ann', annual_vio, ' over100', over100_vio, ' under' , under_main_vio)

        name_of_violation = get_name_of_violation(annual_vio, over100_vio, under_main_vio)

        if name_of_violation > '':
            list_violation_debug.append(lesson + [annual_vio,over100_vio,under_main_vio])

            lesson.append(name_of_violation)
            list_violation.append(lesson)

    utils.write_csv(list_violation, 'list_violation.csv')
    utils.write_csv(list_violation_debug, 'list_violation_debug.csv')

    return list_violation


def save_list_insp_violation() :
    directory  = './tests'
    list_insp_vltn, list_violation_debug = list_inspection_violations(directory)

    output = 'list_violation_debug.csv'
    if output is not None and len(list_violation_debug) > 0 :
        list_violation_debug.insert(0, ['STUDENT', 'AIRPLANE', 'INSTRUCTOR', 'TAKEOFF', 'LANDING', 'FILED', 'AREA', 'ANN', 'OVer100', 'Main' ])
        utils.write_csv(list_violation_debug, output)

if __name__ == '__main__' :
    save_list_insp_violation()