"""
Testes para o serviço de mangás
"""

import unittest
from unittest.mock import MagicMock, patch
from django.test import RequestFactory
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from apps.mangas.models import Manga, Chapter
from apps.categories.models import Category


class TestMangasService(unittest.TestCase):
    """
    Testes para o serviço de mangás
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
        
        # Criar alguns mangás para os testes
        self.manga1 = Manga.objects.create(
            title='Manga 1',
            description='Descrição do manga 1',
            author='Autor 1',
            status='ongoing'
        )
        
        self.manga2 = Manga.objects.create(
            title='Manga 2',
            description='Descrição do manga 2',
            author='Autor 2',
            status='completed'
        )
        
        # Adicionar categorias aos mangás
        self.manga1.genres.add(self.category)
        self.manga2.genres.add(self.category)
        
        # Criar alguns capítulos para os testes
        self.chapter1 = Chapter.objects.create(
            manga=self.manga1,
            number=1,
            title='Capítulo 1',
            pages_count=10
        )
        
        self.chapter2 = Chapter.objects.create(
            manga=self.manga1,
            number=2,
            title='Capítulo 2',
            pages_count=15
        )

    def test_list_mangas(self):
        """
        Testa a listagem de mangás
        """
        url = '/api/v1/mangas/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se a resposta contém os mangás criados
        data = response.json()
        self.assertEqual(data['count'], 2)
        self.assertEqual(len(data['results']), 2)
        
        # Verificar os dados do primeiro mangá
        manga1_data = next(item for item in data['results'] if item['title'] == 'Manga 1')
        self.assertEqual(manga1_data['description'], 'Descrição do manga 1')
        self.assertEqual(manga1_data['author'], 'Autor 1')
        self.assertEqual(manga1_data['status'], 'ongoing')
        
        # Verificar os dados do segundo mangá
        manga2_data = next(item for item in data['results'] if item['title'] == 'Manga 2')
        self.assertEqual(manga2_data['description'], 'Descrição do manga 2')
        self.assertEqual(manga2_data['author'], 'Autor 2')
        self.assertEqual(manga2_data['status'], 'completed')

    def test_get_manga_detail(self):
        """
        Testa a obtenção de detalhes de um mangá
        """
        url = f'/api/v1/mangas/{self.manga1.slug}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar os dados do mangá
        data = response.json()
        self.assertEqual(data['title'], 'Manga 1')
        self.assertEqual(data['description'], 'Descrição do manga 1')
        self.assertEqual(data['author'], 'Autor 1')
        self.assertEqual(data['status'], 'ongoing')

    def test_list_chapters(self):
        """
        Testa a listagem de capítulos de um mangá
        """
        url = f'/api/v1/mangas/{self.manga1.slug}/chapters/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se a resposta contém os capítulos criados
        data = response.json()
        self.assertEqual(len(data), 2)
        
        # Verificar os dados do primeiro capítulo
        chapter1_data = next(item for item in data if item['number'] == 1)
        self.assertEqual(chapter1_data['title'], 'Capítulo 1')
        self.assertEqual(chapter1_data['pages_count'], 10)
        
        # Verificar os dados do segundo capítulo
        chapter2_data = next(item for item in data if item['number'] == 2)
        self.assertEqual(chapter2_data['title'], 'Capítulo 2')
        self.assertEqual(chapter2_data['pages_count'], 15)

    def test_get_chapter_detail(self):
        """
        Testa a obtenção de detalhes de um capítulo
        """
        url = f'/api/v1/mangas/{self.manga1.slug}/chapters/{self.chapter1.number}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar os dados do capítulo
        data = response.json()
        self.assertEqual(data['title'], 'Capítulo 1')
        self.assertEqual(data['number'], 1)
        self.assertEqual(data['pages_count'], 10)

    def test_create_manga(self):
        """
        Testa a criação de um mangá
        """
        # Fazer login como admin
        self.client.force_login(self.admin)
        
        url = '/api/v1/mangas/'
        data = {
            'title': 'Novo Manga',
            'description': 'Descrição do novo manga',
            'author': 'Novo Autor',
            'status': 'ongoing',
            'genres': [self.category.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar os dados do mangá criado
        data = response.json()
        self.assertEqual(data['title'], 'Novo Manga')
        self.assertEqual(data['description'], 'Descrição do novo manga')
        self.assertEqual(data['author'], 'Novo Autor')
        self.assertEqual(data['status'], 'ongoing')
        
        # Verificar se o mangá foi realmente criado no banco de dados
        self.assertTrue(Manga.objects.filter(title='Novo Manga').exists())


if __name__ == '__main__':
    unittest.main()
