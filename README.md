# Movie Information Microservice

A microservice that provides movie information through a REST API, powered by the OMDB API.

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

   # Start the service
   python service.py
   ```

## Search Movies and Actors

The service provides two types of searches:

### 1. Movie Search
```python
import requests

# Search for any movie by title
response = requests.get(
    "http://localhost:5000/api/v1/movies/search",
    params={"q": "Inception"},
    headers={"Accept": "application/json"}
)

if response.status_code == 200:
    movies = response.json()
    for movie in movies:
        print(f"\nTitle: {movie['title']} ({movie['year']})")
        print(f"Rating: {movie['rating']}")
        print(f"Genre: {', '.join(movie['genre'])}")
        print(f"Released: {movie['released']}")
        print("\nCast:")
        for actor in movie['cast']:
            print(f"- {actor}")
        print("\nCrew:")
        for crew_member in movie['crew']:
            print(f"- {crew_member}")
```

Example Response:
```json
[
    {
        "id": "tt1375666",
        "title": "Inception",
        "year": 2010,
        "released": "16 Jul 2010",
        "runtime": 148,
        "rating": "PG-13",
        "genre": ["Action", "Adventure", "Sci-Fi"],
        "cast": [
            "Leonardo DiCaprio",
            "Joseph Gordon-Levitt",
            "Ellen Page",
            "Tom Hardy",
            "Ken Watanabe"
        ],
        "crew": [
            "Christopher Nolan (Director)",
            "Christopher Nolan (Writer)"
        ]
    }
]
```

### 2. Actor Search
```python
# Search for an actor's filmography
response = requests.get(
    "http://localhost:5000/api/v1/movies/search",
    params={"q": "Tom Hanks", "type": "actor"},
    headers={"Accept": "application/json"}
)

if response.status_code == 200:
    data = response.json()
    print(f"\nFilmography for {data['actor']}:")
    for movie in data['filmography']:
        print(f"- {movie['title']} ({movie['year']})")
```

Example Response:
```json
{
    "actor": "Tom Hanks",
    "filmography": [
        {
            "title": "Forrest Gump",
            "year": 1994,
            "role": "Actor",
            "id": "tt0109830"
        },
        {
            "title": "Saving Private Ryan",
            "year": 1998,
            "role": "Actor",
            "id": "tt0120815"
        }
    ]
}
```

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
