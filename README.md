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

# 📌 Planejamento de Sprints

---

## 🚀 Sprint 1: Mapa e Curadoria de Eventos

### 🎯 Valor
Centralizar a divulgação regional e permitir a descoberta visual de eventos por categoria e impacto social.

### ✅ Tarefas
- Configuração do Ambiente e Banco de Dados:
  - Configurar o projeto Django com PostgreSQL e bibliotecas para suporte a mapas.

- Visualização em Mapa (Core):
  - Exibir eventos em um mapa interativo com pins coloridos por categoria.

- Filtros de Categoria e Social:
  - Permitir que o usuário filtre eventos por tipo (Música, Esporte, etc.) e identifique causas beneficentes.

- Detalhes do Evento:
  - Disponibilizar uma visão clara com data, local e link externo para cada evento clicado no mapa.

- Cadastro Administrativo (Curadoria):
  - Interface para a equipe cadastrar manualmente os primeiros eventos de Palmas.

---

##  Features 

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

# 📌 Planejamento de Sprints

##  Sprint 2: Autonomia do Usuário e Engajamento

### 🎯 Valor
Democratizar o acesso à plataforma permitindo o envio colaborativo de eventos e facilitando a busca por localização e tempo.

### ✅ Tarefas
- Formulário de Sugestão Pública:
  - Criar uma interface para que organizadores e usuários comuns sugiram eventos sem precisar acessar o painel administrativo.

- Busca por Endereço:
  - Implementar uma barra de pesquisa que permita ao usuário centrar o mapa em um endereço ou ponto de referência específico.

- Filtros de Data:
  - Adicionar a funcionalidade de filtrar eventos por "Hoje", "Fim de Semana" ou um intervalo de datas específico.

- Sistema de Favoritos Local:
  - Permitir que o usuário salve eventos de interesse para consulta rápida (armazenamento via LocalStorage).

- Fluxo de Aprovação de Curadoria:
  - Implementar um status de "Pendente" para eventos sugeridos, exigindo aprovação do curador antes da publicação no mapa.

---

##  Features 

#### **US-EV-05 — Sugerir Novo Evento (Público)**
**Como** organizador ou entusiasta de eventos  
**Quero** enviar os dados de um evento através de um formulário público  
**Para** que os curadores possam avaliar e publicar minha sugestão no mapa.

* **Critérios de Aceite:**
    * Dado que acesso a página "Sugerir Evento".
    * Quando preencho os campos obrigatórios e seleciono o local no mapa.
    * Então recebo uma confirmação de que a sugestão foi enviada para análise e o evento não aparece no mapa imediatamente.

---

#### **US-EV-06 — Busca por Localização**
**Como** usuário que planeja uma saída  
**Quero** pesquisar por um bairro ou endereço específico  
**Para** ver quais eventos estão acontecendo naquela região sem precisar navegar manualmente pelo mapa.

* **Critérios de Aceite:**
    * Dado que estou na tela inicial.
    * Quando digito um endereço na barra de busca.
    * Então o mapa é centralizado automaticamente nas coordenadas correspondentes com um zoom adequado.

---

#### **US-EV-07 — Filtro por Período de Tempo**
**Como** usuário com agenda limitada  
**Quero** filtrar os eventos que acontecem em datas específicas (ex: apenas hoje)  
**Para** planejar meu lazer de acordo com minha disponibilidade.

* **Critérios de Aceite:**
    * Dado que estou na barra lateral de filtros.
    * Quando seleciono o filtro "Este Fim de Semana".
    * Então apenas os pins de eventos que ocorrem entre sexta e domingo permanecem visíveis.

---

#### **US-EV-08 — Painel de Aprovação (Moderador)**
**Como** curador da plataforma  
**Quero** visualizar uma lista de eventos sugeridos pelo público  
**Para** aprovar, editar ou rejeitar o conteúdo antes dele ir ao ar.

* **Critérios de Aceite:**
    * Dado que estou no painel administrativo.
    * Quando altero o status de um evento de "Pendente" para "Publicado".
    * Então esse evento passa a estar visível para todos os usuários no mapa público.

---

## 📌 DIVISÃO DAS TAREFAS

### 2ª Sprint - Autonomia e Engajamento

