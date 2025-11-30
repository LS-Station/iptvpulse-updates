import requests
import json
import sys

# Arguments: domain, post limit
if len(sys.argv) < 3:
    print("Usage: python3 blogger.py <blog_url> <limit>")
    sys.exit(1)

BLOG_URL = sys.argv[1].rstrip("/")
LIMIT = int(sys.argv[2])

# Blogger JSON feed URL
FEED_URL = f"{BLOG_URL}/feeds/posts/default?alt=json&max-results={LIMIT}"

def fetch_posts():
    print("Fetching JSON feed...")
    r = requests.get(FEED_URL)

    if r.status_code != 200:
        print("Failed to fetch Blogger feed:", r.status_code)
        sys.exit(1)

    return r.json()

def extract_posts(data):
    entries = data.get("feed", {}).get("entry", [])
    posts = []

    for entry in entries:
        title = entry.get("title", {}).get("$t", "No Title")

        # Post link
        link = next((l["href"] for l in entry.get("link", []) if l.get("rel") == "alternate"), "#")

        # Thumbnail if exists
        media = entry.get("media$thumbnail", {})
        image = media.get("url", "")

        posts.append({
            "title": title,
            "link": link,
            "image": image
        })

    return posts

def update_readme(posts):
    print("Updating README.md ...")

    content = "# 📺 Latest IPTV Updates\n\n"

    for p in posts:
        content += f"### {p['title']}\n"
        if p['image']:
            content += f"![Thumbnail]({p['image']})\n\n"
        content += f"🔗 **Playlist Link:** [{p['title']}]({p['link']})\n\n---\n\n"

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

    print("README.md updated successfully!")

# Run workflow
data = fetch_posts()
posts = extract_posts(data)
update_readme(posts)
