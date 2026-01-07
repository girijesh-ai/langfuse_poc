"""
Example 1: Basic Tracing with Langfuse

This example demonstrates:
- Setting up the Langfuse client
- Using the @observe() decorator for automatic tracing
- Nested observations (spans within spans)
- Manual trace updates
"""

import os
from dotenv import load_dotenv
from langfuse.decorators import observe, langfuse_context

# Load environment variables
load_dotenv()

# Simple functions with automatic tracing
@observe()
def retrieve_context(query: str) -> str:
    """Simulate retrieving context from a vector database."""
    print(f"Retrieving context for: {query}")

    # Simulate database lookup
    context = f"Context for '{query}': This is relevant information from our knowledge base."

    # Update current observation with metadata
    langfuse_context.update_current_observation(
        metadata={"retrieval_method": "vector_search", "results_count": 3}
    )

    return context


@observe()
def generate_response(query: str, context: str) -> str:
    """Simulate generating a response using an LLM."""
    print(f"Generating response for: {query}")

    # Simulate LLM call
    response = f"Based on the context, here's the answer: {query} relates to our knowledge base."

    # Update with generation metadata
    langfuse_context.update_current_observation(
        input={"query": query, "context": context},
        output=response,
        metadata={
            "model": "gpt-4",
            "temperature": 0.7,
            "tokens": 150
        }
    )

    return response


@observe()
def rag_pipeline(user_query: str) -> dict:
    """
    Complete RAG pipeline with automatic nested tracing.
    Each function call creates a nested observation.
    """
    print(f"\nProcessing query: {user_query}")

    # Update current trace metadata
    langfuse_context.update_current_trace(
        user_id="user-123",
        session_id="session-456",
        tags=["rag", "production"],
        metadata={"source": "web_app"}
    )

    # Step 1: Retrieve context (creates nested observation)
    context = retrieve_context(user_query)

    # Step 2: Generate response (creates nested observation)
    response = generate_response(user_query, context)

    result = {
        "query": user_query,
        "context": context,
        "response": response
    }

    print("Pipeline completed successfully")
    print("View trace in Langfuse dashboard\n")

    return result


def main():
    """Run the example."""
    print("\n" + "="*60)
    print("Langfuse Example 1: Basic Tracing")
    print("="*60)

    # Example queries
    queries = [
        "What is Langfuse?",
        "How does prompt management work?",
        "Explain LLM tracing"
    ]

    for query in queries:
        result = rag_pipeline(query)
        print(f"Result: {result['response'][:100]}...\n")

    print("\n" + "="*60)
    print("All traces sent to Langfuse")
    print("Visit your Langfuse dashboard to view the traces")
    print(f"URL: {os.getenv('LANGFUSE_HOST', 'https://cloud.langfuse.com')}")
    print("="*60 + "\n")

    # Important: Flush to ensure all traces are sent
    from langfuse.client import Langfuse
    Langfuse().flush()
    


if __name__ == "__main__":
    main()
