# Movie Information Microservice

A microservice that provides movie information through a REST API, powered by the OMDB API.

## Quick Start

1. Get OMDB API Key:
   - Visit http://www.omdbapi.com/ to get a free API key
   - Set the environment variable:
     ```bash
     # Windows (PowerShell)
     $env:OMDB_API_KEY='your_key'
     
     # Linux/macOS
     export OMDB_API_KEY='your_key'
     ```

2. Install and Run:
   ```bash
   # Clone the repository
   git clone https://github.com/xbenxspire/movie-info-service.git
   cd movie-info-service

   # Install dependencies
   pip install -r requirements.txt

   # Start the service (in one terminal)
   python service.py

   # Start the CLI (in another terminal)
   python cli.py
   ```

## Using the CLI

The CLI provides these commands:
- `search <title>` - Search for any movie by title
- `details <movie_id>` - Get details for a specific movie
- `health` - Check if the service is running
- `help` - Show available commands
- `quit` or `exit` - Exit the CLI

Example usage:
```bash
# Search for any movie
movies> search Inception
Search Results:

ID: tt1375666
Title: Inception
Year: 2010
Rating: PG-13

# Get movie details
movies> details tt1375666
Movie Details:
Title: Inception
Year: 2010
Runtime: 148 minutes
Rating: PG-13

Cast:
- Leonardo DiCaprio as Actor
- Joseph Gordon-Levitt as Actor
- Ellen Page as Actor

Release Dates:
- US: 16 Jul 2010
```

## How to Request Data

The service accepts HTTP GET requests. Here are the available endpoints:

### 1. Get Movie Details
```python
import requests

# Get details for any movie using its IMDb ID
response = requests.get(
    "http://localhost:5000/api/v1/movies/tt1375666",  # Inception
    headers={"Accept": "application/json"}
)

if response.status_code == 200:
    movie = response.json()
    print(f"Title: {movie['title']}")
    print(f"Year: {movie['year']}")
    print(f"Rating: {movie['rating']}")
```

### 2. Search Movies
```python
# Search for any movie by title
response = requests.get(
    "http://localhost:5000/api/v1/movies/search",
    params={"title": "Matrix"},  # Search any movie
    headers={"Accept": "application/json"}
)

if response.status_code == 200:
    movies = response.json()
    for movie in movies:
        print(f"Found: {movie['title']} ({movie['year']})")
```

## Response Format

### 1. Successful Response
```json
{
    "id": "tt1375666",
    "title": "Inception",
    "year": 2010,
    "runtime": 148,
    "rating": "PG-13",
    "cast": [
        {
            "name": "Leonardo DiCaprio",
            "role": "Actor"
        }
    ],
    "release_dates": {
        "US": "16 Jul 2010"
    }
}
```

### 2. Error Response
```json
{
    "error": {
        "code": "NOT_FOUND",
        "message": "Movie with ID tt9999999 not found",
        "details": "Please verify the movie ID and try again",
        "timestamp": "2025-02-04T19:31:29Z"
    }
}
```

## UML Sequence Diagram

```
Dashboard CLI                movies.txt               Movie Info Service                OMDB API
     |                          |                            |                            |
     |  Write movie search     |                            |                            |
     |------------------------>|                            |                            |
     |                         |                            |                            |
     |                         |     Read search query      |                            |
     |                         |<---------------------------|                            |
     |                         |                            |                            |
     |                         |                            |    Request movie data      |
     |                         |                            |--------------------------->|
     |                         |                            |                            |
     |                         |                            |    Return movie data       |
     |                         |                            |<---------------------------|
     |                         |                            |                            |
     |                         |  Write movie data response |                            |
     |                         |<---------------------------|                            |
     |                         |                            |                            |
     |   Read response        |                            |                            |
     |<------------------------|                            |                            |
     |                         |                            |                            |
```

## Error Handling

1. Movie Not Found (404)
   ```python
   try:
       response = requests.get("http://localhost:5000/api/v1/movies/tt9999999")
       data = response.json()
   except requests.exceptions.RequestException as e:
       print(f"Error: {e}")
   ```

2. Invalid Request (400)
   ```python
   try:
       response = requests.get("http://localhost:5000/api/v1/movies/search")
       data = response.json()
   except requests.exceptions.RequestException as e:
       print(f"Error: {e}")
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
2. Verify your OMDB API key is set correctly
3. Contact me:
   - Available via Discord 7PM-11PM PST weekdays
   - Response time: within 24-48 hours

## Rate Limits
- OMDB API: 1,000 requests per day (free tier)
- Service: 100 requests per minute

## Dependencies
- Python 3.13.1
- Flask 3.0.2
- Requests 2.31.0
- Flask-CORS 4.0.0
