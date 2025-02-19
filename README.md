# Movie Information Microservice

A microservice that provides movie information through HTTP/JSON communication. Returns accurate, sorted movie data including top-rated movies by actor and genre.

## For New Users / Teammates

1. Clone the Repository:
   ```bash
   git clone https://github.com/xbenxspire/movie-info-service.git
   cd movie-info-service
   ```

2. Get Your OMDB API Key:
   ```bash
   # 1. Visit http://www.omdbapi.com/
   # 2. Click "API Key" tab
   # 3. Choose "FREE! (1,000 daily limit)"
   # 4. Fill out form, get key via email
   # 5. Click activation link in email
   ```

3. Start the Movie Service:
   ```bash
   # In movie-info-service directory:
   python service.py
   ```
   Keep this running in a separate terminal. You should see:
   "Running on http://localhost:5000"

## Integrating with Your CLI

1. Project Structure:
   ```
   your-cli-project/
   ├── main.py           # Main CLI loop
   ├── weather.py        # Weather commands
   ├── todo.py           # Todo commands
   ├── movie_service.py  # Add movie commands here
   └── .env             # Add OMDB API key here
   ```

2. Create movie_service.py:
   ```python
   import requests

   def get_movie_info(query, search_type="movie"):
       """
       Get movie information from the service.
       
       Args:
           query (str): Any movie title, actor name, or genre to search for
           search_type (str): One of "movie", "actor", or "genre"
       
       Returns:
           dict: Movie data if found, None if not found
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
               error = response.json().get('error', {})
               print(f"Error: {error.get('message', 'Unknown error')}")
               return None
               
       except requests.exceptions.ConnectionError:
           print("Error: Movie service is not running")
           print("Start it with: python service.py")
           return None

   def handle_movie_search(query):
       """Search any movie in IMDb's database."""
       result = get_movie_info(query)
       if result and 'movies' in result:
           print(f"\n{result['message']}")
           for movie in result['movies']:
               print(f"\nTitle: {movie['title']} ({movie['year']})")
               print(f"IMDb Rating: {movie['imdb_rating']}")
               print(f"Cast: {', '.join(movie['cast'])}")
   
   def handle_actor_search(name):
       """Get actor's top 5 movies by IMDb rating."""
       result = get_movie_info(name, "actor")
       if result and 'filmography' in result:
           print(f"\n{result['message']}")
           for movie in result['filmography']:
               print(f"- {movie['title']} ({movie['year']}) - IMDb Rating: {movie['imdb_rating']}")
   
   def handle_genre_search(genre):
       """Get top 5 movies in genre from IMDb Top 250."""
       result = get_movie_info(genre, "genre")
       if result and 'movies' in result:
           print(f"\n{result['message']}")
           for movie in result['movies']:
               print(f"- {movie['title']} ({movie['year']}) - IMDb Rating: {movie['imdb_rating']}")
   ```

3. Add to Your CLI's Command Handler:
   ```python
   # In your main CLI file (e.g., main.py)
   from movie_service import handle_movie_search, handle_actor_search, handle_genre_search
   
   def handle_command(command):
       """Handle CLI commands."""
       if command.startswith("/movie"):
           # Remove "/movie " and search
           query = command[7:].strip()
           handle_movie_search(query)
           
       elif command.startswith("/actor"):
           # Remove "/actor " and search
           name = command[7:].strip()
           handle_actor_search(name)
           
       elif command.startswith("/genre"):
           # Remove "/genre " and search
           genre = command[7:].strip()
           handle_genre_search(genre)
   ```

## Example Commands

Your users can now search for any movie, actor, or genre:

```bash
# Search any movie (returns top 5 by IMDb rating):
/movie inception
/movie dark knight
/movie matrix

# Get any actor's top 5 movies (by IMDb rating):
/actor tom hanks
/actor morgan freeman
/actor leonardo dicaprio

# Get top 5 movies in any genre (from IMDb Top 250):
/genre action
/genre sci-fi
/genre drama
```

## Example Responses

1. Movie Search:
```json
{
    "message": "Found 5 movies matching 'inception':",
    "movies": [{
        "title": "Inception",
        "year": 2010,
        "imdb_rating": "8.8",
        "genre": ["Action", "Adventure", "Sci-Fi"],
        "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Ellen Page"],
        "plot": "..."
    }]
}
```

2. Actor Search:
```json
{
    "actor": "Tom Hanks",
    "message": "Top 5 highest-rated movies starring Tom Hanks:",
    "filmography": [
        {
            "title": "Forrest Gump",
            "year": 1994,
            "imdb_rating": "8.8",
            "plot": "..."
        }
    ]
}
```

3. Genre Search:
```json
{
    "genre": "sci-fi",
    "message": "Top 5 highest-rated sci-fi movies:",
    "movies": [
        {
            "title": "The Matrix",
            "year": 1999,
            "imdb_rating": "8.7",
            "genre": ["Action", "Sci-Fi"],
            "plot": "..."
        }
    ]
}
```

## Error Handling

The service returns clear error messages:

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

## Important Notes

1. Service Requirements:
   - Movie service must be running (`python service.py`)
   - OMDB API key must be in .env file
   - Python requests library (`pip install requests`)

2. Results:
   - All searches return top 5 results
   - Results always sorted by IMDb rating
   - Genre searches use IMDb Top 250 list
   - Actor searches return their highest-rated movies

3. Rate Limits:
   - OMDB API: 1,000 requests per day (free tier)
   - Service: No rate limits
   - Results are cached for performance

## Support

If you encounter any issues:
1. Check the service is running (`python service.py`)
2. Verify your OMDB API key in .env
3. Contact me via Teams:
   - Available: 7 PM - 11 PM PST weekdays
   - Response time: Within 24-48 hours
