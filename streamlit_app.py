import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE STREAMLIT ---
st.set_page_config(page_title="ProBet AI V3 - Full API", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
iframe { width: 100vw !important; height: 100vh !important; border: none !important; display: block !important; position: fixed; top: 0; left: 0; z-index: 9999; }
</style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <title>ProBet AI V3 - FULL API</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@400;600;700&family=Inter:wght@400;600;700;900&display=swap');
        
        body { 
            background-color: #020617; 
            color: #f1f5f9; 
            font-family: 'Inter', sans-serif; 
            margin: 0; padding: 0; 
            overflow-x: hidden; 
        }
        .teko { font-family: 'Teko', sans-serif; }
        
        /* Glassmorphism */
        .glass-panel {
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }

        select { 
            background: #0f172a; 
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
            padding: 12px; 
            border-radius: 12px; 
            width: 100%; 
            text-align: center; 
            font-weight: 800; 
            font-size: 1.25rem;
        }

        /* Value Cards */
        .card-result {
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(51, 65, 85, 0.5);
            border-radius: 24px;
            padding: 24px;
            text-align: center;
            position: relative;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .card-result:hover {
            transform: translateY(-5px);
            background: rgba(30, 41, 59, 0.6);
            border-color: rgba(59, 130, 246, 0.5);
        }
        .top-tag {
            position: absolute; top: 12px; right: 12px;
            background: #3b82f6; color: white;
            font-size: 10px; font-weight: 900;
            padding: 4px 10px; border-radius: 100px;
            letter-spacing: 0.05em;
        }

        header { 
            position: fixed; top: 0; left: 0; width: 100%; z-index: 100;
            background: rgba(2, 6, 23, 0.8); backdrop-filter: blur(15px);
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        main { padding: 110px 20px 80px; max-width: 900px; margin: 0 auto; }

        .loader { 
            width: 24px; height: 24px; border: 3px solid rgba(255,255,255,0.1); 
            border-top-color: #3b82f6; border-radius: 50%; 
            animation: spin 1s linear infinite; 
        }
        @keyframes spin { to { transform: rotate(360deg); } }

        .prog-bar {
            height: 4px; background: #1e293b; border-radius: 10px; overflow: hidden;
            margin-top: 10px;
        }
        .prog-inner {
            height: 100%; background: #3b82f6; width: 0%; transition: width 0.3s;
        }
    </style>
</head>
<body>

<header>
    <div class="max-w-6xl mx-auto px-6 h-20 flex items-center justify-between">
        <div class="flex items-center gap-4">
            <div class="text-3xl font-bold teko tracking-tight text-white">PROBET <span class="text-blue-500">AI</span></div>
            <div class="h-4 w-[1px] bg-white/20"></div>
            <div class="text-[10px] uppercase font-black text-white/40 tracking-widest pt-1">Version Full API Automata</div>
        </div>
        <div id="api-status" class="flex items-center gap-3 px-5 py-2 rounded-2xl bg-white/5 border border-white/10">
            <div class="loader-small"></div>
            <span class="text-[11px] font-black uppercase text-blue-400">Connecting...</span>
        </div>
    </div>
</header>

<main>
    <!-- League Selection -->
    <div class="flex justify-center gap-3 mb-10 overflow-x-auto pb-4 no-scrollbar">
        <button onclick="switchLeague('SERIE_A')" id="l-sa" class="px-8 py-3 rounded-2xl font-black text-xs transition-all uppercase tracking-widest border border-white/5 glass-panel">Serie A</button>
        <button onclick="switchLeague('PREMIER')" id="l-pl" class="px-8 py-3 rounded-2xl font-black text-xs transition-all uppercase tracking-widest border border-white/5 glass-panel">Premier</button>
        <button onclick="switchLeague('LIGA')" id="l-lg" class="px-8 py-3 rounded-2xl font-black text-xs transition-all uppercase tracking-widest border border-white/5 glass-panel">La Liga</button>
    </div>

    <!-- Match Config -->
    <div class="glass-panel p-8 rounded-[32px] mb-12">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
            <div>
                <label class="text-[10px] font-black text-white/30 uppercase tracking-[0.2em] mb-3 block">Match Home</label>
                <select id="h-select"></select>
            </div>
            <div>
                <label class="text-[10px] font-black text-white/30 uppercase tracking-[0.2em] mb-3 block">Match Away</label>
                <select id="a-select"></select>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
            <div class="p-5 bg-white/5 rounded-2xl border border-white/5">
                <label class="text-[10px] font-bold text-white/40 text-center block mb-3 uppercase tracking-tighter">Bookmaker Lines - Fouls</label>
                <input type="number" id="line-f" value="24.5" step="0.5" class="input-dark">
            </div>
            <div class="col-span-1 md:col-span-2 p-5 bg-white/5 rounded-2xl border border-white/5">
                <label class="text-[10px] font-bold text-white/40 text-center block mb-3 uppercase tracking-tighter">Bookmaker Lines - Shots</label>
                <div class="grid grid-cols-2 gap-4">
                    <div class="relative">
                        <span class="absolute top-[-15px] left-1/2 -translate-x-1/2 text-[8px] font-bold text-white/20">TOTAL SHOTS</span>
                        <input type="number" id="line-t" value="23.5" step="0.5" class="input-dark">
                    </div>
                    <div class="relative">
                        <span class="absolute top-[-15px] left-1/2 -translate-x-1/2 text-[8px] font-bold text-white/20">ON GOAL</span>
                        <input type="number" id="line-p" value="8.5" step="0.5" class="input-dark">
                    </div>
                </div>
            </div>
        </div>

        <button id="calc-btn" onclick="startAnalysis()" class="w-full relative group">
            <div class="absolute -inset-1 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl blur opacity-30 group-hover:opacity-100 transition duration-1000 group-hover:duration-200"></div>
            <div id="btn-content" class="relative w-full py-6 bg-blue-600 hover:bg-blue-500 rounded-2xl font-black text-xl text-white tracking-widest flex justify-center items-center gap-3 transition-all">
                <i data-lucide="zap" class="w-6 h-6"></i> ANALIZZA DATI
            </div>
        </button>
        
        <div id="analysis-progress" class="hidden mt-6">
            <div class="flex justify-between items-center mb-2">
                <span id="prog-text" class="text-[10px] font-black text-blue-400 uppercase">Fetching Match Data...</span>
                <span id="prog-val" class="text-[10px] font-black text-white">0%</span>
            </div>
            <div class="prog-bar"><div id="prog-inner" class="prog-inner"></div></div>
        </div>
    </div>

    <!-- Results -->
    <div id="results-wrap" class="hidden animate-in fade-in slide-in-from-bottom-10 block pb-20">
        <div class="flex items-center gap-4 mb-10">
            <div class="h-px flex-1 bg-gradient-to-r from-transparent to-white/10"></div>
            <span id="match-header" class="text-3xl font-bold teko tracking-widest uppercase"></span>
            <div class="h-px flex-1 bg-gradient-to-l from-transparent to-white/10"></div>
        </div>

        <section class="mb-12">
            <h3 class="text-xs font-black text-blue-500 uppercase tracking-[0.3em] mb-6 flex items-center gap-3">
                <div class="w-4 h-[2px] bg-blue-500"></div> PREVISIONI FALLI
            </h3>
            <div id="grid-falli" class="grid grid-cols-1 md:grid-cols-3 gap-5"></div>
        </section>

        <section class="mb-12">
            <h3 class="text-xs font-black text-indigo-500 uppercase tracking-[0.3em] mb-6 flex items-center gap-3">
                <div class="w-4 h-[2px] bg-indigo-500"></div> PREVISIONI TIRI
            </h3>
            <div id="grid-tiri" class="grid grid-cols-1 md:grid-cols-3 gap-5"></div>
        </section>

        <section>
            <h3 class="text-xs font-black text-purple-500 uppercase tracking-[0.3em] mb-6 flex items-center gap-3">
                <div class="w-4 h-[2px] bg-purple-500"></div> PREVISIONI IN PORTA
            </h3>
            <div id="grid-porta" class="grid grid-cols-1 md:grid-cols-3 gap-5"></div>
        </section>
    </div>
</main>

<script>
// ==========================================
// 🟢 API CONFIG (USER PAID KEY)
// ==========================================
const API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3"; 
const SEASON = 2025; // Stagione Attuale
// ==========================================

const LEAGUES = {
    SERIE_A: 135,
    PREMIER: 39,
    LIGA: 140
};

let CUR_LEAGUE = 'SERIE_A';
let TEAMS = [];
let CACHE = {};

document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
    switchLeague('SERIE_A');
});

async function switchLeague(l) {
    CUR_LEAGUE = l;
    
    // UI selection
    ['l-sa', 'l-pl', 'l-lg'].forEach(id => {
        const el = document.getElementById(id);
        if(id === 'l-'+l.toLowerCase().substring(0,2) || (id==='l-sa' && l==='SERIE_A')) {
            el.className = "px-8 py-3 rounded-2xl font-black text-xs transition-all uppercase tracking-widest border border-blue-500/50 bg-blue-500/20 text-blue-500";
        } else {
            el.className = "px-8 py-3 rounded-2xl font-black text-xs transition-all uppercase tracking-widest border border-white/5 glass-panel text-white/40";
        }
    });

    const apiStatus = document.getElementById('api-status');
    apiStatus.innerHTML = `<div class="loader-small w-3 h-3 border-2 border-white/10 border-t-blue-500 rounded-full animate-spin"></div><span class="text-[11px] font-black uppercase text-white/40 tracking-widest">Loading Teams...</span>`;

    try {
        const res = await fetch(`https://v3.football.api-sports.io/teams?league=$\{LEAGUES[l]\}&season=$\{SEASON\}`, {
            headers: { "x-apisports-key": API_KEY }
        });
        const data = await res.json();
        
        TEAMS = data.response.map(r => ({ id: r.team.id, name: r.team.name })).sort((a,b) => a.name.localeCompare(b.name));
        
        const hS = document.getElementById('h-select');
        const aS = document.getElementById('a-select');
        hS.innerHTML = ''; aS.innerHTML = '';
        
        TEAMS.forEach(t => {
            hS.add(new Option(t.name, t.id));
            aS.add(new Option(t.name, t.id));
        });
        aS.selectedIndex = 1;

        apiStatus.innerHTML = `<div class="w-2 h-2 rounded-full bg-emerald-500"></div><span class="text-[11px] font-black uppercase text-emerald-500/80 tracking-widest">API CONNECTED: 2025 SEASON</span>`;
    } catch(err) {
        apiStatus.innerHTML = `<div class="w-2 h-2 rounded-full bg-red-500"></div><span class="text-[11px] font-black uppercase text-red-500 tracking-widest">API ERROR</span>`;
    }
}

async function fetchMatchStats(teamId) {
    const cacheKey = `$\{CUR_LEAGUE\}_$\{SEASON\}_$\{teamId\}`;
    if(CACHE[cacheKey]) return CACHE[cacheKey];

    // 1. Get last 15 fixtures
    const resFix = await fetch(`https://v3.football.api-sports.io/fixtures?league=$\{LEAGUES[CUR_LEAGUE]\}&season=$\{SEASON\}&team=$\{teamId\}&last=15`, {
        headers: { "x-apisports-key": API_KEY }
    });
    const fixData = await resFix.json();
    const fixtures = fixData.response || [];

    let stats = {
        home: { p:0, t:0, s:0, p_on:0, p_off:0, f_c:0, f_s:0 },
        away: { p:0, t:0, s:0, p_on:0, p_off:0, f_c:0, f_s:0 }
    };

    // Process parallelly to avoid long waits, but handle rate limits
    const tasks = fixtures.map(async (f, idx) => {
        // Simple delay to respect rate limit if necessary (10req/min is tight, 100 is fine)
        await new Promise(r => setTimeout(r, idx * 50)); 
        
        const resSt = await fetch(`https://v3.football.api-sports.io/fixtures/statistics?fixture=$\{f.fixture.id\}`, {
            headers: { "x-apisports-key": API_KEY }
        });
        const stData = await resSt.json();
        const fStats = stData.response;
        
        if(!fStats || fStats.length < 2) return;

        const isHome = f.teams.home.id === teamId;
        const myIdx = fStats[0].team.id === teamId ? 0 : 1;
        const opIdx = 1 - myIdx;

        const getVal = (list, type) => {
            const item = list.statistics.find(s => s.type === type);
            return item ? parseInt(item.value) || 0 : 0;
        };

        const side = isHome ? 'home' : 'away';
        stats[side].p++;
        stats[side].t += getVal(fStats[myIdx], "Total Shots");
        stats[side].s += getVal(fStats[opIdx], "Total Shots");
        stats[side].p_on += getVal(fStats[myIdx], "Shots on Goal");
        stats[side].p_off += getVal(fStats[opIdx], "Shots on Goal");
        stats[side].f_c += getVal(fStats[myIdx], "Fouls");
        stats[side].f_s += getVal(fStats[opIdx], "Fouls");
    });

    await Promise.all(tasks);
    CACHE[cacheKey] = stats;
    return stats;
}

async function startAnalysis() {
    const btn = document.getElementById('calc-btn');
    const bContent = document.getElementById('btn-content');
    const progress = document.getElementById('analysis-progress');
    const pInner = document.getElementById('prog-inner');
    const pText = document.getElementById('prog-text');
    const pVal = document.getElementById('prog-val');

    const hId = parseInt(document.getElementById('h-select').value);
    const aId = parseInt(document.getElementById('a-select').value);
    const hName = document.getElementById('h-select').options[document.getElementById('h-select').selectedIndex].text;
    const aName = document.getElementById('a-select').options[document.getElementById('a-select').selectedIndex].text;

    btn.disabled = true;
    bContent.innerHTML = `<div class="loader border-t-white"></div> CONNECTING API...`;
    progress.classList.remove('hidden');
    pInner.style.width = "10%"; pVal.innerText = "10%";

    try {
        pText.innerText = "Analyzing " + hName + "...";
        const hStats = await fetchMatchStats(hId);
        pInner.style.width = "50%"; pVal.innerText = "50%";
        
        pText.innerText = "Analyzing " + aName + "...";
        const aStats = await fetchMatchStats(aId);
        pInner.style.width = "90%"; pVal.innerText = "90%";

        const getAvg = (sH, sA, key, type) => {
            const mFH = sH.home.p > 0 ? sH.home[key] / sH.home.p : 12;
            const mSA = sA.away.p > 0 ? sA.away[type] / sA.away.p : 12;
            const mFA = sA.away.p > 0 ? sA.away[key] / sA.away.p : 12;
            const mSH = sH.home.p > 0 ? sH.home[type] / sH.home.p : 12;
            
            return { h: (mFH + mSA) / 2, a: (mFA + mSH) / 2 };
        };

        const fRes = getAvg(hStats, aStats, 'f_c', 'f_s');
        const tRes = getAvg(hStats, aStats, 't', 's');
        const pRes = getAvg(hStats, aStats, 'p_on', 'p_off');

        displayResults(hName, aName, fRes, tRes, pRes);

        pInner.style.width = "100%"; pVal.innerText = "100%";
        pText.innerText = "Analysis Complete!";
        
        setTimeout(() => {
            progress.classList.add('hidden');
            bContent.innerHTML = `<i data-lucide="zap" class="w-6 h-6"></i> ANALIZZA DATI`;
            btn.disabled = false;
        }, 1000);

    } catch(err) {
        console.error(err);
        alert("Errore API: Limite raggiunto (10 req/min) o connessione persa.");
        bContent.innerHTML = `<i data-lucide="zap" class="w-6 h-6"></i> ANALIZZA DATI`;
        btn.disabled = false;
        progress.classList.add('hidden');
    }
}

function displayResults(h, a, f, t, p) {
    document.getElementById('results-wrap').classList.remove('hidden');
    document.getElementById('match-header').innerText = h + " - " + a;

    const lineF = parseFloat(document.getElementById('line-f').value);
    const lineT = parseFloat(document.getElementById('line-t').value);
    const lineP = parseFloat(document.getElementById('line-p').value);

    const render = (container, labelH, valH, valA, lineM) => {
        const tot = valH + valA;
        const diff = tot - lineM;
        let style = "", rec = "UNDER " + lineM, tag = "VALORE";
        
        if(diff >= 1.5) { style = "border-blue-500/50 bg-blue-500/10"; rec = "OVER " + lineM; tag = "TOP"; }
        else if(diff >= 0.5) { style = "border-emerald-500/30 bg-emerald-500/5"; rec = "OVER " + lineM; }
        else if(diff <= -1.5) { style = "border-red-500/50 bg-red-500/10"; rec = "UNDER " + lineM; tag = "TOP"; }
        
        document.getElementById(container).innerHTML = `
            <div class="card-result $\{style\}">
                $\{tag === 'TOP' ? `<div class="top-tag">$\{tag\}</div>` : ''\}
                <div class="text-[10px] uppercase font-black text-white/30 mb-2">Match Prediction</div>
                <div class="res-text text-4xl teko tracking-widest uppercase font-bold">$\{rec\}</div>
                <div class="text-[11px] font-black text-blue-400 mt-2 tracking-tighter">AI: $\{tot.toFixed(2)\} | SUPER VALORE</div>
            </div>
            <div class="card-result">
                <div class="text-[10px] uppercase font-black text-white/30 mb-2">$\{h\} (Exp)</div>
                <div class="res-text text-3xl teko tracking-widest font-bold">$\{valH.toFixed(2)\}</div>
            </div>
            <div class="card-result">
                <div class="text-[10px] uppercase font-black text-white/30 mb-2">$\{a\} (Exp)</div>
                <div class="res-text text-3xl teko tracking-widest font-bold">$\{valA.toFixed(2)\}</div>
            </div>
        `;
    };

    render('grid-falli', h, f.h, f.a, lineF);
    render('grid-tiri', h, t.h, t.a, lineT);
    render('grid-porta', h, p.h, p.a, lineP);
    
    window.scrollTo({ top: document.getElementById('results-wrap').offsetTop - 100, behavior: 'smooth' });
    lucide.createIcons();
}
</script>

</body>
</html>
"""

components.html(html_code, height=1800, scrolling=True)
