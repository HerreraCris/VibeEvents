let allMarkers = []; 
let leafletMap;      

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

const initMap = (containerId, eventosData) => {
    if (leafletMap !== undefined && leafletMap !== null) {
        leafletMap.remove();
    }

    leafletMap = L.map(containerId).setView([-10.18, -48.33], 13); 
    
    L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', { 
        maxZoom: 20, 
        attribution: '© Stadia Maps' 
    }).addTo(leafletMap); 

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

            marker.eventoData = evento; 
            const addressId = `addr-${Math.random().toString(36).substr(2, 9)}`; 

            // Função para gerar o HTML dinâmico do Popup (Garante que o coração atualize ao abrir)
            const getPopupContent = () => {
                const favs = window.getFavoritos();
                const isFav = favs.includes(evento.id.toString());
                return `
                <div class="map-popup" style="color: #0b0f19; min-width: 220px;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <h5 style="margin: 0; font-weight: bold; color: #0b0f19;">${evento.nome}</h5>
                        <button class="btn-favorito ${isFav ? 'is-fav' : ''}" 
                                onclick="window.toggleFavorito('${evento.id}')" 
                                style="border: none; background: none; padding: 0; cursor: pointer;">
                            <i class="bi ${isFav ? 'bi-heart-fill' : 'bi-heart'}" 
                               style="font-size: 1.2rem; color: ${isFav ? '#ff4757' : '#94a3b8'};"></i>
                        </button>
                    </div>
                    <div style="margin: 8px 0 5px; font-size: 0.9rem;">
                        <span>🗓️</span> <b>${new Date(evento.data_evento).toLocaleDateString('pt-BR')}</b>
                    </div>
                    <p style="font-size: 0.75rem; color: #666; border-top: 1px solid #eee; padding-top: 8px; margin-top: 5px;">
                        <b>Endereço:</b><br><span id="${addressId}">Carregando endereço...</span>
                    </p>
                    <button class="btn btn-sm w-100 mt-2" 
                            style="background-color: #7DACFD; color: #0b0f19; font-weight: bold; border-radius: 20px;" 
                            onclick="window.open('${evento.link_externo}', '_blank')">
                        GARANTIR INGRESSO
                    </button> 
                </div>`;
            };

            marker.bindPopup(getPopupContent, { maxWidth: 300 });

            marker.on('popupopen', function() {
                // Atualiza o conteúdo do popup toda vez que abre para pegar o estado real do favorito
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

    allMarkers.forEach(marker => {
        const ev = marker.eventoData;
        const bateCategoria = (categoriaSelecionada === 'ALL' || ev.categoria === categoriaSelecionada);
        const bateSolidario = (!apenasSolidarios || ev.is_beneficente === true);
        const bateFavorito = (!apenasFavoritos || favs.includes(ev.id.toString()));

        if (bateCategoria && bateSolidario && bateFavorito) {
            if (!leafletMap.hasLayer(marker)) marker.addTo(leafletMap);
        } else {
            if (leafletMap.hasLayer(marker)) leafletMap.removeLayer(marker);
        }
    });
};