# CS361 Assignment 8: Movie Information Microservice Implementation

## Communication Contract

### How to Request Data
The microservice provides a RESTful API endpoint that accepts HTTP GET requests for movie title searches:

```python
import requests

# Base URL for the microservice
BASE_URL = "http://localhost:5000/api/v1/movies/search"

# Search by movie title
response = requests.get(BASE_URL, params={
    "q": "Inception"  # Movie title to search for
})
```

### How to Receive Data
The microservice returns data in JSON format. Here's how to handle the responses:

```python
# Check if request was successful
if response.status_code == 200:
    data = response.json()
    
    # Process movie results
    for movie in data.get('movies', []):
        print(f"Title: {movie['title']} ({movie['year']})")
        print(f"IMDb Rating: {movie['imdb_rating']}")
        print(f"Cast: {', '.join(movie['cast'])}")
        print(f"Genre: {', '.join(movie['genre'])}")
        print(f"Plot: {movie['plot']}")
            
else:
    # Handle error response
    error = response.json()
    print(f"Error: {error['error']['message']}")
```

## UML Sequence Diagram
![Sequence Diagram](UML%20Sequnce%20Diagram.png)

The sequence diagram illustrates the complete flow of a movie search request:

1. Client Program initiates search:
   - Makes HTTP GET request to `/api/v1/movies/search?q={title}`
   - Waits for response from microservice

2. Movie Microservice processes request:
   - Validates search query
   - Calls OMDB API search endpoint
   - Receives search results
   - For each movie (up to 5):
     * Fetches detailed movie information
     * Extracts IMDb rating
   - Sorts movies by rating
   - Returns formatted JSON response

3. OMDB API interactions:
   - Initial search request for movies matching title
   - Individual requests for detailed movie information
   - Returns data in JSON format

4. Response handling:
   - Success: Returns sorted movie list with details
   - Errors: Returns appropriate error messages
     * 400 Bad Request (missing query)
     * 404 Not Found (no results)

### Creating the Sequence Diagram (Lucidchart Steps)

1. Create Basic Structure:
   - Go to www.lucidchart.com
   - When asked "Which use case would you like to try first?", select "Document Systems"
   - Click "+ Create" button
   - In the template picker, search for "UML"
   - Select "UML Sequence Diagram" from the templates

2. Add Lifelines (from left sidebar):
   - From "UML Seq..." section, drag the actor symbol (stick figure) for "Program making request"
   - Drag two object boxes (rectangles) for "Movie Microservice" and "OMDB API"
   - Space them evenly across the top of the diagram
   - The dashed lines will automatically extend downward

3. Add Messages (from left sidebar):
   - Click the solid arrow tool under "UML Seq..."
   - Draw from Program to Microservice, label: "GET /api/v1/movies/search?q={title}"
   - Draw from Microservice to OMDB API, label: "search_movies()"
   - Use dashed arrow tool for return messages
   - Draw return arrow from OMDB API to Microservice
   - Draw final return arrow from Microservice to Program

4. Add Loop Frame:
   - From "UML Seq..." section, find the frame/box tool
   - Draw it around the OMDB API interactions
   - Label it "loop" in top-left corner
   - Add "[0..5]" as condition for fetching up to 5 movies

5. Add Opt Frame for Errors:
   - Use same frame/box tool
   - Draw below the main sequence
   - Label it "opt" in top-left corner
   - Add "[no results found]" as condition
   - Add error return message using dashed arrow

6. Add Notes:
   - Use yellow note tool (sticky note icon)
   - Add three notes with:
     * "Query must be a valid movie title"
     * "Microservice fetches movie details and sorts by IMDb rating"
     * "Returns error if no movies found"

6. Export:
   - Save as PNG
   - Name it "sequence-diagram.png"

## Implementation Details & Limitations

### Design Philosophy
- Follows microservice principles with stateless design
- No local caching or stored data - fetches fresh data for every request
- All results sorted by IMDb rating
- Returns up to 5 movies per search

### OMDB API Limitations

The OMDB API provides limited search capabilities:
- Can only search by movie title or IMDb ID
- No direct actor filmography search
- No direct genre-based search
- No built-in sorting by IMDb rating

Therefore, this microservice:
1. Focuses on movie title search only
2. Uses OMDB's search endpoint to find movies
3. Fetches full details for each movie
4. Sorts results by IMDb rating
5. Returns top 5 matches

## Mitigation Plan

1. **Teammate Information**
   - Implementing Microservice A for: Vincent
   - Current Status: Fully implemented and operational
   - Features: Movie title search with IMDb rating sorting

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
