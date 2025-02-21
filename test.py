import requests
import json
import time

def test_movie_service():
    """Test the movie information microservice.
    
    This program demonstrates:
    1. Making HTTP requests to a separate microservice
    2. Sending search parameters via URL query strings
    3. Receiving JSON responses (not direct function calls)
    4. Processing structured data responses
    5. Handling errors through HTTP status codes
    """
    print("\nMovie Information Service Test")
    print("==============================")
    print("Note: This test program and the microservice")
    print("communicate through HTTP/JSON, not direct calls.")
    print("The services are completely independent.\n")
    
    # Test 1: Search by movie title
    print("\nTest 1: Movie Search")
    print("-----------------")
    print("Sending HTTP GET request for 'Harry Potter'...")
    test_search("Harry Potter", "movie")
    time.sleep(1)  # Pause between tests
    
    # Test 2: Search by actor name
    print("\nTest 2: Actor Search")
    print("-----------------")
    print("Sending HTTP GET request for 'Tom Hanks'...")  # Changed to Tom Hanks
    test_search("Tom Hanks", "actor")
    time.sleep(1)  # Pause between tests
    
    # Test 3: Search by genre
    print("\nTest 3: Genre Search")
    print("-----------------")
    print("Sending HTTP GET request for 'action'...")  # Changed to action
    test_search("action", "genre")

def test_search(query, search_type):
    """
    Test the movie service search endpoint.
    
    Shows HTTP/JSON communication between separate programs:
    1. This test program sends HTTP GET request
    2. Microservice processes request independently
    3. Microservice returns JSON response
    4. This program parses the JSON response
    
    Args:
        query (str): Search term (movie title, actor name, or genre)
        search_type (str): Type of search - "movie", "actor", or "genre"
    """
    try:
        # Step 1: Construct HTTP request
        url = "http://localhost:5000/api/v1/movies/search"
        params = {
            "q": query,
            "type": search_type
        }
        
        # Step 2: Send HTTP GET request to microservice
        print(f"GET {url}?q={query}&type={search_type}")
        response = requests.get(url, params=params)
        
        # Step 3: Process JSON response
        print(f"\nResponse from microservice:")
        print(f"Status: HTTP {response.status_code}")
        print("Headers:", response.headers.get('content-type'))
        
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            
            # Display results based on search type
            if search_type == "movie":
                print("\nMovie Results:")
                for movie in data.get('movies', []):
                    print(f"\nTitle: {movie['title']} ({movie['year']})")
                    print(f"IMDb Rating: {movie['imdb_rating']}")
                    print(f"Cast: {', '.join(movie['cast'])}")
            
            elif search_type == "actor":
                print("\nActor Filmography:")
                for movie in data.get('filmography', []):
                    print(f"- {movie['title']} ({movie['year']}) - IMDb Rating: {movie['imdb_rating']}")
            
            elif search_type == "genre":
                print(f"\nTop {data['genre']} Movies:")
                for movie in data.get('movies', []):
                    print(f"- {movie['title']} ({movie['year']}) - IMDb Rating: {movie['imdb_rating']}")
            
            print(f"\nRequest completed in {data.get('elapsed_time', 0)} seconds")
        
        else:
            print("\nError Response:")
            print(json.dumps(response.json(), indent=2))
            
    except requests.exceptions.ConnectionError:
        print("\nError: Cannot connect to movie service")
        print("Make sure microservice.py is running (python microservice.py)")
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    test_movie_service()
