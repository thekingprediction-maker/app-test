import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE STREAMLIT ---
st.set_page_config(page_title="ProBet AI V3.1 - Full API", layout="wide", initial_sidebar_state="collapsed")

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
    <title>ProBet AI V3</title>
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
            padding: 10px; 
            border-radius: 10px; 
            width: 100%; 
            text-align: center; 
            font-weight: 800; 
        }

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
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        
        .val-top { 
            background: linear-gradient(145deg, #064e3b 0%, #022c22 100%); 
            border-color: #10b981; 
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.1);
        }
        .val-good { 
            background: linear-gradient(145deg, #451a03 0%, #1c0a00 100%); 
            border-color: #f59e0b;
            box-shadow: 0 0 20px rgba(245, 158, 11, 0.1);
        }
        
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
        main { padding: 120px 20px 80px; max-width: 900px; margin: 0 auto; }

        .loader { 
            width: 16px; height: 16px; border: 2.5px solid #1e293b; 
            border-bottom-color: #3b82f6; border-radius: 50%; 
            display: inline-block; animation: rot 1s linear infinite; 
        }
        @keyframes rot { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

        .btn-league {
            transition: all 0.3s ease;
            color: #64748b;
        }
        .btn-league.active {
            background: #2563eb !important;
            color: white !important;
            box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.4);
        }
    </style>
</head>
<body>

<header>
    <div class="max-w-6xl mx-auto px-6 h-24 flex items-center justify-between">
        <div class="flex items-center gap-3">
            <div class="text-4xl font-bold teko tracking-tighter text-white flex items-center gap-2">
                PROBET <span class="text-blue-500">AI</span>
            </div>
            <span class="bg-blue-500/10 text-blue-500 text-[10px] font-black px-2.5 py-1 rounded-md border border-blue-500/20">V3.1 PRO</span>
        </div>
        <div id="status-display" class="flex items-center gap-3 px-5 py-2 rounded-full bg-slate-900 border border-slate-800 shadow-inner">
            <div class="loader"></div> 
            <span class="text-[11px] font-black text-slate-400 uppercase tracking-widest">Inizializzazione...</span>
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

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
            <div class="card-bg p-6 rounded-2xl">
                <label class="text-[9px] font-black text-slate-500 uppercase tracking-widest block mb-4">Bookmaker Line Falli</label>
                <input type="number" id="line-f-match" value="23.5" step="1" class="input-dark text-2xl py-4 font-black">
            </div>
            <div class="card-bg p-6 rounded-2xl">
                <label class="text-[9px] font-black text-slate-500 uppercase tracking-widest block mb-4">Bookmaker Line Tiri Tot</label>
                <input type="number" id="line-t-match" value="24.5" step="1" class="input-dark text-2xl py-4 font-black">
            </div>
            <div class="card-bg p-6 rounded-2xl">
                <label class="text-[9px] font-black text-slate-500 uppercase tracking-widest block mb-4">Bookmaker Line Tiri Porta</label>
                <input type="number" id="line-tp-match" value="8.5" step="0.5" class="input-dark text-2xl py-4 font-black">
            </div>
        </div>

        <button id="btn-calc" onclick="processAnalysis()" class="w-full py-6 bg-blue-600 hover:bg-blue-500 text-white font-black text-2xl rounded-2xl shadow-[0_20px_40px_-15px_rgba(37,99,235,0.5)] active:scale-[0.98] transition-all transform uppercase tracking-tighter">
            Analizza Dati
        </button>
    </div>

    <div id="results-area" class="hidden space-y-16 animate-in fade-in duration-700">
        <section>
            <div class="flex items-center gap-4 mb-8 border-b border-slate-800/50 pb-4">
                <div class="w-2 h-8 bg-red-500 rounded-full shadow-[0_0_15px_rgba(239,68,68,0.5)]"></div>
                <h2 class="text-xl font-black text-white uppercase tracking-tight">Analisi Falli</h2>
            </div>
            <div id="res-grid-falli" class="grid grid-cols-1 md:grid-cols-3 gap-6"></div>
        </section>

        <section>
            <div class="flex items-center gap-4 mb-8 border-b border-slate-800/50 pb-4">
                <div class="w-2 h-8 bg-blue-500 rounded-full shadow-[0_0_15px_rgba(59,130,246,0.5)]"></div>
                <h2 class="text-xl font-black text-white uppercase tracking-tight">Analisi Tiri</h2>
            </div>
            <div id="res-grid-tiri" class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6"></div>
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
    const btn = document.getElementById(l === 'SERIE_A' ? 'btn-sa' : l === 'PREMIER' ? 'btn-pl' : 'btn-lg');
    if(btn) btn.classList.add('active');

    const status = document.getElementById('status-display');
    const resultArea = document.getElementById('results-area');
    if(resultArea) resultArea.classList.add('hidden');
    
    status.innerHTML = `<div class="loader"></div> <span class="text-[11px] font-black text-slate-400 uppercase tracking-widest">Connect ${l}...</span>`;
    
    async function trySeason(year) {
        try {
            const url = `https://v3.football.api-sports.io/teams?league=${LEAGUE_IDS[l]}&season=${year}`;
            const res = await fetch(url, { headers: { "x-apisports-key": API_KEY } });
            const data = await res.json();
            if (data.errors && Object.keys(data.errors).length > 0) return { error: Object.values(data.errors)[0] };
            if (!data.response || data.response.length === 0) return null;
            return { data: data.response };
        } catch (e) { return { error: e.message }; }
    }

    try {
        let res = null;
        for (let y of [2024, 2023, 2022]) {
            res = await trySeason(y);
            if (res && res.data) { SEASON = y; break; }
        }
        if (!res || !res.data) throw new Error("Dati non disponibili");

        DB.teams = res.data.map(r => ({ id: r.team.id, name: r.team.name })).sort((a,b) => a.name.localeCompare(b.name));
        const h = document.getElementById('home-team'), a = document.getElementById('away-team');
        h.innerHTML = ''; a.innerHTML = '';
        DB.teams.forEach(t => {
            h.add(new Option(t.name.toUpperCase(), t.id));
            a.add(new Option(t.name.toUpperCase(), t.id));
        });
        if(DB.teams.length > 1) a.selectedIndex = 1;
        status.innerHTML = `<span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span><span class="text-emerald-400 text-[11px] font-black uppercase tracking-widest">${l} ${SEASON} OK</span>`;
    } catch(err) {
        status.innerHTML = `<span class="text-red-500 text-[11px] font-black uppercase tracking-widest">API ERROR</span>`;
    }
}

