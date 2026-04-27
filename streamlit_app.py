import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="PROBET AI - AUTOMATED V3", layout="wide")

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container { padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Teko:wght@600&display=swap');
        body { background: #020617; color: white; font-family: 'Inter', sans-serif; }
        .teko { font-family: 'Teko', sans-serif; }
        .card-main { background: #1e293b; border: 1px solid #334155; border-radius: 24px; padding: 30px; }
        select { background: #0f172a; border: 1px solid #475569; color: white; padding: 12px; width: 100%; border-radius: 12px; font-weight: bold; }
        .btn-analizza { background: #3b82f6; width: 100%; padding: 18px; border-radius: 15px; font-weight: 900; transition: 0.3s; text-transform: uppercase; }
        .btn-analizza:hover { background: #2563eb; transform: translateY(-2px); box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3); }
        .result-box { background: #0f172a; border-radius: 16px; padding: 20px; border-left: 5px solid #3b82f6; }
    </style>
</head>
<body class="p-4 md:p-10">
    <div class="max-w-2xl mx-auto">
        <div class="text-center mb-10">
            <h1 class="text-5xl font-black teko tracking-widest uppercase">PROBET <span class="text-blue-500">AI V3</span></h1>
            <p class="text-[10px] font-bold text-slate-500 tracking-[0.4em] uppercase">Advanced Prediction Engine</p>
        </div>

        <div class="card-main mb-8 shadow-2xl">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div>
                    <label class="text-[10px] font-bold text-blue-400 ml-2 mb-2 block uppercase">Squadra Casa</label>
                    <select id="homeTeam"></select>
                </div>
                <div>
                    <label class="text-[10px] font-bold text-blue-400 ml-2 mb-2 block uppercase">Squadra Ospite</label>
                    <select id="awayTeam"></select>
                </div>
            </div>
            <button onclick="runCalculation()" class="btn-analizza">Esegui Analisi API + xG</button>
        </div>

        <div id="results" class="space-y-4 hidden pb-20"></div>
    </div>

<script>
const API_KEY = "aa5e53f893088010cc7c47af17f306e9";
// LINK RAW CORRETTO PER EVITARE ERRORE 404
const DB_URL = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/DATABASE_AVANZATO_2025.csv";

let dbStats = [];

// Caricamento del database xG da GitHub
Papa.parse(DB_URL, {
    download: true,
    header: true,
    skipEmptyLines: true,
    complete: function(results) {
        dbStats = results.data;
        console.log("Database xG Caricato. Squadre:", dbStats.length);
        loadTeams();
    }
});

async function loadTeams() {
    try {
        const res = await fetch("https://v3.football.api-sports.io/teams?league=135&season=2024", {
            headers: { "x-apisports-key": API_KEY }
        });
        const data = await res.json();
        const h = document.getElementById('homeTeam');
        const a = document.getElementById('awayTeam');
        
        data.response.sort((x,y) => x.team.name.localeCompare(y.team.name)).forEach(t => {
            // Aggiungiamo solo se presente nel tuo CSV per evitare Serie B
            const exists = dbStats.some(s => s.TeamID == t.team.id);
            if(exists) {
                h.add(new Option(t.team.name, t.team.id));
                a.add(new Option(t.team.name, t.team.id));
            }
        });
    } catch(e) { console.error("Errore API Teams:", e); }
}

async function runCalculation() {
    const idH = document.getElementById('homeTeam').value;
    const idA = document.getElementById('awayTeam').value;
    const resDiv = document.getElementById('results');
    
    resDiv.innerHTML = "<div class='text-center py-10 animate-pulse text-blue-400 font-bold'>ELABORAZIONE...</div>";
    resDiv.classList.remove('hidden');

    try {
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2024&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2024&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
        ]);

        // Recupero xG dal database manuale
        const csvH = dbStats.find(x => x.TeamID == idH) || { xG_Per_Shot: 0.11 };
        const csvA = dbStats.find(x => x.TeamID == idA) || { xG_Per_Shot: 0.11 };

        const xGH = parseFloat(csvH.xG_Per_Shot);
        const xGA = parseFloat(csvA.xG_Per_Shot);

        // Calcolo Tiri con protezione undefined
        const tH = rH.response?.shots?.total?.average || 12;
        const tA = rA.response?.shots?.total?.average || 10;

        const finaleTiri = (tH * (xGH / 0.11)) + (tA * (xGA / 0.11));

        resDiv.innerHTML = `
            <div class="result-box">
                <p class="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Previsione Tiri Totali</p>
                <h2 class="text-5xl font-black teko">${finaleTiri.toFixed(2)}</h2>
                <p class="text-[9px] text-blue-400 mt-2 font-bold uppercase">Correttore xG: ${xGH} (Casa) / ${xGA} (Ospite)</p>
            </div>
            <div class="grid grid-cols-2 gap-4">
                <div class="result-box border-l-emerald-500">
                    <p class="text-[10px] font-bold text-slate-500 uppercase">Corner Media</p>
                    <p class="text-3xl font-bold teko">${((rH.response?.corners?.for?.average || 5) + (rA.response?.corners?.for?.average || 4)).toFixed(2)}</p>
                </div>
                <div class="result-box border-l-amber-500">
                    <p class="text-[10px] font-bold text-slate-500 uppercase">Cartellini Media</p>
                    <p class="text-3xl font-bold teko">${((rH.response?.cards?.yellow?.average || 2.2) + (rA.response?.cards?.yellow?.average || 2.1)).toFixed(2)}</p>
                </div>
            </div>
        `;

    } catch(e) {
        resDiv.innerHTML = `<div class='p-4 bg-red-500/20 text-red-400 rounded-xl text-center font-bold'>ERRORE DATI: ${e.message}</div>`;
    }
}
</script>
</body>
</html>
"""
components.html(html_code, height=900, scrolling=True)
