import praw
import os
import sys

# ✅ Your Reddit API credentials
reddit = praw.Reddit(
    client_id="GXJhpA0-iLr2YEOmxY7OSg",
    client_secret="bLCqop5UhpGM1xubZanvNJ2lHkfQ_g",
    user_agent="PersonaScript123"
)

def extract_username(url):
    return url.strip("/").split("/")[-1]

def fetch_user_data(username):
    user = reddit.redditor(username)
    posts = []
    comments = []

    for submission in user.submissions.new(limit=20):
        posts.append(f"Title: {submission.title}\nText: {submission.selftext}\n")

    for comment in user.comments.new(limit=20):
        comments.append(f"Comment: {comment.body}\n")

    return posts, comments

def generate_persona(posts, comments):
    text = " ".join(posts + comments).lower()
    persona = []

    if any(word in text for word in ["python", "code", "developer", "programming"]):
        persona.append("💻 Interest: Programming")

    if any(word in text for word in ["ai", "chatgpt", "machine learning", "model"]):
        persona.append("🤖 Interest: Artificial Intelligence")

    if any(word in text for word in ["game", "steam", "xbox", "playstation", "fps"]):
        persona.append("🎮 Interest: Gaming")

    if any(word in text for word in ["help", "thanks", "appreciate", "kind"]):
        persona.append("🧠 Personality: Helpful and polite")

    if any(word in text for word in ["funny", "lol", "haha"]):
        persona.append("😄 Personality: Humorous")

    if not persona:
        persona.append("🧐 Not enough data to create a detailed persona.")

    return "\n".join(persona)

def save_persona(username, persona_text):
    output_path = f"personas/{username}.txt"
    os.makedirs("personas", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(persona_text)
    print(f"✅ Persona saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("⚠️  Please provide a Reddit profile URL.")
        sys.exit(1)

    profile_url = sys.argv[1]
    username = extract_username(profile_url)

    print(f"🔍 Extracting data for: {username}...")

    posts, comments = fetch_user_data(username)
    persona = generate_persona(posts, comments)
    save_persona(username, persona)
