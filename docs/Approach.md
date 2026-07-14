# Approach — Product Attribute Extraction Pipeline

## Problem Understanding

The task is to convert unstructured fashion product descriptions (free-text
sentences written by vendors/copywriters) into structured, queryable
attributes: Category, Silhouette, Fabric, Neckline, Sleeve, Length,
Embellishment, and Color.

The key observation driving the whole design: each attribute in this domain
has a **finite, closed set of possible values** (a neckline is always one of
V-neck, Sweetheart, Off-shoulder, etc. — not open-ended text). This reframes
the problem from open-ended text generation into **classification** — for
each attribute, predict which value(s) from a known vocabulary apply to a
given description. That reframing is what makes a same-day, classical-ML
solution appropriate instead of requiring a large fine-tuned language model.

## Step 1 — Attribute Schema

Before writing any code, a fixed vocabulary was defined for every attribute
(see `data/attribute_schema.json`). Two attributes — **Embellishment** and
**Color** — are treated as **multi-label**, since a single dress can
legitimately have more than one embellishment (e.g. "beaded and sequin") or
color combination. The remaining six attributes are treated as
**single-label**, since a dress typically has exactly one silhouette, one
fabric, etc.

`"Not Specified"` is used as an explicit value whenever a description simply
doesn't mention that attribute — this reflects the reality of vendor-written
text, which is inconsistent in what it chooses to describe.

## Step 2 — Dataset

50+ product descriptions were labeled against the schema (`data/dataset.csv`),
built from the 10 provided sample descriptions plus 45 additional
descriptions covering the rest of the schema's vocabulary, so that every
attribute value has at least some training coverage. Every label was
programmatically validated against the schema to catch typos before training.

## Step 3 — Preprocessing

Text cleaning (`src/preprocess.py`) is intentionally light: lowercasing,
punctuation stripping (while preserving hyphens, since domain terms like
"V-neck," "A-line," and "off-shoulder" depend on them), and whitespace
normalization. No stemming or stopword removal was applied — for a small,
closed-vocabulary domain with TF-IDF, aggressive NLP preprocessing tends to
strip out exactly the signal words the model needs, rather than noise. This
same function is used both to prepare training data and to clean incoming
requests at inference time, ensuring consistency between training and
serving.

## Step 4 — Model

**TF-IDF vectorization** converts cleaned description text into numerical
features, fit once and shared across all attribute models.

For **single-label attributes** (Category, Silhouette, Fabric, Neckline,
Sleeve, Length): one independent **Logistic Regression** classifier per
attribute.

For **multi-label attributes** (Embellishment, Color): labels are encoded
with `MultiLabelBinarizer`, and a `OneVsRestClassifier(LogisticRegression)`
is trained per attribute, predicting a set of applicable labels rather than
one.

**Threshold tuning:** the default `.predict()` behavior for the multi-label
models initially returned zero labels for every test example, because with
so few training examples per label, predicted probabilities rarely crossed
scikit-learn's default 0.5 decision threshold. This was fixed by using
`predict_proba` directly with a lowered threshold (0.3) and a fallback rule:
if no label crosses the threshold, the single highest-probability label is
still returned. This is a deliberate, explainable design choice, documented
further in `evaluation_report.md`.

All trained artifacts (vectorizer, single-label models, multi-label models,
multi-label binarizers) are persisted with `joblib` to `models/` and loaded
once at API startup.

## Step 6 — API

A single FastAPI endpoint, `POST /extract`, accepts a raw description string
and returns structured JSON. It reuses the exact same `clean_text()`
function from training, applies the shared vectorizer, runs all 8 attribute
models, and assembles the results into one JSON object.

## Why this approach (and not a heavier one)

Given a same-day deadline and a schema with closed-vocabulary attributes,
TF-IDF + Logistic Regression was chosen over a fine-tuned transformer model
because:
- It's fast to train and iterate on with a small dataset (55 rows)
- It's fully explainable (feature weights are inspectable)
- It's realistic to build, evaluate, and serve within the time available
- It directly matches what the assignment brief specified (TF-IDF + Logistic
  Regression)

A natural next step, if given more time/data, would be to explore
transformer-based embeddings (e.g. sentence-transformers) for better
generalization on rarer attribute values, discussed further in the
evaluation report.
