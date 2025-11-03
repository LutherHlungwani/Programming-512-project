from datetime import datetime

def calculate_fine(due_date_str, return_date_str=None):
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    if return_date_str:
        return_date = datetime.strptime(return_date_str, "%Y-%m-%d").date()
    else:
        from datetime import date
        return_date = date.today()

    if return_date > due_date:
        days_overdue = (return_date - due_date).days
        fine = days_overdue * 0.50  # Use config value if needed
        return round(fine, 2)
    return 0.0

def format_date(date_obj):
    if isinstance(date_obj, str):
        return datetime.strptime(date_obj, "%Y-%m-%d").strftime("%B %d, %Y")
    return date_obj.strftime("%B %d, %Y")

def is_valid_isbn(isbn):
    isbn = isbn.replace("-", "").replace(" ", "")
    if len(isbn) == 10:
        return isbn.isdigit()
    elif len(isbn) == 13:
        return isbn.isdigit()
    return False