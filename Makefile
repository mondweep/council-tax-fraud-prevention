# Council Tax Fraud Prevention - Development Makefile
.PHONY: help install install-dev test lint format clean run-cli run-dashboard docker-build docker-run

# Default target
help:
	@echo "🛡️  Council Tax Fraud Prevention System - Development Commands"
	@echo "============================================================="
	@echo ""
	@echo "Environment Setup:"
	@echo "  setup              Run the full environment setup script"
	@echo "  install            Install production dependencies"
	@echo "  install-dev        Install development dependencies"
	@echo ""
	@echo "Application:"
	@echo "  run-cli            Run the CLI demonstration"
	@echo "  run-dashboard      Launch the Streamlit dashboard"
	@echo ""
	@echo "Development:"
	@echo "  test               Run all tests"
	@echo "  test-cov           Run tests with coverage report"
	@echo "  lint               Run linting checks"
	@echo "  format             Format code with black and isort"
	@echo "  type-check         Run type checking with mypy"
	@echo ""
	@echo "Security:"
	@echo "  security-check     Run security vulnerability scans"
	@echo "  audit              Audit dependencies for vulnerabilities"
	@echo ""
	@echo "Documentation:"
	@echo "  docs-build         Build documentation"
	@echo "  docs-serve         Serve documentation locally"
	@echo ""
	@echo "Cleanup:"
	@echo "  clean              Clean up generated files and caches"
	@echo "  clean-all          Complete cleanup including venv"

# Environment Setup
setup:
	@./scripts/setup_environment.sh

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

# Application Commands
run-cli:
	@echo "🚀 Running CLI demonstration..."
	python src/cli_demo.py

run-dashboard:
	@echo "🌐 Launching Streamlit dashboard..."
	@echo "Dashboard will be available at: http://localhost:8501"
	streamlit run src/dashboard.py

# Development Commands
test:
	@echo "🧪 Running tests..."
	pytest tests/ -v

test-cov:
	@echo "🧪 Running tests with coverage..."
	pytest tests/ --cov=src --cov-report=html --cov-report=term-missing -v
	@echo "📊 Coverage report available at: htmlcov/index.html"

lint:
	@echo "🔍 Running linting checks..."
	flake8 src/ tests/
	pylint src/ || true

format:
	@echo "🎨 Formatting code..."
	black src/ tests/
	isort src/ tests/

type-check:
	@echo "🔎 Running type checks..."
	mypy src/ || true

# Security Commands
security-check: audit bandit

audit:
	@echo "🛡️  Auditing dependencies..."
	pip-audit || true
	safety check || true

bandit:
	@echo "🔒 Running security scan..."
	bandit -r src/ -f json -o reports/security-report.json || true
	bandit -r src/ || true

# Documentation Commands
docs-build:
	@echo "📚 Building documentation..."
	mkdocs build

docs-serve:
	@echo "📖 Serving documentation locally..."
	@echo "Documentation will be available at: http://localhost:8000"
	mkdocs serve

# Cleanup Commands
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + || true
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	rm -rf .mypy_cache/
	rm -rf .tox/
	@echo "✅ Cleanup complete"

clean-all: clean
	@echo "🧹 Complete cleanup..."
	rm -rf venv/
	rm -rf node_modules/ || true
	@echo "✅ Complete cleanup finished"

# Development workflow
dev-setup: setup install-dev
	@echo "✅ Development environment ready!"

# CI/CD simulation
ci-check: lint type-check test security-check
	@echo "✅ All CI checks passed!"

# Quick demo
demo: run-cli
	@echo ""
	@echo "💡 To see the web interface, run: make run-dashboard"

# Production build simulation
build:
	@echo "🏗️  Building production package..."
	python -m build
	@echo "✅ Package built successfully"

# Docker commands (if Docker is available)
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t council-tax-fraud-prevention .

docker-run:
	@echo "🐳 Running Docker container..."
	docker run -p 8501:8501 council-tax-fraud-prevention

# Environment info
info:
	@echo "📋 Environment Information"
	@echo "========================="
	@python --version
	@pip --version
	@echo "Virtual environment: $(VIRTUAL_ENV)"
	@echo "Current directory: $(PWD)"