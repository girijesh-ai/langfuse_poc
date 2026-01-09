"""
Example 4: Dataset Creation and Evaluation

This example demonstrates:
- Creating evaluation datasets
- Adding dataset items
- Running experiments
- LLM-as-a-Judge evaluations
- Comparing results
"""

import os
from dotenv import load_dotenv
from langfuse import Langfuse, observe

load_dotenv()


def create_dataset():
    """Create an evaluation dataset."""
    print("\n" + "="*60)
    print("Creating Evaluation Dataset")
    print("="*60 + "\n")
    
    langfuse = Langfuse()
    
    # Create dataset
    langfuse.create_dataset(
        name="qa-evaluation-dataset",
        description="Questions for QA system evaluation",
        metadata={"domain": "customer-support", "version": "1.0"}
    )
    
    # Add test cases
    test_cases = [
        {
            "input": {"question": "What is Langfuse?"},
            "expected_output": {
                "answer": "Langfuse is an open-source LLM observability platform."
            },
            "metadata": {"difficulty": "easy", "category": "product"}
        },
        {
            "input": {"question": "How does tracing work?"},
            "expected_output": {
                "answer": "Tracing captures every LLM call with prompts, completions, and metadata."
            },
            "metadata": {"difficulty": "medium", "category": "technical"}
        },
        {
            "input": {"question": "What are the main features?"},
            "expected_output": {
                "answer": "Main features include tracing, prompt management, evaluation, and analytics."
            },
            "metadata": {"difficulty": "easy", "category": "product"}
        }
    ]
    
    for case in test_cases:
        langfuse.create_dataset_item(
            dataset_name="qa-evaluation-dataset",
            input=case["input"],
            expected_output=case["expected_output"],
            metadata=case["metadata"]
        )
    
    print(f"Created dataset with {len(test_cases)} items")
    print("View dataset in Langfuse dashboard under Datasets\n")


@observe()
def qa_system(question: str) -> str:
    """Simple QA system for testing."""
    from langfuse.openai import openai
    
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Answer questions concisely."
            },
            {"role": "user", "content": question}
        ],
        temperature=0.3,
        max_tokens=100
    )
    
    return response.choices[0].message.content


def run_experiment():
    """Run evaluation experiment on dataset."""
    print("\n" + "="*60)
    print("Running Experiment")
    print("="*60 + "\n")
    
    langfuse = Langfuse()
    
    # Get dataset
    dataset = langfuse.get_dataset("qa-evaluation-dataset")
    
    experiment_name = "gpt-4o-mini-experiment-v1"
    
    # Run each test case
    for item in dataset.items:
        question = item.input["question"]
        print(f"Testing: {question}")
        
        # Run system
        result = qa_system(question)
        
        # Create dataset run item
        langfuse.create_dataset_run_item(
            dataset_item_id=item.id,
            run_name=experiment_name,
            output={"answer": result},
            metadata={"model": "gpt-4o-mini", "temperature": 0.3}
        )
        
        print(f"Result: {result[:80]}...\n")
    
    print(f"Experiment '{experiment_name}' completed")
    print("View results in Langfuse dashboard\n")


def create_evaluation_score(trace_id: str, value: float, comment: str = None):
    """Create evaluation score for a trace."""
    langfuse = Langfuse()
    
    langfuse.score(
        trace_id=trace_id,
        name="quality",
        value=value,
        comment=comment
    )


def main():
    """Run dataset and evaluation examples."""
    print("\n" + "="*60)
    print("Langfuse Example 4: Dataset & Evaluation")
    print("="*60)
    
    try:
        # Step 1: Create dataset
        create_dataset()
        
        # Step 2: Run experiment
        run_experiment()
        
        print("\n" + "="*60)
        print("Evaluation Workflow Complete")
        print("="*60)
        print("\nNext steps:")
        print("  1. View experiment results in Langfuse dashboard")
        print("  2. Set up LLM-as-a-Judge evaluations")
        print("  3. Compare different model versions")
        print("  4. Annotate results in annotation queues\n")
        
    except Exception as e:
        print(f"Error: {e}\n")

    # Shutdown to ensure all traces are sent and resources cleaned up (v3 pattern)
    from langfuse import get_client
    get_client().shutdown()


if __name__ == "__main__":
    main()
