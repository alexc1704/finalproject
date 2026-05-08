# DriftDater

A Vue 3 + Flask dating application for INFO3180. The app uses a Flask REST API, SQLAlchemy models, Flask-Migrate database migrations, bcrypt password hashing, sessions, and a Vue frontend.

## Implemented features

- User registration with email validation and bcrypt password hashing
- Secure login, logout, and session-backed `/api/auth/me`
- Profile creation/editing with age, bio, location preferences, interests, photo upload, occupation, education, and visibility controls
- Database-backed browse page with search, age filters, location filters, interest filters, goal filters, premium/verified/boosted filters, and sorting
- Simple matching algorithm using shared interests, location, age preference, and relationship goal
- Like, dislike, pass, favorites/bookmarks, and mutual match detection
- Database-backed matches page
- Database-backed conversations and messages with polling for near-real-time updates
- Premium features: premium badge, verified badge, advanced filters, and profile boost
- Dark mode / light mode theme toggle
- Faker-style seeded users for testing once a user logs in

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
flask db upgrade
flask --app app --debug run --host 127.0.0.1 --port 5050
```

In a second terminal:

```bash
npm install
npm run dev
```

Open: `http://localhost:5173`

## Fresh database reset

```bash
del instance\app.db
flask db upgrade
```

## Test notes

- Create a new account with a valid email and at least 3 interests.
- Browse automatically has seeded database users after login.
- Some seeded users have already liked the logged-in user, so liking them back creates a mutual match.
- Open Matches, then Messages, to test persistent conversations.
- Turn on Premium in Profile to use Boost Profile.

## Final feature notes

This build connects the Vue frontend to the Flask/SQLAlchemy backend instead of using hard-coded profiles or messages. Registered users are stored in the `users` table with bcrypt password hashes, profile details are stored in `profiles`, interests use a many-to-many table, actions are stored in `likes`, mutual matches are stored in `matches`, saved profiles are stored in `favorites`, and chat history is stored in `messages`.

The app also includes two optional enhancement features: Premium/verified profile badges with profile boosting, and dark/light theme customization. For demonstration purposes, generated seed users can auto-reply when messaged so the messaging screen clearly shows send/receive behavior. Real registered users do not auto-reply; they must log in and reply from another session.
