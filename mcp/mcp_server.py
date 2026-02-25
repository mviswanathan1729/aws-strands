"""
MCP Calculator Example – Server

Provides calculator tools (add, subtract, multiply, divide) over Streamable HTTP.
Run this first, then run mcp_client.py to connect an agent.

Run from project root:  python mcp_calculator/mcp_server.py
Or from this folder:    python mcp_server.py
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

from mcp.server import FastMCP


def start_calculator_server():
    """
    Initialize and start an MCP calculator server.

    This function creates a FastMCP server instance that provides calculator tools
    for performing basic arithmetic operations. The server uses Streamable HTTP
    transport for communication.
    """
    mcp = FastMCP("Calculator Server")

    @mcp.tool(description="Add two numbers together")
    def add(x: int, y: int) -> int:
        """Add two numbers and return the result.

        Args:
            x: First number
            y: Second number

        Returns:
            The sum of x and y
        """
        return x + y

    @mcp.tool(description="Subtract one number from another")
    def subtract(x: int, y: int) -> int:
        """Subtract y from x and return the result.

        Args:
            x: Number to subtract from
            y: Number to subtract

        Returns:
            The difference (x - y)
        """
        return x - y

    @mcp.tool(description="Multiply two numbers together")
    def multiply(x: int, y: int) -> int:
        """Multiply two numbers and return the result.

        Args:
            x: First number
            y: Second number

        Returns:
            The product of x and y
        """
        return x * y

    @mcp.tool(description="Divide one number by another")
    def divide(x: float, y: float) -> float:
        """Divide x by y and return the result.

        Args:
            x: Numerator
            y: Denominator (must not be zero)

        Returns:
            The quotient (x / y)

        Raises:
            ValueError: If y is zero
        """
        if y == 0:
            raise ValueError("Cannot divide by zero")
        return x / y

    print("Starting MCP Calculator Server on http://localhost:8000")
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    start_calculator_server()
