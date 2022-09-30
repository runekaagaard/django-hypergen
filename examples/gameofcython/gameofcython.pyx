# cython: c_string_type=unicode, c_string_encoding=utf8, language_level=3str
# distutils: language=c++
import json
from time import time

from hypergen.ultragen cimport *

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

cdef void crender(Hpg &hpg, char* step_url) nogil:
    cdef int x, y
    cdef string cls
    a(hpg, <s>"Back to documentation", [<s>"href", <s>"/documentation/", T])
    h1(hpg, <s>"Game of life rendered with ultragen", [<s>"style", <s>"color: black;\*æøå*\ ", T])
    p(hpg, <s>"This might look weird if more one than user is using the page at the same time :)")
    table_o(hpg)
    for y in range(HEIGHT):
        tr_o(hpg)
        for x in range(WIDTH):
            cls = <s>""
            if state[x][y] == 1:
                cls = <s>"black"
            td(hpg, <s>"", [<s>"class", cls, T])
        tr_c(hpg)
    table_c(hpg)
    
    button(hpg, <s>"Step", [<s>"id", <s>"step",
                            <s>"onclick", cb(hpg, <s>"step", <s>"onclick", step_url,
                                             [<s>"42", arg_el(<s>"mytext"),
                                              arg(42), arg(42.912), arg("foo"), T]),
                            T])
    button(hpg, <s>"Run", [<s>"onclick", <s>"run()", T])
    
    h1(hpg, <s>"Other ultragen features")
    div(hpg, n2s(200))
    div(hpg, n2s(200.9))
    div(hpg, n2s(200.92344353462345, 3))
    div(hpg, 2222)
    div(hpg, 19.42)
    div(hpg, "NCIE")
    textarea(hpg, <s>"My value", [<s>"id", <s>"mytext", T])

cdef void crender2(Hpg &hpg, foo) nogil:
    div(hpg, "KO")
    with gil:
        div(hpg, <string>foo["foo"])
    
    
def step():
    cstep()
                
def reset():
    creset()
    
def render(step_url):
    cdef Hpg hpg = make_hpg()
    cdef int i
    a = time()
    crender(hpg, step_url)
    crender2(hpg, {"foo": "OK"})
    commit(hpg)
    print("Duration:", (time() - a) * 1000, "ms")
    
