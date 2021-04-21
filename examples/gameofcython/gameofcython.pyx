# cython: c_string_type=unicode, c_string_encoding=utf8, language_level=3str
# distutils: language=c++
from time import time
from hypergen.ultragen cimport *

cdef void template(Hpg &hpg) nogil:
    cdef int i, j
    h1(hpg, <s>"Game of life rendered in nogil Cython", [T])
    table_o(hpg, [T])
    for i in range(50):
        tr_o(hpg, [T])
        for j in range(50):
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
