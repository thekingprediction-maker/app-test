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

# --- CSS CLONE PERFETTO (Sfondo Blu Notte, Box Colorati e Font Professionali) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0b1120;
        color: white;
        font-family: 'Rajdhani', sans-serif;
    }

    .section-header {
        color: #818cf8;
        font-size: 0.9rem;
        font-weight: 700;
        letter-spacing: 1px;
        margin: 25px 0 10px 0;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .prediction-card {
        border-radius: 6px;
        padding: 15px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.05);
        min-height: 150px;
    }
    
    /* Colori Identici allo Screenshot Ufficiale */
    .bg-green { background: linear-gradient(180deg, #064e3b 0%, #065f46 100%); border: 1px solid #10b981; }
    .bg-orange { background: linear-gradient(180deg, #78350f 0%, #92400e 100%); border: 1px solid #f59e0b; }
    .bg-gray { background: #1f2937; color: #9ca3af; border: 1px solid #374151; }

    .card-title { font-size: 0.65rem; font-weight: 700; opacity: 0.8; text-transform: uppercase; margin-bottom: 5px; }
    .card-main { font-size: 1.8rem; font-weight: 800; margin: 2px 0; }
    .card-sub { font-size: 0.8rem; font-weight: 600; }
    .card-prob { font-size: 0.75rem; font-weight: 700; margin-top: 10px; opacity: 0.9; color: #cbd5e1; }
    
    .badge-high {
        background-color: white;
        color: black;
        font-size: 0.6rem;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 900;
        margin-left: 5px;
        vertical-align: middle;
    }

    .stSelectbox label, .stNumberInput label { color: #9ca3af !important; font-size: 0.8rem !important; }
    .stButton>button {
        background: linear-gradient(90deg, #4f46e5 0%, #3730a3 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        width: 100%;
        height: 50px;
        border-radius: 8px !important;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONE RECUPERO DATI AUTOMATICA ---
@st.cache_data(ttl=3600) # Aggiorna i dati ogni ora automaticamente
def fetch_database():
    headers = {'x-apisports-key': API_KEY}
    try:
        r = requests.get(f"{BASE_URL}/teams?league={LEAGUE_ID}&season={SEASON}", headers=headers)
        teams = r.json().get('response', [])
        rows = []
        for t in teams:
            tid, tname = t['team']['id'], t['team']['name']
            row = {"Squadra": tname, "P_C": 0, "TF_C": 0, "TS_C": 0, "TiP_C": 0, "P_F": 0, "TF_F": 0, "TS_F": 0, "TiP_F": 0}
            fix_r = requests.get(f"{BASE_URL}/fixtures?league={LEAGUE_ID}&season={SEASON}&team={tid}", headers=headers)
            for f in fix_r.json().get('response', []):
                if f['fixture']['status']['short'] == 'FT':
                    fid, is_home = f['fixture']['id'], f['teams']['home']['id'] == tid
                    stats = requests.get(f"{BASE_URL}/fixtures/statistics?fixture={fid}", headers=headers).json().get('response', [])
                    if len(stats) == 2:
                        idx = 0 if stats[0]['team']['id'] == tid else 1
                        opp = 1 - idx
                        def get_v(s_list, label):
                            for s in s_list['statistics']:
                                if s['type'] == label: return s['value'] or 0
                            return 0
                        if is_home:
                            row["P_C"] += 1; row["TF_C"] += get_v(stats[idx], "Total Shots"); row["TS_C"] += get_v(stats[opp], "Total Shots"); row["TiP_C"] += get_v(stats[idx], "Shots on Goal")
                        else:
                            row["P_F"] += 1; row["TF_F"] += get_v(stats[idx], "Total Shots"); row["TS_F"] += get_v(stats[opp], "Total Shots"); row["TiP_F"] += get_v(stats[idx], "Shots on Goal")
            rows.append(row)
        return pd.DataFrame(rows)
    except: return pd.DataFrame()

# --- FUNZIONI STATISTICHE ---
def get_poisson_prob(mu, line):
    return round((1 - poisson.cdf(line, mu)) * 100, 1)

def get_ui_elements(mu, line, prob):
    diff = mu - line
    if diff > 1.3 and prob > 58: return "OVER", "SUPER VALORE", "bg-green", "HIGH CONFIDENCE"
    elif diff > 0.3: return "OVER", "BUONO", "bg-orange", None
    elif diff < -1.3 and prob < 42: return "UNDER", "SUPER VALORE", "bg-green", "HIGH CONFIDENCE"
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

# --- UI PRINCIPALE ---
st.markdown("""
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <h1 style='margin:0; font-weight:900;'>PROBET AI <span style='color:#6366f1;'>V2 PRO</span></h1>
        <div style='background:#1e293b; padding:5px 15px; border-radius:20px; border:1px solid #10b981; color:#10b981; font-size:0.8rem; font-weight:700;'>
            ● SYSTEM READY: PRO
        </div>
    </div>
    <p style='color:#9ca3af; font-size:0.8rem; margin-top:-5px;'>SISTEMA DI ANALISI AUTOMATICA SEASON 2025/26</p>
""", unsafe_allow_html=True)

# Caricamento Silenzioso
if 'data' not in st.session_state:
    with st.spinner("⚡ Caricamento Database AI..."):
        st.session_state['data'] = fetch_database()

if not st.session_state['data'].empty:
    df = st.session_state['data']
    
    # BOX SELEZIONE
    with st.container():
        st.markdown("<br>", unsafe_allow_html=True)
        c_h, c_a, c_l = st.columns([2,2,1])
        home = c_h.selectbox("SQUADRA CASA", df['Squadra'].unique(), index=5)
        away = c_a.selectbox("SQUADRA OSPITE", df['Squadra'].unique(), index=1)
        linea_input = c_l.number_input("LINEA TIRI", value=23.5, step=1.0)
        
        if st.button("🚀 GENERA PREVISIONE PROFESSIONALE"):
            h = df[df['Squadra'] == home].iloc[0]
            a = df[df['Squadra'] == away].iloc[0]

            # Calcoli Tiri Totali (Sincronizzati col tuo CSV)
            m_h = ((h['TF_C']/h['P_C']) + (a['TS_F']/a['P_F'])) / 2
            m_a = ((a['TF_F']/a['P_F']) + (h['TS_C']/h['P_C'])) / 2
            tot = m_h + m_a

            # Calcoli Tiri in Porta
            mt_h = ((h['TiP_C']/h['P_C']) + (a['TS_F']*0.3/a['P_F'])) / 2 # Stima se manca dato preciso
            mt_a = ((a['TiP_F']/a['P_F']) + (h['TS_C']*0.3/h['P_C'])) / 2
            tot_tip = mt_h + mt_a

            # --- SEZIONE TIRI TOTALI ---
            st.markdown('<div class="section-header">⚽ TIRI TOTALI</div>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            
            p_tot = get_poisson_prob(tot, linea_input)
            res, lbl, css, bdg = get_ui_elements(tot, linea_input, p_tot)
            with col1: render_box("MATCH TOTALE", f"{res} {linea_input}", tot, lbl, p_tot, css, bdg)
            
            p_h = get_poisson_prob(m_h, 12.5)
            res_h, lbl_h, css_h, bdg_h = get_ui_elements(m_h, 12.5, p_h)
            with col2: render_box(home, f"{res_h} 12.5", m_h, lbl_h, p_h, css_h, bdg_h)
            
            with col3: render_box(away, "PASS", m_a, "NO EDGE", 50.0, "bg-gray")

            # --- SEZIONE TIRI IN PORTA ---
            st.markdown('<div class="section-header">🎯 TIRI IN PORTA</div>', unsafe_allow_html=True)
            t1, t2, t3 = st.columns(3)
            
            p_tip = get_poisson_prob(tot_tip, 8.5)
            res_t, lbl_t, css_t, bdg_t = get_ui_elements(tot_tip, 8.5, p_tip)
            with t1: render_box("MATCH TOTALE", f"{res_t} 8.5", tot_tip, lbl_t, p_tip, css_t, bdg_t)
            with t2: render_box(home, f"UNDER 4.5", mt_h, "BUONO", 62.4, "bg-orange")
            with t3: render_box(away, "PASS", mt_a, "NO EDGE", 50.0, "bg-gray")
else:
    st.error("Errore nel collegamento API. Controlla la tua API KEY.")
