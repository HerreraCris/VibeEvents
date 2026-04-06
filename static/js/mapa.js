const initMap = (containerId, eventosData) => {
    // Centraliza o mapa (Ajuste as coordenadas iniciais se necessário)
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
            const coords = evento.localizacao.coordinates; // [longitude, latitude]
            const lat = coords[1];
            const lng = coords[0];
            
            const markerIcon = icons[evento.categoria] || icons['CULT']; 
            const marker = L.marker([lat, lng], { icon: markerIcon }).addTo(map);
            
            // Criamos um ID único para o elemento de endereço do popup
            const addressId = `addr-${Math.random().toString(36).substr(2, 9)}`;

            marker.bindPopup(`
                <div class="map-popup">
                    <h3 style="margin-bottom: 5px;">${evento.nome}</h3>
                    <p style="color: #666; font-size: 0.9em; margin-top: 0;">${evento.nome_local}</p>

                    <p><b>📅 Data:</b> ${new Date(evento.data_evento).toLocaleString('pt-BR')}</p>
                    <p><b>📝 Descrição:</b><br>${evento.descricao}</p>

                    <p><b>📍 Endereço:</b><br>
                        <span id="${addressId}" style="font-style: italic; color: #555;">Buscando endereço...</span>
                    </p>

                    <button class="vibe-button" 
                        style="width: 100%; margin-top: 10px; cursor: pointer;"
                        onclick="window.open('${evento.link_externo}', '_blank')">
                        Garantir Ingresso
                    </button>
                </div>
            `);

            // Evento disparado quando o popup abre: busca o endereço via API
            marker.on('popupopen', function() {
                fetch(`https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lng}`)
                    .then(response => response.json())
                    .then(data => {
                        const addressElement = document.getElementById(addressId);
                        if (addressElement) {
                            // Pega o endereço formatado ou uma mensagem de erro amigável
                            addressElement.innerText = data.display_name || "Endereço não identificado";
                        }
                    })
                    .catch(() => {
                        const addressElement = document.getElementById(addressId);
                        if (addressElement) addressElement.innerText = "Erro ao carregar endereço.";
                    });
            });
        }
    });
};