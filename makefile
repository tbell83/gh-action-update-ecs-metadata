REPO_NAME := $(shell git config --get remote.origin.url | awk -F'/' '{print $$NF}' | sed 's/.git//g')

build:
	docker build . -t $(REPO_NAME)
