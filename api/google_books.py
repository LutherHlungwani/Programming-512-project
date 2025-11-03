import requests



def fetch_book_by_isbn(isbn):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"


    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('totalItems', 0) > 0:
                book_info = data['items'][0]['volumeInfo']
                return {
                    'title': book_info.get('title', ''),
                    'author': ', '.join(book_info.get('authors', [])),
                    'publisher': book_info.get('publisher', ''),
                    'publication_year': int(book_info['publishedDate'][:4]) if 'publishedDate' in book_info and
                                                                               book_info['publishedDate'] else None,
                    'description': book_info.get('description', ''),
                    'page_count': book_info.get('pageCount', 0),
                    'language': book_info.get('language', 'en'),
                    'cover_image_url': book_info.get('imageLinks', {}).get('thumbnail', ''),
                    'category': ', '.join(book_info.get('categories', []))
                }
    except Exception as e:
        print(f"Google Books API error: {e}")
    return None