version ?= latest
PROJECT_NAME = event-event-stream
IMAGE = $(PROJECT_NAME):$(version)

image:
	docker build -t $(IMAGE) -f ./Dockerfile .
