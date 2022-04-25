import keyword

GLOBALS = list(globals().keys())
BUILTINS = dir(__builtins__)

TEMPLATE = "### TEMPLATE-ELEMENT ###"
RENDERED = "### RENDERED-ELEMENTS ###"
TEMPLATE_VOID = "### TEMPLATE-VOID-ELEMENT ###"
RENDERED_VOID = "### RENDERED-VOID-ELEMENTS ###"
"""
Tags taken from https://www.w3schools.com/tags/, with:

JSON.stringify([...document.getElementsByTagName("td")].filter(x => x.firstElementChild && x.firstElementChild.tagName === "A" && x.firstElementChild.href && x.firstElementChild.href.includes("tags/tag_")).map(x => x.firstElementChild.innerHTML.replace("&lt;", "").replace("&gt;", "").replace("!", "")))

# Add h1 to h6 manually.
"""

ALL_TAGS = set([
    "doctype", "a", "abbr", "acronym", "address", "applet", "area", "article", "aside", "audio", "b", "base",
    "basefont", "bdi", "bdo", "big", "blockquote", "body", "br", "button", "canvas", "caption", "center", "cite",
    "code", "col", "colgroup", "data", "datalist", "dd", "del", "details", "dfn", "dialog", "dir", "div", "dl", "dt",
    "em", "embed", "fieldset", "figcaption", "figure", "font", "footer", "form", "frame", "frameset", "h1", "h2",
    "h3", "h4", "h4", "h5", "h6", "head", "header", "hr", "html", "i", "iframe", "img", "input", "ins", "kbd",
    "label", "legend", "li", "link", "main", "map", "mark", "meta", "meter", "nav", "noframes", "noscript", "object",
    "ol", "optgroup", "option", "output", "p", "param", "picture", "pre", "progress", "q", "rp", "rt", "ruby", "s",
    "samp", "script", "section", "select", "small", "source", "span", "strike", "strong", "style", "sub", "summary",
    "sup", "svg", "table", "tbody", "td", "template", "tfoot", "th", "thead", "time", "title", "tr", "track", "tt",
    "u", "ul", "var", "video", "wbr", "textarea", "select"])
VOID_TAGS = set([
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'meta', 'param', 'source', 'track', 'wbr', 'command', 'keygen',
    'menuitem'])
HARDCODED_TAGS = set(["input", "doctype"])

def protect(x):
    if x in GLOBALS or x in BUILTINS or x in keyword.kwlist:
        return x + "_"
    else:
        return x

print(sorted([protect(x) for x in ALL_TAGS]))
assert False

print("# yapf: disable")
for tag in sorted(ALL_TAGS - HARDCODED_TAGS):
    cls = "base_element_void" if tag in VOID_TAGS else "base_element"
    print("class {}({}): pass".format(protect(tag), cls))
print("# yapf: enable")

# code = open("_hypergen.py").read()
# template = code.split(TEMPLATE)[1]

# s = ""
# for tag in sorted(ALL_TAGS - VOID_TAGS - HARDCODED_TAGS):
#     tag = protect(tag)
#     stag = tag.rstrip("_")
#     s += template.replace('"div"',
#                           '"{}"'.format(stag)).replace("div", tag).replace(
#                               "{}__".format(stag), "{}_".format(stag))

# code = code.replace(RENDERED, s)

# ###

# template = code.split(TEMPLATE_VOID)[1]
# s = ""
# for tag in VOID_TAGS - HARDCODED_TAGS:
#     tag = protect(tag)
#     stag = tag.rstrip("_")
#     s += template.replace('"link"',
#                           '"{}"'.format(stag)).replace("link", tag).replace(
#                               "{}__".format(stag), "{}_".format(stag))

# code = code.replace(RENDERED_VOID, s)

# open("hypergen.py", "w").write(code)
