const initMap = (containerId, eventosData) => {
    const map = L.map(containerId).setView([-10.18, -48.33], 13);
    
    L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', {
        maxZoom: 20,
        attribution: '© Stadia Maps'
    }).addTo(map);

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
            const marker = L.marker([coords[1], coords[0]], { icon: markerIcon }).addTo(map);
            
            marker.bindPopup(`
                <div class="map-popup">
                    <h3>${evento.nome}</h3>
                    <p><b>Data:</b> ${new Date(evento.data_evento).toLocaleString('pt-BR')}</p>
                    <button class="vibe-button" onclick="window.open('${evento.link_externo}', '_blank')">Garantir Ingresso</button>
                </div>
            `);
        }
    });
};