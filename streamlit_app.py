import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="PROBET AI V3 - TEST API", layout="wide", initial_sidebar_state="collapsed")

# CSS per rendere l'app a tutto schermo su Streamlit
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
    <title>ProBet AI - API Version</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@400;600;700&family=Inter:wght@400;600;700;800&display=swap');
        html, body { background-color: #050a18; color: #e2e8f0; font-family: 'Inter', sans-serif; margin: 0; padding: 0; width: 100%; height: 100%; overflow-x: hidden; }
        .teko { font-family: 'Teko', sans-serif; }
        select { background-color: #1e293b; color: white; border: 1px solid #334155; padding: 12px; border-radius: 8px; width: 100%; font-weight: bold; outline: none; appearance: none; }
        .input-dark { background:#1e293b; border:1px solid #334155; color:white; padding:8px; border-radius:6px; width:100%; text-align:center; font-weight:700; }
        .value-box { padding:14px; border-radius:12px; margin-bottom:8px; text-align:center; border:1px solid; position:relative; overflow:hidden; transition: all 0.3s ease; }
        .val-top { background: linear-gradient(135deg,#15803d 0%,#166534 100%); color:white; border-color:#22c55e; box-shadow: 0 0 15px rgba(34, 197, 94, 0.2); }
        .val-med { background: linear-gradient(135deg,#ca8a04 0%,#a16207 100%); color:#fff; border-color:#facc15; }
        .val-low { background: #1e293b; border-color: #334155; opacity: 0.7; }
        .res { font-size:26px; font-weight:900; font-family:'Teko',sans-serif; line-height: 1; margin: 4px 0; }
        .badge-top { position:absolute; top:8px; right:8px; font-size:9px; background:#fff; color:#000; padding:2px 6px; border-radius:4px; font-weight:900; }
        .loader { width:16px; height:16px; border:2px solid #475569; border-bottom-color:#3b82f6; border-radius:50%; display:inline-block; animation:rotation 1s linear infinite; }
        @keyframes rotation { 0% { transform:rotate(0deg);} 100% { transform:rotate(360deg);} }
        header { position: fixed; top: 0; left: 0; width: 100%; z-index: 50; background-color: rgba(5, 10, 24, 0.9); backdrop-filter: blur(12px); border-bottom: 1px solid #1e293b; }
        main { padding: 90px 16px 60px; max-width: 900px; margin: 0 auto; }
        .section-title { font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; color: #64748b; margin-bottom: 12px; border-left: 3px solid #3b82f6; padding-left: 8px; }
    </style>
</head>
<body>
<header>
    <div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <div class="text-2xl font-bold teko text-white tracking-widest">TEST API <span class="text-blue-500">PROBET AI V3</span></div>
        <div id="status-pill" class="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800">
            <div class="loader"></div> <span class="text-[10px] font-bold text-slate-400">CONNESSIONE...</span>
        </div>
    </div>
</header>

<main>
    <div class="flex justify-center mb-8">
        <div class="bg-slate-900 p-1 rounded-xl border border-slate-800 flex gap-1 w-full max-w-sm shadow-2xl">
            <button onclick="switchLeague('SERIE_A')" id="btn-sa" class="flex-1 py-3 text-[10px] font-black rounded-lg transition-all duration-200">SERIE A</button>
            <button onclick="switchLeague('PREMIER')" id="btn-pl" class="flex-1 py-3 text-[10px] font-black rounded-lg transition-all duration-200">PREMIER</button>
            <button onclick="switchLeague('LIGA')" id="btn-lg" class="flex-1 py-3 text-[10px] font-black rounded-lg transition-all duration-200">LIGA</button>
        </div>
    </div>

    <div class="bg-slate-900/50 p-6 rounded-3xl border border-slate-800 shadow-2xl mb-10">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div class="relative">
                <label class="text-[9px] font-bold text-slate-500 uppercase mb-1 block ml-1">SQUADRA CASA</label>
                <select id="home"><option>Caricamento...</option></select>
            </div>
            <div class="relative">
                <label class="text-[9px] font-bold text-slate-500 uppercase mb-1 block ml-1">SQUADRA OSPITE</label>
                <select id="away"><option>Caricamento...</option></select>
            </div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div class="bg-slate-950/50 p-4 rounded-2xl border border-slate-800">
                <div class="text-[9px] font-bold text-red-500/80 uppercase mb-3 text-center tracking-tighter">LINEE FALLI</div>
                <input type="number" id="line-f-match" value="24.5" step="0.5" class="input-dark mb-2 text-xl font-black">
                <div class="grid grid-cols-2 gap-2">
                    <input type="number" id="line-f-h" value="12.25" step="0.25" class="input-dark text-xs opacity-60">
                    <input type="number" id="line-f-a" value="12.25" step="0.25" class="input-dark text-xs opacity-60">
                </div>
            </div>
            <div class="bg-slate-950/50 p-4 rounded-2xl border border-slate-800 md:col-span-2">
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <div class="text-[9px] font-bold text-blue-400 uppercase mb-3 text-center">TIRI TOTALI</div>
                        <input type="number" id="line-t-match" value="23.5" step="0.5" class="input-dark mb-2 text-xl font-black">
                    </div>
                    <div>
                        <div class="text-[9px] font-bold text-purple-400 uppercase mb-3 text-center">TIRI IN PORTA</div>
                        <input type="number" id="line-tp-match" value="8.5" step="0.5" class="input-dark mb-2 text-xl font-black">
                    </div>
                </div>
            </div>
        </div>

        <button id="btn-analyze" onclick="calculate()" class="w-full py-5 bg-blue-600 hover:bg-blue-500 text-white font-black text-xl rounded-2xl shadow-xl transition-all duration-200 transform active:scale-95 flex justify-center items-center gap-3">
            <i data-lucide="zap" class="w-6 h-6 fill-white"></i> ANALIZZA DATI API
        </button>
    </div>

    <div id="results" class="hidden animate-in fade-in duration-500">
        <div class="section-title">Analisi Falli (CSV Storage)</div>
        <div id="grid-falli" class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10"></div>
        
        <div class="section-title">Analisi Tiri (API Sports)</div>
        <div id="grid-tiri" class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4"></div>
        <div id="grid-tp" class="grid grid-cols-1 md:grid-cols-3 gap-4 pb-20"></div>
    </div>
</main>

<script>
// ============================================================
// 🔑 INSERISCI LA TUA API KEY QUI SOTTO
// ============================================================
const API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3"; 
// ============================================================

const LEAGUE_IDS = { SERIE_A: 135, LIGA: 140, PREMIER: 39 };

const CSV_LINKS = {
    SERIE_A: {
        curr: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_CURR_SERIE_A%20-%20Foglio1.csv",
        prev: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_PREV_SERIE_A%20-%20DATI%20STAGIONE%202024_2025%20.csv"
    },
    LIGA: {
        curr: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_CURR_LIGA%20-%20Foglio1.csv",
        prev: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_PREV_LIGA%20%20-%20DATI%20STAGIONE%202024_2025.csv"
    },
    PREMIER: { curr: "", prev: "" }
};

let CURRENT_LEAGUE = 'SERIE_A';
let DB = { fc: [], fp: [], teams: [] };

document.addEventListener('DOMContentLoaded', () => {
    if(window.lucide) lucide.createIcons();
    switchLeague('SERIE_A');
});

function switchLeague(l) {
    CURRENT_LEAGUE = l;
    const active = "bg-blue-600 text-white shadow-lg", inactive = "text-slate-400 hover:bg-slate-800";
    document.getElementById('btn-sa').className = `flex-1 py-3 text-[10px] font-black rounded-lg transition-all ${l==='SERIE_A'?active:inactive}`;
    document.getElementById('btn-pl').className = `flex-1 py-3 text-[10px] font-black rounded-lg transition-all ${l==='PREMIER'?active:inactive}`;
    document.getElementById('btn-lg').className = `flex-1 py-3 text-[10px] font-black rounded-lg transition-all ${l==='LIGA'?active:inactive}`;
    
    loadData();
}

async function loadData() {
    const pill = document.getElementById('status-pill');
    pill.innerHTML = `<div class="loader"></div> <span class="text-[10px] font-bold text-slate-400">CARICAMENTO API...</span>`;
    
    try {
        // 1. Carica Squadre da API (Stagione 2024 per dati attuali)
        const teamsRes = await fetch(`https://v3.football.api-sports.io/teams?league=${LEAGUE_IDS[CURRENT_LEAGUE]}&season=2024`, {
            headers: { "x-apisports-key": API_KEY }
        });
        const teamsData = await teamsRes.json();
        
        if(!teamsData.response || teamsData.response.length === 0) throw new Error("No teams");
        
        DB.teams = teamsData.response.map(t => ({ id: t.team.id, name: t.team.name })).sort((a,b) => a.name.localeCompare(b.name));

        // 2. Carica Falli da CSV
        const L = CSV_LINKS[CURRENT_LEAGUE];
        if(L.curr) {
            const rawFc = await fetch(L.curr).then(r => r.text());
            DB.fc = Papa.parse(rawFc, {skipEmptyLines:true}).data.slice(1).map(r => ({Team:r[1], Loc:r[2], Sub:parseFloat(r[3])||0, Comm:parseFloat(r[4])||0}));
        }
        if(L.prev) {
            const rawFp = await fetch(L.prev).then(r => r.text());
            DB.fp = Papa.parse(rawFp, {skipEmptyLines:true}).data.slice(1).map(r => ({Team:r[1], Loc:r[2], Sub:parseFloat(r[3])||0, Comm:parseFloat(r[4])||0}));
        }

        updateSelectors();
        pill.innerHTML = `<span class="w-2 h-2 rounded-full bg-emerald-500"></span><span class="text-emerald-400 text-[10px] font-bold">API PRONTA</span>`;
    } catch(e) {
        pill.innerHTML = `<span class="w-2 h-2 rounded-full bg-red-500"></span><span class="text-red-400 text-[10px] font-bold">ERRORE API</span>`;
    }
}

function updateSelectors() {
    const h = document.getElementById('home'), a = document.getElementById('away');
    h.innerHTML = ''; a.innerHTML = '';
    DB.teams.forEach(t => {
        h.add(new Option(t.name, t.id));
        a.add(new Option(t.name, t.id));
    });
}

async function calculate() {
    const btn = document.getElementById('btn-analyze');
    const hId = document.getElementById('home').value;
    const aId = document.getElementById('away').value;
    const hName = document.getElementById('home').options[document.getElementById('home').selectedIndex].text;
    const aName = document.getElementById('away').options[document.getElementById('away').selectedIndex].text;
    
    if(hId === aId) return alert("Scegli due squadre diverse!");

    btn.disabled = true;
    btn.innerHTML = "<div class='loader mr-2'></div> ELABORAZIONE API...";

    try {
        // --- CHIAMATE STATISTICHE API ---
        const [hStatsRes, aStatsRes] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${LEAGUE_IDS[CURRENT_LEAGUE]}&season=2024&team=${hId}`, { headers: { "x-apisports-key": API_KEY } }),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${LEAGUE_IDS[CURRENT_LEAGUE]}&season=2024&team=${aId}`, { headers: { "x-apisports-key": API_KEY } })
        ]);
        
        const hS = await hStatsRes.json();
        const aS = await aStatsRes.json();

        const extract = (data, path) => {
            const parts = path.split('.');
            let v = data.response;
            for(let p of parts) v = v ? v[p] : 0;
            return parseFloat(v) || 0;
        };

        const playedH = extract(hS, 'fixtures.played.home') || 1;
        const playedA = extract(aS, 'fixtures.played.away') || 1;

        // Tiri fatti casa e fuori
        const shotsHomeFor = extract(hS, 'shots.total.home') / playedH;
        const shotsAwayFor = extract(aS, 'shots.total.away') / playedA;
        
        // Tiri in porta fatti casa e fuori
        const tpHomeFor = extract(hS, 'shots.on_goal.home') / playedH;
        const tpAwayFor = extract(aS, 'shots.on_goal.away') / playedA;

        // Se l'API non fornisce i subiti direttamente, stimiamo usando i dati della lega o medie cross
        // Qui usiamo i dati attuali per il test
        const expTiriMatch = shotsHomeFor + shotsAwayFor;
        const expTPMatch = tpHomeFor + tpAwayFor;

        renderResultsTiri(hName, aName, shotsHomeFor, shotsAwayFor, tpHomeFor, tpAwayFor);

        // --- FALLI (CSV) ---
        if(CURRENT_LEAGUE !== 'PREMIER') {
            const findF = (n, loc, db) => db.find(x => x.Team.toUpperCase().includes(n.toUpperCase().slice(0,5)) && x.Loc.includes(loc)) || {Comm:11.5, Sub:11.5};
            const fH = findF(hName, 'CASA', DB.fc);
            const fA = findF(aName, 'FUORI', DB.fc);
            const totalF = (fH.Comm + fA.Sub)/2 + (fA.Comm + fH.Sub)/2;
            renderResultsFalli(hName, aName, totalF);
        }

        document.getElementById('results').classList.remove('hidden');
        document.getElementById('results').scrollIntoView({behavior:'smooth'});
    } catch(e) { console.error(e); }
    
    btn.disabled = false;
    btn.innerHTML = '<i data-lucide="zap" class="w-5 h-5 fill-white"></i> ANALIZZA DATI API';
}

function renderResultsTiri(h, a, eth, eta, eph, epa) {
    const gT = document.getElementById('grid-tiri');
    const gP = document.getElementById('grid-tp');
    
    const lT = parseFloat(document.getElementById('line-t-match').value);
    const lP = parseFloat(document.getElementById('line-tp-match').value);

    gT.innerHTML = createBox("MATCH TOTALE", eth + eta, lT);
    gT.innerHTML += createBox(h, eth, 11.5);
    gT.innerHTML += createBox(a, eta, 10.5);

    gP.innerHTML = createBox("TIRI PORTA TOT", eph + epa, lP);
    gP.innerHTML += createBox(h, eph, 4.5);
    gP.innerHTML += createBox(a, epa, 3.5);
}

function renderResultsFalli(h, a, val) {
    const g = document.getElementById('grid-falli');
    const line = parseFloat(document.getElementById('line-f-match').value);
    g.innerHTML = createBox("MATCH FALLI", val, line);
    g.innerHTML += createBox(h, val/2, 12.25);
    g.innerHTML += createBox(a, val/2, 12.25);
}

function createBox(title, val, line) {
    const diff = val - line;
    let c = "val-low", r = "PASS", t = "NO EDGE", badge = "";
    
    if(diff >= 1.2 || diff <= -1.2) { 
        c = "val-top"; 
        r = (diff > 0 ? "OVER " : "UNDER ") + line; 
        t = "SUPER VALORE"; 
        badge = '<span class="badge-top">⚡ TOP</span>';
    } 
    else if(diff >= 0.5 || diff <= -0.5) { 
        c = "val-med"; 
        r = (diff > 0 ? "OVER " : "UNDER ") + line; 
        t = "BUONO"; 
    }
    else {
        r = (diff > 0 ? "OVER " : "UNDER ") + line;
    }
    
    return `<div class="value-box ${c}">${badge}<div class="text-[10px] font-bold opacity-60 uppercase">${title}</div><div class="res">${r}</div><div class="text-[11px] font-bold">AI: ${val.toFixed(2)} | ${t}</div></div>`;
}
</script>
</body>
</html>
"""

components.html(html_code, height=1400, scrolling=True)
