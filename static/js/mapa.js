let allMarkers = []; 
let leafletMap;      

const initMap = (containerId, eventosData) => {
    // 1. Limpeza do mapa anterior
    if (leafletMap !== undefined && leafletMap !== null) {
        leafletMap.remove();
    }

    // 2. Inicialização do Mapa
    leafletMap = L.map(containerId).setView([-10.18, -48.33], 13); 
    
    L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', { 
        maxZoom: 20, 
        attribution: '© Stadia Maps' 
    }).addTo(leafletMap); 

    // 3. Adição da Busca (US-EV-06) - Colocamos dentro de um try/catch para não quebrar os pins se ela falhar
    try {
        const geocoder = L.Control.geocoder({
            defaultMarkGeocode: false,
            placeholder: "Buscar bairro ou local...",
            errorMessage: "Não encontrado."
        })
        .on('markgeocode', function(e) {
            const bbox = e.geocode.bbox;
            const poly = L.polygon([
                bbox.getSouthEast(),
                bbox.getNorthEast(),
                bbox.getNorthWest(),
                bbox.getSouthWest()
            ]);
            leafletMap.fitBounds(poly.getBounds());
        })
        .addTo(leafletMap);
    } catch (e) {
        console.log("Erro ao carregar buscador, mas seguindo com os pins...", e);
    }

    // 4. Configuração de Ícones
    const iconBase = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-"; 
    const icons = {
        'EMPR': L.icon({ iconUrl: iconBase + 'gold.png', shadowSize: [41, 41], iconSize: [25, 41], iconAnchor: [12, 41] }), 
        'ESPO': L.icon({ iconUrl: iconBase + 'green.png', shadowSize: [41, 41], iconSize: [25, 41], iconAnchor: [12, 41] }),
        'MUSI': L.icon({ iconUrl: iconBase + 'red.png', shadowSize: [41, 41], iconSize: [25, 41], iconAnchor: [12, 41] }), 
        'CULT': L.icon({ iconUrl: iconBase + 'blue.png', shadowSize: [41, 41], iconSize: [25, 41], iconAnchor: [12, 41] }), 
    };

    // 5. Renderização dos Pins (Os eventos do banco)
    allMarkers = []; // Resetar a lista antes de preencher
    eventosData.forEach(evento => {
        if (evento.localizacao && evento.localizacao.coordinates) { 
            const coords = evento.localizacao.coordinates; 
            const markerIcon = icons[evento.categoria] || icons['CULT']; 
            
            // O GeoJSON usa [Longitude, Latitude], o Leaflet usa [Latitude, Longitude]
            const marker = L.marker([coords[1], coords[0]], { icon: markerIcon }); 

            marker.eventoData = evento; 
            
            const addressId = `addr-${Math.random().toString(36).substr(2, 9)}`; 
            marker.bindPopup(`
                <div class="map-popup">
                    <h3 style="margin-bottom: 5px; color: white;">${evento.nome}</h3> 
                    <p style="color: #bbb; font-size: 0.9em; margin-top: 0;">${evento.nome_local}</p> 
                    ${evento.is_beneficente ? '<span class="badge bg-success mb-2" style="color: white">❤️ Evento Solidário</span>' : ''}
                    <p style="color: white;"><b>📅 Data:</b> ${new Date(evento.data_evento).toLocaleString('pt-BR')}</p> 
                    <p style="color: white;"><b>📍 Endereço:</b><br><span id="${addressId}" style="font-style: italic; color: #aaa;">Buscando...</span></p> 
                    <button class="vibe-button" onclick="window.open('${evento.link_externo}', '_blank')">Garantir Ingresso</button> 
                </div>
            `); 

            marker.on('popupopen', function() {
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