async function fetchStats(teamId) {
    const key = `${CUR_L}_${SEASON}_${teamId}`;
    if(DB.statsCache[key]) return DB.statsCache[key];
    const res = await fetch(`https://v3.football.api-sports.io/teams/statistics?league=${LEAGUE_IDS[CUR_L]}&season=${SEASON}&team=${teamId}`, {
        headers: { "x-apisports-key": API_KEY }
    });
    const data = await res.json();
    DB.statsCache[key] = data.response;
    return data.response;
}

async function processAnalysis() {
    const btn = document.getElementById('btn-calc');
    const hId = document.getElementById('home-team').value, aId = document.getElementById('away-team').value;
    if(hId === aId) return alert("Seleziona due squadre diverse!");
    btn.disabled = true; btn.innerHTML = `<div class="loader mr-2"></div> ELABORAZIONE...`;

    try {
        const [hStats, aStats] = await Promise.all([fetchStats(hId), fetchStats(aId)]);
        const gH = hStats.fixtures.played.home || (hStats.fixtures.played.total / 2) || 1;
        const gA = aStats.fixtures.played.away || (aStats.fixtures.played.total / 2) || 1;

        const BASE_F = 12.5, BASE_T = 12.0, BASE_P = 4.2;
        const safeAvg = (v, g, b) => { const a = v / g; return (!a || a < 1) ? b : a; };

        const fhComH = safeAvg(hStats.fouls?.committed?.total?.home || (hStats.fouls?.committed?.total?.total/2), gH, BASE_F);
        const faSubA = safeAvg(aStats.fouls?.drawn?.total?.away || (aStats.fouls?.drawn?.total?.total/2), gA, BASE_F);
        const faComA = safeAvg(aStats.fouls?.committed?.total?.away || (aStats.fouls?.committed?.total?.total/2), gA, BASE_F);
        const fhSubH = safeAvg(hStats.fouls?.drawn?.total?.home || (hStats.fouls?.drawn?.total?.total/2), gH, BASE_F);
        
        const efh = (fhComH + faSubA) / 2, efa = (faComA + fhSubH) / 2;

        const thH = safeAvg(hStats.shots?.total?.home || (hStats.shots?.total?.total/2), gH, BASE_T);
        const taA = safeAvg(aStats.shots?.total?.away || (aStats.shots?.total?.total/2), gA, BASE_T);
        const eth = (thH + taA * 0.95) / 2, eta = (taA + thH * 0.9) / 2;

        const phH = safeAvg(hStats.shots?.on_goal?.home || (hStats.shots?.on_goal?.total/2), gH, BASE_P);
        const paA = safeAvg(aStats.shots?.on_goal?.away || (aStats.shots?.on_goal?.total/2), gA, BASE_P);
        const eph = (phH + paA * 0.85) / 2, epa = (paA + phH * 0.8) / 2;

        renderResults(efh, efa, eth, eta, eph, epa);
        document.getElementById('results-area').classList.remove('hidden');
        window.scrollTo({ top: document.getElementById('results-area').offsetTop - 120, behavior: 'smooth' });
    } catch(err) { alert("Errore: " + err.message); } 
    finally { btn.disabled = false; btn.innerHTML = "Analizza Dati"; lucide.createIcons(); }
}

