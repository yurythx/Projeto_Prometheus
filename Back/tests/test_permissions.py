"""
Testes para o utilitário de permissões
"""

import unittest
from unittest.mock import MagicMock, patch

from utils.permissions import (
    BasePermission,
    IsTeamAdminOrReadOnly,
    IsTeamMember,
    IsBoardAdminOrReadOnly,
    IsBoardMember,
    IsTaskAssigneeOrBoardMember,
    IsCommentAuthorOrTaskAssignee,
    IsOwnerOrReadOnly
)


class TestBasePermission(unittest.TestCase):
    """
    Testes para a classe BasePermission
    """

    def setUp(self):
        """
        Configuração inicial para os testes
        """
        self.permission = BasePermission()
        self.request = MagicMock()
        self.user = MagicMock()
        self.team = MagicMock()
        self.board = MagicMock()
        self.task = MagicMock()

    def test_is_safe_method_get(self):
        """
        Testa se o método is_safe_method retorna True para métodos seguros (GET)
        """
        self.request.method = 'GET'
        self.assertTrue(self.permission.is_safe_method(self.request))

    def test_is_safe_method_post(self):
        """
        Testa se o método is_safe_method retorna False para métodos não seguros (POST)
        """
        self.request.method = 'POST'
        self.assertFalse(self.permission.is_safe_method(self.request))

    def test_is_team_admin(self):
        """
        Testa se o método is_team_admin verifica corretamente se um usuário é administrador de uma equipe
        """
        # Configurar o mock para retornar True
        team_membership = MagicMock()
        team_membership.filter.return_value.exists.return_value = True
        self.team.teammembership_set = team_membership

        # Verificar se o método retorna True
        self.assertTrue(self.permission.is_team_admin(self.user, self.team))

        # Verificar se o método filter foi chamado com os parâmetros corretos
        team_membership.filter.assert_called_once_with(user=self.user, role='admin')

    def test_is_board_admin(self):
        """
        Testa se o método is_board_admin verifica corretamente se um usuário é administrador de um quadro
        """
        # Configurar o mock para retornar True
        board_membership = MagicMock()
        board_membership.filter.return_value.exists.return_value = True
        self.board.boardmembership_set = board_membership

        # Verificar se o método retorna True
        self.assertTrue(self.permission.is_board_admin(self.user, self.board))

        # Verificar se o método filter foi chamado com os parâmetros corretos
        board_membership.filter.assert_called_once_with(user=self.user, role='admin')

    def test_is_task_assignee(self):
        """
        Testa se o método is_task_assignee verifica corretamente se um usuário está atribuído a uma tarefa
        """
        # Configurar o mock para retornar True
        self.user.id = 1
        self.task.assignees.filter.return_value.exists.return_value = True

        # Verificar se o método retorna True
        self.assertTrue(self.permission.is_task_assignee(self.user, self.task))

        # Verificar se o método filter foi chamado com os parâmetros corretos
        self.task.assignees.filter.assert_called_once_with(id=self.user.id)


class TestIsTeamAdminOrReadOnly(unittest.TestCase):
    """
    Testes para a classe IsTeamAdminOrReadOnly
    """

    def setUp(self):
        """
        Configuração inicial para os testes
        """
        self.permission = IsTeamAdminOrReadOnly()
        self.request = MagicMock()
        self.view = MagicMock()
        self.obj = MagicMock()

    def test_has_permission_safe_method(self):
        """
        Testa se o método has_permission retorna True para métodos seguros quando o usuário está autenticado
        """
        self.request.method = 'GET'
        self.request.user.is_authenticated = True

        self.assertTrue(self.permission.has_permission(self.request, self.view))

    def test_has_permission_create(self):
        """
        Testa se o método has_permission retorna True para a ação 'create' quando o usuário está autenticado
        """
        self.request.method = 'POST'
        self.request.user.is_authenticated = True
        self.view.action = 'create'

        self.assertTrue(self.permission.has_permission(self.request, self.view))

    def test_has_object_permission_safe_method(self):
        """
        Testa se o método has_object_permission retorna True para métodos seguros quando o usuário está autenticado
        """
        self.request.method = 'GET'
        self.request.user.is_authenticated = True

        self.assertTrue(self.permission.has_object_permission(self.request, self.view, self.obj))

    @patch.object(IsTeamAdminOrReadOnly, 'is_team_admin')
    def test_has_object_permission_not_safe_method(self, mock_is_team_admin):
        """
        Testa se o método has_object_permission verifica se o usuário é administrador da equipe para métodos não seguros
        """
        self.request.method = 'PUT'
        mock_is_team_admin.return_value = True

        self.assertTrue(self.permission.has_object_permission(self.request, self.view, self.obj))
        mock_is_team_admin.assert_called_once_with(self.request.user, self.obj)


class TestIsOwnerOrReadOnly(unittest.TestCase):
    """
    Testes para a classe IsOwnerOrReadOnly
    """

    def setUp(self):
        """
        Configuração inicial para os testes
        """
        self.permission = IsOwnerOrReadOnly()
        self.request = MagicMock()
        self.view = MagicMock()
        self.obj = MagicMock()

    def test_has_object_permission_safe_method(self):
        """
        Testa se o método has_object_permission retorna True para métodos seguros
        """
        self.request.method = 'GET'
        self.assertTrue(self.permission.has_object_permission(self.request, self.view, self.obj))

    def test_has_object_permission_owner(self):
        """
        Testa se o método has_object_permission retorna True quando o usuário é o dono do objeto
        """
        self.request.method = 'PUT'
        self.obj.owner = self.request.user
        self.assertTrue(self.permission.has_object_permission(self.request, self.view, self.obj))

    def test_has_object_permission_not_owner(self):
        """
        Testa se o método has_object_permission retorna False quando o usuário não é o dono do objeto
        """
        self.request.method = 'PUT'
        self.obj.owner = MagicMock()  # Outro usuário
        self.assertFalse(self.permission.has_object_permission(self.request, self.view, self.obj))


if __name__ == '__main__':
    unittest.main()
