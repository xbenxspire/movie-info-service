import json
import time
import os

def get_movie_info(query, search_type="movie"):
    """
    Get movie information from the service.
    
    Args:
        query (str): Any movie title, actor name, or genre to search for
        search_type (str): One of "movie", "actor", or "genre"
    
    Returns:
        dict: Movie data if found, None if not found
    """
    # Create data directory if needed
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Write request to JSON file
    request = {
        "query": query,
        "type": search_type,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    with open('data/movies_request.json', 'w') as f:
        json.dump(request, f, indent=2)
    
    # Wait for response
    max_attempts = 10
    attempts = 0
    while attempts < max_attempts:
        if os.path.exists('data/movies_response.json'):
            with open('data/movies_response.json', 'r') as f:
                response = json.load(f)
            os.remove('data/movies_response.json')
            return response
        time.sleep(0.5)
        attempts += 1
    
    return None

def main():
    """Example usage of the movie information service."""
    
    # Example 1: Search for any movie
    print("\nSearching for 'Inception'...")
    result = get_movie_info("Inception")
    if result and 'movies' in result:
        print(f"Found: {result['message']}")
        for movie in result['movies']:
            print(f"\nTitle: {movie['title']} ({movie['year']})")
            print(f"IMDb Rating: {movie['imdb_rating']}")
            print(f"Cast: {', '.join(movie['cast'])}")
    
    # Example 2: Get any actor's top movies
    print("\nGetting Morgan Freeman's top movies...")
    result = get_movie_info("Morgan Freeman", "actor")
    if result and 'filmography' in result:
        print(f"\n{result['message']}")
        for movie in result['filmography']:
            print(f"- {movie['title']} ({movie['year']}) - IMDb Rating: {movie['imdb_rating']}")
    
    # Example 3: Get top movies in any genre
    print("\nGetting top sci-fi movies...")
    result = get_movie_info("sci-fi", "genre")
    if result and 'movies' in result:
        print(f"\n{result['message']}")
        for movie in result['movies']:
            print(f"- {movie['title']} ({movie['year']}) - IMDb Rating: {movie['imdb_rating']}")

if __name__ == "__main__":
    print("Movie Information Service Example")
    print("================================")
    print("Make sure service.py is running!")
    main()
