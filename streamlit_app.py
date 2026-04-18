import streamlit as st
import requests
import pandas as pd
import time

# --- CONFIGURAZIONE ---
API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3" 
BASE_URL = "https://v3.football.api-sports.io"
LEAGUE_ID = 135  
SEASON = 2025

st.set_page_config(page_title="PROBET AI PROFESSIONAL", layout="wide")

# STILE PULITO E LEGGIBILE (Rimosso il nero che copriva i numeri)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; color: #1e1e1e; }
    .stMetric { 
        background-color: #ffffff !important; 
        padding: 20px !important; 
        border-radius: 12px !important; 
        border: 2px solid #e9ecef !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
    }
    .stMetric div { color: #1e1e1e !important; }
    .stDataFrame { border-radius: 10px; }
    h1, h2, h3 { color: #0d6efd !important; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 PROBET AI - Dashboard Professionale")

# --- FUNZIONE RECUPERO DATI COMPLETI ---
def get_full_database():
    headers = {'x-apisports-key': API_KEY}
    try:
        r = requests.get(f"{BASE_URL}/teams?league={LEAGUE_ID}&season={SEASON}", headers=headers)
        teams_data = r.json().get('response', [])
    except: return None

    final_rows = []
    progress = st.progress(0)
    status = st.empty()
    
    for i, t in enumerate(teams_data):
        tid, tname = t['team']['id'], t['team']['name']
        status.text(f"Analisi dati: {tname}...")
        
        row = {
            "Squadra": tname,
            "P_Casa": 0, "TF_C": 0, "TS_C": 0, "TiP_F_C": 0, "TiP_S_C": 0,
            "P_Fuori": 0, "TF_F": 0, "TS_F": 0, "TiP_F_F": 0, "TiP_S_F": 0
        }

        fix_r = requests.get(f"{BASE_URL}/fixtures?league={LEAGUE_ID}&season={SEASON}&team={tid}", headers=headers)
        fixtures = fix_r.json().get('response', [])

        for f in fixtures:
            if f['fixture']['status']['short'] == 'FT':
                fid, is_home = f['fixture']['id'], f['teams']['home']['id'] == tid
                stat_r = requests.get(f"{BASE_URL}/fixtures/statistics?fixture={fid}", headers=headers)
                stats = stat_r.json().get('response', [])

                if len(stats) == 2:
                    my_idx = 0 if stats[0]['team']['id'] == tid else 1
                    opp_idx = 1 - my_idx
                    
                    def get_v(s_list, label):
                        for s in s_list['statistics']:
                            if s['type'] == label: return s['value'] or 0
                        return 0

                    if is_home:
                        row["P_Casa"] += 1
                        row["TF_C"] += get_v(stats[my_idx], "Total Shots")
                        row["TS_C"] += get_v(stats[opp_idx], "Total Shots")
                        row["TiP_F_C"] += get_v(stats[my_idx], "Shots on Goal")
                        row["TiP_S_C"] += get_v(stats[opp_idx], "Shots on Goal")
                    else:
                        row["P_Fuori"] += 1
                        row["TF_F"] += get_v(stats[my_idx], "Total Shots")
                        row["TS_F"] += get_v(stats[opp_idx], "Total Shots")
                        row["TiP_F_F"] += get_v(stats[my_idx], "Shots on Goal")
                        row["TiP_S_F"] += get_v(stats[opp_idx], "Shots on Goal")
        
        final_rows.append(row)
        progress.progress((i + 1) / len(teams_data))
        time.sleep(0.1)

    return pd.DataFrame(final_rows)

if st.button("🔄 AGGIORNA DATABASE (CREA CSV)"):
    df = get_full_database()
    st.session_state['data'] = df

if 'data' in st.session_state:
    df = st.session_state['data']
    st.dataframe(df, use_container_width=True)

    st.divider()
    st.header("🎯 Analisi Match e Tiri in Porta")
    
    c1, c2, c3 = st.columns(3)
    h_team = c1.selectbox("Squadra Casa", df['Squadra'].unique())
    a_team = c2.selectbox("Squadra Fuori", df['Squadra'].unique())
    linea = c3.number_input("Linea Over Tiri", value=23.5)

    if st.button("GENERA PREVISIONE PROFESSIONALE"):
        h, a = df[df['Squadra'] == h_team].iloc[0], df[df['Squadra'] == a_team].iloc[0]

        # --- CALCOLO MEDIE TIRI TOTALI ---
        m_tf_h = h['TF_C']/h['P_Casa'] if h['P_Casa']>0 else 0
        m_ts_a = a['TS_F']/a['P_Fuori'] if a['P_Fuori']>0 else 0
        m_tf_a = a['TF_F']/a['P_Fuori'] if a['P_Fuori']>0 else 0
        m_ts_h = h['TS_C']/h['P_Casa'] if h['P_Casa']>0 else 0

        prev_tiri_h = (m_tf_h + m_ts_a) / 2
        prev_tiri_a = (m_tf_a + m_ts_h) / 2
        tot_tiri = prev_tiri_h + prev_tiri_a

        # --- CALCOLO MEDIE TIRI IN PORTA ---
        m_tipf_h = h['TiP_F_C']/h['P_Casa'] if h['P_Casa']>0 else 0
        m_tips_a = a['TiP_S_F']/a['P_Fuori'] if a['P_Fuori']>0 else 0
        m_tipf_a = a['TiP_F_F']/a['P_Fuori'] if a['P_Fuori']>0 else 0
        m_tips_h = h['TiP_S_C']/h['P_Casa'] if h['P_Casa']>0 else 0

        prev_tip_h = (m_tipf_h + m_tips_a) / 2
        prev_tip_a = (m_tipf_a + m_tips_h) / 2
        tot_tip = prev_tip_h + prev_tip_a

        # --- RISULTATI VISIBILI ---
        st.subheader(f"Analisi: {h_team} vs {a_team}")
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.metric(f"Tiri Totali {h_team}", f"{prev_tiri_h:.2f}")
            st.metric(f"Tiri in Porta {h_team}", f"{prev_tip_h:.2f}")
        with col_t2:
            st.metric(f"Tiri Totali {a_team}", f"{prev_tiri_a:.2f}")
            st.metric(f"Tiri in Porta {a_team}", f"{prev_tip_a:.2f}")

        st.divider()
        res1, res2 = st.columns(2)
        res1.metric("TOTALE TIRI MATCH", f"{tot_tiri:.2f}", delta=round(tot_tiri-linea, 2))
        res2.metric("TOTALE IN PORTA MATCH", f"{tot_tip:.2f}")

        if tot_tiri > (linea + 0.5):
            st.success(f"CONSIGLIO: OVER {linea} ✅")
        elif tot_tiri < (linea - 0.5):
            st.error(f"CONSIGLIO: UNDER {linea} ❌")
        else:
            st.warning("NO BET: Valore troppo vicino alla linea")
