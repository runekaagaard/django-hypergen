# cython: c_string_type=unicode, c_string_encoding=utf8, language_level=3str
# distutils: language=c++
import json

from libcpp.string cimport string
from libcpp.unordered_map cimport unordered_map
cimport cython
from libc.stdio cimport printf, sprintf
from cymem.cymem cimport Pool

from hypergen.core import context as c

cdef:
    char* T = <char*>"__TERM__" # Terminate list of strings

# Hypergen state passed around to everything
cdef Hpg make_hpg():
    return Hpg(<char*>"", <char*>"{")

cdef void commit(Hpg &hpg):
    # TODO: Dont double encode json, use something like this instead:
    # https://stackoverflow.com/questions/12397279/custom-json-encoder-in-python-with-precomputed-literal-json
    hpg.event_handler_callback_str.append("}")
    c.hypergen.into.append(hpg.html)
    c.hypergen.event_handler_callbacks.update(json.loads(hpg.event_handler_callback_str))
    
# Callback options
cdef struct CbOpts:
    int blocks
    char* confirm_
    int debounce
    int clear
    char* element_id
    int upload_files

cdef CbOpts make_cb_opts(char* id_, int blocks=False, char* confirm=<char*>"", int debounce=0, int clear=False,
                         int upload_files=False) nogil:
    cdef CbOpts opts
    opts.element_id = id_
    opts.blocks = blocks
    opts.confirm_ = confirm
    opts.debounce = debounce
    opts.clear = clear
    opts.upload_files = upload_files
    
    return opts

# Server callback
cdef const char* cb(Hpg &hpg, char* id_, char* attr_name, char* url, char** args, CbOpts cb_opts) nogil:
    cdef:
        string html
        string client_state_key
        string event_handler_callback
        int i
        int arg_i
        char s[100]
        
    client_state_key.append(id_)
    client_state_key.append("__")
    client_state_key.append(attr_name)
    
    html.append("e(event,'")
    html.append(client_state_key)
    html.append("')")

    if hpg.event_handler_callback_str != <char*> "{":
        event_handler_callback.append(',')
    event_handler_callback.append('"')
    event_handler_callback.append(client_state_key)
    event_handler_callback.append('":')
    
    event_handler_callback.append('["hypergen.callback", "')
    event_handler_callback.append(url)
    event_handler_callback.append('",')
    
    event_handler_callback.append('[')
    for i in range(100):
        arg = args[i]
        if arg == T:
            break
        if i != 0:
            event_handler_callback.append(",")
        event_handler_callback.append(arg)
    event_handler_callback.append(']')

    event_handler_callback.append(', {')
    event_handler_callback.append('"blocks":')
    event_handler_callback.append("true") if cb_opts.blocks is True else event_handler_callback.append("false")
    event_handler_callback.append(',"debounce":')
    event_handler_callback.append(n2s(cb_opts.debounce))
    event_handler_callback.append(',"clear":')
    event_handler_callback.append("true") if cb_opts.clear is True else event_handler_callback.append("false")
    event_handler_callback.append(',"elementId":"')
    event_handler_callback.append(id_)
    event_handler_callback.append('"')
    event_handler_callback.append(',"uploadFiles":')
    event_handler_callback.append("true") if cb_opts.upload_files is True else event_handler_callback.append("false")
        
    event_handler_callback.append('}')
    event_handler_callback.append("]")
    
    hpg.event_handler_callback_str.append(event_handler_callback)

# Convert an int or float to a string

cdef string n2s(number v, int float_precision=-1) nogil:
    cdef:
        char s[100]
        char double_fmt[20]
    if number is cython.int:
        sprintf(s, "%d", v)
    elif number is cython.double:
        if float_precision == -1:
            sprintf(s, "%f", v)
        else:
            sprintf(double_fmt, "%%.%df", float_precision)
            sprintf(s, double_fmt, v)
    else:
        raise Exception("Unknown type")
    
    return <string>s
    
cdef string arg_i(int v) nogil:
    cdef:
        char s[100]
    sprintf(s, "%d", v)
    return <string> s

# Cast functions for callback arguments

cdef string arg_s(char* v) nogil:
    cdef string s
    s.append('"')
    s.append(v)
    s.append('"')
    
    return s

cdef struct ArgElOpts:
    string value_func
    string coerce_func

cdef string arg_el(char* id_, ArgElOpts opts) nogil:
    cdef string s
    s.append('["_","element_value",["hypergen.read.value", null, "')
    s.append(id_)
    s.append('"]]')

    return s

# Base HTML element
cdef void element(char* tag, Hpg &hpg, char* s, char** attrs) nogil:
    element_open(tag, hpg, attrs)
    hpg.html.append(s)
    element_close(tag, hpg)

cdef void element_open(char* tag, Hpg &hpg, char** attrs) nogil:
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

cdef void element_close(char* tag, Hpg &hpg) nogil:
    hpg.html.append('</')
    hpg.html.append(tag)
    hpg.html.append('>\n')
    
# HTML elements
cdef inline void div(Hpg &hpg, char* s, char** attrs) nogil:
    element(<char*>"div", hpg, s, attrs)

cdef inline void h1(Hpg &hpg, char* s, char** attrs) nogil:
    element(<char*>"h1", hpg, s, attrs)

cdef inline void b(Hpg &hpg, char* s, char** attrs) nogil:
    element(<char*>"b", hpg, s, attrs)

cdef inline void button(Hpg &hpg, char* s, char** attrs=[T]) nogil:
    element(<char*>"button", hpg, s, attrs)

cdef inline int table_o(Hpg &hpg, char** attrs) nogil:
    element_open(<char*>"table", hpg, attrs)
    return True

cdef inline void table_c(Hpg &hpg) nogil:
    element_close(<char*>"table", hpg)
    
cdef inline void tr(Hpg &hpg, char* s, char** attrs) nogil:
    element(<char*>"tr", hpg, s, attrs)

cdef inline int tr_o(Hpg &hpg, char** attrs) nogil:
    element_open(<char*>"tr", hpg, attrs)
    return True

cdef inline void tr_c(Hpg &hpg) nogil:
    element_close(<char*>"tr", hpg)

cdef inline void td(Hpg &hpg, char* s, char** attrs) nogil:
    element(<char*>"td", hpg, s, attrs)
