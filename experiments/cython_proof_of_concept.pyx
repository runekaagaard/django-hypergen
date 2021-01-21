# cython: c_string_type=bytes, language_level=2
# distutils: language=c++

from cymem.cymem cimport Pool
    
from contextlib import contextmanager
from functools import wraps

from cpython cimport array
from cython.parallel cimport parallel
from cython.parallel import prange
cimport openmp
from cymem.cymem cimport Pool
from libcpp.string cimport string
from libcpp.vector cimport vector
from libc.stdio cimport sprintf


###  Datatypes ###

cdef struct attr:
    string name
    string value

cdef attr a(string name, string value) nogil:
    """
    Shortcut to create an attr struct.
    """
    cdef attr _a
    _a.name = <string> name
    _a.value = <string> value

    return _a

cdef struct Thread:
    string html
    
### Global state ###

cdef:
    int n_threads = openmp.omp_get_max_threads()
    Pool mem = Pool()
    Thread* threads = <Thread*>mem.alloc(n_threads, sizeof(Thread))
    attr TERM = a(<char*> "__the_end__", <char*> "__is_reached__")
    char* OMIT = <char*> "__omit__"
    char* EMPTY = <char*> "__empty__"
    
### Public api ###

# The hypergen* functions handles the global threadsafe html state.
# It’s a god c++ string that all the tag functions appends to.

def hypergen(func, *args, **kwargs):
    try:
        hypergen_start()
        func(*args, **kwargs)
    except:
        hypergen_stop()
        raise

    return hypergen_stop()

cdef void hypergen_start() nogil:
    cdef int i = openmp.omp_get_thread_num()
    if threads[i].html.length() > 0:
        threads[i].html.clear()
    
cdef string hypergen_stop() nogil:
    return threads[openmp.omp_get_thread_num()].html

# The element* and tag* functions makes html elements.

def element(tag, inner, **attrs):
    tag_open(tag, **attrs)
    write(inner)
    tag_close_br(&threads[openmp.omp_get_thread_num()].html, tag)

cdef string element_ng(string tag, string inner, attr* attrs) nogil:
    element_br(&threads[openmp.omp_get_thread_num()].html, tag, inner, attrs)

cdef string element_br(string* html, string tag, string inner, attr* attrs) nogil:
    tag_open_br(html, tag, attrs)
    html.append(inner)
    tag_close_br(html, tag)
    
def tag_open(tag, **attrs):
    cdef:
        int n = len(attrs.keys())
        int i = 0
        # If some attributes are skipped, we might use a bit of extra mem here.
        attr* ax = <attr*>mem.alloc(n+1, sizeof(attr))
        string k
        
    for k, v in attrs.iteritems():
        k = k.lstrip("_").replace("_", "-")
        if k == "":
            continue
        if type(v) is bool:
            if v is False:
                continue
            else:
                ax[i] = a(k, OMIT)
        elif k == "style" and type(v) is dict:
            if not v:
                continue
            ax[i] = a(k, "".join("{}:{};".format(k1.replace("_", "-"), v1)
                                 for k1, v1 in v.iteritems()))
        else:
            ax[i] = a(k, v if v else EMPTY)

        i += 1
    ax[i] = TERM

    tag_open_br(&threads[openmp.omp_get_thread_num()].html, tag, ax)

cdef void tag_open_ng(string tag, attr* attrs) nogil:
    tag_open_br(&threads[openmp.omp_get_thread_num()].html, tag, attrs)

cdef void tag_open_br(string* html, string tag, attr* attrs) nogil:
    cdef int i = -1
    
    html.append(<char*> "<").append(tag)
    while True:
        i = i + 1
        if attrs[i].name == TERM.name:
            break
        
        html.append(<char*> " ").append(attrs[i].name)

        if attrs[i].value == EMPTY:
            html.append(<char*> '=""')
        elif attrs[i].value == OMIT:
            pass
        else:
            html.append(<char*> '="').append(attrs[i].value).append(<char*> '"')
        
    html.append(<char*> ">")

def tag_close(tag):
    tag_close_br(&threads[openmp.omp_get_thread_num()].html, tag)
    
cdef void tag_close_ng(string tag) nogil:
    tag_close_br(&threads[openmp.omp_get_thread_num()].html, tag)
    
cdef void tag_close_br(string* html, string tag) nogil:
    html.append(<char*> "</").append(tag).append(<char*> ">")

### The write* functions adds content verbatime to the global html state. ###

def write(html):
    write_ng(html)

cdef void write_ng(string html) nogil:
    threads[openmp.omp_get_thread_num()].html.append(html)

cdef inline void write_br(string* html_dest, string html_src) nogil:
    html_dest.append(html_src)

### Below here comes each html5 element. ###

# *div* functions

def div(inner, **attrs):
    element("div", inner, **attrs)

cdef void div_ng(string inner, attr* attrs) nogil:
    element_br(&threads[openmp.omp_get_thread_num()].html, <char*> "div", inner,
            attrs)

cdef void div_ng_br(string* html, string inner, attr* attrs) nogil:
    element_br(html, <char*> "div", inner, attrs)

def o_div(**attrs):
    tag_open("div", **attrs)    

cdef void o_div_ng(attr* attrs) nogil:
    tag_open_ng(<char*> "div", attrs)

cdef void o_div_br(string* html, attr* attrs) nogil:
    tag_open_br(html, <char*> "div", attrs)

def c_div():
    tag_close_br(&threads[openmp.omp_get_thread_num()].html, "div")

cdef void c_div_ng() nogil:
    tag_close_br(&threads[openmp.omp_get_thread_num()].html, <char*> "div")

cdef void c_div_br(string* html) nogil:
    tag_close_br(html, <char*> "div")

