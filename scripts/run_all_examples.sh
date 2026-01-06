#!/bin/bash

set -e

echo "========================================"
echo "Running All Langfuse Examples"
echo "========================================"
echo ""

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Check if .env exists
if [[ ! -f .env ]]; then
    echo "Error: .env file not found"
    echo "Please copy .env.example to .env and configure your API keys"
    exit 1
fi

# Run examples in order
examples=(
    "01_basic_tracing.py"
    "02_openai_integration.py"
    "03_prompt_management.py"
    "04_dataset_evaluation.py"
    "05_langchain_integration.py"
    "06_production_rag_system.py"
)

echo "Will run ${#examples[@]} examples"
echo ""

for example in "${examples[@]}"; do
    echo "========================================"
    echo "Running: $example"
    echo "========================================"
    python examples/$example
    echo ""
    echo "Press Enter to continue to next example (or Ctrl+C to stop)..."
    read
done

echo ""
echo "========================================"
echo "All Examples Completed!"
echo "========================================"
echo ""
echo "View your traces in Langfuse dashboard:"
echo "  https://cloud.langfuse.com"
echo ""

