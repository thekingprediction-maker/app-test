import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE STREAMLIT ---
st.set_page_config(page_title="ProBet AI V3 - FULL API", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
iframe { width: 100vw !important; height: 100vh !important; border: none !important; display: block !important; position: fixed; top: 0; left: 0; z-index: 9999; }
</style>
""", unsafe_allow_html=True)

# --- CODICE HTML/JS ---
html_code = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <title>ProBet AI V3 - Pro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@400;600&family=Inter:wght@400;600;700;800&display=swap');
        
        body { background-color: #0c111d; color: #e2e8f0; font-family: 'Inter', sans-serif; margin: 0; padding: 0; width: 100%; height: 100%; overflow-x: hidden; }
        .teko { font-family: 'Teko', sans-serif; }
        
        select { background-color: #1e293b; color: white; border: 1px solid #334155; padding: 12px; border-radius: 12px; width: 100%; font-weight: 700; outline: none; appearance: none; }
        .input-dark { background: #1e293b; border: 1px solid #334155; color: white; padding: 10px; border-radius: 10px; width: 100%; text-align: center; font-weight: 800; font-size: 1.1rem; }

        .value-box { padding: 20px; border-radius: 18px; text-align: center; border: 1px solid; position: relative; background: #1a2236; border-color: #2d3748; transition: all 0.3s ease; }
        .val-top { background: linear-gradient(135deg, #064e3b 0%, #064e3b 100%); border-color: #10b981; box-shadow: 0 0 20px rgba(16, 185, 129, 0.2); }
        .val-good { background: linear-gradient(135deg, #78350f 0%, #78350f 100%); border-color: #f59e0b; }
        .res-text { font-size: 28px; font-weight: 900; font-family: 'Teko', sans-serif; line-height: 1; margin-bottom: 2px; }
        .tag-pill { position: absolute; top: 10px; right: 10px; font-size: 10px; background: #fff; color: #000; padding: 2px 8px; border-radius: 20px; font-weight: 900; }

        header { position: fixed; top: 0; left: 0; width: 100%; z-index: 100; background: rgba(12, 17, 29, 0.95); backdrop-filter: blur(10px); border-bottom: 1px solid #1e293b; }
        main { padding: 100px 16px 80px; max-width: 850px; margin: 0 auto; }

        .btn-main { background: #2563eb; color: white; font-weight: 900; width: 100%; padding: 18px; border-radius: 15px; font-size: 1.25rem; transition: all 0.2s; box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4); }
        .btn-main:active { scale: 0.97; }
        
        .loader { width: 18px; height: 18px; border: 3px solid #475569; border-bottom-color: #3b82f6; border-radius: 50%; display: inline-block; animation: rot 1s linear infinite; }
        @keyframes rot { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>

<header>
    <div class="max-w-6xl mx-auto px-6 h-20 flex items-center justify-between">
        <div class="text-3xl font-bold teko tracking-wider text-white">PROBET <span class="text-blue-500">AI</span> <span class="text-[12px] opacity-50 ml-2">V3.5 FULL AUTO</span></div>
        <div id="status-display" class="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-900 border border-slate-800">
            <div class="loader"></div> 
            <span class="text-[11px] font-black text-slate-400 uppercase">Connecting API...</span>
        </div>
    </div>
</header>

<main>
    <!-- Selettore Lega -->
    <div class="flex justify-center mb-8 bg-slate-900/50 p-1 rounded-2xl border border-slate-800 w-full max-w-sm mx-auto shadow-xl">
        <button onclick="switchLeague('SERIE_A')" id="btn-sa" class="flex-1 py-3 text-xs font-black rounded-xl transition-all">SERIE A</button>
        <button onclick="switchLeague('PREMIER')" id="btn-pl" class="flex-1 py-3 text-xs font-black rounded-xl transition-all">PREMIER</button>
        <button onclick="switchLeague('LIGA')" id="btn-lg" class="flex-1 py-3 text-xs font-black rounded-xl transition-all">LIGA</button>
    </div>

    <!-- Pannello Input -->
    <div class="bg-slate-900/40 p-8 rounded-[2rem] border border-slate-800/80 shadow-2xl backdrop-blur-md mb-10">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
            <div>
                <label class="text-[11px] font-black text-slate-500 uppercase tracking-widest ml-1 mb-3 block">Match Casa</label>
                <select id="home-team"></select>
            </div>
            <div>
                <label class="text-[11px] font-black text-slate-500 uppercase tracking-widest ml-1 mb-3 block">Match Ospite</label>
                <select id="away-team"></select>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
            <div class="bg-black/30 p-6 rounded-2xl border border-red-500/10">
                <span class="text-[11px] font-black text-red-400 uppercase tracking-widest block mb-4">Bookmaker Lines - Fouls</span>
                <input type="number" id="line-f-match" value="24.5" step="0.5" class="input-dark border-red-500/20">
            </div>
            <div class="bg-black/30 p-6 rounded-2xl border border-blue-500/10">
                <span class="text-[11px] font-black text-blue-400 uppercase tracking-widest block mb-4">Bookmaker Lines - Shots</span>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="text-[9px] text-slate-600 block mb-1 font-bold text-center">TOTAL SHOTS</label>
                        <input type="number" id="line-t-match" value="23.5" step="0.5" class="input-dark border-blue-500/20">
                    </div>
                    <div>
                        <label class="text-[9px] text-slate-600 block mb-1 font-bold text-center">ON GOAL</label>
                        <input type="number" id="line-tp-match" value="8.5" step="0.5" class="input-dark border-blue-500/20">
                    </div>
                </div>
            </div>
        </div>

        <button id="btn-calc" onclick="processAnalysis()" class="btn-main">ANALIZZA DATI</button>
    </div>

    <!-- Risultati -->
    <div id="results-area" class="hidden space-y-12">
        <section id="s-fouls">
            <div class="flex items-center gap-3 mb-6">
                <div class="w-1.5 h-6 bg-red-500 rounded-full"></div>
                <span class="text-base font-black text-white uppercase tracking-widest">ANALISI FALLI</span>
            </div>
            <div id="res-grid-falli" class="grid grid-cols-1 md:grid-cols-3 gap-4"></div>
        </section>

        <section id="s-shots">
            <div class="flex items-center gap-3 mb-6">
                <div class="w-1.5 h-6 bg-blue-500 rounded-full"></div>
                <span class="text-base font-black text-white uppercase tracking-widest">ANALISI TIRI</span>
            </div>
            <div id="res-grid-tiri" class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4"></div>
            <div id="res-grid-tp" class="grid grid-cols-1 md:grid-cols-3 gap-4"></div>
        </section>
    </div>
</main>

<script>
// --- CONFIGURAZIONE ---
const API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3"; 
const LEAGUE_IDS = { SERIE_A: 135, LIGA: 140, PREMIER: 39 };

let DB = { teams: [], cache: {} };
let CUR_L = 'SERIE_A';

document.addEventListener('DOMContentLoaded', () => switchLeague('SERIE_A'));

async function switchLeague(l) {
    CUR_L = l;
    const status = document.getElementById('status-display');
    
    // UI Bottoni
    ['btn-sa', 'btn-pl', 'btn-lg'].forEach(b => {
        const el = document.getElementById(b);
        if(b === `btn-${l.substring(0,2).toLowerCase()}` || (b === 'btn-sa' && l === 'SERIE_A')) {
            el.className = "flex-1 py-3 text-xs font-black rounded-xl bg-blue-600 text-white shadow-lg";
        } else {
            el.className = "flex-1 py-3 text-xs font-black rounded-xl text-slate-500 hover:text-slate-300";
        }
    });

    status.innerHTML = `<div class="loader"></div> <span class="text-[11px] font-black text-slate-400 uppercase">Updating League...</span>`;
    
    try {
        const teamsRes = await fetch(`https://v3.football.api-sports.io/teams?league=${LEAGUE_IDS[l]}&season=2024`, {
            headers: { "x-apisports-key": API_KEY }
        });
        const data = await teamsRes.json();
        
        if (data.errors && Object.keys(data.errors).length > 0) throw new Error(JSON.stringify(data.errors));

        DB.teams = data.response.map(r => ({ id: r.team.id, name: r.team.name })).sort((a,b) => a.name.localeCompare(b.name));

        const h = document.getElementById('home-team'), a = document.getElementById('away-team');
        h.innerHTML = ''; a.innerHTML = '';
        DB.teams.forEach(t => { 
            h.add(new Option(t.name, t.id)); 
            a.add(new Option(t.name, t.id)); 
        });
        if(DB.teams.length > 1) a.selectedIndex = 1;

        status.innerHTML = `<span class="w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.5)]"></span><span class="text-emerald-400 text-[11px] font-black uppercase">API CONNECTED: 2024 SEASON</span>`;
    } catch(err) {
        console.error(err);
        status.innerHTML = `<span class="text-red-500 text-[11px] font-black uppercase tracking-tighter">API Error: Check Console</span>`;
    }
}

async function fetchStats(teamId) {
    const key = `${CUR_L}_24_${teamId}`;
    if (DB.cache[key]) return DB.cache[key];

    const res = await fetch(`https://v3.football.api-sports.io/teams/statistics?league=${LEAGUE_IDS[CUR_L]}&season=2024&team=${teamId}`, {
        headers: { "x-apisports-key": API_KEY }
    });
    const data = await res.json();
    
    if (data.errors && Object.keys(data.errors).length > 0) throw new Error("API Limit reached");

    DB.cache[key] = data.response;
    return data.response;
}

// Funzione Helper per estrarre valori annidati in sicurezza
const getSafe = (obj, path, def = 0) => {
    return path.split('.').reduce((o, key) => (o && o[key] !== undefined) ? o[key] : null, obj) || def;
};

async function processAnalysis() {
    const btn = document.getElementById('btn-calc');
    const hId = document.getElementById('home-team').value, aId = document.getElementById('away-team').value;
    const hName = document.getElementById('home-team').options[document.getElementById('home-team').selectedIndex].text;
    const aName = document.getElementById('away-team').options[document.getElementById('away-team').selectedIndex].text;

    if(hId === aId) { alert("Scegli squadre diverse"); return; }

    btn.disabled = true;
    btn.innerHTML = `<div class="loader"></div> CONNECTING API...`;

    try {
        const [hS, aS] = await Promise.all([fetchStats(hId), fetchStats(aId)]);

        // 1. Partite giocate
        const mH = getSafe(hS, 'fixtures.played.home', 1);
        const mA = getSafe(aS, 'fixtures.played.away', 1);

        // 2. Calcolo Falli
        // Exp Falli Casa = (Falli Commessi Casa TeamH + Falli Subiti Trasferta TeamA) / 2
        const fCommH = getSafe(hS, 'fouls.committed.total.home', 12) / mH;
        const fSubA = getSafe(aS, 'fouls.drawn.total.away', 12) / mA;
        const expFalliH = (fCommH + fSubA) / 2;

        const fCommA = getSafe(aS, 'fouls.committed.total.away', 12) / mA;
        const fSubH = getSafe(hS, 'fouls.drawn.total.home', 12) / mH;
        const expFalliA = (fCommA + fSubH) / 2;

        // 3. Calcolo Tiri (Stessa logica del CSV)
        // Poichè l'API non fornisce tiri subiti casa/trasferta, usiamo medie di lega se non disponibili
        const tFattiH = getSafe(hS, 'shots.total.home', 12) / mH;
        const tFattiA = getSafe(aS, 'shots.total.away', 11) / mA;
        
        // Approssimazione tiri subiti basata sulla media team se il valore è mancante
        const tSubA = 11.5; // Media standard league
        const tSubH = 11.5; 
        
        const expTiriH = (tFattiH + tSubA) / 2;
        const expTiriA = (tFattiA + tSubH) / 2;

        // 4. Porta
        const tpFattiH = getSafe(hS, 'shots.on_goal.home', 4) / mH;
        const tpFattiA = getSafe(aS, 'shots.on_goal.away', 3.5) / mA;
        const tpSubA = 4.0;
        const tpSubH = 4.0;

        const expTpH = (tpFattiH + tpSubA) / 2;
        const expTpA = (tpFattiA + tpSubH) / 2;

        renderResults(hName, aName, expFalliH, expFalliA, expTiriH, expTiriA, expTpH, expTpA);
        
        document.getElementById('results-area').classList.remove('hidden');
        window.scrollTo({ top: document.getElementById('results-area').offsetTop - 80, behavior: 'smooth' });

    } catch(err) {
        console.error(err);
        alert("API Error: Limit reached or connection lost.");
    }

    btn.disabled = false;
    btn.innerHTML = "ANALIZZA DATI";
}

function renderResults(h, a, efh, efa, eth, eta, eph, epa) {
    const lF = parseFloat(document.getElementById('line-f-match').value);
    const lT = parseFloat(document.getElementById('line-t-match').value);
    const lP = parseFloat(document.getElementById('line-tp-match').value);

    // Griglie
    document.getElementById('res-grid-falli').innerHTML = 
        createCard("MATCH TOTALE", efh + efa, lF) + createCard(h, efh, lF/2) + createCard(a, efa, lF/2);

    document.getElementById('res-grid-tiri').innerHTML = 
        createCard("TIRI TOTALI", eth + eta, lT) + createCard(h, eth, eth>12?12.5:10.5) + createCard(a, eta, eta>10?10.5:8.5);

    document.getElementById('res-grid-tp').innerHTML = 
        createCard("TIRI IN PORTA", eph + epa, lP) + createCard(h, eph, 4.5) + createCard(a, epa, 3.5);
}

function createCard(title, val, line) {
    const diff = val - line;
    let style = "border-slate-800", rec = "UNDER " + line, tag = "";
    
    // Logica Under/Over
    if(diff >= 1.5) { style = "val-top"; rec = "OVER " + line; tag = "TOP"; }
    else if(diff >= 0.5) { style = "val-good"; rec = "OVER " + line; tag = "SUPER VALORE"; }
    else if(diff <= -1.5) { style = "val-top"; rec = "UNDER " + line; tag = "TOP"; }
    else if(diff <= -0.5) { style = "val-good"; rec = "UNDER " + line; tag = "SUPER VALORE"; }
    else { rec = (val > line ? "OVER " : "UNDER ") + line; }

    return `
        <div class="value-box ${style}">
            ${tag ? `<div class="tag-pill">${tag}</div>` : ''}
            <div class="text-[11px] font-black text-slate-500 uppercase mb-3 tracking-widest">${title}</div>
            <div class="res-text">${rec}</div>
            <div class="text-[12px] font-bold opacity-75">AI SUGGERISCE: ${val.toFixed(2)}</div>
        </div>
    `;
}
</script>
</body>
</html>
"""

components.html(html_code, height=1400, scrolling=True)
