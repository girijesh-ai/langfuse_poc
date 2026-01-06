"""
Example 7: Production Monitoring and Alerting

Demonstrates:
- Real-time metrics monitoring
- Cost tracking and alerting
- Error rate monitoring
- Latency tracking
- Quality score monitoring
- Custom dashboard creation
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()


class ProductionMonitor:
    """Production monitoring system for Langfuse traces."""
    
    def __init__(self):
        self.langfuse = Langfuse()
        self.alert_thresholds = {
            'error_rate': 0.05,          # 5%
            'daily_cost': 100.0,         # $100
            'latency_p95': 5000,         # 5 seconds
            'quality_score': 0.7         # 70%
        }
    
    def get_metrics_summary(self, days: int = 1) -> Dict[str, Any]:
        """Get comprehensive metrics summary."""
        print(f"\nFetching metrics for last {days} day(s)...")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        try:
            metrics = self.langfuse.api.metrics.daily(
                filter={
                    "from_timestamp": start_date.isoformat(),
                    "to_timestamp": end_date.isoformat()
                }
            )
            
            summary = {
                'total_traces': 0,
                'total_cost': 0.0,
                'total_tokens': 0,
                'errors': 0,
                'latencies': [],
                'models_used': set(),
                'users': set()
            }
            
            for metric in metrics:
                summary['total_traces'] += metric.get('trace_count', 0)
                summary['total_cost'] += metric.get('total_cost', 0)
                summary['total_tokens'] += metric.get('total_tokens', 0)
                summary['errors'] += metric.get('error_count', 0)
                
                if 'latency' in metric:
                    summary['latencies'].append(metric['latency'])
                
                if 'model' in metric:
                    summary['models_used'].add(metric['model'])
                
                if 'user_id' in metric:
                    summary['users'].add(metric['user_id'])
            
            summary['models_used'] = list(summary['models_used'])
            summary['users'] = list(summary['users'])
            summary['error_rate'] = (summary['errors'] / summary['total_traces'] 
                                    if summary['total_traces'] > 0 else 0)
            
            return summary
            
        except Exception as e:
            print(f"Error fetching metrics: {e}")
            return {}
    
    def display_metrics_dashboard(self, summary: Dict[str, Any]):
        """Display metrics in a dashboard format."""
        print("\n" + "="*70)
        print("LANGFUSE PRODUCTION DASHBOARD")
        print("="*70)
        
        print("\nOVERVIEW")
        print("-"*70)
        print(f"Total Traces:        {summary.get('total_traces', 0):,}")
        print(f"Unique Users:        {len(summary.get('users', []))}")
        print(f"Models Used:         {', '.join(summary.get('models_used', []))}")
        
        print("\nCOSTS")
        print("-"*70)
        total_cost = summary.get('total_cost', 0)
        total_tokens = summary.get('total_tokens', 0)
        total_traces = summary.get('total_traces', 1)
        
        print(f"Total Cost:          ${total_cost:.4f}")
        print(f"Cost per Trace:      ${total_cost/total_traces:.4f}")
        print(f"Total Tokens:        {total_tokens:,}")
        print(f"Tokens per Trace:    {total_tokens//total_traces:,}")
        
        print("\nQUALITY")
        print("-"*70)
        error_rate = summary.get('error_rate', 0)
        print(f"Error Rate:          {error_rate*100:.2f}%")
        print(f"Total Errors:        {summary.get('errors', 0)}")
        
        if summary.get('latencies'):
            avg_latency = sum(summary['latencies']) / len(summary['latencies'])
            print(f"Avg Latency:         {avg_latency:.0f}ms")
        
        print("\n" + "="*70)
    
    def check_alerts(self, summary: Dict[str, Any]) -> List[str]:
        """Check if any alert thresholds are breached."""
        alerts = []
        
        # Error rate alert
        if summary.get('error_rate', 0) > self.alert_thresholds['error_rate']:
            alerts.append(
                f"HIGH ERROR RATE: {summary['error_rate']*100:.2f}% "
                f"(threshold: {self.alert_thresholds['error_rate']*100}%)"
            )
        
        # Cost alert
        if summary.get('total_cost', 0) > self.alert_thresholds['daily_cost']:
            alerts.append(
                f"HIGH DAILY COST: ${summary['total_cost']:.2f} "
                f"(threshold: ${self.alert_thresholds['daily_cost']})"
            )
        
        # Latency alert
        if summary.get('latencies'):
            p95_latency = sorted(summary['latencies'])[int(len(summary['latencies']) * 0.95)]
            if p95_latency > self.alert_thresholds['latency_p95']:
                alerts.append(
                    f"HIGH LATENCY (P95): {p95_latency:.0f}ms "
                    f"(threshold: {self.alert_thresholds['latency_p95']}ms)"
                )
        
        return alerts
    
    def send_alerts(self, alerts: List[str]):
        """Send alerts via configured channels."""
        if not alerts:
            print("\nNo alerts triggered - all metrics within thresholds")
            return
        
        print("\nALERTS TRIGGERED")
        print("="*70)
        for i, alert in enumerate(alerts, 1):
            print(f"{i}. {alert}")
        print("="*70)
        
        # In production, send to Slack, PagerDuty, etc.
        # Example:
        # slack_webhook = os.getenv('SLACK_WEBHOOK_URL')
        # if slack_webhook:
        #     send_slack_alert(slack_webhook, alerts)
    
    def analyze_cost_by_dimension(self, days: int = 7):
        """Analyze costs broken down by different dimensions."""
        print(f"\nAnalyzing costs by dimension (last {days} days)...")
        print("="*70)
        
        # This would use the actual metrics API
        # Simplified example:
        
        print("\nCOST BY MODEL")
        print("-"*70)
        print(f"gpt-4o              ${45.23:.2f}  (62.5%)")
        print(f"gpt-4o-mini         ${18.45:.2f}  (25.5%)")
        print(f"gpt-3.5-turbo       ${8.67:.2f}   (12.0%)")
        
        print("\nCOST BY USER TIER")
        print("-"*70)
        print(f"Enterprise          ${42.15:.2f}  (58.2%)")
        print(f"Premium             ${22.30:.2f}  (30.8%)")
        print(f"Standard            ${7.90:.2f}   (11.0%)")
        
        print("\nCOST BY FEATURE")
        print("-"*70)
        print(f"chat-completion     ${38.50:.2f}  (53.2%)")
        print(f"rag-retrieval       ${21.25:.2f}  (29.4%)")
        print(f"summarization       ${12.60:.2f}  (17.4%)")
        
        print("\n" + "="*70)
    
    def quality_score_analysis(self):
        """Analyze quality scores across traces."""
        print("\nQUALITY SCORE ANALYSIS")
        print("="*70)
        
        # This would fetch actual scores from Langfuse
        # Simplified example:
        
        print("\nSCORE DISTRIBUTION")
        print("-"*70)
        print(f"Excellent (>0.9):   ████████████████████ 45%")
        print(f"Good (0.7-0.9):     ████████████ 30%")
        print(f"Fair (0.5-0.7):     ████████ 15%")
        print(f"Poor (<0.5):        ████ 10%")
        
        print("\nAVERAGE SCORES BY METRIC")
        print("-"*70)
        print(f"Accuracy:           0.87")
        print(f"Relevance:          0.82")
        print(f"Hallucination:      0.91  (lower is better)")
        print(f"User Satisfaction:  0.79")
        
        print("\n" + "="*70)


def example_realtime_monitoring():
    """Example of real-time monitoring setup."""
    print("\n" + "="*70)
    print("Example 7.1: Real-Time Monitoring")
    print("="*70)
    
    monitor = ProductionMonitor()
    
    # Get metrics for last 24 hours
    summary = monitor.get_metrics_summary(days=1)
    
    # Display dashboard
    monitor.display_metrics_dashboard(summary)
    
    # Check for alerts
    alerts = monitor.check_alerts(summary)
    monitor.send_alerts(alerts)


def example_cost_analysis():
    """Example of detailed cost analysis."""
    print("\n" + "="*70)
    print("Example 7.2: Cost Analysis")
    print("="*70)
    
    monitor = ProductionMonitor()
    monitor.analyze_cost_by_dimension(days=7)


def example_quality_monitoring():
    """Example of quality score monitoring."""
    print("\n" + "="*70)
    print("Example 7.3: Quality Monitoring")
    print("="*70)
    
    monitor = ProductionMonitor()
    monitor.quality_score_analysis()


def main():
    """Run all monitoring examples."""
    print("\n" + "="*70)
    print("Langfuse Example 7: Production Monitoring & Alerting")
    print("="*70)
    
    try:
        example_realtime_monitoring()
        example_cost_analysis()
        example_quality_monitoring()
        
        print("\n" + "="*70)
        print("Monitoring Setup Complete")
        print("="*70)
        print("\nProduction monitoring capabilities demonstrated:")
        print("  - Real-time metrics dashboard")
        print("  - Automated alert checking")
        print("  - Cost analysis by dimension")
        print("  - Quality score tracking")
        print("  - Error rate monitoring")
        print("  - Latency analysis")
        print("\nNext steps:")
        print("  - Set up Slack/PagerDuty integration")
        print("  - Configure custom alert thresholds")
        print("  - Create automated daily reports")
        print("  - Set up cost budgets")
        print(f"\nView live dashboard: {os.getenv('LANGFUSE_HOST')}")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\nError: {e}")
        print("Note: Some features require production data\n")


if __name__ == "__main__":
    main()
