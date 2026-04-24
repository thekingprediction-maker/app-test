import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="ProBet AI - Test API", layout="wide", initial_sidebar_state="collapsed")

# CSS Streamlit per nascondere l'interfaccia standard
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
iframe { width: 100vw !important; height: 100vh !important; border: none !important; display: block !important; position: fixed; top: 0; left: 0; z-index: 9999; }
</style>
""", unsafe_allow_html=True)

# --- CODICE HTML/JS AGGIORNATO CON API ---
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
@import url('https://fonts.googleapis.com/css2?family=Teko:wght@400;600&family=Inter:wght@400;600;700;800&display=swap');
html, body { background-color: #0f172a; color: #e2e8f0; font-family: 'Inter', sans-serif; margin: 0; padding: 0; width: 100%; height: 100%; overflow-x: hidden; }
.teko { font-family: 'Teko', sans-serif; }
select { background-color: #1e293b; color: white; border: 1px solid #334155; padding: 12px; border-radius: 8px; width: 100%; font-weight: bold; outline: none; }
.input-dark { background:#1e293b; border:1px solid #334155; color:white; padding:8px; border-radius:6px; width:100%; text-align:center; font-weight:700; }
.value-box { padding:12px; border-radius:10px; margin-bottom:8px; text-align:center; border:1px solid; position:relative; }
.val-high { background: linear-gradient(135deg,#15803d 0%,#166534 100%); color:white; border-color:#22c55e; }
.val-med { background: linear-gradient(135deg,#ca8a04 0%,#a16207 100%); color:#fff; border-color:#facc15; }
.res { font-size:22px; font-weight:900; font-family:'Teko',sans-serif; }
.confidence-pill { position:absolute; top:6px; right:6px; font-size:10px; background:#fff; color:#000; padding:3px 7px; border-radius:12px; font-weight:800; }
.loader { width:14px; height:14px; border:2px solid #475569; border-bottom-color:#3b82f6; border-radius:50%; display:inline-block; animation:rotation 1s linear infinite; }
@keyframes rotation { 0% { transform:rotate(0deg);} 100% { transform:rotate(360deg);} }
header { position: fixed; top: 0; left: 0; width: 100%; z-index: 50; background-color: rgba(15, 23, 42, 0.95); backdrop-filter: blur(8px); border-bottom: 1px solid #1e293b; }
main { padding: 80px 16px 40px; max-width: 800px; margin: 0 auto; }
</style>
</head>
<body>
<header>
<div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
    <div class="text-2xl font-bold teko text-white">PROBET <span class="text-blue-500">AI</span> <span class="text-[10px] text-slate-500 ml-2">V3 API TEST</span></div>
    <div id="status-pill" class="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800"><div class="loader"></div> <span class="text-[10px] font-bold text-slate-400">LOADING</span></div>
</div>
</header>
<main>
<div class="flex justify-center mb-6">
    <div class="bg-slate-900 p-1 rounded-xl border border-slate-800 flex gap-2 w-full max-w-sm">
        <button onclick="switchLeague('SERIE_A')" id="btn-sa" class="flex-1 py-3 text-xs font-bold rounded-lg bg-blue-600 text-white shadow-lg">SERIE A</button>
        <button onclick="switchLeague('PREMIER')" id="btn-pl" class="flex-1 py-3 text-xs font-bold rounded-lg text-slate-400">PREMIER</button>
        <button onclick="switchLeague('LIGA')" id="btn-lg" class="flex-1 py-3 text-xs font-bold rounded-lg text-slate-400">LIGA</button>
    </div>
</div>
<div class="bg-slate-900 p-5 rounded-2xl border border-slate-800 shadow-xl mb-8">
    <div class="grid grid-cols-1 gap-4 mb-5">
        <div><label class="text-[10px] font-bold text-slate-500 uppercase ml-1">CASA</label><select id="home"><option>Caricamento API...</option></select></div>
        <div><label class="text-[10px] font-bold text-slate-500 uppercase ml-1">OSPITE</label><select id="away"><option>Caricamento API...</option></select></div>
        <div id="ref-box"><label class="text-[10px] font-bold text-slate-500 uppercase ml-1">ARBITRO</label><select id="referee" class="text-yellow-400"></select></div>
    </div>
    <hr class="border-slate-800 mb-5 opacity-50">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-5">
        <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
            <div class="text-[9px] font-bold text-red-400 uppercase mb-2 text-center">LINEE FALLI</div>
            <input type="number" id="line-f-match" value="24.5" step="0.5" class="input-dark mb-2 text-lg">
            <div class="grid grid-cols-2 gap-2">
                <input type="number" id="line-f-h" value="11.5" class="input-dark text-xs">
                <input type="number" id="line-f-a" value="11.5" class="input-dark text-xs">
            </div>
        </div>
        <div id="box-tiri-lines" class="bg-slate-950 p-3 rounded-lg border border-slate-800 md:col-span-2">
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <div class="text-[9px] font-bold text-blue-400 uppercase mb-2 text-center">TIRI TOTALI</div>
                    <input type="number" id="line-t-match" value="23.5" step="0.5" class="input-dark mb-2">
                </div>
                <div>
                    <div class="text-[9px] font-bold text-purple-400 uppercase mb-2 text-center">TIRI IN PORTA</div>
                    <input type="number" id="line-tp-match" value="8.5" step="0.5" class="input-dark mb-2">
                </div>
            </div>
        </div>
    </div>
    <button id="btn-analyze" onclick="calculate()" class="w-full py-4 bg-blue-600 text-white font-black text-xl rounded-xl shadow-lg transition-all flex justify-center items-center gap-2">
        <i data-lucide="zap" class="w-5 h-5 fill-white"></i> ANALIZZA DATI
    </button>
</div>
<div id="results" class="hidden pb-20">
    <div id="sec-falli" class="mb-8">
        <div class="flex items-center gap-2 mb-3 mt-8 border-b border-slate-800 pb-2"><span class="text-sm font-bold text-red-400 uppercase tracking-widest" id="title-falli">Analisi Falli</span></div>
        <div id="grid-falli" class="grid grid-cols-1 md:grid-cols-3 gap-3"></div>
    </div>
    <div id="sec-tiri">
        <div class="flex items-center gap-2 mb-3 mt-8 border-b border-slate-800 pb-2"><span class="text-sm font-bold text-blue-400 uppercase tracking-widest">Analisi Tiri (API)</span></div>
        <div id="grid-tiri" class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-4"></div>
        <div id="grid-tp" class="grid grid-cols-1 md:grid-cols-3 gap-3"></div>
    </div>
</div>
</main>

<script>
// ==========================================
// 🔑 028b02ea1d97fdd09cf5f4a89f6860b3
// ==========================================
const 028b02ea1d97fdd09cf5f4a89f6860b3"; 
// ==========================================

const LEAGUE_IDS = { SERIE_A: 135, LIGA: 140, PREMIER: 39 };

const CSV_LINKS = {
    SERIE_A: {
        arb: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/ARBITRI_SERIE_A%20-%20Foglio1.csv",
        curr: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_CURR_SERIE_A%20-%20Foglio1.csv",
        prev: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_PREV_SERIE_A%20-%20DATI%20STAGIONE%202024_2025%20.csv"
    },
    LIGA: {
        arb: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/ARBITRI_LIGA%20-%20Foglio1.csv",
        curr: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_CURR_LIGA%20-%20Foglio1.csv",
        prev: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_PREV_LIGA%20%20-%20DATI%20STAGIONE%202024_2025.csv"
    },
    PREMIER: { arb: "", curr: "", prev: "" }
};

let CURRENT_LEAGUE = 'SERIE_A';
let DB = { refs: [], fc: [], fp: [], teams: [] };

document.addEventListener('DOMContentLoaded', () => {
    if(window.lucide) lucide.createIcons();
    switchLeague('SERIE_A');
});

function switchLeague(l) {
    CURRENT_LEAGUE = l;
    document.getElementById('btn-sa').className = `flex-1 py-3 text-xs font-bold rounded-lg ${l==='SERIE_A'?'bg-blue-600 text-white':'text-slate-400'}`;
    document.getElementById('btn-pl').className = `flex-1 py-3 text-xs font-bold rounded-lg ${l==='PREMIER'?'bg-blue-600 text-white':'text-slate-400'}`;
    document.getElementById('btn-lg').className = `flex-1 py-3 text-xs font-bold rounded-lg ${l==='LIGA'?'bg-blue-600 text-white':'text-slate-400'}`;
    
    document.getElementById('home').innerHTML = '<option>Caricamento API...</option>';
    document.getElementById('away').innerHTML = '<option>Caricamento API...</option>';
    loadData();
}

async function loadData() {
    try {
        const pill = document.getElementById('status-pill');
        pill.innerHTML = `<div class="loader"></div> <span class="text-[10px] font-bold text-slate-400">LOADING API</span>`;
        
        // 1. Carica Squadre da API
        const teamsRes = await fetch(`https://v3.football.api-sports.io/teams?league=${LEAGUE_IDS[CURRENT_LEAGUE]}&season=2024`, {
            headers: { "x-apisports-key": API_KEY }
        });
        const teamsData = await teamsRes.json();
        DB.teams = teamsData.response.map(t => ({ id: t.team.id, name: t.team.name })).sort((a,b) => a.name.localeCompare(b.name));

        // 2. Carica Falli da CSV
        const L = CSV_LINKS[CURRENT_LEAGUE];
        if(L.arb) {
            const rawArb = await fetch(L.arb).then(r => r.text());
            const parsedArb = Papa.parse(rawArb, {skipEmptyLines:true}).data;
            DB.refs = parsedArb.slice(1).map(r => ({name:r[0], avg:parseFloat(r[2])||0}));
        }
        if(L.curr) {
            const rawFc = await fetch(L.curr).then(r => r.text());
            DB.fc = Papa.parse(rawFc, {skipEmptyLines:true}).data.slice(1).map(r => ({Team:r[1], Loc:r[2], Sub:parseFloat(r[3])||0, Comm:parseFloat(r[4])||0}));
        }
        if(L.prev) {
            const rawFp = await fetch(L.prev).then(r => r.text());
            DB.fp = Papa.parse(rawFp, {skipEmptyLines:true}).data.slice(1).map(r => ({Team:r[1], Loc:r[2], Sub:parseFloat(r[3])||0, Comm:parseFloat(r[4])||0}));
        }

        updateSelectors();
        pill.innerHTML = `<span class="w-2 h-2 rounded-full bg-emerald-500"></span><span class="text-emerald-400 text-[10px] font-bold">API CONNESSA</span>`;
    } catch(e) {
        console.error(e);
        document.getElementById('status-pill').innerHTML = `<span class="text-red-500 text-[10px]">ERRORE API</span>`;
    }
}

function updateSelectors() {
    const h = document.getElementById('home'), a = document.getElementById('away'), r = document.getElementById('referee');
    h.innerHTML = ''; a.innerHTML = ''; r.innerHTML = '<option value="">Seleziona Arbitro</option>';
    DB.teams.forEach(t => {
        h.add(new Option(t.name, t.id));
        a.add(new Option(t.name, t.id));
    });
    DB.refs.forEach(ref => r.add(new Option(ref.name, ref.name)));
}

async function calculate() {
    const btn = document.getElementById('btn-analyze');
    const hId = document.getElementById('home').value;
    const aId = document.getElementById('away').value;
    const hName = document.getElementById('home').options[document.getElementById('home').selectedIndex].text;
    const aName = document.getElementById('away').options[document.getElementById('away').selectedIndex].text;
    
    btn.disabled = true;
    btn.innerHTML = "CALCOLO API...";

    try {
        // --- 1. STATISTICHE TIRI DA API ---
        const [hStatsRes, aStatsRes] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${LEAGUE_IDS[CURRENT_LEAGUE]}&season=2024&team=${hId}`, { headers: { "x-apisports-key": API_KEY } }),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${LEAGUE_IDS[CURRENT_LEAGUE]}&season=2024&team=${aId}`, { headers: { "x-apisports-key": API_KEY } })
        ]);
        const hS = await hStatsRes.json();
        const aS = await aStatsRes.json();

        // Estrazione dati (Media Tiri)
        const getAvg = (s, path) => {
            const parts = path.split('.');
            let val = s.response;
            for(let p of parts) val = val ? val[p] : 0;
            return parseFloat(val) || 0;
        };

        // Calcoli basati su API
        const hFattiCasa = getAvg(hS, 'shots.total.home') / (hS.response.fixtures.played.home || 1);
        const aSubitiFuori = getAvg(aS, 'shots.total.away') / (aS.response.fixtures.played.away || 1); // Nota: API potrebbe non dare subiti direttamente
        
        // Per il test, usiamo i totali medi forniti dall'API
        const expTiriHome = getAvg(hS, 'shots.total.home') / (hS.response.fixtures.played.home || 1);
        const expTiriAway = getAvg(aS, 'shots.total.away') / (aS.response.fixtures.played.away || 1);
        const expTPHome = getAvg(hS, 'shots.on_goal.home') / (hS.response.fixtures.played.home || 1);
        const expTPAway = getAvg(aS, 'shots.on_goal.away') / (aS.response.fixtures.played.away || 1);

        renderResultsTiri(hName, aName, expTiriHome, expTiriAway, expTPHome, expTPAway);

        // --- 2. FALLI (CSV) ---
        if(CURRENT_LEAGUE !== 'PREMIER') {
            const findF = (n, loc, db) => db.find(x => x.Team.toUpperCase().includes(n.toUpperCase().slice(0,5)) && x.Loc.includes(loc)) || {Comm:12, Sub:12};
            const fH = findF(hName, 'CASA', DB.fc);
            const fA = findF(aName, 'FUORI', DB.fc);
            const predF = (fH.Comm + fA.Sub)/2 + (fA.Comm + fH.Sub)/2;
            renderResultsFalli(hName, aName, predF);
        }

        document.getElementById('results').classList.remove('hidden');
    } catch(e) { console.error(e); }
    
    btn.disabled = false;
    btn.innerHTML = '<i data-lucide="zap" class="w-5 h-5 fill-white"></i> ANALIZZA DATI';
}

function renderResultsTiri(h, a, eth, eta, eph, epa) {
    const gT = document.getElementById('grid-tiri');
    const gP = document.getElementById('grid-tp');
    const lT = parseFloat(document.getElementById('line-t-match').value);
    const lP = parseFloat(document.getElementById('line-tp-match').value);

    gT.innerHTML = createBox("MATCH TOTALE", eth + eta, lT);
    gT.innerHTML += createBox(h, eth, eth > 12 ? 12.5 : 10.5);
    gT.innerHTML += createBox(a, eta, eta > 10 ? 10.5 : 8.5);

    gP.innerHTML = createBox("PORTA TOTALE", eph + epa, lP);
    gP.innerHTML += createBox(h, eph, 4.5);
    gP.innerHTML += createBox(a, epa, 3.5);
}

function renderResultsFalli(h, a, val) {
    const g = document.getElementById('grid-falli');
    const line = parseFloat(document.getElementById('line-f-match').value);
    g.innerHTML = createBox("MATCH FALLI", val, line);
    g.innerHTML += createBox(h, val/2, line/2);
    g.innerHTML += createBox(a, val/2, line/2);
}

function createBox(title, val, line) {
    const diff = val - line;
    let c = "bg-slate-800 border-slate-700", r = "PASS", t = "NO EDGE";
    if(diff >= 1.5) { c = "val-high"; r = "OVER " + line; t = "SUPER VALORE"; }
    else if(diff >= 0.5) { c = "val-med"; r = "OVER " + line; t = "BUONO"; }
    else if(diff <= -1.5) { c = "val-high"; r = "UNDER " + line; t = "SUPER VALORE"; }
    
    return `<div class="value-box ${c}"><div class="text-[10px] opacity-70">${title}</div><div class="res">${r}</div><div class="text-xs font-bold">AI: ${val.toFixed(2)} | ${t}</div></div>`;
}
</script>
</body>
</html>
"""

components.html(html_code, height=1200, scrolling=True)
