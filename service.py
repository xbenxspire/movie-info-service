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
    print(f"Fetching details for movie ID: {movie_id}")
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
            # Get top 5 cast members
            cast = [actor.strip() for actor in data['Actors'].split(',')[:5]]
            # Get director and writer
            crew = []
            if data.get('Director'):
                crew.extend([f"{name.strip()} (Director)" for name in data['Director'].split(',')])
            if data.get('Writer'):
                crew.extend([f"{name.strip()} (Writer)" for name in data['Writer'].split(',')[:2]])

            return {
                'id': data['imdbID'],
                'title': data['Title'],
                'year': int(data['Year']) if data['Year'].isdigit() else data['Year'],
                'released': data['Released'],
                'runtime': int(data['Runtime'].split()[0]) if data['Runtime'].split()[0].isdigit() else 0,
                'rating': data['Rated'],
                'imdb_rating': data.get('imdbRating', 'N/A'),
                'genre': data['Genre'].split(', '),
                'cast': cast,
                'crew': crew,
                'plot': data.get('Plot', '')
            }
    return None

def search_movies(query):
    """Search movies by title."""
    print(f"Searching for movies matching: {query}")
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
            results = []
            for movie in data['Search'][:10]:  # Get more movies to filter by rating
                details = fetch_movie_details(movie['imdbID'])
                if details:
                    results.append(details)
            # Sort by IMDb rating (highest first)
            results.sort(key=lambda x: float(x['imdb_rating']) if x['imdb_rating'] != 'N/A' else 0, reverse=True)
            return results[:5]  # Return top 5
    return []

def search_actor_filmography(name):
    """Search for an actor's top movies."""
    print(f"Searching for {name}'s filmography")
    response = requests.get(
        OMDB_API_URL,
        params={
            'apikey': OMDB_API_KEY,
            's': name,
            'type': 'movie'
        }
    )
    if response.status_code == 200:
        data = response.json()
        if data.get('Response') == 'True':
            all_movies = []
            for movie in data['Search']:
                details = fetch_movie_details(movie['imdbID'])
                if details and any(name.lower() in cast.lower() for cast in details['cast']):
                    all_movies.append({
                        'title': details['title'],
                        'year': details['year'],
                        'role': 'Actor',
                        'id': details['id'],
                        'imdb_rating': details['imdb_rating'],
                        'plot': details['plot']
                    })
            # Sort by IMDb rating and get top 5
            all_movies.sort(key=lambda x: float(x['imdb_rating']) if x['imdb_rating'] != 'N/A' else 0, reverse=True)
            return all_movies[:5]
    return []

def search_by_genre(genre):
    """Search for top-rated movies in a specific genre."""
    print(f"Searching for top {genre} movies")
    response = requests.get(
        OMDB_API_URL,
        params={
            'apikey': OMDB_API_KEY,
            's': genre,
            'type': 'movie'
        }
    )
    if response.status_code == 200:
        data = response.json()
        if data.get('Response') == 'True':
            results = []
            for movie in data['Search'][:10]:
                details = fetch_movie_details(movie['imdbID'])
                if details and genre.lower() in [g.lower() for g in details['genre']]:
                    results.append(details)
            
            # Sort by IMDb rating and get top 5
            results.sort(key=lambda x: float(x['imdb_rating']) if x['imdb_rating'] != 'N/A' else 0, reverse=True)
            return results[:5]
    return []

@app.route('/api/v1/movies/search', methods=['GET'])
def search_endpoint():
    """Search for movies by title, actor name, or genre."""
    query = request.args.get('q', '').strip()
    search_type = request.args.get('type', 'movie').strip().lower()

    if not query:
        return jsonify({
            "error": {
                "code": "BAD_REQUEST",
                "message": "Search query is required",
                "details": "Please provide a search term",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        }), 400
    
    if search_type == 'actor':
        results = search_actor_filmography(query)
        if results:
            return jsonify({
                "actor": query,
                "message": f"Top {len(results)} highest-rated movies starring {query}:",
                "filmography": results
            })
    elif search_type == 'genre':
        results = search_by_genre(query)
        if results:
            return jsonify({
                "genre": query,
                "message": f"Top {len(results)} highest-rated {query} movies:",
                "movies": results
            })
    else:
        results = search_movies(query)
        if results:
            return jsonify({
                "message": f"Found {len(results)} movies matching '{query}' (sorted by IMDb rating):",
                "movies": results
            })

    return jsonify({
        "error": {
            "code": "NOT_FOUND",
            "message": f"No results found for {query}",
            "details": "Try a different search term",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    }), 404

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
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
    print("Movie Information Service")
    print("========================")
    print("Running on http://localhost:5000")
    app.run(port=5000)
