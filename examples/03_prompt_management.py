"""
Example 3: Prompt Management with Langfuse

This example demonstrates:
- Creating and managing prompts
- Fetching prompts by label
- Dynamic template compilation
- Linking prompts to traces
- Version control
"""

import os
from dotenv import load_dotenv
from langfuse import Langfuse
from langfuse.decorators import observe

load_dotenv()

def create_prompts():
    """Create example prompts in Langfuse."""
    print("\n" + "="*60)
    print("Creating Prompts in Langfuse")
    print("="*60 + "\n")
    
    langfuse = Langfuse()
    
    # Create a text prompt
    try:
        langfuse.create_prompt(
            name="customer-support-prompt",
            prompt="""You are a helpful customer support agent for TechStore.

Customer tier: {{tier}}
Customer question: {{question}}

Provide a {{tone}} response that addresses their question.""",
            labels=["production"],
            config={
                "model": "gpt-4o-mini",
                "temperature": 0.7,
                "max_tokens": 300
            }
        )
        print("Created: customer-support-prompt")
    except Exception as e:
        print(f"Prompt may already exist: {e}")
    
    # Create a chat prompt
    try:
        langfuse.create_prompt(
            name="chat-assistant",
            prompt=[
                {
                    "role": "system",
                    "content": "You are an AI assistant specialized in {{specialty}}."
                },
                {
                    "role": "user",
                    "content": "{{user_message}}"
                }
            ],
            labels=["staging"],
            config={
                "model": "gpt-4o-mini",
                "temperature": 0.5
            }
        )
        print("Created: chat-assistant")
    except Exception as e:
        print(f"Prompt may already exist: {e}")
    
    print("\nPrompts created successfully")
    print("View them in Langfuse dashboard under Prompts\n")


@observe()
def use_prompt_in_application(question: str, tier: str = "standard"):
    """Demonstrate using prompts in application code."""
    langfuse = Langfuse()
    
    # Fetch prompt by name and label
    prompt = langfuse.get_prompt("customer-support-prompt", label="production")
    
    print(f"Fetched prompt version: {prompt.version}")
    print(f"Prompt config: {prompt.config}")
    
    # Compile prompt with variables
    compiled = prompt.compile(
        tier=tier,
        question=question,
        tone="friendly and professional"
    )
    
    print(f"\nCompiled prompt:\n{compiled}\n")
    
    # Use with OpenAI (automatically linked to trace)
    from langfuse.openai import openai
    
    response = openai.chat.completions.create(
        model=prompt.config.get("model", "gpt-4o-mini"),
        messages=[{"role": "user", "content": compiled}],
        temperature=prompt.config.get("temperature", 0.7),
        max_tokens=prompt.config.get("max_tokens", 300),
        metadata={
            "langfuse_prompt_name": prompt.name,
            "langfuse_prompt_version": prompt.version
        }
    )
    
    return response.choices[0].message.content


def main():
    """Run prompt management examples."""
    print("\n" + "="*60)
    print("Langfuse Example 3: Prompt Management")
    print("="*60)
    
    # Step 1: Create prompts
    create_prompts()
    
    # Step 2: Use prompt in application
    print("\n" + "="*60)
    print("Using Prompt in Application")
    print("="*60 + "\n")
    
    try:
        response = use_prompt_in_application(
            question="How do I return a product?",
            tier="premium"
        )
        print(f"Response: {response}\n")
        
        print("Benefits of prompt management:")
        print("  - Centralized version control")
        print("  - A/B testing capabilities")
        print("  - Automatic prompt-trace linking")
        print("  - Team collaboration")
        print("  - Environment-based deployment\n")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Note: Create the prompt in Langfuse UI first or run create_prompts()\n")
    
    # Flush
    from langfuse import client
    client.flush()



if __name__ == "__main__":
    main()
