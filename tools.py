from langchain_core.tools import tool
import requests


@tool
def author_call(name: str)->str:

    """
    Search Open Library for information about a specific author.
    Use this tool whenever the user asks about an author.
    Args:
        name: The name of the author to search for.
    Returns:
        A dictionary containing information about the first matching author,
        including their full name, birth date, death date, most famous work,
        number of works, average rating, number of ratings, and up to three
        of their top subjects.
        If a field is unavailable, its value will be "Unknown".
        If no subjects are available, the "Top subjects" list may be empty.
        If the output of the function equals False, respond naturally, appologyze and ask to try later.
    """
    try:
        print("AUTHOR TOOL CALLED")
        request = requests.get(
            "https://openlibrary.org/search/authors.json",#modifyed
            params={
                "q": name,
                "limit": 1
            }
        ).json()
        author = request["docs"][0]
        subjects = []
        for index in range(3):
            subjects.append(author.get("top_subjects", "Not given")[index])
        return {
            "Full name": author.get("name", "Unknown"),
            "Birth date": author.get("birth_date", "Unknown"),
            "Death date": author.get("death_date", "Unknown"),
            "Most famous work": author.get("top_work", "Unknown"),
            "Number of works": author.get("work_count", "Unknown"),
            "Average rating": author.get("ratings_average", "Unknown"),
            "Number of ratings": author.get("ratings_count", "Unknown"),
            "Top subjects": subjects 
            }
    except:
        return False

@tool
def book_call(name: str) -> dict:
    """
    Search Open Library for information about a specific book.
    Use this tool whenever the user asks about a book title.
    Args:
        name: The title of the book to search for.
    Returns:
        A dictionary containing information about the first matching book,
        including the title, author, first publication year, number of pages,
        edition count, average rating, and number of ratings.
        If a field is unavailable, its value will be "Unknown".
        If the output of the function equals False, respond naturally, appologyze and ask to try later
    """
    try:
        print("BOOK TOOL CALLED")


        response = requests.get(
                "https://openlibrary.org/search.json",
                params={
                    "title": name,
                    "limit": 1
                }
                ).json()

        book = response["docs"][0]

        return {
        "Title": book.get("title", "Unknown"),
        "Author": book.get("author_name", ["Unknown"])[0],
        "First published": book.get("first_publish_year", "Unknown"),
        "Pages": book.get("number_of_pages_median", "Unknown"),
        "Number of editions": book.get("edition_count", "Unknown"),
        "Average rating": book.get("ratings_average", "Unknown"),
        "Number of ratings": book.get("ratings_count", "Unknown"),
        }
    except:
        return False
@tool
def subject_call(name: str)->str:
    
    """
    Search Open Library for books related to a specific subject.
    Use this tool whenever the user asks for books from a particular subject
    or genre (e.g. fantasy, history, science fiction, mystery).
    Args:
        name: The subject or genre to search for.
    Returns:
        A list containing up to five books that match the requested subject.
        Each entry contains information returned by the Open Library API.
        If no books are found, an empty list is returned.
        If the output of the function equals False, respond naturally, appologyze and ask to try later
    """
    try:
        print("SUBJECT TOOL CALLED")
        request = requests.get(
                        "https://openlibrary.org/search.json",
                        params={
                            "subject": "fantasy",
                            "limit": 5
                        }
                    ).json()
        subjects = request["docs"]
        output = []
        for subject in subjects:
            output.append(subject)
        return output
    except:
        return False
