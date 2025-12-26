"""
Data utility functions for processing time and positional data.
"""

import polars as pl


'''
Convert a time string in "MM:SS.sss" format to total seconds as an integer.

:param time: Time string in "MM:SS.sss" format.
:param start: Boolean indicating if it's the start time (default is True).

:return: Total seconds as an integer.
'''
def seconds_from_time(time: pl.String, start: bool = True) -> pl.Int32:
    minutes = int(str(time).split(":")[0]) * 60
    seconds = int(str(time).split(":")[1].split(".")[0])

    if start:
        increment = -1
    else:
        increment = 1

    return minutes + seconds + increment


'''
Get the vertical subthird code based on the y-coordinate.

:param x: Y-coordinate as a float.

:return: Subthird code as a string.
'''
def get_subthird(x: pl.Float32) -> pl.String:
    V_LIMITS = [-52.5, -36, -17.5, 0, 17.5, 36, 52.5]
    
    subthird = "Out of pitch"
    if x is None:
        subthird = "Out of pitch"
    else:
        for i in range(1, 7):
            if x <= V_LIMITS[i]:
                subthird = str(i)
                break
    
    return subthird


'''
Get the horizontal channel code based on the y-coordinate.

:param y: Y-coordinate as a float.

:return: Channel code as a string.
'''
def get_channel(y: pl.Float32) -> pl.String:
    H_ZONES = [
        (-34, -20.16, "RW"),
        (-20.16, -9.16, "RHS"),
        (-9.16, 9.16, "C"),
        (9.16, 20.16, "LHS"),
        (20.16, 34, "LW")
    ]
    
    channel = "Out of pitch"
    if y is None:
        channel = "Out of pitch"
    else:
        for min_y, max_y, code in H_ZONES:
            if y <= max_y:
                channel = code
                break
    
    return channel