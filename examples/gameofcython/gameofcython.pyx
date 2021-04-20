# cython: c_string_type=unicode, c_string_encoding=utf8, language_level=3str
# distutils: language=c++
from libcpp.string cimport string

from cymem.cymem cimport Pool

from hypergen cimport ultragen
from hypergen.ultragen cimport make_hpg

ctypedef char* s

#cdef void template(hpg):
#    b(hpg, <s>"GET STARTED NOW!", [<s>"class", <s>"my-divø", <s>"id", <s>"foo92", T])

def render():
    cdef hpg = make_hpg()
    #template(hpg)

    # template(hpg)
    #return hpg.html
    return "Jeg er flot"
