"""
Testes de desempenho para a API
"""

import unittest
import time
from django.test import Client
from django.contrib.auth import get_user_model
from apps.articles.models import Article
from apps.books.models import Book
from apps.mangas.models import Manga
from apps.categories.models import Category

User = get_user_model()


class APIPerformanceTestCase(unittest.TestCase):
    """
    Testes de desempenho para a API
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
        
        # Criar alguns artigos para os testes
        for i in range(20):
            Article.objects.create(
                title=f'Artigo {i}',
                content=f'Conteúdo do artigo {i}',
                featured=(i % 5 == 0),
                category=self.category
            )
        
        # Criar alguns livros para os testes
        for i in range(20):
            Book.objects.create(
                title=f'Livro {i}',
                description=f'Descrição do livro {i}',
                has_audio=(i % 2 == 0),
                category=self.category
            )
        
        # Criar alguns mangás para os testes
        for i in range(20):
            manga = Manga.objects.create(
                title=f'Manga {i}',
                description=f'Descrição do manga {i}',
                author=f'Autor {i}',
                status='ongoing' if i % 2 == 0 else 'completed'
            )
            manga.genres.add(self.category)

    def test_articles_list_performance(self):
        """
        Testa o desempenho da listagem de artigos
        """
        url = '/api/v1/articles/'
        
        # Medir o tempo de resposta
        start_time = time.time()
        response = self.client.get(url)
        end_time = time.time()
        
        # Verificar se a resposta é bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar o tempo de resposta (deve ser menor que 500ms)
        response_time = (end_time - start_time) * 1000  # Converter para milissegundos
        self.assertLess(response_time, 500, f"Tempo de resposta muito alto: {response_time:.2f}ms")
        
        print(f"Tempo de resposta para listagem de artigos: {response_time:.2f}ms")

    def test_books_list_performance(self):
        """
        Testa o desempenho da listagem de livros
        """
        url = '/api/v1/books/'
        
        # Medir o tempo de resposta
        start_time = time.time()
        response = self.client.get(url)
        end_time = time.time()
        
        # Verificar se a resposta é bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar o tempo de resposta (deve ser menor que 500ms)
        response_time = (end_time - start_time) * 1000  # Converter para milissegundos
        self.assertLess(response_time, 500, f"Tempo de resposta muito alto: {response_time:.2f}ms")
        
        print(f"Tempo de resposta para listagem de livros: {response_time:.2f}ms")

    def test_mangas_list_performance(self):
        """
        Testa o desempenho da listagem de mangás
        """
        url = '/api/v1/mangas/'
        
        # Medir o tempo de resposta
        start_time = time.time()
        response = self.client.get(url)
        end_time = time.time()
        
        # Verificar se a resposta é bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar o tempo de resposta (deve ser menor que 500ms)
        response_time = (end_time - start_time) * 1000  # Converter para milissegundos
        self.assertLess(response_time, 500, f"Tempo de resposta muito alto: {response_time:.2f}ms")
        
        print(f"Tempo de resposta para listagem de mangás: {response_time:.2f}ms")

    def test_categories_list_performance(self):
        """
        Testa o desempenho da listagem de categorias
        """
        url = '/api/v1/categories/'
        
        # Medir o tempo de resposta
        start_time = time.time()
        response = self.client.get(url)
        end_time = time.time()
        
        # Verificar se a resposta é bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar o tempo de resposta (deve ser menor que 300ms)
        response_time = (end_time - start_time) * 1000  # Converter para milissegundos
        self.assertLess(response_time, 300, f"Tempo de resposta muito alto: {response_time:.2f}ms")
        
        print(f"Tempo de resposta para listagem de categorias: {response_time:.2f}ms")

    def test_article_detail_performance(self):
        """
        Testa o desempenho da obtenção de detalhes de um artigo
        """
        # Obter o slug de um artigo
        article = Article.objects.first()
        url = f'/api/v1/articles/{article.slug}/'
        
        # Medir o tempo de resposta
        start_time = time.time()
        response = self.client.get(url)
        end_time = time.time()
        
        # Verificar se a resposta é bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar o tempo de resposta (deve ser menor que 300ms)
        response_time = (end_time - start_time) * 1000  # Converter para milissegundos
        self.assertLess(response_time, 300, f"Tempo de resposta muito alto: {response_time:.2f}ms")
        
        print(f"Tempo de resposta para detalhes de artigo: {response_time:.2f}ms")

    def test_book_detail_performance(self):
        """
        Testa o desempenho da obtenção de detalhes de um livro
        """
        # Obter o slug de um livro
        book = Book.objects.first()
        url = f'/api/v1/books/{book.slug}/'
        
        # Medir o tempo de resposta
        start_time = time.time()
        response = self.client.get(url)
        end_time = time.time()
        
        # Verificar se a resposta é bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar o tempo de resposta (deve ser menor que 300ms)
        response_time = (end_time - start_time) * 1000  # Converter para milissegundos
        self.assertLess(response_time, 300, f"Tempo de resposta muito alto: {response_time:.2f}ms")
        
        print(f"Tempo de resposta para detalhes de livro: {response_time:.2f}ms")

    def test_manga_detail_performance(self):
        """
        Testa o desempenho da obtenção de detalhes de um mangá
        """
        # Obter o slug de um mangá
        manga = Manga.objects.first()
        url = f'/api/v1/mangas/{manga.slug}/'
        
        # Medir o tempo de resposta
        start_time = time.time()
        response = self.client.get(url)
        end_time = time.time()
        
        # Verificar se a resposta é bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar o tempo de resposta (deve ser menor que 300ms)
        response_time = (end_time - start_time) * 1000  # Converter para milissegundos
        self.assertLess(response_time, 300, f"Tempo de resposta muito alto: {response_time:.2f}ms")
        
        print(f"Tempo de resposta para detalhes de mangá: {response_time:.2f}ms")


if __name__ == '__main__':
    unittest.main()
