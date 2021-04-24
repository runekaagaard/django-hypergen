# cython: c_string_type=unicode, c_string_encoding=utf8, language_level=3str
# distutils: language=c++
cimport cython
from libcpp.string cimport string
from libcpp.unordered_map cimport unordered_map

cdef string T
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
    string confirm_
    int debounce
    int clear
    string element_id
    int upload_files
cdef CbOpts make_cb_opts(string id_, int blocks=*, string confirm=*, int debounce=*, int clear=*,
                         int upload_files=*) nogil
cdef string cb(Hpg &hpg, string id_, string attr_name, string url, string* args, CbOpts cb_opts) nogil
cdef string n2s(number v, int float_precision=*) nogil
cdef string arg_i(int v) nogil
cdef string arg_s(string v) nogil
cdef struct ArgElOpts
cdef string arg_el(string id_, ArgElOpts opts) nogil
cdef void element(string tag, Hpg &hpg, string s, string* attrs) nogil
cdef void div(Hpg &hpg, string s, string* attrs) nogil
cdef void h1(Hpg &hpg, string s, string* attrs) nogil
cdef void b(Hpg &hpg, string s, string* attrs) nogil
cdef void button(Hpg &hpg, string s, string* attrs=*) nogil
cdef void tr(Hpg &hpg, string s, string* attrs) nogil
cdef int tr_o(Hpg &hpg, string* attrs) nogil
cdef void tr_c(Hpg &hpg) nogil
cdef int table_o(Hpg &hpg, string* attrs) nogil
cdef void table_c(Hpg &hpg) nogil
cdef void td(Hpg &hpg, string s, string* attrs) nogil

