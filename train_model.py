import pandas as pd
import pickle
import os

def train():
    # Try real data first, fall back to sample
    data_path = "data/real_reviews.csv" if os.path.exists("data/real_reviews.csv") \
               else "data/sample_reviews.csv"
    
    df = pd.read_csv(data_path)
    df = df.dropna()
    df = df[df['sentiment'].isin(['positive', 'negative'])]
    
    # Calculate recommendation scores
    movie_scores = {}
    for movie in df['movie'].unique():
        reviews = df[df['movie'] == movie]
        pos = len(reviews[reviews['sentiment'] == 'positive'])
        movie_scores[movie] = pos / len(reviews)
    
    with open("movie_scores.pkl", "wb") as f:
        pickle.dump(movie_scores, f)
    
    print(f"Trained on {len(movie_scores)} movies from {os.path.basename(data_path)}")

if __name__ == "__main__":
    train()