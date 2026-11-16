"""FastAPI inference endpoint. JSON endpoint accepts text/metadata; image upload endpoint accepts files."""
from fastapi import FastAPI, UploadFile, File, Form
from PIL import Image
from io import BytesIO
from typing import List, Optional
from src.pipeline import analyze_review
app = FastAPI(title="Multimodal Product Review Intelligence API", version="1.0.0")
@app.get("/health")
def health():
    return {"status": "ok"}
@app.post("/analyze")
def analyze(review_text: str = Form(""), rating: Optional[int] = Form(None),
            product_category: str = Form("Other"), product_name: str = Form(""),
            metadata: str = Form(""),
            customer_images: List[UploadFile] = File(default=[]),
            catalog_images: List[UploadFile] = File(default=[])):
    def load(items):
        output = []
        for item in items:
            try: output.append(Image.open(BytesIO(item.file.read())).convert("RGB"))
            except Exception: continue
        return output
    payload = {"review_text": review_text, "rating": rating, "product_category": product_category,
               "product_name": product_name, "metadata": metadata}
    return analyze_review(payload, load(customer_images), load(catalog_images))
