# Testes do Backend

Este diretório contém os testes para o backend da aplicação. Os testes estão organizados em diferentes categorias:

- **Testes Unitários**: Testam componentes individuais da aplicação.
- **Testes de Integração**: Testam a interação entre diferentes componentes da aplicação.
- **Testes de Desempenho**: Testam o desempenho da aplicação sob diferentes condições.

## Estrutura de Diretórios

```
tests/
├── __init__.py
├── integration/
│   ├── __init__.py
│   ├── test_article_flow.py
│   ├── test_book_flow.py
│   └── test_manga_flow.py
├── performance/
│   ├── __init__.py
│   └── test_api_performance.py
├── test_categories_service.py
├── test_error_handling.py
├── test_exception_middleware.py
├── test_books_service.py
├── test_mangas_service.py
├── test_permissions.py
└── test_users_service.py
```

## Executando os Testes

### Executar Todos os Testes

Para executar todos os testes, use o script `run_all_tests.py`:

```bash
python run_all_tests.py
```

### Executar Testes Específicos

Para executar testes específicos, passe os caminhos dos testes como argumentos:

```bash
python run_all_tests.py tests.test_users_service tests.test_categories_service
```

### Executar Testes por Categoria

#### Testes Unitários

```bash
python run_all_tests.py tests.test_exception_middleware tests.test_error_handling tests.test_permissions tests.test_users_service tests.test_categories_service tests.test_books_service tests.test_mangas_service
```

#### Testes de Integração

```bash
python run_all_tests.py tests.integration.test_article_flow tests.integration.test_book_flow tests.integration.test_manga_flow
```

#### Testes de Desempenho

```bash
python run_all_tests.py tests.performance.test_api_performance
```

## Adicionando Novos Testes

### Testes Unitários

Os testes unitários devem ser adicionados na raiz do diretório `tests/`. Cada arquivo de teste deve seguir a convenção de nomenclatura `test_*.py`.

Exemplo:

```python
"""
Testes para o serviço de exemplo
"""

import unittest
from unittest.mock import MagicMock, patch
from django.test import RequestFactory
from rest_framework.test import APIClient
from rest_framework import status

class TestExampleService(unittest.TestCase):
    """
    Testes para o serviço de exemplo
    """

    def setUp(self):
        """
        Configuração inicial para os testes
        """
        self.client = APIClient()
        self.factory = RequestFactory()

    def test_example(self):
        """
        Testa um exemplo
        """
        self.assertTrue(True)
```

### Testes de Integração

Os testes de integração devem ser adicionados no diretório `tests/integration/`. Cada arquivo de teste deve seguir a convenção de nomenclatura `test_*.py`.

Exemplo:

```python
"""
Testes de integração para o fluxo de exemplo
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
import json

User = get_user_model()

class ExampleFlowTestCase(TestCase):
    """
    Testes de integração para o fluxo de exemplo
    """
    def setUp(self):
        """
        Configuração inicial para os testes
        """
        self.client = Client()

    def test_example(self):
        """
        Testa um exemplo
        """
        self.assertTrue(True)
```

### Testes de Desempenho

Os testes de desempenho devem ser adicionados no diretório `tests/performance/`. Cada arquivo de teste deve seguir a convenção de nomenclatura `test_*.py`.

Exemplo:

```python
"""
Testes de desempenho para o exemplo
"""

import unittest
import time
from django.test import Client

class ExamplePerformanceTestCase(unittest.TestCase):
    """
    Testes de desempenho para o exemplo
    """

    def setUp(self):
        """
        Configuração inicial para os testes
        """
        self.client = Client()

    def test_example_performance(self):
        """
        Testa o desempenho de um exemplo
        """
        # Medir o tempo de resposta
        start_time = time.time()
        # Fazer algo
        end_time = time.time()
        
        # Verificar o tempo de resposta (deve ser menor que 500ms)
        response_time = (end_time - start_time) * 1000  # Converter para milissegundos
        self.assertLess(response_time, 500, f"Tempo de resposta muito alto: {response_time:.2f}ms")
```

## Boas Práticas

1. **Isolamento**: Cada teste deve ser independente dos outros testes.
2. **Nomenclatura**: Use nomes descritivos para os testes.
3. **Documentação**: Documente o propósito de cada teste.
4. **Mocks**: Use mocks para isolar o código que está sendo testado.
5. **Assertions**: Use assertions específicas para verificar o comportamento esperado.
6. **Limpeza**: Limpe os recursos utilizados nos testes.
7. **Cobertura**: Tente cobrir todos os caminhos de código.
8. **Desempenho**: Os testes devem ser rápidos para executar.
9. **Manutenção**: Mantenha os testes atualizados com as mudanças no código.
10. **Simplicidade**: Mantenha os testes simples e fáceis de entender.
