"""
Script to export traces from Langfuse for analysis

Usage:
    python scripts/export_traces.py --days 7 --output traces.json
"""

import argparse
from datetime import datetime, timedelta
from langfuse import Langfuse
import json


def export_traces(days: int = 7, output_file: str = "traces.json"):
    """Export traces from the last N days."""
    langfuse = Langfuse()
    
    print(f"Exporting traces from last {days} days...")
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Fetch traces
    # Note: Use pagination for large datasets
    all_traces = []
    page = 1
    page_size = 50
    
    while True:
        print(f"Fetching page {page}...")
        
        # Using the API to fetch traces
        try:
            response = langfuse.client.trace.list(
                page=page,
                limit=page_size,
                from_timestamp=start_date.isoformat(),
                to_timestamp=end_date.isoformat()
            )
            
            traces = response.data
            
            if not traces:
                break
            
            all_traces.extend([{
                "id": trace.id,
                "name": trace.name,
                "timestamp": trace.timestamp.isoformat() if trace.timestamp else None,
                "user_id": trace.user_id,
                "session_id": trace.session_id,
                "metadata": trace.metadata,
                "tags": trace.tags,
                "input": trace.input,
                "output": trace.output
            } for trace in traces])
            
            page += 1
            
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break
    
    # Save to file
    with open(output_file, 'w') as f:
        json.dump(all_traces, f, indent=2)
    
    print(f"\nExported {len(all_traces)} traces to {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Export Langfuse traces')
    parser.add_argument('--days', type=int, default=7, help='Number of days to export')
    parser.add_argument('--output', type=str, default='traces.json', help='Output file')
    
    args = parser.parse_args()
    
    export_traces(days=args.days, output_file=args.output)


if __name__ == "__main__":
    main()
