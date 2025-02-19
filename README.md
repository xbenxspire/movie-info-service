# Movie Information Microservice

A microservice that provides movie information through JSON file communication. Returns accurate, sorted movie data including top-rated movies by actor and genre.

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

4. Add to Your Program:
   ```python
   # In your main program (e.g., dashboard.py), add:
   
   import json
   import time
   import os

   def get_movie_info(query, search_type="movie"):
       """
       Get movie information from the service.
       
       Args:
           query (str): Any movie title, actor name, or genre to search for
           search_type (str): One of "movie", "actor", or "genre"
       
       Returns:
           dict: Movie data if found, None if not found
       """
       # Create data directory if needed
       if not os.path.exists('data'):
           os.makedirs('data')
       
       # Write request to JSON file
       request = {
           "query": query,
           "type": search_type,
           "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
       }
       with open('data/movies_request.json', 'w') as f:
           json.dump(request, f, indent=2)
       
       # Wait for response
       max_attempts = 10
       attempts = 0
       while attempts < max_attempts:
           if os.path.exists('data/movies_response.json'):
               with open('data/movies_response.json', 'r') as f:
                   response = json.load(f)
               os.remove('data/movies_response.json')
               return response
           time.sleep(0.5)
           attempts += 1
       
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
   - Your program writes requests to: `data/movies_request.json`
   - Service reads the request and processes it
   - Service writes response to: `data/movies_response.json`
   - Your program reads and processes the response

2. Features:
   - Search any movie by title
   - Get any actor's top 5 movies
   - Get top 5 movies in any genre
   - All results sorted by IMDb rating

3. Benefits:
   - No special libraries needed
   - Uses Python's built-in modules
   - Simple JSON file communication
   - Works with any programming language

## Example Usage

```python
# 1. Search for any movie
result = get_movie_info("Inception")
if result and 'movies' in result:
    for movie in result['movies']:
        print(f"Title: {movie['title']} ({movie['year']})")
        print(f"IMDb Rating: {movie['imdb_rating']}")
        print(f"Cast: {', '.join(movie['cast'])}")

# 2. Get any actor's top movies
result = get_movie_info("Morgan Freeman", "actor")
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
    "message": "Found 1 movies matching 'Inception':",
    "movies": [{
        "title": "Inception",
        "year": 2010,
        "imdb_rating": "8.8",
        "genre": ["Action", "Adventure", "Sci-Fi"],
        "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt"],
        "plot": "..."
    }]
}
```

2. Actor's Top Movies:
```json
{
    "actor": "Morgan Freeman",
    "message": "Top 5 highest-rated movies starring Morgan Freeman:",
    "filmography": [
        {
            "title": "The Shawshank Redemption",
            "year": 1994,
            "imdb_rating": "9.3",
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
2. Make sure the data directory exists
3. Verify your OMDB API key in .env
4. Contact me via Teams:
   - Available: 7 PM - 11 PM PST weekdays
   - Response time: Within 24-48 hours

## Rate Limits
- OMDB API: 1,000 requests per day (free tier)
- Service: No rate limits
- All results cached for performance
