from setuptools import Extension, setup
from Cython.Build import cythonize

extensions = [
    Extension("hypergen.ultragen", ["hypergen/ultragen.pyx"]),
    Extension("examples.gameofcython.gameofcython", ["examples/gameofcython/gameofcython.pyx"]),]

setup(
    name="ultra",
    ext_modules=cythonize(extensions),
    zip_safe=False,
)
