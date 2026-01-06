# Langfuse Best Practices

## Tracing Best Practices

### 1. Use Semantic Observation Types

Always use the appropriate observation type:

```python
# Good
@observe(as_type="generation")  # LLM call
def generate_response(prompt):
    ...

@observe(as_type="retriever")  # Vector DB retrieval
def retrieve_context(query):
    ...

@observe(as_type="tool")  # Tool/function call
def calculate(expression):
    ...

# Avoid
@observe()  # Generic - harder to analyze
```

### 2. Add Rich Metadata

```python
from langfuse.decorators import observe, langfuse_context

@observe()
def process_request(user_id, request_type):
    langfuse_context.update_current_trace(
        user_id=user_id,
        session_id=f"session-{user_id}",
        tags=[request_type, "production"],
        metadata={
            "request_type": request_type,
            "source": "api",
            "version": "v2.1"
        }
    )
```

### 3. Implement Proper Session Tracking

```python
# Multi-turn conversation
session_id = generate_session_id()

for turn in conversation:
    @observe()
    def handle_turn(message):
        langfuse_context.update_current_trace(
            session_id=session_id,  # Links all turns
            metadata={"turn": turn["number"]}
        )
```

### 4. Always Flush in Short-Lived Applications

```python
from langfuse import get_client

def lambda_handler(event, context):
    # Process event
    result = process_event(event)
    
    # IMPORTANT: Flush before exit
    get_client().flush()
    
    return result
```

## Prompt Management Best Practices

### 1. Version Control Strategy

```
production  -> Stable version in production
staging     -> Testing in staging environment
development -> Active development
v1.0, v2.0  -> Explicit version tags
```

### 2. Template Variable Naming

```python
# Good: Clear, descriptive names
prompt = """
Customer tier: {{customer_tier}}
Question: {{customer_question}}
Context: {{retrieved_context}}
"""

# Avoid: Generic names
prompt = """
Data: {{data1}}
Info: {{info}}
Stuff: {{x}}
"""
```

### 3. Configuration Management

Store model config with prompts:

```python
langfuse.create_prompt(
    name="customer-support",
    prompt="...",
    config={
        "model": "gpt-4o-mini",
        "temperature": 0.7,
        "max_tokens": 300
    },
    labels=["production"]
)
```

## Evaluation Best Practices

### 1. Combine Online and Offline Evaluation

```python
# Offline: Pre-deployment testing
dataset = langfuse.get_dataset("qa-test")
for item in dataset.items:
    result = qa_system(item.input)
    evaluate(result, item.expected_output)

# Online: Production monitoring
@observe()
def handle_request(query):
    result = qa_system(query)
    
    # Collect user feedback
    if user_feedback:
        langfuse.score(
            trace_id=trace_id,
            name="user_feedback",
            value=user_feedback
        )
    
    return result
```

### 2. Use Multiple Evaluation Metrics

```python
# Quality
langfuse.score(trace_id, "accuracy", 0.9)

# Performance
langfuse.score(trace_id, "latency", 1250, comment="ms")

# Cost
langfuse.score(trace_id, "cost_efficiency", 0.8)

# User satisfaction
langfuse.score(trace_id, "user_rating", 5, comment="5-star")
```

### 3. Automated Evaluation Pipeline

```python
from langfuse.decorators import observe

@observe()
def automated_evaluation(trace_id, output, expected):
    # Accuracy check
    accuracy = check_accuracy(output, expected)
    
    # Hallucination check
    hallucination = check_hallucination(output)
    
    # Relevance check
    relevance = check_relevance(output)
    
    # Submit scores
    langfuse.score(trace_id, "accuracy", accuracy)
    langfuse.score(trace_id, "hallucination", hallucination)
    langfuse.score(trace_id, "relevance", relevance)
```

## Cost Optimization

### 1. Model Selection Strategy

