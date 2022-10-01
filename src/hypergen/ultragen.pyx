# cython: c_string_type=unicode, c_string_encoding=utf8, language_level=3str
# distutils: language=c++
import json

cimport cython
from libcpp.string cimport string
from libc.stdio cimport printf, sprintf

from hypergen.context import context as c

cdef:
    string T = <char*>"__TERM__" # Terminate list of strings
    string* TT = [T]
    

# Hypergen state passed around to everything
cdef Hpg make_hpg():
    return Hpg("", "{")

cdef void commit(Hpg &hpg):
    # TODO: Dont double encode json, use something like this instead:
    # https://stackoverflow.com/questions/12397279/custom-json-encoder-in-python-with-precomputed-literal-json
    hpg.event_handler_callback_str.append("}")
    c.hypergen.into.append(hpg.html)
    c.hypergen.event_handler_callbacks.update(json.loads(hpg.event_handler_callback_str))
    
# Server callback
cdef string cb(Hpg &hpg, string id_, string attr_name, string url, string* args=TT, int blocks=False,
               string confirm=<char*>"", int debounce=0, int clear=False, int upload_files=False) nogil:
    cdef:
        string html
        string client_state_key
        string event_handler_callback
        int i
        
    client_state_key.append(id_)
    client_state_key.append("__")
    client_state_key.append(attr_name)
    
    html.append("hypergen.event(event,'")
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
        elif i != 0:
            event_handler_callback.append(",")
        event_handler_callback.append(arg)
    event_handler_callback.append(']')

    event_handler_callback.append(', {')
    event_handler_callback.append('"blocks":')
    event_handler_callback.append("true") if blocks is True else event_handler_callback.append("false")
    event_handler_callback.append(',"debounce":')
    event_handler_callback.append(n2s(debounce))
    event_handler_callback.append(',"clear":')
    event_handler_callback.append("true") if clear is True else event_handler_callback.append("false")
    event_handler_callback.append(',"elementId":"')
    event_handler_callback.append(id_)
    event_handler_callback.append('"')
    event_handler_callback.append(',"uploadFiles":')
    event_handler_callback.append("true") if upload_files is True else event_handler_callback.append("false")
        
    event_handler_callback.append('}')
    event_handler_callback.append("]")
    
    hpg.event_handler_callback_str.append(event_handler_callback)

    return html

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

cdef string arg(whatever v) nogil:
    cdef char s[20]
    cdef string cs
    if whatever is cython.int:
        sprintf(s, "%d", v)
        return <string> s
    elif whatever is cython.double:
        sprintf(s, "%f", v)
        return <string> s
    elif whatever is cython.p_char:
        cs.append('"')
        cs.append(v)
        cs.append('"')
        return cs
    elif whatever is string:
        return v
    else:
        raise Exception("Bad type")
        

cdef string arg_el(string id_, string value_func=<char*>"hypergen.read.value", string coerce_func=<char*>"null") nogil:
    cdef string s
    s.append('["_","element_value",["')
    s.append(value_func)
    s.append('", ')
    if coerce_func == <char*>"null":
        s.append("null")
    else:
        s.append('"')
        s.append(coerce_func)
        s.append('"')
        
    s.append(', "')
    s.append(id_)
    s.append('"]]')

    return s

# Base HTML element
cdef void element(string tag, Hpg &hpg, whatever s, string* attrs=TT) nogil:
    element_open(tag, hpg, attrs)
    if whatever is cython.int:
        hpg.html.append(n2s(s))
    elif whatever is cython.double:
        hpg.html.append(n2s(s))
    elif whatever is cython.p_char:
        hpg.html.append(s)
    elif whatever is string:
        hpg.html.append(s)
    # elif whatever is unicode:
    #     with gil:
    #         hpg.html.append(<string>s)
    else:
        raise Exception("Bad type")
    element_close(tag, hpg)

cdef void element_open(string tag, Hpg &hpg, string* attrs=TT) nogil:
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
cdef inline void div(Hpg &hpg, whatever s, string* attrs=TT) nogil:
    element(<char*>"div", hpg, s, attrs)

cdef inline void p(Hpg &hpg, whatever s, string* attrs=TT) nogil:
    element(<char*>"p", hpg, s, attrs)

cdef inline void a(Hpg &hpg, string s, string* attrs=TT) nogil:
    element(<char*>"a", hpg, s, attrs)

cdef inline void h1(Hpg &hpg, string s, string* attrs=TT) nogil:
    element(<char*>"h1", hpg, s, attrs)

cdef inline void b(Hpg &hpg, string s, string* attrs=TT) nogil:
    element(<char*>"b", hpg, s, attrs)

cdef inline void button(Hpg &hpg, string s, string* attrs=TT) nogil:
    element(<char*>"button", hpg, s, attrs)

cdef inline int table_o(Hpg &hpg, string* attrs=TT) nogil:
    element_open(<char*>"table", hpg, attrs)
    return True

cdef inline void table_c(Hpg &hpg) nogil:
    element_close(<char*>"table", hpg)
    
cdef inline void tr(Hpg &hpg, string s, string* attrs=TT) nogil:
    element(<char*>"tr", hpg, s, attrs)

cdef inline int tr_o(Hpg &hpg, string* attrs=TT) nogil:
    element_open(<char*>"tr", hpg, attrs)
    return True

cdef inline void tr_c(Hpg &hpg) nogil:
    element_close(<char*>"tr", hpg)

cdef inline void td(Hpg &hpg, string s, string* attrs=TT) nogil:
    element(<char*>"td", hpg, s, attrs)

cdef inline void textarea(Hpg &hpg, string s, string* attrs=TT) nogil:
    element(<char*>"textarea", hpg, s, attrs)
