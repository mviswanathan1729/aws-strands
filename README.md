# aws-strands

[Strands](https://strands.dev) agents using **AWS Bedrock** as the LLM backend: a single-agent demo with tools, a three-stage research workflow (Researcher → Analyst → Writer) with web research, and an **orchestrator** that routes queries to specialized sub-agents (Math and General).

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

Interactive three-agent pipeline for research and fact-checking using the web:

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

Or from inside the folder:

```bash
cd multi-agents
python orchestrator.py
```

At the `> ` prompt, ask anything (math, general knowledge, or both). Example: *"What is the approximate population of India? If it increased by 1.5% per year for 10 years, what would the new population be?"* — the orchestrator will route to General Assistant (for the population) and Math Assistant (for the growth calculation), then summarize. Type `exit` to quit.

## Project layout

- `agent.py` – Single Strands agent with tools (`calculator`, `current_time`, custom `letter_counter`)
- `agents_workflow.py` – Research assistant: Researcher → Analyst → Writer workflow with web tools
- `multi-agents/orchestrator.py` – TeachAssist orchestrator; routes to Math and General sub-agents
- `multi-agents/math_assistant.py` – Math specialist (Strands agent + calculator tool, exposed as a tool)
- `multi-agents/general_assistant.py` – General-knowledge specialist (Strands agent, exposed as a tool)
- `requirements.txt` – Python dependencies (boto3, strands-agents, strands-agents-tools, strands-agents-builder, python-dotenv)
- `env.example` – Template for `.env` (AWS credentials)

## License

MIT
