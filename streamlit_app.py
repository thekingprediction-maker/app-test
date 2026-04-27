import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI V3 - SPREAD ANALYSIS", layout="wide")

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
        select { background: #0f172a; border: 1px solid #475569; color: white; padding: 12px; width: 100%; border-radius: 10px; font-weight: bold; font-size: 13px; outline: none; }
        .btn-analizza { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); width: 100%; padding: 20px; border-radius: 15px; font-weight: 900; text-transform: uppercase; cursor: pointer; transition: 0.3s; margin-top: 20px; }
        .res-box { background: #0f172a; border-radius: 20px; padding: 20px; border-left: 5px solid #3b82f6; position: relative; }
        .prob-text { color: #10b981; font-weight: 900; font-size: 18px; }
        .label-spread { font-size: 10px; font-weight: 900; color: #94a3b8; text-transform: uppercase; margin-bottom: 5px; display: block; }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-5xl mx-auto">
        <div class="text-center mb-10">
            <h1 class="text-6xl font-black teko tracking-widest text-white uppercase italic">PROBET <span class="text-blue-500">AI V3</span></h1>
            <p class="text-[10px] font-bold text-slate-500 tracking-[0.5em] uppercase">Advanced Spread & Team Logic</p>
        </div>

        <div class="card-premium mb-8">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div><label class="label-spread text-blue-400">Home Team</label><select id="homeTeam"></select></div>
                <div><label class="label-spread text-blue-400">Away Team</label><select id="awayTeam"></select></div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 border-t border-slate-700 pt-6">
                <div class="space-y-3">
                    <p class="text-xs font-black text-center text-blue-400 uppercase">Spread Tiri Totali</p>
                    <label class="label-spread">Match</label>
                    <select id="sprTotalMatch">
                        <option value="22.5">Over 22.5</option><option value="23.5" selected>Over 23.5</option><option value="24.5">Over 24.5</option><option value="25.5">Over 25.5</option>
                    </select>
                    <div class="grid grid-cols-2 gap-2">
                        <div><label class="label-spread">Casa</label><select id="sprTotalH"><option value="11.5">Over 11.5</option><option value="12.5" selected>Over 12.5</option><option value="13.5">Over 13.5</option></select></div>
                        <div><label class="label-spread">Ospite</label><select id="sprTotalA"><option value="9.5">Over 9.5</option><option value="10.5" selected>Over 10.5</option><option value="11.5">Over 11.5</option></select></div>
                    </div>
                </div>

                <div class="space-y-3">
                    <p class="text-xs font-black text-center text-purple-400 uppercase">Spread In Porta</p>
                    <label class="label-spread">Match</label>
                    <select id="sprOTMatch">
                        <option value="7.5">Over 7.5</option><option value="8.5" selected>Over 8.5</option><option value="9.5">Over 9.5</option>
                    </select>
                    <div class="grid grid-cols-2 gap-2">
                        <div><label class="label-spread">Casa</label><select id="sprOTH"><option value="3.5">Over 3.5</option><option value="4.5" selected>Over 4.5</option><option value="5.5">Over 5.5</option></select></div>
                        <div><label class="label-spread">Ospite</label><select id="sprOTA"><option value="2.5">Over 2.5</option><option value="3.5" selected>Over 3.5</option><option value="4.5">Over 4.5</option></select></div>
                    </div>
                </div>

                <div class="flex items-end text-center">
                    <button onclick="runDeepAnalysis()" class="btn-analizza shadow-xl">Analizza Probabilità</button>
                </div>
            </div>
        </div>

        <div id="results" class="space-y-6 hidden pb-20"></div>
    </div>

<script>
const API_KEY = "aa5e53f893088010cc7c47af17f306e9";
const DB_URL = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/DATABASE_AVANZATO_2025.csv";

let dbXG = [];
Papa.parse(DB_URL, { download: true, header: true, skipEmptyLines: true, complete: function(r) { dbXG = r.data; loadTeams(); } });

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

function getProb(pred, spread) {
    let diff = pred - spread;
    let prob = 50 + (diff * 8); // Sensibilità 8% per tiro
    return Math.min(Math.max(prob, 5), 98).toFixed(1);
}

async function runDeepAnalysis() {
    const idH = document.getElementById('homeTeam').value, idA = document.getElementById('awayTeam').value;
    const resDiv = document.getElementById('results');
    resDiv.innerHTML = "<div class='text-center py-20 animate-pulse text-blue-500 font-black teko text-3xl uppercase tracking-widest'>Analyzing Spread Probability...</div>";
    resDiv.classList.remove('hidden');

    try {
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
        ]);

        const xGH = parseFloat(dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || 0.11), xGA = parseFloat(dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || 0.11);
        
        // Calcoli Tiri Totali
        const cH = (rH.response.shots.total.average || 12) * (xGH/0.11) * 1.05;
        const cA = (rA.response.shots.total.average || 10.5) * (xGA/0.11);
        const cM = cH + cA;

        // Calcoli In Porta
        const oH = (rH.response.shots.on_goal.average || 4) * (xGH/0.11) * 1.05;
        const oA = (rA.response.shots.on_goal.average || 3.5) * (xGA/0.11);
        const oM = oH + oA;

        resDiv.innerHTML = `
            <div class="res-box border-l-blue-500">
                <div class="flex justify-between items-center mb-4 border-b border-slate-800 pb-2">
                    <p class="text-2xl font-black teko uppercase tracking-widest text-blue-400">Tiri Totali Analysis</p>
                    <p class="prob-text">PROB MATCH: ${getProb(cM, document.getElementById('sprTotalMatch').value)}%</p>
                </div>
                <div class="grid grid-cols-3 gap-4 text-center">
                    <div><p class="label-spread">Match Prediction</p><p class="text-4xl font-black teko">${cM.toFixed(2)}</p></div>
                    <div><p class="label-spread">Casa (${document.getElementById('sprTotalH').value})</p><p class="text-2xl font-black teko text-blue-400">${cH.toFixed(2)}</p><p class="text-[10px] text-emerald-400 font-bold">${getProb(cH, document.getElementById('sprTotalH').value)}%</p></div>
                    <div><p class="label-spread">Ospite (${document.getElementById('sprTotalA').value})</p><p class="text-2xl font-black teko text-blue-400">${cA.toFixed(2)}</p><p class="text-[10px] text-emerald-400 font-bold">${getProb(cA, document.getElementById('sprTotalA').value)}%</p></div>
                </div>
            </div>

            <div class="res-box border-l-purple-500">
                <div class="flex justify-between items-center mb-4 border-b border-slate-800 pb-2">
                    <p class="text-2xl font-black teko uppercase tracking-widest text-purple-400">In Porta Analysis</p>
                    <p class="prob-text" style="color:#a855f7">PROB MATCH: ${getProb(oM, document.getElementById('sprOTMatch').value)}%</p>
                </div>
                <div class="grid grid-cols-3 gap-4 text-center">
                    <div><p class="label-spread">Match Prediction</p><p class="text-4xl font-black teko">${oM.toFixed(2)}</p></div>
                    <div><p class="label-spread">Casa (${document.getElementById('sprOTH').value})</p><p class="text-2xl font-black teko text-purple-400">${oH.toFixed(2)}</p><p class="text-[10px] text-emerald-400 font-bold">${getProb(oH, document.getElementById('sprOTH').value)}%</p></div>
                    <div><p class="label-spread">Ospite (${document.getElementById('sprOTA').value})</p><p class="text-2xl font-black teko text-purple-400">${oA.toFixed(2)}</p><p class="text-[10px] text-emerald-400 font-bold">${getProb(oA, document.getElementById('sprOTA').value)}%</p></div>
                </div>
            </div>
        `;
    } catch(e) { console.error(e); }
}
</script>
</body>
</html>
"""
components.html(html_code, height=1000, scrolling=True)
