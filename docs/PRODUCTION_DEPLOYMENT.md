# Production Deployment Guide

This guide covers deploying Langfuse-instrumented applications to production.

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Configuration](#environment-configuration)
3. [Performance Optimization](#performance-optimization)
4. [Monitoring and Alerting](#monitoring-and-alerting)
5. [Security Best Practices](#security-best-practices)
6. [Scaling Considerations](#scaling-considerations)
7. [Disaster Recovery](#disaster-recovery)

## Pre-Deployment Checklist

Before deploying to production:

- [ ] All traces tested in staging environment
- [ ] Environment variables configured in production
- [ ] API keys secured in secrets management
- [ ] Rate limiting configured
- [ ] Monitoring dashboards created
- [ ] Alert thresholds defined
- [ ] Data retention policy set
- [ ] PII masking implemented
- [ ] Cost budget alerts configured
- [ ] Backup and recovery tested

## Environment Configuration

### Production Environment Variables

```bash
# Langfuse Configuration
LANGFUSE_SECRET_KEY=sk-lf-prod-xxx
LANGFUSE_PUBLIC_KEY=pk-lf-prod-xxx
LANGFUSE_HOST=https://cloud.langfuse.com
LANGFUSE_ENVIRONMENT=production
LANGFUSE_RELEASE=v1.2.3

# SDK Configuration
LANGFUSE_FLUSH_INTERVAL=5000
LANGFUSE_BATCH_SIZE=100
LANGFUSE_ENABLED=true
LANGFUSE_DEBUG=false

# LLM Provider
OPENAI_API_KEY=sk-xxx
```

### Loading Configuration

```python
import os
from dotenv import load_dotenv

# Load environment-specific configuration
env = os.getenv('ENV', 'development')
load_dotenv(f'.env.{env}')
```

## Performance Optimization

### 1. Enable Batching

```python
from langfuse import Langfuse

langfuse = Langfuse(
    flush_interval=5000,  # Flush every 5 seconds
    batch_size=100        # Batch up to 100 events
)
```

### 2. Async Ingestion

All Langfuse SDKs use async ingestion by default. Traces are sent in background threads.

### 3. Sampling for High-Volume Applications

```python
import random
from langfuse.decorators import observe

@observe()
def process_request(request):
    # Sample 10% of traces
    if random.random() < 0.1:
        # Full tracing
        return handle_request(request)
    else:
        # Disable tracing for this request
        return handle_request_no_trace(request)
```

### 4. Caching

Enable prompt caching:

```python
langfuse = Langfuse(
    prompt_cache_ttl=3600  # Cache prompts for 1 hour
)
```

## Monitoring and Alerting

### Key Metrics to Monitor

1. **Error Rate**: Track failed LLM calls
2. **Latency**: Monitor p50, p95, p99 latencies
3. **Cost**: Daily and monthly spend
4. **Token Usage**: Trending token consumption
5. **Quality Scores**: Average quality metrics

### Setting Up Alerts

```python
# Example: Alert on high error rate
from langfuse import Langfuse

langfuse = Langfuse()

# Get error rate from metrics API
metrics = langfuse.api.metrics.daily()
error_rate = calculate_error_rate(metrics)

if error_rate > 0.05:  # 5% threshold
    send_alert("High error rate detected: {error_rate}")
```

### Integration with PostHog

```yaml
# configs/production.yaml
integrations:
  posthog:
    enabled: true
    api_key: ${POSTHOG_API_KEY}
    events:
      - trace_created
      - score_created
      - error_occurred
```

## Security Best Practices

### 1. PII Masking

```python
import re
from langfuse.decorators import observe

def mask_pii(text: str) -> str:
    """Mask PII before sending to Langfuse."""
    # Email
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 
                  '[EMAIL]', text)
    # Phone
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
    # SSN
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', text)
    return text

@observe()
def process_user_input(user_input: str):
    # Mask PII before tracing
    masked_input = mask_pii(user_input)
    # Continue processing with masked input
    return handle_input(masked_input)
```

### 2. Secrets Management

Use environment variables and secrets management:

```python
# Good: Use environment variables
import os
api_key = os.getenv('OPENAI_API_KEY')

# Bad: Hardcode secrets
# api_key = 'sk-...'  # DON'T DO THIS
```

### 3. Network Security

- Use HTTPS for all Langfuse communications
- Enable VPC if self-hosting
- Configure firewall rules
- Use private networks for database access

## Scaling Considerations

### Horizontal Scaling

Langfuse SDKs are stateless and scale horizontally:

```yaml
# Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-app
spec:
  replicas: 5  # Scale to 5 pods
  template:
    spec:
      containers:
      - name: app
        env:
        - name: LANGFUSE_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: langfuse-secrets
              key: secret-key
```

### Rate Limiting

Configure rate limits in production:

- Core Plan: 4,000 requests/minute
- Pro Plan: 20,000 requests/minute
- Enterprise: Custom limits

### Database Considerations (Self-Hosted)

For self-hosted deployments:

- PostgreSQL: Use managed services (RDS, Cloud SQL)
- ClickHouse: Scale vertically first, then shard
- Redis: Use Redis Cluster for high availability
- S3: Enable versioning and lifecycle policies

## Disaster Recovery

### Backup Strategy

1. **Cloud**: Automated backups by Langfuse
2. **Self-Hosted**:
   - Daily PostgreSQL backups
   - ClickHouse snapshots
   - S3 bucket versioning
   - Redis persistence (AOF + RDB)

### Recovery Procedures

```bash
# PostgreSQL backup
pg_dump -h localhost -U langfuse langfuse > backup.sql

# ClickHouse backup
clickhouse-backup create

# S3 sync
aws s3 sync s3://langfuse-events/ ./backup/events/
```

### Failover Testing

Test failover procedures quarterly:

1. Simulate database failure
2. Verify fallback to replica
3. Test data restoration
4. Validate trace continuity

## Production Checklist

### Week 1: Soft Launch

- [ ] Deploy to production with 10% traffic
- [ ] Monitor error rates and latency
- [ ] Verify traces appear correctly
- [ ] Check cost tracking
- [ ] Review security logs

### Week 2: Ramp Up

- [ ] Increase to 50% traffic
- [ ] Set up alerting thresholds
- [ ] Configure automated evaluations
- [ ] Enable user feedback collection
- [ ] Review performance metrics

### Week 3: Full Deployment

- [ ] 100% production traffic
- [ ] Daily cost reviews
- [ ] Weekly quality reviews
- [ ] Monthly security audits
- [ ] Quarterly disaster recovery tests

## Troubleshooting

### Traces Not Appearing

1. Check API keys are correct
2. Verify network connectivity to Langfuse
3. Ensure `flush()` is called before app exit
4. Check SDK version compatibility

### High Latency

1. Reduce batch size
2. Increase flush interval
3. Check network latency to Langfuse
4. Consider regional endpoints

### High Costs

1. Review token usage by model
2. Implement prompt caching
3. Use smaller models where appropriate
4. Set up cost alerts

## Support

- Documentation: https://langfuse.com/docs
- Discord: https://discord.gg/langfuse
- Email: support@langfuse.com
- Enterprise Support: Available on Enterprise plan

