let allMarkers = []; // Lista global para controle dos pins
let leafletMap;      // Instância global do mapa

const initMap = (containerId, eventosData) => {
    // 1. LIMPEZA: Se o mapa já existir, remova-o antes de criar de novo
    if (leafletMap !== undefined && leafletMap !== null) {
        leafletMap.remove();
    }

    // 2. INICIALIZAÇÃO DO MAPA (Palmas)
    leafletMap = L.map(containerId).setView([-10.18, -48.33], 13); 
    
    L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', { 
        maxZoom: 20, 
        attribution: '© Stadia Maps' 
    }).addTo(leafletMap); 

    // 3. BUSCA POR LOCALIZAÇÃO (US-EV-06)
    try {
        L.Control.geocoder({
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
        console.log("Erro ao carregar buscador:", e);
    }

    // 4. ÍCONES POR CATEGORIA
    const iconBase = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-"; 
    const icons = {
        'EMPR': L.icon({ iconUrl: iconBase + 'gold.png', shadowSize: [41, 41], iconSize: [25, 41], iconAnchor: [12, 41] }), 
        'ESPO': L.icon({ iconUrl: iconBase + 'green.png', shadowSize: [41, 41], iconSize: [25, 41], iconAnchor: [12, 41] }),
        'MUSI': L.icon({ iconUrl: iconBase + 'red.png', shadowSize: [41, 41], iconSize: [25, 41], iconAnchor: [12, 41] }), 
        'CULT': L.icon({ iconUrl: iconBase + 'blue.png', shadowSize: [41, 41], iconSize: [25, 41], iconAnchor: [12, 41] }), 
    };

    // 5. RENDERIZAÇÃO DOS EVENTOS
    allMarkers = []; 
    eventosData.forEach(evento => {
        if (evento.localizacao && evento.localizacao.coordinates) { 
            const coords = evento.localizacao.coordinates; 
            const markerIcon = icons[evento.categoria] || icons['CULT']; 
            
            // Inversão de coordenadas (GeoJSON [Lon, Lat] -> Leaflet [Lat, Lon])
            const marker = L.marker([coords[1], coords[0]], { icon: markerIcon }); 

            marker.eventoData = evento; 
            const addressId = `addr-${Math.random().toString(36).substr(2, 9)}`; 

            // POP-UP CORRIGIDO (Texto visível e variáveis certas)
            marker.bindPopup(`
                <div class="map-popup" style="color: #0b0f19; min-width: 200px;">
                    <h5 style="margin-bottom: 8px; font-weight: bold; color: #0b0f19;">${evento.nome}</h5> 
                    
                    <div style="margin-bottom: 5px; font-size: 0.9rem;">
                        <span>🗓️</span> <b>${new Date(evento.data_evento).toLocaleDateString('pt-BR')}</b>
                    </div>

                    <div style="margin-bottom: 10px; font-size: 0.9rem;">
                        <span>📍</span> <span style="color: #444;">${evento.nome_local}</span>
                    </div>

                    ${evento.is_beneficente ? '<div style="color: #198754; font-weight: bold; font-size: 0.85rem; margin-bottom: 10px;">❤️ Evento Solidário</div>' : ''}
                    
                    <p style="font-size: 0.75rem; color: #666; border-top: 1px solid #eee; pt-2; margin-top: 5px;">
                        <b>Endereço:</b><br>
                        <span id="${addressId}">Carregando endereço...</span>
                    </p>

                    <button class="btn btn-sm w-100 mt-2" 
                            style="background-color: #7DACFD; color: #0b0f19; font-weight: bold; border-radius: 20px;" 
                            onclick="window.open('${evento.link_externo}', '_blank')">
                        GARANTIR INGRESSO
                    </button> 
                </div>
            `, { maxWidth: 300 }); 

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

// 6. FUNÇÃO DE FILTRAGEM (Sincronizada com a Busca)
window.aplicarFiltros = (categoriaSelecionada, apenasSolidarios) => {
    if (!leafletMap) return;

    allMarkers.forEach(marker => {
        const ev = marker.eventoData;
        const bateCategoria = (categoriaSelecionada === 'ALL' || ev.categoria === categoriaSelecionada);
        const bateSolidario = (!apenasSolidarios || ev.is_beneficente === true);

        if (bateCategoria && bateSolidario) {
            if (!leafletMap.hasLayer(marker)) {
                marker.addTo(leafletMap);
            }
        } else {
            if (leafletMap.hasLayer(marker)) {
                leafletMap.removeLayer(marker);
            }
        }
    });
};