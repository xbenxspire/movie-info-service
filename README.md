# Movie Information Microservice

A microservice that provides movie information through a REST API, powered by the OMDB API. Returns accurate, sorted movie data including top-rated movies by actor and genre.

## Features

- Movie Search: Find any movie with full details
- Actor Search: Get an actor's top 5 highest-rated movies
- Genre Search: Get top 5 highest-rated movies in any genre
- All results sorted by IMDb rating
- Includes plot summaries, cast, and crew information

## Quick Start

1. Get OMDB API Key:
   ```bash
   # 1. Visit http://www.omdbapi.com/
   # 2. Click "API Key" tab
   # 3. Choose "FREE! (1,000 daily limit)"
   # 4. Fill out form, get key via email
   # 5. Click activation link in email
   
   # Create .env file and add your key:
   echo "OMDB_API_KEY=your_key_here" > .env
   ```

2. Install and Run:
   ```bash
   # Clone and setup
   git clone https://github.com/xbenxspire/movie-info-service.git
   cd movie-info-service
   pip install -r requirements.txt

   # Start the service (keep this running)
   python service.py
   ```

## Using the Microservice

The service provides three main endpoints, all returning results sorted by IMDb rating:

### 1. Search Movies
```python
import requests

# Find any movie
response = requests.get(
    "http://localhost:5000/api/v1/movies/search",
    params={"q": "The Dark Knight"},
    headers={"Accept": "application/json"}
)

# Example Response:
{
    "message": "Found 1 movies matching 'The Dark Knight':",
    "movies": [{
        "title": "The Dark Knight",
        "year": 2008,
        "imdb_rating": "9.0",
        "genre": ["Action", "Crime", "Drama"],
        "cast": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"],
        "plot": "..."
    }]
}
```

### 2. Search Actor's Top Movies
```python
# Get actor's top 5 highest-rated movies
response = requests.get(
    "http://localhost:5000/api/v1/movies/search",
    params={"q": "Christian Bale", "type": "actor"},
    headers={"Accept": "application/json"}
)

# Example Response:
{
    "actor": "Christian Bale",
    "message": "Top 5 highest-rated movies starring Christian Bale:",
    "filmography": [
        {
            "title": "The Dark Knight",
            "year": 2008,
            "imdb_rating": "9.0",
            "plot": "..."
        },
        {
            "title": "The Prestige",
            "year": 2006,
            "imdb_rating": "8.5",
            "plot": "..."
        },
        // ... more movies sorted by rating
    ]
}
```

### 3. Search Genre's Top Movies
```python
# Get top 5 highest-rated movies in a genre
response = requests.get(
    "http://localhost:5000/api/v1/movies/search",
    params={"q": "mystery", "type": "genre"},
    headers={"Accept": "application/json"}
)

# Example Response:
{
    "genre": "mystery",
    "message": "Top 5 highest-rated mystery movies:",
    "movies": [
        {
            "title": "Se7en",
            "year": 1995,
            "imdb_rating": "8.6",
            "genre": ["Crime", "Drama", "Mystery"],
            "plot": "..."
        },
        {
            "title": "The Prestige",
            "year": 2006,
            "imdb_rating": "8.5",
            "plot": "..."
        },
        // ... more movies sorted by rating
    ]
}
```

## Example Integration

Here's how to integrate the movie service into your application:

```python
def get_movie_info(query, search_type="movie"):
    """
    Get movie information from the microservice.
    
    Args:
        query (str): Movie title, actor name, or genre
        search_type (str): One of "movie", "actor", or "genre"
    
    Returns:
        dict: JSON response with movie data
    """
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
            print(f"Error: {response.json()['error']['message']}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("Error: Movie service is not running")
        print("Start it with: python service.py")
        return None

# Example Usage:
movie = get_movie_info("The Dark Knight")
actor = get_movie_info("Christian Bale", "actor")
genre = get_movie_info("mystery", "genre")
```

## Error Handling

The service returns clear error messages:

```python
# No results
{
    "error": {
        "code": "NOT_FOUND",
        "message": "No results found for Matrix 5",
        "details": "Try a different search term",
        "timestamp": "2025-02-04T19:31:29Z"
    }
}

# Missing query
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

Monitor the service status:

```python
response = requests.get("http://localhost:5000/health")
if response.status_code == 200:
    data = response.json()
    print(f"Service: {data['status']}")
    print(f"OMDB API: {data['omdb_api']}")
```

## Rate Limits
- OMDB API: 1,000 requests per day (free tier)
- Service: 100 requests per minute
- Exceeding these will return a 429 error

## Support

If you encounter any issues:
1. Check the service is running (`python service.py`)
2. Verify your OMDB API key is set correctly in the `.env` file
3. Contact me via Teams:
   - Available: 7 PM - 11 PM PST weekdays
   - Response time: Within 24-48 hours

## Dependencies
- Python 3.13.1
- Flask 3.0.2
- Requests 2.31.0
- Flask-CORS 4.0.0
- python-dotenv 1.0.0
