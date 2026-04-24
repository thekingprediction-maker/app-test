import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE STREAMLIT ---
st.set_page_config(page_title="ProBet AI V3 - Multi-League", layout="wide", initial_sidebar_state="collapsed")

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
            background-color: #0f172a; 
            color: #e2e8f0; 
            font-family: 'Inter', sans-serif; 
            margin: 0; padding: 0; 
            width: 100%; height: 100%; 
            overflow-x: hidden; 
        }
        .teko { font-family: 'Teko', sans-serif; }
        
        select { 
            background-color: #1e293b; 
            color: white; 
            border: 1px solid #334155; 
            padding: 12px; 
            border-radius: 12px; 
            width: 100%; 
            font-weight: 700; 
            outline: none;
            appearance: none;
        }
        .input-dark { 
            background: #1e293b; 
            border: 1px solid #334155; 
            color: white; 
            padding: 8px; 
            border-radius: 8px; 
            width: 100%; 
            text-align: center; 
            font-weight: 800; 
        }

        .value-box { 
            padding: 18px; 
            border-radius: 16px; 
            text-align: center; 
            border: 1px solid; 
            position: relative; 
            background: #1e293b;
            border-color: #334155;
            transition: all 0.3s ease;
        }
        .val-top { 
            background: linear-gradient(135deg, #166534 0%, #14532d 100%); 
            border-color: #22c55e; 
        }
        .val-good { 
            background: linear-gradient(135deg, #854d0e 0%, #713f12 100%); 
            border-color: #eab308; 
        }
        .res-text { font-size: 26px; font-weight: 900; font-family: 'Teko', sans-serif; line-height: 1; margin-bottom: 4px; }
        .tag-pill { 
            position: absolute; top: 8px; right: 8px; 
            font-size: 10px; background: #fff; color: #000; 
            padding: 2px 8px; border-radius: 20px; 
            font-weight: 900; display: flex; items-center: center; gap: 3px;
        }

        header { 
            position: fixed; top: 0; left: 0; width: 100%; z-index: 100;
            background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(12px);
            border-bottom: 1px solid #1e293b;
        }
        main { padding: 100px 16px 80px; max-width: 800px; margin: 0 auto; }

        .loader { 
            width: 14px; height: 14px; border: 2px solid #475569; 
            border-bottom-color: #3b82f6; border-radius: 50%; 
            display: inline-block; animation: rot 1s linear infinite; 
        }
        @keyframes rot { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>

<header>
    <div class="max-w-6xl mx-auto px-6 h-20 flex items-center justify-between">
        <div class="text-3xl font-bold teko tracking-tight text-white flex items-center gap-2">
            PROBET <span class="text-blue-500">AI</span> <span class="bg-blue-500/10 text-blue-500 text-[10px] px-2 py-0.5 rounded border border-blue-500/20 ml-2">V3.1</span>
        </div>
        <div id="status-display" class="flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-900 border border-slate-800">
            <div class="loader"></div> 
            <span class="text-[11px] font-black text-slate-400 uppercase">Checking Connection</span>
        </div>
    </div>
</header>

<main>
    <div class="flex justify-center mb-8">
        <div class="bg-slate-900 p-1.5 rounded-2xl border border-slate-800 flex gap-2 w-full max-w-sm shadow-2xl">
            <button onclick="switchLeague('SERIE_A')" id="btn-sa" class="flex-1 py-3.5 text-xs font-black rounded-xl transition-all">SERIE A</button>
            <button onclick="switchLeague('PREMIER')" id="btn-pl" class="flex-1 py-3.5 text-xs font-black rounded-xl transition-all">PREMIER</button>
            <button onclick="switchLeague('LIGA')" id="btn-lg" class="flex-1 py-3.5 text-xs font-black rounded-xl transition-all">LIGA</button>
        </div>
    </div>

    <div class="bg-slate-900/50 p-6 rounded-3xl border border-slate-800 shadow-2xl mb-10">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div>
                <label class="text-[10px] font-black text-slate-500 uppercase tracking-widest ml-1 mb-2 block">CASA</label>
                <select id="home-team"></select>
            </div>
            <div>
                <label class="text-[10px] font-black text-slate-500 uppercase tracking-widest ml-1 mb-2 block">OSPITE</label>
                <select id="away-team"></select>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div class="bg-black/20 p-5 rounded-2xl border border-slate-800/50">
                <span class="text-xs font-black text-slate-400 uppercase tracking-widest block mb-3">Linee Falli</span>
                <input type="number" id="line-f-match" value="24.5" step="0.5" class="input-dark text-xl py-3 mb-2">
            </div>
            <div class="bg-black/20 p-5 rounded-2xl border border-slate-800/50">
                <span class="text-xs font-black text-slate-400 uppercase tracking-widest block mb-3">Linee Tiri</span>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="text-[9px] text-slate-600 block mb-1 text-center font-bold">TOTALI</label>
                        <input type="number" id="line-t-match" value="23.5" step="0.5" class="input-dark">
                    </div>
                    <div>
                        <label class="text-[9px] text-slate-600 block mb-1 text-center font-bold">IN PORTA</label>
                        <input type="number" id="line-tp-match" value="8.5" step="0.5" class="input-dark">
                    </div>
                </div>
            </div>
        </div>

        <button id="btn-calc" onclick="processAnalysis()" class="w-full py-5 bg-blue-600 hover:bg-blue-500 text-white font-black text-xl rounded-2xl shadow-xl active:scale-95 transition-all">
            ANALIZZA DATI
        </button>
    </div>

    <div id="results-area" class="hidden space-y-12">
        <section>
            <div class="flex items-center gap-3 mb-6 border-b border-slate-800 pb-3">
                <div class="w-1.5 h-6 bg-red-500 rounded-full"></div>
                <span class="text-sm font-black text-white uppercase tracking-widest">Analisi Falli</span>
            </div>
            <div id="res-grid-falli" class="grid grid-cols-1 md:grid-cols-3 gap-4"></div>
        </section>

        <section>
            <div class="flex items-center gap-3 mb-6 border-b border-slate-800 pb-3">
                <div class="w-1.5 h-6 bg-blue-500 rounded-full"></div>
                <span class="text-sm font-black text-white uppercase tracking-widest">Analisi Tiri</span>
            </div>
            <div id="res-grid-tiri" class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4"></div>
            <div id="res-grid-tp" class="grid grid-cols-1 md:grid-cols-3 gap-4"></div>
        </section>
    </div>
</main>

<script>
// ==========================================
// 🟢 CONFIG API & LOGICA AUTOMATICA
// ==========================================
const API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3"; 
const LEAGUE_IDS = { SERIE_A: 135, LIGA: 140, PREMIER: 39 };

let DB = { teams: [], statsCache: {} };
let CUR_L = 'SERIE_A';
let SEASON = 2025; 

document.addEventListener('DOMContentLoaded', () => switchLeague('SERIE_A'));

async function switchLeague(l) {
    CUR_L = l;
    const status = document.getElementById('status-display');
    const resultArea = document.getElementById('results-area');
    if(resultArea) resultArea.classList.add('hidden');
    
    status.innerHTML = `<div class="loader"></div> <span class="text-[11px] font-black text-slate-400 uppercase">Connecting ${l}...</span>`;
    
    const trySeason = async (year) => {
        try {
            const url = `https://v3.football.api-sports.io/teams?league=${LEAGUE_IDS[l]}&season=${year}`;
            const res = await fetch(url, {
                headers: { "x-apisports-key": API_KEY }
            });
            const data = await res.json();
            
            if (data.errors && Object.keys(data.errors).length > 0) {
                return { error: Object.values(data.errors)[0] };
            }
            
            if (!data.response || data.response.length === 0) {
                return null;
            }
            return { data: data.response };
        } catch (e) {
            return { error: e.message };
        }
    };

    try {
        let result = await trySeason(2025);
        SEASON = 2025;
        
        if (!result || result.error || !result.data) {
            console.log("Season 2025 failed/empty, trying 2024...");
            result = await trySeason(2024);
            if (result && result.data) SEASON = 2024;
        }
        
        if (!result || result.error || !result.data) {
            console.log("Season 2024 failed/empty, trying 2023...");
            result = await trySeason(2023);
            if (result && result.data) SEASON = 2023;
        }

        if (!result || result.error || !result.data) {
            throw new Error(result?.error || "Dati non trovati nelle ultime 3 stagioni");
        }

        DB.teams = result.data.map(r => ({ id: r.team.id, name: r.team.name })).sort((a,b) => a.name.localeCompare(b.name));

        const h = document.getElementById('home-team'), a = document.getElementById('away-team');
        if (h && a) {
            h.innerHTML = ''; a.innerHTML = '';
            DB.teams.forEach(t => { 
                h.add(new Option(t.name.toUpperCase(), t.id)); 
                a.add(new Option(t.name.toUpperCase(), t.id)); 
            });
            if (DB.teams.length > 1) a.selectedIndex = 1;
        }

        status.innerHTML = `<span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span><span class="text-emerald-400 text-[11px] font-black uppercase">${l} ${SEASON} OK</span>`;
    } catch(err) {
        console.error("CRITICAL API ERROR:", err);
        status.innerHTML = `<span class="text-red-500 text-[11px] font-black uppercase">ERR: ${err.message.substring(0,12)}</span>`;
        alert("Errore Critico API: " + err.message);
    }
}

async function fetchStats(teamId) {
    const cacheKey = `${CUR_L}_${SEASON}_${teamId}`;
    if (DB.statsCache[cacheKey]) return DB.statsCache[cacheKey];

    const res = await fetch(`https://v3.football.api-sports.io/teams/statistics?league=${LEAGUE_IDS[CUR_L]}&season=${SEASON}&team=${teamId}`, {
        headers: { "x-apisports-key": API_KEY }
    });
    const data = await res.json();
    
    if (data.errors && Object.keys(data.errors).length > 0) {
        const errKey = Object.keys(data.errors)[0];
        throw new Error(`${errKey}: ${data.errors[errKey]}`);
    }

    DB.statsCache[cacheKey] = data.response;
    return data.response;
}

async function processAnalysis() {
    const btn = document.getElementById('btn-calc');
    const hId = document.getElementById('home-team').value;
    const aId = document.getElementById('away-team').value;
    const hName = document.getElementById('home-team').options[document.getElementById('home-team').selectedIndex].text;
    const aName = document.getElementById('away-team').options[document.getElementById('away-team').selectedIndex].text;

    if (hId === aId) {
        alert("Seleziona due squadre diverse!");
        return;
    }

    btn.disabled = true;
    btn.innerHTML = `<div class="loader"></div> ELABORAZIONE...`;

    try {
        const [hStats, aStats] = await Promise.all([fetchStats(hId), fetchStats(aId)]);

        if (!hStats || !aStats || !hStats.fixtures || !aStats.fixtures) {
            alert("Dati non disponibili per queste squadre nella stagione " + SEASON);
            throw new Error("Missing Stats Data");
        }

        const gH = hStats.fixtures.played.home || 1;
        const gA = aStats.fixtures.played.away || 1;

        // FALLI
        const fCommH = (hStats.fouls?.committed?.total?.home || 0) / gH;
        const fSubA = (aStats.fouls?.drawn?.total?.away || 0) / gA;
        const expFalliH = (fCommH + fSubA) / 2;

        const fCommA = (aStats.fouls?.committed?.total?.away || 0) / gA;
        const fSubH = (hStats.fouls?.drawn?.total?.home || 0) / gH;
        const expFalliA = (fCommA + fSubH) / 2;

        // TIRI
        const tFattiH = (hStats.shots?.total?.home || 0) / gH;
        const tSubA = (aStats.shots?.total?.away || 0) * 0.95 / gA;
        const expTiriH = (tFattiH + tSubA) / 2;

        const tFattiA = (aStats.shots?.total?.away || 0) / gA;
        const tSubH = (hStats.shots?.total?.home || 0) * 0.9 / gH;
        const expTiriA = (tFattiA + tSubH) / 2;

        // IN PORTA
        const tpFattiH = (hStats.shots?.on_goal?.home || 0) / gH;
        const tpSubA = (aStats.shots?.on_goal?.away || 0) * 0.85 / gA;
        const expTpH = (tpFattiH + tpSubA) / 2;

        const tpFattiA = (aStats.shots?.on_goal?.away || 0) / gA;
        const tpSubH = (hStats.shots?.on_goal?.home || 0) * 0.8 / gH;
        const expTpA = (tpFattiA + tpSubH) / 2;

        renderResults(hName, aName, expFalliH, expFalliA, expTiriH, expTiriA, expTpH, expTpA);
        
        document.getElementById('results-area').classList.remove('hidden');
        window.scrollTo({ top: document.getElementById('results-area').offsetTop - 50, behavior: 'smooth' });

    } catch(err) {
        console.error("Analysis Error:", err);
        alert("Errore durante l'analisi: " + err.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = "ANALIZZA DATI";
    }
}

function renderResults(h, a, efh, efa, eth, eta, eph, epa) {
    const lF = parseFloat(document.getElementById('line-f-match').value);
    const lT = parseFloat(document.getElementById('line-t-match').value);
    const lP = parseFloat(document.getElementById('line-tp-match').value);

    document.getElementById('res-grid-falli').innerHTML = 
        createCard("MATCH FALLI", efh + efa, lF) + 
        createCard(h, efh, lF/2) + 
        createCard(a, efa, lF/2);

    document.getElementById('res-grid-tiri').innerHTML = 
        createCard("MATCH TIRI TOT", eth + eta, lT) + 
        createCard(h, eth, eth > 12 ? 12.5 : 11.5) + 
        createCard(a, eta, eta > 10 ? 10.5 : 9.5);

    document.getElementById('res-grid-tp').innerHTML = 
        createCard("PORTA TOTALE", eph + epa, lP) + 
        createCard(h, eph, 4.5) + 
        createCard(a, epa, 3.5);
}

function createCard(title, val, line) {
    const diff = val - line;
    let style = "border-slate-800", rec = "DATA ERR", tag = "";
    
    if(isNaN(val) || val === 0) {
        return `<div class="value-box border-slate-800 opacity-50"><div class="res-text text-slate-500">N/D</div><div class="text-[10px] uppercase font-black">${title}</div></div>`;
    }

    if(diff >= 1.5) { style = "val-top"; rec = "OVER " + line; tag = "TOP"; }
    else if(diff >= 0.5) { style = "val-good"; rec = "OVER " + line; tag = "GOOD"; }
    else if(diff <= -1.5) { style = "val-top"; rec = "UNDER " + line; tag = "TOP"; }
    else if(diff <= -0.5) { style = "val-good"; rec = "UNDER " + line; tag = "GOOD"; }
    else { rec = "NO EDGE"; }

    return `
        <div class="value-box ${style}">
            ${tag ? `<div class="tag-pill"><i data-lucide="zap" class="w-2.5 h-2.5 fill-current"></i> ${tag}</div>` : ''}
            <div class="text-[10px] font-black text-slate-500 uppercase mb-2 tracking-widest">${title}</div>
            <div class="res-text">${rec}</div>
            <div class="text-[11px] font-black tracking-tighter opacity-80">AI: ${val.toFixed(2)} | SUPER VALORE</div>
        </div>
    `;
}
</script>
</body>
</html>
"""

components.html(html_code, height=1400, scrolling=True)
