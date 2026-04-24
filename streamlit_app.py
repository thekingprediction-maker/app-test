import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE STREAMLIT ---
st.set_page_config(page_title="ProBet AI - V3 Professional", layout="wide", initial_sidebar_state="collapsed")

# CSS per rendere l'interfaccia "nativa" (nasconde elementi Streamlit)
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
iframe { width: 100vw !important; height: 100vh !important; border: none !important; display: block !important; position: fixed; top: 0; left: 0; z-index: 9999; }
</style>
""", unsafe_allow_html=True)

# --- CODICE FRONTEND (HTML/JS) ---
html_code = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@400;600&family=Inter:wght@400;600;700;800&display=swap');
        body { background-color: #0f172a; color: #e2e8f0; font-family: 'Inter', sans-serif; margin: 0; padding: 0; width: 100%; height: 100%; overflow-x: hidden; }
        .teko { font-family: 'Teko', sans-serif; }
        select { background-color: #1e293b; color: white; border: 1px solid #334155; padding: 12px; border-radius: 12px; width: 100%; font-weight: 700; outline: none; appearance: none; }
        .input-dark { background: #1e293b; border: 1px solid #334155; color: white; padding: 8px; border-radius: 8px; width: 100%; text-align: center; font-weight: 800; }
        .value-box { padding: 18px; border-radius: 16px; text-align: center; border: 1px solid; position: relative; transition: all 0.3s; background: #1e293b; border-color: #334155; }
        .val-top { background: linear-gradient(135deg, #166534 0%, #14532d 100%); border-color: #22c55e; box-shadow: 0 10px 25px -5px rgba(21, 128, 61, 0.4); }
        .val-good { background: linear-gradient(135deg, #854d0e 0%, #713f12 100%); border-color: #eab308; box-shadow: 0 10px 25px -5px rgba(161, 98, 7, 0.4); }
        .res-text { font-size: 24px; font-weight: 900; font-family: 'Teko', sans-serif; line-height: 1; margin-bottom: 4px; }
        .tag-pill { position: absolute; top: 8px; right: 8px; font-size: 10px; background: #fff; color: #000; padding: 2px 8px; border-radius: 20px; font-weight: 900; display: flex; align-items: center; gap: 3px; }
        header { position: fixed; top: 0; left: 0; width: 100%; z-index: 100; background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(12px); border-bottom: 1px solid #1e293b; }
        main { padding: 100px 16px 80px; max-width: 800px; margin: 0 auto; }
        .loader { width: 12px; height: 12px; border: 2px solid #475569; border-bottom-color: #3b82f6; border-radius: 50%; display: inline-block; animation: rot 1s linear infinite; }
        @keyframes rot { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>

<header>
    <div class="max-w-6xl mx-auto px-6 h-20 flex items-center justify-between">
        <div class="text-3xl font-bold teko tracking-tight text-white">
            PROBET <span class="text-blue-500">AI</span> <span class="text-xs text-slate-500 ml-2">V3 API</span>
        </div>
        <div id="status-display" class="flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-900 border border-slate-800">
            <div class="loader"></div> <span class="text-[11px] font-black text-slate-400">CONNECTING...</span>
        </div>
    </div>
</header>

<main>
    <div class="flex justify-center mb-8">
        <div class="bg-slate-900 p-1.5 rounded-2xl border border-slate-800 flex gap-2 w-full max-w-sm">
            <button onclick="switchLeague('SERIE_A')" id="btn-sa" class="flex-1 py-3 text-xs font-black rounded-xl">SERIE A</button>
            <button onclick="switchLeague('PREMIER')" id="btn-pl" class="flex-1 py-3 text-xs font-black rounded-xl">PREMIER</button>
            <button onclick="switchLeague('LIGA')" id="btn-lg" class="flex-1 py-3 text-xs font-black rounded-xl">LIGA</button>
        </div>
    </div>

    <div class="bg-slate-900/50 p-6 rounded-3xl border border-slate-800 shadow-2xl backdrop-blur-xl mb-10">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div>
                <label class="text-[10px] font-black text-slate-500 uppercase tracking-widest ml-1 mb-2 block">Team Casa</label>
                <select id="home-team"></select>
            </div>
            <div>
                <label class="text-[10px] font-black text-slate-500 uppercase tracking-widest ml-1 mb-2 block">Team Ospite</label>
                <select id="away-team"></select>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div class="bg-black/20 p-5 rounded-2xl border border-slate-800/50">
                <span class="text-xs font-black text-slate-400 uppercase tracking-widest block mb-4 text-red-400">Linee Falli</span>
                <input type="number" id="line-f-match" value="24.5" step="0.5" class="input-dark text-xl py-3 border-red-500/30">
            </div>
            <div class="bg-black/20 p-5 rounded-2xl border border-slate-800/50">
                <span class="text-xs font-black text-slate-400 uppercase tracking-widest block mb-4 text-blue-400">Linee Tiri</span>
                <div class="flex gap-4">
                    <input type="number" id="line-t-match" value="23.5" step="0.5" class="input-dark border-blue-500/30">
                    <input type="number" id="line-tp-match" value="8.5" step="0.5" class="input-dark border-purple-500/30">
                </div>
            </div>
        </div>

        <button id="btn-calc" onclick="processAnalysis()" class="w-full py-5 bg-blue-600 hover:bg-blue-500 text-white font-black text-xl rounded-2xl flex justify-center items-center gap-3">
            <i data-lucide="zap" class="w-6 h-6 fill-white"></i> ANALIZZA DATI
        </button>
    </div>

    <div id="results-area" class="hidden space-y-12">
        <section id="section-falli">
            <div class="flex items-center gap-3 mb-6 border-b border-slate-800 pb-3">
                <span class="text-sm font-black text-white uppercase tracking-[0.2em]">Analisi Falli (CSV Dati)</span>
            </div>
            <div id="res-grid-falli" class="grid grid-cols-1 md:grid-cols-3 gap-4"></div>
        </section>

        <section id="section-tiri">
            <div class="flex items-center gap-3 mb-6 border-b border-slate-800 pb-3">
                <span class="text-sm font-black text-white uppercase tracking-[0.2em]">Analisi Tiri (Dati Identici CSV)</span>
            </div>
            <div id="res-grid-tiri" class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4"></div>
            <div id="res-grid-tp" class="grid grid-cols-1 md:grid-cols-3 gap-4"></div>
        </section>
    </div>
</main>

<script>
// =========================================================================================
// 🟢 CONFIGURAZIONE API KEY (INSERISCI QUI LA TUA CHIAVE)
// =========================================================================================
const API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3"; 
// =========================================================================================

const L_IDS = { SERIE_A: 135, LIGA: 140, PREMIER: 39 };

// Link CSV per i Falli
const CSV_FALLI = {
    SERIE_A: {
        curr: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_CURR_SERIE_A%20-%20Foglio1.csv",
        prev: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_PREV_SERIE_A%20-%20DATI%20STAGIONE%202024_2025%20.csv"
    },
    LIGA: {
        curr: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_CURR_LIGA%20-%20Foglio1.csv",
        prev: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_PREV_LIGA%20%20-%20DATI%20STAGIONE%202024_2025.csv"
    }
};

// --- DATABASE TIRI (DATI PRESI DAI TUOI FILE CSV) ---
const INTERNAL_SHOTS = {
    SERIE_A: {
        "Atalanta": { mH:17, tfH:294, tsH:175, tpH:88, tpsH:45, mA:16, tfA:195, tsA:215, tpA:62, tpsA:83 },
        "Bologna": { mH:16, tfH:246, tsH:142, tpH:63, tpsH:53, mA:17, tfA:190, tsA:197, tpA:64, tpsA:73 },
        "Cagliari": { mH:16, tfH:160, tsH:191, tpH:52, tpsH:63, mA:17, tfA:178, tsA:240, tpA:55, tpsA:91 },
        "Como": { mH:17, tfH:279, tsH:129, tpH:108, tpsH:48, mA:16, tfA:197, tsA:176, tpA:62, tpsA:63 },
        "Fiorentina": { mH:16, tfH:252, tsH:180, tpH:68, tpsH:61, mA:17, tfA:177, tsA:253, tpA:48, tpsA:88 },
        "Genoa": { mH:17, tfH:209, tsH:183, tpH:71, tpsH:60, mA:16, tfA:182, tsA:244, tpA:63, tpsA:82 },
        "Inter": { mH:17, tfH:317, tsH:148, tpH:119, tpsH:55, mA:16, tfA:265, tsA:147, tpA:84, tpsA:41 },
        "Juventus": { mH:17, tfH:320, tsH:163, tpH:114, tpsH:39, mA:16, tfA:222, tsA:180, tpA:82, tpsA:52 },
        "Lazio": { mH:16, tfH:194, tsH:191, tpH:70, tpsH:71, mA:17, tfA:172, tsA:248, tpA:62, tpsA:63 },
        "Milan": { mH:16, tfH:262, tsH:158, tpH:81, tpsH:51, mA:17, tfA:182, tsA:212, tpA:66, tpsA:63 },
        "Napoli": { mH:16, tfH:210, tsH:178, tpH:79, tpsH:48, mA:17, tfA:221, tsA:164, tpA:75, tpsA:44 },
        "Torino": { mH:16, tfH:194, tsH:208, tpH:70, tpsH:68, mA:17, tfA:192, tsA:243, tpA:66, tpsA:76 },
        "Udinese": { mH:17, tfH:215, tsH:193, tpH:64, tpsH:57, mA:16, tfA:160, tsA:244, tpA:57, tpsA:70 },
    },
    PREMIER: {
        "Arsenal": { mH:16, tfH:263, tsH:104, tpH:79, tpsH:32, mA:17, tfA:216, tsA:161, tpA:78, tpsA:45 },
        "Liverpool": { mH:16, tfH:286, tsH:178, tpH:84, tpsH:58, mA:17, tfA:233, tsA:194, tpA:67, tpsA:68 },
        "Manchester City": { mH:16, tfH:255, tsH:147, tpH:99, tpsH:48, mA:16, tfA:220, tsA:167, tpA:71, tpsA:61 },
        "Manchester United": { mH:16, tfH:282, tsH:160, tpH:110, tpsH:54, mA:17, tfA:234, tsA:217, tpA:78, tpsA:68 },
    }
};

let CURRENT_L = 'SERIE_A';
let DB = { fouls_c: [], fouls_p: [], teams: [] };

document.addEventListener('DOMContentLoaded', () => { if(window.lucide) lucide.createIcons(); switchLeague('SERIE_A'); });

async function switchLeague(l) {
    CURRENT_L = l;
    const status = document.getElementById('status-display');
    status.innerHTML = `<div class="loader"></div> <span class="text-[11px] font-black uppercase">Loading API...</span>`;
    
    try {
        const res = await fetch(`https://v3.football.api-sports.io/teams?league=${L_IDS[l]}&season=2024`, { headers: { "x-apisports-key": API_KEY } });
        const json = await res.json();
        DB.teams = json.response.map(r => ({ id: r.team.id, name: r.team.name })).sort((a,b) => a.name.localeCompare(b.name));

        if(CSV_FALLI[l]) {
            const fc = await fetch(CSV_FALLI[l].curr).then(r => r.text());
            DB.fouls_c = Papa.parse(fc, {skipEmptyLines:true}).data.slice(1).map(r => ({ t:r[1], l:r[2], s:parseFloat(r[3])||0, c:parseFloat(r[4])||0 }));
            const fp = await fetch(CSV_FALLI[l].prev).then(r => r.text());
            DB.fouls_p = Papa.parse(fp, {skipEmptyLines:true}).data.slice(1).map(r => ({ t:r[1], l:r[2], s:parseFloat(r[3])||0, c:parseFloat(r[4])||0 }));
        }

        const hS = document.getElementById('home-team'), aS = document.getElementById('away-team');
        hS.innerHTML = ''; aS.innerHTML = '';
        DB.teams.forEach(t => { hS.add(new Option(t.name, t.id)); aS.add(new Option(t.name, t.id)); });

        status.innerHTML = `<span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span><span class="text-emerald-400 text-[11px] font-black">API PRONTA</span>`;
    } catch(e) { status.innerHTML = "API ERROR"; }
}

async function processAnalysis() {
    const hName = document.getElementById('home-team').options[document.getElementById('home-team').selectedIndex].text;
    const aName = document.getElementById('away-team').options[document.getElementById('away-team').selectedIndex].text;
    
    // --- ANALISI TIRI (CALCOLO CSV) ---
    const findS = (n) => {
        const data = INTERNAL_SHOTS[CURRENT_L];
        if(!data) return null;
        const key = Object.keys(data).find(k => n.includes(k) || k.includes(n));
        return key ? data[key] : null;
    };

    const hS = findS(hName), aS = findS(aName);
    if(hS && aS) {
        // Logica Identica ai CSV: (Fatti Casa / Partite Casa + Subiti Ospite / Partite Ospite) / 2
        const expH = ( (hS.tfH / hS.mH) + (aS.tsA / aS.mA) ) / 2;
        const expA = ( (aS.tfA / aS.mA) + (hS.tsH / hS.mH) ) / 2;
        const expPH = ( (hS.tpH / hS.mH) + (aS.tpsA / aS.mA) ) / 2;
        const expPA = ( (aS.tpA / aS.mA) + (hS.tpsH / hS.mH) ) / 2;

        renderTiri(hName, aName, expH, expA, expPH, expPA);
    }

    // --- ANALISI FALLI ---
    if(DB.fouls_c.length > 0) {
        const getF = (t, loc, dbC, dbP) => {
            const c = dbC.find(x => t.includes(x.t) || x.t.includes(t) && x.l.includes(loc));
            const p = dbP.find(x => t.includes(x.t) || x.t.includes(t) && x.l.includes(loc));
            if(!c) return { comm:12, sub:12 };
            return p ? { comm: c.c*0.8 + p.c*0.2, sub: c.s*0.8 + p.s*0.2 } : { comm: c.c, sub: c.s };
        };
        const fH = getF(hName, 'CASA', DB.fouls_c, DB.fouls_p), fA = getF(aName, 'FUORI', DB.fouls_c, DB.fouls_p);
        renderFalli(hName, aName, (fH.comm + fA.sub)/2, (fA.comm + fH.sub)/2);
    }

    document.getElementById('results-area').classList.remove('hidden');
    if(window.lucide) lucide.createIcons();
}

function renderTiri(h, a, eh, ea, eph, epa) {
    const lT = parseFloat(document.getElementById('line-t-match').value), lP = parseFloat(document.getElementById('line-tp-match').value);
    document.getElementById('res-grid-tiri').innerHTML = createBox("MATCH TOTALE", eh+ea, lT) + createBox(h, eh, eh > 12 ? 12.5 : 10.5) + createBox(a, ea, ea > 10 ? 10.5 : 8.5);
    document.getElementById('res-grid-tp').innerHTML = createBox("TIRI PORTA TOT", eph+epa, lP) + createBox(h, eph, 4.5) + createBox(a, epa, 3.5);
}

function renderFalli(h, a, fh, fa) {
    const line = parseFloat(document.getElementById('line-f-match').value);
    document.getElementById('res-grid-falli').innerHTML = createBox("MATCH FALLI", fh+fa, line) + createBox(h, fh, line/2) + createBox(a, fa, line/2);
}

function createBox(title, val, line) {
    const diff = val - line;
    let s = "", r = diff > 0 ? "OVER" : "UNDER", t = "NO EDGE";
    if(Math.abs(diff) >= 1.5) { s = "val-top"; t = "TOP"; }
    else if(Math.abs(diff) >= 0.5) { s = "val-good"; t = "GOOD"; }
    return `<div class="value-box ${s}">${t!=="NO EDGE"?`<div class="tag-pill"><i data-lucide="zap" class="w-2.5 h-2.5 fill-current"></i> ${t}</div>`:''}<div class="text-[10px] font-black opacity-50 uppercase mb-2">${title}</div><div class="res-text">${r} ${line}</div><div class="text-[11px] font-black">AI: ${val.toFixed(2)} | SUPER VALORE</div></div>`;
}
</script>
</body>
</html>
"""

components.html(html_code, height=1400, scrolling=True)
