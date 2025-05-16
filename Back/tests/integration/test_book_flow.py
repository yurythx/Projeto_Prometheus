"""
Testes de integração para o fluxo de livros
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from apps.books.models import Book, Chapter
from apps.categories.models import Category
import json

User = get_user_model()


class BookFlowTestCase(TestCase):
    """
    Testes de integração para o fluxo de livros
    """
    def setUp(self):
        """
        Configuração inicial para os testes
        """
        self.client = Client()

        # Desativar o Django Axes para os testes
        from django.test.utils import override_settings
        self._override = override_settings(
            AXES_ENABLED=False,
        )
        self._override.enable()

        # Criar um usuário para os testes
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

        # Criar um usuário admin para os testes
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )

        # Criar uma categoria para os testes
        self.category = Category.objects.create(
            name='Categoria de Teste',
            description='Descrição da categoria de teste'
        )

        # Criar alguns livros para os testes
        self.book1 = Book.objects.create(
            title='Livro 1',
            description='Descrição do livro 1',
            has_audio=True,
            category=self.category
        )

        self.book2 = Book.objects.create(
            title='Livro 2',
            description='Descrição do livro 2',
            has_audio=False,
            category=self.category
        )

        # Criar alguns capítulos para os testes
        self.chapter1 = Chapter.objects.create(
            book=self.book1,
            title='Capítulo 1',
            content='Conteúdo do capítulo 1',
            order=1
        )

        self.chapter2 = Chapter.objects.create(
            book=self.book1,
            title='Capítulo 2',
            content='Conteúdo do capítulo 2',
            order=2
        )

    def test_list_books(self):
        """
        Testa a listagem de livros
        """
        url = '/api/v1/books/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['count'], 2)
        self.assertEqual(len(data['results']), 2)

    def test_get_book_detail(self):
        """
        Testa a obtenção de detalhes de um livro
        """
        url = f'/api/v1/books/{self.book1.slug}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], 'Livro 1')
        self.assertEqual(data['description'], 'Descrição do livro 1')
        self.assertTrue(data['has_audio'])

    def test_create_book(self):
        """
        Testa a criação de um livro
        """
        # Fazer login como admin
        self.client.force_login(self.admin)

        url = '/api/v1/books/'
        data = {
            'title': 'Novo Livro',
            'description': 'Descrição do novo livro',
            'has_audio': True,
            'category': self.category.id
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['title'], 'Novo Livro')
        self.assertEqual(data['description'], 'Descrição do novo livro')
        self.assertTrue(data['has_audio'])

        # Verificar se o livro foi realmente criado no banco de dados
        self.assertTrue(Book.objects.filter(title='Novo Livro').exists())

    def test_update_book(self):
        """
        Testa a atualização de um livro
        """
        # Fazer login como admin
        self.client.force_login(self.admin)

        url = f'/api/v1/books/{self.book1.slug}/'
        data = {
            'title': 'Livro 1 Atualizado',
            'description': 'Descrição atualizada',
            'has_audio': False
        }
        response = self.client.patch(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], 'Livro 1 Atualizado')
        self.assertEqual(data['description'], 'Descrição atualizada')
        self.assertFalse(data['has_audio'])

        # Verificar se o livro foi realmente atualizado no banco de dados
        book = Book.objects.get(id=self.book1.id)
        self.assertEqual(book.title, 'Livro 1 Atualizado')
        self.assertEqual(book.description, 'Descrição atualizada')
        self.assertFalse(book.has_audio)

    def test_delete_book(self):
        """
        Testa a exclusão de um livro
        """
        # Fazer login como admin
        self.client.force_login(self.admin)

        url = f'/api/v1/books/{self.book1.slug}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        # Verificar se o livro foi realmente excluído do banco de dados
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    def test_list_chapters(self):
        """
        Testa a listagem de capítulos de um livro
        """
        url = f'/api/v1/books/{self.book1.slug}/chapters/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['title'], 'Capítulo 1')
        self.assertEqual(data[1]['title'], 'Capítulo 2')

    def test_get_chapter_detail(self):
        """
        Testa a obtenção de detalhes de um capítulo
        """
        url = f'/api/v1/books/{self.book1.slug}/chapters/{self.chapter1.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], 'Capítulo 1')
        self.assertEqual(data['content'], 'Conteúdo do capítulo 1')
        self.assertEqual(data['order'], 1)

    def test_create_chapter(self):
        """
        Testa a criação de um capítulo
        """
        # Fazer login como admin
        self.client.force_login(self.admin)

        url = f'/api/v1/books/{self.book1.slug}/chapters/'
        data = {
            'title': 'Novo Capítulo',
            'content': 'Conteúdo do novo capítulo',
            'order': 3
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['title'], 'Novo Capítulo')
        self.assertEqual(data['content'], 'Conteúdo do novo capítulo')
        self.assertEqual(data['order'], 3)

        # Verificar se o capítulo foi realmente criado no banco de dados
        self.assertTrue(Chapter.objects.filter(title='Novo Capítulo').exists())

    def test_update_chapter(self):
        """
        Testa a atualização de um capítulo
        """
        # Fazer login como admin
        self.client.force_login(self.admin)

        url = f'/api/v1/books/{self.book1.slug}/chapters/{self.chapter1.id}/'
        data = {
            'title': 'Capítulo 1 Atualizado',
            'content': 'Conteúdo atualizado',
            'order': 1
        }
        response = self.client.patch(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], 'Capítulo 1 Atualizado')
        self.assertEqual(data['content'], 'Conteúdo atualizado')
        self.assertEqual(data['order'], 1)

        # Verificar se o capítulo foi realmente atualizado no banco de dados
        chapter = Chapter.objects.get(id=self.chapter1.id)
        self.assertEqual(chapter.title, 'Capítulo 1 Atualizado')
        self.assertEqual(chapter.content, 'Conteúdo atualizado')
        self.assertEqual(chapter.order, 1)

    def test_delete_chapter(self):
        """
        Testa a exclusão de um capítulo
        """
        # Fazer login como admin
        self.client.force_login(self.admin)

        url = f'/api/v1/books/{self.book1.slug}/chapters/{self.chapter1.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        # Verificar se o capítulo foi realmente excluído do banco de dados
        self.assertFalse(Chapter.objects.filter(id=self.chapter1.id).exists())
