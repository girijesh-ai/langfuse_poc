# Langfuse Pilot Project

This is a comprehensive pilot project demonstrating [Langfuse](https://langfuse.com/), an open-source LLM engineering platform for tracing, evaluating, and monitoring AI applications.

## What is Langfuse?

Langfuse is an observability and engineering platform that helps:
- Trace and debug LLM application execution with detailed telemetry
- Manage and version prompts centrally across your organization
- Evaluate LLM outputs with datasets and custom scoring metrics
- Monitor production usage, costs, and quality metrics in real-time
- Collaborate on prompt engineering with built-in experimentation tools
- Integrate seamlessly with popular LLM frameworks and providers

## Project Structure

```
langfuse_poc/
├── examples/                          # Example implementations
│   ├── 01_basic_tracing.py           # Basic tracing with @observe decorator
│   ├── 02_openai_integration.py      # OpenAI SDK integration
│   ├── 03_prompt_management.py       # Prompt versioning and management
│   └── 04_dataset_evaluation.py      # Dataset-based evaluation
├── prompts/                           # Prompt templates
├── datasets/                          # Evaluation datasets
├── configs/                           # Configuration files
├── scripts/                           # Utility scripts
├── docs/                             # Additional documentation
├── .env.example                       # Environment variables template
├── requirements.txt                   # Python dependencies
├── package.json                       # Node.js dependencies
├── setup.sh                          # Quick setup script
└── README.md                         # This file
```

## Prerequisites

- **Python 3.8+** or **Node.js 18+** (depending on examples you want to run)
- **Langfuse Account** (free tier available at https://cloud.langfuse.com)
- **OpenAI API Key** (for examples using OpenAI models)

## Setup

### 1. Clone or Navigate to This Directory

```bash
cd /Users/girijesh/Documents/langfuse_poc
```

### 2. Set Up Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your credentials:
```bash
# Langfuse Configuration
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com  # or your self-hosted URL

# OpenAI Configuration (for examples)
OPENAI_API_KEY=sk-...
```

Get your Langfuse keys:
1. Sign up at https://cloud.langfuse.com
2. Create a new project
3. Navigate to Settings > API Keys
4. Copy your public and secret keys

### 3. Install Dependencies

**For Python Examples:**
```bash
pip install -r requirements.txt
```

**For Node.js Examples:**
```bash
npm install
```

**Or use the setup script:**
```bash
chmod +x setup.sh
./setup.sh
```

## Running Examples

### Example 1: Basic Tracing

Demonstrates the core tracing capabilities using the `@observe()` decorator:

```bash
python examples/01_basic_tracing.py
```

**What it shows:**
- Automatic tracing with decorators
- Nested observations (parent-child relationships)
- Adding metadata and tags to traces
- Updating trace context dynamically
- User and session tracking

**Key Concepts:**
- **Trace**: Complete execution flow from start to finish
- **Observation**: Individual step or operation within a trace
- **Span**: Nested observation representing a function call
- **Generation**: LLM API call observation

### Example 2: OpenAI Integration

Shows native OpenAI SDK integration with Langfuse:

```bash
python examples/02_openai_integration.py
```

**What it shows:**
- Drop-in replacement for OpenAI client
- Automatic token counting and cost tracking
- Streaming response tracing
- Model comparison across different versions
- Production-ready error handling

**Key Features:**
- Zero-code instrumentation
- Automatic cost calculation
- Latency tracking
- Token usage monitoring

### Example 3: Prompt Management

Demonstrates centralized prompt management and versioning:

```bash
python examples/03_prompt_management.py
```

**What it shows:**
- Creating and versioning prompts in Langfuse
- Fetching prompts at runtime
- A/B testing different prompt versions
- Prompt variable substitution
- Linking prompts to traces

**Benefits:**
- Single source of truth for prompts
- Non-technical users can edit prompts
- Version control and rollback
- Experimentation tracking

### Example 4: Dataset Evaluation

Shows how to evaluate LLM outputs using datasets:

```bash
python examples/04_dataset_evaluation.py
```

**What it shows:**
- Creating evaluation datasets
- Running batch evaluations
- Custom scoring functions
- Performance metrics aggregation
- Quality comparison across models

**Use Cases:**
- Regression testing
- Model selection
- Quality benchmarking
- Continuous evaluation

## Understanding Results

### Langfuse Dashboard

After running examples, view results at https://cloud.langfuse.com:

**1. Traces View**
- Complete execution flow visualization
- Timing breakdown for each step
- Input/output inspection
- Error tracking and debugging

**2. Generations View**
- All LLM API calls
- Token usage and costs
- Model performance metrics
- Latency distribution

**3. Prompts View**
- All prompt versions
- Usage statistics
- Performance by version
- Collaborative editing

**4. Datasets View**
- Test cases and ground truth
- Evaluation results
- Score distributions
- Quality trends over time

### Key Metrics Tracked

**Performance Metrics:**
- **Latency**: Response time for each operation
- **Tokens**: Input/output token counts
- **Cost**: Calculated API costs (model-specific)
- **Throughput**: Requests per second

**Quality Metrics:**
- **Scores**: Custom evaluation scores (0-1 scale)
- **User Feedback**: Thumbs up/down from users
- **Error Rate**: Failed requests percentage
- **Model Performance**: Accuracy, relevance, safety

## Pilot Scenarios Demonstrated

### 1. Development Debugging

**Use Case**: Debug complex multi-step LLM workflows

**What you'll see:**
- Waterfall view of execution timeline
- Input/output at each step
- Metadata for debugging
- Error stack traces

**Try it**: Run Example 1 and inspect traces in dashboard

### 2. Cost Optimization

**Use Case**: Monitor and reduce API costs

**What you'll see:**
- Cost per request breakdown
- Token usage by model
- Expensive operations identification
- Cost trends over time

**Try it**: Run Example 2 with different models and compare costs

### 3. Prompt Engineering

**Use Case**: Iterate on prompts without code changes

**What you'll see:**
- Side-by-side prompt comparison
- Performance by prompt version
- A/B test results
- Rollback to previous versions

**Try it**: Run Example 3 and modify prompts in dashboard

### 4. Quality Assurance

**Use Case**: Ensure consistent quality across deployments

**What you'll see:**
- Automated evaluation results
- Pass/fail rates by test case
- Regression detection
- Quality score distributions

**Try it**: Run Example 4 and review evaluation dashboard

## Best Practices Demonstrated

### 1. Structured Tracing
```python
@observe()
def my_function():
    # Automatically creates a span
    langfuse_context.update_current_observation(
        metadata={"key": "value"}
    )
```

### 2. User Context Tracking
```python
langfuse_context.update_current_trace(
    user_id="user-123",
    session_id="session-456",
    tags=["production", "web"]
)
```

### 3. Cost-Aware Development
```python
# Costs are automatically tracked
# View in dashboard: Generations > Cost column
```

### 4. Prompt Versioning
```python
# Fetch prompts from Langfuse
prompt = langfuse.get_prompt("customer-support", version=2)

# Use in your application
response = openai.chat.completions.create(
    model="gpt-4",
    messages=prompt.compile(customer_name="John")
)
```

### 5. Evaluation-Driven Development
```python
# Create datasets for regression testing
# Run evaluations before deployment
# Track quality metrics over time
```

## Integration Patterns

### Pattern 1: Decorator-Based (Python)
```python
from langfuse.decorators import observe

@observe()
def process_request(input):
    return result
```

### Pattern 2: SDK Integration (OpenAI)
```python
from langfuse.openai import openai

# Drop-in replacement
response = openai.chat.completions.create(...)
```

### Pattern 3: Manual Instrumentation
```python
from langfuse import Langfuse

langfuse = Langfuse()
trace = langfuse.trace(name="my-trace")
span = trace.span(name="my-operation")
span.end(output=result)
```

### Pattern 4: OpenTelemetry
```python
# Use standard OpenTelemetry instrumentation
# Langfuse acts as OTLP endpoint
```

## Next Steps

### 1. Customize Examples

**Add Your Own Use Case:**
- Copy an example file
- Modify prompts and logic
- Run and view in dashboard
- Iterate based on metrics

### 2. Integrate with Your Application

**Python Application:**
```python
pip install langfuse
# Add @observe() decorators to key functions
```

**Node.js Application:**
```bash
npm install langfuse
# Import and instrument your code
```

### 3. Set Up Prompt Management

1. Create prompts in Langfuse UI
2. Replace hardcoded prompts with `langfuse.get_prompt()`
3. Iterate in UI without code changes
4. Version and track performance

### 4. Create Evaluation Datasets

1. Define test cases in Langfuse
2. Add ground truth answers
3. Create scoring functions
4. Run automated evaluations

### 5. Production Deployment

**Add to CI/CD:**
```yaml
# Run evaluations before deploy
- name: LLM Quality Tests
  run: python run_evaluations.py
```

**Monitor in Production:**
- Set up alerts for cost/latency
- Track user feedback scores
- Monitor error rates
- Review traces for issues

## Common Use Cases

### Customer Support Chatbots
- Trace conversation flows
- Monitor response quality
- Track resolution rates
- Optimize for cost and speed

### RAG Applications
- Debug retrieval quality
- Monitor context relevance
- Evaluate answer accuracy
- Track hallucination rates

### Content Generation
- Compare model outputs
- Version control prompts
- Batch evaluate quality
- Monitor production diversity

### Agent Workflows
- Visualize decision trees
- Debug tool usage
- Track multi-step reasoning
- Optimize agent performance

## Cost Estimates

Running all examples (with OpenAI GPT-4o-mini):

| Example | Traces | API Calls | Est. Cost | Time |
|---------|--------|-----------|-----------|------|
| Basic Tracing | 3 | 0 | $0.00 | 1 min |
| OpenAI Integration | 5 | 10 | $0.02 | 2 min |
| Prompt Management | 4 | 8 | $0.02 | 2 min |
| Dataset Evaluation | 1 | 20 | $0.05 | 3 min |
| **Total** | **13** | **38** | **~$0.09** | **8 min** |

**Note**: Langfuse is free for up to 50k observations/month on the cloud tier.

## Troubleshooting

### Issue: "Invalid API keys"
**Solution**:
- Verify keys in `.env` file
- Check keys in Langfuse dashboard (Settings > API Keys)
- Ensure no extra spaces or quotes

### Issue: "Traces not appearing in dashboard"
**Solution**:
- Wait 5-10 seconds for processing
- Check the correct project is selected
- Call `langfuse.flush()` before script exits
- Verify internet connectivity

### Issue: "Module not found" errors
**Solution**:
```bash
# Python
pip install -r requirements.txt --upgrade

# Node.js
npm install
```

### Issue: OpenAI API errors
**Solution**:
- Verify `OPENAI_API_KEY` is set
- Check API key has credits
- Review OpenAI status page

### Issue: High latency in tracing
**Solution**:
- Tracing is async and shouldn't add latency
- Check network connectivity
- Consider self-hosting for lower latency
- Use SDK caching features

## Useful Commands

```bash
# Run all Python examples
for example in examples/*.py; do python "$example"; done

# View environment variables
cat .env

# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +

# Update dependencies
pip install --upgrade langfuse openai

# Check Langfuse SDK version
python -c "import langfuse; print(langfuse.__version__)"
```

## Resources

**Official Documentation:**
- [Langfuse Docs](https://langfuse.com/docs)
- [API Reference](https://langfuse.com/docs/api)
- [Python SDK](https://langfuse.com/docs/sdk/python)
- [Node.js SDK](https://langfuse.com/docs/sdk/typescript-node)

**Integration Guides:**
- [OpenAI](https://langfuse.com/docs/integrations/openai)
- [LangChain](https://langfuse.com/docs/integrations/langchain)
- [LlamaIndex](https://langfuse.com/docs/integrations/llama-index)
- [Anthropic](https://langfuse.com/docs/integrations/anthropic)

**Advanced Topics:**
- [Self-Hosting](https://langfuse.com/docs/deployment/self-host)
- [Prompt Management](https://langfuse.com/docs/prompts)
- [Datasets & Evaluations](https://langfuse.com/docs/datasets)
- [Scores & Metrics](https://langfuse.com/docs/scores)

**Community:**
- [GitHub](https://github.com/langfuse/langfuse)
- [Discord](https://discord.langfuse.com)
- [Twitter](https://twitter.com/langfuse)

## Architecture Overview

Langfuse operates on a client-server architecture:

**Client Side (Your Application):**
- Lightweight SDK (Python, Node.js, etc.)
- Async data transmission
- Automatic batching and retry logic
- Minimal performance overhead

**Server Side (Langfuse Platform):**
- Cloud-hosted or self-hosted
- Real-time data processing
- Web dashboard for visualization
- REST API for programmatic access

**Data Flow:**
1. SDK instruments your code
2. Telemetry sent to Langfuse server
3. Data processed and stored
4. Available immediately in dashboard
5. Queryable via API

## Security & Privacy

**Data Security:**
- TLS encryption in transit
- API key authentication
- Project-based isolation
- Role-based access control

**Privacy Options:**
- Self-hosting available (full control)
- Cloud hosting in EU/US regions
- Data retention policies configurable
- PII scrubbing capabilities

**Best Practices:**
- Rotate API keys regularly
- Use environment variables (never hardcode)
- Implement rate limiting
- Monitor access logs

## Contributing to This Pilot

Feel free to extend this pilot by:
- Adding new example use cases
- Testing different LLM providers
- Creating custom evaluation metrics
- Implementing production patterns
- Documenting best practices
- Sharing results with team

## Comparison with Alternatives

| Feature | Langfuse | Weights & Biases | LangSmith | Phoenix |
|---------|----------|------------------|-----------|---------|
| Open Source | Yes | Partial | No | Yes |
| Self-Hosting | Yes | No | No | Yes |
| Prompt Management | Yes | No | Yes | No |
| LLM Tracing | Yes | Yes | Yes | Yes |
| Evaluations | Yes | Yes | Yes | Limited |
| Cost Tracking | Yes | Limited | Yes | No |
| Free Tier | 50k obs/mo | Limited | Limited | Unlimited |
| Multi-Provider | Yes | Yes | Limited | Yes |

## License

This pilot project is for educational and demonstration purposes. Langfuse is licensed under MIT (open source).

## Support

For questions about this pilot:
- Review the documentation in `docs/`
- Check example code comments
- Review Langfuse official docs

For Langfuse platform support:
- Documentation: https://langfuse.com/docs
- Discord Community: https://discord.langfuse.com
- GitHub Issues: https://github.com/langfuse/langfuse/issues
- Email: support@langfuse.com (enterprise)

---

**Happy Observing!** Start with Example 1 and explore the Langfuse dashboard to see the power of LLM observability.
