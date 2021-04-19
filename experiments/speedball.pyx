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
    element(<char*>"b", hpg, s, attrs)
    
cdef string cb(Hpg &hpg, string id_, string attr_name, string url, string* args) nogil:
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
    for i in range(100):
        arg = args[i]
        if arg == T:
            break
        if i != 0:
            event_handler_callback.append(",")
        event_handler_callback.append(arg)
    event_handler_callback.append("]")
    
    hpg.event_handler_callbacks[client_state_key] = event_handler_callback
    
    return html


cdef struct Args:
    int* ints
    float* floats
    string* strings

cdef inline string i2s(int v) nogil:
    cdef:
        char s[100]
    sprintf(s, "%d", v)
    return <string> s

    
cdef inline string arg_i(int v) nogil:
    cdef:
        char s[100]
    sprintf(s, "%d", v)
    return <string> s

cdef inline string arg_s(string v) nogil:
    cdef string s
    s.append('"')
    s.append(v)
    s.append('"')
    
    return s
    

cdef void prontotemplate(Hpg &hpg, Item* items, int n) nogil:
    cdef:
        Args args
        string id_
        
    for i in range(1):
        for item in items[:n]:
            if not item.is_completed:
                b(hpg, <char*>"GET STARTED NOW!", [<char*>"class", <char*>"my-divø",
                                               <char*>"id", <char*>"foo92", T])
            div(hpg, item.description, [T])
            id_ = <char*> "my-element-"
            id_.append(i2s(item.pk))
            
            button(
                hpg,
                <char*>"I am the champ!",
                [<char*>"id", id_,
                 <char*>"onclick",
                     cb(hpg, id_, <char*>"onclick", <char*>"/todos/delete_item",
                        [arg_i(item.pk), arg_i(item.pk**4), arg_s(<char*>"The guy is nice!"), T]),
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
    print((b - a) * 1000)
    return {
        "html": hpg.html,
        "event_handler_callbacks": {k: json.loads(v) for k, v in dict(hpg.event_handler_callbacks).items()}
    }
