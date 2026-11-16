# Multimodal Product Review Intelligence System

A starter implementation for analyzing e-commerce review text, ratings, customer-uploaded images, catalog images and product metadata. It produces sentiment, aspect, intent, emotion, severity, visual evidence and text-image alignment fields, plus a business summary.

## Important implementation note

This repository is a **runnable baseline/scaffold**, not a claim that every deep-learning task has already been trained. The text classifier currently uses transparent lexical/rating heuristics. The image module reports image properties but does **not** claim to detect scratches, cracks or other defects. Text-image consistency and catalog discrepancy are explicitly marked as requiring trained models. Train and evaluate these components on a manually labeled subset before presenting them as production predictions.

The project follows the main problem statement's **no-RAG** constraint. It sends only current review inputs and structured predictions to the optional LLM; it does not use a vector database or retrieval pipeline.

## Features

- Streamlit UI for review text, rating, customer images, catalog images and metadata.
- FastAPI endpoint for inference.
- Baseline sentiment, aspect, intent and emotion extraction.
- Rule-based severity estimate with confidence caveat.
- Image dimensions/brightness/contrast and image quality flags.
- Explicit not-assessable states for unsupported multimodal conclusions.
- Optional LLM summary from structured outputs.
- CSV preparation and evaluation scripts.
- JSON download from the UI.

## Project structure

```text
multimodal_product_review_intelligence/
├── app.py
├── api/main.py
├── src/
│   ├── text_analyzer.py
│   ├── vision_analyzer.py
│   ├── fusion.py
│   ├── llm_reasoner.py
│   └── pipeline.py
├── scripts/
│   ├── prepare_dataset.py
│   └── evaluate.py
├── data/sample_reviews.csv
├── requirements.txt
└── README.md
```

## Setup

Python 3.10 or 3.11 recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Run Streamlit

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit (usually http://localhost:8501).

## Run FastAPI

```bash
uvicorn api.main:app --reload
```

Open http://127.0.0.1:8000/docs for interactive API documentation. The `/analyze` endpoint accepts multipart form fields and optional image files.

## Dataset plan

The project specification suggests:
- Amazon Reviews 2023 as the primary source for review text, ratings and customer review images where available.
- Amazon Berkeley Objects (ABO) or comparable catalog image data.
- MVTec AD or VisA as optional auxiliary defect/anomaly datasets.

Do not download the entire corpus. Select one manageable category (for example Electronics or Clothing/Shoes), create a reproducible subset, preserve product/review/image relationships and document dataset versions and licenses. Keep raw datasets outside Git.

Expected review CSV columns: `review_id`, `product_id`, `review_text`, `rating`. Optional columns can include `customer_image_paths`, `catalog_image_paths`, `category`, `brand`, `model`, `gold_sentiment`, `gold_intent`, `gold_emotion`, `gold_aspect`, `gold_defect`, `gold_severity`, `gold_alignment`.

Prepare a subset:

```bash
python scripts/prepare_dataset.py --input data/raw/reviews.csv --output data/processed/reviews_clean.csv
```

## Recommended model-development roadmap

1. **Annotation:** Create annotation guidelines and manually label a stratified subset for sentiment, aspect, emotion, intent, defect type, severity, image relevance and text-image consistency. Measure inter-annotator agreement where possible.
2. **Text baseline:** Replace heuristic functions in `src/text_analyzer.py` with fine-tuned BERT, RoBERTa or DeBERTa multi-task heads. Keep a text-only baseline.
3. **Vision model:** Train/evaluate a classifier or detector for visible defect categories using suitable labeled data. For anomaly detection, evaluate MVTec AD/VisA methods. Do not treat image brightness/contrast as defect labels.
4. **Multimodal fusion:** Extract text and image embeddings, then compare late fusion, gated fusion and cross-attention. Compare against text-only and image-only baselines.
5. **Contrastive alignment (optional):** Train matching review-image pairs closer than unrelated pairs.
6. **Multi-task learning:** Use shared representations and task heads for sentiment, aspect, intent, emotion, defect, severity and alignment.
7. **LLM reasoning:** Pass validated structured outputs to the LLM. Constrain output schema and explicitly preserve uncertainty.
8. **Evaluation:** Report per-task precision, recall, F1, confusion matrices, calibration/confidence, inference latency and modality ablations. Analyze false positives and false negatives.
9. **Deployment:** Add model versioning, structured logs, monitoring, tests and deployment configuration.

## Evaluation

Prepare a held-out test set with gold labels. Example sentiment evaluation:

```bash
python scripts/evaluate.py --input data/processed/predictions.csv --gold gold_sentiment --pred predicted_sentiment
```

Use task-appropriate metrics:
- Classification: accuracy, precision, recall, macro-F1 and confusion matrix.
- Detection: mAP and per-class precision/recall.
- Anomaly detection: AUROC / AUPRO as appropriate to the benchmark.
- Alignment: accuracy/F1 on manually labeled match, mismatch and unrelated pairs.
- Operational: latency, memory use, error rate and confidence calibration.

## Optional LLM configuration

Copy `.env.example` to `.env`, add your key, and load environment variables before running (for example with `python-dotenv` or your deployment secret manager). The LLM feature is optional. Never commit API keys.

## GitHub and deployment

```bash
git init
git add .
git commit -m "Initial multimodal review intelligence baseline"
git branch -M main
git remote add origin <YOUR_PUBLIC_GITHUB_REPOSITORY_URL>
git push -u origin main
```

Keep the repository public if required by your evaluation instructions, but do not commit datasets, model weights, private credentials or copyrighted data. Deploy the Streamlit app and API separately or use a supported combined hosting setup. Configure secrets in the hosting provider.

## Known limitations / next work

- Baseline NLP is rule-based and must be replaced by fine-tuned transformer models for reliable evaluation.
- No trained visual defect detector is bundled.
- Cross-modal alignment and catalog-vs-customer image matching need trained embeddings/classifiers.
- Severity is a transparent heuristic, not a validated risk model.
- LLM output is explanatory and must not override model confidence or human review.
- Add unit tests, model cards, annotation guidelines and reproducibility configuration before final submission.

## Scope corrections from the supplied brief

The brief's main problem statement explicitly says no RAG. A later paragraph labels RAG as optional and says it can be used; this implementation follows the explicit no-RAG problem statement. The isolated license-plate and OCR references in the results/error-handling section do not match this product-review project and are not implemented.