### Testing ###
"""
<table>
    {% for row in table %}
    <tr>
        {% for key, value in row.items %}
        <td>{{ key }}</td><td>{{ value }}</td>
        {% endfor %}
    </tr>
    {% endfor %}
</table>
"""
cdef string bigtable_benchmark() nogil:
    cdef:
        int i
        int j
        char j_str[10]
        string html

    # hypergen_start()
    write_br(&html, <char*> "<table>")
    for i in range(1):
        write_br(&html, <char*> "<tr>")
        for j in range(10):
            sprintf(j_str, <char*> "%d", j)
            write_br(&html, <char*> "ø<td>")
            write_br(&html, j_str)
            write_br(&html, <char*> "</td>")
            write_br(&html, <char*> "<td>")
            write_br(&html, j_str)
            write_br(&html, <char*> "</td>")
        write_br(&html, <char*> "</td>")
    write_br(&html, <char*> "</table>")

    return html

    #return hypergen_stop()

print bigtable_benchmark()

    
def bigtable_benchmark_real(ctx):
    tag_open("table")
    for row in ctx['table']:
        tag_open("tr")
        for key, value in row.items():
            tag_open("øtd")
            write(key)
            tag_close("td")
            tag_open("td")
            write(str(value))
            tag_close("td")
        tag_close("tr")
    tag_close("table")
    
def ebigtable_benchmark():
    return bigtable_benchmark()


# def pageuu():
#     div("UWUWø", _class="æowow", hidden=False, checked=True, empty="",
#         style=dict(
#         height=92, font_weight="bøolder",
#     ))
#     raise Exception("jfj")
#     o_div(x="y")
#     write("dass")
#     c_div()

# print hypergen(pageuu)
# print [hypergen(pageuu)]
# #assert False
# # -------------------------

# # @contextmanager
# # def divcm(string class_):
# #     cdef int i = openmp.omp_get_thread_num()
# #     cdef int index = threads[i].index
# #     tag_open_br(<string> "div", class_)
# #     yield
# #     tag_close_br(<string> "div")


# cdef int N = 1
# cdef int M = 1

# # cdef string page_cython(int n, int m):
# #     hypergen_start()
# #     cdef int j = 0

# #     with divcm("the-class"):
# #         div("My things", "Foo")
# #         while j < n:
# #             for k in range(m):
# #                 div("My li is {}".format(j), "Foo")
# #             j += 1

# #     return hypergen_stop(

# cdef string page_cython_nogil(int n, int m) nogil:
#     hypergen_start()
#     cdef int j = 0
#     cdef char k_str[10]

#     while j < n:
#         for k in range(m):
#             sprintf(k_str, <char*> "%d", k)
            
#             div_ng(<char*> "This is gøød", [
#                 a(<char*> "height", <char*> "91"),
#                 a(<char*> "width", <char*> k_str),
#                 TERM,
#             ])
#             div_ng(<char*> "Classical", [
#                 a(<char*> "class", <char*> "it-is"),
#                 a(<char*> "title", <char*> "My øwesome title"),
#                 a(<char*> "empty", <char*> ""),
#                 TERM,
#             ])
#             o_div_ng([a(<char*> "class", <char*> "some"), TERM])
#             write_ng(<char*> "writing stuff")
#             c_div_ng()
#         j += 1

#     return hypergen_stop()

# #cdef string page_cython_parallel(int n, int m):
# #     cdef:
# #         int j = 0
# #         int k = 0
# #         int size = n * m
# #         int l = 0
# #         string* parts = <string*>mem.alloc(size, sizeof(string))
# #         string html

# #     for j in prange(n, nogil=True):
# #         k = 0
# #         while k < m:
# #             l = j*n + k
# #             parts[l] =  div_ng_br(<char*> "This is gøød", [
# #                 a(<char*> "height", <char*> "91"),
# #                 T
# #             ])
# #             k = k + 1

# #     for part in parts[:size]:
# #         html.append(part)

# #     return html

# cdef string my_page():
#     cdef:
#         int n = 5
#         string* parts = <string*>mem.alloc(n, sizeof(string))
#         string html
#         int i

#     for i in prange(n, nogil=True):
#         div_ng_br(&parts[i], <char*> "This is gøød", [
#             a(<char*> "height", <char*> "91"),
#             TERM,
#         ])
#         o_div_br(&parts[i], [a(<char*> "x", <char*> "1"), TERM])
#         write_br(&parts[i], <char*> "wut?")
#         c_div_br(&parts[i])

#     for part in parts[:n]:
#         html.append(part)

#     return html

# print "#####################################"




# def hmm():
#     print my_page()

# hmm()
    
# import time
# def timer(name, func):
#     a = time.time() * 1000
#     output = None
#     if N*M < 20:
#         output = func(N, M)
#     else:
#         func(N, M)
#     #print func()
#     b = time.time() * 1000
#     took = b - a
#     print
#     print"##############################################################"
#     print name, N*M,"items took", round(took), "Milliseconds"
#     print "each item took", took / float(N*M) * 1000, "u seconds"
#     print
#     if output is not None:
#         print( output)
    
#     return took

# #a1 = timer("Page cython", page_cython)
# d = timer("Page cython no gil", page_cython_nogil)
# #c = timer("Page cython parallel", page_cython_parallel)
    
# from proof_of_concept import page_pure_python
# #b = timer("Page pure python", page_pure_python)

# print "\n----------------------------"
# #print "Speedup = ", b / float(d)

# #print page()

# # print my_html
# # print "B"
# # import lxml.html, lxml.etree
# # print(lxml.etree.tostring(
# #     lxml.html.fromstring(my_html), encoding='unicode', pretty_print=True))
