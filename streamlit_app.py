import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="ProBet AI - LIVE API", layout="wide", initial_sidebar_state="collapsed")

# CSS PER NASCONDERE L'INTERFACCIA STREAMLIT
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
div[data-testid="stHeader"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
<title>ProBet AI - LIVE</title>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://unpkg.com/lucide@latest"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Teko:wght@400;600&family=Inter:wght@400;600;700;800&display=swap');
body { background-color: #0f172a; color: #e2e8f0; font-family: 'Inter', sans-serif; margin: 0; padding: 0; }
.teko { font-family: 'Teko', sans-serif; }
select { background-color: #1e293b; color: white; border: 1px solid #334155; padding: 12px; border-radius: 8px; width: 100%; font-weight: bold; outline: none; }
.input-dark { background:#1e293b; border:1px solid #334155; color:white; padding:8px; border-radius:6px; width:100%; text-align:center; font-weight:700; }
.value-box { padding:12px; border-radius:10px; margin-bottom:8px; text-align:center; border:1px solid; position:relative; overflow:hidden; }
.val-high { background: linear-gradient(135deg,#15803d 0%,#166534 100%); color:white; border-color:#22c55e; }
.val-med { background: linear-gradient(135deg,#ca8a04 0%,#a16207 100%); color:#fff; border-color:#facc15; }
.val-low { background: linear-gradient(135deg,#b91c1c 0%,#991b1b 100%); color:white; border-color:#ef4444; }
.res { font-size:22px; font-weight:900; margin:2px 0; font-family:'Teko',sans-serif; line-height:1; }
.prob-badge { font-size:10px; background:rgba(0,0,0,0.3); padding:2px 6px; border-radius:4px; display:inline-block; margin-top:4px; font-weight:700; }
.confidence-pill { position:absolute; top:6px; right:6px; font-size:10px; background:#fff; color:#000; padding:3px 7px; border-radius:12px; font-weight:800; }
.loader { width:14px; height:14px; border:2px solid #475569; border-bottom-color:#3b82f6; border-radius:50%; display:inline-block; animation:rotation 1s linear infinite; }
@keyframes rotation { 0% { transform:rotate(0deg);} 100% { transform:rotate(360deg);} }
header { position: fixed; top: 0; width: 100%; z-index: 50; background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(8px); border-bottom: 1px solid #1e293b; }
main { padding: 80px 16px 40px; max-width: 800px; margin: 0 auto; }
</style>
</head>
<body>
<header>
<div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
    <div class="text-2xl font-bold teko text-white tracking-wide">PROBET <span class="text-blue-500">AI</span></div>
    <div id="status-pill" class="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800">
        <div class="loader"></div> <span class="text-[10px] font-bold text-slate-400 uppercase" id="plan-text">Verifica API...</span>
    </div>
</div>
</header>
<main>
<div class="flex justify-center mb-6">
    <div class="bg-slate-900 p-1 rounded-xl border border-slate-800 flex gap-2 w-full max-w-sm shadow-lg">
        <button onclick="switchLeague(135, 'SERIE_A')" id="btn-sa" class="flex-1 py-3 text-xs font-bold rounded-lg bg-blue-600 text-white shadow-lg transition-all">SERIE A</button>
        <button onclick="switchLeague(39, 'PREMIER')" id="btn-pl" class="flex-1 py-3 text-xs font-bold rounded-lg text-slate-400 hover:bg-slate-800 transition-all">PREMIER</button>
    </div>
</div>

<div class="bg-slate-900 p-5 rounded-2xl border border-slate-800 shadow-xl mb-8">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-5">
        <div><label class="text-[10px] font-bold text-slate-500 uppercase ml-1">CASA</label><select id="home" class="mt-1"></select></div>
        <div><label class="text-[10px] font-bold text-slate-500 uppercase ml-1">OSPITE</label><select id="away" class="mt-1"></select></div>
    </div>
    
    <details class="group bg-black/20 p-4 rounded-xl border border-slate-800/50 mb-5" open>
        <summary class="flex justify-between items-center cursor-pointer font-bold text-slate-400 text-xs uppercase select-none">
            <span><i data-lucide="edit-3" class="w-3 h-3 inline"></i> Imposta Linee Bookmaker</span>
            <i data-lucide="chevron-down" class="w-4 h-4 transition-transform group-open:rotate-180"></i>
        </summary>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
            <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
                <div class="text-[9px] font-bold text-blue-400 uppercase mb-2 text-center border-b border-slate-800 pb-1">LINEA TIRI TOTALI</div>
                <input type="number" id="line-t-match" value="23.5" step="0.5" class="input-dark mb-2 text-lg font-bold text-white">
                <div class="grid grid-cols-2 gap-2">
                    <input type="number" id="line-t-h" value="12.5" step="0.5" class="input-dark text-xs" placeholder="Casa">
                    <input type="number" id="line-t-a" value="10.5" step="0.5" class="input-dark text-xs" placeholder="Ospite">
                </div>
            </div>
            <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
                <div class="text-[9px] font-bold text-purple-400 uppercase mb-2 text-center border-b border-slate-800 pb-1">LINEA IN PORTA</div>
                <input type="number" id="line-tp-match" value="8.5" step="0.5" class="input-dark mb-2 text-lg font-bold text-white">
                <div class="grid grid-cols-2 gap-2">
                    <input type="number" id="line-tp-h" value="4.5" step="0.5" class="input-dark text-xs" placeholder="Casa">
                    <input type="number" id="line-tp-a" value="3.5" step="0.5" class="input-dark text-xs" placeholder="Ospite">
                </div>
            </div>
        </div>
    </details>

    <button onclick="runAnalysis()" id="btn-run" class="w-full py-4 bg-gradient-to-r from-blue-600 to-blue-500 text-white font-black text-xl rounded-xl shadow-lg active:scale-95 transition-all flex justify-center items-center gap-2">
        <i data-lucide="zap" class="w-5 h-5 fill-white"></i> ANALIZZA DATI LIVE
    </button>
</div>

<div id="results" class="hidden animate-fade-in pb-20">
    <div class="flex items-center gap-2 mb-3 mt-8 border-b border-slate-800 pb-2"><i data-lucide="crosshair" class="text-blue-400 w-4 h-4"></i><span class="text-sm font-bold text-blue-400 uppercase tracking-widest">Tiri Totali</span></div>
    <div id="grid-tiri" class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-8"></div>
    
    <div class="flex items-center gap-2 mb-3 mt-8 border-b border-slate-800 pb-2"><i data-lucide="target" class="text-purple-400 w-4 h-4"></i><span class="text-sm font-bold text-purple-400 uppercase tracking-widest">Tiri In Porta</span></div>
    <div id="grid-tp" class="grid grid-cols-1 md:grid-cols-3 gap-3"></div>
</div>

<div id="console" class="text-[10px] font-mono text-slate-600 mt-10 p-4 border-t border-slate-800"></div>

</main>

<script>
const API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3";
const BASE_URL = "https://v3.football.api-sports.io";
let currentLeagueId = 135;

function log(msg) { document.getElementById('console').innerHTML += `<br>> ${msg}`; }

async function checkStatus() {
    try {
        const r = await fetch(`${BASE_URL}/status`, { headers: { 'x-apisports-key': API_KEY } });
        const d = await r.json();
        const plan = d.response.subscription.plan;
        document.getElementById('status-pill').innerHTML = `<span class="w-2 h-2 rounded-full bg-emerald-500"></span><span class="text-emerald-400 text-[10px] font-bold uppercase">SISTEMA PRONTO: ${plan}</span>`;
    } catch(e) { log("Errore API: Chiave non valida o scaduta."); }
}

async function switchLeague(id, label) {
    currentLeagueId = id;
    const btnSa = document.getElementById('btn-sa');
    const btnPl = document.getElementById('btn-pl');
    if(label === 'SERIE_A') {
        btnSa.className = "flex-1 py-3 text-xs font-bold rounded-lg bg-blue-600 text-white shadow-lg";
        btnPl.className = "flex-1 py-3 text-xs font-bold rounded-lg text-slate-400 hover:bg-slate-800";
    } else {
        btnPl.className = "flex-1 py-3 text-xs font-bold rounded-lg bg-blue-600 text-white shadow-lg";
        btnSa.className = "flex-1 py-3 text-xs font-bold rounded-lg text-slate-400 hover:bg-slate-800";
    }
    loadTeams();
}

async function loadTeams() {
    log(`Caricamento squadre lega ${currentLeagueId}...`);
    try {
        const r = await fetch(`${BASE_URL}/teams?league=${currentLeagueId}&season=2025`, { headers: { 'x-apisports-key': API_KEY } });
        const d = await r.json();
        const h = document.getElementById('home');
        const a = document.getElementById('away');
        h.innerHTML = ""; a.innerHTML = "";
        d.response.sort((x,y) => x.team.name.localeCompare(y.team.name)).forEach(t => {
            const opt = new Option(t.team.name, t.team.id);
            h.add(opt.cloneNode(true)); a.add(opt);
        });
        log("Squadre caricate.");
    } catch(e) { log("Errore caricamento squadre."); }
}

async function getTeamStats(teamId) {
    log(`Analisi profonda Team ${teamId}...`);
    const r = await fetch(`${BASE_URL}/fixtures?team=${teamId}&league=${currentLeagueId}&season=2025&last=10`, { headers: { 'x-apisports-key': API_KEY } });
    const d = await r.json();
    
    let totalShots = 0, onGoal = 0, count = 0;
    for (const fix of d.response) {
        const fId = fix.fixture.id;
        const sR = await fetch(`${BASE_URL}/fixtures/statistics?fixture=${fId}&team=${teamId}`, { headers: { 'x-apisports-key': API_KEY } });
        const sD = await sR.json();
        if(sD.response && sD.response[0]) {
            const stats = sD.response[0].statistics;
            totalShots += stats.find(x => x.type === "Total Shots")?.value || 0;
            onGoal += stats.find(x => x.type === "Shots on Goal")?.value || 0;
            count++;
        }
    }
    return { avgShots: totalShots/(count||1), avgOnGoal: onGoal/(count||1) };
}

function poisson(k, lambda) { return (Math.pow(lambda, k) * Math.exp(-lambda)) / factorial(k); }
function factorial(n) { if (n===0 || n===1) return 1; let r=1; for(let i=2; i<=n; i++) r*=i; return r; }
function getPoissonProb(line, lambda, type) {
    let pUnder = 0;
    for(let k=0; k<=Math.floor(line); k++) pUnder += poisson(k, lambda);
    return type==='OVER' ? (1-pUnder)*100 : pUnder*100;
}

function renderBox(id, title, val, lineId) {
    const el = document.getElementById(id);
    const line = parseFloat(document.getElementById(lineId).value) || 0;
    const diff = val - line;
    
    let color = "bg-slate-800 border-slate-700", label = "NO EDGE", recommendation = "PASS", prob = 50;
    prob = getPoissonProb(line, val, diff > 0 ? 'OVER' : 'UNDER');
    
    if (Math.abs(diff) >= 1.5) {
        color = "val-high"; label = "SUPER VALORE"; recommendation = diff > 0 ? `OVER ${line}` : `UNDER ${line}`;
    } else if (Math.abs(diff) >= 0.5) {
        color = "val-med"; label = "BUONO"; recommendation = diff > 0 ? `OVER ${line}` : `UNDER ${line}`;
    }

    const badge = prob > 68 ? `<span class="confidence-pill">⚡ HIGH CONFIDENCE</span>` : "";
    
    el.innerHTML += `
        <div class="value-box ${color}">
            ${badge}
            <div class="text-[10px] opacity-80 uppercase font-bold">${title}</div>
            <div class="res">${recommendation}</div>
            <div class="text-xs font-bold">AI: ${val.toFixed(2)} | ${label}</div>
            <div class="prob-badge">Prob. ${prob.toFixed(0)}%</div>
        </div>`;
}

async function runAnalysis() {
    const btn = document.getElementById('btn-run');
    btn.disabled = true; btn.innerText = "ELABORAZIONE MATRICE...";
    
    try {
        const hId = document.getElementById('home').value;
        const aId = document.getElementById('away').value;
        const hName = document.getElementById('home').options[document.getElementById('home').selectedIndex].text;
        const aName = document.getElementById('away').options[document.getElementById('away').selectedIndex].text;

        const hStats = await getTeamStats(hId);
        const aStats = await getTeamStats(aId);

        document.getElementById('grid-tiri').innerHTML = "";
        document.getElementById('grid-tp').innerHTML = "";

        // Tiri Totali
        renderBox('grid-tiri', "MATCH TOTALE", hStats.avgShots + aStats.avgShots, 'line-t-match');
        renderBox('grid-tiri', hName, hStats.avgShots, 'line-t-h');
        renderBox('grid-tiri', aName, aStats.avgShots, 'line-t-a');

        // Tiri In Porta
        renderBox('grid-tp', "MATCH IN PORTA", hStats.avgOnGoal + aStats.avgOnGoal, 'line-tp-match');
        renderBox('grid-tp', hName, hStats.avgOnGoal, 'line-tp-h');
        renderBox('grid-tp', aName, aStats.avgOnGoal, 'line-tp-a');

        document.getElementById('results').classList.remove('hidden');
        lucide.createIcons();
        window.scrollTo({ top: document.getElementById('results').offsetTop - 100, behavior: 'smooth' });

    } catch(e) { alert("Errore durante l'analisi."); }
    finally { btn.disabled = false; btn.innerText = "ANALIZZA DATI LIVE"; }
}

window.onload = () => { 
    if(window.lucide) lucide.createIcons();
    checkStatus(); 
    loadTeams(); 
};
</script>
</body>
</html>
"""

components.html(html_code, height=1200, scrolling=True)
