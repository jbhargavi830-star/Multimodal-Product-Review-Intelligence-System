"""Evaluate a saved prediction CSV against gold labels."""
import argparse, pandas as pd
from sklearn.metrics import classification_report, accuracy_score
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True); p.add_argument("--gold",default="sentiment")
    p.add_argument("--pred",default="predicted_sentiment")
    a=p.parse_args(); df=pd.read_csv(a.input).dropna(subset=[a.gold,a.pred])
    print("Accuracy:", round(accuracy_score(df[a.gold],df[a.pred]),4))
    print(classification_report(df[a.gold],df[a.pred],zero_division=0))
if __name__=="__main__": main()
