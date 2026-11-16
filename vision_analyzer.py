"""Lightweight image quality and visual-evidence analysis.
This baseline does not claim trained defect recognition; use labeled data to train a detector.
"""
from PIL import Image, ImageStat
def analyze_images(images):
    results = []
    for idx, image in enumerate(images or []):
        im = image.convert("RGB")
        stat = ImageStat.Stat(im)
        brightness = sum(stat.mean) / 3
        contrast = sum(stat.stddev) / 3
        results.append({
            "image_index": idx,
            "width": im.width, "height": im.height,
            "brightness_mean": round(brightness, 2),
            "contrast_estimate": round(contrast, 2),
            "quality_flag": "low_resolution" if min(im.size) < 128 else "ok",
            "defect_prediction": "not_available_without_trained_defect_model",
            "confidence": 0.0
        })
    return {"image_count": len(results), "images": results,
            "disclaimer": "Image statistics are not defect detection. Train/evaluate a labeled vision model for defect classes."}
def compare_image_sets(customer_images, catalog_images):
    if not customer_images or not catalog_images:
        return {"status": "insufficient_images", "explanation": "Provide both customer and catalog images for comparison."}
    return {"status": "comparison_pending", "explanation": "A trained visual embedding or image-matching model is required for reliable discrepancy detection."}
