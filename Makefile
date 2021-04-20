default:
	echo "No default target here. Please be more specific."
	exit 1
compile-cython:
	python setup_cython.py build_ext --inplace
	mv gameofcython.cpython-39-x86_64-linux-gnu.so examples/gameofcython
