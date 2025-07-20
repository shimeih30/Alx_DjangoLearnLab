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
    
import os
import django
from django.core.exceptions import ObjectDoesNotExist

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    """Create test data for all models"""
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
    central = Library.objects.create(name="Central Library")
    central.books.set(Book.objects.all())
    
    branch = Library.objects.create(name="Branch Library")
    branch.books.set(Book.objects.filter(author=author1))
    
    # Assign librarians
    Librarian.objects.create(name="Ms. Smith", library=central)
    Librarian.objects.create(name="Mr. Johnson", library=branch)
    
    return author1, central

def run_queries():
    """Execute and demonstrate all required queries"""
    print("=== Creating Sample Data ===")
    author, library = create_sample_data()
    
    # 1. Query all books by a specific author using filter()
    print("\n=== 1. Books by author using filter() ===")
    books_filter = Book.objects.filter(author=author)
    print(f"Books by {author.name} (using filter):")
    for book in books_filter:
        print(f"- {book.title}")
    
    # 2. Same query using related_name
    print("\n=== 2. Books by author using related_name ===")
    books_related = author.books.all()
    print(f"Books by {author.name} (using related_name):")
    for book in books_related:
        print(f"- {book.title}")
    
    # 3. List all books in a library
    print("\n=== 3. Books in library ===")
    library_books = library.books.all()
    print(f"Books in {library.name}:")
    for book in library_books:
        print(f"- {book.title} by {book.author.name}")
    
    # 4. Retrieve librarian for a library
    print("\n=== 4. Librarian for library ===")
    try:
        librarian = library.librarian
        print(f"Librarian for {library.name}: {librarian.name}")
    except ObjectDoesNotExist:
        print(f"No librarian for {library.name}")
    
    # 5. Get author by name
    print("\n=== 5. Get author by name ===")
    try:
        found_author = Author.objects.get(name="George R.R. Martin")
        print(f"Found author: {found_author.name}")
    except ObjectDoesNotExist:
        print("Author not found")

if __name__ == "__main__":
    run_queries()
    
import os
import django
from django.core.exceptions import ObjectDoesNotExist

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    """Create test data for all models"""
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
    central = Library.objects.create(name="Central Library")
    central.books.set(Book.objects.all())
    
    branch = Library.objects.create(name="Branch Library")
    branch.books.set(Book.objects.filter(author=author1))
    
    # Assign librarians
    Librarian.objects.create(name="Ms. Smith", library=central)
    Librarian.objects.create(name="Mr. Johnson", library=branch)
    
    return central, branch

def run_queries():
    """Execute and demonstrate all required queries"""
    print("=== Creating Sample Data ===")
    central_lib, branch_lib = create_sample_data()
    
    # 1. Query all books by a specific author
    print("\n=== 1. Books by J.K. Rowling ===")
    try:
        author = Author.objects.get(name="J.K. Rowling")
        books = Book.objects.filter(author=author)
        for book in books:
            print(f"- {book.title}")
    except ObjectDoesNotExist:
        print("Author not found")
    
    # 2. List all books in a library
    print("\n=== 2. Books in Central Library ===")
    books = central_lib.books.all()
    for book in books:
        print(f"- {book.title} by {book.author.name}")
    
    # 3. Retrieve librarian for a library (using both methods)
    print("\n=== 3. Librarian Lookup ===")
    
    # Method 1: Using OneToOne reverse relation
    print("\nMethod 1: Using library.librarian")
    try:
        librarian = central_lib.librarian
        print(f"Central Library librarian: {librarian.name}")
    except ObjectDoesNotExist:
        print("No librarian assigned")
    
    # Method 2: Using Librarian.objects.get()
    print("\nMethod 2: Using Librarian.objects.get(library=...)")
    try:
        librarian = Librarian.objects.get(library=central_lib)
        print(f"Central Library librarian: {librarian.name}")
    except ObjectDoesNotExist:
        print("No librarian found for this library")
    
    # 4. Additional query: Get library by name
    print("\n=== 4. Library by Name ===")
    try:
        library = Library.objects.get(name="Branch Library")
        print(f"Found library: {library.name}")
    except ObjectDoesNotExist:
        print("Library not found")

if __name__ == "__main__":
    run_queries()