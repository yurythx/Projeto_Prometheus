"""
Testes para o serviço de usuários
"""

import unittest
from unittest.mock import MagicMock, patch
from django.test import RequestFactory
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.accounts.models import UserSettings

User = get_user_model()


class TestUsersService(unittest.TestCase):
    """
    Testes para o serviço de usuários
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
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )
        
        # Criar um usuário admin para os testes
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
            first_name='Admin',
            last_name='User'
        )
        
        # Criar configurações para o usuário
        self.user_settings = UserSettings.objects.create(
            user=self.user,
            theme='light',
            language='pt-br',
            notifications_enabled=True
        )

    def test_user_registration(self):
        """
        Testa o registro de um novo usuário
        """
        url = '/api/v1/auth/users/'
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newuserpassword',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar se o usuário foi criado
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # Verificar se as configurações do usuário foram criadas
        new_user = User.objects.get(username='newuser')
        self.assertTrue(UserSettings.objects.filter(user=new_user).exists())

    def test_user_login(self):
        """
        Testa o login de um usuário
        """
        url = '/api/v1/auth/jwt/create/'
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se a resposta contém os tokens
        data = response.json()
        self.assertIn('access', data)
        self.assertIn('refresh', data)

    def test_user_profile(self):
        """
        Testa a obtenção do perfil do usuário
        """
        # Fazer login como usuário
        self.client.force_login(self.user)
        
        url = '/api/v1/auth/users/me/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar os dados do perfil
        data = response.json()
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['first_name'], 'Test')
        self.assertEqual(data['last_name'], 'User')

    def test_update_user_profile(self):
        """
        Testa a atualização do perfil do usuário
        """
        # Fazer login como usuário
        self.client.force_login(self.user)
        
        url = '/api/v1/auth/users/me/'
        data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se os dados foram atualizados
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.last_name, 'Name')

    def test_change_password(self):
        """
        Testa a alteração de senha do usuário
        """
        # Fazer login como usuário
        self.client.force_login(self.user)
        
        url = '/api/v1/auth/users/set_password/'
        data = {
            'current_password': 'testpassword',
            'new_password': 'newtestpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verificar se a senha foi alterada
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newtestpassword'))

    def test_get_user_settings(self):
        """
        Testa a obtenção das configurações do usuário
        """
        # Fazer login como usuário
        self.client.force_login(self.user)
        
        url = '/api/v1/users/settings/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar os dados das configurações
        data = response.json()
        self.assertEqual(data['theme'], 'light')
        self.assertEqual(data['language'], 'pt-br')
        self.assertTrue(data['notifications_enabled'])

    def test_update_user_settings(self):
        """
        Testa a atualização das configurações do usuário
        """
        # Fazer login como usuário
        self.client.force_login(self.user)
        
        url = '/api/v1/users/settings/'
        data = {
            'theme': 'dark',
            'language': 'en',
            'notifications_enabled': False
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se os dados foram atualizados
        self.user_settings.refresh_from_db()
        self.assertEqual(self.user_settings.theme, 'dark')
        self.assertEqual(self.user_settings.language, 'en')
        self.assertFalse(self.user_settings.notifications_enabled)


if __name__ == '__main__':
    unittest.main()
