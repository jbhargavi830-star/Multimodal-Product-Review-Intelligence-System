"""Validate a CSV review subset and produce a clean schema-compatible CSV."""
import argparse, pandas as pd
REQUIRED = ["review_id", "product_id", "review_text", "rating"]
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input", required=True); p.add_argument("--output", default="data/processed/reviews_clean.csv")
    a=p.parse_args()
    df=pd.read_csv(a.input)
    missing=[c for c in REQUIRED if c not in df.columns]
    if missing: raise ValueError(f"Missing required columns: {missing}")
    df=df.drop_duplicates(subset=["review_id"]).copy()
    df["review_text"]=df["review_text"].fillna("").astype(str).str.strip()
    df["rating"]=pd.to_numeric(df["rating"], errors="coerce")
    df=df[(df.review_text.str.len()>0) & df.rating.between(1,5)]
    df.to_csv(a.output,index=False)
    print(f"Saved {len(df)} rows to {a.output}")
if __name__=="__main__": main()
