# Descrição

Esse sistema é um sistema de planejamento de redes LoRaWAN capaz de gerar datasets com soluções otimizadas, permitindo aos administradores ajustar os parâmetros conforme suas necessidades e facilitando novas pesquisas na área. O sistema recebe parâmetros de configuração da rede, regiões a serem atendidas e densidade de usuários, gerando como saída a localização dos nós clientes e dos gateways necessários para cobertura total da área.

# Arquitetura

- Frontend: Vue.js (https://vuejs.org/)
- Backend (API): Django (https://www.djangoproject.com/)
- Visualização de mapa: MapBox (https://www.mapbox.com/)
- Banco de dados: PosgreSQL + PostGIS (https://postgis.net/)

# Como executar

## Backend

### Requisitos

- Python 3.9
- Um banco de dados PostgreSQL configurado com a extensão PostGIS

### Passo a passo

1. Configure um banco de dados externo do PostgreSQL e execute o comando abaixo para ativar a extensão do PostGIS:

```SQL
CREATE EXTENSION postgis;
```

Ou, caso sua máquina possua o Docker instalado, execute o comando abaixo dentro da pasta backend para subir um banco já com o PostGIS configurado:

```bash
$ docker-compose up -d
```

2. Crie um arquivo .env na raiz da pasta do backend e preencha as seguintes variáveis de ambiente:

```
DOMAIN_BACKEND= FQDN do backend (localhost caso seja executado localmente)
DOMAIN_FRONTEND= FQDN do frontend (localhost caso seja executado localmente)

DJANGO_DEBUG= debug ativo ou não (TRUE ou FALSE)
DJANGO_SUPERUSER_EMAIL= login do super usuario do Django
DJANGO_SUPERUSER_PASSWORD= senha do supeu usuario do Django
DJANGO_SECRET_KEY= gere em https://djecrety.ir/
DJANGO_PORT= porta onde a API irá responder

PGDATABASE= nome da base de dados
PGUSER= usuário do banco de dados
PGPASSWORD= senha do banco de dados
PGHOST= host do banco de dados
PGPORT= porta do banco de dados
```

Caso o banco esteja sendo executado dentro do container do Docker construído pelo docker-compose.yml desse projeto, coloque as seguintes credenciais do banco:

```
PGDATABASE=postgres
PGUSER=postgres
PGPASSWORD=postgres
PGHOST=localhost
PGPORT=5439
```

3. Instale o pipenv e as dependências do projeto:

```bash
$ pip install pipenv
$ pipenv install
$ pipenv shell
```

4. Execute o comando abaixo para preencher a base de dados com as tabelas necessárias:

```bash
$ python manage.py migrate
```

5. Execute o comando referente ao ambiente que deseja criar:

```bash
$ python manage.py runserver (ambiente de desenvolvimento)
$ gunicorn core.wsgi (ambiente de produção LINUX)
```

## Frontend

### Requisitos

- Node v18

### Passo a passo

1. Baixe as dependências necessárias com seu gerenciador preferido executando qualquer comando abaixo na raiz da pasta do frontend:

```bash
$ npm install
$ yarn install
$ pnpm install
```

2. Crie uma conta no Mapbox (https://account.mapbox.com/) e gere um TOKEN

3. Crie um arquivo .env na raiz da pasta do frontend e preencha as seguintes variáveis de ambiente:

```
MAPBOX_TOKEN= TOKEN gerado na plataforma do Mapbox
BASE_URL= FQDN do frontend
```

5. Execute o comando referente ao ambiente que deseja criar:

```bash
$ npm/yarn/pnpm dev (Ambiente de desenvolvimento)
$ npm/yarn/pnpm build (Ambiente de produção)
```

Obs.: no ambiente do produção será gerado uma pasta chamada .output. Essa pasta deve ser servida por um servidor HTTP da sua escolha (APACHE, NGINX e afins)

# Como utilizar o sistema
