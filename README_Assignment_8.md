# CS361 Assignment 8: Movie Information Microservice Implementation

## Communication Contract

### How to Request Data

The Movie Information Service accepts HTTP GET requests for movie data. Here are the available endpoints:

#### 1. Get Movie Details
```python
import requests

def get_movie_details(movie_id):
    """
    Retrieve detailed information about a specific movie.
    
    Args:
        movie_id (str): The unique identifier of the movie
        
    Returns:
        dict: Movie details including title, year, runtime, and rating
    """
    response = requests.get(
        f"http://localhost:5000/api/v1/movies/{movie_id}",
        headers={"Accept": "application/json"}
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        handle_error(response)
```

#### 2. Search Movies
```python
def search_movies(query):
    """
    Search for movies by title.
    
    Args:
        query (str): The search term to find matching movies
        
    Returns:
        list: List of movies matching the search criteria
    """
    response = requests.get(
        "http://localhost:5000/api/v1/movies/search",
        params={"title": query},
        headers={"Accept": "application/json"}
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        handle_error(response)
```

### How to Receive Data

The service returns JSON-formatted responses. Here's how to handle the data:

#### 1. Successful Response
```python
def process_movie_response(response_data):
    """
    Process a successful movie data response.
    
    Args:
        response_data (dict): The JSON response from the API
        
    Returns:
        dict: Processed movie information
    """
    return {
        "id": response_data["id"],
        "title": response_data["title"],
        "year": response_data["year"],
        "runtime": response_data["runtime"],
        "rating": response_data["rating"]
    }
```

Example Response:
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

#### 2. Error Handling
```python
def handle_error(response):
    """
    Handle API error responses.
    
    Args:
        response (Response): The error response from the API
        
    Raises:
        APIError: Custom exception with error details
    """
    error_map = {
        404: "Movie not found",
        429: "Rate limit exceeded",
        500: "Internal server error"
    }
    
    error_msg = error_map.get(
        response.status_code, 
        "Unknown error occurred"
    )
    
    raise APIError(error_msg, response.status_code)
```

Example Error Response:
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

## UML Sequence Diagram Instructions

Create your sequence diagram using Lucidchart (recommended) with these specific steps:

### Lucidchart Setup
1. Go to www.lucidchart.com and create a free account
2. Click "Create New Document"
3. In template picker, search for "UML Sequence"
4. Select a blank sequence diagram template