| Atividade | Feature | Autor | Revisor |
| :--- | :--- | :--- | :--- |
| Criação do Formulário Público de Sugestão de Eventos | US-EV-05 | cristian | laura |
| Integração de Busca por Endereço e Centralização do Mapa | US-EV-06 | vinicius | g. marques |
| Implementação de Filtros por Data e Período | US-EV-07 | g.marques | cristian |
| Desenvolvimento do Painel de Aprovação de Eventos | US-EV-08 | laurinda | vinicius |
| Controle de Status dos Eventos (Pendente/Publicado/Rejeitado) | Infra-Admin | cristian | laura |


# 📌 Planejamento de Sprints
---

##  Sprint 3: Mobilidade, Identidade e Integração REST

### 🎯 Valor
Transformar o VibeEvents em uma plataforma móvel e personalizada, permitindo a geolocalização em tempo real, o gerenciamento de perfis e a abertura de dados via API para parceiros regionais.

### ✅ Tarefas
- Infraestrutura de Identidade (Auth):
  - Implementar o sistema de perfil de interesses.

- Geolocalização em Tempo Real:
  - Integrar a API de geolocalização do navegador para centrar o mapa na posição atual do usuário.

- Interface Mobile-First:
  - Adaptar o layout para dispositivos móveis com menus retráteis (Offcanvas).

- Desenvolvimento de API REST:
  - Criar endpoints para consumo de dados de eventos por aplicações externas ou mobile nativo.

---
##  Features 

#### **US-EV-10 — Localização "Onde estou?"**
**Como** usuário em movimento em Palmas  
**Quero** ver minha posição atual no mapa  
**Para** saber quais eventos estão realmente próximos de mim agora.

* **Critérios de Aceite:**
    * Dado que clico no botão de geolocalização.
    * Quando o navegador solicita e recebe permissão de GPS.
    * Então o mapa centraliza na minha posição e exibe um marcador azul pulsante.

---

#### **US-EV-11 — Interface Mobile-First**
**Como** usuário de smartphone  
**Quero** navegar pelos eventos sem que a barra lateral ocupe toda a minha tela  
**Para** visualizar o mapa de forma confortável em dispositivos móveis.

* **Critérios de Aceite:**
    * Dado que acesso a plataforma via dispositivo móvel.
    * Quando o mapa carrega, a barra lateral fica oculta em um menu "Offcanvas".
    * Então o mapa ocupa 100% da área visível da tela.

---

#### **US-EV-14 — Onboarding de Interesses**
**Como** usuário logado  
**Quero** selecionar meus interesses no primeiro acesso  
**Para** receber recomendações personalizadas.

* **Critérios de Aceite:**
    * Dado que realizo meu primeiro login.
    * Quando seleciono categorias como "Esporte" ou "Música".
    * Então o mapa carrega preferencialmente eventos que coincidem com minhas escolhas.

---

#### **US-EV-15 — "Quanto tempo falta?"**
**Como** usuário em movimento em Palmas  
**Quero** ver a distância em quilômetros e o tempo estimado de deslocamento até um evento ao clicar no marcador  
**Para** decidir se vale a pena me deslocar até lá agora.

* **Critérios de Aceite:**
    * **Cálculo Automático:** Ao abrir o popup de um evento, o sistema deve calcular a distância entre o `userMarker` (posição atual) e o marcador do evento.
    * **Exibição no Popup:** O popup deve exibir a distância (ex: `"2.5 km de você"`).
    * **Tempo Estimado:** Exibir uma estimativa simples baseada em uma velocidade média urbana (ex: `40 km/h` para carros ou `15 km/h` para bicicletas).
    * **Atualização Dinâmica:** Se o usuário clicar no botão de geolocalização e sua posição mudar, os cálculos nos popups devem ser atualizados.

---

## 📌 DIVISÃO DAS TAREFAS

### 3ª Sprint - Mobilidade e API

| Atividade | Feature | Autor | Revisor |
| :--- | :--- | :--- | :--- |
| Configuração do Django Rest Framework (DRF) | US-API-01 | cristian | g. marques |
| Implementação de GPS e Centralização de Mapa | US-EV-10 | cristian | vinicius |
| CSS Responsivo e Menu Offcanvas (Mobile) | US-EV-11 | vinicius | g. marques |
| Sistema de Login e Modelagem de Perfil/Interesses | US-EV-14 | laurinda | vinicius |
| Endpoint de Detalhes do Evento e Filtros via API | US-API-01 | cristian | g. marques |
| Cálculo de Distância e Tempo Estimado até Eventos | US-EV-15 | vinicius | cristian |


### 📌 Sprint 4 — Consolidação Mobile e Ecossistema Comunitário


