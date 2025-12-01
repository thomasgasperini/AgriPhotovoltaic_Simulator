"""
Modulo Metriche - Visualizzazione risultati con card pulite e moderne
"""

import streamlit as st


# ==================== CONFIGURAZIONE STILI ====================

# Stile per unità più piccole (personalizzabile una sola volta)
UNIT_SMALL_STYLE = 'font-size:16px'   # cambia valore a piacere

def style_unit(unit: str) -> str:
    """Applica lo stile definito alle unità."""
    return f'<span style="{UNIT_SMALL_STYLE}">{unit}</span>'


# ==================== UTILITY ====================

def format_value(value: float, unit: str = "", decimals: int = 0, small_unit: bool = False) -> str:
    """Formatta valore con unità, opzionalmente riducendo la dimensione dell'unità."""
    if unit and small_unit:
        unit = style_unit(unit)
    return f"{value:.{decimals}f} {unit}".strip()


def create_metric_card(label: str, value: str, description: str = "", color: str = None) -> str:
    color_style = f"color:{color};" if color else ""
    
    return f"""
    <div class="metric-card" style="
        background:#f0f2f6;
        padding:1rem;
        margin:0.25rem;
        border-radius:0.5rem;
        text-align:center;
    ">
        <div class="metric-label" style="font-weight:600; font-size:0.9rem;">{label}</div>
        <div class="metric-value" style="font-size:1.2rem; margin:0.2rem 0; {color_style}">{value}</div>
        {f'<div class="metric-description" style="font-size:0.75rem; color:#555;">{description}</div>' if description else ''}
    </div>
    """


def get_screen_width() -> int:
    try:
        from screeninfo import get_monitors
        return get_monitors()[0].width
    except:
        return 1200


def display_card_group(cards: list):
    screen_width = get_screen_width()
    
    if screen_width > 768:
        for i in range(0, len(cards), 3):
            row_cards = cards[i:i+3]
            while len(row_cards) < 3:
                row_cards.append("")
            
            cols = st.columns(3, gap="medium")
            for col, card in zip(cols, row_cards):
                if card:
                    col.markdown(card, unsafe_allow_html=True)
    else:
        for card in cards:
            st.markdown(card, unsafe_allow_html=True)


# ==================== GENERAZIONE METRICHE ====================

def generate_solar_metrics(results: dict) -> list:
    return [
        create_metric_card(
            "GHI",
            f"{format_value(results['GHI_Wm2'].mean(), 'W/m²', small_unit=True)}<br>"
            f"{format_value(results['GHI_Whm2'], 'Wh/m²', small_unit=True)}",
            "Radiazione globale orizzontale (media oraria / totale giornaliero)"
        ),
        
        create_metric_card(
            "DNI",
            f"{format_value(results['DNI_Wm2'].mean(), 'W/m²', small_unit=True)}<br>"
            f"{format_value(results['DNI_Whm2'], 'Wh/m²', small_unit=True)}",
            "Radiazione diretta normale (media oraria / totale giornaliero)"
        ),
        
        create_metric_card(
            "DHI",
            f"{format_value(results['DHI_Wm2'].mean(), 'W/m²', small_unit=True)}<br>"
            f"{format_value(results['DHI_Whm2'], 'Wh/m²', small_unit=True)}",
            "Radiazione diffusa orizzontale (media oraria / totale giornaliero)"
        ),
        
        create_metric_card(
            "POA",
            f"{format_value(results['POA_Wm2'].mean(), 'W/m²', small_unit=True)}<br>"
            f"{format_value(results['POA_Whm2'], 'Wh/m²', small_unit=True)}",
            "Radiazione sul piano pannelli (media oraria / totale giornaliero)"
        ),
        
        create_metric_card(
            "T° Media Celle",
            f"{format_value(results['T_cell_avg'], '°C', 1)}",
            "Temperatura media delle celle fotovoltaiche"
        ),
    ]


def generate_production_metrics(results: dict) -> list:
    return [
        create_metric_card(
            "Produzione Singolo Pannello",
            f"{format_value(results['power_single_W'].mean(), 'W', small_unit=True)}<br>"
            f"{format_value(results['energy_single_Wh'], 'Wh', small_unit=True)}",
            "Potenza media oraria / Energia giornaliera singolo pannello"
        ),
        
        create_metric_card(
            "Produzione Totale",
            f"{format_value(results['power_total_W'].mean(), 'W', small_unit=True)}<br>"
            f"{format_value(results['energy_total_Wh'], 'Wh', small_unit=True)}",
            "Potenza media oraria / Energia giornaliera tutti i pannelli"
        ),
        
        create_metric_card(
            "Produzione Energetica per m²",
            f"{format_value(results['energy_total_Wh_m2'], 'Wh/m²', 1, small_unit=True)}",
            "Energia giornaliera per metro quadro di pannello"
        ),
    ]


