from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(ext_modules=cythonize("hypergen/ultragen.pyx", annotate=True), include_dirs=numpy.get_include())
setup(ext_modules=cythonize("examples/gameofcython/gameofcython.pyx", annotate=True),
    include_dirs=numpy.get_include())
