"""
Standalone test for fetching a book cover from the Google Books API.
No API key, no Discord, no project dependencies needed — just run it directly:

    python test_google_cover.py
"""

import requests


def get_google_cover(title: str):
    """
    Looks up a book by title on Google Books and returns a cover image URL,
    or None if nothing was found / no cover is available.
    """
    response = requests.get(
        "https://www.googleapis.com/books/v1/volumes",
        params={"q": title, "maxResults": 1},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    items = data.get("items", [])
    if not items:
        print(f"No results found for '{title}'")
        return None

    volume_info = items[0]["volumeInfo"]
    image_links = volume_info.get("imageLinks", {})
    url = image_links.get("thumbnail") or image_links.get("smallThumbnail")

    if not url:
        print(f"'{volume_info.get('title', title)}' found, but it has no cover image")
        return None

    return url.replace("http://", "https://")


def download_cover(url: str, path: str = "cover.jpg"):
    """
    Downloads the cover image to disk, so you can open it and eyeball it.
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    with open(path, "wb") as f:
        f.write(response.content)
    print(f"Saved cover to {path}")


if __name__ == "__main__":
    test_titles = [
        "Harry Potter and the Philosopher's Stone",
        "1984",
        "asdkjaslkdjalskdjqwe",  # deliberately bogus title, should print "no results"
    ]

    for title in test_titles:
        print(f"\nSearching: {title}")
        cover_url = get_google_cover(title)
        if cover_url:
            print(f"Cover URL: {cover_url}")
            download_cover(cover_url, path=f"{title[:20].strip()}.jpg")