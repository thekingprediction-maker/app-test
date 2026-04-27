import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI V3 - TOTAL & ON TARGET", layout="wide")

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
        .res-box { background: #0f172a; border-radius: 20px; padding: 20px; border-left: 5px solid #3b82f6; }
        .stat-grid { display: grid; grid-template-cols: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-4xl mx-auto">
        <div class="text-center mb-10">
            <h1 class="text-6xl font-black teko tracking-widest text-white uppercase italic">PROBET <span class="text-blue-500">AI V3</span></h1>
            <p class="text-[10px] font-bold text-slate-500 tracking-[0.5em] uppercase">Shots & On Target Logic • 75% Precision</p>
        </div>

        <div class="card-premium mb-8">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div>
                    <label class="text-[11px] font-black text-blue-400 mb-2 block uppercase">Home Team</label>
                    <select id="homeTeam"></select>
                </div>
                <div>
                    <label class="text-[11px] font-black text-blue-400 mb-2 block uppercase">Away Team</label>
                    <select id="awayTeam"></select>
                </div>
            </div>
            <button onclick="runDeepAnalysis()" class="btn-analizza shadow-xl">Analizza Tiri e Precisione</button>
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
        const res = await fetch("https://v3.football.api-sports.io/teams?league=135&season=2025", {
            headers: { "x-apisports-key": API_KEY }
        });
        const data = await res.json();
        const h = document.getElementById('homeTeam');
        const a = document.getElementById('awayTeam');
        data.response.sort((x,y) => x.team.name.localeCompare(y.team.name)).forEach(t => {
            h.add(new Option(t.team.name, t.team.id));
            a.add(new Option(t.team.name, t.team.id));
        });
    } catch(e) { console.error(e); }
}

async function runDeepAnalysis() {
    const idH = document.getElementById('homeTeam').value;
    const idA = document.getElementById('awayTeam').value;
    const resDiv = document.getElementById('results');
    resDiv.innerHTML = "<div class='text-center py-20 animate-pulse text-blue-500 font-black teko text-3xl uppercase tracking-widest'>Analyzing Shot Quality...</div>";
    resDiv.classList.remove('hidden');

    try {
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
        ]);

        // DATI XG DAL TUO CSV
        const xGH = parseFloat(dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || 0.11);
        const xGA = parseFloat(dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || 0.11);

        // MEDIE API 2025
        const shotsH = rH.response?.shots?.total?.average || 12.0;
        const shotsA = rA.response?.shots?.total?.average || 10.5;
        const otH = rH.response?.shots?.on_goal?.average || 4.0;
        const otA = rA.response?.shots?.on_goal?.average || 3.5;

        // CALCOLO TIRI TOTALI (Pesati con xG e Home Edge 5%)
        const calcTotalH = shotsH * (xGH / 0.11) * 1.05;
        const calcTotalA = shotsA * (xGA / 0.11);
        const totalMatch = calcTotalH + calcTotalA;

        // CALCOLO TIRI IN PORTA (Pesati con xG e Precisione Storica)
        const calcOTH = otH * (xGH / 0.11) * 1.05;
        const calcOTA = otA * (xGA / 0.11);
        const totalOTMatch = calcOTH + calcOTA;

        resDiv.innerHTML = `
            <div class="res-box border-l-blue-500">
                <p class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">Previsione Tiri Totali Match</p>
                <h2 class="text-6xl font-black teko text-white">${totalMatch.toFixed(2)}</h2>
                <div class="grid grid-cols-2 gap-4 mt-4 border-t border-slate-800 pt-4">
                    <div><p class="text-[10px] text-slate-400 font-bold uppercase">Casa Totali</p><p class="text-xl font-bold teko text-blue-400">${calcTotalH.toFixed(2)}</p></div>
                    <div class="text-right"><p class="text-[10px] text-slate-400 font-bold uppercase">Ospite Totali</p><p class="text-xl font-bold teko text-blue-400">${calcTotalA.toFixed(2)}</p></div>
                </div>
            </div>

            <div class="res-box border-l-purple-500">
                <p class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">Previsione Tiri In Porta Match</p>
                <h2 class="text-6xl font-black teko text-white">${totalOTMatch.toFixed(2)}</h2>
                <div class="grid grid-cols-2 gap-4 mt-4 border-t border-slate-800 pt-4">
                    <div><p class="text-[10px] text-slate-400 font-bold uppercase">Casa In Porta</p><p class="text-xl font-bold teko text-purple-400">${calcOTH.toFixed(2)}</p></div>
                    <div class="text-right"><p class="text-[10px] text-slate-400 font-bold uppercase">Ospite In Porta</p><p class="text-xl font-bold teko text-purple-400">${calcOTA.toFixed(2)}</p></div>
                </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
                <div class="res-box border-l-emerald-500">
                    <p class="text-[10px] font-bold text-slate-500 uppercase">Angoli Previsti</p>
                    <p class="text-3xl font-black teko text-white">${((rH.response?.corners?.for?.average || 5) + (rA.response?.corners?.for?.average || 4.5)).toFixed(2)}</p>
                </div>
                <div class="res-box border-l-amber-500">
                    <p class="text-[10px] font-bold text-slate-500 uppercase">Cartellini Previsti</p>
                    <p class="text-3xl font-black teko text-white">${((rH.response?.cards?.yellow?.average || 2.2) + (rA.response?.cards?.yellow?.average || 2.2)).toFixed(2)}</p>
                </div>
            </div>
        `;
    } catch(e) { console.error(e); }
}
</script>
</body>
</html>
"""
components.html(html_code, height=900, scrolling=True)
