import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI V4 - ULTRA STABLE", layout="wide")

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
        select, input { background: #0f172a; border: 1px solid #475569; color: white; padding: 12px; width: 100%; border-radius: 12px; font-weight: bold; outline: none; }
        .btn-analizza { background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); width: 100%; padding: 20px; border-radius: 15px; font-weight: 900; text-transform: uppercase; cursor: pointer; border: none; color: white; transition: 0.3s; }
        .res-box { background: #0f172a; border-radius: 20px; padding: 25px; border-left: 5px solid #3b82f6; margin-bottom: 20px; }
        .advice-tag { display: inline-block; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 900; margin-left: 10px; }
        .over-tag { background: #10b981; color: #020617; }
        .under-tag { background: #ef4444; color: white; }
        .league-btn { cursor: pointer; padding: 12px; border-radius: 10px; font-weight: 900; border: 1px solid #334155; text-align: center; background: #1e293b; font-size: 11px; }
        .league-active { background: #3b82f6; border-color: #60a5fa; }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-5xl mx-auto">
        <div class="text-center mb-10">
            <h1 class="text-6xl font-black teko tracking-widest uppercase italic">PROBET <span class="text-blue-500">AI V4</span></h1>
            <p class="text-[10px] font-bold text-slate-500 tracking-[0.4em] uppercase">Advanced Prediction Engine • Ultra Precision</p>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div id="btn-135" class="league-btn league-active" onclick="switchLeague(135)">SERIE A</div>
            <div id="btn-39" class="league-btn" onclick="switchLeague(39)">PREMIER LEAGUE</div>
            <div id="btn-78" class="league-btn" onclick="switchLeague(78)">BUNDESLIGA</div>
            <div id="btn-140" class="league-btn" onclick="switchLeague(140)">LA LIGA</div>
        </div>

        <div class="card-premium">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div><label class="text-[10px] font-bold text-blue-400 uppercase mb-1 block">Home Team</label><select id="homeTeam"></select></div>
                <div><label class="text-[10px] font-bold text-blue-400 uppercase mb-1 block">Away Team</label><select id="awayTeam"></select></div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 border-t border-slate-700 pt-6 mb-6">
                <div><label class="text-[10px] font-bold text-emerald-400 uppercase">Spread Match Totali</label><input type="number" id="sTM" step="0.5" value="24.5"></div>
                <div><label class="text-[10px] font-bold text-emerald-400 uppercase">Spread Casa</label><input type="number" id="sTH" step="0.5" value="13.5"></div>
                <div><label class="text-[10px] font-bold text-emerald-400 uppercase">Spread Ospite</label><input type="number" id="sTA" step="0.5" value="10.5"></div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div><label class="text-[10px] font-bold text-purple-400 uppercase">Spread Match In Porta</label><input type="number" id="sOM" step="0.5" value="8.5"></div>
                <div><label class="text-[10px] font-bold text-purple-400 uppercase">Spread Casa Porta</label><input type="number" id="sOH" step="0.5" value="4.5"></div>
                <div><label class="text-[10px] font-bold text-purple-400 uppercase">Spread Ospite Porta</label><input type="number" id="sOA" step="0.5" value="3.5"></div>
            </div>

            <button onclick="runAnalysis()" class="btn-analizza teko text-2xl tracking-widest">GENERA ANALISI ELITE</button>
        </div>

        <div id="results" class="mt-8 space-y-6 hidden pb-20"></div>
    </div>

<script>
const API_KEY = "aa5e53f893088010cc7c47af17f306e9";
const BASE_CSV = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/";
let currentL = 135; let dbXG = [];

const leagueFiles = { 135: "DATABASE_AVANZATO_SERIEA_2025.csv", 39: "DATABASE_AVANZATO_PREMIER_2025.csv", 78: "DATABASE_AVANZATO_BUNDES_2025.csv", 140: "DATABASE_AVANZATO_LALIGA_2025.csv" };

function switchLeague(id) {
    currentL = id;
    document.querySelectorAll('.league-btn').forEach(b => b.classList.remove('league-active'));
    document.getElementById('btn-'+id).classList.add('league-active');
    loadData();
}

function loadData() {
    Papa.parse(BASE_CSV + leagueFiles[currentL], { download: true, header: true, skipEmptyLines: true, complete: function(r) { dbXG = r.data; loadTeams(); } });
}

async function loadTeams() {
    const r = await fetch(`https://v3.football.api-sports.io/teams?league=${currentL}&season=2025`, {headers:{"x-apisports-key":API_KEY}});
    const d = await r.json();
    const h = document.getElementById('homeTeam'), a = document.getElementById('awayTeam');
    h.innerHTML = ""; a.innerHTML = "";
    d.response.sort((x,y)=>x.team.name.localeCompare(y.team.name)).forEach(t => {
        h.add(new Option(t.team.name, t.team.id)); a.add(new Option(t.team.name, t.team.id));
    });
}

function getAdvice(pred, spr) {
    let diff = pred - spr;
    let p = 50 + (diff * 9.2); 
    p = Math.min(Math.max(p, 5), 98);
    const label = p >= 50 ? "OVER" : "UNDER";
    const css = p >= 50 ? "over-tag" : "under-tag";
    const prob = p >= 50 ? p : (100 - p);
    return `<span class="advice-tag ${css}">${label} ${spr} (${prob.toFixed(1)}%)</span>`;
}

async function runAnalysis() {
    const idH = document.getElementById('homeTeam').value, idA = document.getElementById('awayTeam').value;
    const resDiv = document.getElementById('results');
    resDiv.innerHTML = "<div class='text-center py-10 teko text-4xl animate-pulse text-blue-500'>CALCOLANDO DATI ELITE...</div>";
    resDiv.classList.remove('hidden');

    try {
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${currentL}&season=2025&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${currentL}&season=2025&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
        ]);

        const xGH = parseFloat(dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || 0.11);
        const xGA = parseFloat(dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || 0.11);
        const bench = (currentL === 39 || currentL === 78) ? 0.12 : 0.11;

        // TIRI TOTALI
        const avgH = rH.response.shots.total.average || 12.0;
        const avgA = rA.response.shots.total.average || 10.0;
        const predH = ((avgH + 11.5) / 2) * (xGH / bench) * 1.05;
        const predA = ((avgA + 12.0) / 2) * (xGA / bench);
        const total = predH + predA;

        // TIRI IN PORTA
        const onH = rH.response.shots.on_goal.average || 4.0;
        const onA = rA.response.shots.on_goal.average || 3.5;
        const predOnH = ((onH + 3.8) / 2) * (xGH / bench) * 1.05;
        const predOnA = ((onA + 4.1) / 2) * (xGA / bench);
        const totalOn = predOnH + predOnA;

        resDiv.innerHTML = `
            <div class="res-box border-l-blue-500">
                <p class="text-[10px] font-bold text-slate-400 uppercase">Previsione Tiri Totali (Defense-Adjusted)</p>
                <h2 class="text-7xl font-black teko">${total.toFixed(2)} ${getAdvice(total, document.getElementById('sTM').value)}</h2>
                <div class="grid grid-cols-2 mt-4 pt-4 border-t border-slate-800">
                    <div><p class="text-[10px] text-slate-500 uppercase">Casa: ${predH.toFixed(2)}</p>${getAdvice(predH, document.getElementById('sTH').value)}</div>
                    <div class="text-right"><p class="text-[10px] text-slate-500 uppercase">Ospite: ${predA.toFixed(2)}</p>${getAdvice(predA, document.getElementById('sTA').value)}</div>
                </div>
            </div>

            <div class="res-box border-l-purple-500">
                <p class="text-[10px] font-bold text-slate-400 uppercase">Previsione Tiri In Porta (Quality-Adjusted)</p>
                <h2 class="text-7xl font-black teko">${totalOn.toFixed(2)} ${getAdvice(totalOn, document.getElementById('sOM').value)}</h2>
                <div class="grid grid-cols-2 mt-4 pt-4 border-t border-slate-800">
                    <div><p class="text-[10px] text-slate-500 uppercase">Casa: ${predOnH.toFixed(2)}</p>${getAdvice(predOnH, document.getElementById('sOH').value)}</div>
                    <div class="text-right"><p class="text-[10px] text-slate-500 uppercase">Ospite: ${predOnA.toFixed(2)}</p>${getAdvice(predOnA, document.getElementById('sOA').value)}</div>
                </div>
            </div>
        `;
    } catch(e) { resDiv.innerHTML = "<div class='text-red-500 p-10'>ERRORE API: Verifica la connessione o i dati squadra.</div>"; }
}
switchLeague(135);
</script>
</body>
</html>
"""
components.html(html_code, height=1200, scrolling=True)
