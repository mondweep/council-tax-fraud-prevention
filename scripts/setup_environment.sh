#!/bin/bash

# Council Tax Fraud Prevention - Environment Setup Script
# This script sets up the development environment for the project

set -e  # Exit on any error

echo "🛡️  Council Tax Fraud Prevention System - Environment Setup"
echo "==========================================================="

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.8"

echo "📋 Checking Python version..."
if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "✅ Python $python_version is compatible (>= 3.8 required)"
else
    echo "❌ Python $python_version is not compatible. Python 3.8+ required."
    echo "Please install Python 3.8 or higher and try again."
    exit 1
fi

# Create virtual environment
echo "🔧 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install production dependencies
echo "📥 Installing production dependencies..."
pip install -r requirements.txt

# Ask if user wants development dependencies
read -p "📝 Install development dependencies? (y/N): " install_dev
if [[ $install_dev =~ ^[Yy]$ ]]; then
    echo "📥 Installing development dependencies..."
    pip install -r requirements-dev.txt
    
    # Setup pre-commit hooks
    echo "🪝 Setting up pre-commit hooks..."
    pre-commit install
    echo "✅ Pre-commit hooks installed"
fi

# Create necessary directories
echo "📁 Creating project directories..."
mkdir -p data/sample
mkdir -p logs
mkdir -p reports
mkdir -p models
mkdir -p backup

# Create .gitkeep files for empty directories
touch data/.gitkeep
touch data/sample/.gitkeep
touch logs/.gitkeep
touch reports/.gitkeep
touch models/.gitkeep
touch backup/.gitkeep

echo "✅ Directory structure created"

# Set up environment variables template
echo "🔧 Creating environment template..."
cat > .env.example << EOF
# Council Tax Fraud Prevention - Environment Variables Template
# Copy this file to .env and configure your settings

# Application Settings
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO

# Database Configuration (when needed)
# DATABASE_URL=sqlite:///fraud_detection.db
# DATABASE_HOST=localhost
# DATABASE_PORT=5432
# DATABASE_NAME=fraud_detection
# DATABASE_USER=fraud_user
# DATABASE_PASSWORD=secure_password

# API Keys (when integrating external services)
# ELECTORAL_REGISTER_API_KEY=your_api_key_here
# UTILITY_PROVIDER_API_KEY=your_api_key_here
# CREDIT_REFERENCE_API_KEY=your_api_key_here

# Security Settings
# SECRET_KEY=generate_a_secure_secret_key
# ENCRYPTION_KEY=your_encryption_key_here

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Monitoring and Logging
# SENTRY_DSN=your_sentry_dsn_here
# LOG_FILE_PATH=logs/fraud_detection.log

# Performance Settings
MAX_CONCURRENT_CASES=100
BATCH_PROCESSING_SIZE=50

# Alert Settings
ENABLE_EMAIL_ALERTS=false
# SMTP_SERVER=smtp.council.gov.uk
# SMTP_PORT=587
# SMTP_USERNAME=alerts@council.gov.uk
# SMTP_PASSWORD=your_smtp_password

EOF

echo "✅ Environment template created (.env.example)"
echo "📝 Copy .env.example to .env and configure your settings"

# Test the installation
echo "🧪 Testing installation..."
python -c "
import streamlit as st
import pandas as pd
import plotly.express as px
import sys
sys.path.append('src')
from fraud_detector import CouncilTaxFraudDetector
print('✅ All core dependencies imported successfully')
detector = CouncilTaxFraudDetector()
print('✅ Fraud detector initialized successfully')
"

echo ""
echo "🎉 Setup Complete!"
echo "==================="
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Copy .env.example to .env and configure settings"
echo "3. Run the CLI demo: python src/cli_demo.py"
echo "4. Launch the dashboard: streamlit run src/dashboard.py"
echo "5. Run tests: pytest tests/"
echo ""
echo "📚 Documentation: See docs/README.md"
echo "🐛 Issues: Report at project repository"
echo ""
echo "⚠️  Remember: This is a prototype for demonstration purposes."
echo "    Production deployment requires additional security hardening."