"""
Analyze costs from Langfuse traces

Usage:
    python scripts/analyze_costs.py --days 7
"""

import argparse
from datetime import datetime, timedelta
from langfuse import Langfuse
from collections import defaultdict


def analyze_costs(days: int = 7):
    """Analyze costs from Langfuse metrics."""
    langfuse = Langfuse()
    
    print(f"Analyzing costs from last {days} days...")
    print("="*60)
    
    # Fetch daily metrics
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    metrics = langfuse.api.metrics.daily(
        filter={
            "from_timestamp": start_date.isoformat(),
            "to_timestamp": end_date.isoformat()
        }
    )
    
    # Aggregate by different dimensions
    total_cost = 0
    total_tokens = 0
    total_traces = 0
    
    costs_by_model = defaultdict(float)
    costs_by_user = defaultdict(float)
    costs_by_tag = defaultdict(float)
    
    print("\nOverall Metrics:")
    print("-"*60)
    
    for metric in metrics:
        total_cost += metric.get('total_cost', 0)
        total_tokens += metric.get('total_tokens', 0)
        total_traces += metric.get('trace_count', 0)
        
        # By model
        model = metric.get('model', 'unknown')
        costs_by_model[model] += metric.get('total_cost', 0)
        
        # By user
        user_id = metric.get('user_id', 'anonymous')
        costs_by_user[user_id] += metric.get('total_cost', 0)
    
    print(f"Total Cost: ${total_cost:.4f}")
    print(f"Total Tokens: {total_tokens:,}")
    print(f"Total Traces: {total_traces:,}")
    print(f"Average Cost per Trace: ${total_cost/total_traces:.4f}" if total_traces > 0 else "N/A")
    
    print("\n\nCosts by Model:")
    print("-"*60)
    for model, cost in sorted(costs_by_model.items(), key=lambda x: x[1], reverse=True):
        percentage = (cost / total_cost * 100) if total_cost > 0 else 0
        print(f"{model:30s} ${cost:8.4f} ({percentage:5.1f}%)")
    
    print("\n\nCosts by User:")
    print("-"*60)
    for user, cost in sorted(costs_by_user.items(), key=lambda x: x[1], reverse=True)[:10]:
        percentage = (cost / total_cost * 100) if total_cost > 0 else 0
        print(f"{user:30s} ${cost:8.4f} ({percentage:5.1f}%)")
    
    print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(description='Analyze Langfuse costs')
    parser.add_argument('--days', type=int, default=7, help='Number of days to analyze')
    
    args = parser.parse_args()
    
    analyze_costs(days=args.days)


if __name__ == "__main__":
    main()
