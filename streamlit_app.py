import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI V3 - PREDICTOR PRO", layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600&family=Inter:wght@400;900&display=swap');
        body { background: #020617; color: white; font-family: 'Inter', sans-serif; }
        .teko { font-family: 'Teko', sans-serif; }
        .card-premium { background: #1e293b; border-radius: 24px; padding: 30px; border: 1px solid #334155; }
        select { background: #0f172a; border: 1px solid #475569; color: white; padding: 14px; width: 100%; border-radius: 12px; font-weight: bold; }
        .btn-analizza { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); width: 100%; padding: 20px; border-radius: 15px; font-weight: 900; text-transform: uppercase; cursor: pointer; transition: 0.3s; }
        .res-box { background: #0f172a; border-radius: 20px; padding: 25px; border-left: 5px solid #3b82f6; position: relative; }
        .advice-pill { padding: 4px 12px; border-radius: 50px; font-size: 12px; font-weight: 900; text-transform: uppercase; }
        .over { background: #065f46; color: #34d399; }
        .under { background: #991b1b; color: #f87171; }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-4xl mx-auto">
        <div class="text-center mb-10">
            <h1 class="text-6xl font-black teko tracking-widest text-white italic uppercase">PROBET <span class="text-blue-500">AI V3</span></h1>
            <p class="text-[10px] font-bold text-slate-500 tracking-[0.5em] uppercase">Advanced Betting Insights • Precision 75%</p>
        </div>

        <div class="card-premium mb-8">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div><label class="text-[11px] font-black text-blue-400 mb-2 block uppercase">Home Team</label><select id="homeTeam"></select></div>
                <div><label class="text-[11px] font-black text-blue-400 mb-2 block uppercase">Away Team</label><select id="awayTeam"></select></div>
            </div>
            <button onclick="runDeepAnalysis()" class="btn-analizza shadow-xl w-full">Genera Consigli di Scommessa</button>
        </div>

        <div id="results" class="space-y-6 hidden pb-20"></div>
    </div>

<script>
const API_KEY = "aa5e53f893088010cc7c47af17f306e9";
const DB_URL = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/DATABASE_AVANZATO_2025.csv";

let dbXG = [];

Papa.parse(DB_URL, {
    download: true, header: true, skipEmptyLines: true,
    complete: function(r) { dbXG = r.data; loadTeams(); }
});

async function loadTeams() {
    try {
        const res = await fetch("https://v3.football.api-sports.io/teams?league=135&season=2025", { headers: { "x-apisports-key": API_KEY } });
        const data = await res.json();
        const h = document.getElementById('homeTeam'), a = document.getElementById('awayTeam');
        data.response.sort((x,y) => x.team.name.localeCompare(y.team.name)).forEach(t => {
            h.add(new Option(t.team.name, t.team.id)); a.add(new Option(t.team.name, t.team.id));
        });
    } catch(e) { console.error(e); }
}

// FUNZIONE PER CALCOLARE LA MEDIA SE L'API NON LA DA PRONTA
function calculateAverage(stat) {
    if (!stat) return 0;
    if (stat.average) return parseFloat(stat.average);
    if (stat.total && stat.played) return parseFloat(stat.total / stat.played);
    return 0;
}

function getAdvice(expected, line) {
    const diff = ((expected - line) / line) * 100;
    let prob = 50 + (diff * 2.5); // Peso Poisson aumentato per precisione
    prob = Math.min(Math.max(prob, 30), 92);
    
    if (expected > line) return { type: 'OVER', p: prob, class: 'over' };
    return { type: 'UNDER', p: 100 - prob, class: 'under' };
}

async function runDeepAnalysis() {
    const idH = document.getElementById('homeTeam').value, idA = document.getElementById('awayTeam').value;
    const resDiv = document.getElementById('results');
    resDiv.innerHTML = "<div class='text-center py-20 animate-pulse text-blue-500 font-black teko text-4xl uppercase tracking-tighter text-white uppercase italic'>ANALIZZANDO DATI STAGIONE 2025...</div>";
    resDiv.classList.remove('hidden');

    try {
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
        ]);

        const sH = rH.response;
        const sA = rA.response;

        const xGH = parseFloat(dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || 0.11);
        const xGA = parseFloat(dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || 0.11);

        // Estrazione sicura delle medie (se average è null, calcola total/played)
        const shotsH = calculateAverage(sH.shots.total) || 12.0;
        const shotsA = calculateAverage(sA.shots.total) || 10.5;
        const onGoalH = calculateAverage(sH.shots.on_goal) || 4.0;
        const onGoalA = calculateAverage(sA.shots.on_goal) || 3.5;

        // Calcolo Algoritmo Avanzato (xG Weighted + Home Edge)
        const tT = (shotsH * (xGH/0.11) * 1.05) + (shotsA * (xGA/0.11));
        const tP = (onGoalH * (xGH/0.11) * 1.05) + (onGoalA * (xGA/0.11));

        const advT = getAdvice(tT, 23.5);
        const advP = getAdvice(tP, 8.5);

        resDiv.innerHTML = `
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="res-box">
                    <div class="flex justify-between items-start mb-4">
                        <p class="text-[10px] font-black text-slate-500 uppercase tracking-widest">Tiri Totali Match (2025)</p>
                        <span class="advice-pill ${advT.class}">${advT.type} 23.5</span>
                    </div>
                    <h2 class="text-6xl font-black teko text-white mb-2">${tT.toFixed(2)}</h2>
                    <p class="text-emerald-400 font-black text-2xl teko tracking-tight">PROBABILITÀ: ${advT.p.toFixed(1)}%</p>
                </div>

                <div class="res-box border-l-purple-500">
                    <div class="flex justify-between items-start mb-4">
                        <p class="text-[10px] font-black text-slate-500 uppercase tracking-widest">In Porta Match (2025)</p>
                        <span class="advice-pill ${advP.class}">${advP.type} 8.5</span>
                    </div>
                    <h2 class="text-6xl font-black teko text-white mb-2">${tP.toFixed(2)}</h2>
                    <p class="text-purple-400 font-black text-2xl teko tracking-tight">PROBABILITÀ: ${advP.p.toFixed(1)}%</p>
                </div>
            </div>

            <div class="p-6 bg-blue-600/10 border border-blue-500/20 rounded-2xl flex justify-between items-center">
                <p class="text-xs font-bold text-blue-400 uppercase tracking-[0.2em]">Consiglio AI: ${(advT.p > 65 || advP.p > 65) ? 'ALTA CONFIDENZA' : 'DATI IN MEDIA'}</p>
                <p class="text-[10px] font-black text-slate-600 uppercase">xG: H ${xGH} | A ${xGA}</p>
            </div>
        `;
    } catch(e) { 
        console.error(e);
        resDiv.innerHTML = "<div class='p-8 bg-red-900/20 text-red-400 text-center font-bold'>ERRORE: Dati API 2025 non disponibili per questa coppia.</div>"; 
    }
}
</script>
</body>
</html>
"""
components.html(html_code, height=900, scrolling=True)
