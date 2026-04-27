import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ProBet AI - Live API", layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>
        body { background: #0f172a; color: white; font-family: sans-serif; }
        .card { background: #1e293b; border-radius: 15px; padding: 20px; margin-bottom: 20px; border: 1px solid #334155; }
        select, input { background: #0f172a; border: 1px solid #334155; color: white; padding: 10px; border-radius: 8px; width: 100%; }
        .btn-analizza { background: #3b82f6; width: 100%; padding: 15px; border-radius: 10px; font-weight: bold; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="p-4 max-w-4xl mx-auto">
        <h1 class="text-2xl font-black mb-4 text-blue-500">PROBET AI v3 - AUTOMATED</h1>
        
        <div class="card">
            <div class="grid grid-cols-2 gap-4 mb-4">
                <button onclick="loadLeague(135)" class="bg-slate-700 p-2 rounded">SERIE A</button>
                <button onclick="loadLeague(39)" class="bg-slate-700 p-2 rounded">PREMIER</button>
                <button onclick="loadLeague(140)" class="bg-slate-700 p-2 rounded">LIGA</button>
                <button onclick="loadLeague(78)" class="bg-slate-700 p-2 rounded">BUNDES</button>
            </div>
            
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="text-xs text-slate-400">CASA</label>
                    <select id="homeTeam"></select>
                </div>
                <div>
                    <label class="text-xs text-slate-400">OSPITE</label>
                    <select id="awayTeam"></select>
                </div>
            </div>
            <button class="btn-analizza" onclick="startAnalysis()">ANALIZZA DATI API</button>
        </div>

        <div id="results" class="hidden space-y-4"></div>
    </div>

<script>
const API_KEY = "aa5e53f893088010cc7c47af17f306e9";
const GITHUB_CSV = "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/DATABASE_AVANZATO_2025.csv";

let manualData = [];

// Carica i dati manuali (Falli e xG) da GitHub all'avvio
Papa.parse(GITHUB_CSV, {
    download: true,
    header: true,
    complete: function(results) {
        manualData = results.data;
        console.log("Dati manuali GitHub caricati:", manualData);
    }
});

async function loadLeague(leagueId) {
    const res = await fetch(`https://v3.football.api-sports.io/teams?league=${leagueId}&season=2024`, {
        headers: { "x-apisports-key": API_KEY }
    });
    const data = await res.json();
    const teams = data.response;
    
    const h = document.getElementById('homeTeam');
    const a = document.getElementById('awayTeam');
    h.innerHTML = a.innerHTML = "";
    
    // Ordina e popola i select
    teams.sort((x,y) => x.team.name.localeCompare(y.team.name)).forEach(t => {
        h.add(new Option(t.team.name, t.team.id));
        a.add(new Option(t.team.name, t.team.id));
    });
    
    console.log("SQUADRE AGGIORNATE ID:", teams.map(t => `${t.team.id}: ${t.team.name}`));
}

async function startAnalysis() {
    const idH = document.getElementById('homeTeam').value;
    const idA = document.getElementById('awayTeam').value;
    
    // 1. Prendi statistiche reali da API
    const [sH, sA] = await Promise.all([
        fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2024&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
        fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2024&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
    ]);

    // 2. Cerca i correttori xG e Falli nel tuo CSV di GitHub
    const mH = manualData.find(r => r.TeamID == idH) || { xG_Per_Shot: 0.10, Falli_Avg: 12 };
    const mA = manualData.find(r => r.TeamID == idA) || { xG_Per_Shot: 0.10, Falli_Avg: 12 };

    // 3. Calcolo (Esempio Tiri)
    const avgTiriH = sH.response.shots.total.average || 10;
    const avgTiriA = sA.response.shots.total.average || 10;
    const finaleTiri = (avgTiriH + avgTiriA).toFixed(2);

    document.getElementById('results').classList.remove('hidden');
    document.getElementById('results').innerHTML = `
        <div class="card border-l-4 border-blue-500">
            <h3 class="text-blue-400 font-bold">PREVISIONE TIRI (API + xG Weight)</h3>
            <div class="text-4xl font-black">${finaleTiri}</div>
            <p class="text-xs text-slate-400 mt-2">Peso Qualità (xG/Shot): Casa ${mH.xG_Per_Shot} | Ospite ${mA.xG_Per_Shot}</p>
        </div>
    `;
}

loadLeague(135); // Parte con Serie A
</script>
</body>
</html>
"""
components.html(html_code, height=900, scrolling=True)
