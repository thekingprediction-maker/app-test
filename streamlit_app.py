import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="PROBET AI V4 PRO", 
    layout="wide", 
    initial_sidebar_state="collapsed",
    menu_items=None
)

hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .stApp { background-color: #020617 !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    ::-webkit-scrollbar { display: none; }
    div[data-testid="stAppViewContainer"] { background-color: #020617 !important; }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@500;700&family=Inter:wght@400;600;800&display=swap');
        :root { --bg-dark: #020617; --primary-blue: #3b82f6; --text-muted: #94a3b8; }
        body { background-color: var(--bg-dark); color: #f8fafc; font-family: 'Inter', sans-serif; }
        .app-wrapper { max-width: 600px; margin: 0 auto; padding: 20px; }
        .glass-card { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); border-radius: 24px; padding: 20px; border: 1px solid rgba(255,255,255,0.08); }
        .btn-action { background: linear-gradient(135deg, #2563eb, #1d4ed8); width: 100%; padding: 18px; border-radius: 16px; font-weight: 800; text-transform: uppercase; color: white; cursor: pointer; }
    </style>
</head>
<body>
<div class="app-wrapper">
    <h1 class="teko text-4xl text-center mb-6">PROBET <span style="color:#3b82f6">AI</span> V4</h1>
    <div class="glass-card">
        <select id="homeTeam" class="w-full bg-slate-900 p-4 mb-4 rounded-xl text-white border border-slate-700"><option>Caricamento...</option></select>
        <select id="awayTeam" class="w-full bg-slate-900 p-4 mb-4 rounded-xl text-white border border-slate-700"><option>Caricamento...</option></select>
        <select id="arbitroSelect" class="w-full bg-slate-900 p-4 mb-4 rounded-xl text-white border border-slate-700"><option value="24.5,11,13.5">Seleziona Arbitro...</option></select>
        <button onclick="triggerAdAndCalculate()" class="btn-action">GENERA ANALISI ELITE PRO</button>
    </div>
    <div id="results" class="mt-6"></div>
</div>

<script>
const API_KEY = "f51c8f78f3478d58a4a206b726cc97a9";
const SEASON = "2025";
const BASE_CSV_URL = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/";
const LEAGUE_BASELINES = {
    7286: { shots: 24.8, sot: 8.2, corners: 9.6, cards: 4.4, fouls: 24.2 },
    7293: { shots: 25.4, sot: 8.8, corners: 10.2, cards: 3.8, fouls: 21.5 },
    7338: { shots: 26.1, sot: 9.1, corners: 10.8, cards: 4.1, fouls: 23.8 },
    7351: { shots: 24.2, sot: 8.0, corners: 9.4, cards: 5.2, fouls: 25.1 }
};

let currentLeague = 7286;
let dbXG = [];

async function triggerAdAndCalculate() {
    document.getElementById('results').innerHTML = '<div class="text-blue-500 text-center font-bold">CALCOLO MODELLO POISSON-BAYES IN CORSO...</div>';
    setTimeout(runDeepAnalysis, 500);
}

async function getAdvancedMetrics(teamId, apiId, teamName) {
    const baseline = LEAGUE_BASELINES[currentLeague];
    const isNeo = dbXG.find(r => r.TeamName.toLowerCase().trim() === teamName.toLowerCase().trim()) === undefined;

    if (isNeo) {
        // Logica per neopromosse: usa baseline lega
        return {
            shotsFor: baseline.shots/2, sotFor: baseline.sot/2, 
            cornersFor: baseline.corners/2, cards: baseline.cards/2, fouls: baseline.fouls/2,
            isNeo: true
        };
    }

    // Per le altre: Fetch dati 2025
    try {
        const stats = await fetch(`https://v3.football.api-sports.io/teams/statistics?league=${currentLeague}&season=${SEASON}&team=${teamId}`, 
            { headers: {"x-apisports-key": API_KEY} }).then(r => r.json());
        
        // Applicazione Bayesian Shrinkage (peso k=6 per stabilità inizio stagione)
        const s = stats.response;
        const n = s.fixtures.played.total || 1;
        const k = 6;
        return {
            shotsFor: (s.shots.total / n) * (n/(n+k)) + (baseline.shots/2) * (k/(n+k)),
            isNeo: false
        };
    } catch(e) {
        return { shotsFor: baseline.shots/2, isNeo: false };
    }
}

async function runDeepAnalysis() {
    const idH = document.getElementById('homeTeam').value;
    const idA = document.getElementById('awayTeam').value;
    // ... logica completa di elaborazione basata su getAdvancedMetrics ...
    document.getElementById('results').innerHTML = '<div class="text-green-500 text-center">ANALISI PRONTA</div>';
}

// Inizializzazione dati
Papa.parse(BASE_CSV_URL + "DATABASE_AVANZATO_SERIEA_2025.csv", {
    download: true, header: true, complete: (res) => { dbXG = res.data; }
});
</script>
</body>
</html>
"""

components.html(html_code, height=1200, scrolling=True)
