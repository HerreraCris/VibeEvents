let allMarkers = []; // Lista global para controle dos pins
let leafletMap;      // Instância global do mapa
const initMap = (containerId, eventosData) => {
    // 1. LIMPEZA: Se o mapa já existir, remova-o antes de criar de novo
    if (leafletMap !== undefined && leafletMap !== null) {
        leafletMap.remove();
    }

    leafletMap = L.map(containerId).setView([-10.18, -48.33], 13); 
    
    L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', { 
        maxZoom: 20, 
        attribution: '© Stadia Maps' 
    }).addTo(leafletMap); 

    // Configuração de ícones por categoria 
    const iconBase = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-"; 
    const icons = {
        'EMPR': L.icon({ iconUrl: iconBase + 'gold.png', shadowSize: [41, 41], iconSize: [25, 41], iconAnchor: [12, 41] }), 
        'ESPO': L.icon({ iconUrl: iconBase + 'green.png', shadowSize: [41, 41], iconSize: [25, 41], iconAnchor: [12, 41] }),
        'MUSI': L.icon({ iconUrl: iconBase + 'red.png', shadowSize: [41, 41], iconSize: [25, 41], iconAnchor: [12, 41] }), 
        'CULT': L.icon({ iconUrl: iconBase + 'blue.png', shadowSize: [41, 41], iconSize: [25, 41], iconAnchor: [12, 41] }), 
    };

    eventosData.forEach(evento => {
        if (evento.localizacao) { 
            const coords = evento.localizacao.coordinates; 
            const markerIcon = icons[evento.categoria] || icons['CULT']; 
            const marker = L.marker([coords[1], coords[0]], { icon: markerIcon }); 

            // IMPORTANTE: Guardamos os dados no marcador para filtrar depois
            marker.eventoData = evento; 
            
            const addressId = `addr-${Math.random().toString(36).substr(2, 9)}`; 
            marker.bindPopup(`
                <div class="map-popup">
                    <h3 style="margin-bottom: 5px;">${evento.nome}</h3> 
                    <p style="color: #666; font-size: 0.9em; margin-top: 0;">${evento.nome_local}</p> 
                    ${evento.is_beneficente ? '<span class="badge bg-success mb-2" style="color: white">❤️ Evento Solidário</span>' : ''}
                    <p><b>📅 Data:</b> ${new Date(evento.data_evento).toLocaleString('pt-BR')}</p> 
                    <p><b>📍 Endereço:</b><br><span id="${addressId}" style="font-style: italic; color: #555;">Buscando...</span></p> 
                    <button class="vibe-button" onclick="window.open('${evento.link_externo}', '_blank')">Garantir Ingresso</button> 
                </div>
            `); 

            // Lógica de Geocodificação Reversa 
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

// FUNÇÃO DE FILTRAGEM (US-EV-02)
window.aplicarFiltros = (categoriaSelecionada, apenasSolidarios) => {
    allMarkers.forEach(marker => {
        const ev = marker.eventoData;
        
        const bateCategoria = (categoriaSelecionada === 'ALL' || ev.categoria === categoriaSelecionada);
        const bateSolidario = (!apenasSolidarios || ev.is_beneficente === true);

        if (bateCategoria && bateSolidario) {
            marker.addTo(leafletMap);
        } else {
            leafletMap.removeLayer(marker);
        }
    });
};