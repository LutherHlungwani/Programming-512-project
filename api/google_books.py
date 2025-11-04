import requests

def fetch_book_by_isbn(isbn):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('totalItems', 0) > 0:
                book_info = data['items'][0]['volumeInfo']
                published = book_info.get('publishedDate', '')

                return {
                    'title': book_info.get('title', ''),
                    'author': ', '.join(book_info.get('authors', [])),
                    'publisher': book_info.get('publisher', ''),
                    'publication_year': int(published[:4]) if published and published[:4].isdigit() else None,
                    'description': book_info.get('description', ''),
                    'page_count': book_info.get('pageCount', 0),
                    'language': book_info.get('language', 'en'),
                    'cover_image_url': book_info.get('imageLinks', {}).get('thumbnail', ''),
                    'category': ', '.join(book_info.get('categories', []))
                }
    except Exception as e:
        print(f"Google Books API error: {e}")
    return None
