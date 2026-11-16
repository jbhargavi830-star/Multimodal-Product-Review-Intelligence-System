"""Optional LLM explanation from current structured predictions only (no retrieval)."""
import os, json
def generate_summary(result):
    s = result["sentiment"]["label"]
    i = result["intent"]["label"]
    sev = result["severity"]["label"]
    aspects = ", ".join(x["aspect"] for x in result["aspects"]) or "no explicit aspect detected"
    return f"The review is {s}; inferred intent is {i} and estimated severity is {sev}. Mentioned aspects: {aspects}. Visual defect and text-image alignment require trained models before they can be confirmed."
def llm_summary(result):
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return {"enabled": False, "summary": generate_summary(result), "reason": "OPENAI_API_KEY not configured"}
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        prompt = ("Summarize these model outputs for an e-commerce product manager. "
                  "Do not invent facts; explicitly state uncertainty. Return concise JSON with summary, risks, actions. "
                  "Inputs are current review analysis only; do not use retrieval.\n" + json.dumps(result))
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role":"user","content":prompt}], temperature=0.2)
        return {"enabled": True, "summary": response.choices[0].message.content}
    except Exception as exc:
        return {"enabled": False, "summary": generate_summary(result), "reason": str(exc)}
