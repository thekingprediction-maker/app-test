import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE STREAMLIT ---
st.set_page_config(page_title="ProBet AI V3 - FULL API AUTOMATION", layout="wide", initial_sidebar_state="collapsed")

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
    <title>ProBet AI V3 - Full API</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@400;600&family=Inter:wght@400;600;700;800&display=swap');
        
        body { 
            background-color: #0f172a; 
            color: #e2e8f0; 
            font-family: 'Inter', sans-serif; 
            margin: 0; padding: 0; 
            overflow-x: hidden; 
        }
        .teko { font-family: 'Teko', sans-serif; }
        
        select { 
            background-color: #1e293b; 
            color: white; 
            border: 1px solid #334155; 
            padding: 14px; 
            border-radius: 12px; 
            width: 100%; 
            font-weight: 700; 
            appearance: none;
            outline: none;
            cursor: pointer;
        }
        .input-dark { 
            background: #1e293b; 
            border: 1px solid #334155; 
            color: white; 
            padding: 10px; 
            border-radius: 10px; 
            width: 100%; 
            text-align: center; 
            font-weight: 800; 
        }

        .value-box { 
            padding: 20px; 
            border-radius: 20px; 
            text-align: center; 
            border: 1px solid; 
            position: relative; 
            background: #1e293b;
            border-color: #334155;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .val-top { 
            background: linear-gradient(135deg, #166534 0%, #14532d 100%); 
            border-color: #22c55e; 
            box-shadow: 0 10px 30px -10px rgba(34, 197, 94, 0.4);
        }
        .val-good { 
            background: linear-gradient(135deg, #854d0e 0%, #713f12 100%); 
            border-color: #eab308; 
            box-shadow: 0 10px 30px -10px rgba(234, 179, 8, 0.4);
        }
        .res-text { font-size: 28px; font-weight: 900; font-family: 'Teko', sans-serif; line-height: 1; margin-bottom: 4px; color: white; }
        
        .tag-pill { 
            position: absolute; top: 10px; right: 10px; 
            font-size: 10px; background: rgba(255,255,255,0.95); color: #000; 
            padding: 3px 10px; border-radius: 20px; 
            font-weight: 900; display: flex; align-items: center; gap: 4px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }

        header { 
            position: fixed; top: 0; left: 0; width: 100%; z-index: 100;
            background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(15px);
            border-bottom: 1px solid rgba(51, 65, 85, 0.5);
        }
        main { padding: 110px 20px 80px; max-width: 900px; margin: 0 auto; }

        .loader { 
            width: 14px; height: 14px; border: 2px solid rgba(71, 85, 105, 0.3); 
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
            PROBET <span class="text-blue-500">AI</span> <span class="bg-blue-500/10 text-blue-500 text-[10px] px-2 py-0.5 rounded border border-blue-500/20 ml-2">V3.2 - FULL API</span>
        </div>
        <div id="status-display" class="flex items-center gap-2 px-4 py-2 rounded-full bg-slate-900/80 border border-slate-800 backdrop-blur-sm">
            <div class="loader"></div> 
            <span class="text-[11px] font-black text-slate-400 uppercase tracking-tighter">Initial connection...</span>
        </div>
    </div>
</header>

<main>
    <!-- League Selection -->
    <div class="flex justify-center mb-10">
        <div class="bg-slate-900 p-1.5 rounded-2xl border border-slate-800 flex gap-2 w-full max-w-sm shadow-2xl">
            <button onclick="switchLeague('SERIE_A')" id="btn-sa" class="flex-1 py-4 text-xs font-black rounded-xl transition-all">SERIE A</button>
            <button onclick="switchLeague('PREMIER')" id="btn-pl" class="flex-1 py-4 text-xs font-black rounded-xl transition-all">PREMIER</button>
            <button onclick="switchLeague('LIGA')" id="btn-lg" class="flex-1 py-4 text-xs font-black rounded-xl transition-all">LIGA</button>
        </div>
    </div>

    <!-- Interface -->
    <div class="bg-slate-900/40 p-8 rounded-[32px] border border-slate-800 shadow-2xl backdrop-blur-md mb-12">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
            <div>
                <label class="text-[10px] font-black text-slate-500 uppercase tracking-widest ml-2 mb-3 block">Match Home</label>
                <div class="relative">
                    <select id="home-team"></select>
                </div>
            </div>
            <div>
                <label class="text-[10px] font-black text-slate-500 uppercase tracking-widest ml-2 mb-3 block">Match Away</label>
                <div class="relative">
                    <select id="away-team"></select>
                </div>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
            <div class="bg-black/30 p-6 rounded-2xl border border-slate-800/60">
                <div class="flex items-center gap-2 mb-4 text-red-500">
                    <i data-lucide="shield-alert" class="w-4 h-4"></i>
                    <span class="text-xs font-black uppercase tracking-widest">Bookmaker Lines - Fouls</span>
                </div>
                <input type="number" id="line-f-match" value="24.5" step="0.5" class="input-dark text-2xl py-4 border-red-500/20">
            </div>
            <div class="bg-black/30 p-6 rounded-2xl border border-slate-800/60">
                <div class="flex items-center gap-2 mb-4 text-blue-500">
                    <i data-lucide="crosshair" class="w-4 h-4"></i>
                    <span class="text-xs font-black uppercase tracking-widest">Bookmaker Lines - Shots</span>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="text-[9px] text-slate-600 block mb-1 text-center font-bold">TOTAL SHOTS</label>
                        <input type="number" id="line-t-match" value="23.5" step="0.5" class="input-dark border-blue-500/20">
                    </div>
                    <div>
                        <label class="text-[9px] text-slate-600 block mb-1 text-center font-bold">ON GOAL</label>
                        <input type="number" id="line-tp-match" value="8.5" step="0.5" class="input-dark border-purple-500/20">
                    </div>
                </div>
            </div>
        </div>

        <button id="btn-calc" onclick="processAnalysis()" class="w-full py-6 bg-blue-600 hover:bg-blue-500 text-white font-black text-2xl rounded-2xl shadow-[0_0_40px_rgba(37,99,235,0.25)] active:scale-95 transition-all flex justify-center items-center gap-3">
            <i data-lucide="zap" class="w-6 h-6 fill-white"></i> ANALIZZA DATI
        </button>
    </div>

    <!-- Results -->
    <div id="results-area" class="hidden space-y-16">
        <!-- Fouls Section -->
        <section>
            <div class="flex items-center gap-3 mb-8 border-b border-white/5 pb-4">
                <div class="w-1.5 h-7 bg-red-500 rounded-full shadow-[0_0_15px_rgba(239,68,68,0.5)]"></div>
                <span class="text-lg font-black text-white teko tracking-widest uppercase">Analisi Falli (Full API)</span>
            </div>
            <div id="res-grid-falli" class="grid grid-cols-1 md:grid-cols-3 gap-5"></div>
        </section>

        <!-- Shots Section -->
        <section>
            <div class="flex items-center gap-3 mb-8 border-b border-white/5 pb-4">
                <div class="w-1.5 h-7 bg-blue-500 rounded-full shadow-[0_0_15px_rgba(59,130,246,0.5)]"></div>
                <span class="text-lg font-black text-white teko tracking-widest uppercase">Analisi Tiri (Full API)</span>
            </div>
            <div id="res-grid-tiri" class="grid grid-cols-1 md:grid-cols-3 gap-5 mb-5"></div>
            <div id="res-grid-tp" class="grid grid-cols-1 md:grid-cols-3 gap-5"></div>
        </section>
    </div>
</main>

<script>
// ==========================================
// 🟢 CONFIGURAZIONE API & CACHE
// ==========================================
const API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3"; 
const LEAGUE_IDS = { SERIE_A: 135, LIGA: 140, PREMIER: 39 };

let DB = { 
    teams: [], 
    statsCache: {} // Salva i dati per non ripetere chiamate API identiche
};
let CUR_L = 'SERIE_A';

// Inizializzazione icone Lucide
const refreshIcons = () => { if(window.lucide) lucide.createIcons(); };

document.addEventListener('DOMContentLoaded', () => {
    refreshIcons();
    switchLeague('SERIE_A');
});

// Cambia lega ed aggiorna lista squadre
async function switchLeague(l) {
    CUR_L = l;
    const status = document.getElementById('status-display');
    status.innerHTML = `<div class="loader"></div> <span class="text-[11px] font-black text-slate-400 uppercase">Updating League...</span>`;
    
    try {
        const teamsRes = await fetch(`https://v3.football.api-sports.io/teams?league=${LEAGUE_IDS[l]}&season=2024`, {
            headers: { "x-apisports-key": API_KEY }
        });
        const teamsData = await teamsRes.json();
        
        if (teamsData.errors && Object.keys(teamsData.errors).length > 0) {
            const errKey = Object.keys(teamsData.errors)[0];
            throw new Error(`${errKey}: ${teamsData.errors[errKey]}`);
        }

        DB.teams = teamsData.response.map(r => ({ id: r.team.id, name: r.team.name })).sort((a,b) => a.name.localeCompare(b.name));

        const h = document.getElementById('home-team'), a = document.getElementById('away-team');
        if (h && a) {
            h.innerHTML = ''; a.innerHTML = '';
            DB.teams.forEach(t => { 
                h.add(new Option(t.name, t.id)); 
                a.add(new Option(t.name, t.id)); 
            });
            a.selectedIndex = Math.min(1, DB.teams.length - 1);
        }

        status.innerHTML = `<span class="w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.4)]"></span><span class="text-emerald-400 text-[11px] font-black uppercase">API CONNECTED: 2024 SEASON</span>`;
    } catch(err) {
        console.error(err);
        status.innerHTML = `<span class="text-red-500 text-[11px] font-black uppercase">API LIMIT/OFFLINE</span>`;
        if (err.message.includes('rate')) {
            alert("Limite API raggiunto (max 10 richieste/minuto per piano Free). Attendi 60 secondi prima di riprovare.");
        } else {
            alert("Errore API: " + err.message);
        }
    }
}

// Recupera statistiche con caching
async function fetchStats(teamId) {
    const cacheKey = `${CUR_L}_2024_${teamId}`;
    if (DB.statsCache[cacheKey]) return DB.statsCache[cacheKey];

    const res = await fetch(`https://v3.football.api-sports.io/teams/statistics?league=${LEAGUE_IDS[CUR_L]}&season=2024&team=${teamId}`, {
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

    if(hId === aId) { alert("Scegli due squadre differenti!"); return; }

    btn.disabled = true;
    btn.innerHTML = `<div class="loader"></div> ANALYZING FULL API DATA...`;

    try {
        // Recupero statistiche per entrambe le squadre
        const [hStats, aStats] = await Promise.all([fetchStats(hId), fetchStats(aId)]);

        if (!hStats || !aStats) {
            alert("Dati non disponibili per questa partita.");
            btn.disabled = false; btn.innerHTML = "ANALIZZA DATI";
            return;
        }

        // --- CALCOLO FALLI ---
        const gH = hStats.fixtures.played.home || 1;
        const gA = aStats.fixtures.played.away || 1;

        const fCommH = hStats.fouls.committed.total.home / gH;
        const fSubA = aStats.fouls.drawn.total.away / gA;
        const valFalliH = (fCommH + fSubA) / 2;

        const fCommA = aStats.fouls.committed.total.away / gA;
        const fSubH = hStats.fouls.drawn.total.home / gH;
        const valFalliA = (fCommA + fSubH) / 2;

        // --- CALCOLO TIRI ---
        // Usiamo i tiri fatti media casa/trasferta e stimiamo i subiti dai dati league se non diretti
        const tFattiH = hStats.shots.total.home / gH;
        const tFattiA = aStats.shots.total.away / gA;
        // In mancanza di dati diretti sui subiti per team nell'endpoint stats, 
        // usiamo il bilanciamento league (Avg = 12 tiri/partita stimati)
        const expTiriH = (tFattiH + 12) / 2;
        const expTiriA = (tFattiA + 12) / 2;

        // --- CALCOLO PORTA ---
        const tpFattiH = hStats.shots.on_goal.home / gH;
        const tpFattiA = aStats.shots.on_goal.away / gA;
        const expTpH = (tpFattiH + 4) / 2;
        const expTpA = (tpFattiA + 4) / 2;

        renderCards(hName, aName, valFalliH, valFalliA, expTiriH, expTiriA, expTpH, expTpA);
        
        document.getElementById('results-area').classList.remove('hidden');
        window.scrollTo({ top: document.getElementById('results-area').offsetTop - 100, behavior: 'smooth' });

    } catch(err) {
        console.error(err);
        if (err.message.includes('rate')) {
            alert("Limite API raggiunto! Attendi un minuto prima di analizzare un'altra partita.");
        } else {
            alert("Errore durante l'analisi: " + err.message);
        }
    }

    btn.disabled = false;
    btn.innerHTML = `<i data-lucide="zap" class="w-6 h-6 fill-white"></i> ANALIZZA DATI`;
    refreshIcons();
}

function renderCards(h, a, efh, efa, eth, eta, eph, epa) {
    const lF = parseFloat(document.getElementById('line-f-match').value);
    const lT = parseFloat(document.getElementById('line-t-match').value);
    const lP = parseFloat(document.getElementById('line-tp-match').value);

    // Falli
    document.getElementById('res-grid-falli').innerHTML = 
        createCard("MATCH FALLI", efh + efa, lF) + 
        createCard(h, efh, lF/2) + 
        createCard(a, efa, lF/2);

    // Tiri
    document.getElementById('res-grid-tiri').innerHTML = 
        createCard("MATCH TIRI TOT", eth + eta, lT) + 
        createCard(h, eth, eth > 12 ? 12.5 : 11.5) + 
        createCard(a, eta, eta > 10 ? 10.5 : 9.5);

    // Porta
    document.getElementById('res-grid-tp').innerHTML = 
        createCard("PORTA TOTALE", eph + epa, lP) + 
        createCard(h, eph, 4.5) + 
        createCard(a, epa, 3.5);
}

function createCard(title, val, line) {
    const diff = val - line;
    let style = "border-slate-800", rec = "NO EDGE", tag = "";
    
    if(isNaN(val) || val === 0) {
        return `<div class="value-box border-slate-800 opacity-50"><div class="res-text text-slate-500">N/D</div><div class="text-[10px] uppercase font-black">${title}</div></div>`;
    }

    if(diff >= 1.5) { style = "val-top"; rec = "OVER " + line; tag = "TOP"; }
    else if(diff >= 0.5) { style = "val-good"; rec = "OVER " + line; tag = "GOOD"; }
    else if(diff <= -1.5) { style = "val-top"; rec = "UNDER " + line; tag = "TOP"; }
    else if(diff <= -0.5) { style = "val-good"; rec = "UNDER " + line; tag = "GOOD"; }

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
