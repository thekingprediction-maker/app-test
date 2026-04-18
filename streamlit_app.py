import streamlit as st
import requests
import pandas as pd
import time

# --- CONFIGURAZIONE ---
# Inserisci qui la tua chiave API-Football
API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3" 
BASE_URL = "https://v3.football.api-sports.io"
LEAGUE_ID = 135  # Serie A
SEASON = 2025

st.set_page_config(page_title="PROBET AI - Professional Dashboard", layout="wide")

# Stile CSS per rendere l'app professionale e scura
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stDataFrame { border: 1px solid #30363d; border-radius: 10px; }
    .stats-card { background-color: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 PROBET AI - Stagione 2025/26")
st.subheader("Database Automatico Tiri (Identico al CSV)")

# --- FUNZIONE RECUPERO DATI ---
def fetch_serie_a_data():
    headers = {'x-apisports-key': API_KEY}
    
    # 1. Prendo l'elenco squadre
    try:
        r_teams = requests.get(f"{BASE_URL}/teams?league={LEAGUE_ID}&season={SEASON}", headers=headers)
        teams_list = r_teams.json().get('response', [])
    except:
        st.error("Errore di connessione all'API. Controlla la tua chiave.")
        return None

    data_rows = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()

    for idx, item in enumerate(teams_list):
        t_id = item['team']['id']
        t_name = item['team']['name']
        status_text.text(f"Analisi in corso: {t_name}...")
        
        # Inizializzo riga come il tuo CSV
        row = {
            "Squadra": t_name, "Partite Casa": 0, "Tiri Fatti Casa": 0, "Tiri Subiti Casa": 0,
            "Tiri in porta Fatti Casa": 0, "Tiri in porta Subiti Casa": 0,
            "Partite Trasferta": 0, "Tiri Fatti Trasferta": 0, "Tiri Subiti Trasferta": 0,
            "Tiri in porta Fatti Trasferta": 0, "Tiri in porta Subiti Trasferta": 0
        }

        # 2. Prendo le ultime partite di questa squadra
        r_fix = requests.get(f"{BASE_URL}/fixtures?league={LEAGUE_ID}&season={SEASON}&team={t_id}", headers=headers)
        fixtures = r_fix.json().get('response', [])

        for f in fixtures:
            if f['fixture']['status']['short'] == 'FT':
                f_id = f['fixture']['id']
                is_home = f['teams']['home']['id'] == t_id
                
                if is_home: row["Partite Casa"] += 1
                else: row["Partite Trasferta"] += 1

                # 3. Prendo le statistiche dettagliate del match (Tiri Fatti e Subiti)
                r_stat = requests.get(f"{BASE_URL}/fixtures/statistics?fixture={f_id}", headers=headers)
                f_stats = r_stat.json().get('response', [])

                if len(f_stats) == 2:
                    # Individuo chi è la squadra corrente e chi l'avversario
                    my_idx = 0 if f_stats[0]['team']['id'] == t_id else 1
                    opp_idx = 1 - my_idx
                    
                    def get_val(stats_list, label):
                        for s in stats_list:
                            if s['type'] == label: return s['value'] if s['value'] is not None else 0
                        return 0

                    my_shots = get_val(f_stats[my_idx]['statistics'], "Total Shots")
                    my_on_goal = get_val(f_stats[my_idx]['statistics'], "Shots on Goal")
                    opp_shots = get_val(f_stats[opp_idx]['statistics'], "Total Shots")
                    opp_on_goal = get_val(f_stats[opp_idx]['statistics'], "Shots on Goal")

                    if is_home:
                        row["Tiri Fatti Casa"] += my_shots
                        row["Tiri in porta Fatti Casa"] += my_on_goal
                        row["Tiri Subiti Casa"] += opp_shots
                        row["Tiri in porta Subiti Casa"] += opp_on_goal
                    else:
                        row["Tiri Fatti Trasferta"] += my_shots
                        row["Tiri in porta Fatti Trasferta"] += my_on_goal
                        row["Tiri Subiti Trasferta"] += opp_shots
                        row["Tiri in porta Subiti Trasferta"] += opp_on_goal
        
        data_rows.append(row)
        progress_bar.progress((idx + 1) / len(teams_list))
        time.sleep(0.1) # Piccolo delay per non bloccare l'API

    return pd.DataFrame(data_rows)

# --- INTERFACCIA ---
if st.button("🔄 SINCRONIZZA DATABASE DALLE API"):
    df = fetch_serie_a_data()
    if df is not None:
        st.session_state['df_seriea'] = df
        st.success("Database aggiornato con successo!")

if 'df_seriea' in st.session_state:
    df = st.session_state['df_seriea']
    
    st.write("### Tabella Completa Dati Tiri")
    st.dataframe(df, use_container_width=True)

    # --- SEZIONE CALCOLO ---
    st.divider()
    st.header("🎯 Analizzatore Partita")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        home_choice = st.selectbox("Squadra in Casa", df['Squadra'].unique())
    with col2:
        away_choice = st.selectbox("Squadra Ospite", df['Squadra'].unique())
    with col3:
        linea = st.number_input("Linea Tiri Bookmaker", value=23.5, step=0.5)

    if st.button("CALCOLA PREVISIONE"):
        h_data = df[df['Squadra'] == home_choice].iloc[0]
        a_data = df[df['Squadra'] == away_choice].iloc[0]

        # Calcolo Medie (La tua formula)
        # Media Tiri Casa = (Fatti Casa + Subiti Casa) / Partite
        # Ma noi vogliamo incrociare: (Fatti Casa di uno + Subiti Trasferta dell'altro)
        
        m_fatti_h = h_data['Tiri Fatti Casa'] / h_data['Partite Casa'] if h_data['Partite Casa'] > 0 else 0
        m_subiti_h = h_data['Tiri Subiti Casa'] / h_data['Partite Casa'] if h_data['Partite Casa'] > 0 else 0
        
        m_fatti_a = a_data['Tiri Fatti Trasferta'] / a_data['Partite Trasferta'] if a_data['Partite Trasferta'] > 0 else 0
        m_subiti_a = a_data['Tiri Subiti Trasferta'] / a_data['Partite Trasferta'] if a_data['Partite Trasferta'] > 0 else 0

        stima_totale = (m_fatti_h + m_subiti_a) + (m_fatti_a + m_subiti_h)
        # Nota: Ho usato la somma delle medie incrociate, che è il calcolo più preciso.

        st.metric("Tiri Totali Stimati", f"{stima_totale:.2f}")

        if stima_totale > (linea + 1):
            st.success(f"CONSIGLIO: OVER {linea} (Valore Alto)")
        elif stima_totale < (linea - 1):
            st.error(f"CONSIGLIO: UNDER {linea} (Valore Alto)")
        else:
            st.warning("NESSUN VALORE CHIARO")

else:
    st.warning("Clicca sul tasto sopra per caricare i dati dall'API per la prima volta.")
