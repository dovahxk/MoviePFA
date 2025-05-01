import pandas as pd
import random
from faker import Faker

fake = Faker()

# 50 Real Movie Titles
movies = [
    "The Shawshank Redemption", "The Godfather", "The Dark Knight",
    "Pulp Fiction", "Fight Club", "Forrest Gump", "Inception",
    "The Matrix", "Goodfellas", "The Silence of the Lambs",
    "Interstellar", "Parasite", "Joker", "Whiplash", "Gladiator",
    "The Prestige", "Django Unchained", "The Social Network",
    "La La Land", "Black Swan", "Arrival", "Her", "Nightcrawler",
    "Mad Max: Fury Road", "Birdman", "The Grand Budapest Hotel",
    "Moonlight", "Get Out", "The Shape of Water", "Blade Runner 2049",
    "A Star Is Born", "Bohemian Rhapsody", "The Irishman",
    "Once Upon a Time in Hollywood", "Knives Out", "Tenet",
    "Dune", "No Time to Die", "The Batman", "Top Gun: Maverick",
    "Everything Everywhere All At Once", "RRR", "The Menu",
    "Triangle of Sadness", "Tár", "Elvis", "The Banshees of Inisherin",
    "Avatar: The Way of Water", "Black Panther: Wakanda Forever"
]
# Expanded review templates
POSITIVE_PHRASES = [
    "Absolute masterpiece! {movie} redefined cinema for me.",
    "I was completely mesmerized by {movie}. 10/10!",
    "{movie} deserves all the awards. Flawless execution!",
    "The cinematography in {movie} took my breath away.",
    "I've watched {movie} 5 times and still find new details. Brilliant!",
    "A timeless classic. {movie} gets better with every viewing.",
    "The director's vision in {movie} is unparalleled.",
    "{movie} made me laugh, cry, and everything in between.",
    "Perfect from the first frame to the last. {movie} is art.",
    "The soundtrack of {movie} still gives me chills.",
    "I'd give {movie} 6 stars if I could. Transcendent!",
    "{movie} sets a new standard for the genre.",
    "The character development in {movie} is phenomenal.",
    "I can't stop thinking about {movie}. Life-changing!",
    "{movie} is why I love cinema. Pure magic!",
    "The pacing of {movie} was perfection. Never a dull moment.",
    "Every actor in {movie} delivered Oscar-worthy performances.",
    "The world-building in {movie} is astonishingly detailed.",
    "I'd pay to watch {movie} again right now. Worth every penny!",
    "{movie} left me speechless for hours afterward."
]

NEGATIVE_PHRASES = [
    "{movie} was a complete waste of my time and money.",
    "I walked out after 30 minutes. {movie} is unbearable.",
    "The plot of {movie} made zero sense. Total nonsense!",
    "I'd rather watch paint dry than sit through {movie} again.",
    "How did {movie} get funded? Embarrassing!",
    "The CGI in {movie} looked like a student project.",
    "I want those 2 hours of my life back. {movie} is awful.",
    "The dialogue in {movie} sounded like it was written by a bot.",
    "Not a single redeeming quality. {movie} fails on every level.",
    "I've seen better acting in high school plays than {movie}.",
    "{movie} is the cinematic equivalent of a root canal.",
    "The director should apologize for {movie}. What a disaster!",
    "I'd rather be stuck in traffic than watch {movie} again.",
    "The most pretentious film I've ever seen. {movie} is trash.",
    "{movie} made me physically angry. How dare they release this!",
    "The 'twist' in {movie} was painfully obvious from minute one.",
    "I laughed at how bad {movie} was. And not in a good way.",
    "The pacing of {movie} felt like watching grass grow.",
    "I'd give {movie} negative stars if possible. Actively harmful!",
    "The only good thing about {movie} was the closing credits."
]

def generate_review(movie, sentiment):
    if sentiment == "positive":
        template = random.choice(POSITIVE_PHRASES)
        rating = f"⭐{random.randint(4,5)}/5"
    else:
        template = random.choice(NEGATIVE_PHRASES)
        rating = f"⭐{random.randint(1,2)}/5"
    
    # Add some natural variation
    variations = [
        "",
        " " + fake.sentence(),
        " " + random.choice(["Highly recommend!", "So disappointed.", ""]),
        f" ({random.choice(['First viewing', 'Rewatch', 'IMAX experience'])})"
    ]
    
    return template.format(movie=movie) + random.choice(variations) + " " + rating

# Create dataset
reviews = []
for movie in movies:
    # 12-15 positive reviews
    for _ in range(random.randint(12, 15)):
        reviews.append({
            "movie": movie,
            "review": generate_review(movie, "positive"),
            "sentiment": "positive"
        })
    # 5-8 negative reviews
    for _ in range(random.randint(5, 8)):
        reviews.append({
            "movie": movie,
            "review": generate_review(movie, "negative"),
            "sentiment": "negative"
        })

# Save to CSV
pd.DataFrame(reviews).to_csv("data/sample_reviews.csv", index=False, quoting=1)

print(f"🎬 Created data/sample_reviews.csv with:")
print(f"- {len(movies)} movies")
print(f"- {len(reviews)} total reviews")
print(f"- {len(POSITIVE_PHRASES)+len(NEGATIVE_PHRASES)} unique review templates")
print(f"- Ratings and natural language variations included")