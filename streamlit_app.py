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
        select { background: #0f172a; border: 1px solid #475569; color: white; padding: 14px; width: 100%; border-radius: 12px; font-weight: bold; font-size: 14px; }
        .btn-analizza { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); width: 100%; padding: 20px; border-radius: 15px; font-weight: 900; text-transform: uppercase; cursor: pointer; transition: 0.3s; margin-top: 20px; border: none; color: white; }
        .res-box { background: #0f172a; border-radius: 20px; padding: 20px; border-left: 5px solid #3b82f6; position: relative; }
        .prob-badge { background: rgba(16, 185, 129, 0.2); color: #10b981; padding: 4px 10px; border-radius: 8px; font-size: 12px; font-weight: 900; float: right; border: 1px solid #10b981; }
        .label-spread { font-size: 10px; font-weight: 900; color: #94a3b8; text-transform: uppercase; margin-bottom: 5px; display: block; }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-4xl mx-auto">
        <div class="text-center mb-10">
            <h1 class="text-6xl font-black teko tracking-widest text-white uppercase italic">PROBET <span class="text-blue-500">AI V3</span></h1>
            <p class="text-[10px] font-bold text-slate-500 tracking-[0.5em] uppercase">Shots & On Target Logic • Spread Analysis</p>
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

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 pt-4 border-t border-slate-700">
                <div>
                    <label class="label-spread text-emerald-400">Spread Match Totali</label>
                    <select id="sprTotalMatch">
                        <option value="21.5">Over 21.5</option><option value="22.5">Over 22.5</option>
                        <option value="23.5" selected>Over 23.5</option><option value="24.5">Over 24.5</option>
                        <option value="25.5">Over 25.5</option>
                    </select>
                </div>
                <div>
                    <label class="label-spread text-emerald-400">Spread Casa Totali</label>
                    <select id="sprTotalH">
                        <option value="10.5">Over 10.5</option><option value="11.5">Over 11.5</option>
                        <option value="12.5" selected>Over 12.5</option><option value="13.5">Over 13.5</option>
                    </select>
                </div>
                <div>
                    <label class="label-spread text-emerald-400">Spread Ospite Totali</label>
                    <select id="sprTotalA">
                        <option value="8.5">Over 8.5</option><option value="9.5">Over 9.5</option>
                        <option value="10.5" selected>Over 10.5</option><option value="11.5">Over 11.5</option>
                    </select>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div>
                    <label class="label-spread text-purple-400">Spread Match In Porta</label>
                    <select id="sprOTMatch">
                        <option value="6.5">Over 6.5</option><option value="7.5">Over 7.5</option>
                        <option value="8.5" selected>Over 8.5</option><option value="9.5">Over 9.5</option>
                    </select>
                </div>
                <div>
                    <label class="label-spread text-purple-400">Spread Casa In Porta</label>
                    <select id="sprOTH">
                        <option value="3.5">Over 3.5</option><option value="4.5" selected>Over 4.5</option>
                        <option value="5.5">Over 5.5</option>
                    </select>
                </div>
                <div>
                    <label class="label-spread text-purple-400">Spread Ospite In Porta</label>
                    <select id="sprOTA">
                        <option value="2.5">Over 2.5</option><option value="3.5" selected>Over 3.5</option>
                        <option value="4.5">Over 4.5</option>
                    </select>
                </div>
            </div>

            <button onclick="runDeepAnalysis()" class="btn-analizza shadow-xl italic teko text-2xl tracking-widest">ANALIZZA TIRI E PROBABILITÀ</button>
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

// Calcolo probabilità basato su scarto (Shift di 8.5% per ogni unità di scarto dallo spread)
function calcProb(pred, spr) {
    let diff = pred - spr;
    let p = 50 + (diff * 8.5);
    return Math.min(Math.max(p, 5), 98).toFixed(1);
}

async function runDeepAnalysis() {
    const idH = document.getElementById('homeTeam').value, idA = document.getElementById('awayTeam').value;
    const resDiv = document.getElementById('results');
    resDiv.innerHTML = "<div class='text-center py-20 animate-pulse text-blue-500 font-black teko text-3xl uppercase tracking-widest'>Analyzing Spread Data...</div>";
    resDiv.classList.remove('hidden');

    try {
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
        ]);

        const xGH = parseFloat(dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || 0.11);
        const xGA = parseFloat(dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || 0.11);

        const shotsH = rH.response?.shots?.total?.average || 12.0;
        const shotsA = rA.response?.shots?.total?.average || 10.5;
        const otH = rH.response?.shots?.on_goal?.average || 4.0;
        const otA = rA.response?.shots?.on_goal?.average || 3.5;

        // Calcoli AI
        const cH = shotsH * (xGH / 0.11) * 1.05;
        const cA = shotsA * (xGA / 0.11);
        const totalM = cH + cA;

        const oH = otH * (xGH / 0.11) * 1.05;
        const oA = otA * (xGA / 0.11);
        const totalOTM = oH + oA;

        resDiv.innerHTML = `
            <div class="res-box border-l-blue-500">
                <span class="prob-badge">MATCH PROB: ${calcProb(totalM, document.getElementById('sprTotalMatch').value)}%</span>
                <p class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">Previsione Tiri Totali Match</p>
                <h2 class="text-6xl font-black teko text-white">${totalM.toFixed(2)}</h2>
                <div class="grid grid-cols-2 gap-4 mt-4 border-t border-slate-800 pt-4">
                    <div>
                        <p class="text-[10px] text-slate-400 font-bold uppercase">Casa (${document.getElementById('sprTotalH').value})</p>
                        <p class="text-xl font-bold teko text-blue-400">${cH.toFixed(2)} <span class="text-xs text-emerald-400 ml-2">${calcProb(cH, document.getElementById('sprTotalH').value)}%</span></p>
                    </div>
                    <div class="text-right">
                        <p class="text-[10px] text-slate-400 font-bold uppercase">Ospite (${document.getElementById('sprTotalA').value})</p>
                        <p class="text-xl font-bold teko text-blue-400">${cA.toFixed(2)} <span class="text-xs text-emerald-400 ml-2">${calcProb(cA, document.getElementById('sprTotalA').value)}%</span></p>
                    </div>
                </div>
            </div>

            <div class="res-box border-l-purple-500">
                <span class="prob-badge" style="color:#a855f7; border-color:#a855f7">MATCH PROB: ${calcProb(totalOTM, document.getElementById('sprOTMatch').value)}%</span>
                <p class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">Previsione Tiri In Porta Match</p>
                <h2 class="text-6xl font-black teko text-white">${totalOTM.toFixed(2)}</h2>
                <div class="grid grid-cols-2 gap-4 mt-4 border-t border-slate-800 pt-4">
                    <div>
                        <p class="text-[10px] text-slate-400 font-bold uppercase">Casa (${document.getElementById('sprOTH').value})</p>
                        <p class="text-xl font-bold teko text-purple-400">${oH.toFixed(2)} <span class="text-xs text-emerald-400 ml-2">${calcProb(oH, document.getElementById('sprOTH').value)}%</span></p>
                    </div>
                    <div class="text-right">
                        <p class="text-[10px] text-slate-400 font-bold uppercase">Ospite (${document.getElementById('sprOTA').value})</p>
                        <p class="text-xl font-bold teko text-purple-400">${oA.toFixed(2)} <span class="text-xs text-emerald-400 ml-2">${calcProb(oA, document.getElementById('sprOTA').value)}%</span></p>
                    </div>
                </div>
            </div>
        `;
    } catch(e) { console.error(e); }
}
</script>
</body>
</html>
"""
components.html(html_code, height=1100, scrolling=True)
