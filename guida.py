"""
Modulo Guida - Documentazione Tecnica e Operativa del Simulatore Agrivoltaico.
Fornisce una panoramica dettagliata e professionale dei modelli di calcolo utilizzati.
"""

import streamlit as st

try:
    from config import TIMEZONE
except ImportError:
    TIMEZONE = "Europe/Rome"

# ==================== CONTENUTO DELLE TAB ====================


def tab_introduzione():
    """Contenuto per la tab Introduzione e Flusso Operativo."""
    st.markdown("""
    ### Introduzione 
    
    Il simulatore è uno strumento avanzato per l'analisi tecnico-economica di impianti agrivoltaici, 
    integrando la produzione fotovoltaica con l'agricoltura sostenibile. Permette di valutare simultaneamente:
    
    - **Prestazioni energetiche** dell'impianto fotovoltaico
    - **Impatto agronomico** sulle colture sottostanti
    - **Ottimizzazione geometrica** del layout

    Il simulatore si basa su quattro pilastri:
    
    ###### 1. Modellazione Solare
    Algoritmi validati calcolano:
    - Posizione del sole (elevazione e azimuth) in funzione di coordinate geografiche, data e ora
    - Irradianza in condizioni di cielo sereno (modello Ineichen-Perez)
    - Componenti diretta, diffusa e globale della radiazione
    
    ###### 2. Energetica Fotovoltaica
    Modelli termoelettrici per:
    - Calcolo della temperatura delle celle solari (modello NOCT)
    - Correzione dell'efficienza in funzione della temperatura
    
    ###### 3. Geometria Tridimensionale
    Calcoli per:
    - Proiezione dell'ombra in tempo reale
    - Sovrapposizione tra file di pannelli
    - Distribuzione spaziale della radiazione al suolo
    
    ###### 4. Agronomia
    Valutazione della compatibilità colturale tramite:
    - Integrazione del PAR (Photosynthetically Active Radiation)
    - Calcolo del DLI considerando ombreggiamento e trasmissività
    - Confronto con soglie specifiche per ogni specie

    ---

    ### Metodologie e Librerie
    
    Il simulatore si basa su uno stack tecnologico robusto, con l'impiego di librerie specializzate:
    
    | Libreria | Ruolo |
    |----------|-------|
    | **pvlib** | Modellazione fotovoltaica con algoritmi NASA/NREL |
    | **pandas** | Gestione serie temporali e analisi dati |
    | **geopy** | Geocoding e conversione località → coordinate |
    | **streamlit** | Interfaccia web interattiva |
    | **folium** | Mappe georeferenziate interattive |
    | **shapely** | Calcoli geometrici 2D |

    ---

    ### Flusso Operativo della Simulazione
    
    ```
    1. INPUT UTENTE 
       • Localizzazione e Geometria
       • Parametri Elettrici e Colturali
       ↓
    2. CALCOLI FOTOVOLTAICI 
       • Posizione solare oraria (pvlib.solarposition)
       • Irradianza clearsky (pvlib.clearsky)
       • POA (trasposizione sul piano inclinato)
       • Temperatura celle (modello NOCT)
       • Potenza DC/AC con correzione efficienza
       ↓
    3. CALCOLI AGRIVOLTAICI 
       • Proiezione ombra dinamica (trigonometria 3D)
       • Frazione ombreggiata e sovrapposizione file
       • PAR disponibile modulato per ombra
       • DLI giornaliero
       • Valutazione coltura rispetto alle soglie
       ↓
    4. OUTPUT METRICHE 
       • KPI energetici e agronomici visualizzati in card
       • Grafici temporali e indicatori di performance
    ```
    """)


