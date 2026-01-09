# Langfuse Python SDK v3 API Changes

This document summarizes the key API changes in SDK v3 that affected this codebase.

## Key Changes

### 1. Observation Update Methods

**❌ REMOVED in v3:**
```python
langfuse.update_current_observation()  # Does not exist in v3
```

**✅ NEW in v3:**
```python
# For span-type observations (default @observe() or span subtypes)
langfuse.update_current_span(
    input=...,
    output=...,
    metadata={...}
)

# For generation-type observations (@observe(as_type="generation"))
langfuse.update_current_generation(
    input=...,
    output=...,
    metadata={...}
)

# For trace-level updates (unchanged)
langfuse.update_current_trace(
    user_id=...,
    session_id=...,
    tags=[...],
    metadata={...}
)
```

### 2. Observation Types and Methods

| Decorator Type | Update Method |
|---------------|---------------|
| `@observe()` (default) | `update_current_span()` |
| `@observe(as_type="span")` | `update_current_span()` |
| `@observe(as_type="generation")` | `update_current_generation()` |
| `@observe(as_type="retriever")` | `update_current_span()` (span subtype) |
| `@observe(as_type="evaluator")` | `update_current_span()` (span subtype) |
| `@observe(as_type="tool")` | `update_current_span()` (span subtype) |
| `@observe(as_type="chain")` | `update_current_span()` (span subtype) |
| `@observe(as_type="agent")` | `update_current_span()` (span subtype) |
| `@observe(as_type="embedding")` | `update_current_generation()` (generation subtype) |

### 3. Resource Cleanup

**❌ OLD (v2):**
```python
get_client().flush()
```

**✅ NEW (v3):**
```python
get_client().shutdown()  # Ensures proper resource cleanup and data upload
```

### 4. Import Changes

**❌ OLD (v2):**
```python
from langfuse.decorators import observe, langfuse_context
```

**✅ NEW (v3):**
```python
from langfuse import observe, get_client
```

## Migration Checklist

When migrating from v2 to v3:

- [x] Update `requirements.txt`: `langfuse>=2.0.0` → `langfuse>=3.0.0`
- [x] Change imports: `from langfuse.decorators import ...` → `from langfuse import ...`
- [x] Replace `langfuse_context` with `get_client()`
- [x] Replace `update_current_observation()` with:
  - `update_current_span()` for spans (most common)
  - `update_current_generation()` for generations
- [x] Replace `flush()` with `shutdown()`
- [x] Replace `langfuse.score(trace_id, ...)` with `get_client().score_current_trace(...)`
- [x] Replace `create_dataset_run_item()` with `item.run()` context manager
- [x] Test all examples with API keys configured

### 5. Scoring API Changes

**❌ OLD (v2):**
```python
langfuse.score(
    trace_id=trace_id,
    name="quality",
    value=0.9
)
```

**✅ NEW (v3):**
```python
from langfuse import get_client

get_client().score_current_trace(
    name="quality",
    value=0.9
)
```

### 6. Dataset Evaluation Changes

**❌ OLD (v2):**
```python
langfuse.create_dataset_run_item(
    dataset_item_id=item.id,
    run_name="experiment-v1"
)
```

**✅ NEW (v3):**
```python
with item.run(run_name="experiment-v1") as root_span:
    result = my_function()
    root_span.score_trace(name="quality", value=0.9)
```

## Resources

- [SDK Upgrade Path](https://langfuse.com/docs/observability/sdk/upgrade-path)
- [Python SDK v3 Documentation](https://langfuse.com/docs/sdk/python/decorators)
- [Python SDK v3 Release Notes](https://langfuse.com/changelog/2025-06-05-python-sdk-v3-generally-available)

## Why v3?

v3 brings OpenTelemetry (OTEL) standards to Langfuse:
- Better ecosystem compatibility
- Automatic context propagation
- Integration with OTEL-instrumented libraries
- More robust foundation for tracing

While v2 will continue to receive critical bug fixes, v3 is recommended for all new projects and offers future-proof tracing capabilities.
