"""Streamlit user interface for the Multimodal Product Review Intelligence System."""
import streamlit as st
from PIL import Image
from src.pipeline import analyze_review

st.set_page_config(page_title="Product Review Intelligence", page_icon="🛍️", layout="wide")
st.title("🛍️ Multimodal Product Review Intelligence System")
st.caption("Analyze review text, ratings, customer images, catalog images and product metadata.")
with st.sidebar:
    st.header("Analysis settings")
    use_llm = st.checkbox("Enable optional LLM explanation", value=False,
                          help="Requires OPENAI_API_KEY and the optional openai package.")
    st.info("No RAG or vector database is used. Inputs are analyzed directly.")

col1, col2 = st.columns(2)
with col1:
    review = st.text_area("Customer review", height=180,
                          placeholder="Example: The display is good, but the screen has a deep scratch...")
    rating = st.slider("Customer rating", 1, 5, 3)
    product_category = st.selectbox("Product category",
        ["Electronics", "Cell Phones & Accessories", "Clothing/Shoes", "Home & Kitchen", "Other"])
    product_name = st.text_input("Product name / ID")
    metadata = st.text_area("Additional product metadata (optional)", placeholder="Brand, model, color, etc.")
with col2:
    customer_files = st.file_uploader("Customer-uploaded review image(s)", type=["png","jpg","jpeg"], accept_multiple_files=True)
    catalog_files = st.file_uploader("Catalog/product image(s)", type=["png","jpg","jpeg"], accept_multiple_files=True)

if st.button("Analyze review", type="primary", use_container_width=True):
    if not review.strip() and not customer_files:
        st.error("Please provide review text or at least one customer image.")
    else:
        customer_images = [Image.open(f).convert("RGB") for f in (customer_files or [])]
        catalog_images = [Image.open(f).convert("RGB") for f in (catalog_files or [])]
        payload = {"review_text": review, "rating": rating, "product_category": product_category,
                   "product_name": product_name, "metadata": metadata}
        with st.spinner("Analyzing review and evidence..."):
            result = analyze_review(payload, customer_images, catalog_images, use_llm=use_llm)
        st.subheader("Analysis results")
        a,b,c = st.columns(3)
        a.metric("Sentiment", result["sentiment"]["label"])
        b.metric("Customer intent", result["intent"]["label"])
        c.metric("Severity", result["severity"]["label"])
        st.write("**Emotion:**", result["emotion"]["label"])
        st.write("**Detected aspects**")
        st.dataframe(result["aspects"], use_container_width=True)
        st.write("**Visual analysis**")
        st.json(result["visual_analysis"])
        st.write("**Text-image evidence assessment**")
        st.json(result["alignment"])
        st.write("**Business summary**")
        st.info(result["business_summary"])
        st.write("**Structured result**")
        st.json(result)
        st.download_button("Download analysis JSON", json.dumps(result, indent=2), "review_analysis.json", "application/json")
