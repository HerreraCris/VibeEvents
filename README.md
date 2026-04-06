# VibeEvents

Sistema de curadoria de eventos geolocalizados.

## Como rodar o projeto localmente:

1. **Clone o repositório:**
   `git clone <url-do-repo>`

2. **Crie seu ambiente virtual (Ubuntu):**
   `python3 -m venv venv`
   `source venv/bin/activate`

3. **Instale as dependências de sistema (GeoDjango):**
   `sudo apt update && sudo apt install binutils libproj-dev gdal-bin libgdal-dev`

4. **Instale os pacotes Python:**
   `pip install -r requirements.txt`

5. **Configure o banco de dados:**
   - Crie um banco PostgreSQL.
   - Execute `CREATE EXTENSION postgis;` no banco.
   - Crie um arquivo `.env` baseado no seu acesso local.

6. **Rode as migrações:**
   `python manage.py migrate`
   `python manage.py runserver`
