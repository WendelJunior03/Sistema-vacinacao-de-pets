# Sistema de Vacinação (API)

API REST para gestão de clínicas, vacinas, estoque e registro de vacinação de pets.  
Stack: Django + Django REST Framework + SimpleJWT.

**Base URL (local):** `http://127.0.0.1:8000/`

**Sumário**
1. Requisitos
2. Instalação
3. Execução
4. Autenticação (JWT)
5. Endpoints
6. Modelos e campos
7. Fluxo sugerido de uso
8. Exemplos de requisição
9. Admin Django
10. Estrutura do projeto
11. Testes
12. Notas de produção
13. Problemas comuns

**Requisitos**
1. Python `3.11.8` (ver `.python-version`)
2. pip

**Instalação**
1. `git clone <URL_DO_REPOSITORIO>`
2. `cd Sistema-de-vacinacao`
3. `python -m venv .venv`
4. `source .venv/bin/activate` (Linux/macOS)
5. `.\.venv\Scripts\activate` (Windows)
6. `python -m pip install --upgrade pip`
7. `python -m pip install django djangorestframework djangorestframework-simplejwt`
8. `python manage.py migrate`
9. `python manage.py createsuperuser`

**Execução**
1. `python manage.py runserver`
2. Acesse `http://127.0.0.1:8000/`

**Autenticação (JWT)**
Todos os endpoints de dados exigem autenticação (`IsAuthenticated`).

Fluxo padrão:
1. Gere o token em `POST /api/token/`
2. Use o `access` no header `Authorization: Bearer <token>`
3. Atualize o token em `POST /api/token/refresh/`

**Login (obter token)**
```bash
curl -X POST http://127.0.0.1:8000/api/token/ -H "Content-Type: application/json" -d '{"username": "admin", "password": "SUA_SENHA"}'
```

**Resposta esperada (exemplo)**
```json
{
  "refresh": "<REFRESH_TOKEN>",
  "access": "<ACCESS_TOKEN>"
}
```

**Atualizar token**
```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ -H "Content-Type: application/json" -d '{"refresh": "<REFRESH_TOKEN>"}'
```

**Requisição autenticada (exemplo)**
```bash
curl -X GET http://127.0.0.1:8000/clinics/ -H "Authorization: Bearer <ACCESS_TOKEN>"
```

**Navegação no navegador**
1. A API tem a interface navegável do DRF habilitada.
2. Acesse qualquer rota no browser para ver a UI.

**Endpoints**
Todos seguem o padrão CRUD do DRF.

| Recurso | Rota base | Métodos |
| --- | --- | --- |
| Clinics | `/clinics/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Vaccines | `/vaccines/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Vaccine Stocks | `/vaccine-stocks/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Owners | `/owners/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Pets | `/pets/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Vaccination Records | `/vaccination-records/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Token | `/api/token/` | `POST` |
| Token Refresh | `/api/token/refresh/` | `POST` |

**Padrão de rotas**
1. Listagem e criação: `/recurso/` (`GET`, `POST`)
2. Detalhe: `/recurso/{id}/` (`GET`, `PUT`, `PATCH`, `DELETE`)
3. O `id` é gerado automaticamente pelo Django.

**Headers esperados**
1. `Authorization: Bearer <ACCESS_TOKEN>`
2. `Content-Type: application/json`

**Formato de datas**
1. `vaccination_date` deve seguir `YYYY-MM-DD`.

**Modelos e campos**

**Clinic**
1. `clinic_name` (string)
2. `cnpj` (string, único)
3. `responsible_pet_owner` (string)

**Owner**
1. `cpf_owner` (string, único)
2. `owner_name` (string)

**Pet**
1. `pet_name` (string)
2. `pet_breed` (string)
3. `pet_age` (inteiro)
4. `owner_pet` (FK para Owner)
5. `owner` (objeto somente leitura com dados do Owner)

**Vaccine**
1. `vaccine_name` (string, único)

**VaccineStock**
1. `vaccine` (FK para Vaccine)
2. `clinic` (FK para Clinic)
3. `quantity` (inteiro)
4. Restrição única: (`vaccine`, `clinic`)

**VaccinationPetRecord**
1. `pet` (FK para Pet)
2. `vaccine` (FK para Vaccine)
3. `vaccination_date` (date, `YYYY-MM-DD`)
4. Restrição única: (`pet`, `vaccine`, `vaccination_date`)

**Regras importantes**
1. Campos FK exigem IDs existentes.
2. Campos únicos e restrições de unicidade retornam `400` em caso de violação.
3. Não há filtros ou paginação configurados por padrão.
4. O JSON retornado pelos endpoints de listagem é o padrão do DRF.

