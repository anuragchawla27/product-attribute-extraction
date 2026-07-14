import re
def clean_text(text: str) -> str:
    """Lowercase, strip punctuation (keep hyphens), collapse whitespace.

    Hyphens are preserved because domain terms like 'V-neck', 'A-line',
    and 'off-shoulder' rely on them. No stemming/stopword removal is
    applied — for a small closed-vocabulary TF-IDF setup, aggressive
    NLP preprocessing tends to remove signal rather than noise.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\-]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text