# CS361 Assignment 6: Sprint 2 Plan - Movie Information Microservice

## 1) Sprint Goal
Implement a Movie Information Service microservice that provides detailed movie metadata, cast/crew information, and release dates through a RESTful API interface.

## 2) User Stories

### First User Story: Movie Metadata Lookup
**As a** movie application developer  
**I want to** retrieve comprehensive movie information via API  
**So that** I can display accurate movie details to users

#### Acceptance Criteria
**Functional:**
- Given a valid movie ID, return complete metadata (title, year, runtime, rating)
- Given an invalid ID, return appropriate error response with helpful message
- Given a partial movie title, return matching suggestions

**Non-Functional:**
- Performance Quality Attribute: Response time under 500ms for 95% of requests
- Maintainability Quality Attribute: API documentation updated with each change
- Usability Quality Attribute: Error messages follow consistent format

### Second User Story: Cast & Crew Information
**As a** film database maintainer  
**I want to** access detailed cast and crew information  
**So that** I can provide accurate credit information

#### Acceptance Criteria
**Functional:**
- Given a movie ID, return full cast and crew list with roles
- Given a person's name, return their filmography
- Given a crew role, return all matching personnel

**Non-Functional:**
- Availability Quality Attribute: Data updates within 24 hours of source changes
- Scalability Quality Attribute: Support concurrent requests efficiently
- Reliability Quality Attribute: Maintain data consistency across related endpoints

### Third User Story: Release Date Verification
**As a** movie theater programmer  
**I want to** verify movie release dates across regions  
**So that** I can plan screenings accurately

#### Acceptance Criteria
**Functional:**
- Given a movie ID, return global release schedule
- Given a region code, return localized release dates
- Given a date range, return upcoming releases

**Non-Functional:**
- Reliability Quality Attribute: Daily synchronization with authoritative sources
- Performance Quality Attribute: Cache frequently requested data
- Accuracy Quality Attribute: Handle timezone differences correctly

## 3) System Diagram

```
┌───────────────────────────────────────────────────────────────────────────┐
│                                                                           │
│┌──────────────────────┐          ┌──────────────┐        Movie Quotes     │
││ Ben P.               │          │ Movie quotes │        Microservice A   │
││ Movie Recommendation │◄─────────┤              ├─────►  Vincent - Main   │ 
││ System (Movie search │◄─ ─ ─ ─ ─┤              ├─ ─ ─►  Zack - Backup    │
││ & recommendations)   │          │              │                         │
│└──────────────────────┘          └──────────────┘                         │
│┌──────────────────────┐          ┌──────────────┐                         │
││ Vincent              │          │Movie query   │        Movie Info       │
││ Dashboard CLI (Query │◄─────────┤service       │        Microservice A   │
││ weather, books, todo)│◄─ ─ ─ ─ ─┤              ├─────►  Ben P. - Main    │
│└──────────────────────┘          └──────────────┘─ ─ ─►  Ben L. - Backup  │
│┌──────────────────────┐          ┌──────────────┐                         │
││ Benjamin L.          │          │ Thesaurus    │        Thesaurus        │
││ Flashcard CLI        │◄─────────┤              │        Microservice A   │
││ (Learning system)    │◄─ ─ ─ ─ ─┤              ├─────►  Zack - Main      │
│└──────────────────────┘          └──────────────┘─ ─ ─►  Dawson - Backup  │
│┌──────────────────────┐          ┌──────────────┐                         │
││ Zack                 │          │Direct        │        Direct Message   │
││ Language Exchange    │◄─────────┤Messaging     │        Microservice A   │
││ CLI (Native speaker  │◄─ ─ ─ ─ ─┤              ├─────►  Dawson - Main    │
││ language learning)   │          │              │                         │
│└──────────────────────┘          └──────────────┘─ ─ ─►  Vincent - Backup │
│                                                                           │
│┌──────────────────────┐          ┌──────────────┐                         │
││ Dawson               │          │Request Log   │        DB Microservice  │
││ Budget/Finance       │◄─────────┤Database      │        A                │
││ Tracker (Financial   │◄─ ─ ─ ─ ─┤              ├─────►  Ben L. - Main    │
││ tracking system)     │          │              │                         │
│└──────────────────────┘          └──────────────┘─ ─ ─►  Ben P. - Backup  │
│                                                                           │
│  KEY                                                                      │
│  main plan:   ◄────────►                                                  │
│  backup plan: ◄─ ─ ─ ─ ─►                                                 │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

### Component Descriptions

#### Main Programs
- **Ben P.'s Movie Recommendation System**
  - A movie search and recommendation interface that helps users discover movies

- **Vincent's Dashboard CLI**
  - CLI dashboard to query different information including weather, book recommendations, todo list, schedule, and movie info

- **Benjamin L.'s Flashcard CLI**
  - A flashcard learning system for educational purposes

- **Zack's Language Exchange CLI**
  - Provides a space where people can talk to each other (and with native speakers) in their target language for learning

- **Dawson's Budget/Finance Tracker**
  - Financial tracking and management system

#### Microservices
- **Movie Quotes (Vincent)**
  - Provides movie quotes for movies the user searches for

- **Movie Query Service (Ben P.)**
  - Gathers movie data including title, director, release date, and ratings

- **Thesaurus Service (Zack)**
  - Returns synonyms for given words to enhance vocabulary

- **Direct Message Service (Dawson)**
  - Enables direct messaging between users through socket programming for real-time communication

- **DB Service (Ben L.)**
  - Creates a mini database to log request data (time taken, type) and provides summaries (average time, total number, etc.)

## 4) Communication Pipe
RESTful API using HTTP/JSON

**Base URL:** `http://localhost:5000/api/v1`

