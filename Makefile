.PHONY: requirements docker-build docker-run

# Export dependencies to requirements.txt
requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

# Build the Docker image
docker-build:
	docker build -t flask-url-shortener .

# Run the Docker container
docker-run:
	docker run -d -p 5000:5000 --env-file .env flask-url-shortener

# Combine all tasks into a single command
all: requirements docker-build docker-run