```python
def select_model(query_complexity):
    if query_complexity == "simple":
        return "gpt-4o-mini"  # Cheaper
    elif query_complexity == "medium":
        return "gpt-4o"
    else:
        return "gpt-4o"  # For complex tasks
```

### 2. Prompt Caching

```python
# Cache frequently used prompts
langfuse = Langfuse(prompt_cache_ttl=3600)

# Reuse compiled prompts
prompt = langfuse.get_prompt("customer-support")
compiled = prompt.compile(vars)  # Cached
```

### 3. Token Optimization

```python
# Track token usage
langfuse_context.update_current_observation(
    usage={
        "input": input_tokens,
        "output": output_tokens,
        "total": total_tokens
    }
)

# Set reasonable max_tokens
openai.chat.completions.create(
    max_tokens=300,  # Don't over-allocate
    ...
)
```

## Security Best Practices

### 1. Environment-Based Configuration

```python
import os

env = os.getenv('ENVIRONMENT', 'development')

if env == 'production':
    # Production settings
    debug = False
    flush_interval = 5000
else:
    # Development settings
    debug = True
    flush_interval = 1000
```

### 2. Data Sanitization

```python
def sanitize_for_tracing(data):
    """Remove sensitive data before tracing."""
    if isinstance(data, dict):
        return {
            k: "[REDACTED]" if k in ['password', 'api_key', 'token'] else v
            for k, v in data.items()
        }
    return data
```

### 3. Access Control

```python
# Use read-only keys for client-side
# Use full keys only on backend

# Backend
LANGFUSE_SECRET_KEY = os.getenv('LANGFUSE_SECRET_KEY')

# Frontend (if needed)
LANGFUSE_PUBLIC_KEY = os.getenv('LANGFUSE_PUBLIC_KEY')  # Read-only
```

## Performance Best Practices

### 1. Minimize Overhead

```python
# Langfuse adds <10ms overhead
# Further optimization:

# Use async where possible
import asyncio

@observe()
async def async_process(data):
    result = await async_llm_call(data)
    return result

# Batch operations
results = await asyncio.gather(
    async_process(data1),
    async_process(data2),
    async_process(data3)
)
```

### 2. Sampling for High Volume

```python
import random

@observe()
def high_volume_endpoint(request):
    # Sample 1% of traces
    if random.random() < 0.01:
        # Full tracing enabled
        return process_with_tracing(request)
    else:
        # No tracing for this request
        return process_without_tracing(request)
```

## Team Collaboration

### 1. Naming Conventions

```
Traces:     feature-name-operation (e.g., "chat-message-generation")
Sessions:   session-{user_id}-{timestamp}
Tags:       [environment, feature, version]
Metadata:   {descriptive_key: value}
```

### 2. Documentation

Document your traces:

```python
@observe()
def complex_operation(data):
    """
    Complex multi-step operation.
    
    Trace includes:
    - Data retrieval (retriever observation)
    - Processing (span observation)
    - LLM generation (generation observation)
    - Quality check (evaluator observation)
    """
    ...
```

### 3. Review Workflows

- Weekly: Review low-scoring traces
- Monthly: Analyze cost trends
- Quarterly: Audit prompt versions
- Annually: Security review

## Common Pitfalls to Avoid

1. **Not calling flush() in scripts**
   - Always call `get_client().flush()` before exit

2. **Overly generic trace names**
   - Use descriptive names: "chat-completion" not "process"

3. **Missing user/session IDs**
   - Always set these for proper analytics

4. **Hardcoding API keys**
   - Use environment variables

5. **Not setting observation types**
   - Use semantic types (generation, retriever, etc.)

6. **Ignoring errors**
   - Implement proper error handling and logging

7. **Not testing in staging**
   - Always test traces in staging first

8. **Forgetting to update prompt labels**
   - Update production label when deploying

9. **Not monitoring costs**
   - Set up cost alerts early

10. **Mixing environments**
    - Use separate projects for dev/staging/prod

