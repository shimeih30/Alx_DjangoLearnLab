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
    book1 = Book.objects.create(title="Harry Potter", author=author1)
    book2 = Book.objects.create(title="A Game of Thrones", author=author2)
    
    # Create libraries
    central_library = Library.objects.create(name="Central Library")
    central_library.books.add(book1, book2)
    
    branch_library = Library.objects.create(name="Branch Library")
    branch_library.books.add(book1)
    
    # Assign librarians
    Librarian.objects.create(name="Ms. Smith", library=central_library)
    Librarian.objects.create(name="Mr. Johnson", library=branch_library)
    
    return author1, central_library

def run_queries():
    author, library = create_sample_data()
    
    print("\n1. All books by a specific author:")
    books_by_author = Book.objects.filter(author=author)
    for book in books_by_author:
        print(f"- {book.title}")
    
    print("\n2. All books in a library (using library instance):")
    books_in_library = library.books.all()
    for book in books_in_library:
        print(f"- {book.title}")
    
    print("\n3. Get library by name:")
    library_name = "Central Library"
    try:
        library_by_name = Library.objects.get(name=library_name)
        print(f"- Found library: {library_by_name}")
        print("  Books in this library:")
        for book in library_by_name.books.all():
            print(f"  - {book.title}")
    except Library.DoesNotExist:
        print(f"- Library named '{library_name}' not found")
    
    print("\n4. Librarian for a library:")
    try:
        librarian = Librarian.objects.get(library=library)
        print(f"- {librarian.name}")
    except Librarian.DoesNotExist:
        print("- No librarian assigned to this library")

if __name__ == "__main__":
    run_queries()
    
def check_required_queries():
    # Create or get test data
    author = Author.objects.create(name="Test Author")
    book1 = Book.objects.create(title="Test Book 1", author=author)
    book2 = Book.objects.create(title="Test Book 2", author=author)
    
    library = Library.objects.create(name="Test Library")
    library.books.add(book1)
    
    librarian = Librarian.objects.create(name="Test Librarian", library=library)
    
    # 1. Query all books by a specific author
    print("\n=== Checking: Query all books by a specific author ===")
    books = author.books.all()
    assert len(books) == 2
    print("✓ Found books by author:")
    for book in books:
        print(f"- {book.title}")
    
    # 2. Retrieve the librarian for a library
    print("\n=== Checking: Retrieve the librarian for a library ===")
    try:
        lib_librarian = library.librarian
        print(f"✓ Librarian found: {lib_librarian.name}")
    except Librarian.DoesNotExist:
        print("✗ No librarian found for this library")
    
    return books, lib_librarian