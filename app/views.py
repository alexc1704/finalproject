from datetime import datetime, timedelta
from functools import wraps
import os
import re
import random
from uuid import uuid4
import random


try:
    from faker import Faker
except ImportError:
    Faker = None

from flask import jsonify, request, session, send_from_directory
from werkzeug.utils import secure_filename

from app import app, bcrypt, db
from app.models import Favorite, Interest, Like, Match, Message, Profile, User

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

AUTO_REPLY_BANK = [
    "Haha I get you 😄",
    "That sounds interesting. Tell me more!",
    "I like that vibe 😊",
    "Nice! What made you say that?",
    "Same here honestly.",
    "That would be fun sometime!",
    "I was just thinking about that too.",
    "You seem easy to talk to 😊",
    "Hmm, I never thought about it like that.",
    "That’s actually a good point.",
    "Okayyy, I see what you mean.",
    "You have my attention now 👀",
    "That sounds like something I’d want to hear more about.",
    "Not gonna lie, that made me smile.",
    "You seem like you have good energy.",
    "I feel like we could talk about that for a while.",
    "That’s a vibe honestly.",
    "Interestinggg, tell me more.",
    "Haha wait, explain that more.",
    "I like how you think."
]


AUTO_REPLY_CATEGORIES = [
    {
        "name": "greeting",
        "keywords": [
            "hey", "hi", "hello", "yo", "good morning", "good evening", "good afternoon",
            "sup", "wagwan", "wah gwaan", "hola", "heyy", "hii"
        ],
        "responses": [
            "Heyy 😊",
            "Hi there!",
            "Hey, how’s your day going?",
            "Hii 😊 nice to hear from you.",
            "Hey you 😄",
            "Hello hello!",
            "Heyy, what are you up to?",
            "Hi 😊 how’s everything?",
            "Hey, I was hoping you’d message.",
            "Well hello there 😄",
            "Heyyy, how are you?",
            "Hi! You seem friendly already.",
            "Hey, what’s the vibe today?",
            "Yo 😄 what’s good?",
            "Hey, nice seeing your message pop up."
        ],
    },
    {
        "name": "how_are_you",
        "keywords": [
            "how are you", "how are u", "how you doing", "how yuh doing", "how are things",
            "how is your day", "how's your day", "how was your day", "are you okay",
            "you good", "u good", "wyd", "what are you doing", "what you doing"
        ],
        "responses": [
            "I’m doing good 😊 what about you?",
            "Pretty good honestly. Just relaxing.",
            "I’m okayyy 😄 how about yourself?",
            "I’m good, better now that you messaged.",
            "I’m doing alright. How’s your day going?",
            "I’m chilling honestly. What about you?",
            "I’m good 😊 just taking the day easy.",
            "Not bad at all. What have you been up to?",
            "I’m feeling good today, can’t complain.",
            "I’m good, just in a talkative mood.",
            "I’m alright. You checking up on me? 😊",
            "Doing pretty well. Tell me about your day.",
            "I’m good, just relaxing a bit.",
            "I’m okay, but I could use a fun conversation.",
            "I’m doing fine 😊 what’s on your mind?"
        ],
    },
    {
        "name": "date_invite",
        "keywords": [
            "date", "go on a date", "take you out", "go out", "link up", "meet up",
            "hang out", "see you", "can we meet", "want to meet", "dinner", "movie date",
            "coffee date", "lunch date", "take me out"
        ],
        "responses": [
            "That actually sounds really nice 😊",
            "I’d be down for that honestly.",
            "Where would you take me? 👀",
            "A date sounds cute. What did you have in mind?",
            "Hmm, I might say yes depending on the plan 😊",
            "That sounds fun. Are we talking food, movie, or adventure?",
            "I like the confidence 😄 what’s the plan?",
            "Maybeee 👀 tell me what kind of date.",
            "That could be nice. I’d want somewhere with good vibes.",
            "I’m open to it if the conversation keeps flowing.",
            "A thoughtful date would definitely get my attention.",
            "That sounds sweet. What would we do?",
            "I’d consider it 😊 convince me with the plan.",
            "Food date or activity date?",
            "That sounds like a vibe honestly."
        ],
    },
    {
        "name": "compliment",
        "keywords": [
            "beautiful", "pretty", "cute", "handsome", "gorgeous", "fine", "attractive",
            "sexy", "nice smile", "look good", "you look good", "stunning", "lovely",
            "queen", "king", "hot"
        ],
        "responses": [
            "Aww thank you 😊 that’s sweet.",
            "You’re making me blush a little.",
            "That’s really nice of you to say.",
            "Smoothhh 😄 thank you.",
            "I appreciate that 😊",
            "Okay, you’re good with compliments.",
            "That was cute, thank you.",
            "You know how to make someone smile.",
            "Thank you 😊 that actually made my day.",
            "Aww, you seem sweet.",
            "That’s a nice way to start a conversation.",
            "You’re not too bad yourself 😄",
            "Haha thank you, I’ll take that.",
            "That compliment landed well 😊",
            "You’re making a good impression."
        ],
    },
    {
        "name": "music",
        "keywords": [
            "music", "song", "artist", "playlist", "spotify", "apple music", "dancehall",
            "reggae", "r&b", "rap", "hip hop", "afrobeats", "soca", "concert", "album",
            "sing", "singing"
        ],
        "responses": [
            "I love music 😄 what do you listen to?",
            "Music taste says a lot about a person honestly.",
            "Okay, what’s one song you’d put me on to?",
            "I’m always looking for new songs. What’s your current favorite?",
            "That’s a good topic. Are you more dancehall, R&B, or something else?",
            "Music can change my whole mood honestly.",
            "Send me a song that describes your vibe.",
            "I feel like playlist chemistry matters 😄",
            "What artist have you been playing the most lately?",
            "I love a good music conversation.",
            "You seem like you might have interesting taste.",
            "What’s your go-to song when you’re in a good mood?",
            "I’d definitely judge you by your playlist a little 😭",
            "Music dates sound underrated.",
            "That’s a vibe. What genre do you like most?"
        ],
    },
    {
        "name": "gaming",
        "keywords": [
            "game", "gaming", "gamer", "fifa", "cod", "call of duty", "fortnite", "valorant",
            "minecraft", "2k", "gta", "playstation", "ps5", "xbox", "pc", "steam",
            "controller", "twitch", "stream"
        ],
        "responses": [
            "Ouuu you game too? 👀",
            "What games do you normally play?",
            "Okay gamer, are you competitive or just for fun?",
            "That’s cool. Console or PC?",
            "I feel like gaming dates could be fun.",
            "You better not be toxic on the mic 😭",
            "What’s your favorite game right now?",
            "Are you the carry or the one getting carried? 😄",
            "That sounds fun. I’d probably talk mess while playing.",
            "Gaming and good conversation is a strong combo.",
            "Okay, what game would you teach me?",
            "I like that. Do you stream too?",
            "That could be a fun way to hang out.",
            "I’m interested now. What rank are you?",
            "Gaming together sounds like a vibe."
        ],
    },
    {
        "name": "food",
        "keywords": [
            "food", "eat", "restaurant", "dinner", "lunch", "breakfast", "cook", "cooking",
            "pizza", "burger", "jerk", "chicken", "pasta", "seafood", "sushi", "dessert",
            "ice cream", "coffee", "drink", "hungry"
        ],
        "responses": [
            "Food dates are elite honestly 😭",
            "What’s your favorite food?",
            "Okay but are you sharing fries or no?",
            "A good food spot can fix almost anything.",
            "That sounds nice. I love trying new food places.",
            "You had me at food 😄",
            "What’s your go-to order?",
            "If you can cook, that’s bonus points.",
            "Food is definitely a love language.",
            "Now I’m hungry 😭",
            "That sounds like a perfect date idea.",
            "Are you more casual food spot or fancy dinner?",
            "I’d definitely be down for a food adventure.",
            "What restaurant would you recommend?",
            "Food plus good conversation sounds perfect."
        ],
    },
    {
        "name": "movies",
        "keywords": [
            "movie", "film", "netflix", "series", "show", "anime", "cinema", "watch",
            "horror", "comedy", "romance", "action", "documentary", "binge"
        ],
        "responses": [
            "I’m always down for a good movie. What kind do you like?",
            "Movie night sounds like a vibe.",
            "Are you a horror person or do you get scared easily? 😄",
            "I need recommendations. What are you watching now?",
            "That sounds like a chill plan.",
            "I love shows that keep me hooked.",
            "Netflix and snacks? That’s a classic.",
            "What’s one movie you can watch over and over?",
            "I’m judging your movie taste a little 😭",
            "That could be a good date idea.",
            "I like movies with good stories.",
            "Are you into anime too?",
            "That sounds fun. I’d bring snacks.",
            "What series are you currently watching?",
            "Movie conversations always reveal personality."
        ],
    },
    {
        "name": "travel_outdoors",
        "keywords": [
            "travel", "trip", "vacation", "beach", "river", "hike", "hiking", "mountain",
            "nature", "outdoor", "road trip", "adventure", "explore", "swim", "swimming",
            "jamaica", "ochi", "montego bay", "portland", "negril"
        ],
        "responses": [
            "I love outdoor plans. That sounds like a vibe!",
            "That would be fun. Where would you want to go?",
            "A beach day sounds perfect honestly.",
            "I like people who enjoy exploring.",
            "Road trips are underrated.",
            "That sounds peaceful. I’d definitely be interested.",
            "Okay, adventure person 👀",
            "Nature dates can be so nice.",
            "I’d want good music for the drive though.",
            "That sounds like the kind of memory I’d enjoy.",
            "Where’s your favorite place to go?",
            "That’s a nice idea. I like scenic spots.",
            "I could definitely do a chill beach day.",
            "That sounds refreshing.",
            "Travel plans always make conversations better."
        ],
    },
    {
        "name": "school_work",
        "keywords": [
            "school", "class", "uwi", "utech", "college", "university", "exam", "study",
            "assignment", "project", "work", "job", "career", "business", "degree",
            "course", "deadline"
        ],
        "responses": [
            "School has been a lot lately, but I’m managing 😅",
            "Oh nice, what are you studying?",
            "Work-life balance is so hard sometimes.",
            "I respect someone who’s focused.",
            "That sounds stressful. Hope you’re taking breaks too.",
            "What’s your career goal?",
            "Assignments really love appearing at the worst time 😭",
            "I like ambition. That’s attractive.",
            "You sound like you have a lot going on.",
            "I hope the hard work pays off for you.",
            "Tell me more about what you do.",
            "That’s interesting. Do you enjoy it?",
            "I know that deadline pressure too well.",
            "At least you’re pushing through.",
            "Focused people are underrated."
        ],
    },
    {
        "name": "relationship_goals",
        "keywords": [
            "relationship", "love", "dating", "serious", "long term", "long-term",
            "casual", "commitment", "loyal", "loyalty", "marriage", "partner",
            "girlfriend", "boyfriend", "single"
        ],
        "responses": [
            "I like when people are clear about what they want.",
            "That’s important. Communication matters a lot.",
            "I’m more interested in something genuine.",
            "Loyalty is definitely important to me.",
            "I respect honesty when it comes to dating.",
            "It depends on the connection honestly.",
            "I think the best relationships start with good conversation.",
            "I like when things feel natural, not forced.",
            "That’s a good thing to talk about early.",
            "I’m open-minded, but I value respect.",
            "A real connection matters more than rushing.",
            "I like consistency more than big promises.",
            "That’s fair. What are you looking for?",
            "I appreciate someone who knows their intentions.",
            "Connection and communication are big for me."
        ],
    },
    {
        "name": "plans_weekend",
        "keywords": [
            "weekend", "tonight", "today", "tomorrow", "plans", "free", "available",
            "busy", "party", "club", "outing", "event", "link"
        ],
        "responses": [
            "I might be free. What did you have in mind?",
            "Depends on the plan 👀",
            "I like spontaneous plans sometimes.",
            "Tonight could be nice if the vibe is right.",
            "What kind of plans are you thinking?",
            "I’m not sure yet, but I’m open to ideas.",
            "A chill plan sounds good honestly.",
            "Weekend plans are always better with good company.",
            "I could be convinced 😄",
            "Tell me the plan and I’ll rate it.",
            "That sounds like it could be fun.",
            "I usually like something relaxed.",
            "Maybe, what time were you thinking?",
            "I like when someone actually plans properly.",
            "What’s the vibe, chill or outside?"
        ],
    },
    {
        "name": "humor_laugh",
        "keywords": [
            "lol", "lmao", "haha", "funny", "joke", "joking", "laugh", "dead",
            "😭", "😂", "🤣"
        ],
        "responses": [
            "You’re funny 😭",
            "Haha stoppp 😄",
            "Not you making me laugh.",
            "Okay, you have jokes.",
            "I like your sense of humor.",
            "That actually made me laugh.",
            "You’re unserious 😭",
            "I can tell you’d be fun to talk to.",
            "Haha you’re trouble.",
            "That was a good one.",
            "I like someone who can make me laugh.",
            "You’re making this conversation easy.",
            "Haha, I wasn’t expecting that.",
            "Okay comedian 😄",
            "That’s the energy I like."
        ],
    },
    {
        "name": "deep_conversation",
        "keywords": [
            "life", "dream", "goals", "future", "purpose", "meaning", "mental", "growth",
            "healing", "faith", "family", "values", "honest", "trust", "respect"
        ],
        "responses": [
            "That’s actually a deep question.",
            "I like conversations like this.",
            "That says a lot about how you think.",
            "I value honesty and growth a lot.",
            "That’s something worth talking about properly.",
            "You seem thoughtful.",
            "I respect that perspective.",
            "That’s a mature way to look at it.",
            "I like people who can talk about real things.",
            "That made me think for a second.",
            "I appreciate meaningful conversations.",
            "That sounds important to you.",
            "I feel like values matter a lot.",
            "That’s the kind of topic that builds connection.",
            "I like where this conversation is going."
        ],
    },
    {
        "name": "photos_profile",
        "keywords": [
            "picture", "pic", "photo", "profile", "selfie", "image", "look", "fit",
            "outfit", "style", "dress", "hair"
        ],
        "responses": [
            "I like when someone has their own style.",
            "Your profile caught my attention too.",
            "A good picture says a lot.",
            "Style matters, but personality matters more.",
            "I like confidence in a profile.",
            "That’s cute 😊",
            "You seem like you pay attention to details.",
            "I’d want to see more of your personality too.",
            "Photos are nice, but conversation seals it.",
            "Okay, I see you 👀",
            "That’s a good look.",
            "You have style?",
            "I like people who present themselves well.",
            "A nice outfit always helps.",
            "Confidence looks good on people."
        ],
    },
    {
        "name": "app_meta",
        "keywords": [
            "match", "matched", "profile", "app", "driftdater", "swipe", "liked you",
            "likes", "message me", "chat"
        ],
        "responses": [
            "I guess the app did something right matching us 😄",
            "Looks like we matched for a reason.",
            "Your profile seemed interesting to me.",
            "I’m glad we matched 😊",
            "Okay, let’s see if the match makes sense.",
            "I like that you actually started a conversation.",
            "Most people just match and say nothing 😭",
            "Your message already makes this more interesting.",
            "Let’s see if the compatibility score was right.",
            "I’m curious about you now.",
            "The profile was one thing, but conversation matters more.",
            "This could be a good match.",
            "I’m glad you didn’t just say nothing.",
            "So what made you like my profile?",
            "I like when matches actually talk."
        ],
    },
]


