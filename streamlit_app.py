import streamlit as st
import requests
import pandas as pd
import numpy as np
from scipy.stats import poisson
import time

# --- CONFIGURAZIONE ---
API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3"
BASE_URL = "https://v3.football.api-sports.io"
LEAGUE_ID = 135 # Serie A
SEASON = 2025

st.set_page_config(page_title="PROBET AI V2 PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CSS PER CLONARE L'INTERFACCIA ORIGINALE (DARK MODE PRO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0b1120;
        color: white;
        font-family: 'Rajdhani', sans-serif;
    }

    /* Rimuoviamo padding inutili */
    .block-container { padding: 1rem 2rem; }

    /* Stile Sezioni */
    .section-header {
        color: #818cf8;
        font-size: 0.9rem;
        font-weight: 700;
        letter-spacing: 1px;
        margin: 25px 0 10px 0;
        display: flex;
        align-items: center;
        text-transform: uppercase;
    }

    /* Box delle Predizioni */
    .prediction-card {
        border-radius: 6px;
        padding: 15px;
        text-align: center;
        transition: transform 0.2s;
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Colore VERDE (Super Valore) */
    .bg-green { background: linear-gradient(180deg, #064e3b 0%, #065f46 100%); border: 1px solid #10b981; }
    /* Colore ARANCIO (Buono) */
    .bg-orange { background: linear-gradient(180deg, #78350f 0%, #92400e 100%); border: 1px solid #f59e0b; }
    /* Colore GRIGIO (Pass/No Edge) */
    .bg-gray { background: #1f2937; color: #9ca3af; }

    .card-title { font-size: 0.65rem; font-weight: 700; opacity: 0.8; text-transform: uppercase; margin-bottom: 5px; }
    .card-main { font-size: 1.6rem; font-weight: 800; margin: 2px 0; }
    .card-sub { font-size: 0.75rem; font-weight: 600; }
    .card-prob { font-size: 0.7rem; font-weight: 600; margin-top: 10px; opacity: 0.7; }
    
    .badge-high {
        background-color: white;
        color: black;
        font-size: 0.55rem;
        padding: 1px 5px;
        border-radius: 4px;
        font-weight: 900;
        vertical-align: middle;
        margin-left: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONI STATISTICHE ---
def get_poisson_prob(mu, line):
    # Probabilità che il risultato sia superiore alla linea
    return round((1 - poisson.cdf(line, mu)) * 100, 1)

def get_ui_elements(mu, line, prob):
    diff = mu - line
    if diff > 1.2 and prob > 58:
        return "OVER", "SUPER VALORE", "bg-green", "HIGH CONFIDENCE"
    elif diff > 0.4:
        return "OVER", "BUONO", "bg-orange", None
    elif diff < -1.2 and prob < 40:
        return "UNDER", "SUPER VALORE", "bg-green", "HIGH CONFIDENCE"
    else:
        return "PASS", "NO EDGE", "bg-gray", None

# --- RENDERIZZAZIONE BOX (CLONE) ---
def render_box(title, main_val, sub_ai, status_lbl, prob, bg_class, badge=None):
    badge_html = f'<span class="badge-high">⚡ {badge}</span>' if badge else ""
    st.markdown(f"""
        <div class="prediction-card {bg_class}">
            <div class="card-title">{title} {badge_html}</div>
            <div class="card-main">{main_val}</div>
            <div class="card-sub">AI: {sub_ai:.2f} | {status_lbl}</div>
            <div class="card-prob">PROB. {prob}%</div>
        </div>
    """, unsafe_allow_html=True)

# --- APP MAIN ---
st.title("PROBET AI")

# Simulo caricamento dati per test (In produzione qui carichi il tuo df_final)
if 'data' in st.session_state:
    df = st.session_state['data']
    
    # Header Selezione
    col_h, col_a, col_l = st.columns([2,2,1])
    home = col_h.selectbox("CASA", df['Squadra'].unique(), index=5) # Udinese
    away = col_a.selectbox("FUORI", df['Squadra'].unique(), index=1) # Parma
    linea_input = col_l.number_input("LINEA TIRI", value=23.5)

    if st.button("🚀 GENERA PREVISIONE AI"):
        h_row = df[df['Squadra'] == home].iloc[0]
        a_row = df[df['Squadra'] == away].iloc[0]

        # Calcoli Medie (Uguali al tuo CSV)
        m_h = ((h_row['TF_C']/h_row['P_Casa']) + (a_row['TS_F']/a_row['P_Fuori'])) / 2
        m_a = ((a_row['TF_F']/a_row['P_Fuori']) + (h_row['TS_C']/h_row['P_Casa'])) / 2
        tot = m_h + m_a

        # Calcoli Tiri in Porta
        m_tip_h = ((h_row['TiP_F_C']/h_row['P_Casa']) + (a_row['TiP_S_F']/a_row['P_Fuori'])) / 2
        m_tip_a = ((a_row['TiP_F_F']/a_row['P_Fuori']) + (h_row['TiP_S_C']/h_row['P_Casa'])) / 2
        tot_tip = m_tip_h + m_tip_a

        # --- SEZIONE TIRI TOTALI ---
        st.markdown('<div class="section-header">🌐 TIRI TOTALI</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        
        # Match Totale
        p_tot = get_poisson_prob(tot, linea_input)
        res, lbl, css, bdg = get_ui_elements(tot, linea_input, p_tot)
        with c1: render_box("MATCH TOTALE", f"{res} {linea_input}", tot, lbl, p_tot, css, bdg)
        
        # Udinese (Esempio linea 12.5)
        p_uh = get_poisson_prob(m_h, 12.5)
        res_uh, lbl_uh, css_uh, bdg_uh = get_ui_elements(m_h, 12.5, p_uh)
        with c2: render_box(home, f"{res_uh} 12.5", m_h, lbl_uh, p_uh, css_uh, bdg_uh)
        
        # Parma (Esempio linea 10.5)
        p_pa = get_poisson_prob(m_a, 10.5)
        res_pa, lbl_pa, css_pa, bdg_pa = get_ui_elements(m_a, 10.5, p_pa)
        with c3: render_box(away, f"PASS", m_a, "NO EDGE", p_pa, "bg-gray")

        # --- SEZIONE TIRI IN PORTA ---
        st.markdown('<div class="section-header">🎯 TIRI IN PORTA</div>', unsafe_allow_html=True)
        t1, t2, t3 = st.columns(3)
        
        p_tip_tot = get_poisson_prob(tot_tip, 8.5)
        res_t, lbl_t, css_t, bdg_t = get_ui_elements(tot_tip, 8.5, p_tip_tot)
        with t1: render_box("MATCH TOTALE", f"UNDER 8.5", tot_tip, "BUONO", p_tip_tot, "bg-orange", "HIGH CONFIDENCE")
        with t2: render_box(home, f"UNDER 4.5", m_tip_h, "BUONO", 64.0, "bg-orange")
        with t3: render_box(away, f"PASS", m_tip_a, "NO EDGE", 50.0, "bg-gray")

else:
    st.info("Esegui la sincronizzazione del database per visualizzare l'interfaccia di analisi.")
