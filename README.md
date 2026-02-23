# aws-strands

A [Strands](https://strands.dev) agent that uses **AWS Bedrock** as the LLM backend, with built-in and custom tools (calculator, current time, letter counter).

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

Run the agent:

```bash
python agent.py
```

The script sends a single message that asks for the current time, a calculation, and a letter count; the agent uses the available tools and Bedrock to answer.

## Project layout

- `agent.py` – Strands agent with tools (`calculator`, `current_time`, custom `letter_counter`)
- `requirements.txt` – Python dependencies (boto3, strands-agents, strands-agents-tools, strands-agents-builder, python-dotenv)
- `env.example` – Template for `.env` (AWS credentials)

## License

MIT
