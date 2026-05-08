# DriftDater — API Documentation

**Base URL (Development):** `http://localhost:5000`
**Base URL (Production):** *(add Render URL when deployed)*

All endpoints requiring authentication use Flask session cookies set on login.
All request/response bodies are JSON unless noted (photo uploads use multipart/form-data).

---

## Table of Contents
- [Authentication](#authentication)
- [Profile](#profile)
- [Profiles (Browse)](#profiles-browse)
- [Matches](#matches)
- [Messages](#messages)
- [Favourites](#favourites)
- [Interests](#interests)
- [Static Files](#static-files)
- [HTTP Status Code Reference](#http-status-code-reference)

---

## Authentication

### POST /api/auth/register
Registers a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1998-05-14",
  "gender": "male",
  "looking_for": "female",
  "password": "SecurePass123"
}
```

**Success Response — 201 Created:**
```json
{
  "message": "User registered successfully",
  "user_id": 1
}
```

**Error Responses:**
- `400 Bad Request` — `{ "error": "Email already in use" }`
- `422 Unprocessable Entity` — validation errors with field details

---

### POST /api/auth/login
Logs in a user and creates a session.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Success Response — 200 OK:**
```json
{
  "message": "Login successful",
  "user_id": 1
}
```

**Error Responses:**
- `401 Unauthorized` — `{ "error": "Invalid email or password" }`

---

### POST /api/auth/logout
Logs out the currently authenticated user and clears the session.

**Success Response — 200 OK:**
```json
{ "message": "Logged out successfully" }
```

**Error Response:**
- `401 Unauthorized` — no active session

---

### GET /api/auth/me
Returns the currently logged-in user's basic information.

**Success Response — 200 OK:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe"
}
```

**Error Response:**
- `401 Unauthorized` — not logged in

---

## Profile

### GET /api/profile
Returns the authenticated user's own full profile.

**Success Response — 200 OK:**
```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "age": 26,
  "bio": "Software dev by day, photographer by night.",
  "location": "Kingston, Jamaica",
  "gender": "male",
  "looking_for": "female",
  "interests": ["hiking", "photography", "coding"],
  "profile_photo": "/uploads/photos/1.jpg",
  "visibility": "public",
  "is_boosted": false,
  "created_at": "2026-04-01T09:00:00"
}
```

**Error Response:**
- `401 Unauthorized` — not logged in

---

### PUT /api/profile
Updates the authenticated user's profile. Partial updates are accepted.

**Request Body (all fields optional):**
```json
{
  "bio": "Updated bio text here",
  "location": "Montego Bay, Jamaica",
  "interests": ["gaming", "cooking", "hiking"],
  "visibility": "private"
}
```

**Success Response — 200 OK:**
```json
{ "message": "Profile updated successfully" }
```

**Error Responses:**
- `400 Bad Request` — invalid data provided
- `401 Unauthorized` — not logged in

---

### POST /api/profile/boost
Boosts the authenticated user's profile (premium feature) so it appears higher in browse results.

**Request Body:** *(none required)*

**Success Response — 200 OK:**
```json
{ "message": "Profile boosted successfully" }
```

**Error Responses:**
- `401 Unauthorized` — not logged in
- `400 Bad Request` — boost already active

---

## Profiles (Browse)

### GET /api/profiles
Returns a list of profiles for the authenticated user to browse (excludes already-actioned profiles).

**Query Parameters (optional):**

| Parameter | Type | Description |
|-----------|------|-------------|
| `location` | string | Filter by city/region |
| `age_min` | integer | Minimum age |
| `age_max` | integer | Maximum age |
| `interests` | string | Comma-separated interest names |
| `gender` | string | Filter by gender |
| `sort` | string | `newest` or `match_score` |

**Success Response — 200 OK:**
```json
[
  {
    "id": 3,
    "first_name": "Alice",
    "age": 25,
    "location": "Kingston, Jamaica",
    "bio": "Love hiking and adventure!",
    "interests": ["hiking", "travel"],
    "match_score": 82.5,
    "profile_photo": "/uploads/photos/3.jpg"
  }
]
```

---

### POST /api/profiles/\<profile_id\>/action
Performs a Like or Pass action on a profile.

**Request Body:**
```json
{ "action": "like" }
```
> `action` must be either `"like"` or `"pass"`

**Success Response — 200 OK (no mutual match yet):**
```json
{
  "message": "Action recorded",
  "mutual_match": false
}
```

**Success Response — 200 OK (mutual match created):**
```json
{
  "message": "It's a match!",
  "mutual_match": true,
  "match_id": 5
}
```

**Error Responses:**
- `400 Bad Request` — invalid action value
- `404 Not Found` — profile does not exist
- `409 Conflict` — action already recorded for this profile

---

## Matches

### GET /api/matches
Returns all mutual matches for the authenticated user.

**Success Response — 200 OK:**
```json
[
  {
    "match_id": 5,
    "user": {
      "id": 3,
      "first_name": "Alice",
      "age": 25,
      "location": "Kingston, Jamaica",
      "profile_photo": "/uploads/photos/3.jpg"
    },
    "match_score": 82.5,
    "matched_at": "2026-04-20T10:32:00"
  }
]
```

**Error Response:**
- `401 Unauthorized` — not logged in

---

## Messages

### GET /api/messages/\<match_id\>
Retrieves the full message history for a mutual match conversation.

**Success Response — 200 OK:**
```json
[
  {
    "id": 1,
    "sender_id": 1,
    "content": "Hey! How are you?",
    "sent_at": "2026-04-21T14:05:00"
  },
  {
    "id": 2,
    "sender_id": 3,
    "content": "Doing great, thanks!",
    "sent_at": "2026-04-21T14:06:30"
  }
]
```

**Error Responses:**
- `403 Forbidden` — users are not a mutual match
- `404 Not Found` — match does not exist

---

### POST /api/messages
Sends a message to a matched user.

**Request Body:**
```json
{
  "match_id": 5,
  "content": "Hey! How are you?"
}
```

**Success Response — 201 Created:**
```json
{
  "message_id": 1,
  "sent_at": "2026-04-21T14:05:00"
}
```

**Error Responses:**
- `400 Bad Request` — empty message content
- `403 Forbidden` — not a mutual match

---

## Favourites

### GET /api/favorites
Returns all profiles the authenticated user has favourited.

**Success Response — 200 OK:**
```json
[
  {
    "favourite_id": 1,
    "user": {
      "id": 7,
      "first_name": "Emma",
      "age": 23,
      "location": "Montego Bay, Jamaica",
      "profile_photo": "/uploads/photos/7.jpg"
    },
    "saved_at": "2026-04-22T09:15:00"
  }
]
```

---

### POST /api/profiles/\<profile_id\>/favorite
Adds a profile to the authenticated user's favourites.

**Success Response — 201 Created:**
```json
{ "message": "Profile added to favourites" }
```

**Error Responses:**
- `409 Conflict` — already favourited
- `404 Not Found` — profile does not exist

---

### DELETE /api/profiles/\<profile_id\>/favorite
Removes a profile from the authenticated user's favourites.

**Success Response — 200 OK:**
```json
{ "message": "Removed from favourites" }
```

**Error Response:**
- `404 Not Found` — favourite record does not exist

---

## Interests

### GET /api/interests
Returns the full list of available interests/hobbies for use in profile setup and filtering.

**Success Response — 200 OK:**
```json
[
  { "id": 1, "name": "hiking" },
  { "id": 2, "name": "photography" },
  { "id": 3, "name": "coding" },
  { "id": 4, "name": "cooking" }
]
```

---

## Static Files

### GET /uploads/\<filename\>
Serves uploaded files (profile photos, etc.) stored on the server.

**Example:** `GET /uploads/photos/1.jpg`

**Error Response:**
- `404 Not Found` — file does not exist

---

## HTTP Status Code Reference

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET, PUT, DELETE |
| 201 | Created | New resource successfully created |
| 400 | Bad Request | Missing or invalid data |
| 401 | Unauthorized | Not logged in / no valid session |
| 403 | Forbidden | Logged in but lacks permission |
| 404 | Not Found | Resource does not exist |
| 409 | Conflict | Duplicate action (already liked, already favourited) |
| 422 | Unprocessable Entity | Validation failed on input fields |
| 500 | Internal Server Error | Unexpected server-side error |

---

*DriftDater API — INFO3180 Group Project, UWI Mona*