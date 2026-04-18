import streamlit as st
import requests
import pandas as pd
import numpy as np
from scipy.stats import poisson

# --- CONFIGURAZIONE API ---
API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3"
BASE_URL = "https://v3.football.api-sports.io"

st.set_page_config(page_title="PROBET AI V2 PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CSS PER INTERFACCIA IDENTICA (DARK PRO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] { background-color: #0b1120; color: white; font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 2rem; }
    
    /* Box Stile Match */
    .prediction-box {
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        margin-bottom: 10px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .val-over { background: linear-gradient(135deg, #1e3a2f 0%, #064e3b 100%); border: 1px solid #10b981; }
    .val-caution { background: linear-gradient(135deg, #451a03 0%, #78350f 100%); border: 1px solid #f59e0b; }
    .val-pass { background: #1f2937; color: #9ca3af; }
    
    .title-box { font-size: 0.7rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    .main-val { font-size: 1.5rem; font-weight: 900; line-height: 1; margin: 5px 0; }
    .sub-val { font-size: 0.75rem; font-weight: 600; opacity: 0.9; }
    .prob-val { font-size: 0.7rem; font-weight: 700; margin-top: 8px; opacity: 0.8; }
    
    .section-header { 
        font-size: 0.8rem; font-weight: 800; color: #6366f1; 
        display: flex; align-items: center; gap: 8px; margin: 20px 0 10px 0;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGICA STATISTICA AVANZATA (POISSON) ---
def calcola_probabilita(media_prevista, linea):
    # Calcola la probabilità di Over usando la distribuzione di Poisson
    prob_under = poisson.cdf(linea, media_prevista)
    prob_over = (1 - prob_under) * 100
    return round(prob_over, 1)

def get_status(media, linea, prob):
    diff = media - linea
    if diff > 1.5 and prob > 60: return "OVER", "SUPER VALORE", "val-over", "HIGH CONFIDENCE"
    if diff > 0.3: return "OVER", "BUONO", "val-caution", None
    if diff < -1.5 and prob < 40: return "UNDER", "SUPER VALORE", "val-over", "HIGH CONFIDENCE"
    return "PASS", "NO EDGE", "val-pass", None

# --- CARICAMENTO DATI (HIDDEN) ---
if 'db' not in st.session_state:
    st.session_state['db'] = None # Qui andrebbe la funzione fetch_data() che abbiamo testato

# --- INTERFACCIA ---
st.title("PROBET AI")

# Selezione Match (In una riga pulita)
if st.session_state['db'] is not None:
    df = st.session_state['db']
    col_a, col_b, col_c = st.columns([2,2,1])
    h_team = col_a.selectbox("CASA", df['Squadra'].unique())
    a_team = col_b.selectbox("FUORI", df['Squadra'].unique())
    linea_tiri = col_c.number_input("LINEA", value=23.5)
    
    if st.button("ESEGUI ANALISI AVANZATA"):
        h = df[df['Squadra'] == h_team].iloc[0]
        a = df[df['Squadra'] == a_team].iloc[0]

        # Calcoli (già verificati come corretti)
        m_h = ( (h['TF_C']/h['P_Casa']) + (a['TS_F']/a['P_Fuori']) ) / 2
        m_a = ( (a['TF_F']/a['P_Fuori']) + (h['TS_C']/h['P_Casa']) ) / 2
        tot = m_h + m_a
        
        m_tip_h = ( (h['TiP_F_C']/h['P_Casa']) + (a['TiP_S_F']/a['P_Fuori']) ) / 2
        m_tip_a = ( (a['TiP_F_F']/a['P_Fuori']) + (h['TiP_S_C']/h['P_Casa']) ) / 2
        tot_tip = m_tip_h + m_tip_a

        # --- SEZIONE TIRI TOTALI (GRAFICA UGUALE) ---
        st.markdown(f'<div class="section-header">⚽ TIRI TOTALI</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        
        # Match Totale
        p_over = calcola_probabilita(tot, linea_tiri)
        res, lbl, css, badge = get_status(tot, linea_tiri, p_over)
        badge_html = f'<span style="background:white; color:black; font-size:10px; padding:2px 6px; border-radius:10px; margin-left:5px;">⚡ {badge}</span>' if badge else ""
        
        c1.markdown(f'''<div class="prediction-box {css}">
            <div class="title-box">MATCH TOTALE {badge_html}</div>
            <div class="main-val">{res} {linea_tiri}</div>
            <div class="sub-val">AI: {tot:.2f} | {lbl}</div>
            <div class="prob-val">PROB. {p_over}%</div>
        </div>''', unsafe_allow_html=True)

        # Singola Casa
        p_h = calcola_probabilita(m_h, 12.5)
        res_h, lbl_h, css_h, _ = get_status(m_h, 12.5, p_h)
        c2.markdown(f'''<div class="prediction-box {css_h}">
            <div class="title-box">{h_team}</div>
            <div class="main-val">{res_h} 12.5</div>
            <div class="sub-val">AI: {m_h:.2f} | {lbl_h}</div>
            <div class="prob-val">PROB. {p_h}%</div>
        </div>''', unsafe_allow_html=True)

        # Singola Fuori
        p_a = calcola_probabilita(m_a, 10.5)
        res_a, lbl_a, css_a, _ = get_status(m_a, 10.5, p_a)
        c3.markdown(f'''<div class="prediction-box {css_a}">
            <div class="title-box">{a_team}</div>
            <div class="main-val">{res_a} 10.5</div>
            <div class="sub-val">AI: {m_a:.2f} | {lbl_a}</div>
            <div class="prob-val">PROB. {p_a}%</div>
        </div>''', unsafe_allow_html=True)

        # --- SEZIONE TIRI IN PORTA ---
        st.markdown(f'<div class="section-header">🎯 TIRI IN PORTA</div>', unsafe_allow_html=True)
        i1, i2, i3 = st.columns(3)
        
        p_tip = calcola_probabilita(tot_tip, 8.5)
        res_tip, lbl_tip, css_tip, _ = get_status(tot_tip, 8.5, p_tip)
        
        i1.markdown(f'''<div class="prediction-box {css_tip}">
            <div class="title-box">MATCH TOTALE</div>
            <div class="main-val">{res_tip} 8.5</div>
            <div class="sub-val">AI: {tot_tip:.2f} | {lbl_tip}</div>
            <div class="prob-val">PROB. {p_tip}%</div>
        </div>''', unsafe_allow_html=True)
        
        # ... (Stessa logica per i2 e i3 tiri in porta)