### 🎯 Valor
Converter o VibeEvents em uma experiência de aplicativo nativo via PWA, estabelecendo um ecossistema de interação social e governança de dados. A sprint foca em transformar o usuário de um espectador passivo em um colaborador ativo, garantindo a integridade da plataforma através de curadoria autenticada e automação do ciclo de vida dos eventos.

### ✅ Tarefas
- Conversão PWA e Interface Adaptativa:
  - Implementar manifesto e Service Workers para instalação mobile.
  - Desenvolver suporte a Dark Mode.
  - Criar visualização alternativa em lista.

- Sistema de Autenticação e Perfil:
  - Consolidar o fluxo de registro opcional, login e gerenciamento de conta.

- Ferramentas de Engajamento e Rota:
  - Integrar o sistema de presença ("Eu Vou").
  - Implementar compartilhamento otimizado para redes sociais.
  - Adicionar integração com aplicativos de navegação externa (Google Maps/Waze).

- Módulo de Conteúdo e Feedback:
  - Desenvolver mural de fotos.
  - Criar sistema de comentários moderados.
  - Integrar previsão meteorológica em tempo real.

- Gestão de Ciclo de Vida e Curadoria:
  - Implementar pipeline de aprovação de eventos vinculados a autores.
  - Desenvolver serviço de limpeza automática para eventos finalizados há mais de 24 horas.
 
##  Features 


#### **US-EV-16 — Registro e Login Opcional**
**Como** usuário do VibeEvents Palmas  
**Quero** ter a opção de criar uma conta ou navegar como convidado  
**Para** acessar funcionalidades sociais sem ser obrigado a logar logo de cara.

* **Critérios de Aceite:**
    * O sistema deve permitir login via e-mail/senha.
    * Usuários não autenticados devem conseguir visualizar o mapa normalmente.
    * Ao clicar em uma função restrita (ex: confirmar presença), o sistema deve redirecionar para a tela de login.

---

#### **US-EV-18 — Dark Mode Automático**
**Como** usuário que utiliza o app à noite nos eventos  
**Quero** que a interface se adapte ao modo escuro do meu celular  
**Para** economizar bateria e não cansar a vista.

* **Critérios de Aceite:**
    * O CSS deve usar `@media (prefers-color-scheme: dark)`.
    * O estilo do mapa (Leaflet) deve alternar para uma camada escura (ex: CartoDB Dark Matter).

---

#### **US-EV-19 — Integração com Rotas (Ir agora)**
**Como** usuário que decidiu ir a um evento  
**Quero** um botão que abra o GPS do meu celular com a rota traçada  
**Para** chegar ao local sem precisar digitar o endereço manualmente.

* **Critérios de Aceite:**
    * O botão deve identificar se o usuário está no Android (Google Maps) ou iOS (Apple Maps).
    * As coordenadas exatas do evento devem ser passadas via URL Scheme.

---

#### **US-EV-20 — Contador de "Eu Vou"**
**Como** usuário que busca os "rolês" mais badalados  
**Quero** ver quantas pessoas confirmaram presença em um evento  
**Para** entender o nível de engajamento daquela atividade.

* **Critérios de Aceite:**
    * Botão `"Vou nesse!"` visível apenas para usuários logados.
    * Contador atualizado via AJAX (sem recarregar a página).

---

#### **US-EV-21 — Compartilhamento Inteligente**
**Como** organizador ou entusiasta  
**Quero** compartilhar o evento via WhatsApp com um "card" visual  
**Para** convidar amigos de forma atrativa.

* **Critérios de Aceite:**
    * Configuração de tags `og:image` e `og:title` dinâmicas.
    * O link gerado deve conter o ID do evento para abrir o mapa já focado nele.

---

#### **US-EV-22 — foto do evento**
**Como** criador de um evento   
**Quero** subir fotos do evento  
**Para** mostrar o clima do evento para outros usuários no mapa.

* **Critérios de Aceite:**
    * O sistema deve solicitar acesso ao armazenamento.
    * As fotos devem ser exibidas em um carrossel nos detalhes do evento.

---

#### **US-EV-23 — Comentários e Avaliações**
**Como** usuário com dúvidas ou feedbacks  
**Quero** deixar um comentário na página do evento  
**Para** interagir com o organizador e outros participantes.

* **Critérios de Aceite:**
    * Exibição de nome e data do comentário.
    * Filtro de palavras ofensivas básico.

---

#### **US-EV-24 — Previsão do Tempo para Palmas**
**Como** usuário planejando um evento ao ar livre  
**Quero** ver a previsão do tempo no detalhe do evento  
**Para** saber se devo levar guarda-chuva ou protetor solar.