def get_auto_reply(message):
    text = message.lower().strip()

    # Score each response category by how many of its keywords appear.
    # Longer phrase matches count more than short one-word matches.
    best_category = None
    best_score = 0

    for category in AUTO_REPLY_CATEGORIES:
        score = 0
        for keyword in category["keywords"]:
            keyword = keyword.lower()
            if keyword in text:
                score += 3 if " " in keyword else 1

        if score > best_score:
            best_score = score
            best_category = category

    if best_category and best_score > 0:
        return random.choice(best_category["responses"])

    # If no keyword category matches, choose a general conversational response.
    return random.choice(AUTO_REPLY_BANK)



def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def normalize_interest(name):
    return re.sub(r"\s+", " ", str(name).strip().lower())


def clean_interests(items):
    return [normalize_interest(x) for x in items if normalize_interest(x)]


def calculate_age(dob):
    dob_date = datetime.strptime(dob, "%Y-%m-%d")
    today = datetime.today()
    return today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))


def current_user():
    uid = session.get("user_id")
    return User.query.get(uid) if uid else None


def should_auto_reply(user):
    """Return True for generated demo users so chat demos feel alive.
    Real registered users do not auto-reply; they must log in and respond themselves.
    """
    return bool(user and user.email and user.email.startswith("driftdater.seed"))


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user():
            return jsonify({"error": "Authentication required"}), 401
        return fn(*args, **kwargs)
    return wrapper


