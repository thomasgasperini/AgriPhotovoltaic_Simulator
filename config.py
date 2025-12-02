"""
Configurazione centralizzata per PV Simulator
Contiene: costanti, parametri default, stili CSS, configurazioni UI
"""

from zoneinfo import ZoneInfo

# ==================== COSTANTI FISICHE ====================
HECTARE_M2 = 10000  # 1 ettaro in m²
TIMEZONE = "Europe/Rome"
TIMEZONE_OBJ = ZoneInfo(TIMEZONE)

# ==================== PARAMETRI DEFAULT ====================
DEFAULT_PARAMS = {
    # Localizzazione
    "comune": "Roma",
    "lat": 41.9,
    "lon": 12.5,
    
    # Layout pannelli
    "num_panels_per_row": 5,  # pannelli per fila (larghezza)
    "num_rows": 2,  # numero di file/righe (profondità)
    "lato_minore": 2.0,  # m - lato minore
    "lato_maggiore": 2.5,  # m - lato maggiore
    
    # Geometria installazione
    "carreggiata": 5.0,  # m - distanza tra file
    "pitch_laterale": 3.0,  # m - centro-centro pannelli
    "tilt": 30,  # gradi
    "azimuth": 180,  # gradi (Sud)
    
    # Caratteristiche elettriche
    "eff": 0.20,  # efficienza 20%
    "noct": 45.0,  # °C
    "temp_coeff": -0.004,  # %/°C
    "losses": 0.10,  # perdite di sistema 10%
    "albedo": 0.2,  # riflettanza del suolo
    
    # Superficie terreno
    "hectares": 1.0,  # ettari totali del campo
}

# ==================== COLORI TEMA ====================
COLORS = {
    "primary": "#74a65b",
    "secondary": "#a3c68b",
    "accent": "#f7e08e",
    "warning": "#f39c12",
    "danger": "#e74c3c",
    "info": "#3498db",
    "white": "#ffffff",
    "text": "#000000",
    "light_bg": "#f8f9fa",
}

# ==================== CONFIGURAZIONE GRAFICI ====================
CHART_CONFIG = {
    "fig_height": 4,
    "fig_width_min": 10,
    "fig_width_max": 14,
    "screen_width_fallback": 1200,
    "map_height_mobile": 300,
    "map_height_desktop": 400,
}

# ==================== MESSAGGI UI ====================
MESSAGES = {
    "location_not_found": "Comune non trovato",
    "location_success": "Coordinate: {lat:.4f} °N, {lon:.4f}°E",
}

# ==================== CONFIGURAZIONE PAGINA ====================
PAGE_CONFIG = {
    "page_title": "Analisi Produzione Fotovoltaico",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# ==================== ASSETS ====================
LOGO_URL = "http://www.resfarm.it/wp-content/uploads/2025/02/Logo_Resfarm_home_white.svg#121"

# ==================== CSS GLOBALE ====================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

/* ===== RESET BASE ===== */
* { box-sizing: border-box; }
html { font-size: 16px; overflow-x: hidden; }
body, :root, div[data-testid="stAppViewContainer"], 
div[data-testid="stAppViewContainer"] > .main, 
div[data-testid="stSidebar"] {
    background-color: white !important;
    font-family: 'Inter', sans-serif;
    color: #000 !important;
    line-height: 1.5;
}

/* ===== LAYOUT PRINCIPALE ===== */
.main, section.main, [data-testid="stAppViewContainer"] .main,
section.main > div, section.main > div > div,
.main .block-container, .appview-container .main .block-container {
    width: 100% !important;
    max-width: none !important;
    padding: clamp(0.5rem, 2vw, 1.5rem) !important;
    margin: 0 !important;
    transition: none !important;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    min-width: 250px !important;
}

[data-testid="stSidebar"] > div:first-child {
    display: flex !important;
    flex-direction: column;
    align-items: stretch !important;
    padding: 0 clamp(0.5rem, 2vw, 1rem) clamp(0.5rem, 2vw, 1rem) !important;  /* <--- MODIFICA: 0 top, poi right, bottom */
}


/* Sidebar responsive width */
@media screen and (min-width: 1200px) {
    [data-testid="stSidebar"][aria-expanded="true"] { 
        width: 380px !important;
    }
}

@media screen and (min-width: 768px) and (max-width: 1199px) {
    [data-testid="stSidebar"][aria-expanded="true"] { 
        width: 320px !important;
    }
}

@media screen and (max-width: 767px) {
    [data-testid="stSidebar"][aria-expanded="true"] { 
        width: 280px !important;
    }
    [data-testid="stSidebar"][aria-expanded="false"] { 
        margin-left: -280px !important;
    }
}

@media screen and (max-width: 480px) {
    [data-testid="stSidebar"][aria-expanded="true"] { 
        width: 100vw !important;
        max-width: 280px !important;
    }
}

/* ===== LOGO SIDEBAR ===== */
.sidebar-header-logo {
    position: relative;
    z-index: 1;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #74a65b, #f9d71c);
    border-radius: 12px;
    padding: clamp(-1.5rem, 2vw, 1rem);
    margin-bottom: 1rem;
    width: 100%;
    box-sizing: border-box;
}

.sidebar-header-logo img {
    width: 100%;
    height: auto;
    max-height: clamp(60px, 15vw, 120px);
    object-fit: contain;
    object-position: center;
    border-radius: 5px;
}

@media screen and (max-width: 480px) {
    .sidebar-header-logo {
        padding: 0.75rem;
        margin-bottom: 0.75rem;
    }
    .sidebar-header-logo img {
        max-height: 80px;
    }
}


/* ===== WIDGET SIDEBAR ===== */
[data-testid="stSidebar"] > div:first-child > * {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
}

/* Input fields responsive */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] select,
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stNumberInput input {
    font-size: clamp(0.75rem, 2vw, 0.9rem) !important;
    padding: clamp(0.3rem, 1vw, 0.5rem) !important;
}

