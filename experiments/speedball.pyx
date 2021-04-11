# cython: c_string_type=unicode, c_string_encoding=utf8, language_level=3str
# cython: profile=False, nonecheck=False, overflowcheck=False
# cython: cdivision_warnings=False, unraisable_tracebacks=False
# distutils: language=c++
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
            div(hpg, <char*> "GET STARTED NOW!", [<char*> "class", <char*>"my-divø",
                                                  <char*>"id", <char*>"foo92", T])
        div(hpg, item.description, [T])


def speedball(python_items):
    cdef:
        Pool mem = Pool()
        Hpg hpg = Hpg(<char*> "")
        
    items = <Item*>mem.alloc(len(python_items), sizeof(Item))
    for i, item in enumerate(python_items):
         items[i] =Item(item["is_completed"], item["description"])

    prontotemplate(hpg, items, len(python_items))
    return hpg.html
