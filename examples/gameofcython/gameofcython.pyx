# cython: c_string_type=unicode, c_string_encoding=utf8, language_level=3str
# distutils: language=c++
from time import time

from libcpp.string cimport string
from libcpp.unordered_map cimport unordered_map

from cymem.cymem cimport Pool

from hypergen.ultragen cimport *


ctypedef char* s
cdef struct Hpg:
    string html
    unordered_map [string, string] event_handler_callbacks

cdef void template(Hpg &hpg) nogil:
    cdef int i,j
    table_o(hpg, [T])
    for i in range(100):
        tr_o(hpg, [T])
        for j in range(100):
            td(hpg, i2s(i+j), [T])
        tr_c(hpg)

    table_c(hpg)
        
def render():
    cdef Hpg hpg = make_hpg()
    cdef int i
    a = time()
    template(hpg)
    print("Duration:", (time() - a) * 1000, "ms")
    return hpg.html
