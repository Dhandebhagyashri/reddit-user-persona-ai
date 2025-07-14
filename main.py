import praw
import openai
import os
import sys

# Replace with your OpenAI API key
openai.api_key = "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"

# Replace with your Reddit API credentials
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
    prompt = f"""
You are an AI assistant tasked with creating a detailed user persona based on the following Reddit posts and comments.
Highlight key traits such as interests, tone, personality, possible profession, values, and political leaning.

Make sure to cite one post or comment under each trait.

--- START DATA ---
POSTS:
{''.join(posts)}

COMMENTS:
{''.join(comments)}
--- END DATA ---

Now create the user persona:
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=800
    )
    return response["choices"][0]["message"]["content"]

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
