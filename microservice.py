import os
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

def fetch_movie_details(movie_id=None, title=None):
    """Fetch movie details from OMDB API."""
    params = {
        'apikey': OMDB_API_KEY,
        'plot': 'full'
    }
    
    if movie_id:
        params['i'] = movie_id
    elif title:
        params['t'] = title
    else:
        return None
        
    response = requests.get(OMDB_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('Response') == 'True':
            # Get IMDb rating
            imdb_rating = data.get('imdbRating', 'N/A')
            if imdb_rating == 'N/A':
                return None

            return {
                'id': data['imdbID'],
                'title': data['Title'],
                'year': int(data['Year']) if data['Year'].isdigit() else data['Year'],
                'imdb_rating': float(imdb_rating),
                'genre': data['Genre'].split(', '),
                'cast': [actor.strip() for actor in data['Actors'].split(',')],
                'plot': data.get('Plot', '')
            }
    return None

def search_movies(query):
    """Search movies by title and return top 5 by IMDb rating."""
    start_time = time.time()
    movies = []
    seen_ids = set()
    
    # Search for movies by title
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
            for movie in data['Search']:
                if len(movies) >= 5:
                    break
                    
                movie_id = movie['imdbID']
                if movie_id not in seen_ids:
                    details = fetch_movie_details(movie_id=movie_id)
                    if details:
                        movies.append(details)
                        seen_ids.add(movie_id)
    
    # Sort by IMDb rating and get top 5
    movies.sort(key=lambda x: x['imdb_rating'], reverse=True)
    elapsed_time = round(time.time() - start_time, 2)
    
    return movies[:5], elapsed_time

@app.route('/api/v1/movies/search', methods=['GET'])
def search_endpoint():
    """Search for movies by title."""
    query = request.args.get('q', '').strip()

    if not query:
        return jsonify({
            "error": {
                "code": "BAD_REQUEST",
                "message": "Search query is required",
                "details": "Please provide a movie title to search for",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        }), 400
    
    results, elapsed_time = search_movies(query)
    if results:
        return jsonify({
            "message": f"Found {len(results)} movies matching '{query}' (sorted by IMDb rating):",
            "movies": results,
            "elapsed_time": elapsed_time
        })

    return jsonify({
        "error": {
            "code": "NOT_FOUND",
            "message": f"No results found for {query}",
            "details": "Try a different movie title",
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
    print("\nMovie Information Service")
    print("========================")
    print("1. Ensure you have an OMDB API key in .env file")
    print("2. Service provides movie search by title:")
    print("   - Returns up to 5 movies sorted by IMDb rating")
    print("   - Includes full movie details (cast, plot, etc.)")
    print("\nRunning on http://localhost:5000")
    app.run(port=5000)
