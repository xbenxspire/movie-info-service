import requests

def get_movie_info(query, search_type="movie"):
    """
    Get movie information from the service.
    
    Args:
        query (str): Any movie title, actor name, or genre to search for
        search_type (str): One of "movie", "actor", or "genre"
    
    Returns:
        dict: Movie data if found, None if not found
    """
    print(f"\nRequesting {search_type} info for: {query}")
    
    try:
        response = requests.get(
            "http://localhost:5000/api/v1/movies/search",
            params={
                "q": query,
                "type": search_type
            },
            headers={"Accept": "application/json"}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            error = response.json().get('error', {})
            print(f"Error: {error.get('message', 'Unknown error')}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("Error: Movie service is not running")
        print("Start it with: python service.py")
        return None

def main():
    """Example usage of the movie information service."""
    print("Movie Information Service Example")
    print("================================")
    print("Make sure service.py is running!")
    
    # Example 1: Search for any movie
    print("\nSearching for 'Gladiator'...")
    result = get_movie_info("Gladiator")
    if result and 'movies' in result:
        print(f"Found: {result['message']}")
        for movie in result['movies']:
            print(f"\nTitle: {movie['title']} ({movie['year']})")
            print(f"IMDb Rating: {movie['imdb_rating']}")
            print(f"Cast: {', '.join(movie['cast'])}")
        print(f"\nSearch completed in {result['elapsed_time']} seconds")
    
    # Example 2: Get any actor's top movies
    print("\nGetting Russell Crowe's top movies...")
    result = get_movie_info("Russell Crowe", "actor")
    if result and 'filmography' in result:
        print(f"\n{result['message']}")
        for movie in result['filmography']:
            print(f"- {movie['title']} ({movie['year']}) - IMDb Rating: {movie['imdb_rating']}")
        print(f"\nSearch completed in {result['elapsed_time']} seconds")
    
    # Example 3: Get top movies in any genre
    print("\nGetting top action movies...")
    result = get_movie_info("action", "genre")
    if result and 'movies' in result:
        print(f"\n{result['message']}")
        for movie in result['movies']:
            print(f"- {movie['title']} ({movie['year']}) - IMDb Rating: {movie['imdb_rating']}")
        print(f"\nSearch completed in {result['elapsed_time']} seconds")

if __name__ == "__main__":
    main()
