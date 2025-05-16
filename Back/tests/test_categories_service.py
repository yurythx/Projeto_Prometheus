"""
Testes para o serviço de categorias
"""

import unittest
from unittest.mock import MagicMock, patch
from django.test import RequestFactory
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from apps.categories.models import Category


class TestCategoriesService(unittest.TestCase):
    """
    Testes para o serviço de categorias
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
        
        # Criar algumas categorias para os testes
        self.category1 = Category.objects.create(
            name='Categoria 1',
            description='Descrição da categoria 1',
            slug='categoria-1'
        )
        
        self.category2 = Category.objects.create(
            name='Categoria 2',
            description='Descrição da categoria 2',
            slug='categoria-2'
        )

    def test_list_categories(self):
        """
        Testa a listagem de categorias
        """
        url = '/api/v1/categories/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se a resposta contém as categorias criadas
        data = response.json()
        self.assertGreaterEqual(len(data), 2)  # Pode haver categorias padrão
        
        # Verificar os dados da primeira categoria
        category1_data = next(item for item in data if item['slug'] == 'categoria-1')
        self.assertEqual(category1_data['name'], 'Categoria 1')
        self.assertEqual(category1_data['description'], 'Descrição da categoria 1')
        
        # Verificar os dados da segunda categoria
        category2_data = next(item for item in data if item['slug'] == 'categoria-2')
        self.assertEqual(category2_data['name'], 'Categoria 2')
        self.assertEqual(category2_data['description'], 'Descrição da categoria 2')

    def test_get_category_detail(self):
        """
        Testa a obtenção de detalhes de uma categoria
        """
        url = f'/api/v1/categories/{self.category1.slug}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar os dados da categoria
        data = response.json()
        self.assertEqual(data['name'], 'Categoria 1')
        self.assertEqual(data['description'], 'Descrição da categoria 1')
        self.assertEqual(data['slug'], 'categoria-1')

    def test_create_category(self):
        """
        Testa a criação de uma categoria
        """
        # Fazer login como admin
        self.client.force_login(self.admin)
        
        url = '/api/v1/categories/'
        data = {
            'name': 'Nova Categoria',
            'description': 'Descrição da nova categoria'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar os dados da categoria criada
        data = response.json()
        self.assertEqual(data['name'], 'Nova Categoria')
        self.assertEqual(data['description'], 'Descrição da nova categoria')
        self.assertEqual(data['slug'], 'nova-categoria')
        
        # Verificar se a categoria foi realmente criada no banco de dados
        self.assertTrue(Category.objects.filter(name='Nova Categoria').exists())

    def test_update_category(self):
        """
        Testa a atualização de uma categoria
        """
        # Fazer login como admin
        self.client.force_login(self.admin)
        
        url = f'/api/v1/categories/{self.category1.slug}/'
        data = {
            'name': 'Categoria 1 Atualizada',
            'description': 'Descrição atualizada'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar os dados da categoria atualizada
        data = response.json()
        self.assertEqual(data['name'], 'Categoria 1 Atualizada')
        self.assertEqual(data['description'], 'Descrição atualizada')
        
        # Verificar se a categoria foi realmente atualizada no banco de dados
        category = Category.objects.get(id=self.category1.id)
        self.assertEqual(category.name, 'Categoria 1 Atualizada')
        self.assertEqual(category.description, 'Descrição atualizada')

    def test_delete_category(self):
        """
        Testa a exclusão de uma categoria
        """
        # Fazer login como admin
        self.client.force_login(self.admin)
        
        url = f'/api/v1/categories/{self.category1.slug}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verificar se a categoria foi realmente excluída do banco de dados
        self.assertFalse(Category.objects.filter(id=self.category1.id).exists())

    def test_category_articles(self):
        """
        Testa a obtenção de artigos de uma categoria
        """
        url = f'/api/v1/categories/{self.category1.slug}/articles/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se a resposta é uma lista (mesmo que vazia)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIn('results', data)
        self.assertIsInstance(data['results'], list)

    def test_category_books(self):
        """
        Testa a obtenção de livros de uma categoria
        """
        url = f'/api/v1/categories/{self.category1.slug}/books/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se a resposta é uma lista (mesmo que vazia)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIn('results', data)
        self.assertIsInstance(data['results'], list)


if __name__ == '__main__':
    unittest.main()
