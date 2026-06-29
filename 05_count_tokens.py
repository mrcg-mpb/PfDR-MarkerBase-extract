"""
Experiment 5 — Count tokens before sending (this call is FREE).

Counting tokens costs nothing and is how you estimate the price of a request
before you send it — handy once you start feeding whole PDFs.

Run:  python 05_count_tokens.py
"""
import anthropic

MODEL = "claude-opus-4-8"
client = anthropic.Anthropic()

text = (
    "Count how many tokens this sentence costs, and estimate the price. "
    "Replace this with a longer passage to see the count grow."
)

n = client.messages.count_tokens(
    model=MODEL,
    messages=[{"role": "user", "content": text}],
).input_tokens

# Opus 4.8 input rate is $5 per 1,000,000 tokens.
cost = n / 1e6 * 5
print(f"{n} input tokens  ≈  ${cost:.6f} at the Opus input rate")