def generate_geometric_metrics(results: dict) -> list:
    gcr = results['gcr']
    gcr_color = "red" if gcr > 0.4 else "green"
    
    return [
        create_metric_card(
            "Superficie Totale Pannelli",
            f"{format_value(results['superficie_totale_pannelli'], 'm²', 0, small_unit=True)}",
            "Area nominale totale (base × altezza × numero pannelli)"
        ),
        
        create_metric_card(
            "Spazio Occupato (Proiezione)",
            f"{format_value(results['proiezione_totale_pannelli'], 'm²', 0, small_unit=True)}",
            "Ingombro al suolo considerando tilt (proiezione pannelli)"
        ),

        create_metric_card(
            "GCR (Ground Coverage Ratio)",
            f"{format_value(gcr * 100, '%', 1)}",
            "Rapporto tra proiezione pannelli e superficie campo",
            color=gcr_color
        ),
        
        create_metric_card(
            "Superficie Libera",
            f"{format_value(results['superficie_libera'], 'm²', 0, small_unit=True)}",
            "Terreno libero disponibile (campo - proiezione pannelli)"
        ),

        create_metric_card(
            "Pannelli installabili",
            f"{format_value(results['total_panels'], '', 0)}",
            "N. pannelli installabili secondo dimensionamento (campo/pannelli)"
        )
    ]


def generate_agri_metrics(agri_results: dict) -> list:
    crop_color = agri_results.get('crop_status_color', None)

    return [
        create_metric_card(
            "DLI totale giornaliero",
            f"{format_value(agri_results['DLI_mol_m2_day'], 'mol/m²·day', 1, small_unit=True)}",
            "Totale giornaliero di luce fotosinteticamente attiva"
        ),

        create_metric_card( 
            "DLI Richiesto",
            f"{format_value(agri_results['DLI_min'], agri_results['unit'], small_unit=True)}<br>"
            f"{format_value(agri_results['DLI_opt'], agri_results['unit'], small_unit=True)}",
            "Fabbisogno giornaliero della coltura (min - ottimale)"
        ),

        create_metric_card(
            "Adeguatezza Luminosità",
            f"{format_value(agri_results['crop_light_adequacy_pct'], '%', 0)}",
            "Percentuale del fabbisogno luminoso soddisfatto dalla luce disponibile",
            color=crop_color
        ),

        create_metric_card(
            "Stato Coltura",
            agri_results['crop_status'],
            "Valutazione dell'idoneità agronomica della coltura secondo il DLI",
            color=crop_color
        ),

        create_metric_card(
            "Ombreggiamento Medio",
            f"{format_value(agri_results['shaded_fraction_avg']*100, '%', 1)}",
            "Media giornaliera della frazione di superficie del campo in ombra"
        ),
        
        create_metric_card(
            "Ombra Massima",
            f"{format_value(agri_results['shadow_area_max_m2'], 'm²', 0, small_unit=True)}",
            "Area massima in ombra rilevata sul campo durante la giornata"
        ),
    ]


# ==================== FUNZIONE PRINCIPALE ====================

def display_metrics(results: dict, params: dict):
    st.markdown(
        '<p class="section-header" style="margin-top: 1rem;">'
        'Irradiamento Solare e Temperatura Pannelli'
        '</p>',
        unsafe_allow_html=True
    )
    display_card_group(generate_solar_metrics(results))
    
    st.markdown(
        '<p class="section-header" style="margin-top: 1rem;">'
        'Produzione Elettrica'
        '</p>',
        unsafe_allow_html=True
    )
    display_card_group(generate_production_metrics(results))
    
    st.markdown(
        '<p class="section-header" style="margin-top: 1rem;">'
        'Geometria e Copertura Terreno'
        '</p>',
        unsafe_allow_html=True
    )
    display_card_group(generate_geometric_metrics(results))

    st.markdown(
        '<p class="section-header" style="margin-top: 1rem;">'
        'Metriche Agronomiche'
        '</p>',
        unsafe_allow_html=True
    )
    display_card_group(generate_agri_metrics(results["agri_results"]))
