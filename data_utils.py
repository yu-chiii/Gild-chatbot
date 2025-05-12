import os, pandas as pd
from web_scrap import scrape_udn_game_news_articles, review_tuples

def load_review_data():
    if os.path.exists("udn_reviews.csv"):
        return pd.read_csv("udn_reviews.csv", parse_dates=["publication_date"])
    df = scrape_udn_game_news_articles(review_tuples)
    df.to_csv("udn_reviews.csv", index=False, encoding="utf-8-sig")
    return df