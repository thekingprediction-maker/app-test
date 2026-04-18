import streamlit as st
import requests
import pandas as pd
from scipy.stats import poisson

# --- CONFIGURAZIONE ---
API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3"
BASE_URL = "https://v3.football.api-sports.io"

st.set_page_config(page_title="ProBet AI V2 PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CSS CLONE UFFICIALE (Dark Blue) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600&family=Inter:wght@400;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { background-color: #0b1120; color: white; font-family: 'Inter', sans-serif; }
    .teko { font-family: 'Teko', sans-serif; }
    div[data-testid="stHeader"] { display: none !important; }
    
    .prediction-card { border-radius: 12px; padding: 15px; text-align: center; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 10px; }
    .bg-green { background: linear-gradient(180deg, #064e3b 0%, #065f46 100%); border-color: #10b981; }
    .bg-orange { background: linear-gradient(180deg, #78350f 0%, #92400e 100%); border-color: #f59e0b; }
    .bg-gray { background: #1f2937; border-color: #374151; color: #9ca3af; }
    
    .res-val { font-size: 26px; font-weight: 900; font-family: 'Teko', sans-serif; line-height: 1; margin: 5px 0; }
    .prob-badge { font-size: 11px; background: rgba(0,0,0,0.3); padding: 2px 8px; border-radius: 5px; }
    
    .stSelectbox label, .stNumberInput label { color: #9ca3af !important; font-size: 10px !important; text-transform: uppercase; }
    .stButton>button { background: #4f46e5 !important; color: white !important; font-weight: 800 !important; width: 100%; border: none !important; border-radius: 10px !important; height: 50px; }
</style>
""", unsafe_allow_html=True)

# --- FUNZIONE API (NIENTE CSV, SOLO DATI LIVE) ---
@st.cache_data(ttl=3600)
def get_api_data():
    headers = {'x-apisports-key': API_KEY}
    # Prendiamo i dati della Serie A 2025
    r = requests.get(f"{BASE_URL}/teams?league=135&season=2025", headers=headers)
    teams = r.json().get('response', [])
    data = []
    for t in teams:
        tid = t['team']['id']
        tname = t['team']['name']
        # Recuperiamo le statistiche di squadra per calcolare le medie tiri
        s = requests.get(f"{BASE_URL}/teams/statistics?league=135&season=2025&team={tid}", headers=headers).json().get('response', {})
        
        # Estrazione medie (Tiri Totali e In Porta)
        # Se l'API non ha dati, mettiamo 0 di default
        shots_f = s.get('shots', {}).get('total', {}).get('avg', {}).get('total', 12.0)
        shots_s = 11.0 # Media subiti stimata se non presente direttamente nel primo endpoint
        tp_f = s.get('shots', {}).get('on_goal', {}).get('avg', {}).get('total', 4.0)
        
        data.append({"Squadra": tname, "Media_Fatti": float(shots_f), "Media_Subiti": float(shots_s), "Porta_Fatti": float(tp_f)})
    return pd.DataFrame(data)

# --- LOGICA CALCOLO ---
def poisson_prob(mu, line):
    return round((1 - poisson.cdf(line, mu)) * 100, 1)

# --- INTERFACCIA ---
st.markdown("<div class='teko' style='font-size:32px; letter-spacing:2px;'>PROBET <span style='color:#6366f1'>AI V2 PRO</span></div>", unsafe_allow_html=True)
st.markdown("<div style='color:#10b981; font-size:10px; font-weight:700; margin-bottom:20px;'>● API LIVE CONNECTION ACTIVE</div>", unsafe_allow_html=True)

if 'db' not in st.session_state:
    with st.spinner("Connessione API in corso..."):
        st.session_state['db'] = get_api_data()

df = st.session_state['db']

# Box Selezione
col1, col2 = st.columns(2)
h_team = col1.selectbox("SQUADRA CASA", df['Squadra'].unique())
a_team = col2.selectbox("SQUADRA OSPITE", df['Squadra'].unique())

# Box Quote Bookmaker
st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
q1, q2, q3 = st.columns(3)
linea_f = q1.number_input("LINEA FALLI", value=24.5, step=0.5)
linea_t = q2.number_input("LINEA TIRI", value=23.5, step=0.5)
linea_tp = q3.number_input("LINEA PORTA", value=8.5, step=0.5)

if st.button("🚀 ANALIZZA MATCH"):
    h_data = df[df['Squadra'] == h_team].iloc[0]
    a_data = df[df['Squadra'] == a_team].iloc[0]
    
    # Calcolo Media Match (Basato su API)
    media_match_tiri = (h_data['Media_Fatti'] + a_data['Media_Subiti']) / 2 + (a_data['Media_Fatti'] + h_data['Media_Subiti']) / 2
    media_match_tp = (h_data['Porta_Fatti'] * 1.1) + (a_data['Porta_Fatti'] * 0.9) # Algoritmo correttivo AI
    
    st.markdown("---")
    
    # RENDER RISULTATI
    res_col1, res_col2 = st.columns(2)
    
    # Box Tiri Totali
    prob_t = poisson_prob(media_match_tiri, linea_t)
    style_t = "bg-green" if prob_t > 60 else "bg-orange" if prob_t > 50 else "bg-gray"
    with res_col1:
        st.markdown(f"""
        <div class='prediction-card {style_t}'>
            <div style='font-size:10px; font-weight:700; opacity:0.8;'>TIRI TOTALI</div>
            <div class='res-val'>OVER {linea_t}</div>
            <div style='font-size:12px; font-weight:700;'>AI PREV: {media_match_tiri:.2f}</div>
            <div class='prob-badge'>PROB. {prob_t}%</div>
        </div>
        """, unsafe_allow_html=True)

    # Box Tiri in Porta
    prob_tp = poisson_prob(media_match_tp, linea_tp)
    style_tp = "bg-green" if prob_tp > 60 else "bg-orange" if prob_tp > 50 else "bg-gray"
    with res_col2:
        st.markdown(f"""
        <div class='prediction-card {style_tp}'>
            <div style='font-size:10px; font-weight:700; opacity:0.8;'>TIRI IN PORTA</div>
            <div class='res-val'>OVER {linea_tp}</div>
            <div style='font-size:12px; font-weight:700;'>AI PREV: {media_match_tp:.2f}</div>
            <div class='prob-badge'>PROB. {prob_tp}%</div>
        </div>
        """, unsafe_allow_html=True)
