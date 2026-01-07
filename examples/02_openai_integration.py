"""
Example 2: OpenAI SDK Integration with Langfuse

This example demonstrates:
- Drop-in replacement for OpenAI SDK
- Automatic tracing of OpenAI calls
- Streaming support
- Function calling
- Adding custom metadata to traces
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# IMPORTANT: Import OpenAI from Langfuse wrapper
# This is the only change needed - everything else stays the same
from langfuse.openai import openai

def example_basic_completion():
    """Basic chat completion with automatic tracing."""
    print("\n" + "="*60)
    print("Example 2.1: Basic Chat Completion")
    print("="*60 + "\n")

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": "Explain Langfuse in one sentence."}
        ],
        temperature=0.7,
        max_tokens=100,
        # Add Langfuse-specific metadata
        metadata={
            "langfuse_user_id": "user-789",
            "langfuse_session_id": "session-abc",
            "langfuse_tags": ["openai", "demo"],
            "langfuse_trace_name": "openai-basic-completion"
        }
    )

    print(f"Response: {response.choices[0].message.content}")
    print(f"Tokens used: {response.usage.total_tokens}")
    print("Automatically traced in Langfuse\n")


def example_streaming():
    """Streaming chat completion with automatic tracing."""
    print("\n" + "="*60)
    print("Example 2.2: Streaming Chat Completion")
    print("="*60 + "\n")

    print("Streaming response: ", end="", flush=True)

    stream = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Count from 1 to 5 slowly."}
        ],
        stream=True,
        stream_options={"include_usage": True},  # Important for token tracking
        metadata={
            "langfuse_trace_name": "openai-streaming",
            "langfuse_tags": ["streaming"]
        }
    )

    full_response = ""
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            full_response += content

    print("\nStreaming complete")
    print("Stream automatically traced with token usage\n")


def example_function_calling():
    """Function calling with automatic tracing."""
    print("\n" + "="*60)
    print("Example 2.3: Function Calling")
    print("="*60 + "\n")

    # Define a function tool
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the current weather in a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"]
                        }
                    },
                    "required": ["location"]
                }
            }
        }
    ]

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "What's the weather like in San Francisco?"}
        ],
        tools=tools,
        tool_choice="auto",
        metadata={
            "langfuse_trace_name": "openai-function-calling",
            "langfuse_tags": ["functions", "tools"]
        }
    )

    message = response.choices[0].message

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        print(f"Function called: {tool_call.function.name}")
        print(f"Arguments: {tool_call.function.arguments}")
        print("Function call traced\n")
    else:
        print(f"Response: {message.content}\n")


def example_custom_observation():
    """Create custom observations with the OpenAI wrapper."""
    print("\n" + "="*60)
    print("Example 2.4: Custom Observation Name")
    print("="*60 + "\n")

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert on LLM observability."},
            {"role": "user", "content": "Why is tracing important for LLM applications?"}
        ],
        # Custom observation properties
        name="expert-response-generation",  # Custom observation name
        metadata={
            "langfuse_trace_name": "expert-consultation",
            "langfuse_user_id": "expert-user-001",
            "langfuse_tags": ["expert", "consultation"],
            "topic": "llm-observability",
            "priority": "high"
        }
    )

    print("Expert response:")
    print(f"   {response.choices[0].message.content}\n")
    print("Traced with custom observation name and metadata\n")


def main():
    """Run all OpenAI integration examples."""
    print("\n" + "="*70)
    print("Langfuse Example 2: OpenAI SDK Integration")
    print("="*70)
    print("\nThis demonstrates the drop-in replacement for OpenAI SDK")
    print("All you need to change: from langfuse.openai import openai\n")

    try:
        # Run examples
        example_basic_completion()
        example_streaming()
        example_function_calling()
        example_custom_observation()

        print("\n" + "="*70)
        print("All OpenAI calls automatically traced")
        print("Features captured:")
        print("   - Prompts and completions")
        print("   - Token usage and costs")
        print("   - Latency")
        print("   - Streaming data")
        print("   - Function calls")
        print("   - Custom metadata")
        print(f"\nView in: {os.getenv('LANGFUSE_HOST', 'https://cloud.langfuse.com')}")
        print("="*70 + "\n")

    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure OPENAI_API_KEY is set in your .env file\n")

    # Flush to ensure all traces are sent
    from langfuse.client import Langfuse
    Langfuse().flush()



if __name__ == "__main__":
    main()