def profile_to_dict(profile, viewer=None, include_private=False):
    user = profile.user
    interests = [i.name for i in profile.interests]
    data = {
        "id": profile.id,
        "user_id": profile.user_id,
        "email": user.email if include_private else None,
        "username": user.username,
        "first_name": profile.first_name,
        "last_name": profile.last_name,
        "name": f"{profile.first_name} {profile.last_name}",
        "age": profile.age,
        "gender": profile.gender,
        "looking_for": profile.looking_for,
        "bio": profile.bio,
        "location": profile.location,
        "preferred_location": profile.preferred_location or "",
        "min_age": profile.min_age or 18,
        "max_age": profile.max_age or 99,
        "relationship_goal": profile.relationship_goal or "",
        "occupation": profile.occupation or "",
        "education": profile.education or "",
        "is_private": user.is_private,
        "is_premium": user.is_premium,
        "is_verified": user.is_verified,
        "is_boosted": bool(user.boosted_until and user.boosted_until > datetime.utcnow()),
        "boosted_until": user.boosted_until.isoformat() if user.boosted_until else None,
        "profile_picture": profile.profile_picture or "",
        "photo": profile.profile_picture or "",
        "interests": interests,
        "created_at": profile.created_at.isoformat() if profile.created_at else None,
    }
    if viewer and viewer.profile and viewer.id != profile.user_id:
        data["match_score"] = match_score(viewer.profile, profile)
        data["is_favorite"] = Favorite.query.filter_by(user_id=viewer.id, profile_id=profile.id).first() is not None
        action = Like.query.filter_by(liker_id=viewer.id, liked_id=profile.user_id).first()
        data["my_action"] = action.action if action else None
    return data