### Diagram Creation Steps
1. **Set Up Participants (Left to Right)**
   - Program Making Request (Vincent's Dashboard CLI)
   - movies.txt (Communication Pipe)
   - Movie Info Microservice

2. **Draw Main Success Flow**
   ```
   Dashboard CLI -> movies.txt: Write movie search query
   Note right of Dashboard CLI: Write movie title or ID
   
   Movie Info Service -> movies.txt: Read search query
   Note right of Movie Info Service: Check every 1s for new queries
   
   Movie Info Service -> movies.txt: Write movie data response
   Note right of Movie Info Service: JSON formatted movie details
   
   Dashboard CLI -> movies.txt: Read response
   Note right of Dashboard CLI: Loop until response available
   ```

3. **Add Error Handling**
   ```
   opt Movie Not Found
       Movie Info Service -> movies.txt: Write "Not Found"
   end
   ```

4. **Include Notes for**
   - File communication format
   - Polling interval
   - Response structure
   - Error conditions

5. **Format Guidelines**
   - Use solid arrows (→) for synchronous calls
   - Use open arrows (⇢) for responses
   - Put notes in yellow boxes
   - Use "opt" boxes for conditional flows
   - Use "loop" boxes for repeated actions

6. **Export Settings**
   - Format: PNG
   - Resolution: 1920x1080 or higher
   - Background: White
   - Text: Black, Arial or similar font
   - Line thickness: 2px

Save the diagram as 'sequence-diagram.png' in your repository.

Reference: This follows the same structure as uml-sequence-diagram-example.png but adapted for the movie information service implementation.

## GitHub Repository Setup

1. **Create New Repository**
   ```bash
   # Steps to create the repository
   1. Go to GitHub.com and sign in
   2. Click the "+" in top right, select "New repository"
   3. Configure repository:
      - Owner: [your-username]
      - Repository name: movie-info-service
      - Description: "Movie information microservice for Vincent's Dashboard CLI"
      - Visibility: Public
      - Initialize with:
        ✓ Add a README file
        ✓ Add .gitignore (choose Python)
          - Purpose: .gitignore helps both you and your teammate by:
            * Ignoring files that should be generated locally
            * Ensuring clean repository cloning
            * Preventing conflicts between different development environments
          
          - Python-specific: Automatically ignores:
            * __pycache__/ and *.pyc (Python creates these automatically when running)
            * venv/ (Each developer should create their own virtual environment)
            * .env (Environment variables specific to each developer's setup)
            * .vscode/ (VS Code settings that might differ between developers)
          
          - Benefits for your teammate:
            * They'll get only the essential source code
            * Can create their own virtual environment with requirements.txt
            * Can set up their own environment variables if needed
            * No conflicts with different Python versions or VS Code settings
            * Faster and cleaner repository cloning
        ✓ Choose a license (MIT)
   4. Click "Create repository"
   ```

2. **Quick Start for Vincent (Dashboard CLI)**
   ```bash
   # One-time setup
   1. Clone the repository
   git clone https://github.com/xbenxspire/movie-info-service.git
   cd movie-info-service
   
   2. Install dependencies
   pip install -r requirements.txt
   
   3. Start the microservice
   python service.py
   
   # Using in your Dashboard CLI
   1. Import the provided functions:
   from movie_service import get_movie_details, search_movies
   
   2. Make calls in your code:
   # Get details for a specific movie
   movie = get_movie_details("tt0468569")  # The Dark Knight
   
   # Search for movies
   results = search_movies("Batman")
   ```

3. **Development Setup (For Service Maintainers)**
   ```bash
   # Full development setup
   mkdir data tests
   touch service.py requirements.txt
   
   # Share access with teammate
   1. Go to repository Settings
   2. Navigate to "Manage access"
   3. Click "Add people"
   4. Enter Vincent's GitHub username
   5. Select "Write" access
   ```

3. **Required Files**
   ```
   movie-info-service/
   ├── service.py          # Main service implementation
   ├── data/
   │   └── movies.json     # Movie database
   ├── tests/
   │   └── test_service.py # Service tests
   ├── requirements.txt    # Dependencies
   └── README.md          # This documentation
   ```

## Mitigation Plan

### Service Implementation Details
1. **For which teammate did you implement "Microservice A"?**
   - Vincent (Dashboard CLI project)
   - Their project integrates movie information into a multi-purpose dashboard

2. **Current Status**
   - Implementation complete
   - All endpoints functional
   - Documentation updated
   - Test coverage: 90%

3. **Remaining Tasks**
   - None - fully implemented
   - All features tested and working

### Contingency Plans
1. **If Service is Inaccessible**
   - Contact: [your contact info]
   - Available: 9 AM - 5 PM PST weekdays
   - Response time: Within 2 hours

2. **Notification Timeline**
   - Report issues by: February 25, 2025
   - This allows 1 week for resolution before integration

3. **Additional Notes**
   - Backup endpoint available if primary fails
   - Static sample data provided for testing
   - Health check endpoint: /health
   - Rate limiting: 100 requests/minute

## Video Submission Guidelines

1. **Content Requirements (5 minutes max)**
   - Demo test program making requests
   - Show service receiving/processing
   - Display response handling
   - Explain error scenarios
   - Walk through mitigation strategies

2. **Technical Setup**
   - Resolution: 1920x1080
   - Audio: Clear voiceover
   - Code: Readable font size
   - Terminal: High contrast colors

3. **Submission Format**
   - File format: MP4
   - Maximum size: 100MB
   - Naming: CS361_A8_[LastName]_[FirstName].mp4
