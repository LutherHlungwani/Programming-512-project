import requests


def fetch_book_by_isbn_openlib(isbn):
    url = f"https://openlibrary.org/isbn/{isbn}.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Get author info from author key if available
            author_key = data.get('authors', [{}])[0].get('key', '')
            author_name = ''
            if author_key:
                author_response = requests.get(f"https://openlibrary.org{author_key}.json")
                if author_response.status_code == 200:
                    author_data = author_response.json()
                    author_name = author_data.get('name', '')

            return {
                'title': data.get('title', ''),
                'author': author_name,
                'publisher': ', '.join(data.get('publishers', [])),
                'publication_year': int(data.get('publish_date', '')[-4:]) if data.get('publish_date') and data[
                                                                                                               'publish_date'][
                                                                                                           -4:].isdigit() else None,
                'description': data.get('description', ''),
                'page_count': data.get('number_of_pages', 0),
                'language': data.get('languages', [{}])[0].get('key', 'en').split('/')[-1] if data.get(
                    'languages') else 'en',
                'cover_image_url': f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg",
                'category': ', '.join(data.get('subjects', []))
            }
    except Exception as e:
        print(f"Open Library API error: {e}")
    return None