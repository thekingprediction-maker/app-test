import streamlit as st
import requests
import pandas as pd
import time

# --- CONFIGURAZIONE ---
API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3"
BASE_URL = "https://v3.football.api-sports.io"
LEAGUE_ID = 135  # Serie A
SEASON = 2025

st.set_page_config(page_title="PROBET AI PROFESSIONAL", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 PROBET AI: Generatore Database Serie A")

# --- MOTORE DI RECUPERO DATI (UGUALE AL TUO CSV) ---
def get_full_database():
    headers = {'x-apisports-key': API_KEY}
    
    # Prendo le squadre
    try:
        r = requests.get(f"{BASE_URL}/teams?league={LEAGUE_ID}&season={SEASON}", headers=headers)
        teams_data = r.json().get('response', [])
    except:
        return None

    final_rows = []
    progress = st.progress(0)
    
    for i, t in enumerate(teams_data):
        tid = t['team']['id']
        tname = t['team']['name']
        
        # Inizializzo i dati identici al tuo file CSV
        data = {
            "Squadra": tname,
            "Partite Casa": 0, "Tiri Fatti Casa": 0, "Tiri Subiti Casa": 0,
            "Partite Trasferta": 0, "Tiri Fatti Trasferta": 0, "Tiri Subiti Trasferta": 0
        }

        # Prendo le partite della squadra per calcolare i tiri FATTI e SUBITI
        fix_r = requests.get(f"{BASE_URL}/fixtures?league={LEAGUE_ID}&season={SEASON}&team={tid}", headers=headers)
        fixtures = fix_r.json().get('response', [])

        for f in fixtures:
            if f['fixture']['status']['short'] == 'FT':
                fid = f['fixture']['id']
                is_home = f['teams']['home']['id'] == tid
                
                # Statistiche del match
                stat_r = requests.get(f"{BASE_URL}/fixtures/statistics?fixture={fid}", headers=headers)
                stats = stat_r.json().get('response', [])

                if len(stats) == 2:
                    my_idx = 0 if stats[0]['team']['id'] == tid else 1
                    opp_idx = 1 - my_idx
                    
                    def find_shots(s_list):
                        for s in s_list['statistics']:
                            if s['type'] == "Total Shots": return s['value'] or 0
                        return 0

                    my_sh = find_shots(stats[my_idx])
                    opp_sh = find_shots(stats[opp_idx])

                    if is_home:
                        data["Partite Casa"] += 1
                        data["Tiri Fatti Casa"] += my_sh
                        data["Tiri Subiti Casa"] += opp_sh
                    else:
                        data["Partite Trasferta"] += 1
                        data["Tiri Fatti Trasferta"] += my_sh
                        data["Tiri Subiti Trasferta"] += opp_sh
        
        final_rows.append(data)
        progress.progress((i + 1) / len(teams_data))
        time.sleep(0.1) # Per non bloccare l'API

    return pd.DataFrame(final_rows)

# --- INTERFACCIA APP ---
if st.button("🔄 SINCRONIZZA TUTTI I DATI (CREA CSV AUTOMATICO)"):
    df = get_full_database()
    st.session_state['data'] = df
    st.success("Dati aggiornati!")

if 'data' in st.session_state:
    df = st.session_state['data']
    st.dataframe(df, use_container_width=True)

    st.divider()
    st.header("🎯 Analisi Match")
    
    col1, col2, col3 = st.columns(3)
    h_team = col1.selectbox("Squadra Casa", df['Squadra'].unique())
    a_team = col2.selectbox("Squadra Fuori", df['Squadra'].unique())
    linea = col3.number_input("Linea Bookmaker", value=23.5)

    if st.button("GENERA PREVISIONE PROFESSIONALE"):
        h = df[df['Squadra'] == h_team].iloc[0]
        a = df[df['Squadra'] == a_team].iloc[0]

        # CALCOLO DELLE MEDIE (Così non esce 48!)
        # Udinese in Casa
        m_fatti_h = h['Tiri Fatti Casa'] / h['Partite Casa'] if h['Partite Casa'] > 0 else 0
        m_subiti_h = h['Tiri Subiti Casa'] / h['Partite Casa'] if h['Partite Casa'] > 0 else 0
        
        # Parma in Fuori
        m_fatti_a = a['Tiri Fatti Trasferta'] / a['Partite Trasferta'] if a['Partite Trasferta'] > 0 else 0
        m_subiti_a = a['Tiri Subiti Trasferta'] / a['Partite Trasferta'] if a['Partite Trasferta'] > 0 else 0

        # Calcolo incrociato: Quanto tira la squadra + Quanto concede l'avversario
        previsione_h = (m_fatti_h + m_subiti_a) / 2
        previsione_a = (m_fatti_a + m_subiti_h) / 2
        totale_match = previsione_h + previsione_a

        # --- RISULTATO PER I CLIENTI ---
        c1, c2 = st.columns(2)
        c1.metric(f"Tiri previsti {h_team}", f"{previsione_h:.2f}")
        c2.metric(f"Tiri previsti {a_team}", f"{previsione_a:.2f}")
        
        st.subheader(f"TOTALE STIMATO: {totale_match:.2f}")

        if totale_match > (linea + 0.5):
            st.success(f"CONSIGLIO: OVER {linea}")
        elif totale_match < (linea - 0.5):
            st.error(f"CONSIGLIO: UNDER {linea}")
        else:
            st.warning("NO BET: Valore troppo vicino alla linea")
