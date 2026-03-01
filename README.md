# AWS Strands

[Strands](https://strands.dev) agents using **AWS Bedrock** as the LLM backend: a single-agent demo with tools, a three-stage research workflow (Researcher → Analyst → Writer) with web research, an **orchestrator** that routes queries to specialized sub-agents (Math and General), an **MCP calculator** example (server + client), an **A2A (Agent-to-Agent)** calculator (server + client), and a **Swarm** of cooperating agents (researcher, coder, reviewer, architect).

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Environment

Copy the example env file and add your credentials:

```bash
copy env.example .env   # Windows
# cp env.example .env   # macOS/Linux
```

Edit `.env` and set:

- `AWS_ACCESS_KEY_ID` – AWS access key
- `AWS_SECRET_ACCESS_KEY` – AWS secret key
- `AWS_BEARER_TOKEN_BEDROCK` – Bedrock bearer token (if required)

Do not commit `.env`; it is for local secrets only.

## Usage

### Single agent (`agent.py`)

Runs one agent with tools (calculator, current time, letter counter) on a fixed multi-part question:

```bash
python agent.py
```

### Research workflow (`agents_workflow.py`)

In a sequential workflow, agents process tasks in a defined order, with each agent's output becoming the input for the next. Interactive three-agent pipeline for research and fact-checking using the web:

1. **Researcher** – Fetches information via `http_request`
2. **Analyst** – Verifies facts and summarizes findings
3. **Writer** – Produces the final report

```bash
python agents_workflow.py
```

At the `> ` prompt, enter a research question or a claim to fact-check (e.g. *"What are quantum computers?"* or *"Tuesday comes before Monday in the week"*). Type `exit` to quit.

### Orchestrator (`multi-agents/orchestrator.py`)

Interactive **OrchestratorAssist** (orchestrator) that routes each query to one or more specialized sub-agents:

- **Math Assistant** – Mathematical calculations, step-by-step solutions; uses a calculator tool.
- **General Assistant** – General knowledge; answers with a brief non-expert disclaimer.

**How routing works:** The orchestrator is a single Strands agent with both assistants registered as **tools**. The LLM (Bedrock) reads your question and the tools’ docstrings, then decides which tool(s) to call. For mixed questions it can call both; tools run **sequentially** (one after the other), and the orchestrator waits for all results before producing a final summary.

Run from the project root (loads `.env` from there):

```bash
python multi-agents/orchestrator.py
```

At the `> ` prompt, ask anything (math, general knowledge, or both). Example: *"What is the approximate population of India? If it increased by 1.5% per year for 10 years, what would the new population be?"* — the orchestrator will route to General Assistant (for the population) and Math Assistant (for the growth calculation), then summarize. Type `exit` to quit.

### MCP calculator (`mcp/`)

An **MCP (Model Context Protocol)** example: a calculator server exposing tools (add, subtract, multiply, divide) over HTTP, and a Strands client that connects to it and uses those tools via natural language.

**Run the server** (terminal 1, from project root with venv’s Python so the installed `mcp` package is used):

```bash
python mcp/mcp_server.py
```

**Run the client** (terminal 2):

```bash
python mcp/mcp_client.py
```

The client prompts with `Question: ` — ask things like *"What is 12 plus 4?"* or *"Divide 100 by 3."* Type `exit` to quit.

### A2A calculator (`a2a/`)

An **A2A (Agent-to-Agent)** example: a calculator server that exposes a Strands agent over the [A2A protocol](https://spec.modelcontextprotocol.io/specification/a2a/) (JSON-RPC over HTTP), and a client that sends a question and prints the agent’s answer.

**Server** (`a2a_server.py`): Strands agent with the SymPy calculator tool, wrapped in `A2AServer`. Serves the agent card at `/.well-known/agent-card.json` and handles messages at `/`. Requires AWS credentials (Bedrock) in `.env`; loads them from the project root.

**Client** (`a2a_client.py`): Uses the `a2a` client library to fetch the agent card, send a single message (e.g. *"what is 70 * 11"*), and print the extracted answer text from the task response.

**Run the server** (terminal 1, from project root; ensure `.env` is configured):

```bash
python a2a/a2a_server.py
```

Server listens on `http://127.0.0.1:9000` by default.

**Run the client** (terminal 2):

```bash
python a2a/a2a_client.py
```

The client sends one question, prints **Answer:** followed by the agent’s reply, then exits. To ask a different question, edit the `send_sync_message(...)` call in `a2a_client.py` or call it with another URL/query.

If the client reports a JSON-RPC internal error, check the **server** terminal for the real traceback (e.g. missing AWS credentials or Bedrock errors).

### Swarm (`swarm.py`)

A **Swarm** of four Strands agents that cooperate on a single task via handoffs: **researcher**, **coder**, **reviewer**, and **architect**. The swarm starts with the researcher; each agent can hand off to another using an injected coordination tool. Execution continues until the task is done, a timeout is hit, or repetitive handoffs are detected.

Requires AWS credentials in `.env` (loads from project root). Run from project root:

```bash
python swarm.py
```

The script runs one task by default (*"Design and implement a simple REST API for a todo app"*). It prints the final status and node history. To change the task, edit the `swarm(...)` call in `swarm.py`. Debug logs for the swarm are sent to stderr.

## Project layout

- `agent.py` – Single Strands agent with tools (`calculator`, `current_time`, custom `letter_counter`)
- `agents_workflow.py` – Research assistant: Researcher → Analyst → Writer workflow with web tools
- `multi-agents/orchestrator.py` – TeachAssist orchestrator; routes to Math and General sub-agents
- `multi-agents/math_assistant.py` – Math specialist (Strands agent + calculator tool, exposed as a tool)
- `multi-agents/general_assistant.py` – General-knowledge specialist (Strands agent, exposed as a tool)
- `mcp/mcp_server.py` – MCP calculator server (Streamable HTTP)
- `mcp/mcp_client.py` – MCP calculator client (Strands agent using server tools)
- `a2a/a2a_server.py` – A2A calculator server (Strands agent + SymPy calculator, JSON-RPC on port 9000)
- `a2a/a2a_client.py` – A2A client (sends one message, prints answer from task/artifacts)
- `swarm.py` – Swarm of four agents (researcher, coder, reviewer, architect) with handoffs; single task run
- `requirements.txt` – Python dependencies (boto3, strands-agents, strands-agents-tools, strands-agents-builder, python-dotenv, httpx)
- `env.example` – Template for `.env` (AWS credentials)

## License

MIT
