# cython: c_string_type=unicode, c_string_encoding=utf8, language_level=3str
# distutils: language=c++
from libcpp.string cimport string
from libcpp.unordered_map cimport unordered_map

cdef string T
ctypedef char* s # Shortcut for char*
cdef struct Hpg:
    string html
    unordered_map [string, string] event_handler_callbacks
cdef Hpg make_hpg()
cdef struct CbOpts
cdef CbOpts make_cb_opts(string id_) nogil
cdef string cb(Hpg &hpg, string id_, string attr_name, string url, string* args, CbOpts cb_opts) nogil
cdef string i2s(int v) nogil
cdef string arg_i(int v) nogil
cdef string arg_s(string v) nogil
cdef struct ArgElOpts
cdef string arg_el(string id_, ArgElOpts opts) nogil
cdef void element(string tag, Hpg &hpg, string s, string* attrs) nogil
cdef void div(Hpg &hpg, string s, string* attrs) nogil
cdef void h1(Hpg &hpg, string s, string* attrs) nogil
cdef void b(Hpg &hpg, string s, string* attrs) nogil
cdef void button(Hpg &hpg, string s, string* attrs) nogil
cdef void tr(Hpg &hpg, string s, string* attrs) nogil
cdef int tr_o(Hpg &hpg, string* attrs) nogil
cdef void tr_c(Hpg &hpg) nogil
cdef int table_o(Hpg &hpg, string* attrs) nogil
cdef void table_c(Hpg &hpg) nogil
cdef void td(Hpg &hpg, string s, string* attrs) nogil

