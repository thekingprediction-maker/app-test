import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE STREAMLIT ---
st.set_page_config(page_title="ProBet AI V3.1 - Full API Professional", layout="wide", initial_sidebar_state="collapsed")

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
    <title>ProBet AI V3.1 PRO</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@400;600&family=Inter:wght@400;600;700;800&display=swap');
        
        body { 
            background-color: #020617; 
            color: #f8fafc; 
            font-family: 'Inter', sans-serif; 
            margin: 0; padding: 0; 
            width: 100%; height: 100%; 
            overflow-x: hidden; 
        }
        .teko { font-family: 'Teko', sans-serif; }
        
        select { 
            background-color: #0f172a; 
            color: white; 
            border: 1px solid #1e293b; 
            padding: 14px; 
            border-radius: 14px; 
            width: 100%; 
            font-weight: 700; 
            outline: none;
            appearance: none;
        }
        .input-dark { 
            background: #0f172a; 
            border: 1px solid #1e293b; 
            color: white; 
            padding: 8px; 
            border-radius: 10px; 
            width: 100%; 
            text-align: center; 
            font-weight: 800; 
            outline: none;
        }
        .input-dark:focus { border-color: #3b82f6; }

        .card-bg {
            background: #0f172a;
            border: 1px solid #1e293b;
        }

        .value-box { 
            padding: 24px; 
            border-radius: 20px; 
            text-align: center; 
            border: 1px solid #1e293b; 
            position: relative; 
            background: #0f172a;
            transition: all 0.4s ease;
        }
        
        .val-top { background: linear-gradient(145deg, #064e3b 0%, #022c22 100%); border-color: #10b981; }
        .val-good { background: linear-gradient(145deg, #451a03 0%, #1c0a00 100%); border-color: #f59e0b; }
        
        .res-text { font-size: 32px; font-weight: 900; font-family: 'Teko', sans-serif; line-height: 1; margin-bottom: 8px; }
        
        .tag-pill { 
            position: absolute; top: 12px; right: 12px; 
            font-size: 10px; background: #fff; color: #000; 
            padding: 2px 10px; border-radius: 20px; 
            font-weight: 900; display: flex; align-items: center; gap: 4px;
        }

        header { 
            position: fixed; top: 0; left: 0; width: 100%; z-index: 100;
            background: rgba(2, 6, 23, 0.9); backdrop-filter: blur(16px);
            border-bottom: 1px solid #1e293b;
        }
        main { padding: 120px 20px 80px; max-width: 1000px; margin: 0 auto; }

        .loader { 
            width: 16px; height: 16px; border: 2.5px solid #1e293b; 
            border-bottom-color: #3b82f6; border-radius: 50%; 
            display: inline-block; animation: rot 1s linear infinite; 
        }
        @keyframes rot { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

        .btn-league { transition: all 0.3s ease; color: #64748b; }
        .btn-league.active { background: #2563eb !important; color: white !important; }
    </style>
</head>
<body>

<header>
    <div class="max-w-6xl mx-auto px-6 h-24 flex items-center justify-between">
        <div class="flex items-center gap-3">
            <div class="text-4xl font-bold teko tracking-tighter text-white">PROBET <span class="text-blue-500">AI</span></div>
            <span class="bg-blue-500/10 text-blue-500 text-[10px] font-black px-2.5 py-1 rounded-md border border-blue-500/20">V3.1 PRO</span>
        </div>
        <div id="status-display" class="flex items-center gap-3 px-5 py-2 rounded-full bg-slate-900 border border-slate-800 shadow-inner">
            <div class="loader"></div> 
            <span class="text-[11px] font-black text-slate-400 uppercase tracking-widest">Sincronizzazione...</span>
        </div>
    </div>
</header>

<main>
    <div class="flex justify-center mb-10">
        <div class="bg-slate-900 p-2 rounded-2xl border border-slate-800 flex gap-3 w-full max-w-md shadow-2xl">
            <button onclick="switchLeague('SERIE_A')" id="btn-sa" class="btn-league flex-1 py-4 text-[11px] font-black rounded-xl">SERIE A</button>
            <button onclick="switchLeague('PREMIER')" id="btn-pl" class="btn-league flex-1 py-4 text-[11px] font-black rounded-xl">PREMIER</button>
            <button onclick="switchLeague('LIGA')" id="btn-lg" class="btn-league flex-1 py-4 text-[11px] font-black rounded-xl">LIGA</button>
        </div>
    </div>

    <div class="bg-slate-900/40 p-8 rounded-[32px] border border-slate-800/60 shadow-2xl backdrop-blur-sm mb-12">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
            <div>
                <label class="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] ml-1 mb-3 block">Match Home</label>
                <select id="home-team"></select>
            </div>
            <div>
                <label class="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] ml-1 mb-3 block">Match Away</label>
                <select id="away-team"></select>
            </div>
        </div>

        <!-- SPREAD INPUTS -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
            <div class="card-bg p-6 rounded-2xl">
                <label class="text-[9px] font-black text-slate-500 uppercase tracking-widest block mb-4">Linea Totale Match</label>
                <div class="space-y-4">
                    <div><span class="text-[8px] text-slate-400 block mb-1 uppercase">Falli</span><input type="number" id="line-f-match" value="23.5" step="0.5" class="input-dark"></div>
                    <div><span class="text-[8px] text-slate-400 block mb-1 uppercase">Tiri Tot</span><input type="number" id="line-t-match" value="24.5" step="0.5" class="input-dark"></div>
                    <div><span class="text-[8px] text-slate-400 block mb-1 uppercase">In Porta</span><input type="number" id="line-tp-match" value="8.5" step="0.5" class="input-dark"></div>
                </div>
            </div>
            
            <div class="card-bg p-6 rounded-2xl">
                <label class="text-[9px] font-black text-blue-500 uppercase tracking-widest block mb-4">Spread CASA</label>
                <div class="space-y-4">
                    <div><span class="text-[8px] text-slate-400 block mb-1 uppercase">Falli Casa</span><input type="number" id="line-f-h" value="11.5" step="0.5" class="input-dark"></div>
                    <div><span class="text-[8px] text-slate-400 block mb-1 uppercase">Tiri Casa</span><input type="number" id="line-t-h" value="12.5" step="0.5" class="input-dark"></div>
                    <div><span class="text-[8px] text-slate-400 block mb-1 uppercase">Porta Casa</span><input type="number" id="line-tp-h" value="4.5" step="0.5" class="input-dark"></div>
                </div>
            </div>

            <div class="card-bg p-6 rounded-2xl">
                <label class="text-[9px] font-black text-red-500 uppercase tracking-widest block mb-4">Spread FUORI</label>
                <div class="space-y-4">
                    <div><span class="text-[8px] text-slate-400 block mb-1 uppercase">Falli Fuori</span><input type="number" id="line-f-a" value="11.5" step="0.5" class="input-dark"></div>
                    <div><span class="text-[8px] text-slate-400 block mb-1 uppercase">Tiri Fuori</span><input type="number" id="line-t-a" value="11.5" step="0.5" class="input-dark"></div>
                    <div><span class="text-[8px] text-slate-400 block mb-1 uppercase">Porta Fuori</span><input type="number" id="line-tp-a" value="3.5" step="0.5" class="input-dark"></div>
                </div>
            </div>
        </div>

        <button onclick="processAnalysis()" id="btn-calc" class="w-full py-6 bg-blue-600 hover:bg-blue-500 text-white font-black text-2xl rounded-2xl transition-all transform uppercase">
            Genera Previsione Professionale
        </button>
    </div>

    <div id="results-area" class="hidden space-y-16 animate-in fade-in duration-700">
        <section>
            <div class="flex items-center gap-4 mb-8 border-b border-slate-800 pb-4"><div class="w-2 h-8 bg-red-500 rounded-full"></div><h2 class="text-xl font-black text-white uppercase">Analisi Falli (Live Spread)</h2></div>
            <div id="res-grid-falli" class="grid grid-cols-1 md:grid-cols-3 gap-6"></div>
        </section>
        <section>
            <div class="flex items-center gap-4 mb-8 border-b border-slate-800 pb-4"><div class="w-2 h-8 bg-blue-500 rounded-full"></div><h2 class="text-xl font-black text-white uppercase">Analisi Tiri Totali</h2></div>
            <div id="res-grid-tiri" class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12"></div>
            <div class="flex items-center gap-4 mb-8 border-b border-slate-800 pb-4"><div class="w-2 h-8 bg-emerald-500 rounded-full"></div><h2 class="text-xl font-black text-white uppercase">Analisi Tiri in Porta</h2></div>
            <div id="res-grid-tp" class="grid grid-cols-1 md:grid-cols-3 gap-6"></div>
        </section>
    </div>
</main>

<script>
const API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3"; 
const LEAGUE_IDS = { SERIE_A: 135, LIGA: 140, PREMIER: 39 };

let DB = { teams: [], statsCache: {} };
let CUR_L = 'SERIE_A';
let SEASON = 2024; 

document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
    switchLeague('SERIE_A');
});

async function switchLeague(l) {
    CUR_L = l;
    document.querySelectorAll('.btn-league').forEach(b => b.classList.remove('active'));
    document.getElementById(l === 'SERIE_A' ? 'btn-sa' : l === 'PREMIER' ? 'btn-pl' : 'btn-lg').classList.add('active');

    const status = document.getElementById('status-display');
    status.innerHTML = `<div class="loader"></div> <span class="text-[11px] font-black text-slate-400 uppercase tracking-widest">Sincronizzo ${l}...</span>`;
    
    try {
        const res = await fetch(`https://v3.football.api-sports.io/teams?league=${LEAGUE_IDS[l]}&season=2024`, { headers: { "x-apisports-key": API_KEY } });
        const data = await res.json();
        if (!data.response) throw new Error();
        
        DB.teams = data.response.map(r => ({ id: r.team.id, name: r.team.name })).sort((a,b) => a.name.localeCompare(b.name));
        const h = document.getElementById('home-team'), a = document.getElementById('away-team');
        h.innerHTML = ''; a.innerHTML = '';
        DB.teams.forEach(t => {
            h.add(new Option(t.name.toUpperCase(), t.id));
            a.add(new Option(t.name.toUpperCase(), t.id));
        });
        a.selectedIndex = 1;
        status.innerHTML = `<span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span><span class="text-emerald-400 text-[11px] font-black uppercase tracking-widest">${l} 24/25 OK</span>`;
    } catch { status.innerHTML = `<span class="text-red-500 text-[11px] font-black uppercase">CONNESSIONE FALLITA</span>`; }
}

async function fetchStats(teamId) {
    const key = `${CUR_L}_2024_${teamId}`;
    if(DB.statsCache[key]) return DB.statsCache[key];
    const res = await fetch(`https://v3.football.api-sports.io/teams/statistics?league=${LEAGUE_IDS[CUR_L]}&season=2024&team=${teamId}`, { headers: { "x-apisports-key": API_KEY } });
    const data = await res.json();
    DB.statsCache[key] = data.response;
    return data.response;
}

async function processAnalysis() {
    const btn = document.getElementById('btn-calc');
    const hId = document.getElementById('home-team').value;
    const aId = document.getElementById('away-team').value;
    if(hId === aId) return alert("Squadre UGUALI!");

    btn.disabled = true; btn.innerHTML = "ANALISI DATABASE...";

    try {
        const [hStats, aStats] = await Promise.all([fetchStats(hId), fetchStats(aId)]);
        const gH = hStats.fixtures.played.home || 1, gA = aStats.fixtures.played.away || 1;

        // LOGICA INCROCIATA CSV
        const expFH = ((hStats.fouls?.committed?.total?.home || 0)/gH + (aStats.fouls?.drawn?.total?.away || 0)/gA) / 2;
        const expFA = ((aStats.fouls?.committed?.total?.away || 0)/gA + (hStats.fouls?.drawn?.total?.home || 0)/gH) / 2;
        
        const expTH = ((hStats.shots?.total?.home || 0)/gH + (aStats.shots?.total?.away || 0)*0.95/gA) / 2;
        const expTA = ((aStats.shots?.total?.away || 0)/gA + (hStats.shots?.total?.home || 0)*0.9/gH) / 2;

        const expPH = ((hStats.shots?.on_goal?.home || 0)/gH + (aStats.shots?.on_goal?.away || 0)*0.85/gA) / 2;
        const expPA = ((aStats.shots?.on_goal?.away || 0)/gA + (hStats.shots?.on_goal?.home || 0)*0.8/gH) / 2;

        renderResults(
            document.getElementById('home-team').options[document.getElementById('home-team').selectedIndex].text,
            document.getElementById('away-team').options[document.getElementById('away-team').selectedIndex].text,
            expFH, expFA, expTH, expTA, expPH, expPA
        );
        document.getElementById('results-area').classList.remove('hidden');
        lucide.createIcons();
    } finally { btn.disabled = false; btn.innerHTML = "Genera Previsione Professionale"; }
}

function renderResults(hName, aName, efh, efa, eth, eta, eph, epa) {
    const getL = (id) => parseFloat(document.getElementById(id).value);
    document.getElementById('res-grid-falli').innerHTML = createCard("MATCH FALLI", efh+efa, getL('line-f-match')) + createCard(hName, efh, getL('line-f-h')) + createCard(aName, efa, getL('line-f-a'));
    document.getElementById('res-grid-tiri').innerHTML = createCard("MATCH TIRI TOT", eth+eta, getL('line-t-match')) + createCard(hName, eth, getL('line-t-h')) + createCard(aName, eta, getL('line-t-a'));
    document.getElementById('res-grid-tp').innerHTML = createCard("PORTA TOTALE", eph+epa, getL('line-tp-match')) + createCard(hName, eph, getL('line-tp-h')) + createCard(aName, epa, getL('line-tp-a'));
}

function createCard(title, val, line) {
    const diff = val - line;
    let style = "", tag = "", rec = "NO BET";
    if(Math.abs(diff) >= 0.75) { style = "val-top"; tag = "AI TOP"; rec = diff > 0 ? "OVER "+line : "UNDER "+line; }
    else if(Math.abs(diff) >= 0.25) { style = "val-good"; tag = "BET"; rec = diff > 0 ? "OVER "+line : "UNDER "+line; }
    return `<div class="value-box ${style}">${tag?`<div class="tag-pill"><i data-lucide="shield-check" class="w-3 h-3"></i> ${tag}</div>`:''}<div class="text-[10px] font-black text-slate-500 uppercase mb-3 tracking-widest">${title}</div><div class="res-text">${rec}</div><div class="text-[12px] font-black text-white/50">STIMA: ${val.toFixed(2)}</div></div>`;
}
</script>
</body>
</html>
"""
components.html(html_code, height=1600, scrolling=True)
