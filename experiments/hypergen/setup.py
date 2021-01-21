from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

# Remove the "-Wstrict-prototypes" compiler option, which isn't valid for C++.
import distutils.sysconfig
cfg_vars = distutils.sysconfig.get_config_vars()
for key, value in cfg_vars.items():
    if type(value) == str:
        cfg_vars[key] = value.replace("-Wstrict-prototypes", "").replace(
            "-Wunused-function", "")

ext_modules = [
    Extension(
        "cython_proof_of_concept", ["cython_proof_of_concept.pyx"],
        extra_compile_args=['-fopenmp', '-O3', '-Wno-unused-function'],
        extra_link_args=['-fopenmp']),
    Extension(
        "pure_python_proof_of_concept", ["pure_python_proof_of_concept.pyx"],
        extra_compile_args=['-O3', '-Wno-unused-function'],
        extra_link_args=[]),
]

setup(name='wwwgen', ext_modules=cythonize(ext_modules, annotate=True))
