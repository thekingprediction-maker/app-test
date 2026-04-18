import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import time
from datetime import datetime, timedelta

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
API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3"  # <-- LA TUA API KEY
BASE_URL = "https://v3.football.api-sports.io"

LEAGUES = {
    'SERIE_A': {'id': 135, 'season': 2025, 'name': 'Serie A'},
    'PREMIER': {'id': 39, 'season': 2025, 'name': 'Premier League'},
    'LIGA': {'id': 140, 'season': 2025, 'name': 'La Liga'}
}

# --- SESSION STATE PERSISTENTE ---
if 'current_league' not in st.session_state:
    st.session_state.current_league = 'SERIE_A'
if 'api_cache' not in st.session_state:
    st.session_state.api_cache = {}  # Cache persistente per tutta la sessione
if 'last_load' not in st.session_state:
    st.session_state.last_load = {}

current_league = st.session_state.current_league

# --- FUNZIONI API OTTIMIZZATE ---
def make_api_call(url, headers, max_retries=3):
    """Chiama API con retry e rate limiting"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=15)
            
            # Gestione rate limit
            if response.status_code == 429:
                wait_time = (attempt + 1) * 3
                time.sleep(wait_time)
                continue
                
            return response
        except Exception as e:
            if attempt == max_retries - 1:
                return None
            time.sleep(2)
    return None

def get_teams_fast(league_id, season):
    """Recupera squadre - 1 chiamata API"""
    cache_key = f"teams_{league_id}_{season}"
    
    # Check cache
    if cache_key in st.session_state.api_cache:
        return st.session_state.api_cache[cache_key]
    
    headers = {'x-apisports-key': API_KEY}
    url = f"{BASE_URL}/teams?league={league_id}&season={season}"
    
    response = make_api_call(url, headers)
    if not response or response.status_code != 200:
        return {"error": f"HTTP {response.status_code if response else 'ERROR'}", "teams": []}
    
    data = response.json()
    if not data.get('response'):
        return {"teams": [], "error": "Nessun dato"}
    
    teams = [{'id': t['team']['id'], 'name': t['team']['name']} for t in data['response']]
    result = {"teams": teams, "error": None}
    
    # Salva in cache
    st.session_state.api_cache[cache_key] = result
    return result

def get_all_fixtures_stats(league_id, season):
    """Recupera TUTTE le partite giocate della lega - ottimizzato"""
    cache_key = f"fixtures_{league_id}_{season}"
    
    if cache_key in st.session_state.api_cache:
        return st.session_state.api_cache[cache_key]
    
    headers = {'x-apisports-key': API_KEY}
    
    # Prendi tutte le partite giocate della lega (massimo 100 per pagina)
    all_fixtures = []
    page = 1
    
    while True:
        url = f"{BASE_URL}/fixtures?league={league_id}&season={season}&status=FT&per_page=100&page={page}"
        response = make_api_call(url, headers)
        
        if not response or response.status_code != 200:
            break
            
        data = response.json()
        fixtures = data.get('response', [])
        
        if not fixtures:
            break
            
        all_fixtures.extend(fixtures)
        
        if len(fixtures) < 100:
            break
            
        page += 1
        time.sleep(0.5)  # Rate limiting tra pagine
    
    # Ora recupera le statistiche per ogni partita
    fixtures_stats = {}
    total = len(all_fixtures)
    
    for i, fixture in enumerate(all_fixtures):
        fid = fixture['fixture']['id']
        home_id = fixture['teams']['home']['id']
        away_id = fixture['teams']['away']['id']
        
        # Check se abbiamo già questa partita in cache
        if fid in st.session_state.api_cache:
            fixtures_stats[fid] = st.session_state.api_cache[fid]
            continue
        
        url = f"{BASE_URL}/fixtures/statistics?fixture={fid}"
        response = make_api_call(url, headers)
        
        if response and response.status_code == 200:
            stat_data = response.json().get('response', [])
            if len(stat_data) == 2:
                fixtures_stats[fid] = {
                    'home_id': home_id,
                    'away_id': away_id,
                    'home_stats': stat_data[0],
                    'away_stats': stat_data[1]
                }
                # Cache individuale per partita
                st.session_state.api_cache[fid] = fixtures_stats[fid]
        
        # Progress ogni 10 partite
        if i % 10 == 0:
            time.sleep(0.3)  # Rate limiting
    
    result = {"fixtures": fixtures_stats, "count": len(fixtures_stats)}
    st.session_state.api_cache[cache_key] = result
    return result

def calculate_team_stats_from_fixtures(team_id, fixtures_data):
    """Calcola statistiche squadra dai dati fixtures già recuperati"""
    stats = {
        'matches_home': 0, 'matches_away': 0,
        'shots_for_home': 0, 'shots_for_away': 0,
        'shots_against_home': 0, 'shots_against_away': 0,
        'shots_on_for_home': 0, 'shots_on_for_away': 0,
        'shots_on_against_home': 0, 'shots_on_against_away': 0,
        'fouls_for_home': 0, 'fouls_for_away': 0,
        'fouls_against_home': 0, 'fouls_against_away': 0,
        'yellows_for_home': 0, 'yellows_for_away': 0,
        'reds_for_home': 0, 'reds_for_away': 0
    }
    
    def get_val(s_list, label):
        for s in s_list.get('statistics', []):
            if s['type'] == label:
                return s['value'] or 0
        return 0
    
    for fid, fdata in fixtures_data.items():
        is_home = fdata['home_id'] == team_id
        is_away = fdata['away_id'] == team_id
        
        if not (is_home or is_away):
            continue
        
        if is_home:
            my_stats = fdata['home_stats']
            opp_stats = fdata['away_stats']
            stats['matches_home'] += 1
            stats['shots_for_home'] += get_val(my_stats, "Total Shots")
            stats['shots_against_home'] += get_val(opp_stats, "Total Shots")
            stats['shots_on_for_home'] += get_val(my_stats, "Shots on Goal")
            stats['shots_on_against_home'] += get_val(opp_stats, "Shots on Goal")
            stats['fouls_for_home'] += get_val(my_stats, "Fouls")
            stats['fouls_against_home'] += get_val(opp_stats, "Fouls")
            stats['yellows_for_home'] += get_val(my_stats, "Yellow Cards")
            stats['reds_for_home'] += get_val(my_stats, "Red Cards")
        else:
            my_stats = fdata['away_stats']
            opp_stats = fdata['home_stats']
            stats['matches_away'] += 1
            stats['shots_for_away'] += get_val(my_stats, "Total Shots")
            stats['shots_against_away'] += get_val(opp_stats, "Total Shots")
            stats['shots_on_for_away'] += get_val(my_stats, "Shots on Goal")
            stats['shots_on_against_away'] += get_val(opp_stats, "Shots on Goal")
            stats['fouls_for_away'] += get_val(my_stats, "Fouls")
            stats['fouls_against_away'] += get_val(opp_stats, "Fouls")
            stats['yellows_for_away'] += get_val(my_stats, "Yellow Cards")
            stats['reds_for_away'] += get_val(my_stats, "Red Cards")
    
    return stats

def load_league_data_optimized(league_key):
    """Carica dati lega in modo ottimizzato - meno chiamate API"""
    league = LEAGUES[league_key]
    league_id = league['id']
    season = league['season']
    
    # Check se abbiamo già caricato questa lega recentemente
    cache_key = f"league_data_{league_key}"
    if cache_key in st.session_state.api_cache:
        return st.session_state.api_cache[cache_key]
    
    if not API_KEY:
        return {"error": "API KEY MANCANTE", "teams": []}
    
    # 1. Recupera squadre (1 chiamata)
    teams_result = get_teams_fast(league_id, season)
    if teams_result.get("error"):
        return {"error": teams_result["error"], "teams": []}
    
    # 2. Recupera TUTTE le partite e statistiche (circa 20-30 chiamate per lega intera)
    fixtures_data = get_all_fixtures_stats(league_id, season)
    
    if not fixtures_data or fixtures_data.get('count', 0) == 0:
        return {"error": "Nessuna partita trovata", "teams": []}
    
    # 3. Calcola statistiche per ogni squadra (0 chiamate - usa dati già recuperati)
    teams_data = []
    for team in teams_result['teams']:
        stats = calculate_team_stats_from_fixtures(team['id'], fixtures_data['fixtures'])
        
        # Solo squadre con almeno 3 partite giocate
        total_matches = stats['matches_home'] + stats['matches_away']
        if total_matches >= 3:
            teams_data.append({
                'name': team['name'],
                'id': team['id'],
                'stats': stats,
                'total_matches': total_matches
            })
    
    result = {
        "teams": teams_data, 
        "error": None,
        "last_update": datetime.now().isoformat()
    }
    
    # Salva in cache persistente
    st.session_state.api_cache[cache_key] = result
    return result

# --- CARICAMENTO DATI ---
cache_key = f"league_data_{current_league}"

if cache_key not in st.session_state.api_cache:
    with st.spinner():
        league_data = load_league_data_optimized(current_league)
else:
    league_data = st.session_state.api_cache[cache_key]

teams_list = league_data.get("teams", [])
error_msg = league_data.get("error")
last_update = league_data.get("last_update", "")

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
.cache-info {{
    background: #1e293b;
    border: 1px solid #334155;
    color: #94a3b8;
    padding: 8px 12px;
    border-radius: 8px;
    text-align: center;
    margin-bottom: 16px;
    font-size: 11px;
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
<div id="cache-info" class="cache-info hidden"></div>
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
    </div>
    
    <hr class="border-slate-800 mb-5 opacity-50">
    
    <details class="group bg-black/20 p-4 rounded-xl border border-slate-800/50 mb-5" open>
        <summary class="flex justify-between items-center cursor-pointer font-bold text-slate-400 text-xs uppercase mb-2 select-none">
            <span class="flex items-center gap-2"><i data-lucide="edit-3" class="w-3 h-3"></i> Quote Bookmaker</span>
            <i data-lucide="chevron-down" class="w-4 h-4 transition-transform group-open:rotate-180"></i>
        </summary>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-3">
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
const LAST_UPDATE = "{last_update}";

document.addEventListener('DOMContentLoaded', () => {{
    if(window.lucide) lucide.createIcons();
    initApp();
}});

function initApp() {{
    const pill = document.getElementById('status-pill');
    const warningBox = document.getElementById('warning-box');
    const cacheInfo = document.getElementById('cache-info');
    
    if(ERROR_MSG && ERROR_MSG.includes("API KEY")) {{
        pill.className = 'api-status status-error';
        pill.innerHTML = '<span>❌ API KEY MANCANTE</span>';
        warningBox.innerHTML = '⚠️ ' + ERROR_MSG + '<br><small>Inserisci la tua API key nel codice (riga 39)</small>';
        warningBox.classList.remove('hidden');
        populateEmptySelectors();
        return;
    }}
    
    if(ERROR_MSG) {{
        pill.className = 'api-status status-error';
        pill.innerHTML = '<span>❌ ERRORE API</span>';
        warningBox.innerHTML = '⚠️ Errore: ' + ERROR_MSG + '<br><small>Riprova tra qualche minuto (rate limit)</small>';
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
    
    // Mostra info cache
    if(LAST_UPDATE) {{
        const date = new Date(LAST_UPDATE);
        const timeStr = date.toLocaleTimeString('it-IT', {{hour: '2-digit', minute:'2-digit'}});
        cacheInfo.innerHTML = '📊 Dati aggiornati alle ' + timeStr + ' • In cache per questa sessione';
        cacheInfo.classList.remove('hidden');
    }}
    
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
    
    document.getElementById('results').classList.remove('hidden');
    
    renderBox('grid-tiri', "MATCH TOTALE", totTiri, 'line-t-match');
    renderBox('grid-tiri', homeName, expTiriHome, 'line-t-h');
    renderBox('grid-tiri', awayName, expTiriAway, 'line-t-a');
    
    renderBox('grid-tp', "MATCH IN PORTA", totTP, 'line-tp-match');
    renderBox('grid-tp', homeName, expTPHome, 'line-tp-h');
    renderBox('grid-tp', awayName, expTPAway, 'line-tp-a');
    
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

# Gestione cambio lega
query_params = st.query_params
if 'league' in query_params:
    new_league = query_params['league']
    if new_league in LEAGUES and new_league != st.session_state.current_league:
        st.session_state.current_league = new_league
        st.rerun()

# Pulsante per svuotare cache (utile se l'API si blocca)
if st.sidebar.button("🗑️ Svuota Cache API"):
    st.session_state.api_cache = {}
    st.rerun()