def user_to_dict(user):
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "is_private": user.is_private,
        "is_premium": user.is_premium,
        "is_verified": user.is_verified,
        "is_boosted": bool(user.boosted_until and user.boosted_until > datetime.utcnow()),
        "profile": profile_to_dict(user.profile, include_private=True) if user.profile else None,
    }


def match_score(my_profile, other):
    score = 20
    my_interests = {i.name for i in my_profile.interests}
    other_interests = {i.name for i in other.interests}
    shared = my_interests & other_interests
    score += min(len(shared) * 15, 35)

    if other.location.lower() == my_profile.location.lower():
        score += 20
    elif my_profile.preferred_location and my_profile.preferred_location.lower() in other.location.lower():
        score += 15

    if (my_profile.min_age or 18) <= other.age <= (my_profile.max_age or 99):
        score += 15

    if (my_profile.relationship_goal or "").lower() == (other.relationship_goal or "").lower():
        score += 10

    return min(score, 100)


def get_or_create_interest(name):
    clean = normalize_interest(name)
    interest = Interest.query.filter_by(name=clean).first()
    if not interest:
        interest = Interest(name=clean)
        db.session.add(interest)
    return interest


def save_profile_picture(file):
    if not file or file.filename == "" or not allowed_file(file.filename):
        return None
    original = secure_filename(file.filename)
    ext = original.rsplit(".", 1)[1].lower()
    filename = f"{uuid4().hex}.{ext}"
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    return f"/uploads/{filename}"



