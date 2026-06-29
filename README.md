# Anthropic API exploration

Five tiny scripts to get a feel for the Claude API. Each costs a fraction of a
cent to run — your $20 covers thousands of these.

## One-time setup

Install the libraries (just once — this has nothing to do with the API key):

```bash
pip install anthropic pydantic
```

## Each terminal session

Set the key in the specific terminal where you want to run these. It lives only
in that terminal and vanishes when you close it:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Keeping it per-terminal (rather than in `~/.zshrc`) is deliberate: only this
terminal bills the API. Claude Code and everything else keep using your
subscription — a globally-set key would get picked up by Claude Code and billed
to the API instead.

Check what a terminal currently has (without printing the secret):

```bash
[ -n "$ANTHROPIC_API_KEY" ] && echo "API key set" || echo "no API key here"
```

## Run them

```bash
python 01_hello.py
python 02_system_prompt.py
python 03_structured_output.py
python 04_eligibility.py
python 05_count_tokens.py
```

## What each one teaches

| Script | Idea |
|---|---|
| `01_hello.py` | A basic call + reading token usage (your cost meter). |
| `02_system_prompt.py` | Steering the model's role/behaviour with a system prompt. |
| `03_structured_output.py` | **Forcing schema-shaped output — the core of the extraction pipeline.** |
| `04_eligibility.py` | A yes/no judgment with reasoning (mirrors pipeline Step 4). |
| `05_count_tokens.py` | Estimating cost before sending (a free call). |

## Things to try

- In any script, change `MODEL` between `claude-haiku-4-5` (cheapest),
  `claude-sonnet-4-6` (balanced), and `claude-opus-4-8` (smartest) and rerun the
  same prompt. Comparing them is the single most useful exercise here — it's the
  same Sonnet-vs-Opus tradeoff your real pipeline depends on.
- Linger on `03_structured_output.py`: feed it messier or ambiguous text and
  watch how it copes. That's exactly the probing the real validation step does.
- Watch the token counts printed at the end of each run — that's your cost
  intuition building.
