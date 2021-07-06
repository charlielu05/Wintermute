PROJECT=wintermute

# sets up the src directory as a python package
pkg:
	python -m pip install -e .

# builds the development environment
build-dev: 
	docker build --tag $(PROJECT)-dev .

# starts the dev environments
start-dev: build-dev
	docker run -d \
	-t \
	--rm \
	--name winterdev \
	--mount source=$(shell pwd),target=/app,type=bind \
	$(PROJECT)-dev:latest