# cython: c_string_type=unicode, c_string_encoding=utf8, language_level=3str
# distutils: language=c++
import json
from time import time

from hypergen.ultragen cimport *
from hypergen.core import context as c, t

cdef extern from "stdlib.h":
    double drand48() nogil
    void srand48(long int seedval)

DEF W = 200
DEF H = 200
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
    if populated(x, y+1): num += 1
    if populated(x-1, y+1): num += 1
    if populated(x, y+1): num += 1
    if populated(x+1, y+1): num += 1
            
    return num

cdef void cstep() nogil:
    cdef int x, y, num
    for x in range(WIDTH):
        for y in range(HEIGHT):
            num = num_neighbours(x, y)
            if state[x][y] == 1:
                if not (1 < num < 4):
                    state[x][y] = 0
            else:
                if num == 3:
                    state[x][y] = 1

cdef void creset() nogil:
    cdef int x, y
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            if drand48() > 0.50:
                state[x][y] = 1
            else:
                state[x][y] = 0

cdef void crender(Hpg &hpg) nogil:
    cdef int x, y
    cdef string cls
    h1(hpg, <s>"Game of life rendered in nogil Cython", [T])
    table_o(hpg, [T])
    for x in range(WIDTH):
        tr_o(hpg, [T])
        for y in range(HEIGHT):
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
    if not c.request.is_ajax():
        c.hypergen.commands.append(["fastSetTable", json.dumps(hpg.html).strip('"')])
    else:
        c.hypergen.commands.append(["fastSetTable", hpg.html])
