# CS361 Assignment 8: Movie Information Microservice Implementation

## Communication Contract

### How to Request Data
The microservice provides a RESTful API endpoint that accepts HTTP GET requests. Here's how to request data:

```python
import requests

# Base URL for the microservice
BASE_URL = "http://localhost:5000/api/v1/movies/search"

# Example 1: Search by movie title
response = requests.get(BASE_URL, params={
    "q": "Inception",
    "type": "movie"
})

# Example 2: Search by actor name
response = requests.get(BASE_URL, params={
    "q": "Tom Hanks",
    "type": "actor"
})

# Example 3: Search by genre
response = requests.get(BASE_URL, params={
    "q": "action",
    "type": "genre"
})
```

### How to Receive Data
The microservice returns data in JSON format. Here's how to handle the responses:

```python
# Check if request was successful
if response.status_code == 200:
    data = response.json()
    
    # For movie search
    if 'movies' in data:
        for movie in data['movies']:
            print(f"Title: {movie['title']} ({movie['year']})")
            print(f"IMDb Rating: {movie['imdb_rating']}")
            print(f"Cast: {', '.join(movie['cast'])}")
    
    # For actor search
    elif 'filmography' in data:
        for movie in data['filmography']:
            print(f"- {movie['title']} ({movie['year']}) - IMDb Rating: {movie['imdb_rating']}")
    
    # For genre search
    elif 'genre' in data:
        for movie in data['movies']:
            print(f"- {movie['title']} ({movie['year']}) - IMDb Rating: {movie['imdb_rating']}")
            
else:
    # Handle error response
    error = response.json()
    print(f"Error: {error['error']['message']}")
```

## UML Sequence Diagram
![Sequence Diagram](sequence-diagram.png)

The sequence diagram shows:
1. Your program makes HTTP GET request to the microservice
2. Microservice processes request and calls OMDB API
3. OMDB API returns movie data
4. Microservice processes and sorts results
5. Microservice returns JSON response to your program

## Mitigation Plan

1. **Teammate Information**
   - Implementing Microservice A for: Vincent
   - Current Status: Fully implemented and operational
   - Problems: No problems - all features working as specified

2. **Access Instructions**
   - Code available on GitHub: https://github.com/xbenxspire/movie-info-service
   - Clone repository: `git clone https://github.com/xbenxspire/movie-info-service.git`
   - Install dependencies: `pip install -r requirements.txt`
   - Get OMDB API key from http://www.omdbapi.com/
   - Create .env file with: `OMDB_API_KEY=your_key_here`
   - Run service: `python microservice.py`

3. **Troubleshooting Steps**
   If you cannot access/call the microservice:
   1. Verify microservice is running (`python microservice.py`)
   2. Check OMDB API key in .env file
   3. Test health endpoint: `GET http://localhost:5000/health`
   4. Contact me via Teams (available 7 PM - 11 PM PST weekdays)

4. **Notification Deadline**
   - Please notify me of any issues by February 25th, 2025
   - This allows time to resolve issues before Sprint 3

5. **Additional Notes**
   - Service requires Python 3.6+ and requests library
   - Free OMDB API key has 1,000 requests/day limit
   - All responses sorted by IMDb rating
   - No caching used - all requests fetch fresh data
   - Error handling included for all edge cases

## Video Demonstration
The video demonstrates:
1. Test program making HTTP requests
2. Microservice receiving and processing requests
3. JSON responses being returned
4. Error handling scenarios
5. Integration with OMDB API
6. No direct function calls - all communication via HTTP/JSON
