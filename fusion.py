"""Confidence-aware fusion of text and image evidence."""
def estimate_severity(text_result, visual_result, rating=None):
    intent = text_result["intent"]["label"]
    sentiment = text_result["sentiment"]["label"]
    defect_words = {"broken","crack","cracked","damaged","damage","defective","not working"}
    text_stats = text_result["text_stats"]
    if intent in {"refund", "replacement", "warranty/service request"} or (sentiment == "negative" and text_stats["negative_term_count"] >= 2):
        label = "high"
    elif sentiment == "negative" or (rating is not None and rating <= 2):
        label = "medium"
    else:
        label = "low"
    return {"label": label, "confidence": 0.55, "basis": "Heuristic text/rating rule; visual defect model is not trained in the starter implementation."}
def assess_alignment(review_text, customer_image_count):
    if not review_text.strip() or not customer_image_count:
        return {"label": "not_assessable", "confidence": 0.0,
                "explanation": "Both review text and customer-uploaded image evidence are required."}
    return {"label": "requires_model", "confidence": 0.0,
            "explanation": "Text-image consistency requires a trained multimodal similarity/entailment model; no unsupported match is asserted."}
