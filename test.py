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
    
    # Test successful movie search
    print("\nTest 1: Successful Movie Search")
    print("-----------------------------")
    print("Sending HTTP GET request for 'The Dark Knight'...")
    test_search("The Dark Knight")
    time.sleep(1)  # Pause between tests
    
    # Test movie not found
    print("\nTest 2: Movie Not Found")
    print("--------------------")
    print("Sending HTTP GET request for 'NonexistentMovie123'...")
    test_search("NonexistentMovie123")
    time.sleep(1)  # Pause between tests
    
    # Test empty search
    print("\nTest 3: Empty Search")
    print("----------------")
    print("Sending HTTP GET request with empty query...")
    test_search("")

def test_search(query):
    """
    Test the movie service search endpoint.
    
    Shows HTTP/JSON communication between separate programs:
    1. This test program sends HTTP GET request
    2. Microservice processes request independently
    3. Microservice returns JSON response
    4. This program parses the JSON response
    
    Args:
        query (str): Movie title to search for
    """
    try:
        # Step 1: Construct HTTP request
        url = "http://localhost:5000/api/v1/movies/search"
        params = {"q": query}
        
        # Step 2: Send HTTP GET request to microservice
        print(f"GET {url}?q={query}")
        response = requests.get(url, params=params)
        
        # Step 3: Process JSON response
        print(f"\nResponse from microservice:")
        print(f"Status: HTTP {response.status_code}")
        print("Headers:", response.headers.get('content-type'))
        
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            
            # Display movie results
            print("\nMovie Results:")
            for movie in data.get('movies', []):
                print(f"\nTitle: {movie['title']} ({movie['year']})")
                print(f"IMDb Rating: {movie['imdb_rating']}")
                print(f"Cast: {', '.join(movie['cast'])}")
                print(f"Genre: {', '.join(movie['genre'])}")
                print(f"Plot: {movie['plot']}")
            
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
