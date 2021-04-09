# cython: c_string_type=unicode, c_string_encoding=utf8, language_level=3str
# distutils: language=c++
import numpy as np
cimport numpy as np

from libcpp.vector cimport vector
from libcpp.string cimport string

cdef void div(vector[string] &vect, vector[string] ss) nogil:
    vect.push_back(<char*> '<div>')
    for s in ss:
        vect.push_back(s)
    
    vect.push_back(<char*> '</div>\n')

cdef vector[string] prontotemplate(rows) nogil:
    cdef vector[string] vect
    cdef int i, x
    cdef vector[string] xs
    
    xs.push_back(<char*>"fo")
    xs.push_back(<char*>"fo")
    xs.push_back(<char*>"fo")
    xs.push_back(<char*>"fo")
    xs.push_back(<char*>"fo")

    for i in range(10):
        div(vect, xs)

    return vect

ctypedef fused sink:
    char
    float
    string

cdef packed struct oh_hi:
    int lucky
    char unlucky

DEF MAXPOWER = 100000

def speedball():
    rows = np.array([11, 1, 2])
    # print (rows.dtype)
    # cdef np.ndarray hi2u = np.ndarray((MAXPOWER, 3),dtype=[('lucky','i4'),('unlucky','a10')])
    # cdef oh_hi [:] hi2me = hi2u
    #cdef int [:] rowsv = rows
    print("".join(prontotemplate(rows)))