**Endpoints:**
```
GET /movies/{id}
GET /movies/search?title={query}
GET /cast/{movie_id}
GET /releases/{movie_id}?region={code}
```

## 5) Data Request Examples

### Movie Details Request
```python
import requests

def get_movie_details(movie_id):
    response = requests.get(
        f"http://localhost:5000/api/v1/movies/{movie_id}",
        headers={"Accept": "application/json"}
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        handle_error(response)
```

### Error Handling
```python
def handle_error(response):
    error_map = {
        404: "Movie not found",
        429: "Rate limit exceeded",
        500: "Internal server error"
    }
    
    error_msg = error_map.get(
        response.status_code, 
        "Unknown error occurred"
    )
    
    logging.error(f"API Error: {error_msg}")
    raise APIError(error_msg, response.status_code)
```

## 6) Data Response Examples

### Successful Response
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
        },
        {
            "name": "Heath Ledger",
            "role": "Joker"
        }
    ],
    "release_dates": {
        "US": "2008-07-18",
        "UK": "2008-07-24",
        "JP": "2008-08-09"
    }
}
```

### Error Response
```json
{
    "error": {
        "code": "NOT_FOUND",
        "message": "Movie with ID tt9999999 not found",
        "details": "Please verify the movie ID and try again",
        "timestamp": "2025-02-04T19:31:29Z",
        "request_id": "req_abc123"
    }
}
```

### Rate Limit Response
```json
{
    "error": {
        "code": "RATE_LIMITED",
        "message": "Too many requests",
        "details": "Please wait 30 seconds before retrying",
        "reset_at": "2025-02-04T19:32:29Z"
    }
}
```

## 7) API Documentation Screenshot
<!-- Insert Swagger/OpenAPI documentation screenshot here -->
```
[Screenshot showing API endpoints, request/response examples, and error codes]
```

## Error Handling Strategy

### HTTP Status Codes
- 200: Success
- 400: Bad Request (invalid parameters)
- 404: Not Found (invalid movie ID)
- 429: Too Many Requests (rate limit)
- 500: Internal Server Error

### Error Response Format
All error responses follow this structure:
```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human readable message",
        "details": "Additional context",
        "timestamp": "ISO-8601 timestamp",
        "request_id": "Unique request identifier"
    }
}
```

### Rate Limiting
- 100 requests per minute per API key
- Headers included in responses:
  - X-RateLimit-Limit
  - X-RateLimit-Remaining
  - X-RateLimit-Reset

## Request Flow Sequence
```
Client    Movie CLI    Primary Info    Backup Info
  |           |             |              |
  | Search    |             |              |
  |---------->|             |              |
  |           | Get Details |              |
  |           |------------>|              |
  |           |     X       |              |
  |           | (timeout)   |              |
  |           |             |              |
  |           | Failover    |              |
  |           |--------------------------->|
  |           |             |        Get   |
  |           |             |     Details  |
  |           |             |              |
  |           |      Response              |
  |           |<---------------------------|
  |  Results  |             |              |
  |<----------|             |              |
```

### Failover Strategy
1. Primary Service Check
   - Attempt primary service first
   - Timeout after 3 seconds
   - Track failed attempts

2. Backup Service Activation
   - Switch to backup after 2 failed primary attempts
   - Log service switching events
   - Monitor backup service health

3. Service Recovery
   - Periodic health checks of primary
   - Auto-switch back when primary recovers
   - Maintain request consistency during switch

## Implementation Notes

### Service Independence
- Each microservice runs independently
- Services communicate via HTTP/JSON
- No shared databases between services
- Graceful handling of service outages

### Data Consistency
- Cache invalidation on updates
- Versioned API responses
- Timestamp tracking for changes
- Conflict resolution strategies

### Monitoring
- Request logging
- Performance metrics
- Error tracking
- Rate limit monitoring
- Service health checks
