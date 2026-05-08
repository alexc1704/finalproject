# 💘 DriftDater — Date Matching Application

> A full-stack dating web platform built with **Vue 3** (frontend) and **Flask** (backend).
> Course: INFO3180 | Due: Thursday May 08, 2026

---

## Table of Contents
- [Project Description](#project-description)
- [Team Members & Roles](#team-members--roles)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Deployed Application](#deployed-application)
- [Known Issues & Limitations](#known-issues--limitations)
- [Project Structure](#project-structure)

---

## Project Description

**DriftDater** is a full-featured dating web application that allows registered users to:

- Create and manage detailed personal profiles
- Discover compatible matches using a smart matching algorithm
- Like or Pass on other users' profiles
- Message mutual matches
- Search and filter potential matches by location, age, and interests

Built with a Vue 3 frontend, Flask REST API backend, and PostgreSQL database.

---

## Team Members & Roles

| Name | Role | Responsibilities |
|------|------|-----------------|
| Kelandra | Project Manager / Documentation Lead | Timeline, coordination, README, API docs, user manual |
| Stephen | Backend Developer | Flask API, database models, authentication, security |
| Blair | Backend Developer | API endpoints, database migrations, input validation |
| Alex | Frontend Developer | Vue 3 components, routing, UI/UX design |
| Nasya | Frontend Developer | State management, forms, responsive design |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue 3, Vue Router, JavaScript, Vite |
| Backend | Python 3.x, Flask, Flask-SQLAlchemy, Flask-Migrate |
| Database | PostgreSQL (production) / SQLite (development) |
| Authentication | Flask Sessions + Bcrypt |

---

## Features

### Core Features

**Authentication & Profile Management**
- User registration with email validation
- Secure login and logout
- Password hashing with bcrypt
- Profile creation and editing (name, age, bio, location, interests, profile photo)
- Profile visibility controls (public/private)

**Matching System**
- Algorithm based on location, age range, shared interests, and gender preference
- Like / Pass action on browse mode
- Mutual match detection (both users must Like each other)
- Match notifications and confirmations
- Browse mode with filtering options

**Messaging**
- Messages restricted to mutual matches only
- Persistent message history in database
- Conversation list with timestamps
- Near-real-time updates via Vue reactivity

**Search & Discovery**
- Filter by location, age range, interests, gender, goals
- Sort by newest or highest match score
- Bookmark / favourite profiles

### Optional Features Implemented
- Premium User Features (profile boost)
- Dark mode

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL (or SQLite for local development)
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/alexc1704/finalproject.git
cd finalproject
```

### 2. Backend Setup (Flask)
```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
.\venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

Create a `.env` file in the project root based on `.env.sample`:
```
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://username:password@localhost/driftdater
DEBUG=True
```

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
flask --app app --debug run
# Runs at http://localhost:5000
```

### 3. Frontend Setup (Vue 3)
Open a **new terminal** in the same project root:
```bash
npm install
npm run dev
# Runs at http://localhost:5173
```

### 4. Servers at a Glance
| Service | URL |
|---------|-----|
| Flask API | http://localhost:5000 |
| Vue Frontend | http://localhost:5173 |

---

## API Documentation

Full details in [`docs/API_DOCUMENTATION.md`](./docs/API_DOCUMENTATION.md).

### Endpoint Quick Reference

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:---:|
| POST | `/api/auth/register` | Register new user | No |
| POST | `/api/auth/login` | Login | No |
| POST | `/api/auth/logout` | Logout | Yes |
| GET | `/api/auth/me` | Get current logged-in user | Yes |
| GET | `/api/profile` | Get own profile | Yes |
| PUT | `/api/profile` | Update own profile | Yes |
| GET | `/api/profiles` | Browse all profiles | Yes |
| POST | `/api/profiles/<id>/action` | Like or Pass on a profile | Yes |
| POST | `/api/profiles/<id>/favorite` | Favourite a profile | Yes |
| DELETE | `/api/profiles/<id>/favorite` | Remove favourite | Yes |
| GET | `/api/matches` | Get mutual matches | Yes |
| GET | `/api/messages/<match_id>` | Get messages for a match | Yes |
| POST | `/api/messages` | Send a message | Yes |
| POST | `/api/profile/boost` | Boost profile (premium) | Yes |
| GET | `/api/favorites` | Get favourited profiles | Yes |
| GET | `/api/interests` | Get list of all interests | No |
| GET | `/uploads/<filename>` | Serve uploaded files | No |

---

## Database Schema

ER Diagram: [`docs/ER_DIAGRAM.png`](./docs/ER_Diagram.png)

| Table | Description |
|-------|-------------|
| `users` | Account credentials and basic info |
| `profiles` | Bio, location, age, photo |
| `interests` | Master list of interests/hobbies |
| `user_interests` | Many-to-many: users ↔ interests |
| `matches` | Like/pass actions between users |
| `messages` | Conversations between mutual matches |
| `favourites` | Bookmarked profiles per user |

All tables normalised to **3rd Normal Form (3NF)**. Indexes on `user_id`, `email`, `location`, `created_at`.

---

## Deployed Application

| Resource | URL |
|----------|-----|
| GitHub Repo | https://github.com/alexc1704/finalproject |



---

## Known Issues & Limitations
- Messaging uses Vue polling, not WebSockets — slight delay may occur
- Profile photo uploads: JPG/PNG only, max 5MB
- Location matching is city-name text based, not GPS
- Registered users are not currently being shown on the main page
- Difficulty with user response handling in some edge cases

---

## Project Structure

```
finalproject/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── forms.py
│   ├── models.py
│   └── views.py
│
├── migrations/
│   ├── versions/
│   │   └── 168716fccd0e_correction_migration.py
│   ├── alembic.ini
│   ├── env.py
│   └── script.py.mako
│
├── src/
│   ├── assets/
│   │   ├── base.css
│   │   └── logo.svg
│   ├── components/
│   │   ├── AppFooter.vue
│   │   ├── AppHeader.vue
│   │   ├── LoadingSpinner.vue
│   │   ├── MessageBubble.vue
│   │   └── ProfileCard.vue
│   ├── router/
│   │   └── index.js
│   ├── stores/
│   │   └── auth.js
│   ├── views/
│   │   ├── DashboardView.vue
│   │   ├── HomeView.vue
│   │   ├── LoginView.vue
│   │   ├── MatchesView.vue
│   │   ├── MessagesView.vue
│   │   ├── NotFoundView.vue
│   │   ├── ProfileView.vue
│   │   └── RegisterView.vue
│   ├── App.vue
│   └── main.js
│
├── public/
│   └── favicon.ico
│
├── docs/
│   ├── API_DOCUMENTATION.md
│   ├── user_manual.md
│   └── er_diagram.png
│
├── .env.sample
├── .gitignore
├── index.html
├── package.json
├── requirements.txt
├── vite.config.js
└── README.md
```

---

*INFO3180 Group Project — University of the West Indies, Mona | Contact: laurie.leitch@uwi.edu*