function renderResults(efh, efa, eth, eta, eph, epa) {
    const lF = parseFloat(document.getElementById('line-f-match').value), lT = parseFloat(document.getElementById('line-t-match').value), lP = parseFloat(document.getElementById('line-tp-match').value);
    const hN = document.getElementById('home-team').options[document.getElementById('home-team').selectedIndex].text, aN = document.getElementById('away-team').options[document.getElementById('away-team').selectedIndex].text;

    document.getElementById('res-grid-falli').innerHTML = createCard("MATCH FALLI", efh + efa, lF) + createCard(hN, efh, lF/2) + createCard(aN, efa, lF/2);
    document.getElementById('res-grid-tiri').innerHTML = createCard("MATCH TIRI TOT", eth + eta, lT) + createCard(hN, eth, 11.5) + createCard(aN, eta, 9.5);
    document.getElementById('res-grid-tp').innerHTML = createCard("PORTA TOTALE", eph + epa, lP) + createCard(hN, eph, 4.5) + createCard(aN, epa, 3.5);
    lucide.createIcons();
}

function createCard(title, val, line) {
    const diff = val - line;
    let s = "", t = "", r = "NO EDGE";
    if(diff >= 1.2) { s = "val-top"; t = "TOP"; r = "OVER " + line; }
    else if(diff >= 0.4) { s = "val-good"; t = "GOOD"; r = "OVER " + line; }
    else if(diff <= -1.2) { s = "val-top"; t = "TOP"; r = "UNDER " + line; }
    else if(diff <= -0.4) { s = "val-good"; t = "GOOD"; r = "UNDER " + line; }
    return `<div class="value-box ${s}">${t ? `<div class="tag-pill"><i data-lucide="zap" class="w-3 h-3 fill-current"></i> ${t}</div>` : ''}<div class="text-[10px] font-black text-slate-500 uppercase mb-3 tracking-[0.15em]">${title}</div><div class="res-text">${r}</div><div class="text-[12px] font-black tracking-tight text-white/50">AI: ${val.toFixed(2)}</div></div>`;
}
</script>
</body>
</html>
"""
components.html(html_code, height=1500, scrolling=True)
