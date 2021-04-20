default:
	echo "No default target here. Please be more specific."
	exit 1
compile-cython:
	python setup_cython.py build_ext --inplace
clean-cython:
	find . -iname "__pycache__" -exec rm -rf '{}' \;
	find . -iname "*.so" -delete

