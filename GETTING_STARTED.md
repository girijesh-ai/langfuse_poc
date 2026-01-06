# Getting Started with Langfuse POC

**A Step-by-Step Guide to Using This Repository**

This guide will walk you through everything you need to get started with the Langfuse POC, from initial setup to running your first production-ready example.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Configuration](#configuration)
4. [Running Your First Example](#running-your-first-example)
5. [Exploring All Examples](#exploring-all-examples)
6. [Understanding the Results](#understanding-the-results)
7. [Next Steps](#next-steps)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required

- **Python 3.9+** installed on your system
- **Git** for cloning the repository
- **Langfuse Account**: Sign up at [cloud.langfuse.com](https://cloud.langfuse.com)
- **OpenAI API Key**: Get one from [platform.openai.com](https://platform.openai.com)

### Optional

- **Docker** (for containerized deployment)
- **Node.js 18+** (for JavaScript examples)

### Check Your Prerequisites

```bash
# Check Python version (should be 3.9 or higher)
python3 --version

# Check Git
git --version

# Check Docker (optional)
docker --version
```

---

## Initial Setup

### Step 1: Clone or Navigate to the Repository

```bash
cd /Users/girijesh/Documents/langfuse_poc
```

### Step 2: Run Automated Setup

```bash
# Make setup script executable (if not already)
chmod +x setup.sh

# Run the setup script
./setup.sh
```

**What this does:**
- Creates a Python virtual environment
- Installs all required dependencies
- Sets up the project structure

**Expected output:**
```
==========================================
Langfuse POC Setup Script
==========================================

Checking Python version...
Found Python 3.11.x
Creating Python virtual environment...
...
Setup Complete!
```

### Step 3: Activate the Virtual Environment

```bash
# Activate the virtual environment
source venv/bin/activate

# Your terminal prompt should now show (venv)
```

**Verification:**
```bash
# Check that langfuse is installed
pip list | grep langfuse
# Should show: langfuse x.x.x
```

---

## Configuration

### Step 4: Create Your Environment File

```bash
# Copy the example environment file
cp .env.example .env
```

### Step 5: Get Your Langfuse API Keys

1. Go to [cloud.langfuse.com](https://cloud.langfuse.com)
2. Sign up or log in
3. Create a new project (or use existing)
4. Go to **Settings** → **API Keys**
5. Click **Create New API Keys**
6. Copy both keys:
   - **Public Key** (starts with `pk-lf-...`)
   - **Secret Key** (starts with `sk-lf-...`)

### Step 6: Get Your OpenAI API Key

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign in to your account
3. Click **Create new secret key**
4. Copy the key (starts with `sk-...`)

### Step 7: Configure the .env File

```bash
# Edit the .env file
nano .env
# or
vim .env
# or use your preferred editor
```

**Add your keys:**

```bash
# Langfuse Configuration
LANGFUSE_SECRET_KEY=sk-lf-YOUR_SECRET_KEY_HERE
LANGFUSE_PUBLIC_KEY=pk-lf-YOUR_PUBLIC_KEY_HERE
LANGFUSE_HOST=https://cloud.langfuse.com

# OpenAI API Key
OPENAI_API_KEY=sk-YOUR_OPENAI_KEY_HERE

# Environment
LANGFUSE_ENVIRONMENT=development
```

**Save and close** the file (Ctrl+X, then Y, then Enter in nano).

### Step 8: Verify Configuration

```bash
# Test that configuration is working
python -c "from langfuse import get_client; client = get_client(); print('Connection successful!' if client.auth_check() else 'Connection failed')"
```

**Expected output:**
```
Connection successful!
```

---

## Running Your First Example

### Step 9: Run Basic Tracing Example

```bash
python examples/01_basic_tracing.py
```

**What you'll see:**

```
============================================================
Langfuse Example 1: Basic Tracing
============================================================

Processing query: What is Langfuse?
Retrieving context for: What is Langfuse?
Generating response for: What is Langfuse?

Pipeline completed successfully
View trace in Langfuse dashboard

Result: Based on the context, here's the answer...
...

All traces sent to Langfuse
Visit your Langfuse dashboard to view the traces
URL: https://cloud.langfuse.com
============================================================
```

### Step 10: View Your Traces in Langfuse Dashboard

1. Open your browser and go to [cloud.langfuse.com](https://cloud.langfuse.com)
2. Navigate to your project
3. Click on **Traces** in the left sidebar
4. You should see your first traces appearing!

**What to look for:**
- Trace name: `rag_pipeline`
- Nested observations: `retrieve_context` and `generate_response`
- Metadata: user_id, session_id, tags
- Timing and cost information

---

## Exploring All Examples

### Available Examples

| Example | File | What It Demonstrates | Runtime |
|---------|------|---------------------|---------|
| **1. Basic Tracing** | `01_basic_tracing.py` | Decorators, nested traces, metadata | ~10 sec |
| **2. OpenAI Integration** | `02_openai_integration.py` | Drop-in wrapper, streaming, functions | ~30 sec |
| **3. Prompt Management** | `03_prompt_management.py` | Versioning, templates, compilation | ~15 sec |
| **4. Dataset Evaluation** | `04_dataset_evaluation.py` | Test creation, experiments, scoring | ~20 sec |
| **5. LangChain Integration** | `05_langchain_integration.py` | Callbacks, chains, RAG | ~25 sec |
| **6. Production RAG** | `06_production_rag_system.py` | Quality checks, hallucination detection | ~40 sec |
| **7. Monitoring** | `07_monitoring_alerting.py` | Metrics, alerts, cost analysis | ~15 sec |

### Run All Examples Interactively

```bash
# Run the interactive script
./scripts/run_all_examples.sh
```

This script will:
- Run each example in sequence
- Wait for your confirmation between examples
- Show you what each example does

### Run Individual Examples

```bash
# Example 2: OpenAI Integration
python examples/02_openai_integration.py

# Example 3: Prompt Management
python examples/03_prompt_management.py

# Example 6: Production RAG System
python examples/06_production_rag_system.py
```

---

## Understanding the Results

### In Your Terminal

Each example outputs:
- What operations are being performed
- Any generated responses
- Confirmation that traces were sent
- Link to view in dashboard

### In Langfuse Dashboard

Navigate through different views:

1. **Traces View**
   - Click on any trace to see details
   - Expand nested observations
   - View input/output
   - Check timing and costs

2. **Sessions View**
   - See multi-turn conversations
   - Track user interactions
   - Analyze session-level metrics

3. **Users View**
   - See activity by user
   - Track costs per user
   - View user-specific traces

4. **Metrics View**
   - Overall statistics
   - Cost trends
   - Token usage
   - Error rates

### Key Metrics to Watch

- **Total Traces**: Number of executions
- **Total Cost**: Cumulative LLM costs
- **Average Latency**: Response times
- **Error Rate**: Failed requests
- **Token Usage**: Input + output tokens

---

## Next Steps

### Option 1: Explore Datasets

```bash
# View the evaluation datasets
cat datasets/qa_evaluation_dataset.csv
cat datasets/hallucination_test_cases.csv
cat datasets/rag_benchmark_queries.csv
```

**Use these to:**
- Create your own evaluation tests
- Build quality benchmarks
- Test for hallucinations

### Option 2: Customize Prompts

```bash
# View prompt templates
cat prompts/customer_support.json
cat prompts/rag_prompts.json
cat prompts/agent_prompts.json
```

**Modify these for:**
- Your specific use case
- Different customer tiers
- Custom agent behaviors

### Option 3: Analyze Costs

```bash
# Run cost analysis
python scripts/analyze_costs.py --days 7
```

### Option 4: Export Traces

```bash
# Export your traces
python scripts/export_traces.py --days 7 --output my_traces.json
```

### Option 5: Try Docker Deployment

```bash
# Build and run with Docker
docker-compose up langfuse-app
```

### Option 6: Read Documentation

Recommended reading order:

1. **QUICKSTART.md** - 5-minute guide (you're beyond this now!)
2. **README.md** - Complete pilot guide
3. **PRODUCT_OVERVIEW.md** - Executive overview with diagrams
4. **TECHNICAL_DOCUMENTATION.md** - Deep technical reference
5. **docs/BEST_PRACTICES.md** - Production best practices
6. **docs/PRODUCTION_DEPLOYMENT.md** - Deployment guide

---

## Troubleshooting

### Problem: "Connection failed" when testing configuration

**Solution:**
```bash
# Check your .env file
cat .env | grep LANGFUSE

# Verify keys are correct (no extra spaces)
# Ensure you're using the right host for your region
# US: https://us.cloud.langfuse.com
# EU: https://cloud.langfuse.com
```

### Problem: "ModuleNotFoundError: No module named 'langfuse'"

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Problem: "openai.AuthenticationError"

**Solution:**
```bash
# Check your OpenAI API key
echo $OPENAI_API_KEY

# Verify it's set in .env
cat .env | grep OPENAI_API_KEY

# Make sure you're loading the .env file
# The examples use python-dotenv to load it automatically
```

### Problem: "Traces not appearing in dashboard"

**Solution:**
1. Check that examples ran without errors
2. Wait 5-10 seconds for ingestion
3. Refresh the Langfuse dashboard
4. Verify you're looking at the correct project
5. Check the date filter (should include today)

### Problem: "Rate limit exceeded"

**Solution:**
```bash
# You're on OpenAI's free tier with rate limits
# Wait a few minutes between runs
# Or upgrade your OpenAI plan
```

### Problem: Examples run but show errors

**Solution:**
```bash
# Check Python version
python3 --version  # Should be 3.9+

# Update dependencies
pip install --upgrade langfuse openai python-dotenv

# Clear any cached files
find . -type d -name __pycache__ -exec rm -r {} +
```

### Getting Help

If you're still stuck:

1. **Check Documentation**
   - Read QUICKSTART.md
   - Review README.md
   - Check TECHNICAL_DOCUMENTATION.md

2. **Langfuse Resources**
   - Docs: https://langfuse.com/docs
   - Discord: https://discord.gg/langfuse
   - GitHub Issues: https://github.com/langfuse/langfuse/issues

3. **OpenAI Resources**
   - Docs: https://platform.openai.com/docs
   - Help: https://help.openai.com

---

## Quick Reference

### Common Commands

```bash
# Activate environment
source venv/bin/activate

# Run an example
python examples/01_basic_tracing.py

# Run all examples
./scripts/run_all_examples.sh

# Analyze costs
python scripts/analyze_costs.py --days 7

# Export traces
python scripts/export_traces.py --output traces.json

# Deactivate environment
deactivate
```

### File Locations

```
Configuration:    .env
Examples:         examples/
Prompts:          prompts/
Datasets:         datasets/
Scripts:          scripts/
Documentation:    *.md files
```

### Environment Variables

```bash
LANGFUSE_SECRET_KEY    # Your Langfuse secret key
LANGFUSE_PUBLIC_KEY    # Your Langfuse public key
LANGFUSE_HOST          # Langfuse instance URL
OPENAI_API_KEY         # Your OpenAI API key
LANGFUSE_ENVIRONMENT   # development/staging/production
```

---

## Success Checklist

After completing this guide, you should have:

- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] .env file configured with API keys
- [ ] Successfully run at least one example
- [ ] Viewed traces in Langfuse dashboard
- [ ] Understanding of what each example does
- [ ] Knowledge of where to find documentation

---

## What's Next?

### Beginner Path (Week 1)
1. Run all 7 examples
2. Explore Langfuse dashboard features
3. Review provided datasets
4. Read PRODUCT_OVERVIEW.md

### Intermediate Path (Week 2)
1. Create your own prompt templates
2. Build a custom evaluation dataset
3. Integrate Langfuse into a simple app
4. Read TECHNICAL_DOCUMENTATION.md

### Advanced Path (Week 3-4)
1. Deploy with Docker
2. Set up CI/CD pipeline
3. Implement production monitoring
4. Read docs/PRODUCTION_DEPLOYMENT.md

### Production Path (Month 1-2)
1. Integrate with your production LLM app
2. Set up multi-environment deployment
3. Configure alerting and monitoring
4. Establish evaluation workflows
5. Train your team

---

## Summary

You've now:
1. Set up the Langfuse POC environment
2. Configured your API keys
3. Run your first trace example
4. Learned how to view results
5. Know how to explore further

**Total time**: ~15 minutes

**Next immediate action**: Run another example or explore the dashboard!

---

**Need Help?** Reference this guide anytime, or check the other documentation files in this repository.

**Ready for More?** Check out QUICKSTART.md, README.md, or jump into the advanced examples!

