# cython: c_string_type=unicode, c_string_encoding=utf8, language_level=3str
# distutils: language=c++
import json
from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp.unordered_map cimport unordered_map

from libc.stdlib cimport calloc, free
from libc.stdio cimport printf, sprintf

from cymem.cymem cimport Pool
from time import time

ctypedef char* s

cdef:
    string T = <char*>"__TERM__"
    int T_int = -1 # TODO: Longer int!
    
cdef struct Item:
    int is_completed
    string description
    int pk

cdef struct Hpg:
    string html
    unordered_map [string, string] event_handler_callbacks
    

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
    
cdef void element(string tag, Hpg &hpg, string s, string* attrs) nogil:
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
    hpg.html.append(s)
    hpg.html.append('</')
    hpg.html.append(tag)
    hpg.html.append('>\n')
    
cdef inline void div(Hpg &hpg, string s, string* attrs) nogil:
    element(<char*>"div", hpg, s, attrs)

cdef inline void b(Hpg &hpg, string s, string* attrs) nogil:
    element(<char*>"b", hpg, s, attrs)

cdef inline void button(Hpg &hpg, string s, string* attrs) nogil:
    element(<char*>"button", hpg, s, attrs)
    
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


cdef struct Args:
    int* ints
    float* floats
    string* strings

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

cdef string arg_el(string id_) nogil:
    cdef string s
    s.append('["_","element_value",["hypergen.read.value", null, "')
    s.append(id_)
    s.append('"]]')

    return s

cdef void prontotemplate(Hpg &hpg, Item* items, int n) nogil:
    cdef:
        Args args
        string id_
        CbOpts cb_opts
        
    for i in range(10000):
        for item in items[:n]:
            if not item.is_completed:
                b(hpg, <s>"GET STARTED NOW!", [<s>"class", <s>"my-divø", <s>"id", <s>"foo92", T])
            div(hpg, item.description, [T])
            id_ = <s> "my-element-"
            id_.append(i2s(item.pk))

            cb_otps = make_cb_opts(id_)
            cb_opts.blocks = True
            cb_opts.clear = True
            button(hpg, <s>"I am the champ!", [
                <s>"id", id_,
                <s>"onclick",
                     cb(hpg, id_, <s>"onclick", <s>"/todos/delete_item",
                        [arg_el(id_), arg_i(item.pk), arg_i(item.pk**4), arg_s(<s>"The guy is nice!"), T],
                        cb_opts
                        ),
                T
            ])

# @hypergen_callback(...)
def delete_item(request, item_id, other_id, who_is_nice_Str):
    # reverse url = "/todos/delete_item"
    pass
            
def speedball(python_items):
    print ("----------------------------------------------------------------")
    cdef:
        unordered_map [string, string] event_handler_callbacks
        Pool mem = Pool()
        Hpg hpg = Hpg(<char*>"", event_handler_callbacks)
        int i
        dict item
        
    items = <Item*>mem.alloc(len(python_items), sizeof(Item))
    for i, item in enumerate(python_items):
         items[i] =Item(item["is_completed"], item["description"], item["pk"])

    a = time()
    prontotemplate(hpg, items, len(python_items))
    b = time()
    print("runtime", (b - a) * 1000, "ms")
    return {
        "html": hpg.html,
        "event_handler_callbacks": {k: json.loads(v) for k, v in dict(hpg.event_handler_callbacks).items()}
    }
