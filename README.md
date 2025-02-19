# Movie Information Microservice

A microservice that provides movie information through a REST API, powered by the OMDB API.

## Repository Structure

```
movie-info-service/
├── service.py          # Headless microservice (core service)
├── test_microservice.py # Demonstration program
├── test_service.py     # Internal unit tests
├── example/            # Example code for integration
│   └── cli.py         # Example CLI implementation
├── data/              # Data directory
│   └── movies.json    # Movie database
└── README.md          # Documentation
```

## Quick Start

1. Get OMDB API Key:
   - Visit http://www.omdbapi.com/ to get a free API key
   - Create a `.env` file in the root directory of the project
   - Add your API key to the `.env` file:
     ```
     OMDB_API_KEY=your_key_here
     ```
     Replace `your_key_here` with the actual API key you received from OMDB.

   Note: The `.env` file is already in `.gitignore` to keep your API key secure.

2. Install and Run:
   ```bash
   # Clone the repository
   git clone https://github.com/xbenxspire/movie-info-service.git
   cd movie-info-service

   # Install dependencies
   pip install -r requirements.txt

   # Start the microservice (keep this running)
   python service.py
   ```

3. Test the Service (Optional):
   ```bash
   # In a new terminal, run the demonstration program
   python test_microservice.py
   ```

4. Using the Service:
   - The microservice runs on http://localhost:5000
   - Keep service.py running in the background
   - Make API requests from your application using the endpoints below
   - See API Integration section for example code

## Testing the Microservice

The repository includes two test programs:

### 1. Demonstration Program (test_microservice.py)
This program shows how to interact with the microservice programmatically:
- Health check functionality
- Movie search examples
- Actor search examples
- Genre search examples
- Error handling examples

Run it with:
```bash
python test_microservice.py
```

### 2. Unit Tests (test_service.py)
Internal tests for service functionality:
- API endpoint testing
- Response validation
- Error case testing

Run it with:
```bash
python test_service.py
```

## Example Integration (example/cli.py)

The example directory contains a CLI implementation showing how to integrate the microservice into your own application. This is provided as a reference but should not be used as part of the microservice itself.

## API Integration

Here are reusable functions you can add to your application to search for any movie, actor, or genre:

### 1. Search Any Movie
```python
import requests

def search_movie(title):
    """
    Get information about any movie.
    
    Args:
        title (str): Any movie title to search for
    
    Returns:
        dict: Movie data if found, None if not found
    """
    response = requests.get(
        "http://localhost:5000/api/v1/movies/search",
        params={"q": title},
        headers={"Accept": "application/json"}
    )
    return response.json() if response.status_code == 200 else None

# Examples:
movies = search_movie("The Matrix")
movies = search_movie("Star Wars")
movies = search_movie("Jurassic Park")

# Process the results
if movies:
    for movie in movies:
        print(f"\nTitle: {movie['title']} ({movie['year']})")
        print(f"Rating: {movie['rating']}")
        print(f"IMDb Rating: {movie['imdb_rating']}")
        print(f"Genre: {', '.join(movie['genre'])}")
        print(f"Released: {movie['released']}")
        print("\nCast:")
        for actor in movie['cast']:
            print(f"- {actor}")
        print("\nCrew:")
        for crew_member in movie['crew']:
            print(f"- {crew_member}")
```

### 2. Search Any Actor
```python
def search_actor(name):
    """
    Get filmography for any actor.
    
    Args:
        name (str): Any actor's name to search for
    
    Returns:
        dict: Actor's filmography if found, None if not found
    """
    response = requests.get(
        "http://localhost:5000/api/v1/movies/search",
        params={"q": name, "type": "actor"},
        headers={"Accept": "application/json"}
    )
    return response.json() if response.status_code == 200 else None

# Examples:
films = search_actor("Brad Pitt")
films = search_actor("Morgan Freeman")
films = search_actor("Meryl Streep")

# Process the results
if films:
    print(f"\nFilmography for {films['actor']}:")
    for movie in films['filmography']:
        print(f"- {movie['title']} ({movie['year']}) - IMDb Rating: {movie['imdb_rating']}")
```

### 3. Search Any Genre
```python
def search_genre(genre_name):
    """
    Get top-rated movies in any genre.
    
    Args:
        genre_name (str): Any genre (action, comedy, drama, etc.)
    
    Returns:
        dict: Genre movies if found, None if not found
    """
    response = requests.get(
        "http://localhost:5000/api/v1/movies/search",
        params={"q": genre_name, "type": "genre"},
        headers={"Accept": "application/json"}
    )
    return response.json() if response.status_code == 200 else None

# Examples:
movies = search_genre("comedy")
movies = search_genre("horror")
movies = search_genre("drama")

# Process the results
if movies:
    print(f"\nTop {len(movies['movies'])} {movies['genre'].title()} Movies:")
    for movie in movies['movies']:
        print(f"- {movie['title']} ({movie['year']}) - IMDb Rating: {movie['imdb_rating']}")
```

These functions can be copied directly into your application. Just make sure the microservice is running (`python service.py`), and you can search for any movie, actor, or genre!

## Error Responses

### 1. No Results Found
```json
{
    "error": {
        "code": "NOT_FOUND",
        "message": "No results found for Matrix 5",
        "details": "Try a different search term",
        "timestamp": "2025-02-04T19:31:29Z"
    }
}
```

### 2. Missing Search Term
```json
{
    "error": {
        "code": "BAD_REQUEST",
        "message": "Search query is required",
        "details": "Please provide a search term",
        "timestamp": "2025-02-04T19:31:29Z"
    }
}
```

## Health Check

```python
response = requests.get("http://localhost:5000/health")
if response.status_code == 200:
    data = response.json()
    print(f"Service: {data['status']}")
    print(f"OMDB API: {data['omdb_api']}")
```

## Support

If you encounter any issues:
1. Check the service is running (`python service.py`)
2. Verify your OMDB API key is set correctly in the `.env` file
3. Contact me via Teams:
   - Available: 7 PM - 11 PM PST weekdays
   - Response time: Within 24-48 hours

## Rate Limits
- OMDB API: 1,000 requests per day (free tier)
- Service: 100 requests per minute
- Exceeding these will return a 429 error

## Dependencies
- Python 3.13.1
- Flask 3.0.2
- Requests 2.31.0
- Flask-CORS 4.0.0
- python-dotenv 1.0.0
