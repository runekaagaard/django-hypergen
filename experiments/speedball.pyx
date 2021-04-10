# cython: c_string_type=unicode, c_string_encoding=utf8, language_level=3str
# distutils: language=c++
"""
# cython: wraparound=False, boundscheck=False, cdivision=True
# cython: profile=False, nonecheck=False, overflowcheck=False
# cython: cdivision_warnings=False, unraisable_tracebacks=False
"""

# import numpy as np
# cimport numpy as np

from libcpp.vector cimport vector
from libcpp.string cimport string

from libc.stdlib cimport calloc, free
from libc.stdio cimport printf

from cymem.cymem cimport Pool

cdef:
    string T = <char*>"__TERM__"
    
cdef struct Item:
    int is_completed
    string description

cdef struct Hpg:
    string html
    
cdef void div(Hpg &hpg, string s, string* attrs) nogil:
    cdef int i, j
    hpg.html.append('<div')

    if attrs[0] != T:
        for i in range(0, 100, 2):
            j = i + 1
            if attrs[i] == T:
                break
            else:
                hpg.html.append(" ")
                hpg.html.append(attrs[i])
                hpg.html.append('="')
                hpg.html.append(attrs[j])
                hpg.html.append('"')

    hpg.html.append('>')
    hpg.html.append(s)
    hpg.html.append('</div>\n')

cdef string prontotemplate(Hpg &hpg, Item* items, int n) nogil:
    for item in items[:n]:
        if not item.is_completed:
            div(hpg, <char*> "GET STARTED NOW!", [<char*>"class", <char*>"my-div",
                                                  <char*>"id", <char*>"foo92", T])
        div(hpg, item.description, [T])


def speedball():
    cdef Pool mem = Pool()
    python_items = [
        {"is_completed": True, "description": "I am the Zohan!"},
        {"is_completed": False, "description": "Who are you!"},
        {"is_completed": True, "description": "I am nice!"},
        {"is_completed": False, "description": "Done with this!"},
    ]
    items = <Item*>mem.alloc(len(python_items), sizeof(Item))
    for i, item in enumerate(python_items):
         items[i] =Item(item["is_completed"], item["description"])

    cdef Hpg hpg = Hpg(<char*> "")
    prontotemplate(hpg, items, len(python_items))
    print()
    print(hpg.html)
