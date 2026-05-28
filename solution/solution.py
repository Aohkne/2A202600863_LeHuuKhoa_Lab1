"""
Day 1 — LLM API Foundation
AICB-P1: AI Practical Competency Program, Phase 1

Instructions:
    1. Fill in every section marked with TODO.
    2. Do NOT change function signatures.
    3. Copy this file to solution/solution.py when done.
    4. Run: pytest tests/ -v
"""

import os
import time
from typing import Any, Callable

import openai
from dotenv import load_dotenv
load_dotenv()

# Estimated costs per 1K OUTPUT tokens (USD)
COST_PER_1K_OUTPUT_TOKENS = {
    "gpt-4o": 0.010,
    "gpt-4o-mini": 0.0006,
}

OPENAI_MODEL = "gpt-4o"
OPENAI_MINI_MODEL = "gpt-4o-mini"


# Task 1 — Call GPT-4o
def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API and return the response text + latency.
    """
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    start = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    latency = time.time() - start

    return response.choices[0].message.content, latency


# Task 2 — Call GPT-4o-mini
def call_openai_mini(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API using gpt-4o-mini.
    """
    return call_openai(
        prompt,
        model=OPENAI_MINI_MODEL,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )


# Task 3 — Compare GPT-4o vs GPT-4o-mini
def compare_models(prompt: str) -> dict:
    """
    Call both gpt-4o and gpt-4o-mini with the same prompt and return a
    comparison dictionary.
    """
    gpt4o_response, gpt4o_latency = call_openai(prompt)
    mini_response, mini_latency = call_openai_mini(prompt)

    # Cost estimate: words / 0.75 ≈ tokens; cost per 1K tokens
    gpt4o_cost_estimate = (
        (len(gpt4o_response.split()) / 0.75) / 1000
        * COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]
    )

    return {
        "gpt4o_response": gpt4o_response,
        "mini_response": mini_response,
        "gpt4o_latency": gpt4o_latency,
        "mini_latency": mini_latency,
        "gpt4o_cost_estimate": gpt4o_cost_estimate,
    }


# Task 4 — Streaming chatbot with conversation history
def streaming_chatbot() -> None:
    """
    Run an interactive streaming chatbot in the terminal.
    Streams tokens as they arrive and maintains last 3 conversation turns.
    """
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    history = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit"):
            break
        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})

        print("Assistant: ", end="", flush=True)
        assistant_reply = ""

        stream = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=history,
            stream=True,
        )

        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            print(delta, end="", flush=True)
            assistant_reply += delta

        print()  # newline after streaming ends

        history.append({"role": "assistant", "content": assistant_reply})
        # Keep only the last 3 turns (each turn = 1 user + 1 assistant message)
        history = history[-6:]


# Bonus Task A — Retry with exponential backoff
def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    """
    Call fn(). If it raises, retry up to max_retries times with
    exponential backoff (base_delay * 2^attempt).
    """
    last_exception = None
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as e:
            last_exception = e
            if attempt < max_retries:
                time.sleep(base_delay * (2 ** attempt))

    raise last_exception


# Bonus Task B — Batch compare
def batch_compare(prompts: list[str]) -> list[dict]:
    """
    Run compare_models on each prompt in the list.
    """
    results = []
    for prompt in prompts:
        result = compare_models(prompt)
        result["prompt"] = prompt
        results.append(result)
    return results


# Bonus Task C — Format comparison table
def format_comparison_table(results: list[dict]) -> str:
    """
    Format a list of compare_models results as a readable text table.
    """
    def truncate(text: str, length: int = 40) -> str:
        return text[:length] + "..." if len(text) > length else text

    header = (
        f"{'Prompt':<43} | {'GPT-4o Response':<43} | "
        f"{'Mini Response':<43} | {'GPT-4o Latency':>14} | {'Mini Latency':>12}"
    )
    separator = "-" * len(header)
    rows = [header, separator]

    for r in results:
        row = (
            f"{truncate(r.get('prompt', '')):<43} | "
            f"{truncate(r.get('gpt4o_response', '')):<43} | "
            f"{truncate(r.get('mini_response', '')):<43} | "
            f"{r.get('gpt4o_latency', 0):>14.3f} | "
            f"{r.get('mini_latency', 0):>12.3f}"
        )
        rows.append(row)

    return "\n".join(rows)



# Entry point for manual testing
if __name__ == "__main__":
    test_prompt = "Explain the difference between temperature and top_p in one sentence."
    print("=== Comparing models ===")
    result = compare_models(test_prompt)
    for key, value in result.items():
        print(f"{key}: {value}")

    print("\n=== Starting chatbot (type 'quit' to exit) ===")
    streaming_chatbot()