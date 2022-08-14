.PHONY: container clean_container

# Use ./dist as build context to avoid .venv and other files from creating a fat build context
# Docker builds only install from artifacts in ./dist. We can avoid .dockerignore by adjusting
# the build context.


container:
	docker build -t $(shell basename $(CURDIR)):$(shell grep 'version' ./pyproject.toml | cut -d'"' -f2) -f ./multilayer_caching_memcached/deploy/Dockerfile .

clean_container:
	-docker rmi -f $(shell basename $(CURDIR)):$(shell grep 'version' ./pyproject.toml | cut -d'"' -f2)
