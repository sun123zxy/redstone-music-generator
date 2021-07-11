from math import *

def firstRE(arr, val, l = 0, r = 0):
    """first position which >= val"""
    if r == 0: r = len(arr) - 1
    pos = l
    while l <= r:
        mid = floor((l + r) / 2)
        if arr[mid] >= val:
            pos = mid
            r = mid - 1
        else:
            l = mid + 1
    return pos

def lastL(arr, val, l = 0, r = 0):
    """last position which <= val"""
    if r == 0: r = len(arr) - 1
    pos = l
    while l <= r:
        mid = floor((l + r) / 2)
        if arr[mid] < val:
            pos = mid
            l = mid + 1
        else:
            r = mid - 1
    return pos