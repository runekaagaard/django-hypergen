# cython: c_string_type=unicode, c_string_encoding=utf8, language_level=3str
# distutils: language=c++
from libcpp.vector cimport vector
from libcpp.string cimport string

from libc.stdlib cimport calloc, free
from libc.stdio cimport printf

from cymem.cymem cimport Pool
from time import time

ctypedef char* s

cdef:
    string T = <char*>"__TERM__"
    
cdef struct Item:
    int is_completed
    string description

cdef struct Hpg:
    string html

cdef void element(string tag, Hpg &hpg, string s, string* attrs) nogil:
    cdef int i, j
    hpg.html.append('<')
    hpg.html.append(tag)

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
    hpg.html.append('</')
    hpg.html.append(tag)
    hpg.html.append('>\n')

cdef inline void div(Hpg &hpg, string s, string* attrs) nogil:
    element(<char*>"div", hpg, s, attrs)

cdef inline void b(Hpg &hpg, string s, string* attrs) nogil:
    element(<char*>"b", hpg, s, attrs)
    
cdef string prontotemplate(Hpg &hpg, Item* items, int n) nogil:
    cdef int i
    for i in range(10000):
        for item in items[:n]:
            if not item.is_completed:
                b(hpg, <s>"GET STARTED NOW!", [<s>"class", <s>"my-divø",
                                               <s>"id", <s>"foo92", T])
            div(hpg, item.description, [T])


def speedball(python_items):
    cdef:
        Pool mem = Pool()
        Hpg hpg = Hpg(<s>"")
        int i
        dict item
        
    items = <Item*>mem.alloc(len(python_items), sizeof(Item))
    for i, item in enumerate(python_items):
         items[i] =Item(item["is_completed"], item["description"])

    a = time()
    prontotemplate(hpg, items, len(python_items))
    b = time()
    print((b - a) * 1000)
    return hpg.html
