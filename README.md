# VibeEvents 🚀 - Curadoria de Eventos Geolocalizados

**UFT - Campus Palmas** **Disciplina:** Projeto de Sistemas 2026/1
**Professor:** Dr. Edeilson Milhomem da Silva  
**Grupo:** VibeEvents  
**Integrantes:** Cristian, Gabriel Marques, Gabriel Portuguez, Laurinda, Vinicius Fernandes.

---

## 📌 Sobre o Projeto
O **VibeEvents** é um sistema web intuitivo para a curadoria e visualização de eventos na cidade de Palmas. O foco é oferecer uma plataforma prática para que usuários encontrem lazer e causas sociais através de um mapa interativo com geolocalização em tempo real.

### Com o VibeEvents, você pode:
* **Explorar o Mapa Interativo:** Visualize eventos em Palmas com pins personalizados por categoria.
* **Filtrar Experiências (US-EV-02):** Encontre rapidamente eventos de Música, Esporte, Cultura ou Empreendedorismo.
* **Apoiar Causas Sociais:** Identifique "Eventos Solidários" através de selos de impacto social nos cards e popups.
* **Gestão de Curadoria:** Painel administrativo restrito para cadastro de eventos com interface intuitiva e suporte a mapas.
* **Garantir Ingressos:** Links diretos para plataformas externas de inscrição ou compra.

---
## 🚀 Como rodar o projeto localmente

### 1. Clone o repositório
```bash
git clone <url-do-seu-repositorio>
cd VibeEvents
```

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


---

## 🚀 Features do Projeto

### 📌 Sprint 1 — Mapa e Curadoria

#### **US-EV-01 — Visualizar Mapa de Eventos**
**Como** usuário final  
**Quero** visualizar eventos em um mapa interativo  
**Para** encontrar eventos próximos de mim facilmente.

* **Critérios de Aceite:**
    * Dado que acesso a URL principal da plataforma.
    * Quando o mapa carrega, vejo pins coloridos representando eventos em Palmas.
    * Então, ao clicar em um pin, vejo um resumo com nome e data do evento.

#### **US-EV-02 — Filtrar por Categoria e Impacto Social**
**Como** usuário interessado em causas sociais ou lazer  
**Quero** filtrar eventos por categoria e por selo "beneficente"  
**Para** encontrar rapidamente o tipo de rolê ou causa que quero apoiar.

* **Critérios de Aceite:**
    * Dado que estou na tela do mapa.
    * Quando seleciono uma categoria (ex: Esporte), apenas pins dessa categoria permanecem visíveis.
    * Quando ativo o filtro "Beneficente", vejo apenas eventos com o selo "Evento Solidário".

#### **US-EV-03 — Ver Detalhes e Link Externo**
**Como** usuário que encontrou um evento interessante  
**Quero** acessar a descrição completa e o link de inscrição  
**Para** decidir se vou participar e acessar a ticketeira externa.

* **Critérios de Aceite:**
    * Dado que cliquei em um evento no mapa.
    * Quando a aba de detalhes abre, vejo descrição, local exato e um botão "Garantir Ingresso".
    * Então, ao clicar no botão, sou redirecionado para o link externo cadastrado.

#### **US-EV-04 — Cadastro de Eventos (Curadoria)**
**Como** administrador do sistema  
**Quero** cadastrar eventos manualmente via painel administrativo  
**Para** garantir que a plataforma tenha conteúdo relevante no lançamento.

* **Critérios de Aceite:**
    * Dado que estou autenticado como admin no Django.
    * Quando preencho nome, coordenadas geográficas, categoria e link.
    * Então o evento aparece imediatamente no mapa público com a cor e informações corretas.

---

## 📌 DIVISÃO DAS TAREFAS

### 1ª Sprint - Mapa e Curadoria

| Atividade | Feature | Autor | Revisor |
| :--- | :--- | :--- | :--- |
| Configuração PostGIS e Modelagem de Eventos | Infra-DB | cristian | laura |
| Integração Leaflet.js e Exibição de Pins | US-EV-01 | g. Português | vinicius |
| Lógica de Filtros (Categorias e Beneficente) | US-EV-02 | g.marques | cristian |
| Tela de Detalhes e Redirecionamento Externo | US-EV-03 | vinicius | g. marques |
| Interface de Curadoria (Django Admin Custom) | US-EV-04 | Laurinda | cristian |
