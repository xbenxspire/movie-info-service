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
[See project_plan.md for full system diagram]

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
[See service.py and example_usage.py for implementation]

## 6) Data Response Examples
[See README.md for example responses]

## 7) API Documentation Screenshot
[See README.md for API documentation]
