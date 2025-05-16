"""
Testes para o serviço de livros
"""

import unittest
from unittest.mock import MagicMock, patch
from django.test import RequestFactory
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from apps.books.models import Book
from apps.categories.models import Category


class TestBooksService(unittest.TestCase):
    """
    Testes para o serviço de livros
    """

    def setUp(self):
        """
        Configuração inicial para os testes
        """
        self.client = APIClient()
        self.factory = RequestFactory()
        
        # Desativar o Django Axes para os testes
        from django.test.utils import override_settings
        self._override = override_settings(
            AXES_ENABLED=False,
        )
        self._override.enable()
        
        # Criar um usuário para os testes
        User = get_user_model()
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

    def test_list_books(self):
        """
        Testa a listagem de livros
        """
        url = '/api/v1/books/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se a resposta contém os livros criados
        data = response.json()
        self.assertEqual(data['count'], 2)
        self.assertEqual(len(data['results']), 2)
        
        # Verificar os dados do primeiro livro
        book1_data = next(item for item in data['results'] if item['title'] == 'Livro 1')
        self.assertEqual(book1_data['description'], 'Descrição do livro 1')
        self.assertTrue(book1_data['has_audio'])
        
        # Verificar os dados do segundo livro
        book2_data = next(item for item in data['results'] if item['title'] == 'Livro 2')
        self.assertEqual(book2_data['description'], 'Descrição do livro 2')
        self.assertFalse(book2_data['has_audio'])

    def test_get_book_detail(self):
        """
        Testa a obtenção de detalhes de um livro
        """
        url = f'/api/v1/books/{self.book1.slug}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar os dados do livro
        data = response.json()
        self.assertEqual(data['title'], 'Livro 1')
        self.assertEqual(data['description'], 'Descrição do livro 1')
        self.assertTrue(data['has_audio'])
        self.assertEqual(data['category'], self.category.id)

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
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar os dados do livro criado
        data = response.json()
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
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar os dados do livro atualizado
        data = response.json()
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
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verificar se o livro foi realmente excluído do banco de dados
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())


if __name__ == '__main__':
    unittest.main()
