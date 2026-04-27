import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI V3 - SMART ADVICE", layout="wide")

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
        .prob-badge { background: rgba(16, 185, 129, 0.15); color: #10b981; padding: 4px 10px; border-radius: 8px; font-size: 12px; font-weight: 900; float: right; border: 1px solid #10b981; }
        .advice-badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 900; text-transform: uppercase; margin-left: 10px; }
        .over-style { background: #10b981; color: #020617; }
        .under-style { background: #ef4444; color: white; }
        .label-spread { font-size: 10px; font-weight: 900; color: #94a3b8; text-transform: uppercase; margin-bottom: 5px; display: block; }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-4xl mx-auto">
        <div class="text-center mb-10">
            <h1 class="text-6xl font-black teko tracking-widest text-white uppercase italic">PROBET <span class="text-blue-500">AI V3</span></h1>
            <p class="text-[10px] font-bold text-slate-500 tracking-[0.5em] uppercase">Shots & On Target • Smart Advice Logic</p>
        </div>

        <div class="card-premium mb-8">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div><label class="label-spread text-blue-400">Home Team</label><select id="homeTeam"></select></div>
                <div><label class="label-spread text-blue-400">Away Team</label><select id="awayTeam"></select></div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 pt-4 border-t border-slate-700">
                <div><label class="label-spread text-emerald-400">Spread Match Totali</label><select id="sprTotalMatch"><option value="22.5">Over 22.5</option><option value="23.5" selected>Over 23.5</option><option value="24.5">Over 24.5</option></select></div>
                <div><label class="label-spread text-emerald-400">Spread Casa Totali</label><select id="sprTotalH"><option value="11.5">Over 11.5</option><option value="12.5" selected>Over 12.5</option><option value="13.5">Over 13.5</option></select></div>
                <div><label class="label-spread text-emerald-400">Spread Ospite Totali</label><select id="sprTotalA"><option value="9.5">Over 9.5</option><option value="10.5" selected>Over 10.5</option><option value="11.5">Over 11.5</option></select></div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div><label class="label-spread text-purple-400">Spread Match In Porta</label><select id="sprOTMatch"><option value="7.5">Over 7.5</option><option value="8.5" selected>Over 8.5</option><option value="9.5">Over 9.5</option></select></div>
                <div><label class="label-spread text-purple-400">Spread Casa In Porta</label><select id="sprOTH"><option value="3.5">Over 3.5</option><option value="4.5" selected>Over 4.5</option><option value="5.5">Over 5.5</option></select></div>
                <div><label class="label-spread text-purple-400">Spread Ospite In Porta</label><select id="sprOTA"><option value="2.5">Over 2.5</option><option value="3.5" selected>Over 3.5</option><option value="4.5">Over 4.5</option></select></div>
            </div>

            <button onclick="runDeepAnalysis()" class="btn-analizza shadow-xl italic teko text-2xl tracking-widest">CALCOLA CONSIGLIO AI</button>
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

function getAdvice(pred, spr) {
    const isOver = pred >= spr;
    const diff = Math.abs(pred - spr);
    let prob = 50 + ( (pred - spr) * 9); 
    prob = Math.min(Math.max(prob, 5), 98).toFixed(1);
    const badgeClass = isOver ? 'over-style' : 'under-style';
    const label = isOver ? 'OVER' : 'UNDER';
    return { label, badgeClass, prob };
}

async function runDeepAnalysis() {
    const idH = document.getElementById('homeTeam').value, idA = document.getElementById('awayTeam').value;
    const resDiv = document.getElementById('results');
    resDiv.innerHTML = "<div class='text-center py-20 animate-pulse text-blue-500 font-black teko text-3xl uppercase tracking-widest'>Generating Advice...</div>";
    resDiv.classList.remove('hidden');

    try {
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
        ]);

        const xGH = parseFloat(dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || 0.11), xGA = parseFloat(dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || 0.11);
        const cH = (rH.response.shots.total.average || 12) * (xGH/0.11) * 1.05, cA = (rA.response.shots.total.average || 10.5) * (xGA/0.11);
        const totalM = cH + cA;
        const oH = (rH.response.shots.on_goal.average || 4) * (xGH/0.11) * 1.05, oA = (rA.response.shots.on_goal.average || 3.5) * (xGA/0.11);
        const totalOTM = oH + oA;

        const advM = getAdvice(totalM, document.getElementById('sprTotalMatch').value);
        const advOTM = getAdvice(totalOTM, document.getElementById('sprOTMatch').value);

        resDiv.innerHTML = `
            <div class="res-box border-l-blue-500">
                <span class="prob-badge">WIN PROB: ${advM.prob}%</span>
                <p class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">Tiri Totali: Previsione vs Spread</p>
                <h2 class="text-6xl font-black teko text-white inline-block">${totalM.toFixed(2)}</h2>
                <span class="advice-badge ${advM.badgeClass}">${advM.label} ${document.getElementById('sprTotalMatch').value}</span>
                <div class="grid grid-cols-2 gap-4 mt-4 border-t border-slate-800 pt-4">
                    <div><p class="label-spread">Casa (${document.getElementById('sprTotalH').value})</p><p class="text-xl font-bold teko text-blue-400">${cH.toFixed(2)}</p></div>
                    <div class="text-right"><p class="label-spread">Ospite (${document.getElementById('sprTotalA').value})</p><p class="text-xl font-bold teko text-blue-400">${cA.toFixed(2)}</p></div>
                </div>
            </div>
            <div class="res-box border-l-purple-500">
                <span class="prob-badge">WIN PROB: ${advOTM.prob}%</span>
                <p class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">In Porta: Previsione vs Spread</p>
                <h2 class="text-6xl font-black teko text-white inline-block">${totalOTM.toFixed(2)}</h2>
                <span class="advice-badge ${advOTM.badgeClass}">${advOTM.label} ${document.getElementById('sprOTMatch').value}</span>
                <div class="grid grid-cols-2 gap-4 mt-4 border-t border-slate-800 pt-4">
                    <div><p class="label-spread">Casa (${document.getElementById('sprOTH').value})</p><p class="text-xl font-bold teko text-purple-400">${oH.toFixed(2)}</p></div>
                    <div class="text-right"><p class="label-spread">Ospite (${document.getElementById('sprOTA').value})</p><p class="text-xl font-bold teko text-purple-400">${oA.toFixed(2)}</p></div>
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
