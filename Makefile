.PHONY: help install test test-cov test-docker build run clean lint format

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements.txt

test: ## Run tests
	pytest tests/ -v

test-cov: ## Run tests with coverage
	pytest tests/ --cov=app --cov-report=html --cov-report=term-missing

test-docker: ## Test the Docker container
	docker build -t weather-predictor-test .
	docker run -d --name weather-test -p 5001:5000 weather-predictor-test
	sleep 5
	curl -f http://localhost:5001/health || (docker logs weather-test && docker stop weather-test && docker rm weather-test && exit 1)
	docker stop weather-test
	docker rm weather-test
	@echo "Docker test passed!"

build: ## Build Docker image
	docker build -t weather-predictor .

run: ## Run the application locally
	python app.py

run-docker: ## Run the application in Docker
	docker run -p 5000:5000 weather-predictor

clean: ## Clean up generated files
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +

lint: ## Run linting
	pip install flake8
	flake8 app.py tests/

format: ## Format code with black
	pip install black
	black app.py tests/

security: ## Run security checks
	pip install safety
	safety check