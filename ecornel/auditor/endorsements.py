"""
Module to check endorsement violations for a flight lesson (OPTIONAL)

There are three kinds of endorsement violations. (1) A student has not soloed
but flies without an instructor.  (2) A student flies a plane that he or she
has no endorsement for. (3) A student files an invalid IFR flight (which could
be for several reasons).

This module is actually no more difficult than violations.py (and can be quite
easy if you have finished that already).  This material was cut to make the
project shorter.  To implement this module, you need to familiarize yourself
with two files beyond what you have used already.

First, instructors.csv is a CSV file with the following header:

    ID  LASTNAME  FIRSTNAME  CFI  CFII  MEI

This lists the instructors in the flight school. The first three columns are
general strings, while the last three columns are Yes/No strings. They indicate
whether the instructor can teach a student on a VFR flight, whether the
instructor can teach a student on an IFR flight, and whether the instructor
can teach a student on a multiengine flight.

Next, fleet.csv is a CSV file with the following header:

    TAILNO  TYPE  CAPABILITY  ADVANCED  MULTIENGINE ANNUAL  HOURS

This lists the planes at the flight school.  The first three columns are
general strings.  The third column is one of the strings VFR/IFR, indicating
if the plane is outfitted for instrument flight.  The fourth and fifth columns
are Yes/No strings indicating the endorsments required for this plane.  The
last two columns may be ignored for this module.

The preconditions for many of these functions are quite messy.  While this
makes writing the functions simpler (because the preconditions ensure we have
less to worry about), enforcing these preconditions can be quite hard. That is
why it is not necessary to enforce any of the preconditions in this module.

Author: Billy Wookyoung Hong
Date: May 2023
"""
import pilots
import utils
import os.path
import datetime


def teaches_multiengine(instructor):
    """
    Returns True if this instructor can teach a student on a multiengine flight.
    False otherwise.
    
    Parameter instructor: The flight instructor
    Precondition: instructor is a 6-element list of strings representing an instructor
    """
    return True if instructor[5] == 'Yes' else False

def teaches_instrument(instructor):
    """
    Returns True if this instructor can teach a student on an IFR flight.
    False otherwise.
    
    Parameter instructor: The flight instructor
    Precondition: instructor is a 6-element list of strings representing an instructor
    """
    return True if instructor[4] == 'Yes' else False

def is_advanced(plane):
    """
    Returns True if the plane requires an advanced endorsement; False otherwise.
    
    Parameter plane: The school airplane
    Precondition: plane is a 7-element list of strings representing an airplane
    """
    return True if plane[3] == 'Yes' else False

def is_multiengine(plane):
    """
    Returns True if the plane requires a multiengine endorsement; False otherwise.
    
    Parameter plane: The school airplane
    Precondition: plane is a 7-element list of strings representing an airplane
    """
    return True if plane[4] == 'Yes' else False


def is_ifr_capable(plane):
    """
    Returns True if the plane is outfitted for IFR flight; False otherwise.
    
    NOTE: Just because a plane is IFR capable, does not mean that every flight
    with it is an IFR flight.
    
    Parameter plane: The school airplane
    Precondition: plane is a 7-element list of strings representing an airplane
    """
    return True if plane[2] == 'IFR' else False


def bad_endorsement(takeoff,student,instructor,plane):
    """
    Returns True if the student or instructor did not have the right endorsement.
    
    The endorsement depends on the plane type (advanced, multiengine).  All
    instructors are certified for advanced planes, so a flight with an instructor
    is only a problem if the plane is multiengine and the instructor does not
    have an MEI.
    
    If there is no instructor, the student must be endorsed for this type of
    plane before the time of takeoff.
    
    Parameter takeoff: The takeoff time of this flight
    Precondition: takeoff is a datetime object
    
    Parameter student: The student pilot
    Precondition: student is 10-element list of strings representing a pilot
    
    Parameter instructor: The flight instructor
    Precondition: instructor is a 6-element list of strings representing an instructor
    
    Parameter plane: The school airplane
    Precondition: plane is a 7-element list of strings representing an airplane
    """
    if is_multiengine(plane) :
        if instructor is not None and teaches_multiengine(instructor) : 
            return False
        elif pilots.has_multiengine_endorsement(takeoff,student): 
            return False
        else :
            return True

    # find good cases?
    if is_advanced(plane): 
        if instructor is not None:
            return False
        elif pilots.has_advanced_endorsement(takeoff,student):
            return False
        else:
            return True

    return False


