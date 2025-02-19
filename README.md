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
   
   # Create .env file and add your key:
   OMDB_API_KEY=your_key_here
   ```

3. Start the Service:
   ```bash
   # Run in a terminal and keep it running:
   python service.py
   ```
   You should see: "Running on http://localhost:5000"

4. Add to Your Program:
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

   # Then use it in your code:
   def handle_movie_command():
       """Example: Get movie info in your CLI."""
       title = input("Enter movie title: ")
       result = get_movie_info(title)
       if result and 'movies' in result:
           for movie in result['movies']:
               print(f"\nTitle: {movie['title']} ({movie['year']})")
               print(f"Rating: {movie['imdb_rating']}")
               print(f"Cast: {', '.join(movie['cast'])}")
   ```

## How It Works

1. Communication Flow:
   - Your program makes HTTP GET requests to http://localhost:5000
   - Service processes the request and returns JSON response
   - All results sorted by IMDb rating

2. Features:
   - Search any movie by title
   - Get any actor's top 5 movies
   - Get top 5 movies in any genre
   - All results sorted by IMDb rating

3. Benefits:
   - Simple HTTP/JSON communication
   - No special setup needed
   - Works with any programming language
   - Reliable response handling

## Example Usage

```python
# 1. Search for any movie
result = get_movie_info("Endgame")
if result and 'movies' in result:
    for movie in result['movies']:
        print(f"Title: {movie['title']} ({movie['year']})")
        print(f"IMDb Rating: {movie['imdb_rating']}")
        print(f"Cast: {', '.join(movie['cast'])}")

# 2. Get any actor's top movies
result = get_movie_info("Ethan Hawke", "actor")
if result and 'filmography' in result:
    for movie in result['filmography']:
        print(f"- {movie['title']} ({movie['year']}) - IMDb Rating: {movie['imdb_rating']}")

# 3. Get top movies in any genre
result = get_movie_info("sci-fi", "genre")
if result and 'movies' in result:
    for movie in result['movies']:
        print(f"- {movie['title']} ({movie['year']}) - IMDb Rating: {movie['imdb_rating']}")
```

## Example Responses

1. Movie Search:
```json
{
    "message": "Found 5 movies matching 'Endgame':",
    "movies": [{
        "title": "Avengers: Endgame",
        "year": 2019,
        "imdb_rating": "8.4",
        "genre": ["Action", "Adventure", "Drama"],
        "cast": ["Robert Downey Jr.", "Chris Evans", "Mark Ruffalo"],
        "plot": "..."
    }]
}
```

2. Actor's Top Movies:
```json
{
    "actor": "Ethan Hawke",
    "message": "Top 5 highest-rated movies starring Ethan Hawke:",
    "filmography": [
        {
            "title": "Before Sunset",
            "year": 2004,
            "imdb_rating": "8.1",
            "plot": "..."
        }
    ]
}
```

3. Genre's Top Movies:
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

## Support

If you encounter any issues:
1. Check the service is running (`python service.py`)
2. Verify your OMDB API key in .env
3. Contact me via Teams:
   - Available: 7 PM - 11 PM PST weekdays
   - Response time: Within 24-48 hours

## Rate Limits
- OMDB API: 1,000 requests per day (free tier)
- Service: No rate limits
- All results cached for performance
