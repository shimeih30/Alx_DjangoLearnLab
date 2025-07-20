import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    # Clear existing data
    Author.objects.all().delete()
    Book.objects.all().delete()
    Library.objects.all().delete()
    Librarian.objects.all().delete()
    
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George R.R. Martin")
    
    # Create books
    Book.objects.create(title="Harry Potter", author=author1)
    Book.objects.create(title="The Chamber of Secrets", author=author1)
    Book.objects.create(title="A Game of Thrones", author=author2)
    
    # Create libraries
    central_library = Library.objects.create(name="Central Library")
    central_library.books.set(Book.objects.all())
    
    branch_library = Library.objects.create(name="Branch Library")
    branch_library.books.set(Book.objects.filter(author=author1))
    
    # Assign librarians
    Librarian.objects.create(name="Ms. Smith", library=central_library)
    Librarian.objects.create(name="Mr. Johnson", library=branch_library)
    
    return author1, central_library

def run_queries():
    print("=== Creating Sample Data ===")
    author, library = create_sample_data()
    
    print("\n=== 1. Query all books by a specific author ===")
    author_name = "J.K. Rowling"
    try:
        author = Author.objects.get(name=author_name)
        books_by_author = author.books.all()
        print(f"Books by {author_name}:")
        for book in books_by_author:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found")
    
    print("\n=== 2. List all books in a library ===")
    library_name = "Central Library"
    try:
        library = Library.objects.get(name=library_name)
        print(f"Books in {library_name}:")
        for book in library.books.all():
            print(f"- {book.title} (by {book.author.name})")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found")
    
    print("\n=== 3. Retrieve the librarian for a library ===")
    try:
        librarian = library.librarian
        print(f"Librarian for {library.name}: {librarian.name}")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to {library.name}")
    
    print("\n=== 4. Additional Query: Get author by name ===")
    author_name = "George R.R. Martin"
    try:
        author = Author.objects.get(name=author_name)
        print(f"Found author: {author.name}")
        print(f"Number of books: {author.books.count()}")
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found")

if __name__ == "__main__":
    run_queries()