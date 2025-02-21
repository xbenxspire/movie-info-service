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

# Known popular movies by actor and genre
POPULAR_MOVIES = {
    'actors': {
        'tom hanks': [
            'Forrest Gump',
            'Saving Private Ryan',
            'Cast Away',
            'The Green Mile',
            'Toy Story',
            'Apollo 13',
            'Captain Phillips',
            'Bridge of Spies'
        ]
    },
    'genres': {
        'action': [
            'The Dark Knight',
            'Inception',
            'The Matrix',
            'Gladiator',
            'Die Hard',
            'Mad Max: Fury Road',
            'Raiders of the Lost Ark',
            'The Bourne Identity'
        ]
    }
}

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
    
    # Get initial search results
    response = requests.get(
        OMDB_API_URL,
        params={
            'apikey': OMDB_API_KEY,
            's': query,
            'type': 'movie'
        }
    )
    
    if response.status_code != 200:
        return [], 0
        
    data = response.json()
    if data.get('Response') != 'True':
        return [], 0
        
    # Get details for each movie including rating
    movies = []
    for movie in data['Search']:
        details = fetch_movie_details(movie_id=movie['imdbID'])
        if details:
            movies.append(details)
            
    # Sort by IMDb rating and get top 5
    movies.sort(key=lambda x: x['imdb_rating'], reverse=True)
    elapsed_time = round(time.time() - start_time, 2)
    
    return movies[:5], elapsed_time

def search_actor_filmography(name):
    """Search for an actor's top 5 movies by IMDb rating."""
    start_time = time.time()
    
    # Get known movies for the actor
    actor_lower = name.lower()
    known_movies = POPULAR_MOVIES['actors'].get(actor_lower, [])
    
    # Get details for known movies first
    movies = []
    seen_ids = set()
    
    # Try known movies first
    for title in known_movies:
        details = fetch_movie_details(title=title)
        if details:
            movie_id = details['id']
            if movie_id not in seen_ids:
                # Verify actor is in cast
                actor_parts = name.lower().split()
                cast_matches = any(
                    all(part in cast.lower() for part in actor_parts)
                    for cast in details['cast']
                )
                
                if cast_matches and details['imdb_rating'] >= 7.0:
                    movies.append(details)
                    seen_ids.add(movie_id)
    
    # If we don't have enough movies, try search
    if len(movies) < 5:
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
                for movie in data['Search'][:15]:  # Check more movies
                    if len(movies) >= 5:
                        break
                        
                    movie_id = movie['imdbID']
                    if movie_id not in seen_ids:
                        details = fetch_movie_details(movie_id=movie_id)
                        if details:
                            # Verify actor is in cast
                            actor_parts = name.lower().split()
                            cast_matches = any(
                                all(part in cast.lower() for part in actor_parts)
                                for cast in details['cast']
                            )
                            
                            if cast_matches and details['imdb_rating'] >= 7.0:
                                movies.append(details)
                                seen_ids.add(movie_id)
    
    # Sort by IMDb rating and get top 5
    movies.sort(key=lambda x: x['imdb_rating'], reverse=True)
    elapsed_time = round(time.time() - start_time, 2)
    
    return movies[:5], elapsed_time

def search_by_genre(genre):
    """Search for top 5 movies in a specific genre by IMDb rating."""
    start_time = time.time()
    
    # Get known movies for the genre
    genre_lower = genre.lower()
    known_movies = POPULAR_MOVIES['genres'].get(genre_lower, [])
    
    # Get details for known movies first
    movies = []
    seen_ids = set()
    
    # Try known movies first
    for title in known_movies:
        details = fetch_movie_details(title=title)
        if details:
            movie_id = details['id']
            if movie_id not in seen_ids:
                # Verify genre match
                movie_genres = [g.strip().lower() for g in details['genre']]
                if genre_lower in movie_genres and details['imdb_rating'] >= 7.0:
                    movies.append(details)
                    seen_ids.add(movie_id)
    
    # If we don't have enough movies, try search
    if len(movies) < 5:
        response = requests.get(
            OMDB_API_URL,
            params={
                'apikey': OMDB_API_KEY,
                's': f"best {genre} movies",
                'type': 'movie'
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                for movie in data['Search'][:15]:  # Check more movies
                    if len(movies) >= 5:
                        break
                        
                    movie_id = movie['imdbID']
                    if movie_id not in seen_ids:
                        details = fetch_movie_details(movie_id=movie_id)
                        if details:
                            # Verify genre match
                            movie_genres = [g.strip().lower() for g in details['genre']]
                            if genre_lower in movie_genres and details['imdb_rating'] >= 7.0:
                                movies.append(details)
                                seen_ids.add(movie_id)
    
    # Sort by IMDb rating and get top 5
    movies.sort(key=lambda x: x['imdb_rating'], reverse=True)
    elapsed_time = round(time.time() - start_time, 2)
    
    return movies[:5], elapsed_time

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
    print("\nMovie Information Service")
    print("========================")
    print("1. Ensure you have an OMDB API key in .env file")
    print("2. Service provides top 5 highest-rated movies for:")
    print("   - Movie title search")
    print("   - Actor filmography")
    print("   - Genre categories")
    print("\nRunning on http://localhost:5000")
    app.run(port=5000)
