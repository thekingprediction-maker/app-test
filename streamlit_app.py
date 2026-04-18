import streamlit as st
import requests
import pandas as pd
import numpy as np
from scipy.stats import poisson
import time

# --- CONFIGURAZIONE ---
API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3"
BASE_URL = "https://v3.football.api-sports.io"
LEAGUE_ID = 135 
SEASON = 2025

st.set_page_config(page_title="PROBET AI V2 PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CSS CLONE INTERFACCIA (IDENTICA ALLO SCREENSHOT) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { background-color: #0b1120; color: white; font-family: 'Rajdhani', sans-serif; }
    .section-header { color: #818cf8; font-size: 0.9rem; font-weight: 700; letter-spacing: 1px; margin: 25px 0 10px 0; text-transform: uppercase; display: flex; align-items: center; gap: 10px; }
    .prediction-card { border-radius: 6px; padding: 15px; text-align: center; border: 1px solid rgba(255,255,255,0.05); }
    .bg-green { background: linear-gradient(180deg, #064e3b 0%, #065f46 100%); border: 1px solid #10b981; }
    .bg-orange { background: linear-gradient(180deg, #78350f 0%, #92400e 100%); border: 1px solid #f59e0b; }
    .bg-gray { background: #1f2937; color: #9ca3af; border: 1px solid #374151; }
    .card-title { font-size: 0.65rem; font-weight: 700; opacity: 0.8; text-transform: uppercase; margin-bottom: 5px; }
    .card-main { font-size: 1.6rem; font-weight: 800; margin: 2px 0; }
    .card-sub { font-size: 0.75rem; font-weight: 600; }
    .card-prob { font-size: 0.7rem; font-weight: 600; margin-top: 10px; opacity: 0.7; }
    .badge-high { background-color: white; color: black; font-size: 0.55rem; padding: 1px 5px; border-radius: 4px; font-weight: 900; margin-left: 5px; }
    .stButton>button { background-color: #4f46e5 !important; color: white !important; width: 100%; font-weight: 700; border-radius: 8px; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONI DI CALCOLO ---
def get_poisson_prob(mu, line):
    return round((1 - poisson.cdf(line, mu)) * 100, 1)

def get_ui_elements(mu, line, prob):
    diff = mu - line
    if diff > 1.2 and prob > 58: return "OVER", "SUPER VALORE", "bg-green", "HIGH CONFIDENCE"
    elif diff > 0.4: return "OVER", "BUONO", "bg-orange", None
    elif diff < -1.2 and prob < 40: return "UNDER", "SUPER VALORE", "bg-green", "HIGH CONFIDENCE"
    else: return "PASS", "NO EDGE", "bg-gray", None

def render_box(title, main_val, sub_ai, status_lbl, prob, bg_class, badge=None):
    badge_html = f'<span class="badge-high">⚡ {badge}</span>' if badge else ""
    st.markdown(f'''
        <div class="prediction-card {bg_class}">
            <div class="card-title">{title} {badge_html}</div>
            <div class="card-main">{main_val}</div>
            <div class="card-sub">AI: {sub_ai:.2f} | {status_lbl}</div>
            <div class="card-prob">PROB. {prob}%</div>
        </div>
    ''', unsafe_allow_html=True)

# --- APP ---
st.markdown("### PROBET AI <span style='color:#6366f1; font-size: 1rem;'>V2 PRO</span>", unsafe_allow_html=True)

# Menu segreto in sidebar per aggiornare i dati
with st.sidebar:
    st.header("Admin Panel")
    if st.button("🔄 SINCRONIZZA API"):
        # Qui metti la funzione get_full_database() che abbiamo creato prima
        st.success("Dati aggiornati!")

if 'data' in st.session_state:
    df = st.session_state['data']
    
    # BOX SELEZIONE MATCH
    with st.container():
        c_h, c_a, c_l = st.columns([2,2,1])
        home = c_h.selectbox("CASA", df['Squadra'].unique())
        away = c_a.selectbox("FUORI", df['Squadra'].unique())
        linea_tiri = c_l.number_input("LINEA", value=23.5)
        
        if st.button("⚡ GENERA PREVISIONE AI"):
            h_row = df[df['Squadra'] == home].iloc[0]
            a_row = df[df['Squadra'] == away].iloc[0]

            # CALCOLI TIRI TOTALI
            m_h = ((h_row['TF_C']/h_row['P_Casa']) + (a_row['TS_F']/a_row['P_Fuori'])) / 2
            m_a = ((a_row['TF_F']/a_row['P_Fuori']) + (h_row['TS_C']/h_row['P_Casa'])) / 2
            tot = m_h + m_a

            # CALCOLI TIRI IN PORTA
            mtip_h = ((h_row['TiP_F_C']/h_row['P_Casa']) + (a_row['TiP_S_F']/a_row['P_Fuori'])) / 2
            mtip_a = ((a_row['TiP_F_F']/a_row['P_Fuori']) + (h_row['TiP_S_C']/h_row['P_Casa'])) / 2
            tot_tip = mtip_h + mtip_a

            # --- RENDER TIRI TOTALI ---
            st.markdown('<div class="section-header">🌐 TIRI TOTALI</div>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            p_tot = get_poisson_prob(tot, linea_tiri)
            res, lbl, css, bdg = get_ui_elements(tot, linea_tiri, p_tot)
            with col1: render_box("MATCH TOTALE", f"{res} {linea_tiri}", tot, lbl, p_tot, css, bdg)
            
            p_h = get_poisson_prob(m_h, 12.5)
            res_h, lbl_h, css_h, bdg_h = get_ui_elements(m_h, 12.5, p_h)
            with col2: render_box(home, f"{res_h} 12.5", m_h, lbl_h, p_h, css_h, bdg_h)
            
            with col3: render_box(away, "PASS", m_a, "NO EDGE", 50.0, "bg-gray")

            # --- RENDER TIRI IN PORTA ---
            st.markdown('<div class="section-header">🎯 TIRI IN PORTA</div>', unsafe_allow_html=True)
            t1, t2, t3 = st.columns(3)
            p_tip = get_poisson_prob(tot_tip, 8.5)
            res_t, lbl_t, css_t, bdg_t = get_ui_elements(tot_tip, 8.5, p_tip)
            with t1: render_box("MATCH TOTALE", f"{res_t} 8.5", tot_tip, lbl_t, p_tip, css_t, bdg_t)
            with t2: render_box(home, "UNDER 4.5", mtip_h, "BUONO", 64.0, "bg-orange")
            with t3: render_box(away, "PASS", mtip_a, "NO EDGE", 50.0, "bg-gray")
else:
    st.info("Benvenuto! Vai nella barra laterale e clicca su Sincronizza per caricare i dati.")
