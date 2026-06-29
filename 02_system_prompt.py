"""
Experiment 2 — Steering the model with a system prompt.

Run:  python 02_system_prompt.py

The `system` text sets the model's role and behaviour. Edit it and rerun to
feel how much it changes the answer.
"""
import anthropic

MODEL = "claude-opus-4-8"
client = anthropic.Anthropic()

SYSTEM = (
    "You are a flirtatious zookeeper. "
    "In your answer you should use loads of animal metaphors and puns."
)

resp = client.messages.create(
    model=MODEL,
    max_tokens=400,
    system=SYSTEM,
    messages=[
        {
            "role": "user",
            "content": "Tell me about malaria.",
        }
    ],
)

# resp.content can be empty (e.g. a refusal) or lead with a non-text block, so
# don't assume content[0] is text — pull out the text blocks and check why it
# stopped.
text = "".join(block.text for block in resp.content if block.type == "text")

if text:
    print(text)
else:
    print(f"[no text returned — stop_reason: {resp.stop_reason}]")
    if resp.stop_reason == "refusal":
        print("The model declined this prompt. Try rewording the SYSTEM text.")

print(f"\n— stop_reason: {resp.stop_reason}")
print(f"— tokens: {resp.usage.input_tokens} in / {resp.usage.output_tokens} out")
