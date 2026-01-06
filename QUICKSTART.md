# Quick Start Guide

Get up and running with the Langfuse pilot in 5 minutes!

## Prerequisites Check

Before starting, ensure you have:
- Python 3.8+ or Node.js 18+ installed
- A Langfuse account (free at https://cloud.langfuse.com)
- An OpenAI API key (optional, for full examples)

## Step 1: Get Your Langfuse API Keys

1. **Sign up** at https://cloud.langfuse.com
2. **Create a project** (or use default project)
3. **Navigate to Settings > API Keys**
4. **Copy your keys:**
   - Public Key (pk-lf-...)
   - Secret Key (sk-lf-...)

Keep these handy for the next step.

## Step 2: Configure Environment

Create a `.env` file in the project root:

```bash
cd /Users/girijesh/Documents/langfuse_poc
cp .env.example .env
```

Edit `.env` and add your keys:

```bash
# Required: Langfuse credentials
LANGFUSE_PUBLIC_KEY=pk-lf-your-key-here
LANGFUSE_SECRET_KEY=sk-lf-your-key-here
LANGFUSE_HOST=https://cloud.langfuse.com

# Optional: For OpenAI examples
OPENAI_API_KEY=sk-your-openai-key-here
```

## Step 3: Install Dependencies

Choose your path:

### Python Path (Recommended for beginners)

```bash
pip install -r requirements.txt
```

### Node.js Path

```bash
npm install
```

### Quick Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

The script will:
- Install Python and Node.js dependencies
- Verify environment setup
- Run connectivity tests

## Step 4: Run Your First Trace

Run the basic tracing example:

```bash
python examples/01_basic_tracing.py
```

You should see output like:
```
============================================================
Langfuse Example 1: Basic Tracing
============================================================

Processing query: What is Langfuse?
Retrieving context for: What is Langfuse?
Generating response for: What is Langfuse?
Pipeline completed successfully
View trace in Langfuse dashboard

Result: Based on the context, here's the answer: What is Langfuse? relates to our knowledge base...

============================================================
All traces sent to Langfuse
Visit your Langfuse dashboard to view the traces
URL: https://cloud.langfuse.com
============================================================
```

## Step 5: View Your Trace in Langfuse

1. **Open** https://cloud.langfuse.com
2. **Go to Traces** in the left sidebar
3. **Click on the latest trace** (should appear within 5-10 seconds)

You'll see:
- Timeline visualization of the entire workflow
- Individual operations (retrieve context, generate response)
- Metadata and tags
- Nested spans showing parent-child relationships

## Understanding Your First Trace

### What You're Looking At

**Trace Overview:**
- Name: "rag_pipeline"
- User ID: "user-123"
- Session ID: "session-456"
- Tags: ["rag", "production"]

**Nested Observations:**
```
rag_pipeline (parent)
├── retrieve_context (child span)
└── generate_response (child span)
```

**Key Insights:**
- Total execution time
- Number of operations
- Metadata at each step
- Complete input/output data

### Trace Details Panel

Click on individual operations to see:
- **Input/Output**: Exact data passed and returned
- **Metadata**: Custom key-value pairs
- **Timing**: Start time, end time, duration
- **Status**: Success, error, or pending

## Running More Examples

### Example 2: OpenAI Integration (Requires OpenAI API Key)

```bash
python examples/02_openai_integration.py
```

**Cost**: ~$0.02 | **Time**: 2 minutes

**What you'll see:**
- Automatic token counting
- Cost calculations
- Model comparison
- Streaming traces

**In Dashboard:**
- Go to "Generations" view
- See all OpenAI API calls
- Token usage and costs
- Response times

### Example 3: Prompt Management

```bash
python examples/03_prompt_management.py
```

**Cost**: ~$0.02 | **Time**: 2 minutes

**What you'll see:**
- Centralized prompt storage
- Version management
- Runtime prompt fetching
- A/B testing

**In Dashboard:**
- Go to "Prompts" view
- See prompt versions
- Edit prompts without code changes
- Track usage by version

### Example 4: Dataset Evaluation

```bash
python examples/04_dataset_evaluation.py
```

**Cost**: ~$0.05 | **Time**: 3 minutes

**What you'll see:**
- Batch evaluation
- Custom scoring
- Quality metrics
- Pass/fail analysis

**In Dashboard:**
- Go to "Datasets" view
- See evaluation results
- Score distributions
- Compare across runs

## Customization Quick Wins

### 1. Add Your Own Trace

Create `my_example.py`:

```python
from langfuse.decorators import observe, langfuse_context
from dotenv import load_dotenv

load_dotenv()

@observe()
def my_function(input_text):
    """Your custom function."""
    # Add metadata
    langfuse_context.update_current_observation(
        metadata={"custom_field": "custom_value"}
    )

    # Your logic here
    result = f"Processed: {input_text}"

    return result

@observe()
def main():
    result = my_function("Hello Langfuse!")
    print(result)

if __name__ == "__main__":
    main()

    # Flush to send traces
    from langfuse import get_client
    get_client().flush()
```

Run it:
```bash
python my_example.py
```

View in dashboard immediately!

### 2. Add User Context

Update any example to track users:

```python
langfuse_context.update_current_trace(
    user_id="your-user-id",
    session_id="your-session-id",
    tags=["custom-tag"]
)
```

Filter by user in dashboard: Traces > Filter by User ID

### 3. Track Custom Metrics

Add scores to traces:

```python
from langfuse import get_client

client = get_client()
client.score(
    trace_id="trace-id",
    name="quality",
    value=0.95,  # 0-1 scale
    comment="Excellent response"
)
```

View in: Traces > Scores column

### 4. Monitor Costs

For OpenAI calls, costs are automatic:

```python
from langfuse.openai import openai

# This automatically tracks costs
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello"}]
)
```

View in: Generations > Cost column

## Cost Estimates

Running the full pilot:

| Component | Cost | Details |
|-----------|------|---------|
| **Langfuse Platform** | FREE | Up to 50k observations/month |
| **Example 1** | $0.00 | No API calls |
| **Example 2** | $0.02 | 10 OpenAI calls (GPT-4o-mini) |
| **Example 3** | $0.02 | 8 OpenAI calls |
| **Example 4** | $0.05 | 20 evaluation calls |
| **Total** | **~$0.09** | **All examples once** |

**Cost Optimization Tips:**
- Use GPT-4o-mini instead of GPT-4 (80% cheaper)
- Enable caching for repeated calls
- Set token limits on responses
- Use local models for development (free)

## Troubleshooting

### Traces Not Appearing

**Check 1**: Wait 5-10 seconds for processing

**Check 2**: Verify API keys
```bash
# Print first few characters (safe)
echo $LANGFUSE_PUBLIC_KEY | cut -c1-10
# Should show: pk-lf-...
```

**Check 3**: Ensure flush is called
```python
from langfuse import get_client
get_client().flush()
```

**Check 4**: Check the correct project
- Dashboard > Project Selector (top right)
- Ensure you're viewing the right project

### API Key Errors

**Error**: "Invalid API keys"

**Solution**:
```bash
# Re-copy keys from dashboard
# Ensure no extra spaces or newlines
# Check quotes are not included in .env file
```

**Verify**:
```python
import os
from dotenv import load_dotenv

load_dotenv()
print(f"Public Key: {os.getenv('LANGFUSE_PUBLIC_KEY')[:15]}...")
print(f"Secret Key: {os.getenv('LANGFUSE_SECRET_KEY')[:15]}...")
print(f"Host: {os.getenv('LANGFUSE_HOST')}")
```

### Module Not Found

**Error**: "No module named 'langfuse'"

**Solution**:
```bash
pip install langfuse --upgrade
```

**For OpenAI errors**:
```bash
pip install openai --upgrade
```

**Verify installation**:
```bash
python -c "import langfuse; print(langfuse.__version__)"
```

### OpenAI API Errors

**Error**: "Incorrect API key provided"

**Solution**:
- Check `OPENAI_API_KEY` in `.env`
- Get new key: https://platform.openai.com/api-keys
- Ensure key has credits: https://platform.openai.com/usage

**Error**: "Rate limit exceeded"

**Solution**:
- Wait a few minutes
- Upgrade OpenAI plan
- Reduce parallel requests

### Network/Connection Issues

**Error**: "Connection timeout"

**Solution**:
- Check internet connectivity
- Verify firewall allows HTTPS to langfuse.com
- Try with VPN disabled (some VPNs block)
- Check Langfuse status: https://status.langfuse.com

### Script Exits Before Sending Traces

**Problem**: Script finishes but no traces appear

**Solution**: Always call flush before exit
```python
if __name__ == "__main__":
    main()

    # Critical: flush before exit
    from langfuse import get_client
    get_client().flush()
```

## Understanding Dashboard Views

### Traces View

**What**: All execution flows

**Use for**:
- Debugging workflows
- Finding slow operations
- Viewing user sessions
- Error investigation

**Filters**:
- User ID
- Session ID
- Tags
- Time range
- Name

### Generations View

**What**: All LLM API calls

**Use for**:
- Cost monitoring
- Token usage analysis
- Model performance
- Latency tracking

**Metrics**:
- Tokens (input/output)
- Cost (calculated)
- Latency (ms)
- Model used

### Prompts View

**What**: Managed prompt templates

**Use for**:
- Prompt versioning
- A/B testing
- Team collaboration
- Performance tracking

**Features**:
- Version history
- Usage statistics
- Edit in-place
- Rollback capability

### Datasets View

**What**: Evaluation test cases

**Use for**:
- Quality testing
- Regression detection
- Model comparison
- Continuous evaluation

**Components**:
- Test cases
- Ground truth
- Scores
- Run history

## Next Steps

After completing the quick start:

**Level 1: Exploration (10 min)**
- Run all examples
- Explore dashboard views
- Try filtering and searching
- Review trace details

**Level 2: Customization (30 min)**
- Create your own traced function
- Add custom metadata
- Track user sessions
- Implement scoring

**Level 3: Integration (1-2 hours)**
- Integrate with your app
- Set up prompt management
- Create evaluation datasets
- Configure dashboards

**Level 4: Production (ongoing)**
- Deploy with tracing enabled
- Monitor costs and quality
- Set up alerts
- Optimize based on metrics

## Quick Reference

### Environment Variables
```bash
LANGFUSE_PUBLIC_KEY=pk-lf-...      # From dashboard
LANGFUSE_SECRET_KEY=sk-lf-...      # From dashboard
LANGFUSE_HOST=https://cloud.langfuse.com
OPENAI_API_KEY=sk-...              # From OpenAI
```

### Basic Tracing
```python
from langfuse.decorators import observe

@observe()
def my_function():
    return "result"
```

### Update Trace
```python
from langfuse.decorators import langfuse_context

langfuse_context.update_current_trace(
    user_id="user-123",
    session_id="session-456",
    tags=["tag1", "tag2"]
)
```

### OpenAI Integration
```python
from langfuse.openai import openai

response = openai.chat.completions.create(...)
```

### Flush Traces
```python
from langfuse import get_client
get_client().flush()
```

## Useful Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run all examples
python examples/01_basic_tracing.py
python examples/02_openai_integration.py
python examples/03_prompt_management.py
python examples/04_dataset_evaluation.py

# Check version
python -c "import langfuse; print(langfuse.__version__)"

# Update SDK
pip install langfuse --upgrade

# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
```

## Need Help?

**Documentation**: https://langfuse.com/docs
**Discord Community**: https://discord.langfuse.com
**GitHub Issues**: https://github.com/langfuse/langfuse/issues
**Email Support**: support@langfuse.com (enterprise)

**This Pilot**: Check README.md for detailed documentation

---

**Ready to start?** Run `python examples/01_basic_tracing.py` now and view your first trace!
