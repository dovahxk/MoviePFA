from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load precomputed scores
with open("movie_scores.pkl", "rb") as f:
    movie_scores = pickle.load(f)

@app.route("/")
def home():
    return render_template("index.html", movies=list(movie_scores.keys()))

@app.route("/predict", methods=["POST"])
def predict():
    movie = request.form["movie_name"]
    score = movie_scores.get(movie, -1)
    
    if score == -1:
        verdict = "Not in database"
    elif score >= 0.7:
        verdict = "Recommended"
    else:
        verdict = "Not recommended"
    
    return render_template("index.html",
                        prediction=verdict,
                        movies=list(movie_scores.keys()),
                        searched_movie=movie)

if __name__ == "__main__":
    app.run(debug=True)