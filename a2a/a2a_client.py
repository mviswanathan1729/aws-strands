import asyncio
import logging
from uuid import uuid4

import httpx
from a2a.client import A2ACardResolver, ClientConfig, ClientFactory
from a2a.client.errors import A2AClientJSONRPCError
from a2a.types import Message, Part, Role, TextPart

#logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 300 # set request timeout to 5 minutes

def create_message(*, role: Role = Role.user, text: str) -> Message:
    return Message(
        kind="message",
        role=role,
        parts=[Part(TextPart(kind="text", text=text))],
        message_id=uuid4().hex,
    )


def get_text_from_message(message: Message) -> str:
    """Extract all text parts from an A2A Message into a single string."""
    parts = getattr(message, "parts", []) or []
    texts = []
    for p in parts:
        if hasattr(p, "text"):
            texts.append(p.text)
        elif hasattr(p, "root") and hasattr(p.root, "text"):
            texts.append(p.root.text)
        elif isinstance(p, dict) and "text" in p:
            texts.append(p["text"])
        elif hasattr(p, "get") and callable(p.get) and p.get("text"):
            texts.append(p.get("text", ""))
    return "\n".join(texts).strip() if texts else ""


def get_text_from_task(task) -> str:
    """Extract answer text from an A2A Task (artifacts or agent messages in history)."""
    # Prefer artifacts (e.g. agent_response with full answer)
    artifacts = getattr(task, "artifacts", []) or []
    for art in artifacts:
        parts = getattr(art, "parts", []) or []
        for p in parts:
            if hasattr(p, "root") and hasattr(p.root, "text"):
                return (p.root.text or "").strip()
            if hasattr(p, "text"):
                return (p.text or "").strip()
    # Fallback: concatenate agent messages from history
    history = getattr(task, "history", []) or []
    agent_texts = []
    for msg in history:
        if getattr(msg, "role", None) and str(getattr(msg, "role", "")).endswith("agent"):
            t = get_text_from_message(msg)
            if t:
                agent_texts.append(t)
    return "\n".join(agent_texts).strip() if agent_texts else ""

async def send_sync_message(message: str, base_url: str = "http://127.0.0.1:9000"):
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as httpx_client:
        # Get agent card
        resolver = A2ACardResolver(httpx_client=httpx_client, base_url=base_url)
        agent_card = await resolver.get_agent_card()

        # Create client using factory
        config = ClientConfig(
            httpx_client=httpx_client,
            streaming=False,  # Use non-streaming mode for sync response
        )
        factory = ClientFactory(config)
        client = factory.create(agent_card)

        # Create and send message
        msg = create_message(text=message)

        # With streaming=False, this will yield exactly one result
        async for event in client.send_message(msg):
            if isinstance(event, Message):
                #logger.info(event.model_dump_json(exclude_none=True, indent=2))
                return event
            elif isinstance(event, tuple) and len(event) == 2:
                # (Task, UpdateEvent) tuple
                task, update_event = event
                #logger.info(f"Task: {task.model_dump_json(exclude_none=True, indent=2)}")
                if update_event:
                    logger.info(f"Update: {update_event.model_dump_json(exclude_none=True, indent=2)}")
                return task
            else:
                # Fallback for other response types
                #logger.info(f"Response: {str(event)}")
                return event

# Usage
if __name__ == "__main__":
    try:
        answer = asyncio.run(send_sync_message("what is 70 / 11"))
        if isinstance(answer, Message):
            text = get_text_from_message(answer)
        else:
            text = get_text_from_task(answer)
        print("Answer:", text if text else answer)
        print("--------------------------------")

    except A2AClientJSONRPCError as e:
        logger.error(
            "Server returned an error (code=%s): %s. "
            "Check the A2A server terminal for the full traceback (e.g. missing AWS credentials or Bedrock error).",
            getattr(e, "code", None),
            str(e),
        )
        raise