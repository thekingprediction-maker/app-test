import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import time

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="ProBet AI", layout="wide", initial_sidebar_state="collapsed")

# NASCONDI TUTTO LO STREAMLIT NATIVO
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
}
.stSpinner, .stAlert, .stProgress, .stException, .stError {
    display: none !important;
}
iframe {
    width: 100vw !important;
    height: 100vh !important;
    border: none !important;
    display: block !important;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 9999;
}
div[data-testid="stHeader"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURAZIONE API ---
API_KEY = st.secrets.get("API_KEY", "028b02ea1d97fdd09cf5f4a89f6860b3"
BASE_URL = "https://v3.football.api-sports.io"

LEAGUES = {
    'SERIE_A': {'id': 135, 'season': 2025, 'name': 'Serie A'},
    'PREMIER': {'id': 39, 'season': 2025, 'name': 'Premier League'},
    'LIGA': {'id': 140, 'season': 2025, 'name': 'La Liga'}
}

# --- FUNZIONI API CON GESTIONE ERRORI ---
def get_teams(league_id, season):
    """Recupera squadre con gestione errori"""
    headers = {'x-apisports-key': API_KEY}
    try:
        r = requests.get(
            f"{BASE_URL}/teams?league={league_id}&season={season}", 
            headers=headers, 
            timeout=15
        )
        if r.status_code != 200:
            return {"error": f"HTTP {r.status_code}", "teams": []}
        
        data = r.json()
        if data.get('response'):
            teams = [{'id': t['team']['id'], 'name': t['team']['name']} for t in data['response']]
            return {"teams": teams, "error": None}
        return {"teams": [], "error": "Nessun dato"}
    except Exception as e:
        return {"teams": [], "error": str(e)}

def get_team_stats(team_id, league_id, season):
    """Recupera statistiche con gestione errori"""
    headers = {'x-apisports-key': API_KEY}
    
    stats = {
        'matches_home': 0, 'matches_away': 0,
        'shots_for_home': 0, 'shots_for_away': 0,
        'shots_against_home': 0, 'shots_against_away': 0,
        'shots_on_for_home': 0, 'shots_on_for_away': 0,
        'shots_on_against_home': 0, 'shots_on_against_away': 0,
        'fouls_for_home': 0, 'fouls_for_away': 0,  # Per piano pagamento
        'fouls_against_home': 0, 'fouls_against_away': 0,
        'yellows_for_home': 0, 'yellows_for_away': 0,
        'reds_for_home': 0, 'reds_for_away': 0
    }
    
    try:
        # Fixtures giocate
        fix_r = requests.get(
            f"{BASE_URL}/fixtures?league={league_id}&season={season}&team={team_id}&status=FT", 
            headers=headers, 
            timeout=15
        )
        fixtures = fix_r.json().get('response', [])
        
        if not fixtures:
            return None
            
        for f in fixtures:
            fid = f['fixture']['id']
            is_home = f['teams']['home']['id'] == team_id
            
            stat_r = requests.get(
                f"{BASE_URL}/fixtures/statistics?fixture={fid}", 
                headers=headers, 
                timeout=10
            )
            stat_data = stat_r.json().get('response', [])
            
            if len(stat_data) == 2:
                my_idx = 0 if stat_data[0]['team']['id'] == team_id else 1
                opp_idx = 1 - my_idx
                
                def get_val(s_list, label):
                    for s in s_list.get('statistics', []):
                        if s['type'] == label:
                            return s['value'] or 0
                    return 0
                
                if is_home:
                    stats['matches_home'] += 1
                    stats['shots_for_home'] += get_val(stat_data[my_idx], "Total Shots")
                    stats['shots_against_home'] += get_val(stat_data[opp_idx], "Total Shots")
                    stats['shots_on_for_home'] += get_val(stat_data[my_idx], "Shots on Goal")
                    stats['shots_on_against_home'] += get_val(stat_data[opp_idx], "Shots on Goal")
                    # Dati falli - piano pagamento
                    stats['fouls_for_home'] += get_val(stat_data[my_idx], "Fouls")
                    stats['fouls_against_home'] += get_val(stat_data[opp_idx], "Fouls")
                    stats['yellows_for_home'] += get_val(stat_data[my_idx], "Yellow Cards")
                    stats['reds_for_home'] += get_val(stat_data[my_idx], "Red Cards")
                else:
                    stats['matches_away'] += 1
                    stats['shots_for_away'] += get_val(stat_data[my_idx], "Total Shots")
                    stats['shots_against_away'] += get_val(stat_data[opp_idx], "Total Shots")
                    stats['shots_on_for_away'] += get_val(stat_data[my_idx], "Shots on Goal")
                    stats['shots_on_against_away'] += get_val(stat_data[opp_idx], "Shots on Goal")
                    # Dati falli - piano pagamento
                    stats['fouls_for_away'] += get_val(stat_data[my_idx], "Fouls")
                    stats['fouls_against_away'] += get_val(stat_data[opp_idx], "Fouls")
                    stats['yellows_for_away'] += get_val(stat_data[my_idx], "Yellow Cards")
                    stats['reds_for_away'] += get_val(stat_data[my_idx], "Red Cards")
        
        return stats
        
    except Exception as e:
        print(f"Errore stats team {team_id}: {e}")
        return None

# --- CARICAMENTO DATI ---
@st.cache_data(ttl=1800)
def load_all_league_data(league_key):
    """Carica tutti i dati di una lega"""
    league = LEAGUES[league_key]
    
    # Check API key
    if API_KEY == "INSERISCI_API_KEY_QUI" or not API_KEY:
        return {"error": "API KEY MANCANTE", "teams": []}
    
    teams_result = get_teams(league['id'], league['season'])
    if teams_result.get("error"):
        return {"error": teams_result["error"], "teams": []}
    
    teams_data = []
    for t in teams_result["teams"]:
        stats = get_team_stats(t['id'], league['id'], league['season'])
        if stats and (stats['matches_home'] > 0 or stats['matches_away'] > 0):
            teams_data.append({
                'name': t['name'],
                'id': t['id'],
                'stats': stats
            })
        time.sleep(0.1)  # Rate limiting
    
    return {"teams": teams_data, "error": None}

# --- SESSION STATE ---
if 'current_league' not in st.session_state:
    st.session_state.current_league = 'SERIE_A'
if 'data_cache' not in st.session_state:
    st.session_state.data_cache = {}

current_league = st.session_state.current_league

# Carica dati se non in cache
if current_league not in st.session_state.data_cache:
    with st.spinner():
        result = load_all_league_data(current_league)
        st.session_state.data_cache[current_league] = result

league_data = st.session_state.data_cache.get(current_league, {"teams": [], "error": "Nessun dato"})
teams_list = league_data.get("teams", [])
error_msg = league_data.get("error")

# Prepara JSON per JavaScript
teams_json = json.dumps(teams_list)
error_json = json.dumps(error_msg if error_msg else "")

# --- HTML/JS COMPLETO ---
html_template = f"""
<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
<title>ProBet AI</title>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://unpkg.com/lucide@latest"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Teko:wght@400;600&family=Inter:wght@400;600;700;800&display=swap');
html, body {{
    background-color: #0f172a;
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow-x: hidden;
    -webkit-tap-highlight-color: transparent;
}}
.teko {{ font-family: 'Teko', sans-serif; }}
select {{
    background-color: #1e293b;
    color: white;
    border: 1px solid #334155;
    padding: 12px;
    border-radius: 8px;
    width: 100%;
    font-weight: bold;
    appearance: none;
    outline: none;
    cursor: pointer;
}}
.input-dark {{
    background:#1e293b;
    border:1px solid #334155;
    color:white;
    padding:8px;
    border-radius:6px;
    width:100%;
    text-align:center;
    font-weight:700;
}}
.value-box {{
    padding:12px;
    border-radius:10px;
    margin-bottom:8px;
    text-align:center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    border:1px solid;
    position:relative;
    overflow:hidden;
}}
.val-high {{
    background: linear-gradient(135deg,#15803d 0%,#166534 100%);
    color:white;
    border-color:#22c55e;
}}
.val-med {{
    background: linear-gradient(135deg,#ca8a04 0%,#a16207 100%);
    color:#fff;
    border-color:#facc15;
}}
.val-low {{
    background: linear-gradient(135deg,#b91c1c 0%,#991b1b 100%);
    color:white;
    border-color:#ef4444;
}}
.res {{
    font-size:22px;
    font-weight:900;
    margin:2px 0;
    font-family:'Teko',sans-serif;
    line-height:1;
}}
.prob-badge {{
    font-size:10px;
    background:rgba(0,0,0,0.3);
    padding:2px 6px;
    border-radius:4px;
    display:inline-block;
    margin-top:4px;
    font-weight:700;
}}
.confidence-pill {{
    position:absolute;
    top:6px;
    right:6px;
    font-size:10px;
    background:#fff;
    color:#000;
    padding:3px 7px;
    border-radius:12px;
    font-weight:800;
    box-shadow:0 2px 4px rgba(0,0,0,0.2);
}}
.loader {{
    width:14px;
    height:14px;
    border:2px solid #475569;
    border-bottom-color:#3b82f6;
    border-radius:50%;
    display:inline-block;
    animation:rotation 1s linear infinite;
}}
@keyframes rotation {{
    0% {{ transform:rotate(0deg);}}
    100% {{ transform:rotate(360deg);}}
}}
header {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 50;
    background-color: rgba(15, 23, 42, 0.95);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid #1e293b;
}}
main {{
    padding-top: 80px;
    padding-bottom: 40px;
    padding-left: 16px;
    padding-right: 16px;
    max-width: 800px;
    margin: 0 auto;
}}
.api-status {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 700;
}}
.status-loading {{ background: #1e293b; color: #94a3b8; }}
.status-ready {{ background: #064e3b; color: #34d399; }}
.status-error {{ background: #450a0a; color: #f87171; }}
.warning-box {{
    background: #451a03;
    border: 1px solid #92400e;
    color: #fbbf24;
    padding: 16px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 20px;
    font-size: 14px;
}}
.hidden {{ display: none !important; }}
</style>
</head>
<body>
<header>
<div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
    <div class="flex items-center gap-3">
        <div class="text-2xl font-bold teko text-white tracking-wide">PROBET <span class="text-blue-500">AI</span></div>
    </div>
    <div id="status-pill" class="api-status status-loading">
        <div class="loader"></div> 
        <span>CARICAMENTO...</span>
    </div>
</div>
</header>

<main>
<div id="warning-box" class="warning-box hidden"></div>

<div class="flex justify-center mb-6">
    <div class="bg-slate-900 p-1 rounded-xl border border-slate-800 flex gap-2 w-full max-w-sm shadow-lg">
        <button onclick="switchLeague('SERIE_A')" id="btn-sa" class="flex-1 py-3 text-xs font-bold rounded-lg transition-all">SERIE A</button>
        <button onclick="switchLeague('PREMIER')" id="btn-pl" class="flex-1 py-3 text-xs font-bold rounded-lg transition-all">PREMIER</button>
        <button onclick="switchLeague('LIGA')" id="btn-lg" class="flex-1 py-3 text-xs font-bold rounded-lg transition-all">LIGA</button>
    </div>
</div>

<div class="bg-slate-900 p-5 rounded-2xl border border-slate-800 shadow-xl mb-8">
    <div class="grid grid-cols-1 gap-4 mb-5">
        <div>
            <label class="text-[10px] font-bold text-slate-500 uppercase ml-1">CASA</label>
            <select id="home" class="mt-1"><option>Caricamento...</option></select>
        </div>
        <div>
            <label class="text-[10px] font-bold text-slate-500 uppercase ml-1">OSPITE</label>
            <select id="away" class="mt-1"><option>Caricamento...</option></select>
        </div>
        <div id="ref-box" class="hidden">
            <label class="text-[10px] font-bold text-slate-500 uppercase ml-1">ARBITRO (Piano Pro)</label>
            <select id="referee" class="mt-1 text-yellow-400">
                <option>Seleziona Arbitro</option>
            </select>
        </div>
    </div>
    
    <hr class="border-slate-800 mb-5 opacity-50">
    
    <details class="group bg-black/20 p-4 rounded-xl border border-slate-800/50 mb-5" open>
        <summary class="flex justify-between items-center cursor-pointer font-bold text-slate-400 text-xs uppercase mb-2 select-none">
            <span class="flex items-center gap-2"><i data-lucide="edit-3" class="w-3 h-3"></i> Quote Bookmaker</span>
            <i data-lucide="chevron-down" class="w-4 h-4 transition-transform group-open:rotate-180"></i>
        </summary>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-3">
            <!-- Sezione Falli - visibile solo con dati -->
            <div id="box-falli-lines" class="bg-slate-950 p-3 rounded-lg border border-slate-800 hidden">
                <div class="text-[9px] font-bold text-red-400 uppercase mb-2 text-center border-b border-slate-800 pb-1">LINEE FALLI</div>
                <input type="number" id="line-f-match" value="24.5" step="0.5" class="input-dark mb-2 text-lg font-bold text-white">
                <div class="grid grid-cols-2 gap-2">
                    <input type="number" id="line-f-h" value="11.5" class="input-dark text-xs" placeholder="Casa">
                    <input type="number" id="line-f-a" value="11.5" class="input-dark text-xs" placeholder="Ospite">
                </div>
            </div>
            
            <div id="box-tiri-lines" class="bg-slate-950 p-3 rounded-lg border border-slate-800 md:col-span-3">
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <div class="text-[9px] font-bold text-blue-400 uppercase mb-2 text-center border-b border-slate-800 pb-1">TIRI TOTALI</div>
                        <input type="number" id="line-t-match" value="23.5" step="0.5" class="input-dark mb-2 font-bold text-white">
                        <div class="grid grid-cols-2 gap-2">
                            <input type="number" id="line-t-h" value="12.5" class="input-dark text-xs text-slate-300">
                            <input type="number" id="line-t-a" value="10.5" class="input-dark text-xs text-slate-300">
                        </div>
                    </div>
                    <div class="border-l border-slate-800 pl-4">
                        <div class="text-[9px] font-bold text-purple-400 uppercase mb-2 text-center border-b border-slate-800 pb-1">IN PORTA</div>
                        <input type="number" id="line-tp-match" value="8.5" step="0.5" class="input-dark mb-2 font-bold text-white">
                        <div class="grid grid-cols-2 gap-2">
                            <input type="number" id="line-tp-h" value="4.5" class="input-dark text-xs text-slate-300">
                            <input type="number" id="line-tp-a" value="3.5" class="input-dark text-xs text-slate-300">
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </details>
    
    <button onclick="calculate()" class="w-full py-4 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 text-white font-black text-xl rounded-xl shadow-[0_0_20px_rgba(59,130,246,0.3)] active:scale-95 transition-all flex justify-center items-center gap-2 transform active:scale-95 duration-100">
        <i data-lucide="zap" class="w-5 h-5 fill-white"></i> ANALIZZA DATI
    </button>
</div>

<div id="results" class="hidden pb-20">
    <div id="sec-falli" class="hidden">
        <div class="flex items-center gap-2 mb-3 mt-8 border-b border-slate-800 pb-2">
            <i data-lucide="alert-circle" class="text-red-400 w-4 h-4"></i>
            <span class="text-sm font-bold text-red-400 uppercase tracking-widest" id="title-falli">Analisi Falli</span>
        </div>
        <div id="grid-falli" class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-8"></div>
    </div>
    
    <div id="sec-tiri">
        <div class="flex items-center gap-2 mb-3 mt-8 border-b border-slate-800 pb-2">
            <i data-lucide="crosshair" class="text-blue-400 w-4 h-4"></i>
            <span class="text-sm font-bold text-blue-400 uppercase tracking-widest">Tiri Totali</span>
        </div>
        <div id="grid-tiri" class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-8"></div>
        
        <div class="flex items-center gap-2 mb-3 mt-8 border-b border-slate-800 pb-2">
            <i data-lucide="target" class="text-purple-400 w-4 h-4"></i>
            <span class="text-sm font-bold text-purple-400 uppercase tracking-widest">Tiri In Porta</span>
        </div>
        <div id="grid-tp" class="grid grid-cols-1 md:grid-cols-3 gap-3"></div>
    </div>
</div>
</main>

<script>
const TEAMS_DATA = {teams_json};
const ERROR_MSG = {error_json};
const CURRENT_LEAGUE = "{current_league}";

document.addEventListener('DOMContentLoaded', () => {{
    if(window.lucide) lucide.createIcons();
    initApp();
}});

function initApp() {{
    const pill = document.getElementById('status-pill');
    const warningBox = document.getElementById('warning-box');
    
    // Gestione errori/API key
    if(ERROR_MSG && ERROR_MSG.includes("API KEY")) {{
        pill.className = 'api-status status-error';
        pill.innerHTML = '<span>❌ API KEY MANCANTE</span>';
        warningBox.innerHTML = '⚠️ ' + ERROR_MSG + '<br><small>Inserisci la tua API key di API-Sports.io nelle secrets di Streamlit o nel codice</small>';
        warningBox.classList.remove('hidden');
        populateEmptySelectors();
        return;
    }}
    
    if(ERROR_MSG) {{
        pill.className = 'api-status status-error';
        pill.innerHTML = '<span>❌ ERRORE API</span>';
        warningBox.innerHTML = '⚠️ Errore: ' + ERROR_MSG;
        warningBox.classList.remove('hidden');
        populateEmptySelectors();
        return;
    }}
    
    if(!TEAMS_DATA || TEAMS_DATA.length === 0) {{
        pill.className = 'api-status status-loading';
        pill.innerHTML = '<div class="loader"></div><span>CARICAMENTO DATI...</span>';
        populateEmptySelectors();
        return;
    }}
    
    // Successo
    pill.className = 'api-status status-ready';
    pill.innerHTML = '<span class="w-2 h-2 rounded-full bg-emerald-500"></span><span>API CONNESSA • ' + TEAMS_DATA.length + ' SQUADRE</span>';
    warningBox.classList.add('hidden');
    
    populateSelectors();
    updateLeagueButtons(CURRENT_LEAGUE);
}}

function populateEmptySelectors() {{
    const h = document.getElementById('home');
    const a = document.getElementById('away');
    h.innerHTML = '<option value="">Nessun dato disponibile</option>';
    a.innerHTML = '<option value="">Nessun dato disponibile</option>';
}}

function populateSelectors() {{
    const h = document.getElementById('home');
    const a = document.getElementById('away');
    
    h.innerHTML = '<option value="">Seleziona Squadra Casa</option>';
    a.innerHTML = '<option value="">Seleziona Squadra Ospite</option>';
    
    TEAMS_DATA.forEach(t => {{
        h.add(new Option(t.name, t.name));
        a.add(new Option(t.name, t.name));
    }});
}}

function updateLeagueButtons(l) {{
    const act = "bg-blue-600 text-white shadow-lg";
    const inact = "text-slate-400 hover:bg-slate-800";
    
    document.getElementById('btn-sa').className = `flex-1 py-3 text-xs font-bold rounded-lg transition-all ${{l==='SERIE_A'?act:inact}}`;
    document.getElementById('btn-pl').className = `flex-1 py-3 text-xs font-bold rounded-lg transition-all ${{l==='PREMIER'?act:inact}}`;
    document.getElementById('btn-lg').className = `flex-1 py-3 text-xs font-bold rounded-lg transition-all ${{l==='LIGA'?act:inact}}`;
}}

function switchLeague(l) {{
    // Ricarica la pagina con nuova lega
    const url = new URL(window.location.href);
    url.searchParams.set('league', l);
    window.location.href = url.toString();
}}

function poisson(k, lambda) {{ 
    return (Math.pow(lambda, k) * Math.exp(-lambda)) / factorial(k); 
}}

function factorial(n) {{ 
    if (n===0 || n===1) return 1; 
    let r=1; 
    for(let i=2; i<=n; i++) r*=i; 
    return r; 
}}

function poissonProb(line, lambda, type) {{
    let pUnder = 0;
    for(let k=0; k<=Math.floor(line); k++) pUnder += poisson(k, lambda);
    return type==='OVER' ? (1-pUnder)*100 : pUnder*100;
}}

function calculate() {{
    const homeName = document.getElementById('home').value;
    const awayName = document.getElementById('away').value;
    
    if(!homeName || !awayName) {{
        alert("Seleziona entrambe le squadre");
        return;
    }}
    if(homeName === awayName) {{
        alert("Seleziona squadre diverse");
        return;
    }}
    
    const home = TEAMS_DATA.find(t => t.name === homeName);
    const away = TEAMS_DATA.find(t => t.name === awayName);
    
    if(!home || !away) {{
        alert("Dati squadre non disponibili");
        return;
    }}
    
    const hStats = home.stats;
    const aStats = away.stats;
    
    // Calcolo Tiri Totali
    const m_tf_h = hStats.matches_home > 0 ? hStats.shots_for_home / hStats.matches_home : 0;
    const m_ts_a = aStats.matches_away > 0 ? aStats.shots_against_away / aStats.matches_away : 0;
    const m_tf_a = aStats.matches_away > 0 ? aStats.shots_for_away / aStats.matches_away : 0;
    const m_ts_h = hStats.matches_home > 0 ? hStats.shots_against_home / hStats.matches_home : 0;
    
    const expTiriHome = (m_tf_h + m_ts_a) / 2;
    const expTiriAway = (m_tf_a + m_ts_h) / 2;
    const totTiri = expTiriHome + expTiriAway;
    
    // Calcolo Tiri In Porta
    const m_tipf_h = hStats.matches_home > 0 ? hStats.shots_on_for_home / hStats.matches_home : 0;
    const m_tips_a = aStats.matches_away > 0 ? hStats.shots_on_against_away / aStats.matches_away : 0;
    const m_tipf_a = aStats.matches_away > 0 ? hStats.shots_on_for_away / aStats.matches_away : 0;
    const m_tips_h = hStats.matches_home > 0 ? hStats.shots_on_against_home / hStats.matches_home : 0;
    
    const expTPHome = (m_tipf_h + m_tips_a) / 2;
    const expTPAway = (m_tipf_a + m_tips_h) / 2;
    const totTP = expTPHome + expTPAway;
    
    // Rendering
    document.getElementById('results').classList.remove('hidden');
    
    renderBox('grid-tiri', "MATCH TOTALE", totTiri, 'line-t-match');
    renderBox('grid-tiri', homeName, expTiriHome, 'line-t-h');
    renderBox('grid-tiri', awayName, expTiriAway, 'line-t-a');
    
    renderBox('grid-tp', "MATCH IN PORTA", totTP, 'line-tp-match');
    renderBox('grid-tp', homeName, expTPHome, 'line-tp-h');
    renderBox('grid-tp', awayName, expTPAway, 'line-tp-a');
    
    // Scroll ai risultati
    setTimeout(() => document.getElementById('results').scrollIntoView({{behavior:'smooth'}}), 100);
}}

function renderBox(id, title, val, lineId) {{
    const el = document.getElementById(id);
    if(!el) return;
    if(title.includes("MATCH")) el.innerHTML = "";
    
    const line = parseFloat(document.getElementById(lineId).value) || 23.5;
    const diff = val - line;
    let c = "val-low", t = "NO VALUE", r = "PASS", prob = 50;
    
    prob = poissonProb(line, val, diff > 0 ? 'OVER' : 'UNDER');
    let badge = prob > 65 ? `<span class="confidence-pill">⚡ HIGH CONFIDENCE</span>` : "";
    
    if(diff >= 1.5) {{
        c = "val-high";
        t = "SUPER VALORE";
        r = `OVER ${{line}}`;
    }} else if(diff >= 0.5) {{
        c = "val-med";
        t = "BUONO";
        r = `OVER ${{line}}`;
    }} else if(diff <= -1.5) {{
        c = "val-high";
        t = "SUPER VALORE";
        r = `UNDER ${{line}}`;
    }} else if(diff <= -0.5) {{
        c = "val-med";
        t = "BUONO";
        r = `UNDER ${{line}}`;
    }}
    
    if(Math.abs(diff) < 0.5) {{
        c = "bg-slate-800 border-slate-700";
        r = "PASS";
        t = "NO EDGE";
        prob = 50;
        badge = "";
    }}
    
    el.innerHTML += `<div class="value-box ${{c}} relative">${{badge}}<div class="lbl" style="font-size:10px; opacity:0.8">${{title}}</div><div class="res">${{r}}</div><div style="font-size:12px; font-weight:bold">AI: ${{val.toFixed(2)}} | ${{t}}</div><div class="prob-badge">Prob. ${{prob.toFixed(0)}}%</div></div>`;
}}
</script>
</body>
</html>
"""

components.html(html_template, height=1200, scrolling=True)

# Gestione cambio lega da URL
query_params = st.query_params
if 'league' in query_params:
    new_league = query_params['league']
    if new_league in LEAGUES and new_league != st.session_state.current_league:
        st.session_state.current_league = new_league
        st.rerun()