fake = Faker() if Faker else None
if fake:
    Faker.seed(3180)

SEED_FIRST_NAMES = ["Amelia", "Brianna", "Cassie", "Dana", "Elena", "Faith", "Gabrielle", "Hannah", "Ivy", "Jada", "Kayla", "Leah", "Maya", "Nia", "Olivia", "Renee", "Sasha", "Tiana", "Zara", "Andre", "Brian", "Chris", "Daniel", "Ethan", "Jason", "Kevon", "Liam", "Malik", "Nathan", "Omar", "Ryan", "Sean", "Tevin", "Xavier"]
SEED_LAST_NAMES = ["Brown", "Campbell", "Clarke", "Davis", "Edwards", "Francis", "Gordon", "Henry", "Johnson", "King", "Lewis", "Miller", "Morgan", "Nelson", "Reid", "Roberts", "Smith", "Taylor", "Thomas", "Williams"]
SEED_LOCATIONS = ["Kingston, Jamaica", "Portmore, Jamaica", "Spanish Town, Jamaica", "Half Way Tree, Jamaica", "New Kingston, Jamaica", "Mandeville, Jamaica", "Montego Bay, Jamaica", "May Pen, Jamaica", "Ocho Rios, Jamaica"]
SEED_INTERESTS = ["gaming", "music", "travel", "fitness", "foodie", "movies", "art", "reading", "tech", "nature", "sports", "photography", "cooking", "theatre", "wellness", "dancing", "hiking", "anime", "fashion", "coffee"]
SEED_OCCUPATIONS = ["Student", "Developer", "Teacher", "Designer", "Nurse", "Entrepreneur", "Streamer", "Chef", "Photographer", "Accountant", "Marketing Assistant", "Fitness Coach"]
SEED_EDUCATION = ["UWI", "UTECH", "UCC", "Edna Manley", "NCTVET", "Northern Caribbean University", "Community College"]
SEED_GOALS = ["Friendship", "Long-term", "Casual", "Networking"]


def create_seed_profile(index):
    email = f"driftdater.seed{index}@example.com"
    existing = User.query.filter_by(email=email).first()
    if existing:
        return existing

    gender = "Female" if index % 2 == 0 else "Male"
    if fake:
        first = fake.first_name_female() if gender == "Female" else fake.first_name_male()
        last = fake.last_name()
    else:
        first = SEED_FIRST_NAMES[index % len(SEED_FIRST_NAMES)]
        last = SEED_LAST_NAMES[(index * 3) % len(SEED_LAST_NAMES)]
    age = 18 + ((index * 7) % 18)
    location = SEED_LOCATIONS[(index * 5) % len(SEED_LOCATIONS)]
    goal = SEED_GOALS[index % len(SEED_GOALS)]
    chosen = [SEED_INTERESTS[(index + j * 3) % len(SEED_INTERESTS)] for j in range(3 + (index % 3))]

    user = User(
        email=email,
        username=f"seeduser{index}",
        password_hash=bcrypt.generate_password_hash("password123").decode("utf-8"),
        is_private=False,
        is_premium=(index % 5 == 0),
        is_verified=(index % 4 == 0),
        boosted_until=(datetime.utcnow() + timedelta(days=7)) if index % 7 == 0 else None,
    )
    db.session.add(user)
    db.session.flush()

    profile = Profile(
        user_id=user.id,
        first_name=first,
        last_name=last,
        age=age,
        gender=gender,
        looking_for="Everyone",
        bio=f"{goal} minded person who enjoys {', '.join(chosen[:3])}.",
        location=location,
        preferred_location=location,
        min_age=18,
        max_age=40,
        relationship_goal=goal,
        occupation=(fake.job() if fake else SEED_OCCUPATIONS[(index * 2) % len(SEED_OCCUPATIONS)]),
        education=SEED_EDUCATION[(index * 4) % len(SEED_EDUCATION)],
    )
    for interest in chosen:
        profile.interests.append(get_or_create_interest(interest))
    db.session.add(profile)
    return user