* **Critérios de Aceite:**
    * Integração com API de clima (ex: OpenWeather).
    * Exibição de temperatura e condição climática para o dia do evento.

---

#### **US-EV-25 — Lista de Eventos (View Alternativa)**
**Como** usuário que prefere uma navegação rápida por texto e imagem  
**Quero** alternar do modo mapa para o modo lista  
**Para** ver os eventos ordenados por data ou proximidade.

* **Critérios de Aceite:**
    * Cards contendo imagem, título e distância.
    * Botão de `"toggle"` (Mapa/Lista) persistente na interface.

---

#### **US-EV-27 — Ciclo de Vida do Evento (Sugestão & Curadoria)**
**Como** organizador ou membro da comunidade  
**Quero** sugerir um evento para que o curador aprove  
**Para** manter o mapa atualizado e com informações auditadas.

* **Critérios de Aceite:**
    * O usuário logado sugere o evento e o Curador aprova.
    * O evento deve transicionar entre os novos status: `Pendente`, `Futuro`, `Acontecendo` e `Finalizado`.

---

#### **US-EV-28 — Transformação em PWA (App Mobile)**
**Como** usuário que frequenta eventos na cidade  
**Quero** instalar o VibeEvents na tela inicial do meu celular  
**Para** acessá-lo rapidamente como um aplicativo nativo, sem digitar URLs.

* **Critérios de Aceite:**
    * Configuração de `manifest.json` com ícones do VibeEvents.
    * O app deve abrir em modo `"standalone"` (sem barras de navegação do browser).
    * Uso de Service Workers para carregar o mapa básico mesmo em conexões lentas de Palmas.

---

#### **US-EV-29 — Gestão de Perfil Mobile-Responsive**
**Como** membro da comunidade VibeEvents  
**Quero** editar meus dados e interesses em uma tela otimizada para celular  
**Para** manter meu perfil atualizado e minhas recomendações precisas.

* **Critérios de Aceite:**
    * Botões e campos com tamanho mínimo de `44px` para facilitar o toque.
    * Possibilidade de alterar a lista de interesses definida na US-EV-14.

---

#### **US-EV-30 — Faxina Automática (Cleanup Service)**
**Como** curador da plataforma  
**Quero** que o sistema arquive automaticamente eventos passados  
**Para** manter o mapa limpo e otimizar a renderização de marcadores ativos.

* **Critérios de Aceite:**
    * Criação de uma rotina (`management command`) que verifica eventos cujo término ocorreu há mais de `24 horas`.
    * O mapa só deve renderizar eventos com status `Futuro` ou `Acontecendo`, removendo os `Finalizados` após 24h do término.

---

### 📌 Divisão de Tarefas — Sprint 4

| Integrante | Atividade / Feature | Código da US |
| :--- | :--- | :--- |
|  **Cristian: Identidade e App** | Registro e Login Opcional (Navegação como convidado e controle de restrições) | US-EV-16 |
|  | Transformação em PWA (App Mobile standalone, manifest.json e Service Workers) | US-EV-28 |
|  | Gestão de Perfil Mobile-Responsive (Ajuste de inputs ≥ 44px e interesses) | US-EV-29 |
|  | Dark Mode Automático (Media queries e camadas do CartoDB Dark Matter) | US-EV-18 |
|  **Vinicius: Engenheiro Social** | Integração com Rotas (Abertura automatizada do Google Maps/Apple Maps via GPS) | US-EV-19 |
|  | Contador de "Eu Vou" (Controle de presenças interativo atualizado via AJAX) | US-EV-20 |
|  | Compartilhamento Inteligente (Configuração de OpenGraph dinâmico para WhatsApp) | US-EV-21 |
|  **Gabryel: Curador de Conteúdo** | Mural de Fotos (Acesso à câmera do celular e carrossel de detalhes) | US-EV-22 |
|  | Comentários e Avaliações (Sistema de comentários com filtro de palavras básicas) | US-EV-23 |
|  | Previsão do Tempo para Palmas (Integração e exibição com a API OpenWeather) | US-EV-24 |
|  **Laura: Retenção e Business** | Lista de Eventos (Visualização em lista alternativa paralela ao mapa com toggle) | US-EV-25 |
|  | Ciclo de Vida do Evento (Estados temporais: Pendente, Futuro, Acontecendo, Finalizado) | US-EV-27 |
|  | Faxina Automática (Management command de limpeza e arquivamento de dados passados) | US-EV-30 |


