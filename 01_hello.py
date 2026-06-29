"""
Experiment 1 — Hello world + token accounting.

Run:  python 01_hello.py                 (defaults to opus)
      python 01_hello.py --model haiku   (or sonnet / opus)

The last lines print how many tokens the call used and the estimated cost.
Rerunning with each --model is the core cost/quality comparison:
  haiku    cheapest  ($1 / $5  per 1M input/output tokens)
  sonnet   balanced  ($3 / $15)
  opus     smartest  ($5 / $25)
"""
import argparse

import anthropic

# Maps the short --model name to (full model ID, input $/1M, output $/1M).
MODELS = {
    "haiku": ("claude-haiku-4-5", 1.0, 5.0),
    "sonnet": ("claude-sonnet-4-6", 3.0, 15.0),
    "opus": ("claude-opus-4-8", 5.0, 25.0),
}

parser = argparse.ArgumentParser(description="Hello-world call to the Claude API.")
parser.add_argument("--model", choices=MODELS, default="opus",
                    help="which model to call (default: opus)")
args = parser.parse_args()

MODEL, in_price, out_price = MODELS[args.model]

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from your environment

resp = client.messages.create(
    model=MODEL,
    max_tokens=300,
    messages=[
        {
            "role": "user",
            "content": "Explain in 3 sentences what the pfkelch13 gene has to do "
                       "with malaria drug resistance.",
        }
    ],
)

print(resp.content[0].text)
print(f"\n— model: {MODEL}")
print(f"— tokens: {resp.usage.input_tokens} in / {resp.usage.output_tokens} out")

cost = resp.usage.input_tokens / 1e6 * in_price + resp.usage.output_tokens / 1e6 * out_price
print(f"— estimated cost: ${cost:.6f}")
