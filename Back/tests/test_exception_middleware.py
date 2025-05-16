"""
Testes para o middleware de exceção
"""

import unittest
from unittest.mock import MagicMock, patch
from django.http import JsonResponse
from django.test import RequestFactory
from rest_framework import status

from core.middleware.exception import ExceptionMiddleware


class TestExceptionMiddleware(unittest.TestCase):
    """
    Testes para o middleware de exceção
    """

    def setUp(self):
        """
        Configuração inicial para os testes
        """
        self.middleware = ExceptionMiddleware(get_response=MagicMock())
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

    @patch('core.middleware.exception.logger')
    def test_process_exception_returns_json_response(self, mock_logger):
        """
        Testa se o middleware retorna uma resposta JSON quando ocorre uma exceção
        """
        # Criar uma exceção
        exception = Exception("Teste de exceção")

        # Chamar o método process_exception
        response = self.middleware.process_exception(self.request, exception)

        # Verificar se o logger foi chamado
        mock_logger.error.assert_called_once()

        # Verificar se a resposta é do tipo JsonResponse
        self.assertIsInstance(response, JsonResponse)

        # Verificar o código de status
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Verificar o conteúdo da resposta
        content = response.content.decode('utf-8')
        self.assertIn('"error": "Erro Interno"', content)
        self.assertIn('"detail": "Erro interno do servidor"', content)
        self.assertIn('"status_code": 500', content)

    @patch('core.middleware.exception.logger')
    def test_process_exception_logs_exception(self, mock_logger):
        """
        Testa se o middleware registra a exceção no log
        """
        # Criar uma exceção
        exception = ValueError("Valor inválido")

        # Chamar o método process_exception
        self.middleware.process_exception(self.request, exception)

        # Verificar se o logger foi chamado com a mensagem correta
        mock_logger.error.assert_called_once_with(
            f"Exceção não tratada: {str(exception)}",
            exc_info=True
        )

    @patch('core.middleware.exception.logger')
    def test_process_exception_with_different_exception_types(self, mock_logger):
        """
        Testa o middleware com diferentes tipos de exceção
        """
        # Lista de exceções para testar
        exceptions = [
            ValueError("Valor inválido"),
            TypeError("Tipo inválido"),
            KeyError("Chave inválida"),
            AttributeError("Atributo inválido"),
            IndexError("Índice inválido"),
        ]

        for exception in exceptions:
            # Chamar o método process_exception
            response = self.middleware.process_exception(self.request, exception)

            # Verificar se o logger foi chamado
            mock_logger.error.assert_called()

            # Verificar se a resposta é do tipo JsonResponse
            self.assertIsInstance(response, JsonResponse)

            # Verificar o código de status
            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Limpar o mock para o próximo teste
            mock_logger.reset_mock()


if __name__ == '__main__':
    unittest.main()
