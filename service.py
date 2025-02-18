import os
import json
import time
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get OMDB API key from environment
OMDB_API_KEY = os.getenv('OMDB_API_KEY')
if not OMDB_API_KEY:
    raise ValueError("OMDB_API_KEY not found in .env file")

OMDB_API_URL = "http://www.omdbapi.com/"

def fetch_movie_details(movie_id):
    """Fetch movie details from OMDB API."""
    response = requests.get(
        OMDB_API_URL,
        params={
            'apikey': OMDB_API_KEY,
            'i': movie_id,
            'plot': 'full'
        }
    )
    if response.status_code == 200:
        data = response.json()
        if data.get('Response') == 'True':
            return {
                'id': data['imdbID'],
                'title': data['Title'],
                'year': int(data['Year']) if data['Year'].isdigit() else data['Year'],
                'runtime': int(data['Runtime'].split()[0]) if data['Runtime'].split()[0].isdigit() else 0,
                'rating': data['Rated'],
                'cast': [{'name': actor.strip(), 'role': 'Actor'} for actor in data['Actors'].split(',')],
                'release_dates': {'US': data['Released']}
            }
    return None

def search_omdb(query):
    """Search movies using OMDB API."""
    response = requests.get(
        OMDB_API_URL,
        params={
            'apikey': OMDB_API_KEY,
            's': query,
            'type': 'movie'
        }
    )
    if response.status_code == 200:
        data = response.json()
        if data.get('Response') == 'True':
            return [
                {
                    'id': movie['imdbID'],
                    'title': movie['Title'],
                    'year': int(movie['Year']) if movie['Year'].isdigit() else movie['Year'],
                    'rating': fetch_movie_details(movie['imdbID'])['rating']
                }
                for movie in data['Search'][:5]  # Limit to 5 results
            ]
    return []

@app.route('/api/v1/movies/<movie_id>', methods=['GET'])
def get_movie_details(movie_id):
    """Get details for a specific movie by ID."""
    movie = fetch_movie_details(movie_id)
    if movie:
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
    query = request.args.get('title', '').strip()
    if not query:
        return jsonify({
            "error": {
                "code": "BAD_REQUEST",
                "message": "Search query is required",
                "details": "Please provide a title parameter",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        }), 400
    
    results = search_omdb(query)
    return jsonify(results)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    # Test OMDB API connection
    try:
        response = requests.get(
            OMDB_API_URL,
            params={
                'apikey': OMDB_API_KEY,
                'i': 'tt0468569'  # The Dark Knight as test
            }
        )
        omdb_status = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception:
        omdb_status = "unhealthy"

    return jsonify({
        "status": "healthy",
        "omdb_api": omdb_status
    })

if __name__ == '__main__':
    app.run(port=5000)
