# cython: c_string_type=unicode, c_string_encoding=utf8, language_level=3str
# distutils: language=c++
import json
from time import time

from hypergen.ultragen cimport *
from hypergen.core import context as c, t

cdef extern from "stdlib.h":
    double drand48() nogil
    void srand48(long int seedval)

DEF W = 100
DEF H = 100
cdef int WIDTH = W
cdef int HEIGHT = H

# Keeping state likes this of course only works in a one process, one user setting.
cdef int state[W][H]

cdef int populated(int x, int y) nogil:
    return 0 < y < HEIGHT - 1 and 0 < x < WIDTH - 1 and state[x][y] == 1

cdef int num_neighbours(int x, int y) nogil:
    cdef int num = 0
    if populated(x-1, y-1): num += 1
    if populated(x, y-1): num += 1
    if populated(x+1, y-1): num += 1
    
    if populated(x-1, y): num += 1
    if populated(x+1, y): num += 1
    
    if populated(x-1, y+1): num += 1
    if populated(x, y+1): num += 1
    if populated(x+1, y+1): num += 1
            
    return num

cdef void cstep() nogil:
    cdef int x, y, num
    for y in range(HEIGHT):
        for x in range(WIDTH):
            num = num_neighbours(x, y)
            if state[x][y] == 1:
                if not (1 < num < 4):
                    state[x][y] = 0
            else:
                if num == 3:
                    state[x][y] = 1

cdef void creset() nogil:
    cdef int x, y
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            if drand48() > 0.90:
                state[x][y] = 1
            else:
                state[x][y] = 0

cdef void crender(Hpg &hpg) nogil:
    cdef int x, y
    cdef string cls
    h1(hpg, <s>"Game of life rendered with ultragen", [T])
    table_o(hpg, [T])
    for y in range(HEIGHT):
        tr_o(hpg, [T])
        for x in range(WIDTH):
            cls = <s>""
            if state[x][y] == 1:
                cls = <s>"black"
            td(hpg, <s>"", [<s>"class", cls, T])
        tr_c(hpg)
    table_c(hpg)
                
def step():
    cstep()
                
def reset():
    creset()
    
def render():
    cdef Hpg hpg = make_hpg()
    cdef int i
    a = time()
    crender(hpg)
    print("Duration:", (time() - a) * 1000, "ms")
    c.hypergen.into.append(hpg.html)
