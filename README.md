# Sistema de Votação (Voting System)

Um sistema de votação simples desenvolvido em Django para o curso Python-ISCTE.

## Funcionalidades

- **Criar Questões**: Administradores podem criar questões de votação
- **Adicionar Opções**: Cada questão pode ter múltiplas opções de resposta
- **Sistema de Votação**: Usuários podem votar em uma opção por questão
- **Visualização de Resultados**: Resultados em tempo real das votações
- **Interface Administrativa**: Painel admin para gerenciar questões e opções

## Estrutura do Projeto

```
Python-ISCTE-master/
├── sitepr1/           # Configurações principais do Django
├── votacao/           # Aplicação principal de votação
│   ├── models.py      # Modelos Questao e Opcao
│   ├── views.py       # Lógica de negócio
│   ├── urls.py        # Configuração de URLs
│   ├── admin.py       # Interface administrativa
│   └── templates/     # Templates HTML
└── manage.py          # Script de gerenciamento Django
```

## Modelos de Dados

### Questao (Question)
- `questao_texto`: Texto da questão
- `pub_data`: Data de publicação
- `foi_publicada_recentemente()`: Método para verificar se foi publicada nas últimas 24h

### Opcao (Option)
- `questao`: Referência à questão (ForeignKey)
- `opcao_texto`: Texto da opção
- `votos`: Contador de votos

## Como Usar

### 1. Instalação e Configuração

```bash
# Instalar Django
pip install django==3.0.5

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

### 2. Acessar a Aplicação

- **Página Principal**: http://localhost:8000/votacao/
- **Lista de Questões**: http://localhost:8000/votacao/questoes/
- **Admin**: http://localhost:8000/admin/

### 3. Criar Questões e Opções

1. Acesse http://localhost:8000/admin/
2. Faça login com suas credenciais de superusuário
3. Em "Votacao" > "Questões", clique em "Adicionar Questão"
4. Preencha o texto da questão e a data de publicação
5. Adicione opções de resposta (mínimo 2)
6. Salve a questão

### 4. Votar

1. Acesse a lista de questões
2. Clique em "Votar nesta Questão"
3. Selecione uma opção
4. Clique em "Votar"

## URLs da Aplicação

- `/votacao/` - Página inicial
- `/votacao/questoes/` - Lista de todas as questões
- `/votacao/<id>/` - Detalhes de uma questão específica
- `/votacao/<id>/votar/` - Processar voto (POST)

## Tecnologias Utilizadas

- **Django 3.0.5**: Framework web Python
- **SQLite**: Banco de dados
- **HTML/CSS**: Interface do usuário
- **Python 3.10+**: Linguagem de programação

## Próximos Passos para Desenvolvimento

- [ ] Sistema de autenticação de usuários
- [ ] Histórico de votos por usuário
- [ ] Gráficos de resultados
- [ ] API REST para integração
- [ ] Testes automatizados
- [ ] Deploy em produção

## Autor

Desenvolvido para o curso Python-ISCTE