**Exemplo de resposta (Pet)**  
O endpoint de pets retorna o `owner_pet` (id) e também o objeto `owner` somente leitura.
```json
{
  "id": 1,
  "pet_name": "Rex",
  "pet_breed": "Labrador",
  "pet_age": 4,
  "owner_pet": 1,
  "owner": {
    "id": 1,
    "cpf_owner": "123.456.789-00",
    "owner_name": "Maria Silva"
  }
}
```

**Exemplos de payload**

**Criar Owner**
```json
{
  "cpf_owner": "123.456.789-00",
  "owner_name": "Maria Silva"
}
```

**Criar Pet**
```json
{
  "pet_name": "Rex",
  "pet_breed": "Labrador",
  "pet_age": 4,
  "owner_pet": 1
}
```

**Criar Clinic**
```json
{
  "clinic_name": "Clínica Central",
  "cnpj": "12.345.678/0001-90",
  "responsible_pet_owner": "João Souza"
}
```

**Criar Vaccine**
```json
{
  "vaccine_name": "V8"
}
```

**Criar VaccineStock**
```json
{
  "vaccine": 1,
  "clinic": 1,
  "quantity": 50
}
```

**Criar VaccinationPetRecord**
```json
{
  "pet": 1,
  "vaccine": 1,
  "vaccination_date": "2026-02-13"
}
```

**Fluxo sugerido de uso**
1. Crie um `Owner`.
2. Crie um `Pet` apontando para `owner_pet`.
3. Crie uma `Clinic`.
4. Crie uma `Vaccine`.
5. Crie um `VaccineStock` relacionando `clinic` e `vaccine`.
6. Crie um `VaccinationPetRecord` relacionando `pet` e `vaccine`.

**Exemplos de requisição (curl)**

**Criar Owner**
```bash
curl -X POST http://127.0.0.1:8000/owners/ -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"cpf_owner":"123.456.789-00","owner_name":"Maria Silva"}'
```

**Criar Pet**
```bash
curl -X POST http://127.0.0.1:8000/pets/ -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"pet_name":"Rex","pet_breed":"Labrador","pet_age":4,"owner_pet":1}'
```

**Criar Clinic**
```bash
curl -X POST http://127.0.0.1:8000/clinics/ -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"clinic_name":"Clínica Central","cnpj":"12.345.678/0001-90","responsible_pet_owner":"João Souza"}'
```

**Criar Vaccine**
```bash
curl -X POST http://127.0.0.1:8000/vaccines/ -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"vaccine_name":"V8"}'
```

**Criar VaccineStock**
```bash
curl -X POST http://127.0.0.1:8000/vaccine-stocks/ -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"vaccine":1,"clinic":1,"quantity":50}'
```

**Criar VaccinationPetRecord**
```bash
curl -X POST http://127.0.0.1:8000/vaccination-records/ -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"pet":1,"vaccine":1,"vaccination_date":"2026-02-13"}'
```

**Atualizar recurso (exemplo)**
```bash
curl -X PATCH http://127.0.0.1:8000/pets/1/ -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"pet_age":5}'
```

**Remover recurso (exemplo)**
```bash
curl -X DELETE http://127.0.0.1:8000/pets/1/ -H "Authorization: Bearer <ACCESS_TOKEN>"
```

**Exemplo de erro (unicidade)**
```json
{
  "non_field_errors": [
    "The fields vaccine, clinic must make a unique set."
  ]
}
```

**Códigos de status mais comuns**
1. `200 OK` (leitura)
2. `201 Created` (criação)
3. `204 No Content` (delete)
4. `400 Bad Request` (validação/uniqueness)
5. `401 Unauthorized` (sem token ou token inválido)
6. `404 Not Found` (id inexistente)

**Admin Django**
1. Crie um superusuário com `python manage.py createsuperuser`
2. Acesse `http://127.0.0.1:8000/admin/`

**Estrutura do projeto**
1. `api_root/` configurações do Django (settings, urls, wsgi)
2. `vacinacao/` app principal (models, serializers, views)
3. `manage.py` entrada principal para comandos
4. `db.sqlite3` banco local (SQLite)

**Testes**
1. `python manage.py test`

**Notas de produção**
1. `DEBUG = True` e `SECRET_KEY` estão fixos no arquivo `api_root/settings.py`
2. Ajuste `ALLOWED_HOSTS` antes de publicar
3. Configure um banco apropriado para produção (ex: PostgreSQL)
4. Considere configurar `CORS` se for consumir a API em um front-end separado

**Problemas comuns**
1. `401 Unauthorized`: verifique se o token está válido e no header `Authorization`.
2. `400 Bad Request`: confira formato de data `YYYY-MM-DD` e IDs existentes.
3. Erros de unicidade: campos como `cnpj`, `cpf_owner` e combinações únicas não podem se repetir.
4. Erro de tabela inexistente: rode `python manage.py migrate`.
5. Para recriar o banco local, apague `db.sqlite3` e rode `python manage.py migrate`.
