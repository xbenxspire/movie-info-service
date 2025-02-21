# Movie Information Microservice

A Flask-based microservice that provides movie information through HTTP/JSON communication. Returns up to 5 movies matching a title search, sorted by IMDb rating.

## Quick Start

1. Clone the Repository:
   ```bash
   git clone https://github.com/xbenxspire/movie-info-service.git
   cd movie-info-service
   ```

2. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Get Your OMDB API Key:
   - Visit http://www.omdbapi.com/
   - Click "API Key" tab
   - Choose "FREE! (1,000 daily limit)"
   - Fill out form, get key via email
   - Click activation link in email

4. Create .env File:
   ```bash
   # Create .env file in the root directory
   echo "OMDB_API_KEY=your_api_key_here" > .env
   ```

5. Start the Service:
   ```bash
   python microservice.py
   ```
   The service will run on http://localhost:5000

## API Usage

The service provides a single endpoint for movie title searches:

```
GET /api/v1/movies/search?q={movie_title}
```

Parameters:
- `q`: Movie title to search for (required)

Example HTTP Request:
```python
import requests

# Search by movie title
response = requests.get(
    "http://localhost:5000/api/v1/movies/search",
    params={"q": "Inception"}
)
```

## Response Format

The service returns JSON responses in the following format:

```json
{
    "message": "Found 5 movies matching 'inception' (sorted by IMDb rating):",
    "movies": [
        {
            "title": "Inception",
            "year": 2010,
            "imdb_rating": 8.8,
            "genre": ["Action", "Adventure", "Sci-Fi"],
            "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Ellen Page"],
            "plot": "..."
        }
    ],
    "elapsed_time": 1.23
}
```

## Features

1. Movie Title Search:
   - Returns up to 5 movies sorted by IMDb rating
   - Includes full movie details:
     * Title and year
     * IMDb rating
     * Genre list
     * Cast list
     * Full plot
   - Response time: ~2-3 seconds

## Error Handling

The service provides clear error messages:

```json
{
    "error": {
        "code": "NOT_FOUND",
        "message": "No results found for Matrix 5",
        "details": "Try a different movie title",
        "timestamp": "2025-02-04T19:31:29Z"
    }
}
```

Common error codes:
- `BAD_REQUEST`: Missing movie title
- `NOT_FOUND`: No results for search query
- `UNAUTHORIZED`: Invalid OMDB API key
- `SERVICE_UNAVAILABLE`: OMDB API is down

## Rate Limits & Performance

- OMDB API: 1,000 requests per day (free tier)
- No caching - all requests fetch fresh data
- Average response time: 2-3 seconds per search

## Support

For issues or questions:
1. Check service is running (`python microservice.py`)
2. Verify OMDB API key in .env file
3. Contact via GitHub issues
4. Available: 7 PM - 11 PM PST weekdays
