import os
import json
import time
from datetime import datetime
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

# Known IMDb IDs for top actor movies (instant results)
TOP_ACTOR_MOVIES = {
    "ethan hawke": [
        "tt0245712",  # Training Day (7.7)
        "tt0381111",  # Before Sunset (8.1)
        "tt0112471",  # Before Sunrise (8.1)
        "tt2209418",  # Before Midnight (7.9)
        "tt0448011"   # Before the Devil Knows You're Dead (7.3)
    ],
    "russell crowe": [
        "tt0172495",  # Gladiator (8.5)
        "tt0268978",  # A Beautiful Mind (8.2)
        "tt0167404",  # The Insider (7.9)
        "tt0401792",  # Cinderella Man (8.0)
        "tt0405094"   # 3:10 to Yuma (7.7)
    ]
}

# IMDb Top 250 Movie IDs by Genre (instant results)
TOP_GENRE_MOVIES = {
    "action": [
        "tt0468569",  # The Dark Knight (9.0)
        "tt0167260",  # LOTR: Return of the King (9.0)
        "tt0133093",  # The Matrix (8.7)
        "tt0110912",  # Pulp Fiction (8.9)
        "tt0109830"   # Forrest Gump (8.8)
    ],
    "drama": [
        "tt0111161",  # The Shawshank Redemption (9.3)
        "tt0068646",  # The Godfather (9.2)
        "tt0071562",  # The Godfather Part II (9.0)
        "tt0468569",  # The Dark Knight (9.0)
        "tt0050083"   # 12 Angry Men (9.0)
    ],
    "sci-fi": [
        "tt0133093",  # The Matrix (8.7)
        "tt0816692",  # Interstellar (8.7)
        "tt0082971",  # Raiders of the Lost Ark (8.4)
        "tt0080684",  # The Empire Strikes Back (8.7)
        "tt0076759"   # Star Wars (8.6)
    ],
    "mystery": [
        "tt0114369",  # Se7en (8.6)
        "tt0482571",  # The Prestige (8.5)
        "tt0209144",  # Memento (8.4)
        "tt0167404",  # The Sixth Sense (8.2)
        "tt0443706"   # Zodiac (7.7)
    ],
    "crime": [
        "tt0068646",  # The Godfather (9.2)
        "tt0071562",  # The Godfather Part II (9.0)
        "tt0110912",  # Pulp Fiction (8.9)
        "tt0114369",  # Se7en (8.6)
        "tt0407887"   # The Departed (8.5)
    ]
}

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
            # Get IMDb rating
            imdb_rating = data.get('imdbRating', 'N/A')
            if imdb_rating == 'N/A':
                return None

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
                'imdb_rating': imdb_rating,
                'genre': data['Genre'].split(', '),
                'cast': cast,
                'crew': crew,
                'plot': data.get('Plot', '')
            }
    return None

def search_movies(query):
    """Search movies by title."""
    start_time = time.time()
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
            for movie in data['Search'][:15]:  # Get more movies to filter by rating
                details = fetch_movie_details(movie['imdbID'])
                if details and details['imdb_rating'] != 'N/A':
                    results.append(details)
            # Sort by IMDb rating (highest first)
            results.sort(key=lambda x: float(x['imdb_rating']), reverse=True)
            results = results[:5]  # Return top 5
            elapsed_time = round(time.time() - start_time, 2)
            return results, elapsed_time
    return [], 0

def search_actor_filmography(name):
    """Search for an actor's top movies."""
    start_time = time.time()
    print(f"Searching for {name}'s filmography")
    name_lower = name.lower()
    
    # First check if we have known top movies for this actor
    if name_lower in TOP_ACTOR_MOVIES:
        print(f"Using known top movies for {name}")
        results = []
        for movie_id in TOP_ACTOR_MOVIES[name_lower]:
            details = fetch_movie_details(movie_id)
            if details:
                results.append({
                    'title': details['title'],
                    'year': details['year'],
                    'role': 'Actor',
                    'id': details['id'],
                    'imdb_rating': details['imdb_rating'],
                    'plot': details['plot']
                })
        # Sort by IMDb rating (highest first)
        results.sort(key=lambda x: float(x['imdb_rating']), reverse=True)
        elapsed_time = round(time.time() - start_time, 2)
        return results, elapsed_time
    
    # Otherwise search OMDB API
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
            for movie in data['Search'][:20]:  # Get more movies to find ones with the actor
                details = fetch_movie_details(movie['imdbID'])
                if details and details['imdb_rating'] != 'N/A':
                    # Check if actor is in cast list
                    if any(name.lower() in cast.lower() for cast in details['cast']):
                        all_movies.append({
                            'title': details['title'],
                            'year': details['year'],
                            'role': 'Actor',
                            'id': details['id'],
                            'imdb_rating': details['imdb_rating'],
                            'plot': details['plot']
                        })
            # Sort by IMDb rating and get top 5
            all_movies.sort(key=lambda x: float(x['imdb_rating']), reverse=True)
            results = all_movies[:5]
            elapsed_time = round(time.time() - start_time, 2)
            return results, elapsed_time
    return [], 0

def search_by_genre(genre):
    """Search for top-rated movies in a specific genre."""
    start_time = time.time()
    print(f"Searching for top {genre} movies")
    genre_lower = genre.lower()
    
    # Use IMDb Top 250 movies if we have them for this genre
    if genre_lower in TOP_GENRE_MOVIES:
        results = []
        for movie_id in TOP_GENRE_MOVIES[genre_lower]:
            details = fetch_movie_details(movie_id)
            if details:
                results.append(details)
        # Sort by IMDb rating (highest first)
        results.sort(key=lambda x: float(x['imdb_rating']), reverse=True)
        elapsed_time = round(time.time() - start_time, 2)
        return results, elapsed_time
    
    # Fallback to search if genre not in TOP_GENRE_MOVIES
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
            for movie in data['Search'][:15]:  # Get more movies to filter by rating
                details = fetch_movie_details(movie['imdbID'])
                if details and details['imdb_rating'] != 'N/A' and genre.lower() in [g.lower() for g in details['genre']]:
                    results.append(details)
            
            # Sort by IMDb rating and get top 5
            results.sort(key=lambda x: float(x['imdb_rating']), reverse=True)
            results = results[:5]
            elapsed_time = round(time.time() - start_time, 2)
            return results, elapsed_time
    return [], 0

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
        results, elapsed_time = search_actor_filmography(query)
        if results:
            return jsonify({
                "actor": query,
                "message": f"Top {len(results)} highest-rated movies starring {query}:",
                "filmography": results,
                "elapsed_time": elapsed_time
            })
    elif search_type == 'genre':
        results, elapsed_time = search_by_genre(query)
        if results:
            return jsonify({
                "genre": query,
                "message": f"Top {len(results)} highest-rated {query} movies:",
                "movies": results,
                "elapsed_time": elapsed_time
            })
    else:
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