def tab_input_utente():
    """Contenuto per la tab Input Utente."""
    st.markdown("""
    ### Input Utente

    ###### Localizzazione e Data
    
    | Parametro | Descrizione | Implementazione |
    |-----------|------------|----------------|
    | Comune | Località della simulazione | Geocoding tramite `geopy.Nominatim` |
    | Latitudine e Longitudine | Coordinate geografiche del sito | Derivate dal Geocoding o inserite manualmente |
    | Data | Giorno della simulazione | Serie temporale oraria (24 ore) |
    
    ---

    ### Parametri Pannelli
    
    - **Dimensioni:** `Lato Maggiore [m]`, `Lato Minore [m]` → area pannello
    - **Layout:** `Pannelli per Fila`, `Numero File` → totale pannelli
    - **Orientamento:** `Tilt [°]`, `Azimuth [°]` (180° = Sud)
    - **Spaziatura:** `Carreggiata [m]`, `Pitch Laterale [m]`
    - **Altezza dal suolo [m]**

    ---

    ### Sistema Elettrico

    - **Efficienza nominale e coeff. termico (γ [%/°C])**
    - **Temperatura NOCT [°C]**
    - **Perdite di sistema [%]**
    - **Albedo del suolo (0-1)**
    ---

    ### Parametri Agricoli

    - **Superficie:** Ettari Totali
    - **Coltura:** Tipo di coltura → requisiti DLI specifici
    """)


def tab_calculations():
    """Contenuto per la tab Calcoli Energetici e Geometrici."""
    st.markdown(r"""
    ### Calcoli Energetici e Geometrici

    ---

    ### Calcoli Geometrici e Layout
    - **Proiezione a Terra:** $A_{proj} = A_{pannello} \cdot \cos(\text{Tilt})$
    - **Superficie Libera:** Area Totale Campo − Proiezione Totale Pannelli
    - **Ground Cover Ratio (GCR):**
      $$\text{GCR} = \frac{\text{Proiezione Totale Pannelli}}{\text{Superficie Totale Campo}}$$

    ---

    ### Calcoli Solari
    - Posizione Solare oraria: `pvlib.solarposition.get_solarposition`
    - Irradianza Clearsky: `pvlib.location.Location.get_clearsky(model="ineichen")`
    - Irradianza POA: `pvlib.irradiance.get_total_irradiance`

    ---

    ### Calcoli Produzione Elettrica
    - **Temperatura Celle (NOCT):**
      $$T_{cell} = T_{amb} + \frac{\text{POA}_{global}}{800} \cdot (NOCT - 20)$$
    - **Efficienza corretta:**
      $$\eta_{corr} = \eta \cdot [1 + \gamma \cdot (T_{cell} - 25)]$$
    - **Potenza DC:**
      $$\text{Potenza}_{DC} = \text{POA}_{global} \cdot A_{pannello} \cdot \eta_{corr} \cdot (1 - \text{Perdite})$$
    """)


def tab_agri_calculations():
    """Contenuto per la tab Calcoli Agrivoltaici e Bibliografia."""
    st.markdown(r"""
    ### Calcoli Agrivoltaici

    ---

    ### Ombreggiamento Dinamico
    - **Altezza effettiva:** $H = \text{Altezza suolo} + L_{minore} \cdot \sin(\text{Tilt})$
    - **Lunghezza ombra:** $L_{ombra} = \frac{H}{\tan(\alpha)}$
    - **Frazione ombreggiata:** area ombra corretta per sovrapposizione file

    ---

    ### Daily Light Integral (DLI)
    - **Conversione GHI → PAR:** $PAR_{totale} = GHI \cdot 0.45$
    - **PAR pesato per ombra:**
      $$PAR_{pesato} = PAR_{totale} \cdot [(f\_ombra \cdot T_{sotto}) + (1 - f\_ombra) \cdot T_{libera}]$$
    - **DLI finale:**
      $$DLI = \frac{\sum (PAR_{pesato} \cdot 4.6) \cdot 3600}{10^6}$$

    ---

    ### Bibliografia
    - Perez et al., Solar Energy, 1990
    - NREL, Solar Position Algorithm
    - IEC 61215:2016
    - McCree, Agricultural Meteorology, 1972
    - Database CEA per requisiti DLI coltur
    """)

# ==================== FUNZIONE PRINCIPALE ====================

def show_pv_guide():
    """
    Funzione principale per visualizzare la guida tecnica completa in un expander con tab.
    """

    with st.expander("🔬 Manuale Operativo", expanded=False):
        tab1, tab2, tab3, tab4 = st.tabs([
            "Introduzione e Flusso", 
            "Input Utente", 
            "Calcoli PV & Geometria", 
            "Calcoli Agronomici & Bibliografia"
        ])
        
        with tab1:
            tab_introduzione()
        
        with tab2:
            tab_input_utente()
            
        with tab3:
            tab_calculations()
            
        with tab4:
            tab_agri_calculations()
