"""Text analysis baseline. Replace/extend with fine-tuned BERT/RoBERTa classifiers."""
import re

ASPECT_TERMS = {
    "battery": ["battery", "charge", "charging", "backup"],
    "display": ["display", "screen", "brightness", "pixel"],
    "camera": ["camera", "photo", "picture", "video"],
    "design": ["design", "look", "appearance", "color"],
    "stitching": ["stitch", "seam", "thread"],
    "comfort": ["comfort", "comfortable", "fit", "size"],
    "quality": ["quality", "material", "build", "durable"],
    "packaging": ["packaging", "package", "box"],
    "delivery": ["delivery", "shipping", "arrived"],
}
POSITIVE = {"good","great","excellent","love","perfect","amazing","comfortable","fast","clear","durable","beautiful"}
NEGATIVE = {"bad","poor","broken","damage","damaged","crack","cracked","scratch","scratched","slow","terrible","disappointed","defective","issue","problem"}
EMOTIONS = {
    "anger": {"angry","furious","unacceptable","worst"},
    "frustration": {"frustrated","annoying","issue","problem","doesn't","not working"},
    "disappointment": {"disappointed","expected","waste","regret"},
    "satisfaction": {"satisfied","happy","love","excellent","great"},
    "excitement": {"excited","amazing","fantastic","wow"},
    "confusion": {"confused","unclear","don't understand","how"},
}
INTENTS = {
    "refund": ["refund","money back"],
    "replacement": ["replacement","replace","exchange"],
    "warranty/service request": ["warranty","repair","service"],
    "complaint": ["broken","damaged","defective","poor","not working","disappointed","problem","issue"],
    "inquiry": ["?", "how do", "does it", "can it", "whether"],
    "praise": ["love","excellent","great","amazing","perfect","recommend"],
}
def _confidence(score, total):
    return round(min(0.99, 0.50 + abs(score) / max(total, 1) * 0.45), 3)
def analyze_text(text, rating=None):
    clean = re.sub(r"\s+", " ", (text or "").lower()).strip()
    tokens = re.findall(r"[a-z']+", clean)
    pos = sum(t in POSITIVE for t in tokens)
    neg = sum(t in NEGATIVE for t in tokens)
    if rating is not None:
        pos += 1 if rating >= 4 else 0
        neg += 1 if rating <= 2 else 0
    score = pos - neg
    sentiment = "positive" if score > 0 else "negative" if score < 0 else "neutral"
    aspects = []
    for aspect, words in ASPECT_TERMS.items():
        hits = [w for w in words if re.search(r"\b" + re.escape(w) + r"\b", clean)]
        if hits:
            aspects.append({"aspect": aspect, "evidence_terms": hits,
                            "sentiment": "negative" if any(w in clean for w in NEGATIVE) and neg > pos else sentiment})
    intent = "other"
    for label, phrases in INTENTS.items():
        if any(p in clean for p in phrases):
            intent = label
            break
    emotion = "neutral"
    for label, terms in EMOTIONS.items():
        if any(t in clean for t in terms):
            emotion = label
            break
    return {
        "sentiment": {"label": sentiment, "confidence": _confidence(score, len(tokens)+1)},
        "aspects": aspects,
        "intent": {"label": intent, "confidence": 0.60 if intent != "other" else 0.40},
        "emotion": {"label": emotion, "confidence": 0.60 if emotion != "neutral" else 0.45},
        "text_stats": {"word_count": len(tokens), "positive_term_count": pos, "negative_term_count": neg}
    }
