SHELL := /bin/bash
default:
	echo "No default target here. Please be more specific."
	exit 1
cython-compile:
	ln -s src/hypergen hypergen
	mv setup.cfg xxx
	python setup_cython.py build_ext --inplace || true
	mv xxx setup.cfg
	rm hypergen
cython-clean:
	rm -rf build
	find . -iname "__pycache__" -exec rm -rf '{}' \; || true
	find . -iname *.pyc -delete
	find . -iname "*.so" -delete
python-clean:
	find . -iname "__pycache__" -exec rm -rf '{}' \; || true
	find . -iname *.pyc -delete
docker-build:
	docker image rm hypergen-site || true
	docker build -t hypergen-site .
docker-run:
	docker run --network=host -a STDOUT -a STDERR --rm --name hypergen-site hypergen-site
docker-bash:
	docker exec -it hypergen-site bash
docker-system-prune:
	docker system prune -a
pytest-run:
	pytest --tb=native -x -vvvv src/hypergen/test_all.py
testcafe-run:
	cd examples && testcafe chrome test_all.js -q attemptLimit=5,successThreshold=1 |& ansi2txt
testcafe-run-headless:
	cd examples && testcafe ""chrome:headless"" test_all.js -q attemptLimit=5,successThreshold=1
test-all:
	make pytest-run
	make testcafe-run-headless
pypi-build:
	rm -rf dist/*
	python3 -m build
pypi-check:
	python3 -m twine check dist/*
pypi-show:
	rm -rf /tmp/hypergen_test_build
	virtualenv --python=python3.9 /tmp/hypergen_test_build
	source /tmp/hypergen_test_build/bin/activate && \
		pip install dist/*.whl && \
		tree /tmp/hypergen_test_build/lib/python3.9/site-packages/django_hypergen-1.5.1.dist-info/ && \
		tree /tmp/hypergen_test_build/lib/python3.9/site-packages/hypergen/
pypi-release-test:
	python3 -m twine upload --repository testpypi dist/*
pypi-release:
	python3 -m twine upload dist/*
