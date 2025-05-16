"""
Testes para o utilitário de tratamento de erros
"""

import unittest
from unittest.mock import MagicMock, patch
from django.core.exceptions import RequestDataTooBig, SuspiciousFileOperation
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from utils.error_handling import custom_exception_handler


class TestErrorHandling(unittest.TestCase):
    """
    Testes para o utilitário de tratamento de erros
    """

    def setUp(self):
        """
        Configuração inicial para os testes
        """
        self.context = {'view': MagicMock(), 'request': MagicMock()}

    @patch('utils.error_handling.exception_handler')
    @patch('utils.error_handling.logger')
    def test_custom_exception_handler_with_drf_handled_exception(self, mock_logger, mock_exception_handler):
        """
        Testa se o manipulador de exceções personalizado retorna a resposta do DRF
        quando a exceção já foi tratada pelo DRF
        """
        # Configurar o mock para retornar uma resposta
        mock_response = Response(data={'detail': 'Erro tratado pelo DRF'}, status=400)
        mock_exception_handler.return_value = mock_response

        # Criar uma exceção
        exception = Exception("Teste de exceção")

        # Chamar o manipulador de exceções personalizado
        response = custom_exception_handler(exception, self.context)

        # Verificar se o manipulador de exceções do DRF foi chamado
        mock_exception_handler.assert_called_once_with(exception, self.context)

        # Verificar se o logger foi chamado
        mock_logger.error.assert_not_called()

        # Verificar se a resposta é a mesma retornada pelo DRF
        self.assertEqual(response, mock_response)

    @patch('utils.error_handling.exception_handler')
    @patch('utils.error_handling.logger')
    def test_custom_exception_handler_with_request_data_too_big(self, mock_logger, mock_exception_handler):
        """
        Testa se o manipulador de exceções personalizado trata corretamente a exceção RequestDataTooBig
        """
        # Configurar o mock para retornar None (exceção não tratada pelo DRF)
        mock_exception_handler.return_value = None

        # Criar uma exceção RequestDataTooBig
        exception = RequestDataTooBig("Arquivo muito grande")

        # Chamar o manipulador de exceções personalizado
        response = custom_exception_handler(exception, self.context)

        # Verificar se o manipulador de exceções do DRF foi chamado
        mock_exception_handler.assert_called_once_with(exception, self.context)

        # Verificar se o logger foi chamado
        mock_logger.error.assert_called_once()

        # Verificar se a resposta é do tipo Response
        self.assertIsInstance(response, Response)

        # Verificar o código de status
        self.assertEqual(response.status_code, status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

        # Verificar o conteúdo da resposta
        self.assertEqual(response.data['code'], 'file_too_large')
        self.assertIn('O arquivo enviado é muito grande', response.data['detail'])

    @patch('utils.error_handling.exception_handler')
    @patch('utils.error_handling.logger')
    def test_custom_exception_handler_with_suspicious_file_operation(self, mock_logger, mock_exception_handler):
        """
        Testa se o manipulador de exceções personalizado trata corretamente a exceção SuspiciousFileOperation
        """
        # Configurar o mock para retornar None (exceção não tratada pelo DRF)
        mock_exception_handler.return_value = None

        # Criar uma exceção SuspiciousFileOperation
        exception = SuspiciousFileOperation("Operação suspeita")

        # Chamar o manipulador de exceções personalizado
        response = custom_exception_handler(exception, self.context)

        # Verificar se o manipulador de exceções do DRF foi chamado
        mock_exception_handler.assert_called_once_with(exception, self.context)

        # Verificar se o logger foi chamado
        mock_logger.error.assert_called_once()

        # Verificar se a resposta é do tipo Response
        self.assertIsInstance(response, Response)

        # Verificar o código de status
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verificar o conteúdo da resposta
        self.assertEqual(response.data['code'], 'invalid_file_operation')
        self.assertIn('Operação de arquivo suspeita', response.data['detail'])

    @patch('utils.error_handling.exception_handler')
    @patch('utils.error_handling.logger')
    def test_custom_exception_handler_with_http404(self, mock_logger, mock_exception_handler):
        """
        Testa se o manipulador de exceções personalizado trata corretamente a exceção Http404
        """
        # Configurar o mock para retornar None (exceção não tratada pelo DRF)
        mock_exception_handler.return_value = None

        # Criar uma exceção Http404
        exception = Http404("Recurso não encontrado")

        # Chamar o manipulador de exceções personalizado
        response = custom_exception_handler(exception, self.context)

        # Verificar se o manipulador de exceções do DRF foi chamado
        mock_exception_handler.assert_called_once_with(exception, self.context)

        # Verificar se o logger foi chamado
        mock_logger.error.assert_called_once()

        # Verificar se a resposta é do tipo Response
        self.assertIsInstance(response, Response)

        # Verificar o código de status
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verificar o conteúdo da resposta
        self.assertEqual(response.data['code'], 'not_found')
        self.assertIn('O recurso solicitado não foi encontrado', response.data['detail'])

    @patch('utils.error_handling.exception_handler')
    @patch('utils.error_handling.logger')
    def test_custom_exception_handler_with_unhandled_exception(self, mock_logger, mock_exception_handler):
        """
        Testa se o manipulador de exceções personalizado trata corretamente exceções não tratadas
        """
        # Configurar o mock para retornar None (exceção não tratada pelo DRF)
        mock_exception_handler.return_value = None

        # Criar uma exceção genérica
        exception = ValueError("Valor inválido")

        # Chamar o manipulador de exceções personalizado
        response = custom_exception_handler(exception, self.context)

        # Verificar se o manipulador de exceções do DRF foi chamado
        mock_exception_handler.assert_called_once_with(exception, self.context)

        # Verificar se o logger foi chamado
        mock_logger.error.assert_called_once()

        # Verificar se a resposta é do tipo Response
        self.assertIsInstance(response, Response)

        # Verificar o código de status
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Verificar o conteúdo da resposta
        self.assertEqual(response.data['code'], 'internal_server_error')
        self.assertIn('Ocorreu um erro interno no servidor', response.data['detail'])


if __name__ == '__main__':
    unittest.main()
