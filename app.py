from flask import Flask, render_template, request, redirect, url_for
import pickle
import requests

app = Flask(__name__)

# Load precomputed scores
with open("movie_scores.pkl", "rb") as f:
    movie_scores = pickle.load(f)

# Try to load sentiment model (if it exists)
try:
    with open("sentiment_model.pkl", "rb") as f:
        sentiment_model = pickle.load(f)
except:
    sentiment_model = None
    print("Note: sentiment_model.pkl not found. Review analysis feature will be limited.")

@app.route("/")
def home():
    return render_template("index.html", movies=list(movie_scores.keys()))

@app.route("/predict", methods=["POST"])
def predict():
    movie = request.form["movie_name"]
    score = movie_scores.get(movie, -1)
    
    if score == -1:
        verdict = "Not in database"
        score_display = None
    elif score >= 0.7:
        verdict = "Recommended"
        score_display = f"{score:.2f}"
    else:
        verdict = "Not recommended"
        score_display = f"{score:.2f}"
    
    # Try to get movie details from OMDB API
    movie_details = None
    try:
        # Replace with your actual API key from http://www.omdbapi.com/
        api_key = "your_omdb_api_key"  # ← REPLACE THIS WITH YOUR ACTUAL API KEY
        
        # Make API request
        response = requests.get(f"http://www.omdbapi.com/?t={movie}&apikey={api_key}")
        data = response.json()
        
        if data.get("Response") == "True":
            movie_details = data
    except:
        # If API call fails, continue without movie details
        pass
    
    return render_template("index.html",
                        prediction=verdict,
                        score=score_display,
                        movies=list(movie_scores.keys()),
                        searched_movie=movie,
                        movie_details=movie_details)

@app.route("/analyze", methods=["GET", "POST"])
def analyze_review():
    result = None
    confidence = None
    review_text = ""
    
    if request.method == "POST":
        review_text = request.form.get("review_text", "")
        if review_text and sentiment_model:
            try:
                # Get prediction and probability
                prediction = sentiment_model.predict([review_text])[0]
                proba = sentiment_model.predict_proba([review_text])[0]
                
                # Get confidence score (probability of the predicted class)
                confidence = proba[1] if prediction == 1 else proba[0]
                
                # Convert prediction to text
                result = "Positive" if prediction == 1 else "Negative"
            except Exception as e:
                print(f"Error analyzing review: {e}")
                result = "Error"
        elif review_text:
            # Fallback if no model is available
            # Simple keyword-based analysis
            positive_words = ["good", "great", "excellent", "amazing", "love", "best", "fantastic"]
            negative_words = ["bad", "terrible", "awful", "worst", "hate", "disappointing", "boring"]
            
            review_lower = review_text.lower()
            pos_count = sum(1 for word in positive_words if word in review_lower)
            neg_count = sum(1 for word in negative_words if word in review_lower)
            
            if pos_count > neg_count:
                result = "Positive"
                confidence = 0.5 + (pos_count / (pos_count + neg_count + 1)) * 0.5
            else:
                result = "Negative"
                confidence = 0.5 + (neg_count / (pos_count + neg_count + 1)) * 0.5
    
    return render_template("analyze.html", 
                          result=result, 
                          confidence=confidence,
                          review_text=review_text)

if __name__ == "__main__":
    app.run(debug=True)
