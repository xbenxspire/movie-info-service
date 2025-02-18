import requests

def test_get_movie_details():
    """Test getting details for a specific movie."""
    movie_id = "tt0468569"  # The Dark Knight
    response = requests.get(
        f"http://localhost:5000/api/v1/movies/{movie_id}",
        headers={"Accept": "application/json"}
    )
    
    if response.status_code == 200:
        movie = response.json()
        print("\nMovie Details Test:")
        print(f"Title: {movie['title']}")
        print(f"Year: {movie['year']}")
        print(f"Rating: {movie['rating']}")
        return True
    else:
        print(f"\nError getting movie details: {response.status_code}")
        return False

def test_search_movies():
    """Test searching for movies by title."""
    query = "Batman"
    response = requests.get(
        "http://localhost:5000/api/v1/movies/search",
        params={"title": query},
        headers={"Accept": "application/json"}
    )
    
    if response.status_code == 200:
        movies = response.json()
        print("\nMovie Search Test:")
        for movie in movies:
            print(f"Found: {movie['title']} ({movie['year']})")
        return True
    else:
        print(f"\nError searching movies: {response.status_code}")
        return False

def test_error_handling():
    """Test error handling for invalid movie ID."""
    movie_id = "tt9999999"  # Non-existent movie
    response = requests.get(
        f"http://localhost:5000/api/v1/movies/{movie_id}",
        headers={"Accept": "application/json"}
    )
    
    if response.status_code == 404:
        error = response.json()['error']
        print("\nError Handling Test:")
        print(f"Error Code: {error['code']}")
        print(f"Message: {error['message']}")
        return True
    else:
        print("\nUnexpected response for error handling test")
        return False

def run_all_tests():
    """Run all test cases."""
    print("Starting Movie Service Tests...")
    
    # Test health check
    try:
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            print("\nService is healthy ✓")
        else:
            print("\nService health check failed!")
            return
    except requests.exceptions.ConnectionError:
        print("\nError: Service is not running!")
        print("Please start the service with: python service.py")
        return
    
    # Run functional tests
    tests = [
        ("Movie Details", test_get_movie_details),
        ("Movie Search", test_search_movies),
        ("Error Handling", test_error_handling)
    ]
    
    results = []
    for name, test in tests:
        try:
            result = test()
            results.append((name, result))
            status = "✓" if result else "✗"
            print(f"\n{name} Test: {status}")
        except Exception as e:
            results.append((name, False))
            print(f"\n{name} Test: ✗ (Error: {str(e)})")
    
    # Summary
    print("\nTest Summary:")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"Passed: {passed}/{total} tests")

if __name__ == "__main__":
    run_all_tests()
