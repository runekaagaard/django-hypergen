# cython: c_string_type=unicode, c_string_encoding=utf8, language_level=3str
# distutils: language=c++
cimport cython
from libcpp.string cimport string

cdef string T
ctypedef char* s # Shortcut for char*
ctypedef fused number:
    cython.int
    cython.double
ctypedef fused whatever:
    cython.int
    cython.double
    cython.p_char
    string
cdef struct Hpg:
    string html
    string event_handler_callback_str
cdef Hpg make_hpg()
cdef void commit(Hpg &hpg)
cdef string cb(Hpg &hpg, string id_, string attr_name, string url, string* args=*, int blocks=*,
               string confirm=*, int debounce=*, int clear=*, int upload_files=*) nogil
cdef string n2s(number v, int float_precision=*) nogil
cdef string arg(whatever v) nogil
cdef string arg_el(string id_, string value_func=*, string coerce_func=*) nogil
cdef void element(string tag, Hpg &hpg, whatever s, string* attrs=*) nogil
cdef void div(Hpg &hpg, whatever s, string* attrs=*) nogil
cdef void p(Hpg &hpg, whatever s, string* attrs=*) nogil
cdef void a(Hpg &hpg, string s, string* attrs=*) nogil
cdef void h1(Hpg &hpg, string s, string* attrs=*) nogil
cdef void b(Hpg &hpg, string s, string* attrs=*) nogil
cdef void button(Hpg &hpg, string s, string* attrs=*) nogil
cdef void tr(Hpg &hpg, string s, string* attrs=*) nogil
cdef int tr_o(Hpg &hpg, string* attrs=*) nogil
cdef void tr_c(Hpg &hpg) nogil
cdef int table_o(Hpg &hpg, string* attrs=*) nogil
cdef void table_c(Hpg &hpg) nogil
cdef void td(Hpg &hpg, string s, string* attrs=*) nogil
cdef void textarea(Hpg &hpg, string s, string* attrs=*) nogil

