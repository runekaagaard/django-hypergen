from hypergen.template import base_element, base_element_void

__all__ = [
    # Container/Structural Elements
    'g', 'defs', 'symbol', 'marker', 'mask', 'pattern', 'clipPath', 'foreignObject',
    'switch',
    
    # Shape Elements  
    'circle', 'ellipse', 'line', 'path', 'polygon', 'polyline', 'rect',
    
    # Text Elements
    'text', 'tspan', 'textPath', 'tref',
    
    # Gradient & Paint Elements
    'linearGradient', 'radialGradient', 'stop', 'solidColor',
    
    # Filter Elements
    'filter_', 'feBlend', 'feColorMatrix', 'feComponentTransfer', 'feComposite',
    'feConvolveMatrix', 'feDiffuseLighting', 'feDisplacementMap', 'feDistantLight',
    'feDropShadow', 'feFlood', 'feFuncA', 'feFuncB', 'feFuncG', 'feFuncR',
    'feGaussianBlur', 'feImage', 'feMerge', 'feMergeNode', 'feMorphology',
    'feOffset', 'fePointLight', 'feSpecularLighting', 'feSpotLight', 'feTile',
    'feTurbulence',
    
    # Animation Elements
    'animate', 'animateTransform', 'animateMotion', 'set_', 'mpath',
    
    # Descriptive Elements
    'desc', 'metadata',
    
    # Self-closing Elements
    'use', 'image', 'view', 'cursor', 'animateColor',
]

# Container/Structural Elements
class g(base_element): pass
class defs(base_element): pass
class symbol(base_element): pass
class marker(base_element): pass
class mask(base_element): pass
class pattern(base_element): pass
class clipPath(base_element): pass
class foreignObject(base_element): pass
class switch(base_element): pass

# Shape Elements
class circle(base_element): pass
class ellipse(base_element): pass
class line(base_element): pass
class path(base_element): pass
class polygon(base_element): pass
class polyline(base_element): pass
class rect(base_element): pass

# Text Elements
class text(base_element): pass
class tspan(base_element): pass
class textPath(base_element): pass
class tref(base_element): pass  # Deprecated but still used

# Gradient & Paint Elements
class linearGradient(base_element): pass
class radialGradient(base_element): pass
class stop(base_element): pass
class solidColor(base_element): pass

# Filter Elements
class filter_(base_element): pass
class feBlend(base_element): pass
class feColorMatrix(base_element): pass
class feComponentTransfer(base_element): pass
class feComposite(base_element): pass
class feConvolveMatrix(base_element): pass
class feDiffuseLighting(base_element): pass
class feDisplacementMap(base_element): pass
class feDistantLight(base_element): pass
class feDropShadow(base_element): pass
class feFlood(base_element): pass
class feFuncA(base_element): pass
class feFuncB(base_element): pass
class feFuncG(base_element): pass
class feFuncR(base_element): pass
class feGaussianBlur(base_element): pass
class feImage(base_element): pass
class feMerge(base_element): pass
class feMergeNode(base_element): pass
class feMorphology(base_element): pass
class feOffset(base_element): pass
class fePointLight(base_element): pass
class feSpecularLighting(base_element): pass
class feSpotLight(base_element): pass
class feTile(base_element): pass
class feTurbulence(base_element): pass

# Animation Elements
class animate(base_element): pass
class animateTransform(base_element): pass
class animateMotion(base_element): pass
class set_(base_element): pass
class mpath(base_element): pass

# Descriptive Elements
class desc(base_element): pass
class metadata(base_element): pass

# Self-closing Elements (void elements)
class use(base_element_void): pass
class image(base_element_void): pass
class view(base_element_void): pass
class cursor(base_element_void): pass
class animateColor(base_element_void): pass  # Deprecated but sometimes used