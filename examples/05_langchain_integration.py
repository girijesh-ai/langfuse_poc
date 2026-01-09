"""
Example 5: LangChain Integration with Langfuse

Demonstrates:
- LangChain callback handler
- Chain tracing
- Agent tracing
- RAG pipeline with LangChain
- Automatic observation capture
"""

import os
from dotenv import load_dotenv

load_dotenv()

try:
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate
    from langchain.schema import StrOutputParser
    from langfuse.langchain import CallbackHandler
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call(["pip", "install", "-q", "langchain", "langchain-openai"])
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate
    from langchain.schema import StrOutputParser
    from langfuse.langchain import CallbackHandler


def example_simple_chain():
    """Simple LangChain chain with Langfuse tracing."""
    print("\n" + "="*60)
    print("Example 5.1: Simple LangChain Chain")
    print("="*60 + "\n")
    
    # Initialize Langfuse callback
    langfuse_handler = CallbackHandler()
    
    # Create chain
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    prompt = ChatPromptTemplate.from_template(
        "You are a helpful assistant. Answer this question: {question}"
    )
    chain = prompt | llm | StrOutputParser()
    
    # Execute with tracing
    result = chain.invoke(
        {"question": "What is LangChain?"},
        config={"callbacks": [langfuse_handler]}
    )
    
    print(f"Result: {result}")
    print("Chain execution traced in Langfuse\n")
    
    return result


def example_multi_step_chain():
    """Multi-step chain with intermediate steps traced."""
    print("\n" + "="*60)
    print("Example 5.2: Multi-Step Chain")
    print("="*60 + "\n")
    
    langfuse_handler = CallbackHandler()
    
    # Step 1: Extract key points
    llm = ChatOpenAI(model="gpt-4o-mini")
    
    extract_prompt = ChatPromptTemplate.from_template(
        "Extract 3 key points from this text:\n\n{text}"
    )
    extract_chain = extract_prompt | llm | StrOutputParser()
    
    # Step 2: Summarize
    summarize_prompt = ChatPromptTemplate.from_template(
        "Summarize these key points in one sentence:\n\n{points}"
    )
    summarize_chain = summarize_prompt | llm | StrOutputParser()
    
    # Execute multi-step
    text = """
    Langfuse is an open-source LLM observability platform. It provides tracing,
    prompt management, evaluation, and analytics. Teams use it to debug, monitor,
    and improve their LLM applications in production.
    """
    
    points = extract_chain.invoke(
        {"text": text},
        config={"callbacks": [langfuse_handler]}
    )
    print(f"Extracted points:\n{points}\n")
    
    summary = summarize_chain.invoke(
        {"points": points},
        config={"callbacks": [langfuse_handler]}
    )
    print(f"Summary: {summary}")
    print("Multi-step chain traced with nested observations\n")


def example_rag_chain():
    """RAG chain with retrieval and generation traced separately."""
    print("\n" + "="*60)
    print("Example 5.3: RAG Chain")
    print("="*60 + "\n")
    
    langfuse_handler = CallbackHandler()
    
    # Simulate retrieval
    def retrieve_context(query: str) -> str:
        """Simulated vector database retrieval."""
        # In production, this would query a vector database
        contexts = {
            "langfuse": "Langfuse is an open-source observability platform for LLM applications.",
            "tracing": "Tracing captures every LLM call with prompts, completions, and metadata.",
            "default": "No specific context found."
        }
        for key, value in contexts.items():
            if key in query.lower():
                return value
        return contexts["default"]
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    
    # RAG prompt
    rag_prompt = ChatPromptTemplate.from_template("""
Answer the question based on the context below. If the context doesn't contain
the answer, say "I don't have enough information."

Context: {context}

Question: {question}

Answer:""")
    
    # Create RAG chain
    rag_chain = rag_prompt | llm | StrOutputParser()
    
    # Execute RAG
    question = "What is Langfuse?"
    context = retrieve_context(question)
    
    print(f"Retrieved context: {context}\n")
    
    answer = rag_chain.invoke(
        {"context": context, "question": question},
        config={"callbacks": [langfuse_handler]}
    )
    
    print(f"Answer: {answer}")
    print("RAG pipeline traced with context and generation\n")


def main():
    """Run all LangChain integration examples."""
    print("\n" + "="*70)
    print("Langfuse Example 5: LangChain Integration")
    print("="*70)
    
    try:
        example_simple_chain()
        example_multi_step_chain()
        example_rag_chain()
        
        print("\n" + "="*70)
        print("LangChain Integration Complete")
        print("="*70)
        print("\nAll chains automatically traced with:")
        print("  - Chain structure and steps")
        print("  - LLM calls with prompts/completions")
        print("  - Token usage and costs")
        print("  - Latency per step")
        print("  - Session and user tracking")
        print(f"\nView in: {os.getenv('LANGFUSE_HOST', 'https://cloud.langfuse.com')}")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\nError: {e}")
        print("Ensure langchain and langchain-openai are installed:")
        print("  pip install langchain langchain-openai\n")

    # Shutdown to ensure all traces are sent and resources cleaned up (v3 pattern)
    from langfuse import get_client
    get_client().shutdown()


if __name__ == "__main__":
    main()
