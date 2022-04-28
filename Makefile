default:
	echo "No default target here. Please be more specific."
	exit 1
cython-compile:
	make cython-clean
	ln -s src/hypergen hypergen
	mv setup.cfg xxx
	python setup_cython.py build_ext --inplace
	mv xxx setup.cfg
	rm hypergen
cython-clean:
	find . -iname "__pycache__" -exec rm -rf '{}' \; || true
	find . -iname "*.so" -delete
docker-build:
	docker image rm hypergen-site
	docker build -t hypergen-site .
docker-run:
	docker run --network=host -a STDOUT -a STDERR --rm --name hypergen-site hypergen-site
docker-bash:
	docker exec -it hypergen-site bash
copilot-deploy:
	copilot deploy
