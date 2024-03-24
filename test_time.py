def str_to_time(timestamp, tzsource=None):
    """
    Returns the datetime object for the given timestamp (or None if timestamp is
    invalid).

    This function should just use the parse function in dateutil.parser to
    convert the timestamp to a datetime object.  If it is not a valid date (so
    the parser crashes), this function should return None.

    If the timestamp has a time zone, then it should keep that time zone even if
    the value for tzsource is not None.  Otherwise, if timestamp has no time zone
    and tzsource is not None, then this function will use tzsource to assign
    a time zone to the new datetime object.

    The value for tzsource can be None, a string, or a datetime object.  If it
    is a string, it will be the name of a time zone, and it should localize the
    timestamp.  If it is another datetime, then the datetime object created from
    timestamp should get the same time zone as tzsource.

    Parameter timestamp: The time stamp to convert
    Precondition: timestamp is a string

    Parameter tzsource: The time zone to use (OPTIONAL)
    Precondition: tzsource is either None, a string naming a valid time zone,
    or a datetime object.
    """
    # HINT: Use the code from the previous exercise and add time zone handling.
    # Use localize if tzsource is a string; otherwise replace the time zone if not None
    import pytz
    from datetime import tzinfo
    from dateutil.parser import parse

    try:
        d = parse(timestamp)
    except:
        return None

    if d.tzinfo is not None and d.tzinfo.utcoffset(d) is not None:
        return d

    # only d.tzinfo is None below
    # txsource tree way split
    if tzsource == None:
        return d
    else:
        try:  # datetime with timezone
            e = d.replace(tzinfo=tzsource.tzinfo)
            return e
        except:
            tz = pytz.timezone(tzsource)
            e = tz.localize(d)
            return e

def time_to_isoformat(time):
    return time.isoformat()

dt1 = str_to_time('2017-01-02 09:00:00-05:00')
dt2 = str_to_time('2016-01-29 00:00:00')


print( type(dt1),  type(dt2) )


print( time_to_isoformat(dt1), time_to_isoformat(dt2))

print( type(dt1),  type(dt2) )
