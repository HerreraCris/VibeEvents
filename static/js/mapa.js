    let allMarkers = []; 
    let leafletMap;      
    let userMarker;

    // --- SISTEMA GLOBAL DE FAVORITOS ---
    window.getFavoritos = () => JSON.parse(localStorage.getItem('vibe_favs')) || [];

    window.gerenciarFavoritoMapa = (eventoId) => {
        let favs = window.getFavoritos();
        const idStr = eventoId.toString();

        if (favs.includes(idStr)) {
            favs = favs.filter(id => id !== idStr);
        } else {
            favs.push(idStr);
        }
        localStorage.setItem('vibe_favs', JSON.stringify(favs));
        
        // Chama a função do HTML para atualizar a tela
        if (typeof filterChange === "function") {
            filterChange();
        }
    };

    const obterInfoProximidade = (latlngEvento) => {
        if (!userMarker) return ""; 

        const userLatLng = userMarker.getLatLng();
        const distanciaMetros = userLatLng.distanceTo(latlngEvento);
        const distanciaKm = (distanciaMetros / 1000).toFixed(1);

        // Estimativa baseada em 40km/h (média em Palmas)
        const tempoMinutos = Math.round((distanciaKm / 40) * 60);

        return `
            <div style="margin-top: 8px; padding-top: 8px; border-top: 1px dashed #ccc; color: #007bff; font-weight: bold; font-size: 0.8rem;">
                <i class="bi bi-geo-alt-fill"></i> ${distanciaKm} km de você <br>
                <i class="bi bi-clock-history"></i> ~${tempoMinutos < 1 ? '1' : tempoMinutos} min de deslocamento
            </div>
        `;
    };

    const initMap = (containerId, eventosData) => {
        if (leafletMap !== undefined && leafletMap !== null) {
            leafletMap.remove();
        }

        leafletMap = L.map(containerId).setView([-10.18, -48.33], 13); 

        // --- GERENCIAMENTO DINÂMICO DE TEMA (US-EV-18) ---
        let temaSalvo = localStorage.getItem('vibe_theme');
        let isDarkMode = temaSalvo === 'dark' || 
            (!temaSalvo && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);

        let tileLayerUrl = isDarkMode 
            ? 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
            : 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
            
        let tileAttribution = isDarkMode 
            ? '© OpenStreetMap contributors, © CARTO' 
            : '© OpenStreetMap contributors';

        L.tileLayer(tileLayerUrl, {
            maxZoom: 19,
            attribution: tileAttribution
        }).addTo(leafletMap);

        document.body.classList.toggle('dark-mode-active', isDarkMode);

        // --- UNIFICAÇÃO DOS LISTENERS DE TEMA ---
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
                if (!localStorage.getItem('vibe_theme')) {
                    location.reload(); 
                } else if (typeof filterChange === "function") { 
                    filterChange(); 
                }
            });
        }

        // --- FUNÇÃO GLOBAL DO BOTÃO DE INTERNVEÇÃO MANUAL ---
        window.alternarTemaManual = () => {
            let atualmenteEscuro = document.body.classList.contains('dark-mode-active');
            localStorage.setItem('vibe_theme', atualmenteEscuro ? 'light' : 'dark');
            location.reload(); 
        };

        // --- CONFIGURAÇÃO DE EVENTOS DE LOCALIZAÇÃO (GPS) ---
        leafletMap.on('locationfound', (e) => {
            if (userMarker) {
                leafletMap.removeLayer(userMarker);
            }

            const userIcon = L.divIcon({
                className: 'user-location-marker',
                iconSize: [15, 15]
            });

            userMarker = L.marker(e.latlng, { icon: userIcon }).addTo(leafletMap)
                .bindPopup("Você está aqui!").openPopup();
        });

        leafletMap.on('locationerror', (e) => {
            alert("Não foi possível acessar sua localização. Verifique as permissões do navegador.");
            console.log("Erro de GPS:", e.message);
        });

        try {
            L.Control.geocoder({
                defaultMarkGeocode: false,
                placeholder: "Buscar bairro ou local...",
                errorMessage: "Não encontrado."
            })
            .on('markgeocode', function(e) {
                leafletMap.fitBounds(e.geocode.bbox);
            })
            .addTo(leafletMap);
        } catch (e) { console.log("Erro geocoder:", e); }

        const iconBase = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-"; 
        const icons = {
            'EMPR': L.icon({ iconUrl: iconBase + 'gold.png', shadowSize: [41, 41], iconSize: [25, 41], iconAnchor: [12, 41] }), 
            'ESPO': L.icon({ iconUrl: iconBase + 'green.png', shadowSize: [41, 41], iconSize: [25, 41], iconAnchor: [12, 41] }),
            'MUSI': L.icon({ iconUrl: iconBase + 'red.png', shadowSize: [41, 41], iconSize: [25, 41], iconAnchor: [12, 41] }), 
            'CULT': L.icon({ iconUrl: iconBase + 'blue.png', shadowSize: [41, 41], iconSize: [25, 41], iconAnchor: [12, 41] }), 
        };

        allMarkers = []; 
        eventosData.forEach(evento => {
            if (evento.localizacao && evento.localizacao.coordinates) { 
                const coords = evento.localizacao.coordinates; 
                const markerIcon = icons[evento.categoria] || icons['CULT']; 
                const marker = L.marker([coords[1], coords[0]], { icon: markerIcon }); 

                const addressId = `addr-${Math.random().toString(36).substr(2, 9)}`; 
                const interesses = window.VIBE_INTERESSES || [];
                if (interesses.length > 0) {
                    if (!interesses.includes(evento.categoria)) {
                        marker.setOpacity(0.4); 
                    } else {
                        marker.setZIndexOffset(1000); 
                    }
                }
                marker.eventoData = evento; 

                const getPopupContent = () => {
                    const favs = window.getFavoritos();
                    const isFav = favs.includes(evento.id.toString());
                    const proximidadeHtml = obterInfoProximidade([coords[1], coords[0]]);
                    return `
                        <div class="map-popup" style="color: #0b0f19; min-width: 220px;">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                                <h5 style="margin: 0; font-weight: bold;">${evento.nome}</h5>
                                <button class="btn-favorito ${isFav ? 'is-fav' : ''}" onclick="window.gerenciarFavoritoMapa('${evento.id}')">
                                    <i class="bi ${isFav ? 'bi-heart-fill' : 'bi-heart'}"></i>
                                </button>
                            </div>
                            <div style="margin: 8px 0 5px; font-size: 0.9rem;">
                                🗓️ <b>${new Date(evento.data_evento).toLocaleDateString('pt-BR')}</b>
                            </div>
                            
                            ${proximidadeHtml}

                            <p style="font-size: 0.75rem; color: #666; border-top: 1px solid #eee; padding-top: 8px; margin-top: 5px;">
                                <b>Endereço:</b><br><span id="${addressId}">Carregando...</span>
                            </p>
                            <hr>
                            <div style="margin-top: 10px;">
                                <h6 style="font-size: 0.9rem;">Comentários</h6>
                                <div id="comentarios-${evento.id}" style="max-height: 150px; overflow-y: auto; margin-bottom: 8px; font-size: 0.8rem;">
                                    ${(evento.comentarios || []).map(c => `
                                        <div style="border-bottom:1px solid #ddd; padding:6px 0;">
                                            <b>${c.usuario}</b>
                                            <small style="display:block; color:#777;">${c.data}</small>
                                            ${c.texto}
                                        </div>
                                    `).join('')}
                                </div>
                                <hr>
                                <a href="/evento/${evento.id}/" class="btn btn-outline-primary btn-sm w-100 mt-2">
                                    Ver detalhes do evento
                                </a>
                            </div>
                        </div>`;
                };
                marker.bindPopup(getPopupContent, { maxWidth: 300 });

                marker.on('popupopen', function() {
                    marker.setPopupContent(getPopupContent());
                    fetch(`https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${coords[1]}&lon=${coords[0]}`) 
                        .then(r => r.json()) 
                        .then(data => {
                            const el = document.getElementById(addressId); 
                            if (el) el.innerText = data.display_name || "Endereço não identificado"; 
                        });
                });

                marker.addTo(leafletMap); 
                allMarkers.push(marker); 
            }
        });
    };
    window.aplicarFiltros = (categoriaSelecionada, apenasSolidarios, apenasFavoritos = false) => {
        if (!leafletMap) return;
        const favs = window.getFavoritos();
        const eventosFiltrados = []; 

        allMarkers.forEach(marker => {
            const ev = marker.eventoData;
            const bateCategoria = (categoriaSelecionada === 'ALL' || ev.categoria === categoriaSelecionada);
            const bateSolidario = (!apenasSolidarios || ev.is_beneficente === true);
            const bateFavorito = (!apenasFavoritos || favs.includes(ev.id.toString()));

            if (bateCategoria && bateSolidario && bateFavorito) {
                if (!leafletMap.hasLayer(marker)) marker.addTo(leafletMap);
                eventosFiltrados.push(ev); 
            } else {
                if (leafletMap.hasLayer(marker)) leafletMap.removeLayer(marker);
            }
        });
        renderizarLista(eventosFiltrados);
    }
    // Função para encontrar o usuário
    window.localizarUsuario = () => {
        if (!leafletMap) return;

        leafletMap.locate({ 
            setView: true, 
            maxZoom: 16, 
            enableHighAccuracy: true, 
            timeout: 10000,          
            maximumAge: 0            
        });
    };


    function toggleView(view) {
        const mapDiv = document.getElementById('map');
        const listDiv = document.getElementById('lista-eventos-container');
        const btnMap = document.getElementById('view-map-btn');
        const btnList = document.getElementById('view-list-btn');

        if (view === 'list') {
            mapDiv.classList.add('d-none');
            listDiv.classList.remove('d-none');
            btnList.classList.add('active');
            btnMap.classList.remove('active');
            
            if (window.aplicarFiltros) {
                const isSolidario = document.querySelector('#filter-solidario:checked') !== null;
                window.aplicarFiltros(currentCategory, isSolidario, apenasFavoritos);
            }
        } else {
            listDiv.classList.add('d-none');
            mapDiv.classList.remove('d-none');
            btnMap.classList.add('active');
            btnList.classList.remove('active');
            
            setTimeout(() => {
                if (leafletMap) leafletMap.invalidateSize();
            }, 100);
        }
    }

    function renderizarLista(dadosParaExibir) {
        const wrapper = document.getElementById('cards-wrapper');
        if (!wrapper) return;
        
        wrapper.innerHTML = '';
        let lista = dadosParaExibir;
        if (!lista) {
            const dataEl = document.getElementById('eventos-data');
            lista = dataEl ? JSON.parse(dataEl.textContent) : [];
        }
        

        if (lista.length === 0) {
            wrapper.innerHTML = `<div class="col-12 text-center text-muted py-5">Nenhum evento encontrado com esses filtros em Palmas.</div>`;
            return;
        }

        lista.forEach(evento => {
            const coords = evento.localizacao.coordinates;
            const infoProximidade = obterInfoProximidade([coords[1], coords[0]]);
            const dataObj = new Date(evento.data_evento);
            const dataFormatada = dataObj.toLocaleDateString('pt-BR');
            const horarioFormatado = dataObj.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
            wrapper.innerHTML += `
                    <div class="col-12 col-md-6 col-lg-4">
                        <div class="event-card h-100 p-3 shadow-sm" style="background: #1e2533; border-radius: 15px; border: 1px solid #2d3748;">
                            <img src="${evento.imagem || '/static/img/default-event.jpg'}" 
                                class="card-img-top mb-3" 
                                style="height: 160px; object-fit: cover; border-radius: 10px;">
                            
                            <div class="card-body p-0">
                                <h5 class="card-title text-white h6 mb-3 fw-bold">${evento.nome}</h5>
                                
                                <div class="d-flex gap-3 mb-2" style="font-size: 0.85rem; color: #94a3b8;">
                                    <span><i class="bi bi-calendar3 me-1 text-primary"></i> ${dataFormatada}</span>
                                    <span><i class="bi bi-clock me-1 text-primary"></i> ${horarioFormatado}</span>
                                </div>

                                <div class="mb-2" style="font-size: 0.85rem; color: #94a3b8;">
                                    <i class="bi bi-geo-alt me-1 text-danger"></i> 
                                    <strong>${evento.nome_local || 'Local não informado'}</strong>
                                </div>

                                <div class="proximidade-container mb-3" style="font-size: 0.8rem; color: #7dacfd;">
                                    ${infoProximidade}
                                </div>

                                <button class="btn btn-primary btn-sm w-100 mt-2 py-2" 
                                        style="border-radius: 10px; font-weight: bold;"
                                        onclick="toggleView('map'); setTimeout(() => { leafletMap.setView([${coords[1]}, ${coords[0]}], 16); }, 200);">
                                    VER NO MAPA
                                </button>
                            </div>
                        </div>
                    </div>
                `;
            });
    }

