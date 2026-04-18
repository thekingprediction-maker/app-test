import streamlit as st
import requests
import pandas as pd
from scipy.stats import poisson

# --- CONFIGURAZIONE API ---
API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3"
BASE_URL = "https://v3.football.api-sports.io"

st.set_page_config(page_title="PROBET AI - Dashboard", layout="wide", initial_sidebar_state="collapsed")

# --- CSS PER COPIARE L'INTERFACCIA ORIGINALE ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #050a18 !important;
        color: white !important;
        font-family: 'Inter', sans-serif;
    }

    /* Nasconde header Streamlit */
    div[data-testid="stHeader"] { display: none !important; }
    .block-container { padding-top: 2rem !important; }

    /* Titolo ProBet AI */
    .main-title { font-size: 32px; font-weight: 900; letter-spacing: 1px; margin-bottom: 20px; }
    .v2-pro { color: #6366f1; }
    .status-ready { color: #10b981; font-size: 10px; font-weight: bold; border: 1px solid #10b981; padding: 2px 8px; border-radius: 20px; float: right; }

    /* Card Layout */
    .prediction-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-bottom: 30px; }
    
    .card {
        background: #1e293b; /* Grigio/Blu scuro di base */
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        border: 1px solid #334155;
        position: relative;
    }

    /* Colori Card basati sui valori */
    .card-gold { background: linear-gradient(180deg, #b45309 0%, #78350f 100%); border-color: #f59e0b; }
    .card-green { background: linear-gradient(180deg, #065f46 0%, #064e3b 100%); border-color: #10b981; }
    .card-dark { background: #161e2d; border-color: #1e293b; color: #9ca3af; }

    .card-label { font-size: 10px; font-weight: 800; text-transform: uppercase; margin-bottom: 8px; opacity: 0.8; }
    .card-main-val { font-size: 24px; font-weight: 900; margin: 5px 0; }
    .card-sub-val { font-size: 12px; font-weight: 700; margin-bottom: 5px; }
    .card-prob { font-size: 11px; background: rgba(0,0,0,0.2); padding: 2px 10px; border-radius: 10px; display: inline-block; }

    /* Sezioni */
    .section-header { font-size: 14px; font-weight: 800; color: #94a3b8; margin: 25px 0 15px 0; display: flex; align-items: center; gap: 10px; }
    
    /* Input Style */
    .stSelectbox div[data-baseweb="select"] { background-color: #1e293b !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# --- FUNZIONI DATI ---
@st.cache_data(ttl=3600)
def fetch_api_stats():
    # In un caso reale qui chiameresti gli endpoint per i tiri. 
    # Per farti vedere il layout subito uso dei dati simulati basati sulle tue foto.
    data = [
        {"Team": "Udinese", "Tiri_F": 13.66, "Tiri_S": 12.10, "Porta_F": 3.97, "Falli_F": 12.5},
        {"Team": "Parma", "Team_id": 2, "Tiri_F": 10.56, "Tiri_S": 14.30, "Porta_F": 3.16, "Falli_F": 11.4}
    ]
    return pd.DataFrame(data)

def calc_prob(mu, line):
    return round((1 - poisson.cdf(line, mu)) * 100, 1)

# --- HEADER ---
st.markdown(f"""
    <div>
        <span class="status-ready">● SYSTEM READY: PRO</span>
        <div class="main-title">PROBET <span class="v2-pro">AI V2 PRO</span></div>
        <div style="color:#6366f1; font-size:11px; font-weight:700; margin-top:-15px; margin-bottom:30px;">SISTEMA DI ANALISI AUTOMATICA SEASON 2025/26</div>
    </div>
""", unsafe_allow_html=True)

df = fetch_api_stats()

# --- SELEZIONE ---
c1, c2, c3 = st.columns([2,2,1])
h_team = c1.selectbox("SQUADRA CASA", df['Team'].unique())
a_team = c2.selectbox("SQUADRA OSPITE", df['Team'].unique())
line_tiri = c3.number_input("LINEA TIRI", value=23.5, step=0.5)

if st.button("🚀 GENERA PREVISIONE PROFESSIONALE"):
    h_data = df[df['Team'] == h_team].iloc[0]
    a_data = df[df['Team'] == a_team].iloc[0]
    
    # Calcoli
    total_tiri = h_data['Tiri_F'] + a_data['Tiri_F']
    prob_total = calc_prob(total_tiri, line_tiri)
    prob_h = calc_prob(h_data['Tiri_F'], 12.5)

    # --- SEZIONE TIRI TOTALI ---
    st.markdown('<div class="section-header">⚽ TIRI TOTALI</div>', unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a: # Match Totale
        st.markdown(f"""
        <div class="card card-gold">
            <div class="card-label">MATCH TOTALE</div>
            <div class="card-main-val">OVER {line_tiri}</div>
            <div class="card-sub-val">AI: {total_tiri:.2f} | BUONO</div>
            <div class="card-prob">Prob. {prob_total}%</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_b: # Casa
        st.markdown(f"""
        <div class="card card-gold">
            <div class="card-label">{h_team.upper()}</div>
            <div class="card-main-val">OVER 12.5</div>
            <div class="card-sub-val">AI: {h_data['Tiri_F']:.2f} | BUONO</div>
            <div class="card-prob">Prob. {prob_h}%</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_c: # Ospite
        st.markdown(f"""
        <div class="card card-dark">
            <div class="card-label">{a_team.upper()}</div>
            <div class="card-main-val">PASS</div>
            <div class="card-sub-val">AI: {a_data['Tiri_F']:.2f} | NO EDGE</div>
            <div class="card-prob">Prob. 50.0%</div>
        </div>
        """, unsafe_allow_html=True)

    # --- SEZIONE TIRI IN PORTA ---
    st.markdown('<div class="section-header">🎯 TIRI IN PORTA</div>', unsafe_allow_html=True)
    # ... qui puoi ripetere lo schema delle card per i tiri in porta ...
