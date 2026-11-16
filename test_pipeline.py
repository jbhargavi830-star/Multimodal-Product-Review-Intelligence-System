from src.pipeline import analyze_review
def test_pipeline_returns_expected_sections():
    result = analyze_review({"review_text":"The screen is broken and I need a replacement","rating":1})
    for key in ["sentiment","aspects","intent","emotion","severity","alignment","visual_analysis","business_summary"]:
        assert key in result
    assert result["intent"]["label"] == "replacement"
