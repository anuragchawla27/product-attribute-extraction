# Product Attribute Extraction — AI/NLP Pipeline

An end-to-end pipeline that converts unstructured fashion product
descriptions into structured attributes (Category, Silhouette, Fabric,
Neckline, Sleeve, Length, Embellishment, Color) using TF-IDF and Logistic
Regression, served via a FastAPI endpoint.

## Demo

A short walkthrough video demonstrating the dataset, training, evaluation
metrics, and a live API request is available in
https://github.com/anuragchawla27/product-attribute-extraction/blob/main/Demo.mp4


## Example

**Input:**
```json
{"description": "Off shoulder satin ball gown with corset bodice and sweep train in royal navy"}
```

**Output:**
```json
{
  "Category": "Wedding Dress",
  "Silhouette": "Ball Gown",
  "Fabric": "Satin",
  "Neckline": "Off-shoulder",
  "Sleeve": "Short Sleeve",
  "Length": "Floor Length",
  "Embellishment": ["Not Specified"],
  "Color": ["Ivory"]
}
```

## Project Structure

```
Product Attribute Extraction/
│
├── api/
│   └── main.py                    # FastAPI app — POST /extract
│
├── Data/
│   ├── attribute_schema.json      # fixed vocabulary for each attribute
│   ├── dataset.csv                # 55 labeled product descriptions
│   └── dataset_clean.csv          # cleaned version used for training
│
├── docs/
│   ├── approach.md                # methodology write-up
│   ├── evaluation_report.md       # metrics + failure case analysis
│   └── evaluation_metrics.csv     # raw per-attribute scores
│
├── demo/
│   └── demo_recording.mp4         # short walkthrough / demo video
│
├── models/
│   ├── vectorizer.pkl             # shared TF-IDF vectorizer
│   ├── single_label_models.pkl    # Category, Silhouette, Fabric, etc.
│   ├── multi_label_models.pkl     # Embellishment, Color
│   └── multi_label_binarizers.pkl # label encoders for multi-label attrs
│
├── notebook/
│   └── exploration.ipynb          # preprocessing, training, evaluation
│
├── src/
│   ├── build_dataset.py           # dataset generator
│   └── preprocess.py              # shared text-cleaning function
│
├── venv/                          # virtual environment (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

## How to Run

**1. Set up the environment:**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

**2. (Optional) Regenerate the dataset:**
```bash
python src/build_dataset.py
```

**3. Train the models:**
Open `notebook/exploration.ipynb` and run all cells. This performs
preprocessing, TF-IDF vectorization, trains all 8 attribute models, and
saves them to `models/`.

**4. Run the API:**
```bash
uvicorn api.main:app --reload
```

**5. Test it:**
Open `http://127.0.0.1:8000/docs` for the interactive Swagger UI, or send a
request directly:
```bash
curl -X POST "http://127.0.0.1:8000/extract" \
  -H "Content-Type: application/json" \
  -d "{\"description\": \"Floor length chiffon bridesmaid dress with pleated bodice and V neckline in sage\"}"
```

## Approach Summary

Each attribute has a closed, finite set of possible values, which reframes
this as a **classification problem** rather than open-ended text
generation. TF-IDF converts descriptions into features; single-label
attributes (Category, Silhouette, Fabric, Neckline, Sleeve, Length) use
independent Logistic Regression classifiers, while multi-label attributes
(Embellishment, Color) use `OneVsRestClassifier` with a tuned decision
threshold. Full methodology details are in
[`docs/approach.md`](docs/approach.md).

## Evaluation Summary

Overall average F1 score across all 8 attributes: **0.402**, evaluated on a
held-out test set. Strongest attributes are Category (0.63 F1) and Neckline
(0.72 F1); weaker attributes (Silhouette, Length, Fabric, Sleeve) are
primarily limited by the small dataset size (55 rows) relative to the
number of possible classes per attribute. Full metrics and failure case
analysis are in [`docs/evaluation_report.md`](docs/evaluation_report.md).


## Author

Anurag Chawla