/* ===== COLONNE AFFIANCATE NELLA SIDEBAR ===== */
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
    display: grid !important;
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 0.5rem !important;
}

[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > div,
[data-testid="stSidebar"] [data-testid="column"] {
    flex: unset !important;
    width: 100% !important;
    min-width: 0 !important;
    box-sizing: border-box !important;
}

@media screen and (max-width: 480px) {
    [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
        grid-template-columns: 1fr !important;
        gap: 0.25rem !important;
    }
}

/* ===== EXPANDER SIDEBAR ===== */
[data-testid="stSidebar"] .streamlit-expanderHeader {
    font-size: clamp(0.8rem, 2vw, 0.95rem) !important;
    padding: clamp(0.4rem, 1.5vw, 0.6rem) !important;
}

/* ===== HEADER PRINCIPALE ===== */
.main-header {
    background: linear-gradient(135deg, #74a65b 0%, #a3c68b 100%);
    padding: clamp(1rem, 3vw, 2rem);
    border-radius: clamp(8px, 2vw, 15px);
    color: white;
    margin-bottom: clamp(1rem, 3vw, 2rem);
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}
.main-header h1 { 
    font-size: clamp(1.3rem, 4vw, 2.5rem); 
    font-weight: 700; 
    margin-bottom: 0.5rem; 
    line-height: 1.2;
}
.main-header p { 
    font-size: clamp(0.85rem, 2vw, 1.1rem); 
    opacity: 0.95; 
    font-weight: 300; 
}

/* ===== CARD METRICHE ===== */
.metric-card {
    background: white; 
    padding: clamp(0.6rem, 2vw, 1rem); 
    border-radius: clamp(8px, 2vw, 12px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.08); 
    border-left: 4px solid #74a65b;
    transition: transform 0.2s, box-shadow 0.2s;
    min-height: clamp(100px, 20vw, 120px); 
    width: 100% !important;
    display: flex; 
    flex-direction: column; 
    justify-content: center; 
    text-align: center;
}
.metric-card:hover { 
    transform: translateY(-3px); 
    box-shadow: 0 8px 25px rgba(0,0,0,0.15); 
}
.metric-value { 
    font-size: clamp(1.2rem, 3.5vw, 2rem); 
    font-weight: 700; 
    color: #74a65b; 
    margin: 0.25rem 0; 
    line-height: 1.2; 
}
.metric-label { 
    font-size: clamp(0.7rem, 1.8vw, 0.85rem); 
    color: #000 !important; 
    text-transform: uppercase; 
    letter-spacing: 0.5px; 
    font-weight: 600; 
    white-space: normal;
    word-wrap: break-word;
}

.metric-description {
    font-size: clamp(0.65rem, 1.5vw, 0.75rem) !important;
    line-height: 1.3;
}

/* ===== TITOLI SEZIONE ===== */
.section-header {
    font-size: clamp(1.1rem, 2.5vw, 1.6rem); 
    font-weight: 600; 
    color: #74a65b;
    margin: clamp(1.5rem, 3vw, 3rem) 0 clamp(1rem, 2vw, 2rem) 0; 
    padding-bottom: 0.5rem; 
    border-bottom: 3px solid #74a65b;
}

/* ===== FORMULA BOX ===== */
.formula-box {
    background: #f8f9fa; 
    border-left: 4px solid #74a65b; 
    padding: clamp(0.6rem, 1.5vw, 1rem); 
    border-radius: clamp(6px, 1.5vw, 8px);
    margin: clamp(0.75rem, 2vw, 1.5rem) 0; 
    font-family: 'Courier New', monospace; 
    color: #333;
    font-size: clamp(0.7rem, 1.8vw, 0.95rem); 
    overflow-x: auto;
}

/* ===== INFO ITEM ===== */
.info-item {
    background: white;
    padding: clamp(0.25rem, 1vw, 0.5rem);
    border-radius: 4px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    font-size: clamp(0.75rem, 1.8vw, 0.9rem);
}

/* ===== PULSANTI ===== */
.stButton>button {
    width: 100% !important; 
    max-width: 300px !important; 
    min-width: 120px !important;
    margin-bottom: 1rem; 
    border-radius: clamp(6px, 1.5vw, 8px);
    background: linear-gradient(135deg, #74a65b 0%, #a3c68b 100%);
    color: white; 
    border: none; 
    padding: clamp(0.4rem, 1.5vw, 0.6rem) clamp(1rem, 2vw, 1.5rem); 
    font-weight: 600;
    font-size: clamp(0.8rem, 2vw, 1rem);
    transition: all 0.3s;
}
.stButton>button:hover { 
    transform: translateY(-2px); 
    box-shadow: 0 5px 15px rgba(116,166,91,0.4); 
}

/* ===== COLONNE RESPONSIVE ===== */
[data-testid="column"] {
    padding: clamp(0.25rem, 1vw, 0.5rem) !important;
}

@media screen and (max-width: 768px) {
    [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
    }
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
    }
}

/* ===== MAPPA ===== */
.folium-map {
    border-radius: clamp(6px, 1.5vw, 8px);
    overflow: hidden;
}

/* ===== VISUALIZZAZIONE 3D ===== */
#canvas-container {
    width: 100% !important;
    height: clamp(400px, 60vw, 600px) !important;
    border-radius: clamp(8px, 2vw, 12px) !important;
}

#info-panel, #controls {
    font-size: clamp(0.7rem, 1.8vw, 0.85rem) !important;
    padding: clamp(0.6rem, 1.5vw, 1rem) !important;
}

