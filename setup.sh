#!/bin/bash

set -e

echo "=========================================="
echo "Langfuse POC Setup Script"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Copy .env.example to .env:"
echo "     cp .env.example .env"
echo ""
echo "  2. Edit .env and add your API keys:"
echo "     - LANGFUSE_SECRET_KEY (from cloud.langfuse.com)"
echo "     - LANGFUSE_PUBLIC_KEY (from cloud.langfuse.com)"
echo "     - OPENAI_API_KEY"
echo ""
echo "  3. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  4. Run an example:"
echo "     python examples/01_basic_tracing.py"
echo ""
echo "For more information, see README.md"
echo ""
