"""
MCP Calculator Client

Connects to the MCP Calculator Server and runs a Strands agent with the
calculator tools. Start the server first (mcp_server.py), then run this client.

Run from project root:  python mcp_calculator/mcp_client.py
Or from this folder:    python mcp_client.py
"""
import sys
from pathlib import Path

# Ensure the project root is not on sys.path, so "import mcp" uses the installed
# package (e.g. from venv) instead of the local mcp/ folder in this repo.
_script_dir = Path(__file__).resolve().parent
_project_root = _script_dir.parent
def _ok(p):
    if p == "":
        return False
    try:
        return Path(p).resolve() != _project_root
    except Exception:
        return True
sys.path = [str(_script_dir)] + [p for p in sys.path if _ok(p)]

from dotenv import load_dotenv
from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient

# Load .env from project root
load_dotenv(_project_root / ".env")

MCP_SERVER_URL = "http://localhost:8000/mcp/"

SYSTEM_PROMPT = """
You are a helpful calculator assistant that can perform basic arithmetic operations.
You have access to the following calculator tools:
- add: Add two numbers together
- subtract: Subtract one number from another
- multiply: Multiply two numbers together
- divide: Divide one number by another

When asked to perform calculations, use the appropriate tool rather than calculating the result yourself.
Explain the calculation and show the result clearly.
"""


def main():
    """Connect to the MCP server and run the interactive calculator agent."""
    def create_streamable_http_transport():
        return streamablehttp_client(MCP_SERVER_URL)

    streamable_http_mcp_client = MCPClient(create_streamable_http_transport)

    print("Connecting to MCP server...")

    with streamable_http_mcp_client:
        tools = streamable_http_mcp_client.list_tools_sync()
        print(f"Available MCP tools: {[tool.tool_name for tool in tools]}")

        agent = Agent(system_prompt=SYSTEM_PROMPT, tools=tools)

        print("\nCalculator Agent Ready! Type 'exit' to quit.\n")
        while True:
            user_input = input("Question: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            print("\nThinking...\n")
            response = agent(user_input)
            print(f"Answer: {response}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
