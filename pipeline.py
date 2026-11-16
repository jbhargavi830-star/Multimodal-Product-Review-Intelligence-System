"""End-to-end inference pipeline."""
from src.text_analyzer import analyze_text
from src.vision_analyzer import analyze_images, compare_image_sets
from src.fusion import estimate_severity, assess_alignment
from src.llm_reasoner import llm_summary, generate_summary
def analyze_review(payload, customer_images=None, catalog_images=None, use_llm=False):
    text = analyze_text(payload.get("review_text", ""), payload.get("rating"))
    visual = analyze_images(customer_images or [])
    catalog = analyze_images(catalog_images or [])
    severity = estimate_severity(text, visual, payload.get("rating"))
    alignment = assess_alignment(payload.get("review_text", ""), len(customer_images or []))
    comparison = compare_image_sets(customer_images or [], catalog_images or [])
    result = {
        "product": {"name": payload.get("product_name", ""), "category": payload.get("product_category", ""),
                    "metadata": payload.get("metadata", "")},
        "rating": payload.get("rating"),
        **text,
        "visual_analysis": {"customer_images": visual, "catalog_images": catalog, "comparison": comparison},
        "severity": severity,
        "alignment": alignment,
        "human_review_required": severity["confidence"] < 0.70 or alignment["label"] == "requires_model",
    }
    if use_llm:
        result["llm"] = llm_summary(result)
        result["business_summary"] = result["llm"]["summary"]
    else:
        result["business_summary"] = generate_summary(result)
    return result
