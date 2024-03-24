"""
Test procedures for the utility functions for this project.

These tests read and write from files in the same directory as this file.

Author: Walker M. White (wmw2)
Date:   June 7, 2019
"""

import os.path
import json
# See: https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time
if __package__ is None or __package__ == '':
    # Access the module if run from __main__.py (Script visibility)
    from support import *
else:
    # Access the module if run from __init__.py (Packages visibility)
    from .support import *


# Load the utils modle
utils = load_from_path('utils')




# TEST FUNCTIONS
def test_read_csv():
    """
    Tests the function utils.read_csv
    """
    fcn = 'utils.read_csv'
    
    # Access the file relative to this one, not the user's terminal
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'file1.csv')
    table = utils.read_csv(fpath)
    
    assert_equals(list, type(table),
                  '%s did not return a list: %s' % (fcn,repr(table)))
    assert_true(len(table) > 0 and type(table[0]) == list,
                  '%s did not return a nested list: %s' % (fcn,repr(table)))
    assert_true(len(table[0]) > 0 and type(table[0][0]) == str,
                  '%s did not return a 2d list of strings: %s' % (fcn,repr(table)))
    assert_equals(FILE1, table,
                  '%s did not return the correct 2d list: %s vs %s' % (fcn,repr(table), repr(FILE1)))
    
    print('  %s passed all tests' % fcn)


def test_write_csv():
    """
    Tests the function utils.write_csv
    """
    fcn = 'utils.write_csv'
    
    # Make the file in this directory
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'file2.csv')
    utils.write_csv(FILE2,fpath)
    
    assert_true(os.path.isfile(fpath),'%s did not create a file' % fcn)
    
    file = open(fpath)
    data = file.read()
    file.close()
    assert_true(len(data) > 0,'%s did not write anything to the file' % fcn)
    
    data = data.strip().split('\n')
    assert_equals(len(FILE2), len(data),
                  '%s did not write the correct number of lines' % fcn)
    
    # And check each line
    for pos in range(len(data)):
        line = data[pos].strip().split(',')
        assert_equals(FILE2[pos], line,
                      '%s did not write the correct values for line %d' % (fcn,pos))
    
    print('  %s passed all tests' % fcn)



def test_str_to_time():
    """
    Tests the function utils.str_to_time
    """
    fcn = 'utils.str_to_time'
    
    from dateutil.parser import parse
    from pytz import timezone
    
    input   = '2016-05-12'
    assert_equals(parse(input), utils.str_to_time(input),
                  '%s did not properly parse %s' % (fcn,repr(input)))
    
    input   = '16:23'
    assert_equals(parse(input), utils.str_to_time(input),
                  '%s did not properly parse %s' % (fcn,repr(input)))
    
    input   = '16:23-4:00'
    assert_equals(parse(input), utils.str_to_time(input),
                  '%s did not properly parse %s' % (fcn,repr(input)))
    
    input   = '2016-05-12T16:23-4:00'
    assert_equals(parse(input), utils.str_to_time(input),
                  '%s did not properly parse %s' % (fcn,repr(input)))
    
    input   = '2016-05-12T16:23'
    correct = parse(input+'-4:00')
    assert_equals(correct, utils.str_to_time(input,correct),
                  '%s did not properly assign time zone %s' % (fcn,repr(correct.tzinfo)))
    
    input   = '2016-05-12T16:23'
    correct = parse(input+'-5:00')
    offset =  parse(input+'-4:00')
    result  = utils.str_to_time(input+'-5:00',offset)
    assert_equals(correct, result,
                  '%s overwrote a previously existing time zone: %s vs %s' % (fcn,repr(result.tzinfo),repr(correct.tzinfo)))
    
    input   = '2016-05-12T16:23'
    central = 'America/Chicago'
    correct = timezone(central).localize(parse(input))
    result  =  utils.str_to_time(input,central)
    assert_equals(correct, result, '%s could not handle time zone string %s' % (fcn,repr(central)))
    
    print('  %s passed all tests' % fcn)

def test_daytime():
    """
    Tests the function utils.daytime
    """
    fcn = 'utils.daytime'
    
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'daycycle.json')
    cycle = utils.read_json(fpath)
    
    times = [('2015-06-05T07:00:00',True,True),  ('2015-06-05T17:00:00',True,True),
             ('2015-10-31T06:00:00',False,True), ('2015-10-31T17:00:00',True,False),
             ('2015-11-17T07:00:00',True,True),  ('2015-11-17T17:00:00',False,False),
             ('2015-12-11T07:00:00',False,True), ('2015-06-05T17:00:00',True,True),
             ('2016-11-01T07:00:00',True,True),  ('2016-11-01T17:00:00',False,False),
             ('2017-11-17T07:00:00',False,True), ('2017-11-17T17:00:00',False,False),
             ('2018-06-05T07:00:00',True,True),  ('2018-06-05T17:00:00',True,True),
             ('2018-11-15T07:00:00',True,True),  ('2018-11-15T17:00:00',False,False),
             ('2019-11-15T07:00:00',True,True),  ('2019-11-15T17:00:00',False,False)]
    
    # CHECK THE TEST CASES
    for time in times:
        act  = utils.str_to_time(time[0],"America/New_York")
        day  = utils.daytime(act,cycle)
        data = (fcn,repr(act),'daycycle',repr(day),repr(time[1]))
        assert_equals(time[1], day,'%s(%s,%s) returned %s, but should have returned %s' % data)
        
        act  = utils.str_to_time(time[0],"America/Chicago")
        day  = utils.daytime(act,cycle)
        data = (fcn,repr(act),'daycycle',repr(day),repr(time[2]))
        assert_equals(time[2], day,'%s(%s,%s) returned %s, but should have returned %s' % data)

        # Test the case of no time zone (Same result as first test above) (Edited by STT)
        act  = utils.str_to_time(time[0])
        day  = utils.daytime(act,cycle)
        data = (fcn,repr(act),'daycycle',repr(day),repr(time[1]))
        assert_equals(time[1], day,'%s(%s,%s) returned %s, but should have returned %s' % data)
    
    print('  %s passed all tests' % fcn)


def test_get_for_id():
    """
    Tests the function utils.get_for_id
    """
    fcn = 'utils.get_for_id'
    
    # With header
    result = utils.get_for_id('S00324',FILE1)
    assert_equals(FILE1[3], result,
                  '%s was unable to find student %s in %s' % (fcn,repr('S00324'),repr(FILE1)))
    
    # Without header
    result = utils.get_for_id('S00324',FILE1[1:])
    assert_equals(FILE1[3], result,
                  '%s was unable to find student %s in %s' % (fcn,repr('S00324'),repr(FILE1[1:])))
    
    # Next table
    result = utils.get_for_id('811AX',FILE2)
    assert_equals(FILE2[2], result,
                  '%s was unable to find plane %s in %s' % (fcn,repr('811AX'),repr(FILE2)))
    
    # Bad query
    result = utils.get_for_id('XXXXXX',FILE1)
    assert_equals(None, result, '%s could not properly handle a missing id'% fcn)
    
    print('  %s passed all tests' % fcn)

def test_annual():
    takeoff  = utils.str_to_time('2017-11-10T09:00:00-05:00')
    annual = utils.str_to_time('2016-11-09', "America/New_York")
    import datetime
    print(annual)
    print(annual + datetime.timedelta(days=365) )  #2016-11-09 00:00:00-05:00
    print(annual + datetime.timedelta(days=365) < takeoff)

def test():
    """
    Performs all tests on the module utils.
    """
    print('Testing module utils')
    test_annual()