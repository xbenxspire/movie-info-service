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

## Integrating with Your CLI Program

1. Create a Movie Service Module:
   ```python
   # movie_service.py
   import requests

   def search_movies(title):
       """
       Search for movies by title.
       
       Args:
           title (str): Movie title to search for
           
       Returns:
           list: List of movie dictionaries sorted by IMDb rating
           None: If no movies found or error occurs
       """
       try:
           # Send request to microservice
           response = requests.get(
               "http://localhost:5000/api/v1/movies/search",
               params={"q": title}
           )
           
           # Check if request was successful
           if response.status_code == 200:
               data = response.json()
               return data.get('movies', [])
           else:
               # Handle error response
               error = response.json().get('error', {})
               print(f"Error: {error.get('message', 'Unknown error')}")
               return None
               
       except requests.exceptions.ConnectionError:
           print("Error: Movie service is not running")
           print("Start it with: python microservice.py")
           return None
       except Exception as e:
           print(f"Error: {str(e)}")
           return None
   ```

2. Add Movie Commands to Your CLI:
   ```python
   # main.py
   from movie_service import search_movies

   def handle_movie_command(command):
       """Handle movie-related commands."""
       if command.startswith("/movie"):
           # Extract movie title from command
           title = command[7:].strip()
           if not title:
               print("Please provide a movie title")
               return

           # Search for movies
           movies = search_movies(title)
           if movies:
               print(f"\nFound {len(movies)} movies:")
               for movie in movies:
                   print(f"\nTitle: {movie['title']} ({movie['year']})")
                   print(f"IMDb Rating: {movie['imdb_rating']}")
                   print(f"Cast: {', '.join(movie['cast'])}")
                   print(f"Genre: {', '.join(movie['genre'])}")
                   print(f"Plot: {movie['plot']}")

   def main():
       """Main CLI loop."""
       print("Welcome to Movie CLI!")
       print("Commands:")
       print("  /movie <title>  - Search for movies")
       print("  /quit          - Exit program")
       
       while True:
           command = input("\nEnter command: ").strip()
           
           if command == "/quit":
               break
           elif command.startswith("/movie"):
               handle_movie_command(command)
           else:
               print("Unknown command")

   if __name__ == "__main__":
       main()
   ```

3. Project Structure:
   ```
   your-cli-project/
   ├── main.py           # Main CLI program
   ├── movie_service.py  # Movie service integration
   └── requirements.txt  # Add 'requests' to your dependencies
   ```

4. Usage Example:
   ```
   $ python main.py
   Welcome to Movie CLI!
   Commands:
     /movie <title>  - Search for movies
     /quit          - Exit program

   Enter command: /movie inception
   
   Found 5 movies:

   Title: Inception (2010)
   IMDb Rating: 8.8
   Cast: Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page
   Genre: Action, Adventure, Sci-Fi
   Plot: A thief who steals corporate secrets through...
   ```

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

## UML Sequence Diagram

![Sequence Diagram](UML%20Sequnce%20Diagram.png)

This sequence diagram shows how the microservice:
1. Receives movie search requests from client programs
2. Validates queries and handles errors
3. Fetches and sorts movie data from OMDB API
4. Returns formatted JSON responses with elapsed time

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
3. Contact via Discord
4. Available: 7 PM - 11 PM PST weekdays
