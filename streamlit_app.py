import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE STREAMLIT ---
st.set_page_config(page_title="ProBet AI V3 - FULL API AUTOMATION", layout="wide", initial_sidebar_state="collapsed")

# CSS per rendere l'app a tutto schermo e con look nativo
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
    <title>ProBet AI V3 - API FULL</title>
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
            padding: 14px; 
            border-radius: 14px; 
            width: 100%; 
            font-weight: 800; 
            outline: none;
            appearance: none;
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
            padding: 22px; 
            border-radius: 18px; 
            text-align: center; 
            border: 1px solid; 
            position: relative; 
            background: #1e293b;
            border-color: #334155;
            transition: transform 0.2s ease;
        }
        .val-top { 
            background: linear-gradient(135deg, #166534 0%, #14532d 100%); 
            border-color: #22c55e; 
            box-shadow: 0 0 20px rgba(34, 197, 94, 0.2);
        }
        .val-good { 
            background: linear-gradient(135deg, #854d0e 0%, #713f12 100%); 
            border-color: #eab308; 
        }
        .res-text { font-size: 28px; font-weight: 900; font-family: 'Teko', sans-serif; line-height: 1; margin-bottom: 4px; }
        .tag-pill { 
            position: absolute; top: 10px; right: 10px; 
            font-size: 10px; background: #fff; color: #000; 
            padding: 2px 10px; border-radius: 20px; 
            font-weight: 900; display: flex; items-center: center; gap: 4px;
        }

        header { 
            position: fixed; top: 0; left: 0; width: 100%; z-index: 100;
            background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(15px);
            border-bottom: 1px solid #1e293b;
        }
        main { padding: 110px 16px 80px; max-width: 850px; margin: 0 auto; }

        .loader { 
            width: 16px; height: 16px; border: 2px solid #475569; 
            border-bottom-color: #3b82f6; border-radius: 50%; 
            display: inline-block; animation: rot 1s linear infinite; 
        }
        @keyframes rot { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>

<header>
    <div class="max-w-6xl mx-auto px-6 h-20 flex items-center justify-between">
        <div class="text-3xl font-bold teko tracking-wider text-white">
            PROBET <span class="text-blue-500">AI</span> <span class="text-slate-500 text-xs ml-2">VERSION FULL API</span>
        </div>
        <div id="status-display" class="flex items-center gap-2 px-5 py-2 rounded-full bg-slate-900 border border-slate-800 shadow-xl">
            <div class="loader"></div> 
            <span class="text-[11px] font-black text-slate-400 uppercase tracking-tighter">Connecting to Global Data</span>
        </div>
    </div>
</header>

<main>
    <!-- League Switcher -->
    <div class="flex justify-center mb-10">
        <div class="bg-slate-900 p-2 rounded-2xl border border-slate-800 flex gap-2 w-full max-w-sm">
            <button onclick="switchLeague('SERIE_A')" id="btn-sa" class="flex-1 py-4 text-xs font-black rounded-xl transition-all">SERIE A</button>
            <button onclick="switchLeague('PREMIER')" id="btn-pl" class="flex-1 py-4 text-xs font-black rounded-xl transition-all">PREMIER</button>
            <button onclick="switchLeague('LIGA')" id="btn-lg" class="flex-1 py-4 text-xs font-black rounded-xl transition-all">LIGA</button>
        </div>
    </div>

    <!-- Inputs -->
    <div class="bg-slate-900/60 p-8 rounded-[32px] border border-slate-800 shadow-2xl backdrop-blur-xl mb-12">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
            <div class="relative">
                <label class="text-[10px] font-black text-slate-500 uppercase tracking-widest ml-1 mb-3 block">Match Home</label>
                <select id="home-team"></select>
            </div>
            <div class="relative">
                <label class="text-[10px] font-black text-slate-500 uppercase tracking-widest ml-1 mb-3 block">Match Away</label>
                <select id="away-team"></select>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
            <div class="bg-black/30 p-6 rounded-2xl border border-slate-800/50">
                <span class="text-xs font-black text-slate-400 uppercase tracking-widest block mb-4">Bookmaker Lines - Fouls</span>
                <input type="number" id="line-f-match" value="24.5" step="0.5" class="input-dark text-2xl py-4 border-red-500/20">
            </div>
            <div class="bg-black/30 p-6 rounded-2xl border border-slate-800/50">
                <span class="text-xs font-black text-slate-400 uppercase tracking-widest block mb-4">Bookmaker Lines - Shots</span>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="text-[9px] text-slate-600 block mb-2 text-center font-black">TOTAL SHOTS</label>
                        <input type="number" id="line-t-match" value="23.5" step="0.5" class="input-dark">
                    </div>
                    <div>
                        <label class="text-[9px] text-slate-600 block mb-2 text-center font-black">ON GOAL</label>
                        <input type="number" id="line-tp-match" value="8.5" step="0.5" class="input-dark">
                    </div>
                </div>
            </div>
        </div>

        <button id="btn-calc" onclick="runAnalysis()" class="w-full py-6 bg-blue-600 hover:bg-blue-500 text-white font-black text-2xl rounded-2xl shadow-[0_15px_30px_-5px_rgba(37,99,235,0.4)] active:scale-[0.98] transition-all">
            RUN AI PREDICTION
        </button>
    </div>

    <!-- Results -->
    <div id="results-area" class="hidden space-y-16">
        <section>
            <div class="flex items-center gap-4 mb-8 border-b border-slate-800 pb-4">
                <div class="w-2 h-8 bg-red-500 rounded-full shadow-[0_0_10px_rgba(239,68,68,0.5)]"></div>
                <span class="text-lg font-black text-white uppercase tracking-tighter">Fouls Prediction (API Powered)</span>
            </div>
            <div id="res-f" class="grid grid-cols-1 md:grid-cols-3 gap-5"></div>
        </section>

        <section>
            <div class="flex items-center gap-4 mb-8 border-b border-slate-800 pb-4">
                <div class="w-2 h-8 bg-blue-500 rounded-full shadow-[0_0_10px_rgba(59,130,246,0.5)]"></div>
                <span class="text-lg font-black text-white uppercase tracking-tighter">Shots Analysis (Live Stats)</span>
            </div>
            <div id="res-t" class="grid grid-cols-1 md:grid-cols-3 gap-5 mb-6"></div>
            <div id="res-tp" class="grid grid-cols-1 md:grid-cols-3 gap-5"></div>
        </section>
    </div>
</main>

<script>
// =====================================================================
// 🔑 INSERISCI QUI LA TUA API KEY - (API-SPORTS.IO)
// =====================================================================
const API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3"; 
// =====================================================================

const L_IDS = { SERIE_A: 135, LIGA: 140, PREMIER: 39 };
let CURRENT_L = 'SERIE_A';
let TEAMS_CACHE = [];

document.addEventListener('DOMContentLoaded', () => {
    if(window.lucide) lucide.createIcons();
    switchLeague('SERIE_A');
});

async function switchLeague(l) {
    CURRENT_L = l;
    
    // UI Buttons
    ['btn-sa', 'btn-pl', 'btn-lg'].forEach(id => {
        const el = document.getElementById(id);
        const isActive = (id === `btn-${l.toLowerCase().substring(0,2)}`) || (id === 'btn-sa' && l === 'SERIE_A');
        el.className = isActive 
            ? "flex-1 py-4 text-xs font-black rounded-xl bg-blue-600 text-white shadow-xl" 
            : "flex-1 py-4 text-xs font-black rounded-xl text-slate-400 hover:bg-slate-800 transition-colors";
    });

    const status = document.getElementById('status-display');
    status.innerHTML = `<div class="loader"></div> <span class="text-[11px] font-black text-slate-400">SEARCHING TEAMS...</span>`;

    try {
        const res = await fetch(`https://v3.football.api-sports.io/teams?league=${L_IDS[l]}&season=2024`, {
            headers: { "x-apisports-key": API_KEY }
        });
        const data = await res.json();
        TEAMS_CACHE = data.response.map(r => ({ id: r.team.id, name: r.team.name })).sort((a,b) => a.name.localeCompare(b.name));

        const hS = document.getElementById('home-team'), aS = document.getElementById('away-team');
        hS.innerHTML = ''; aS.innerHTML = '';
        TEAMS_CACHE.forEach(t => {
            hS.add(new Option(t.name, t.id));
            aS.add(new Option(t.name, t.id));
        });
        aS.selectedIndex = 1;

        status.innerHTML = `<span class="w-3 h-3 rounded-full bg-emerald-500 shadow-[0_0_12px_rgba(16,185,129,0.5)]"></span><span class="text-emerald-400 text-[11px] font-black">API CONNECTED: 2024 SEASON</span>`;
    } catch(err) {
        status.innerHTML = `<span class="text-red-500 text-[11px] font-black">CONNECTION FAILED</span>`;
    }
}

async function runAnalysis() {
    const btn = document.getElementById('btn-calc');
    const hId = document.getElementById('home-team').value;
    const aId = document.getElementById('away-team').value;
    const hName = document.getElementById('home-team').options[document.getElementById('home-team').selectedIndex].text;
    const aName = document.getElementById('away-team').options[document.getElementById('away-team').selectedIndex].text;

    if(hId === aId) return alert("Select different teams");

    btn.disabled = true;
    btn.innerHTML = '<div class="loader"></div> CONNECTING API...';

    try {
        // --- FETCHING STATISTICS FOR BOTH TEAMS ---
        const [hStats, aStats] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${L_IDS[CURRENT_L]}&season=2024&team=${hId}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${L_IDS[CURRENT_L]}&season=2024&team=${aId}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
        ]);

        const h = hStats.response, a = aStats.response;

        // --- 📊 CALCOLO TIRI (AUTOMATICO) ---
        // Media = (Tiri fatti Casa / Partite fatte Casa + Tiri subiti Ospite / Partite fatte Ospite) / 2
        // Nota: API Sports fornisce totali. Calcoliamo la media per partita.
        const playedH = h.fixtures.played.home || 1;
        const playedA = a.fixtures.played.away || 1;

        // TIRI TOTALI
        const tfH = (h.shots.total.home || 0) / playedH;
        const tsA = (a.shots.total.away || 0) / playedA; // Approssimazione: usiamo i fatti in trasferta come proxy se subiti non disponibili in questo endpoint
        const expTiriHome = (tfH + tsA) / 2;

        const tfA = (a.shots.total.away || 0) / playedA;
        const tsH = (h.shots.total.home || 0) / playedH;
        const expTiriAway = (tfA + tsH) / 2;

        // TIRI IN PORTA
        const tpfH = (h.shots.on_goal.home || 0) / playedH;
        const tpsA = (a.shots.on_goal.away || 0) / playedA;
        const expTPHome = (tpfH + tpsA) / 2;

        const tpfA = (a.shots.on_goal.away || 0) / playedA;
        const tpsH = (h.shots.on_goal.home || 0) / playedH;
        const expTPAway = (tpfA + tpsH) / 2;

        renderTiriUI(hName, aName, expTiriHome, expTiriAway, expTPHome, expTPAway);

        // --- 🥊 CALCOLO FALLI (AUTOMATICO) ---
        // Poiché l'API non ha "fouls_avg" nelle statistiche team, usiamo i CARTELLINI GIALLI 
        // e calcoliamo una stima basata sul trend della lega (Proxy: 1 Giallo ogni ~5-6 falli)
        const getCardAvg = (teamStats) => {
            let totalCards = 0;
            const cards = teamStats.cards.yellow;
            for(let key in cards) totalCards += cards[key].total || 0;
            return totalCards / (teamStats.fixtures.played.total || 1);
        };

        const cardH = getCardAvg(h);
        const cardA = getCardAvg(a);
        
        // Conversione Cartellini -> Falli stimati (Base scientifica sportiva: ~11-13 falli per team a partita)
        const baseFouls = 12.5; 
        const estFoulsH = baseFouls + (cardH - 2) * 2.5; // Pesiamo i gialli
        const estFoulsA = baseFouls + (cardA - 2) * 2.5;

        renderFalliUI(hName, aName, estFoulsH, estFoulsA);

        document.getElementById('results-area').classList.remove('hidden');
        window.scrollTo({ top: document.getElementById('results-area').offsetTop - 100, behavior: 'smooth' });

    } catch(err) {
        console.error(err);
        alert("API Error: Limit reached or connection lost.");
    }

    btn.disabled = false;
    btn.innerHTML = 'RUN AI PREDICTION';
}

function renderTiriUI(h, a, eth, eta, eph, epa) {
    const lT = parseFloat(document.getElementById('line-t-match').value);
    const lP = parseFloat(document.getElementById('line-tp-match').value);
    
    document.getElementById('res-t').innerHTML = 
        createCard("MATCH SHOTS TOTAL", eth + eta, lT) + 
        createCard(h, eth, eth > 12 ? 12.5 : 11.5) + 
        createCard(a, eta, eta > 10 ? 10.5 : 9.5);
        
    document.getElementById('res-tp').innerHTML = 
        createCard("TOTAL ON GOAL", eph + epa, lP) + 
        createCard(h, eph, 4.5) + 
        createCard(a, epa, 3.5);
}

function renderFalliUI(h, a, efh, efa) {
    const l = parseFloat(document.getElementById('line-f-match').value);
    document.getElementById('res-f').innerHTML = 
        createCard("MATCH FOULS EST.", efh + efa, l) + 
        createCard(h, efh, l/2) + 
        createCard(a, efa, l/2);
}

function createCard(title, val, line) {
    const diff = val - line;
    let style = "border-slate-800", rec = "NO EDGE", tag = "";
    
    if(diff >= 1.2) { style = "val-top"; rec = "OVER " + line; tag = "TOP"; }
    else if(diff >= 0.4) { style = "val-good"; rec = "OVER " + line; tag = "VALUE"; }
    else if(diff <= -1.2) { style = "val-top"; rec = "UNDER " + line; tag = "TOP"; }
    else if(diff <= -0.4) { style = "val-good"; rec = "UNDER " + line; tag = "VALUE"; }

    return `
        <div class="value-box ${style}">
            ${tag ? `<div class="tag-pill"><i data-lucide="zap" class="w-3 h-3 fill-current text-blue-500"></i> ${tag}</div>` : ''}
            <div class="text-[10px] font-black text-slate-500 uppercase mb-3 tracking-widest">${title}</div>
            <div class="res-text">${rec}</div>
            <div class="text-[11px] font-black tracking-tighter opacity-80 uppercase">Expected: ${val.toFixed(2)}</div>
        </div>
    `;
}
</script>
</body>
</html>
"""

components.html(html_code, height=1400, scrolling=True)