window.enviarComentario = function(eventoId) {
    const textoInput = document.getElementById(`texto-comentario-${eventoId}`);
    const texto = textoInput.value.trim();

    if (!texto) {
        alert("Digite um comentário antes de enviar.");
        return;
    }

    fetch(`/evento/${eventoId}/comentar/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: `texto=${encodeURIComponent(texto)}`
    })

    .then(response => {
        if (response.redirected) {
            alert("Você precisa estar logado para comentar.");
            return null;
        }

        return response.json().then(data => ({
            status: response.status,
            body: data
        }));
    })
    .then(result => {
        if (!result) return;

        if (result.status !== 200) {
            alert(result.body.erro || "Não foi possível enviar seu comentário.");
            return;
        }


        const data = result.body;
        const container = document.getElementById(`comentarios-${eventoId}`);

        container.innerHTML = data.comentarios.map(c => `
            <div style="border-bottom:1px solid #ddd; padding:6px 0;">
                <b>${c.usuario}</b>
                <small style="display:block; color:#777;">${c.data}</small>
                ${c.texto}
            </div>
        `).join('');

        allMarkers.forEach(marker => {
            if (marker.eventoData.id == eventoId) {
                marker.eventoData.comentarios = data.comentarios;
            }
        });

        textoInput.value = '';
    })
    .catch(error => {
        console.error(error);
        alert("Falha na conexão. Tente novamente.");
    });
};


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}