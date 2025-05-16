"""
Testes de integração para o fluxo de mangás
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from apps.mangas.models import Manga, Chapter
from apps.categories.models import Category
import json

User = get_user_model()


class MangaFlowTestCase(TestCase):
    """
    Testes de integração para o fluxo de mangás
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

        # Criar alguns mangás para os testes
        self.manga1 = Manga.objects.create(
            title='Manga 1',
            description='Descrição do manga 1',
            author='Autor 1',
            status='ongoing'
        )
        self.manga1.genres.add(self.category)

        self.manga2 = Manga.objects.create(
            title='Manga 2',
            description='Descrição do manga 2',
            author='Autor 2',
            status='completed'
        )
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
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['count'], 2)
        self.assertEqual(len(data['results']), 2)

    def test_get_manga_detail(self):
        """
        Testa a obtenção de detalhes de um mangá
        """
        url = f'/api/v1/mangas/{self.manga1.slug}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], 'Manga 1')
        self.assertEqual(data['description'], 'Descrição do manga 1')
        self.assertEqual(data['author'], 'Autor 1')
        self.assertEqual(data['status'], 'ongoing')

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
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['title'], 'Novo Manga')
        self.assertEqual(data['description'], 'Descrição do novo manga')
        self.assertEqual(data['author'], 'Novo Autor')
        self.assertEqual(data['status'], 'ongoing')

        # Verificar se o mangá foi realmente criado no banco de dados
        self.assertTrue(Manga.objects.filter(title='Novo Manga').exists())

    def test_update_manga(self):
        """
        Testa a atualização de um mangá
        """
        # Fazer login como admin
        self.client.force_login(self.admin)

        url = f'/api/v1/mangas/{self.manga1.slug}/'
        data = {
            'title': 'Manga 1 Atualizado',
            'description': 'Descrição atualizada',
            'author': 'Autor Atualizado',
            'status': 'completed'
        }
        response = self.client.patch(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], 'Manga 1 Atualizado')
        self.assertEqual(data['description'], 'Descrição atualizada')
        self.assertEqual(data['author'], 'Autor Atualizado')
        self.assertEqual(data['status'], 'completed')

        # Verificar se o mangá foi realmente atualizado no banco de dados
        manga = Manga.objects.get(id=self.manga1.id)
        self.assertEqual(manga.title, 'Manga 1 Atualizado')
        self.assertEqual(manga.description, 'Descrição atualizada')
        self.assertEqual(manga.author, 'Autor Atualizado')
        self.assertEqual(manga.status, 'completed')

    def test_delete_manga(self):
        """
        Testa a exclusão de um mangá
        """
        # Fazer login como admin
        self.client.force_login(self.admin)

        url = f'/api/v1/mangas/{self.manga1.slug}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        # Verificar se o mangá foi realmente excluído do banco de dados
        self.assertFalse(Manga.objects.filter(id=self.manga1.id).exists())

    def test_list_chapters(self):
        """
        Testa a listagem de capítulos de um mangá
        """
        url = f'/api/v1/mangas/{self.manga1.slug}/chapters/'
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
        url = f'/api/v1/mangas/{self.manga1.slug}/chapters/{self.chapter1.number}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], 'Capítulo 1')
        self.assertEqual(data['number'], 1)
        self.assertEqual(data['pages_count'], 10)

    def test_create_chapter(self):
        """
        Testa a criação de um capítulo
        """
        # Fazer login como admin
        self.client.force_login(self.admin)

        url = f'/api/v1/mangas/{self.manga1.slug}/chapters/'
        data = {
            'number': 3,
            'title': 'Novo Capítulo',
            'pages_count': 20
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['title'], 'Novo Capítulo')
        self.assertEqual(data['number'], 3)
        self.assertEqual(data['pages_count'], 20)

        # Verificar se o capítulo foi realmente criado no banco de dados
        self.assertTrue(Chapter.objects.filter(manga=self.manga1, number=3).exists())

    def test_update_chapter(self):
        """
        Testa a atualização de um capítulo
        """
        # Fazer login como admin
        self.client.force_login(self.admin)

        url = f'/api/v1/mangas/{self.manga1.slug}/chapters/{self.chapter1.number}/'
        data = {
            'title': 'Capítulo 1 Atualizado',
            'pages_count': 12
        }
        response = self.client.patch(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], 'Capítulo 1 Atualizado')
        self.assertEqual(data['pages_count'], 12)

        # Verificar se o capítulo foi realmente atualizado no banco de dados
        chapter = Chapter.objects.get(id=self.chapter1.id)
        self.assertEqual(chapter.title, 'Capítulo 1 Atualizado')
        self.assertEqual(chapter.pages_count, 12)

    def test_delete_chapter(self):
        """
        Testa a exclusão de um capítulo
        """
        # Fazer login como admin
        self.client.force_login(self.admin)

        url = f'/api/v1/mangas/{self.manga1.slug}/chapters/{self.chapter1.number}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        # Verificar se o capítulo foi realmente excluído do banco de dados
        self.assertFalse(Chapter.objects.filter(id=self.chapter1.id).exists())
