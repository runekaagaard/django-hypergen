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
copilot-deploy:
	cd src/hypergen/static/hypergen/ && parcel build -o hypergen.min.js -d . hypergen.js
	cd src/hypergen/static/hypergen/v2 && parcel build -o hypergen.min.js -d . hypergen.js
	git commit -am "website: Building hypergen.js" || true
	git push || true
	cd examples && PROD=1 python manage.py collectstatic --noinput
	copilot deploy -n hypergen-service -e prod
copilot-deploy-no-static:
	copilot deploy -n hypergen-service -e prod
copilot-bash:
	copilot svc exec --name hypergen-service env prod -c /bin/bash
copilot-logs:
	copilot svc logs -n hypergen-service -e prod --follow
docker-system-prune:
	docker system prune -a
pytest-run:
	pytest --tb=native -x -vvvv src/hypergen/test_all.py
testcafe-run:
	cd examples && testcafe chrome test_all.js |& ansi2txt
testcafe-run-headless:
	cd examples && testcafe ""chrome:headless"" test_all.js
test-all:
	make pytest-run
	make testcafe-run-headless
pypi-release:
	rm -rf dist/*
	python3 -m build
	python3 -m twine upload dist/*
