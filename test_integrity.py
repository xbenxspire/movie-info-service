import requests

def test_specific_searches():
    """Test specific movie, actor, and genre searches."""
    print("\nMovie Information Microservice Integrity Tests")
    print("============================================")
    
    # 1. The Dark Knight Search
    print("\nTest 1: The Dark Knight Search")
    print("------------------------------")
    response = requests.get(
        "http://localhost:5000/api/v1/movies/search",
        params={"q": "The Dark Knight"},
        headers={"Accept": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ {data['message']}")
        for movie in data['movies']:
            print(f"\nTitle: {movie['title']} ({movie['year']})")
            print(f"IMDb Rating: {movie['imdb_rating']}")
            print(f"Genre: {', '.join(movie['genre'])}")
            print(f"Cast: {', '.join(movie['cast'])}")
            print(f"Plot: {movie['plot'][:150]}...")
    
    # 2. Christian Bale Filmography
    print("\nTest 2: Christian Bale Filmography")
    print("--------------------------------")
    response = requests.get(
        "http://localhost:5000/api/v1/movies/search",
        params={"q": "Christian Bale", "type": "actor"},
        headers={"Accept": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ {data['message']}")
        for movie in data['filmography']:
            print(f"\nTitle: {movie['title']} ({movie['year']})")
            print(f"IMDb Rating: {movie['imdb_rating']}")
            print(f"Plot: {movie['plot'][:150]}...")
    
    # 3. Mystery Genre
    print("\nTest 3: Mystery Genre")
    print("-------------------")
    response = requests.get(
        "http://localhost:5000/api/v1/movies/search",
        params={"q": "mystery", "type": "genre"},
        headers={"Accept": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ {data['message']}")
        for movie in data['movies']:
            print(f"\nTitle: {movie['title']} ({movie['year']})")
            print(f"IMDb Rating: {movie['imdb_rating']}")
            print(f"Genre: {', '.join(movie['genre'])}")
            print(f"Plot: {movie['plot'][:150]}...")

if __name__ == "__main__":
    test_specific_searches()
