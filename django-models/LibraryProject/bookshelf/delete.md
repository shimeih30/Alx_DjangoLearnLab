from bookshelf.models import Book"<pre> ```python book = Book.objects.get(title="Nineteen Eighty-Four") book.delete() # (1, {'bookshelf.Book': 1}) Book.objects.all() # <QuerySet []> ``` </pre>
