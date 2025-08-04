from django.db import models

# Author model stores basic author information
class Author(models.Model):
    name = models.CharField(max_length=100)  # Author's full name

    def __str__(self):
        return self.name

# Book model represents a book written by an author
class Book(models.Model):
    title = models.CharField(max_length=200)  # Title of the book
    publication_year = models.PositiveIntegerField()  # Year of publication
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    # One author can write many books

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
