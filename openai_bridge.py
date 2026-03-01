import os
from openai import OpenAI

# Single client for the process
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def call_model(prompt: str, model: str = "gpt-4.1-mini") -> dict:
    """
    Returns a dict so your receipt ledger can store metadata cleanly.
    """
    if not client:
        raise RuntimeError("OPENAI_API_KEY not set in environment")

    resp = client.responses.create(
        model=model,
        input=prompt
    )

    # output_text is a convenience aggregator
    text = resp.output_text

    # best-effort metadata
    meta = {
        "model": model,
        "response_id": getattr(resp, "id", None),
    }

    return {"text": text, "meta": meta}
