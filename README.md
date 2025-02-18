# Movie Information Microservice

A simple microservice that provides movie information through a REST API.

## Quick Start

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

The CLI provides these commands:
- `details <movie_id>` - Get details for a specific movie
- `search <title>` - Search for movies by title
- `health` - Check if the service is running
- `help` - Show available commands
- `quit` or `exit` - Exit the CLI

Example usage:
```bash
movies> search Batman
Search Results:

ID: tt0468569
Title: The Dark Knight
Year: 2008
Rating: PG-13

ID: tt0372784
Title: Batman Begins
Year: 2005
Rating: PG-13

movies> details tt0468569
Movie Details:
Title: The Dark Knight
Year: 2008
Runtime: 152 minutes
Rating: PG-13

Cast:
- Christian Bale as Bruce Wayne / Batman

Release Dates:
- US: 2008-07-18
```

## How to Request Data

The service accepts HTTP GET requests. Here are the available endpoints:

### 1. Get Movie Details
```python
import requests

# Get details for a specific movie
response = requests.get(
    "http://localhost:5000/api/v1/movies/tt0468569",  # The Dark Knight
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
# Search for movies by title
response = requests.get(
    "http://localhost:5000/api/v1/movies/search",
    params={"title": "Batman"},
    headers={"Accept": "application/json"}
)

if response.status_code == 200:
    movies = response.json()
    for movie in movies:
        print(f"Found: {movie['title']} ({movie['year']})")
```

## How to Receive Data

The service returns JSON-formatted responses:

### 1. Successful Response
```json
{
    "id": "tt0468569",
    "title": "The Dark Knight",
    "year": 2008,
    "runtime": 152,
    "rating": "PG-13",
    "cast": [
        {
            "name": "Christian Bale",
            "role": "Bruce Wayne / Batman"
        }
    ],
    "release_dates": {
        "US": "2008-07-18"
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
Dashboard CLI                movies.txt               Movie Info Service
     |                          |                            |
     |  Write movie search     |                            |
     |------------------------>|                            |
     |                         |                            |
     |                         |     Read search query      |
     |                         |<---------------------------|
     |                         |                            |
     |                         |  Write movie data response |
     |                         |<---------------------------|
     |                         |                            |
     |   Read response        |                            |
     |<------------------------|                            |
     |                         |                            |
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
    print("Service is healthy")
```

## Support

If you encounter any issues:
1. Check the service is running (`python service.py`)
2. Verify your Python version (3.13.1 recommended)
3. Contact me via Teams:
   - Available: 7 PM - 11 PM PST weekdays
   - Response time: Within 24-48 hours

## Rate Limits
- 100 requests per minute
- Exceeding this will return a 429 error

## Dependencies
- Python 3.13.1
- Flask 3.0.2
- Requests 2.31.0
