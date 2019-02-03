from random import randint
from math import atan2
import numpy as np


def help():
    from eyevents.messages import messages
    from eyevents.settings import LANG
    print(messages['SETTINGS_INFO_MESSAGE'][LANG])


def get_shortname(path):
    """Returns filename only"""
    buf = path.replace('..', '_').split('.')
    if len(buf) < 2:
        shortname = path.split('/')[-1].split('\\')[-1]
    else:
        shortname = '_'.join(buf[:-1]).split('\\')[-1].split('/')[-1]
    return shortname


def geron(x, y):
    """Calculates triangle area by Geron's formula"""
    a = np.sqrt((x[1] - x[0])**2 + (y[1] - y[0])**2)
    b = np.sqrt((x[2] - x[1])**2 + (y[2] - y[1])**2)
    c = np.sqrt((x[0] - x[2])**2 + (y[0] - y[2])**2)
    p = (a+b+c) / 2
    result = np.sqrt(p * (p-a) * (p-b) * (p-c))
    return result


def polar_angle(p0,p1=None):
    """Returns the polar angle (radians) from p0 to p1.
If p1 is None, defaults to replacing it with the global variable 'anchor', normally set in the 'graham_scan'."""
    if p1 is None:
        p1 = anchor
    y_span = p0[1]-p1[1]
    x_span = p0[0]-p1[0]
    return atan2(y_span,x_span)


def distance(p0,p1=None):
    """Returns the euclidean distance from p0 to p1, square root is not applied for sake of speed.
If p1 is None, defaults to replacing it with the global variable 'anchor', normally set in the 'graham_scan'."""
    if p1 is None:
        p1 = anchor
    y_span=p0[1]-p1[1]
    x_span=p0[0]-p1[0]
    return y_span**2 + x_span**2


def det(p1,p2,p3):
    """Returns the determinant of the 3x3 matrix"""
    return (p2[0]-p1[0])*(p3[1]-p1[1]) - (p2[1]-p1[1])*(p3[0]-p1[0])


def quicksort(a):
    """Sorts in order of increasing polar angle from 'anchor' point.
'anchor' variable is assumed to be global, set from within 'graham_scan'.
For any values with equal polar angles, a second sort is applied to ensure increasing distance from the 'anchor'."""
    if len(a) <= 1:
        return a
    smaller,equal,larger=[],[],[]
    piv_ang=polar_angle(a[randint(0,len(a)-1)]) # select random pivot
    for pt in a:
        pt_ang = polar_angle(pt) # calculate current point angle
        if pt_ang < piv_ang:
            smaller.append(pt)
        elif pt_ang == piv_ang:
            equal.append(pt)
        else:
            larger.append(pt)
    return quicksort(smaller) + sorted(equal,key=distance) + quicksort(larger)


def graham_scan(points):
    """Returns the vertices comprising the boundaries of convex hull containing all points in the input set.
The input 'points' is a list of (x,y) coordinates."""
    global anchor  # to be set, (x,y) with smallest y value
    # Find the (x,y) point with the lowest y value, along with its index in the 'points' list.
    # If there are multiple points with the same y value, choose the one with smallest x.
    min_idx = None
    for i,(x,y) in enumerate(points):
        if min_idx is None or y < points[min_idx][1]:
            min_idx = i
        if y == points[min_idx][1] and x < points[min_idx][0]:
            min_idx = i
    # set the global variable 'anchor', used by the 'polar_angle' and 'distance' functions
    anchor = points[min_idx]

    # sort the points by polar angle then delete  the anchor from the sorted list
    sorted_pts = quicksort(points)
    del sorted_pts[sorted_pts.index(anchor)]

    # anchor and point with smallest polar angle will always be on hull
    hull = [anchor, sorted_pts[0]]
    for s in sorted_pts[1:]:
        while det(hull[-2], hull[-1], s) <= 0:
            del hull[-1]  # backtrack
            if len(hull) < 2:
                break
        hull.append(s)
    return hull
