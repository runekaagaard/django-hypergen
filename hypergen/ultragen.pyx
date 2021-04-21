# cython: c_string_type=unicode, c_string_encoding=utf8, language_level=3str
# distutils: language=c++
from libcpp.string cimport string
from libcpp.unordered_map cimport unordered_map

from libc.stdio cimport printf, sprintf

from cymem.cymem cimport Pool

cdef:
    string T = <char*>"__TERM__" # Terminate list of strings

# Hypergen state passed around to everything
cdef struct Hpg:
    string html
    unordered_map [string, string] event_handler_callbacks

cdef Hpg make_hpg():
    cdef:
        unordered_map [string, string] event_handler_callbacks
        hpg = Hpg(<char*>"", event_handler_callbacks)

    return hpg
    
# Callback options
cdef struct CbOpts:
    int blocks
    string confirm_
    int debounce
    int clear
    string element_id
    int upload_files

cdef CbOpts make_cb_opts(string id_) nogil:
    cdef CbOpts opts
    opts.blocks = False
    opts.confirm_ = <char*>""
    opts.debounce = 0
    opts.clear = False
    opts.element_id = id_
    opts.upload_files = False
    
    return opts

# Server callback
cdef string cb(Hpg &hpg, string id_, string attr_name, string url, string* args, CbOpts cb_opts) nogil:
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

    event_handler_callback.append('["')
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
    event_handler_callback.append(i2s(cb_opts.debounce))
    event_handler_callback.append(',"clear":')
    event_handler_callback.append("true") if cb_opts.clear is True else event_handler_callback.append("false")
    event_handler_callback.append(',"elementId":"')
    event_handler_callback.append(id_)
    event_handler_callback.append('"')
    event_handler_callback.append(',"uploadFiles":')
    event_handler_callback.append("true") if cb_opts.upload_files is True else event_handler_callback.append("false")
        
    event_handler_callback.append('}')
    event_handler_callback.append("]")
    
    hpg.event_handler_callbacks[client_state_key] = event_handler_callback
    
    return html

# Cast functions for callback arguments 

cdef string i2s(int v) nogil:
    cdef:
        char s[100]
    sprintf(s, "%d", v)
    return <string> s

    
cdef string arg_i(int v) nogil:
    cdef:
        char s[100]
    sprintf(s, "%d", v)
    return <string> s

cdef string arg_s(string v) nogil:
    cdef string s
    s.append('"')
    s.append(v)
    s.append('"')
    
    return s

cdef struct ArgElOpts:
    string value_func
    string coerce_func

cdef string arg_el(string id_, ArgElOpts opts) nogil:
    cdef string s
    s.append('["_","element_value",["hypergen.read.value", null, "')
    s.append(id_)
    s.append('"]]')

    return s

# Base HTML element
cdef void element(string tag, Hpg &hpg, string s, string* attrs) nogil:
    element_open(tag, hpg, attrs)
    hpg.html.append(s)
    element_close(tag, hpg)

cdef void element_open(string tag, Hpg &hpg, string* attrs) nogil:
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

cdef void element_close(string tag, Hpg &hpg) nogil:
    hpg.html.append('</')
    hpg.html.append(tag)
    hpg.html.append('>\n')
    
# HTML elements
cdef inline void div(Hpg &hpg, string s, string* attrs) nogil:
    element(<char*>"div", hpg, s, attrs)

cdef inline void h1(Hpg &hpg, string s, string* attrs) nogil:
    element(<char*>"h1", hpg, s, attrs)

cdef inline void b(Hpg &hpg, string s, string* attrs) nogil:
    element(<char*>"b", hpg, s, attrs)

cdef inline void button(Hpg &hpg, string s, string* attrs) nogil:
    element(<char*>"button", hpg, s, attrs)

cdef inline int table_o(Hpg &hpg, string* attrs) nogil:
    element_open(<char*>"table", hpg, attrs)
    return True

cdef inline void table_c(Hpg &hpg) nogil:
    element_close(<char*>"table", hpg)
    
cdef inline void tr(Hpg &hpg, string s, string* attrs) nogil:
    element(<char*>"tr", hpg, s, attrs)

cdef inline int tr_o(Hpg &hpg, string* attrs) nogil:
    element_open(<char*>"tr", hpg, attrs)
    return True

cdef inline void tr_c(Hpg &hpg) nogil:
    element_close(<char*>"tr", hpg)

cdef inline void td(Hpg &hpg, string s, string* attrs) nogil:
    element(<char*>"td", hpg, s, attrs)
