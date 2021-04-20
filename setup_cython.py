from setuptools import Extension, setup
from Cython.Build import cythonize
import numpy

extensions = [
    Extension("hypergen.ultragen", ["hypergen/ultragen.pyx"]),
    Extension("examples.gameofcython.gameofcython", ["examples/gameofcython/gameofcython.pyx"]),]

setup(
    name="ultra",
    ext_modules=cythonize(extensions),
)

# setup(ext_modules=cythonize("hypergen/ultragen.pyx", "./examples/gameofcython/gameofcython.pyx", annotate=True),
#     include_dirs=numpy.get_include())
