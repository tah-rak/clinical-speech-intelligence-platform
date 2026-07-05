"""Word Error Rate calculation utilities."""

import re
from typing import Any


def normalize_text(text: str) -> list[str]:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s']", " ", text)
    return [w for w in text.split() if w]


def calculate_wer(reference: str, hypothesis: str) -> dict[str, Any]:
    """Calculate Word Error Rate using dynamic programming."""
    ref_words = normalize_text(reference)
    hyp_words = normalize_text(hypothesis)

    if not ref_words:
        return {
            "wer": 0.0 if not hyp_words else 1.0,
            "substitutions": 0,
            "deletions": 0,
            "insertions": len(hyp_words),
            "reference_word_count": 0,
            "hypothesis_word_count": len(hyp_words),
            "details": {"note": "Empty reference transcript"},
        }

    n, m = len(ref_words), len(hyp_words)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if ref_words[i - 1] == hyp_words[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j - 1],  # substitution
                    dp[i - 1][j],      # deletion
                    dp[i][j - 1],      # insertion
                )

    # Backtrack for operation counts
    i, j = n, m
    subs, dels, ins = 0, 0, 0
    while i > 0 or j > 0:
        if i > 0 and j > 0 and ref_words[i - 1] == hyp_words[j - 1]:
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            subs += 1
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            dels += 1
            i -= 1
        else:
            ins += 1
            j -= 1

    errors = subs + dels + ins
    wer = errors / n

    return {
        "wer": round(wer, 4),
        "substitutions": subs,
        "deletions": dels,
        "insertions": ins,
        "reference_word_count": n,
        "hypothesis_word_count": m,
        "details": {
            "error_count": errors,
            "accuracy": round(1 - wer, 4),
        },
    }