@media screen and (max-width: 768px) {
    #canvas-container {
        height: 400px !important;
    }
    #info-panel {
        top: 8px !important;
        left: 8px !important;
        right: 8px !important;
        padding: 0.6rem !important;
    }
    #controls {
        bottom: 8px !important;
        left: 8px !important;
        font-size: 0.7rem !important;
    }
}

@media screen and (max-width: 480px) {
    #canvas-container {
        height: 350px !important;
    }
    #info-panel h4 {
        font-size: 0.9rem !important;
    }
    #info-panel p {
        font-size: 0.7rem !important;
    }
}

/* ===== SCROLLBAR ===== */
.formula-box::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
.formula-box::-webkit-scrollbar-track {
    background: #ffffff;
    border-radius: 4px;
}
.formula-box::-webkit-scrollbar-thumb {
    background-color: #74a65b;
    border-radius: 4px;
}

/* ===== LINK ===== */
a, a:visited, a:hover, a:active { 
    color: #74a65b !important; 
    text-decoration: none; 
}

/* ===== UTILITY ===== */
.hide-on-mobile {
    display: block;
}

@media screen and (max-width: 768px) {
    .hide-on-mobile {
        display: none;
    }
}

.show-on-mobile {
    display: none;
}

@media screen and (max-width: 768px) {
    .show-on-mobile {
        display: block;
    }
}
</style>
"""