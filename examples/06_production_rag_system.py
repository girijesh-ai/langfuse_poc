"""
Example 6: Production-Ready RAG System

Demonstrates:
- Complete RAG pipeline with quality checks
- Context relevance evaluation
- Hallucination detection
- Answer quality scoring
- Production error handling
- Performance monitoring
"""

import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from langfuse import observe, get_client
from langfuse.openai import openai

load_dotenv()


class ProductionRAGSystem:
    """Production-ready RAG system with observability and quality checks."""
    
    def __init__(self):
        self.embedding_model = "text-embedding-3-small"
        self.generation_model = "gpt-4o"
        self.eval_model = "gpt-4o-mini"
    
    @observe(as_type="retriever")
    def retrieve_contexts(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve relevant contexts from vector database."""
        # Simulated vector database retrieval
        # In production: use Pinecone, Weaviate, Qdrant, etc.
        
        knowledge_base = [
            {
                "id": "doc-001",
                "content": "Langfuse provides comprehensive tracing for LLM applications, capturing prompts, completions, token usage, and costs.",
                "metadata": {"source": "docs", "section": "tracing"},
                "score": 0.95
            },
            {
                "id": "doc-002",
                "content": "Prompt management in Langfuse enables version control, A/B testing, and environment-based deployment of prompts.",
                "metadata": {"source": "docs", "section": "prompts"},
                "score": 0.88
            },
            {
                "id": "doc-003",
                "content": "Evaluation features include LLM-as-a-Judge, human annotation, and user feedback collection.",
                "metadata": {"source": "docs", "section": "evaluation"},
                "score": 0.82
            }
        ]
        
        # Filter based on query (simplified)
        results = knowledge_base[:top_k]

        # Update span with retrieval metadata (v3 API - retriever is a span type)
        langfuse = get_client()
        langfuse.update_current_span(
            input=query,
            output=results,
            metadata={
                "top_k": top_k,
                "num_results": len(results),
                "retrieval_method": "vector_similarity"
            }
        )

        return results
    
    @observe(as_type="generation")
    def evaluate_context_relevance(self, query: str, context: str) -> Dict[str, Any]:
        """Evaluate if retrieved context is relevant to the query."""
        response = openai.chat.completions.create(
            model=self.eval_model,
            messages=[
                {
                    "role": "system",
                    "content": "Evaluate if the context is relevant to answer the question. Respond with RELEVANT, PARTIALLY_RELEVANT, or NOT_RELEVANT and a brief explanation."
                },
                {
                    "role": "user",
                    "content": f"Question: {query}\n\nContext: {context}\n\nEvaluation:"
                }
            ],
            temperature=0.1,
            max_tokens=100
        )
        
        evaluation = response.choices[0].message.content
        
        # Parse relevance
        if "RELEVANT" in evaluation and "NOT_RELEVANT" not in evaluation:
            relevance = "RELEVANT"
            score = 1.0
        elif "PARTIALLY_RELEVANT" in evaluation:
            relevance = "PARTIALLY_RELEVANT"
            score = 0.5
        else:
            relevance = "NOT_RELEVANT"
            score = 0.0
        
        return {
            "relevance": relevance,
            "score": score,
            "explanation": evaluation
        }
    
    @observe(as_type="generation")
    def generate_answer(self, query: str, contexts: List[Dict]) -> str:
        """Generate answer using retrieved contexts."""
        # Combine contexts
        combined_context = "\n\n".join([
            f"[Source {i+1}]: {ctx['content']}"
            for i, ctx in enumerate(contexts)
        ])
        
        response = openai.chat.completions.create(
            model=self.generation_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Answer questions using ONLY the provided context. If the context doesn't contain the answer, say 'I don't have enough information to answer that question.'"
                },
                {
                    "role": "user",
                    "content": f"Context:\n{combined_context}\n\nQuestion: {query}\n\nAnswer:"
                }
            ],
            temperature=0.4,
            max_tokens=300
        )
        
        answer = response.choices[0].message.content

        # Update generation with context info (v3 API - this is a generation type)
        langfuse = get_client()
        langfuse.update_current_generation(
            metadata={
                "num_contexts": len(contexts),
                "model": self.generation_model,
                "context_length": len(combined_context)
            }
        )

        return answer
    
    @observe(as_type="evaluator")
    def check_hallucination(self, query: str, context: str, answer: str) -> Dict[str, Any]:
        """Check if answer is grounded in the provided context."""
        response = openai.chat.completions.create(
            model=self.eval_model,
            messages=[
                {
                    "role": "system",
                    "content": "Determine if the answer is fully grounded in the context or contains hallucinated information. Respond with GROUNDED, PARTIALLY_GROUNDED, or HALLUCINATED with explanation."
                },
                {
                    "role": "user",
                    "content": f"Context: {context}\n\nAnswer: {answer}\n\nEvaluation:"
                }
            ],
            temperature=0.1,
            max_tokens=150
        )
        
        evaluation = response.choices[0].message.content
        
        if "GROUNDED" in evaluation and "PARTIALLY" not in evaluation and "HALLUCINATED" not in evaluation:
            status = "GROUNDED"
            score = 1.0
        elif "PARTIALLY_GROUNDED" in evaluation:
            status = "PARTIALLY_GROUNDED"
            score = 0.5
        else:
            status = "HALLUCINATED"
            score = 0.0
        
        return {
            "status": status,
            "score": score,
            "explanation": evaluation
        }
    
    @observe()
    def query(self, user_query: str) -> Dict[str, Any]:
        """Main RAG query method with full observability."""
        print(f"Processing query: {user_query}")

        # Update trace metadata (v3 pattern)
        langfuse = get_client()
        langfuse.update_current_trace(
            user_id="production-user",
            session_id="rag-session",
            tags=["rag", "production", "quality-checked"]
        )
        
        try:
            # Step 1: Retrieve contexts
            contexts = self.retrieve_contexts(user_query, top_k=3)
            print(f"Retrieved {len(contexts)} contexts")
            
            # Step 2: Evaluate context relevance
            relevance_scores = []
            for ctx in contexts:
                rel_eval = self.evaluate_context_relevance(user_query, ctx['content'])
                relevance_scores.append(rel_eval['score'])
                print(f"Context relevance: {rel_eval['relevance']}")
            
            # Check if we have relevant contexts
            avg_relevance = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0
            
            if avg_relevance < 0.3:
                return {
                    "answer": "I don't have enough relevant information to answer that question.",
                    "contexts": contexts,
                    "quality_checks": {
                        "relevance": avg_relevance,
                        "hallucination": None,
                        "quality_passed": False
                    }
                }
            
            # Step 3: Generate answer
            answer = self.generate_answer(user_query, contexts)
            print(f"Generated answer: {answer[:100]}...")
            
            # Step 4: Check for hallucinations
            combined_context = " ".join([ctx['content'] for ctx in contexts])
            hallucination_check = self.check_hallucination(
                user_query, combined_context, answer
            )
            print(f"Hallucination check: {hallucination_check['status']}")
            
            # Step 5: Score the result (v3 pattern)
            langfuse = get_client()

            # Add quality scores using score_current_trace (v3 API)
            langfuse.score_current_trace(
                name="context_relevance",
                value=avg_relevance,
                comment=f"Average relevance across {len(contexts)} contexts"
            )
            
            langfuse.score_current_trace(
                name="hallucination_check",
                value=hallucination_check['score'],
                comment=hallucination_check['explanation'][:200]  # Truncate for comment
            )
            
            # Overall quality score
            quality_score = (avg_relevance + hallucination_check['score']) / 2
            langfuse.score_current_trace(
                name="overall_quality",
                value=quality_score
            )
            
            print(f"Overall quality score: {quality_score:.2f}")
            
            return {
                "answer": answer,
                "contexts": contexts,
                "quality_checks": {
                    "relevance": avg_relevance,
                    "hallucination": hallucination_check['score'],
                    "overall": quality_score,
                    "quality_passed": quality_score >= 0.7
                }
            }
            
        except Exception as e:
            print(f"Error in RAG pipeline: {e}")

            # Log error (v3 pattern)
            langfuse = get_client()
            langfuse.update_current_trace(
                metadata={"error": str(e), "error_type": type(e).__name__}
            )

            raise


def main():
    """Run production RAG examples."""
    print("\n" + "="*70)
    print("Langfuse Example 6: Production RAG System")
    print("="*70 + "\n")
    
    rag = ProductionRAGSystem()
    
    # Test queries
    queries = [
        "What tracing capabilities does Langfuse provide?",
        "How does prompt management work?",
        "What is the capital of France?"  # Should trigger low relevance
    ]
    
    for query in queries:
        print("\n" + "-"*70)
        result = rag.query(query)
        print(f"\nFinal Answer: {result['answer']}")
        print(f"Quality Passed: {result['quality_checks']['quality_passed']}")
        print("-"*70)
    
    print("\n" + "="*70)
    print("Production RAG System Complete")
    print("="*70)
    print("\nFeatures demonstrated:")
    print("  - Context retrieval with metadata")
    print("  - Context relevance evaluation")
    print("  - Answer generation")
    print("  - Hallucination detection")
    print("  - Quality scoring")
    print("  - Error handling")
    print("  - Full trace observability")
    print(f"\nView traces in: {os.getenv('LANGFUSE_HOST')}")
    print("="*70 + "\n")

    # Shutdown to ensure all traces are sent and resources cleaned up (v3 pattern)
    langfuse = get_client()
    langfuse.shutdown()


if __name__ == "__main__":
    main()
