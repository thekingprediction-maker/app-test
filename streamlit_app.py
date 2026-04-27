import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="ProBet AI - Global Stats", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
iframe { width: 100vw !important; height: 100vh !important; border: none !important; position: fixed; top: 0; left: 0; z-index: 9999; }
</style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@400;700&family=Inter:wght@400;700;900&display=swap');
        body { background-color: #0f172a; color: #e2e8f0; font-family: 'Inter', sans-serif; }
        .teko { font-family: 'Teko', sans-serif; }
        .input-dark { background:#1e293b; border:1px solid #334155; color:white; padding:12px; border-radius:10px; width:100%; text-align:center; font-weight:bold; }
        .card-res { background: #1e293b; border: 1px solid #334155; border-radius: 16px; padding: 20px; text-align: center; transition: 0.3s; }
        .val-high { border-left: 5px solid #22c55e; background: linear-gradient(135deg, #1e293b 0%, #064e3b 100%); }
        .val-med { border-left: 5px solid #eab308; background: linear-gradient(135deg, #1e293b 0%, #422006 100%); }
        .btn-main { background: #3b82f6; color: white; font-weight: 900; width: 100%; padding: 18px; border-radius: 12px; font-size: 1.2rem; }
    </style>
</head>
<body>

<div class="max-w-4xl mx-auto p-4 pt-10">
    <div class="text-center mb-8">
        <h1 class="text-4xl font-black teko tracking-widest">PROBET <span class="text-blue-500">AI v3</span></h1>
        <p class="text-[10px] text-slate-500 font-bold uppercase tracking-widest">Automated Prediction Engine</p>
    </div>

    <div class="grid grid-cols-4 gap-2 mb-6">
        <button onclick="changeLeague(135)" class="bg-blue-600 p-2 rounded-lg text-[10px] font-bold">SERIE A</button>
        <button onclick="changeLeague(39)" class="bg-slate-800 p-2 rounded-lg text-[10px] font-bold">PREMIER</button>
        <button onclick="changeLeague(140)" class="bg-slate-800 p-2 rounded-lg text-[10px] font-bold">LIGA</button>
        <button onclick="changeLeague(78)" class="bg-slate-800 p-2 rounded-lg text-[10px] font-bold">BUNDES</button>
    </div>

    <div class="bg-slate-900/50 p-6 rounded-3xl border border-slate-800">
        <div class="grid grid-cols-2 gap-4 mb-6">
            <div><label class="text-[10px] text-slate-500 font-bold ml-2">CASA</label><select id="homeTeam" class="input-dark mt-1"></select></div>
            <div><label class="text-[10px] text-slate-500 font-bold ml-2">OSPITE</label><select id="awayTeam" class="input-dark mt-1"></select></div>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
            <div><label class="text-[9px] text-slate-500 font-bold">LINEA TIRI</label><input type="number" id="l_tiri" value="24.5" step="0.5" class="input-dark text-sm"></div>
            <div><label class="text-[9px] text-slate-500 font-bold">LINEA CORNER</label><input type="number" id="l_corner" value="9.5" step="0.5" class="input-dark text-sm"></div>
            <div><label class="text-[9px] text-slate-500 font-bold">LINEA CARTELLINI</label><input type="number" id="l_cards" value="4.5" step="0.5" class="input-dark text-sm"></div>
            <div><label class="text-[9px] text-slate-500 font-bold">LINEA FALLI</label><input type="number" id="l_falli" value="25.5" step="0.5" class="input-dark text-sm"></div>
        </div>

        <button onclick="analyze()" class="btn-main shadow-lg shadow-blue-500/20 active:scale-95 transition-all">ANALIZZA MATCH</button>
    </div>

    <div id="results" class="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4 hidden pb-20"></div>
</div>

<script>
const API_KEY = "aa5e53f893088010cc7c47af17f306e9";
const DB_URL = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/DATABASE_AVANZATO_2025.csv";
let currentLeague = 135;
let manualStats = [];

// Carica il tuo CSV di GitHub all'avvio
Papa.parse(DB_URL, {
    download: true,
    header: true,
    complete: (results) => { manualStats = results.data; console.log("DB GitHub Caricato"); }
});

async function changeLeague(id) {
    currentLeague = id;
    const res = await fetch(`https://v3.football.api-sports.io/teams?league=${id}&season=2024`, {
        headers: {"x-apisports-key": API_KEY}
    });
    const data = await res.json();
    const h = document.getElementById('homeTeam');
    const a = document.getElementById('awayTeam');
    h.innerHTML = a.innerHTML = "";
    data.response.sort((x,y)=>x.team.name.localeCompare(y.team.name)).forEach(t => {
        h.add(new Option(t.team.name, t.team.id));
        a.add(new Option(t.team.name, t.team.id));
    });
}

async function analyze() {
    const idH = document.getElementById('homeTeam').value;
    const idA = document.getElementById('awayTeam').value;
    const resDiv = document.getElementById('results');
    resDiv.innerHTML = "<div class='col-span-full text-center py-10 font-bold animate-pulse text-blue-400'>INTERROGAZIONE AI ENGINE...</div>";
    resDiv.classList.remove('hidden');

    try {
        const [hRes, aRes] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${currentLeague}&season=2024&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${currentLeague}&season=2024&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
        ]);

        const sH = hRes.response;
        const sA = aRes.response;
        const mH = manualStats.find(r => r.TeamID == idH) || { xG_Per_Shot: 0.11, Falli_Fatti_Avg: 12, Falli_Subiti_Avg: 12 };
        const mA = manualStats.find(r => r.TeamID == idA) || { xG_Per_Shot: 0.11, Falli_Fatti_Avg: 12, Falli_Subiti_Avg: 12 };

        // --- CALCOLI AVANZATI ---
        // Tiri: Media API * Peso xG manuale
        const tiriH = (sH.shots.total.average || 12) * (parseFloat(mH.xG_Per_Shot)/0.11);
        const tiriA = (sA.shots.total.average || 10) * (parseFloat(mA.xG_Per_Shot)/0.11);
        const totTiri = tiriH + tiriA;

        // Corner: Totale medie API
        const totCorner = (sH.corners.for.average + sA.corners.for.average);

        // Cartellini: Media API corretta per i falli manuali
        const totCards = (sH.cards.yellow.average + sA.cards.yellow.average);
        
        // Falli: Media dei tuoi dati manuali
        const totFalli = parseFloat(mH.Falli_Fatti_Avg) + parseFloat(mA.Falli_Subiti_Avg);

        // Rendering Box
        resDiv.innerHTML = `
            ${renderBox("TIRI MATCH", totTiri, "l_tiri")}
            ${renderBox("CORNER MATCH", totCorner, "l_corner")}
            ${renderBox("CARTELLINI", totCards, "l_cards")}
            ${renderBox("FALLI TOTALI", totFalli, "l_falli")}
        `;

    } catch(e) { 
        resDiv.innerHTML = "<div class='col-span-full text-red-500 text-center'>ERRORE CONNESSIONE API</div>";
    }
}

function renderBox(title, val, lineId) {
    const line = parseFloat(document.getElementById(lineId).value);
    const diff = val - line;
    const isOver = diff > 0;
    const isSuper = Math.abs(diff) > 1.5;
    const colorClass = isSuper ? "val-high" : (Math.abs(diff) > 0.5 ? "val-med" : "");
    
    return `
        <div class="card-res ${colorClass}">
            <div class="text-[10px] font-bold text-slate-500 uppercase">${title}</div>
            <div class="text-4xl font-black teko">${val.toFixed(2)}</div>
            <div class="text-[10px] mt-2 font-bold ${isOver ? 'text-green-400' : 'text-red-400'}">
                PREVISIONE: ${isOver ? 'OVER' : 'UNDER'} ${line}
            </div>
        </div>
    `;
}

changeLeague(135);
</script>
</body>
</html>
"""
components.html(html_code, height=1000, scrolling=True)
