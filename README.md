# Gerenciador de atividades avaliativas

## 1. Clonando o repositório e criando ambiente virtual
### clone o repositorio pelo comando
```bash
git clone https://github.com/LucasMairon/Gerenciador_Atividades_Avaliativas.git
```
### Entre na pasta do projeto
```bash
cd backend
```
### Crie o ambiente virtual com o seguinte comando
```bash
python3 -m venv venv
```
### Ative seu ambiente virtual
```bash
source venv/bin/activate
```
## Instale as dependências
### Do Back-End
```bash
pip install -r requirements.txt
```
### Do Front-End
```bash
npm install
```

## 2. Criando arquivo .env
### Va na pasta dotenv_files e duplique o arquivo .env-example, trocando o seu nome por .env
### Substitua as variaveis pelos seus valores reais
```bash
# Secret Key configuration
SECRET_KEY = 'CHANGE_HERE'

# Debug Mode configuration
# Use True or false
DEBUG = True

ALLOWED_HOSTS = "127.0.0.1, locahost"

# Postgres database configuration
DB_ENGINE = 'django.db.backends.postgresql'
POSTGRES_DB = 'CHANGE_HERE'
POSTGRES_USER = 'CHANGE_HERE'
POSTGRES_PASSWORD = 'CHANGE_HERE'
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = '5432'
```
## 3. Prepare o Banco
```bash
python manage.py migrate
```

## 4. Crie um SuperUser
```bash
python manage.py createsuperuser
```


## 3. Execute o programa
```bash
python manage.py runserver
```
### Após esse passo deve aparecer um link sobre o seu terminal, essa é a rota raiz e o sistema já está executando corretamente