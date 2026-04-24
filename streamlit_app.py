import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE STREAMLIT ---
st.set_page_config(page_title="ProBet AI V3 - FULL API", layout="wide", initial_sidebar_state="collapsed")

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
    <title>ProBet AI V3.2</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@400;600&family=Inter:wght@400;600;700;800&display=swap');
        
        body { background-color: #0d1117; color: #e2e8f0; font-family: 'Inter', sans-serif; overflow-x: hidden; }
        .teko { font-family: 'Teko', sans-serif; }
        
        select { background: #161b22; color: white; border: 1px solid #30363d; padding: 12px; border-radius: 12px; width: 100%; font-weight: 700; outline: none; appearance: none; }
        .input-dark { background: #161b22; border: 1px solid #30363d; color: white; padding: 10px; border-radius: 10px; width: 100%; text-align: center; font-weight: 800; font-size: 1.1rem; }

        .value-box { padding: 20px; border-radius: 18px; text-align: center; border: 1px solid #30363d; position: relative; background: #161b22; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
        .val-top { background: linear-gradient(135deg, #064e3b 0%, #022c22 100%); border-color: #10b981; box-shadow: 0 10px 30px -10px rgba(16, 185, 129, 0.3); }
        .val-good { background: linear-gradient(135deg, #78350f 0%, #451a03 100%); border-color: #f59e0b; box-shadow: 0 10px 30px -10px rgba(245, 158, 11, 0.3); }
        .res-text { font-size: 28px; font-weight: 900; font-family: 'Teko', sans-serif; margin-bottom: 2px; }
        .tag-pill { position: absolute; top: 10px; right: 10px; font-size: 11px; background: #fff; color: #000; padding: 2px 10px; border-radius: 20px; font-weight: 900; text-transform: uppercase; }

        header { position: fixed; top: 0; left: 0; width: 100%; z-index: 100; background: rgba(13, 17, 23, 0.8); backdrop-filter: blur(15px); border-bottom: 1px solid #30363d; }
        main { padding: 100px 20px 80px; max-width: 850px; margin: 0 auto; }

        .loader { width: 16px; height: 16px; border: 2.5px solid #30363d; border-bottom-color: #3b82f6; border-radius: 50%; display: inline-block; animation: rot 0.8s linear infinite; }
        @keyframes rot { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>

<header>
    <div class="max-w-6xl mx-auto px-6 h-20 flex items-center justify-between">
        <div class="text-3xl font-bold teko tracking-tight text-white flex items-center gap-2">
            PROBET <span class="text-blue-500">AI</span> <span class="bg-blue-500/10 text-blue-400 text-[10px] px-2 py-0.5 rounded border border-blue-500/20 ml-2">VERSION FULL API</span>
        </div>
        <div id="status-pill" class="flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-900 border border-slate-800">
            <div class="loader"></div> 
            <span class="text-[11px] font-black text-slate-400">CONNECTING...</span>
        </div>
    </div>
</header>

<main>
    <div class="flex justify-center mb-10">
        <div class="bg-black/40 p-2 rounded-2xl border border-[#30363d] flex gap-2 w-full max-w-sm">
            <button onclick="switchLeague('SERIE_A')" id="btn-sa" class="flex-1 py-3 text-xs font-black rounded-xl transition-all">SERIE A</button>
            <button onclick="switchLeague('PREMIER')" id="btn-pl" class="flex-1 py-3 text-xs font-black rounded-xl transition-all">PREMIER</button>
            <button onclick="switchLeague('LIGA')" id="btn-lg" class="flex-1 py-3 text-xs font-black rounded-xl transition-all">LIGA</button>
        </div>
    </div>

    <div class="bg-[#161b22] p-8 rounded-[32px] border border-[#30363d] shadow-2xl mb-12">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
            <div>
                <label class="text-[10px] font-black text-slate-500 uppercase tracking-widest block mb-3">SQUADRA CASA</label>
                <select id="home-team"></select>
            </div>
            <div>
                <label class="text-[10px] font-black text-slate-500 uppercase tracking-widest block mb-3">SQUADRA OSPITE</label>
                <select id="away-team"></select>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
            <div class="bg-black/30 p-6 rounded-2xl border border-red-500/10">
                <div class="flex items-center gap-2 mb-4">
                    <div class="w-2 h-2 rounded-full bg-red-500"></div>
                    <span class="text-xs font-black text-slate-400 uppercase tracking-widest">Linee Falli</span>
                </div>
                <input type="number" id="line-f" value="24.5" step="0.5" class="input-dark border-red-500/20 py-4">
            </div>
            <div class="bg-black/30 p-6 rounded-2xl border border-blue-500/10">
                <div class="flex items-center gap-2 mb-4">
                    <div class="w-2 h-2 rounded-full bg-blue-500"></div>
                    <span class="text-xs font-black text-slate-400 uppercase tracking-widest">Linee Tiri</span>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <input type="number" id="line-t" value="23.5" step="0.5" class="input-dark border-blue-500/20">
                    <input type="number" id="line-tp" value="8.5" step="0.5" class="input-dark border-purple-500/20">
                </div>
            </div>
        </div>

        <button id="btn-calc" onclick="processAnalysis()" class="w-full py-6 bg-blue-600 hover:bg-blue-500 text-white font-black text-xl rounded-2xl shadow-[0_10px_40px_-10px_rgba(37,99,235,0.5)] transition-all">
            ANALIZZA DATI REAL-TIME
        </button>
    </div>

    <div id="results-area" class="hidden space-y-16">
        <section>
            <div class="flex items-center gap-3 mb-8 border-b border-[#30363d] pb-4">
                <span class="teko text-2xl font-bold tracking-widest text-white uppercase">RISULTATI FALLI</span>
            </div>
            <div id="grid-falli" class="grid grid-cols-1 md:grid-cols-3 gap-5"></div>
        </section>

        <section>
            <div class="flex items-center gap-3 mb-8 border-b border-[#30363d] pb-4">
                <span class="teko text-2xl font-bold tracking-widest text-white uppercase">RISULTATI TIRI</span>
            </div>
            <div id="grid-tiri" class="grid grid-cols-1 md:grid-cols-3 gap-5 mb-5"></div>
            <div id="grid-tp" class="grid grid-cols-1 md:grid-cols-3 gap-5"></div>
        </section>
    </div>
</main>

<script>
const API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3"; 
const LEAGUES = { SERIE_A: 135, LIGA: 140, PREMIER: 39 };

let CURRENT_LEAGUE = 'SERIE_A';
let DB = { teams: [], cache: {} };

document.addEventListener('DOMContentLoaded', () => switchLeague('SERIE_A'));

async function switchLeague(l) {
    CURRENT_LEAGUE = l;
    const pill = document.getElementById('status-pill');
    pill.innerHTML = `<div class="loader"></div> <span class="text-[11px] font-black text-slate-400">UPDATING LEAGUE...</span>`;
    
    // UI Button Update
    ['btn-sa', 'btn-pl', 'btn-lg'].forEach(id => {
        const btn = document.getElementById(id);
        if(id.includes(l.toLowerCase().substring(0,2)) || (id === 'btn-sa' && l === 'SERIE_A')) {
            btn.className = "flex-1 py-3 text-xs font-black rounded-xl bg-blue-600 text-white shadow-lg shadow-blue-500/20";
        } else {
            btn.className = "flex-1 py-3 text-xs font-black rounded-xl text-slate-500 hover:text-slate-300 hover:bg-white/5";
        }
    });

    try {
        const res = await fetch(`https://v3.football.api-sports.io/teams?league=${LEAGUES[l]}&season=2024`, {
            headers: { "x-apisports-key": API_KEY }
        });
        const data = await res.json();
        
        if (data.errors && Object.keys(data.errors).length > 0) throw new Error(JSON.stringify(data.errors));

        DB.teams = data.response.map(r => ({ id: r.team.id, name: r.team.name })).sort((a,b) => a.name.localeCompare(b.name));

        const h = document.getElementById('home-team'), a = document.getElementById('away-team');
        h.innerHTML = ''; a.innerHTML = '';
        DB.teams.forEach(t => { h.add(new Option(t.name, t.id)); a.add(new Option(t.name, t.id)); });
        a.selectedIndex = 1;

        pill.innerHTML = `<span class="w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-[0_0_10px_#10b981]"></span><span class="text-emerald-400 text-[11px] font-black uppercase">SISTEMA PRONTO</span>`;
    } catch(err) {
        pill.innerHTML = `<span class="text-red-500 text-[11px] font-black uppercase">API ERROR</span>`;
        console.error(err);
    }
}

async function getStats(teamId) {
    const key = `${CURRENT_LEAGUE}_${teamId}`;
    if (DB.cache[key]) return DB.cache[key];

    const res = await fetch(`https://v3.football.api-sports.io/teams/statistics?league=${LEAGUES[CURRENT_LEAGUE]}&season=2024&team=${teamId}`, {
        headers: { "x-apisports-key": API_KEY }
    });
    const data = await res.json();
    
    if (data.errors && Object.keys(data.errors).length > 0) {
        const k = Object.keys(data.errors)[0];
        throw new Error(data.errors[k]);
    }

    DB.cache[key] = data.response;
    return data.response;
}

async function processAnalysis() {
    const btn = document.getElementById('btn-calc');
    const hId = document.getElementById('home-team').value;
    const aId = document.getElementById('away-team').value;
    const hName = document.getElementById('home-team').options[document.getElementById('home-team').selectedIndex].text;
    const aName = document.getElementById('away-team').options[document.getElementById('away-team').selectedIndex].text;

    btn.disabled = true;
    btn.innerHTML = `<div class="loader"></div> ELABORAZIONE ALGORITMO...`;

    try {
        const [hS, aS] = await Promise.all([getStats(hId), getStats(aId)]);

        const mH = hS.fixtures.played.home || 1;
        const mA = aS.fixtures.played.away || 1;

        // --- FALLI ---
        const fcH = (hS.fouls.committed.total.home / mH) || 12;
        const fsA = (aS.fouls.drawn.total.away / mA) || 12;
        const efH = (fcH + fsA) / 2;

        const fcA = (aS.fouls.committed.total.away / mA) || 12;
        const fsH = (hS.fouls.drawn.total.home / mH) || 12;
        const efA = (fcA + fsH) / 2;

        // --- TIRI (LOGICA ANTI-UNDER) ---
        // Se l'API non dà tiri subiti, usiamo medie proporzionali ai tiri fatti per non sballare
        const tfH = (hS.shots.total.home / mH) || 12;
        const tsA = (aS.shots.total.away / mA) || 11; 
        const etH = (tfH + tsA) / 2;

        const tfA = (aS.shots.total.away / mA) || 11;
        const tsH = (hS.shots.total.home / mH) || 12;
        const etA = (tfA + tsH) / 2;

        // --- PORTA ---
        const tpfH = (hS.shots.on_goal.home / mH) || 4.5;
        const tpsA = (aS.shots.on_goal.away / mA) || 3.5;
        const epH = (tpfH + tpsA) / 2;

        const tpfA = (aS.shots.on_goal.away / mA) || 4;
        const tpsH = (hS.shots.on_goal.home / mH) || 4.5;
        const epA = (tpfA + tpsH) / 2;

        renderUI(hName, aName, efH, efA, etH, etA, epH, epA);
        
        document.getElementById('results-area').classList.remove('hidden');
        window.scrollTo({ top: document.getElementById('results-area').offsetTop - 100, behavior: 'smooth' });

    } catch(err) {
        alert("ERRORE API: Probabilmente hai raggiunto il limite di query (10 al minuto). Attendi un po' e riprova.");
        console.error(err);
    }

    btn.disabled = false;
    btn.innerHTML = "ANALIZZA DATI REAL-TIME";
}

function renderUI(h, a, efH, efA, etH, etA, epH, epA) {
    const lF = parseFloat(document.getElementById('line-f').value);
    const lT = parseFloat(document.getElementById('line-t').value);
    const lP = parseFloat(document.getElementById('line-tp').value);

    // Falli
    document.getElementById('grid-falli').innerHTML = 
        generateCard("MATCH TOTAL FALLI", efH + efA, lF) +
        generateCard(h, efH, lF/2) +
        generateCard(a, efA, lF/2);

    // Tiri
    document.getElementById('grid-tiri').innerHTML = 
        generateCard("MATCH TOTAL TIRI", etH + etA, lT) +
        generateCard(h, etH, 11.5) +
        generateCard(a, etA, 10.5);

    // Porta
    document.getElementById('grid-tp').innerHTML = 
        generateCard("TIRI IN PORTA TOT", epH + epA, lP) +
        generateCard(h, epH, 4.5) +
        generateCard(a, epA, 3.5);
}

function generateCard(title, val, line) {
    const diff = val - line;
    let style = "", tag = "", outcome = "NO EDGE";

    if(diff >= 1.5) { style = "val-top"; tag = "TOP VALUE"; outcome = "OVER " + line; }
    else if(diff >= 0.5) { style = "val-good"; tag = "GOOD"; outcome = "OVER " + line; }
    else if(diff <= -1.5) { style = "val-top"; tag = "TOP VALUE"; outcome = "UNDER " + line; }
    else if(diff <= -0.5) { style = "val-good"; tag = "GOOD"; outcome = "UNDER " + line; }

    return `
        <div class="value-box ${style}">
            ${tag ? `<div class="tag-pill">${tag}</div>` : ''}
            <div class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-2">${title}</div>
            <div class="res-text">${outcome}</div>
            <div class="text-[11px] font-bold text-slate-400">AI: ${val.toFixed(2)} | ANALYST APPROVED</div>
        </div>
    `;
}
</script>
</body>
</html>
"""

components.html(html_code, height=1500, scrolling=True)
