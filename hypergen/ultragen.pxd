# cython: c_string_type=unicode, c_string_encoding=utf8, language_level=3str
# distutils: language=c++
cimport cython
from libcpp.string cimport string
from libcpp.unordered_map cimport unordered_map

cdef char* T
ctypedef char* s # Shortcut for char*
ctypedef fused number:
    cython.int
    cython.double
cdef struct Hpg:
    string html
    string event_handler_callback_str
cdef Hpg make_hpg()
cdef void commit(Hpg &hpg)
cdef struct CbOpts:
    int blocks
    char* confirm_
    int debounce
    int clear
    char* element_id
    int upload_files
cdef CbOpts make_cb_opts(char* id_, int blocks=*, char* confirm=*, int debounce=*, int clear=*,
                         int upload_files=*) nogil
cdef char* cb(Hpg &hpg, char* id_, char* attr_name, char* url, char** args, CbOpts cb_opts) nogil
cdef string n2s(number v, int float_precision=*) nogil
cdef string arg_i(int v) nogil
cdef string arg_s(char* v) nogil
cdef struct ArgElOpts
cdef string arg_el(char* id_, ArgElOpts opts) nogil
cdef void element(char* tag, Hpg &hpg, char* s, char** attrs) nogil
cdef void div(Hpg &hpg, char* s, char** attrs) nogil
cdef void h1(Hpg &hpg, char* s, char** attrs) nogil
cdef void b(Hpg &hpg, char* s, char** attrs) nogil
cdef void button(Hpg &hpg, char* s, char** attrs=*) nogil
cdef void tr(Hpg &hpg, char* s, char** attrs) nogil
cdef int tr_o(Hpg &hpg, char** attrs) nogil
cdef void tr_c(Hpg &hpg) nogil
cdef int table_o(Hpg &hpg, char** attrs) nogil
cdef void table_c(Hpg &hpg) nogil
cdef void td(Hpg &hpg, char* s, char** attrs) nogil

