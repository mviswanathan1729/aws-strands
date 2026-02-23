# aws-strands

[Strands](https://strands.dev) agents using **AWS Bedrock** as the LLM backend: a single-agent demo with tools, and a three-stage research workflow (Researcher → Analyst → Writer) with web research.

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

## Project layout

- `agent.py` – Single Strands agent with tools (`calculator`, `current_time`, custom `letter_counter`)
- `agents_workflow.py` – Research assistant: Researcher → Analyst → Writer workflow with web tools
- `requirements.txt` – Python dependencies (boto3, strands-agents, strands-agents-tools, strands-agents-builder, python-dotenv)
- `env.example` – Template for `.env` (AWS credentials)

## License

MIT
