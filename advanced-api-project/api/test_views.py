from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book, Author


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user and authenticate
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = APIClient()

        # Create test authors and books
        self.author = Author.objects.create(name="Chinua Achebe")
        self.book1 = Book.objects.create(title="Things Fall Apart", publication_year=1958, author=self.author)
        self.book2 = Book.objects.create(title="No Longer at Ease", publication_year=1960, author=self.author)

        self.create_url = '/api/books/create/'
        self.list_url = '/api/books/'
        self.detail_url = f'/api/books/{self.book1.pk}/'
        self.update_url = f'/api/books/{self.book1.pk}/update/'
        self.delete_url = f'/api/books/{self.book1.pk}/delete/'

    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_create_book_unauthenticated(self):
        data = {
            'title': 'Arrow of God',
            'publication_year': 1964,
            'author': self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='password123')
        data = {
            'title': 'Arrow of God',
            'publication_year': 1964,
            'author': self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Arrow of God')

    def test_update_book_authenticated(self):
        self.client.login(username='testuser', password='password123')
        data = {
            'title': 'Things Fall Apart - Updated',
            'publication_year': 1959,
            'author': self.author.id
        }
        response = self.client.patch(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Things Fall Apart - Updated')

    def test_delete_book_authenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())

    def test_filter_books_by_year(self):
        response = self.client.get(self.list_url + '?publication_year=1958')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books_by_title(self):
        response = self.client.get(self.list_url + '?search=No')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'No Longer at Ease')

    def test_order_books_by_title_desc(self):
        response = self.client.get(self.list_url + '?ordering=-title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))
