from libcpp.string cimport string

cdef struct Hpg
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
cdef void b(Hpg &hpg, string s, string* attrs) nogil
cdef void button(Hpg &hpg, string s, string* attrs) nogil
cdef void tr(Hpg &hpg, string s, string* attrs) nogil
cdef void td(Hpg &hpg, string s, string* attrs) nogil
cdef string ok()
