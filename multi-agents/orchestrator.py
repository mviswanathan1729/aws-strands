#!/usr/bin/env python3
"""
# 📁 Orchestrator Strands Agent

A specialized Strands agent that is the orchestrator to utilize sub-agents and tools at its disposal to answer a user query.

## What This Example Shows

"""
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root so AWS credentials work from any cwd
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from strands import Agent
from strands_tools import file_read, file_write, editor
from math_assistant import math_assistant

from general_assistant import general_assistant


# Define a focused system prompt for file operations
ORCHESTRATOR_SYSTEM_PROMPT = """
You are OrchestratorAssist, a sophisticated educational orchestrator designed to coordinate educational support across multiple subjects. Your role is to:

1. Analyze incoming student queries and determine the most appropriate specialized agent to handle them:
   - Math Agent: For mathematical calculations, problems, and concepts
   - General Assistant: For all other topics outside these specialized domains

2. Key Responsibilities:
   - Accurately classify student queries by subject area
   - Route requests to the appropriate specialized agent
   - Maintain context and coordinate multi-step problems
   - Ensure cohesive responses when multiple agents are needed

3. Decision Protocol:
   - If query involves calculations/numbers → Math Agent
   - If query is outside these specialized areas → General Assistant
   - For complex queries, coordinate multiple agents as needed

Always confirm your understanding before routing to ensure accurate assistance.
"""

# Create a file-focused agent with selected tools
orchestrator_agent = Agent(
    system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
    callback_handler=None,
    tools=[math_assistant, general_assistant],
)


# Example usage
if __name__ == "__main__":
    print("\n📁 Orchestrator Strands Agent 📁\n")
    print("Ask a question in any subject area, and I'll route it to the appropriate specialist.")
    print("Type 'exit' to quit.")

    # Interactive loop
    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() == "exit":
                print("\nGoodbye! 👋")
                break

            response = orchestrator_agent(
                user_input, 
            )
            
            # Extract and print only the relevant content from the specialized agent's response
            content = str(response)
            print(content)
            
        except KeyboardInterrupt:
            print("\n\nExecution interrupted. Exiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try asking a different question.")