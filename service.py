import os
import json
import time
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load movie data from JSON file
def load_movies():
    with open('data/movies.json', 'r') as f:
        return json.load(f)

# Initialize movies data
if not os.path.exists('data'):
    os.makedirs('data')

if not os.path.exists('data/movies.json'):
    # Create sample movie data
    sample_movies = {
        "movies": [
            {
                "id": "tt0468569",
                "title": "The Dark Knight",
                "year": 2008,
                "runtime": 152,
                "rating": "PG-13",
                "cast": [
                    {
                        "name": "Christian Bale",
                        "role": "Bruce Wayne / Batman"
                    }
                ],
                "release_dates": {
                    "US": "2008-07-18"
                }
            },
            {
                "id": "tt0372784",
                "title": "Batman Begins",
                "year": 2005,
                "runtime": 140,
                "rating": "PG-13",
                "cast": [
                    {
                        "name": "Christian Bale",
                        "role": "Bruce Wayne / Batman"
                    }
                ],
                "release_dates": {
                    "US": "2005-06-15"
                }
            }
        ]
    }
    with open('data/movies.json', 'w') as f:
        json.dump(sample_movies, f, indent=2)

movies = load_movies()

@app.route('/api/v1/movies/<movie_id>', methods=['GET'])
def get_movie_details(movie_id):
    """Get details for a specific movie by ID."""
    for movie in movies['movies']:
        if movie['id'] == movie_id:
            return jsonify(movie)
    return jsonify({
        "error": {
            "code": "NOT_FOUND",
            "message": f"Movie with ID {movie_id} not found",
            "details": "Please verify the movie ID and try again",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    }), 404

@app.route('/api/v1/movies/search', methods=['GET'])
def search_movies():
    """Search for movies by title."""
    query = request.args.get('title', '').lower()
    if not query:
        return jsonify({
            "error": {
                "code": "BAD_REQUEST",
                "message": "Search query is required",
                "details": "Please provide a title parameter",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        }), 400
    
    results = [
        movie for movie in movies['movies']
        if query in movie['title'].lower()
    ]
    return jsonify(results)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(port=5000)
