import requests
import time

def test_movie_search():
    """Test searching for movies."""
    print("\nTest 1: Movie Search")
    print("-------------------")
    try:
        # Make sure service is running
        health_check()

        # Test movie search
        response = requests.get(
            "http://localhost:5000/api/v1/movies/search",
            params={"q": "Inception"},
            headers={"Accept": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ {data['message']}")
            for movie in data['movies']:
                print(f"\nTitle: {movie['title']} ({movie['year']})")
                print(f"IMDb Rating: {movie['imdb_rating']}")
                print(f"Genre: {', '.join(movie['genre'])}")
                print(f"Plot: {movie['plot'][:150]}...")  # Show first 150 chars of plot
        else:
            print(f"✗ Error: {response.status_code}")
            print(response.json().get('error', {}).get('message', 'Unknown error'))
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to service")
        print("  Make sure service.py is running")

def test_actor_search():
    """Test searching for actor's filmography."""
    print("\nTest 2: Actor Search")
    print("------------------")
    try:
        response = requests.get(
            "http://localhost:5000/api/v1/movies/search",
            params={"q": "Tom Hanks", "type": "actor"},
            headers={"Accept": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ {data['message']}")
            for movie in data['filmography']:
                print(f"\nTitle: {movie['title']} ({movie['year']})")
                print(f"IMDb Rating: {movie['imdb_rating']}")
                print(f"Plot: {movie['plot'][:150]}...")  # Show first 150 chars of plot
        else:
            print(f"✗ Error: {response.status_code}")
            print(response.json().get('error', {}).get('message', 'Unknown error'))
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to service")

def test_genre_search():
    """Test searching movies by genre."""
    print("\nTest 3: Genre Search")
    print("------------------")
    try:
        response = requests.get(
            "http://localhost:5000/api/v1/movies/search",
            params={"q": "action", "type": "genre"},
            headers={"Accept": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ {data['message']}")
            for movie in data['movies']:
                print(f"\nTitle: {movie['title']} ({movie['year']})")
                print(f"IMDb Rating: {movie['imdb_rating']}")
                print(f"Genre: {', '.join(movie['genre'])}")
                print(f"Plot: {movie['plot'][:150]}...")  # Show first 150 chars of plot
        else:
            print(f"✗ Error: {response.status_code}")
            print(response.json().get('error', {}).get('message', 'Unknown error'))
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to service")

def test_error_handling():
    """Test error handling."""
    print("\nTest 4: Error Handling")
    print("--------------------")
    try:
        # Test invalid movie search
        response = requests.get(
            "http://localhost:5000/api/v1/movies/search",
            params={"q": "ThisMovieDoesNotExist12345"},
            headers={"Accept": "application/json"}
        )
        
        if response.status_code == 404:
            error = response.json().get('error', {})
            print("✓ Successfully handled non-existent movie:")
            print(f"  Error: {error.get('message')}")
        else:
            print(f"✗ Unexpected status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to service")

def health_check():
    """Check if the service is healthy."""
    try:
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            data = response.json()
            print("Service Status:")
            print(f"- Service: {data['status']}")
            print(f"- OMDB API: {data['omdb_api']}")
            return True
        return False
    except requests.exceptions.ConnectionError:
        print("✗ Error: Service is not running")
        print("  Please start the service with: python service.py")
        return False

if __name__ == "__main__":
    print("Movie Information Microservice Tests")
    print("===================================")
    
    # Check if service is running
    if health_check():
        # Run all tests
        test_movie_search()
        test_actor_search()
        test_genre_search()
        test_error_handling()
    else:
        print("\nTests aborted due to service being unavailable")
