from bs4 import BeautifulSoup as bs
import bs4
import os
import sys

import argparse

import pyperclip as pc

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file")
args = parser.parse_args()


def indent(txt, i):
    return "".join(["".join(["    " for x in range(i)]), txt])

def _attr_val(val):
    if type(val) is list:
        return (" ".join(val))
    return val

def _attrs(tag):
    _attr_map = {
        'class': 'class_',
        'id': 'id_',
        'placeholder': 'placeholder',
        'type': 'type_',
        'href': 'href'
    }   
    return ', '.join(map(
        lambda k: '{}="{}"'.format(_attr_map[k], _attr_val(tag.get(k))),
        [k for k in _attr_map.keys() if tag.get(k)]
    ))

def _string(tag):
    for child in tag.children:
        if type(child) == bs4.element.NavigableString:
            return child.string

def _params(tag):
    if _string(tag):
        txt = 'u"{}"'.format(tag.string)
        if _attrs(tag):
            return  ', '.join([txt, _attrs(tag)])
        return txt
    return _attrs(tag)


def _c(tag, i):
    if not tag.name:
        return ""
    
    return indent("with {}.c({}):\n".format(tag.name, _params(tag)), i)

def _(tag, i):
    if not tag.name:
        return ""
    return indent("{}({})\n".format(tag.name, _params(tag)), i)
                   

def hyperfy(html, i_start=1):
    soup = bs(html, 'html.parser')
    #print(h(soup))
    txt = ""
    for d in soup.descendants:
        indent = len(list(d.parents))-i_start
        if type(d) == bs4.element.Tag:
            if len(list(d.children)) == 0 or (len(list(d.children)) == 1 and type(next(d.children)) == bs4.element.NavigableString):
                txt+=_(d, indent)
            else:
                txt+=_c(d, indent)
        else:
            pass    
    return txt


if args.file:
    with open(args.file, "r") as file:
        sys.stdout.write(hyperfy(file))
else:
    txt = hyperfy(pc.paste())
    pc.copy(txt)
    sys.stdout.write(txt)
