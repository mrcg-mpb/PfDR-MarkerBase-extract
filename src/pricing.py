"""
Token pricing for cost estimation — USD per 1M tokens (input, output), keyed by
the full model id recorded in the roster.

Verified against the Anthropic pricing reference (Opus 4.8 $5/$25, Sonnet 4.6
$3/$15, Haiku 4.5 $1/$5 per 1M). Keep in step with the MODELS registries in
eligibility.py / extraction.py, which carry the same numbers. Stdlib-only so the
lightweight stats/README generator can import it without the anthropic dep.
"""

PRICES = {
    "claude-haiku-4-5":  (1.0, 5.0),
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-opus-4-8":   (5.0, 25.0),
}


def _int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return 0


def cost_usd(model_id, tok_in, tok_out):
    """Estimated USD for a call. Unknown models cost 0 (flagged as such upstream)."""
    p_in, p_out = PRICES.get(model_id, (0.0, 0.0))
    return _int(tok_in) / 1e6 * p_in + _int(tok_out) / 1e6 * p_out