def ensure_seeded_users_for(viewer, total=50):
    """Create a realistic pool of database users and pre-like the logged-in user from some of them.
    This keeps Browse data database-driven while making the demo easy to test: when the user likes
    a pre-liked profile, a mutual match is created and appears in Matches.
    """
    created_any = False
    seed_users = []
    for i in range(1, total + 1):
        seed_user = create_seed_profile(i)
        seed_users.append(seed_user)
        created_any = True

    # Make a healthy number of seeded users already like the logged-in user.
    # The match is still only created when the logged-in user likes them back.
    if viewer:
        for seed_user in seed_users[:25]:
            if seed_user.id == viewer.id:
                continue
            existing = Like.query.filter_by(liker_id=seed_user.id, liked_id=viewer.id).first()
            if not existing:
                db.session.add(Like(liker_id=seed_user.id, liked_id=viewer.id, action="like"))
                created_any = True
    if created_any:
        db.session.commit()


@app.route("/")
def index():
    return jsonify(message="DriftDater API is running")


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    interests = clean_interests(data.get("interests", []))

    required = [email, username, password, data.get("firstName"), data.get("lastName"), data.get("dob"), data.get("gender"), data.get("lookingFor"), data.get("bio"), data.get("location")]
    if not all(required):
        return jsonify({"error": "Missing required registration fields"}), 400
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return jsonify({"error": "Please enter a valid email address"}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400
    if len(interests) < 3:
        return jsonify({"error": "Please choose at least 3 interests"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    try:
        age = calculate_age(data.get("dob"))
    except ValueError:
        return jsonify({"error": "Invalid date format for dob. Use YYYY-MM-DD."}), 400
    if age < 18:
        return jsonify({"error": "Users must be 18 or older"}), 400

    user = User(
        email=email,
        username=username,
        password_hash=bcrypt.generate_password_hash(password).decode("utf-8"),
        is_private=bool(data.get("isPrivate", False)),
        is_premium=bool(data.get("isPremium", False)),
        is_verified=bool(data.get("isVerified", False)),
    )
    db.session.add(user)
    db.session.flush()

    profile = Profile(
        user_id=user.id,
        first_name=data.get("firstName").strip(),
        last_name=data.get("lastName").strip(),
        age=age,
        gender=data.get("gender"),
        looking_for=data.get("lookingFor"),
        bio=data.get("bio").strip(),
        location=data.get("location").strip(),
        preferred_location=(data.get("preferredLocation") or data.get("location") or "").strip(),
        min_age=int(data.get("minAge") or 18),
        max_age=int(data.get("maxAge") or 99),
        relationship_goal=data.get("relationshipGoal") or "Friendship",
        occupation=data.get("occupation") or "",
        education=data.get("education") or "",
    )
    for interest_name in interests:
        profile.interests.append(get_or_create_interest(interest_name))
    db.session.add(profile)
    db.session.commit()

    session["user_id"] = user.id
    return jsonify({"message": "Registration successful", "user": user_to_dict(user)}), 201


@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401
    session["user_id"] = user.id
    return jsonify({"message": "Login successful", "user": user_to_dict(user)}), 200


@app.route("/api/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200


@app.route("/api/auth/me")
def me():
    user = current_user()
    if not user:
        return jsonify({"user": None}), 200
    return jsonify({"user": user_to_dict(user)}), 200


@app.route("/api/profile", methods=["GET", "PUT"])
@login_required
def my_profile():
    user = current_user()
    if request.method == "GET":
        return jsonify({"profile": profile_to_dict(user.profile, include_private=True)}), 200

    data = request.form.to_dict() if request.form else (request.get_json() or {})
    profile = user.profile
    for key, attr in [
        ("first_name", "first_name"), ("last_name", "last_name"), ("gender", "gender"),
        ("looking_for", "looking_for"), ("bio", "bio"), ("location", "location"),
        ("preferred_location", "preferred_location"), ("relationship_goal", "relationship_goal"),
        ("occupation", "occupation"), ("education", "education"),
    ]:
        if key in data:
            setattr(profile, attr, data.get(key) or "")
    for key, attr in [("min_age", "min_age"), ("max_age", "max_age"), ("age", "age")]:
        if key in data and str(data.get(key)).strip():
            setattr(profile, attr, int(data.get(key)))
    if "is_private" in data:
        user.is_private = str(data.get("is_private")).lower() in ("true", "1", "yes", "on")
    if "is_premium" in data:
        user.is_premium = str(data.get("is_premium")).lower() in ("true", "1", "yes", "on")
    if "is_verified" in data:
        user.is_verified = str(data.get("is_verified")).lower() in ("true", "1", "yes", "on")
    if "interests" in data:
        raw = data.get("interests")
        names = clean_interests(raw.split(",") if isinstance(raw, str) else raw)
        if len(names) < 3:
            return jsonify({"error": "Please keep at least 3 interests"}), 400
        profile.interests.clear()
        for name in names:
            profile.interests.append(get_or_create_interest(name))
    if "profile_picture" in request.files:
        saved = save_profile_picture(request.files["profile_picture"])
        if saved:
            profile.profile_picture = saved
    db.session.commit()
    return jsonify({"message": "Profile updated", "profile": profile_to_dict(profile, include_private=True)}), 200


@app.route("/api/profiles")
@login_required
def browse_profiles():
    user = current_user()
    ensure_seeded_users_for(user, total=50)
    q = (request.args.get("q") or "").lower()
    location = (request.args.get("location") or "").lower()
    interest = normalize_interest(request.args.get("interest") or "")
    min_age = request.args.get("min_age", type=int)
    max_age = request.args.get("max_age", type=int)
    relationship_goal = (request.args.get("relationship_goal") or "").lower()
    gender = (request.args.get("gender") or "").lower()
    verified_only = (request.args.get("verified") or "").lower() in ("1", "true", "yes")
    premium_only = (request.args.get("premium") or "").lower() in ("1", "true", "yes")
    boosted_only = (request.args.get("boosted") or "").lower() in ("1", "true", "yes")
    sort = request.args.get("sort") or "score"

    query = Profile.query.join(User).filter(Profile.user_id != user.id, User.is_private == False)
    if location:
        query = query.filter(Profile.location.ilike(f"%{location}%"))
    if min_age:
        query = query.filter(Profile.age >= min_age)
    if max_age:
        query = query.filter(Profile.age <= max_age)
    if relationship_goal:
        query = query.filter(Profile.relationship_goal.ilike(f"%{relationship_goal}%"))
    if gender:
        query = query.filter(Profile.gender.ilike(gender))
    if verified_only:
        query = query.filter(User.is_verified == True)
    if premium_only:
        query = query.filter(User.is_premium == True)
    if boosted_only:
        query = query.filter(User.boosted_until.isnot(None), User.boosted_until > datetime.utcnow())
    profiles = query.all()
    if q:
        profiles = [p for p in profiles if q in f"{p.first_name} {p.last_name} {p.bio}".lower()]
    if interest:
        profiles = [p for p in profiles if interest in {i.name for i in p.interests}]

    items = [profile_to_dict(p, viewer=user) for p in profiles]
    if sort == "newest":
        items.sort(key=lambda x: x["created_at"] or "", reverse=True)
    elif sort == "age":
        items.sort(key=lambda x: x["age"])
    elif sort == "boosted":
        items.sort(key=lambda x: (x.get("is_boosted", False), x.get("match_score", 0)), reverse=True)
    elif sort == "verified":
        items.sort(key=lambda x: (x.get("is_verified", False), x.get("match_score", 0)), reverse=True)
    else:
        # Premium/boosted profiles get visibility, but normal users are still sorted by compatibility.
        items.sort(key=lambda x: (x.get("is_boosted", False), x.get("is_premium", False), x.get("match_score", 0)), reverse=True)
    return jsonify({"profiles": items}), 200


@app.route("/api/profiles/<int:profile_id>/action", methods=["POST"])
@login_required
def profile_action(profile_id):
    user = current_user()
    target = Profile.query.get_or_404(profile_id)
    if target.user_id == user.id:
        return jsonify({"error": "You cannot act on your own profile"}), 400
    action = (request.get_json() or {}).get("action")
    if action not in {"like", "pass", "dislike"}:
        return jsonify({"error": "Action must be like, pass or dislike"}), 400

    like = Like.query.filter_by(liker_id=user.id, liked_id=target.user_id).first()
    if not like:
        like = Like(liker_id=user.id, liked_id=target.user_id, action=action)
        db.session.add(like)
    else:
        like.action = action

    created_match = None
    if action == "like":
        reciprocal = Like.query.filter_by(liker_id=target.user_id, liked_id=user.id, action="like").first()
        if reciprocal:
            low, high = sorted([user.id, target.user_id])
            created_match = Match.query.filter_by(user1_id=low, user2_id=high).first()
            if not created_match:
                created_match = Match(user1_id=low, user2_id=high)
                db.session.add(created_match)
    db.session.commit()
    return jsonify({"message": f"Profile {action}d", "matched": created_match is not None, "match_id": created_match.id if created_match else None}), 200


@app.route("/api/matches")
@login_required
def get_matches():
    user = current_user()
    matches = Match.query.filter((Match.user1_id == user.id) | (Match.user2_id == user.id)).order_by(Match.created_at.desc()).all()
    items = []
    for match in matches:
        other_id = match.user2_id if match.user1_id == user.id else match.user1_id
        other = User.query.get(other_id)
        last = Message.query.filter_by(match_id=match.id).order_by(Message.created_at.desc()).first()
        items.append({
            "id": match.id,
            "match_id": match.id,
            "created_at": match.created_at.isoformat(),
            "other_user": profile_to_dict(other.profile, viewer=user),
            "last_message": last.body if last else "Start a conversation",
            "last_message_time": last.created_at.isoformat() if last else None,
            "last_sender_id": last.sender_id if last else None,
        })
    return jsonify({"matches": items}), 200


@app.route("/api/messages/<int:match_id>")
@login_required
def get_messages(match_id):
    user = current_user()
    match = Match.query.get_or_404(match_id)
    if user.id not in (match.user1_id, match.user2_id):
        return jsonify({"error": "You are not part of this match"}), 403
    messages = Message.query.filter_by(match_id=match_id).order_by(Message.created_at.asc()).all()
    return jsonify({"messages": [{"id": m.id, "match_id": m.match_id, "sender_id": m.sender_id, "receiver_id": m.receiver_id, "body": m.body, "created_at": m.created_at.isoformat()} for m in messages]}), 200


@app.route("/api/messages", methods=["POST"])
@login_required
def send_message():
    user = current_user()
    data = request.get_json() or {}
    match = Match.query.get_or_404(data.get("match_id"))
    if user.id not in (match.user1_id, match.user2_id):
        return jsonify({"error": "You are not part of this match"}), 403
    body = (data.get("body") or "").strip()
    if not body:
        return jsonify({"error": "Message cannot be empty"}), 400
    receiver_id = match.user2_id if match.user1_id == user.id else match.user1_id
    receiver = User.query.get(receiver_id)

    message = Message(match_id=match.id, sender_id=user.id, receiver_id=receiver_id, body=body)
    db.session.add(message)
    db.session.flush()

    auto_reply = None
    if should_auto_reply(receiver):
        reply_text = get_auto_reply(body)
        auto_reply = Message(match_id=match.id, sender_id=receiver_id, receiver_id=user.id, body=reply_text)
        db.session.add(auto_reply)
        db.session.flush()

    db.session.commit()

    def serialize(m):
        return {
            "id": m.id,
            "match_id": m.match_id,
            "sender_id": m.sender_id,
            "receiver_id": m.receiver_id,
            "body": m.body,
            "created_at": m.created_at.isoformat(),
        }

    response = {"message": serialize(message)}
    if auto_reply:
        response["auto_reply"] = serialize(auto_reply)
    return jsonify(response), 201


@app.route("/api/profile/boost", methods=["POST"])
@login_required
def boost_profile():
    user = current_user()
    if not user.is_premium:
        return jsonify({"error": "Boost Profile is a premium feature. Turn on Premium in your profile first."}), 403
    user.boosted_until = datetime.utcnow() + timedelta(hours=24)
    db.session.commit()
    return jsonify({"message": "Profile boosted for 24 hours", "user": user_to_dict(user)}), 200


@app.route("/api/favorites", methods=["GET"])
@login_required
def list_favorites():
    user = current_user()
    favs = Favorite.query.filter_by(user_id=user.id).order_by(Favorite.created_at.desc()).all()
    return jsonify({"favorites": [profile_to_dict(Profile.query.get(f.profile_id), viewer=user) for f in favs]}), 200


@app.route("/api/profiles/<int:profile_id>/favorite", methods=["POST", "DELETE"])
@login_required
def favorite(profile_id):
    user = current_user()
    profile = Profile.query.get_or_404(profile_id)
    fav = Favorite.query.filter_by(user_id=user.id, profile_id=profile.id).first()
    if request.method == "DELETE":
        if fav:
            db.session.delete(fav)
            db.session.commit()
        return jsonify({"message": "Favorite removed"}), 200
    if not fav:
        db.session.add(Favorite(user_id=user.id, profile_id=profile.id))
        db.session.commit()
    return jsonify({"message": "Favorite saved"}), 201


@app.route("/api/interests")
def list_interests():
    return jsonify({"interests": [i.name for i in Interest.query.order_by(Interest.name.asc()).all()]}), 200



@app.cli.command("seed-users")
def seed_users_command():
    """Seed the database with 50 realistic DriftDater profiles."""
    ensure_seeded_users_for(None, total=50)
    print("Seeded 50 DriftDater demo users. Demo password: password123")


@app.after_request
def add_header(response):
    response.headers["X-UA-Compatible"] = "IE=Edge,chrome=1"
    response.headers["Cache-Control"] = "public, max-age=0"
    return response