def bad_ifr(takeoff,student,instructor,plane):
    """
    Returns True if the student, instructor, or plane is not certified for IFR.
    
    For an IFR flight to be valid, the plane must be outfitted for IFR.  If there
    is an instructor, that instructor must have a CFII. If the student is alone,
    the student must have an instrument rating at the time of takeoff.
    
    NOTE: The precondition for takeoff does not assume anything about the flight. 
    It may be a VFR flight not subject to IFR rules.  This function should still
    return False if that flight COULD have been a successful IFR flight.
    
    Parameter takeoff: The takeoff time of this flight
    Precondition: takeoff is a datetime object
    
    Parameter student: The student pilot
    Precondition: student is 10-element list of strings representing a pilot
    
    Parameter instructor: The flight instructor
    Precondition: instructor is a 6-element list of strings representing an instructor
    
    Parameter plane: The school airplane
    Precondition: plane is a 7-element list of strings representing an airplane
    """
   
    if not is_ifr_capable(plane): return True
    if instructor is not None and teaches_instrument(instructor): return False
    if instructor is None and  pilots.has_instrument_rating(takeoff,student): return False

    return True

# FILENAMES
# Sunrise and sunset (mainly useful for timezones, since repairs do not have them)
DAYCYCLE = 'daycycle.json'
# The list of all take-offs (and landings)
LESSONS  = 'lessons.csv'
# The list of all registered students in the flight school
STUDENTS = 'students.csv'
# The list of all certified instructors in the flight school
TEACHERS = 'instructors.csv'
# The list of all planes in the flight school
PLANES   = 'fleet.csv'
# The list of all repairs made to planes over the past year
REPAIRS  = 'repairs.csv'


def list_endorsement_violations(directory):
    """
    Returns the (annotated) list of flight lessons that violate endorsement
    or rating regulations.
    
    This function reads the data files in the given directory (the data files
    are all identified by the constants defined above in this module).  It loops
    through the list of flight lessons (in lessons.csv), identifying those
    takeoffs for which (1) a student has not soloed but flies without an instructor,
    (2) a student or instructor flies a plane that he or she has no endorsement
    for, (3) a student files an invalid IFR flight.
    
    This function returns a list that contains a copy of each violating lesson,
    together with the violation appended to the lesson.  Violation of type (1)
    is annotated 'Solo'.  Violation of type (2) is annotated 'Endorsement'.
    Violations of type (3) is annotated 'IFR'.  If more than one is violated,
    it should be annotated 'Credentials'.
    
    Example: Suppose that the lessons
    
        S00898  426JQ        2017-01-02T11:00:00-05:00  2017-01-02T13:00:00-05:00  VFR  Pattern
        S00811  811AX  I077  2017-01-07T10:00:00-05:00  2017-01-07T12:00:00-05:00  IFR	Pattern
        S00526  446BU        2017-01-16T08:00:00-05:00	2017-01-16T10:00:00-05:00  VFR	Practice Area
    
    violate for reasons of 'SOLO', 'IFR', and 'Endorsement', respectively (and
    are the only violations).  Then this function will return the 2d list
    
        [['S00898', '426JQ', '',     '2017-01-02T11:00:00-05:00', '2017-01-02T13:00:00-05:00', 'VFR', 'Pattern', 'Solo'],
         ['S00811', '811AX', 'I077', '2017-01-07T10:00:00-05:00', '2017-01-07T12:00:00-05:00', 'IFR', 'Pattern', 'IFR'],
         ['S00526', '446BU', '',     '2017-01-16T08:00:00-05:00', '2017-01-16T10:00:00-05:00', 'VFR', 'Practice Area', 'Endorsement']]
    
    Parameter directory: The directory of files to audit
    Precondition: directory is the name of a directory containing the files
    'daycycle.json', 'students.csv', 'instructors.csv', 'fleet.csv' and
    'lessons.csv'
    """
    # Load in all of the files
    lessons = utils.read_csv(os.path.join(directory,'lessons.csv'))
    students = utils.read_csv(os.path.join(directory ,'students.csv'))
    instructors = utils.read_csv(os.path.join(directory ,'instructors.csv'))
    fleet = utils.read_csv(os.path.join(directory ,'fleet.csv'))

    list_violation= []
    # For each of the lessons
    lessons.pop(0)
    for lesson in lessons :
        # Check if the student is allowed to fly by themselves
        # Check if pilot/instructor is endorsed for the plane
        # Check if pilot/instructor is permitted to fly IFR in this plane
        # Add any violations to the result

        # Get id from
        takeoff = utils.str_to_time(lesson[3])
        student = utils.get_for_id(lesson[0],students)
        instructor = utils.get_for_id(lesson[2],instructors)
        plane = utils.get_for_id(lesson[1],fleet)

        if bad_endorsement(takeoff,student,instructor,plane):
            vltn = lesson + ['Endorsement']
            list_violation.append( vltn)

        if lesson[5] == 'IFR' and bad_ifr(takeoff,student,instructor,plane):
            vltn = lesson +  ['IFR']
            list_violation.append( vltn)

    #print(list_violation)
    return list_violation