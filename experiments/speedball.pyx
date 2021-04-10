# cython: c_string_type=unicode, c_string_encoding=utf8, language_level=3str
# distutils: language=c++
# import numpy as np
# cimport numpy as np

from libcpp.vector cimport vector
from libcpp.string cimport string

from libc.stdlib cimport calloc, free
from libc.stdio cimport printf

from cymem.cymem cimport Pool

cdef void div(vector[string] &vect, string s) nogil:
    vect.push_back(<char*> '<div>')
    vect.push_back(s)
    vect.push_back(<char*> '</div>\n')

cdef vector[string] prontotemplate(Item* items, int n) nogil:
    cdef:
        vector[string] html

    for item in items[:n]:
        if not item.is_completed:
            div(html, <char*> "GET STARTED NOW!")
        div(html, item.description)

    return html

cdef struct Item:
    int is_completed
    string description


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

    print()
    print("".join(prontotemplate(items, len(python_items))))
