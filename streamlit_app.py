import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI V3 - MANUAL SPREAD", layout="wide")

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
        
        /* Stile Input e Select */
        select, input { 
            background: #0f172a; 
            border: 1px solid #475569; 
            color: white; 
            padding: 12px; 
            width: 100%; 
            border-radius: 12px; 
            font-weight: bold; 
            font-size: 14px;
            outline: none;
        }
        input:focus { border-color: #3b82f6; background: #1e293b; }

        .btn-analizza { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); width: 100%; padding: 20px; border-radius: 15px; font-weight: 900; text-transform: uppercase; cursor: pointer; transition: 0.3s; margin-top: 20px; border: none; color: white; }
        .res-box { background: #0f172a; border-radius: 20px; padding: 20px; border-left: 5px solid #3b82f6; position: relative; }
        
        /* Badge Advice */
        .advice-tag { display: inline-block; padding: 2px 10px; border-radius: 6px; font-size: 12px; font-weight: 900; margin-left: 10px; vertical-align: middle; }
        .over-tag { background: #10b981; color: #020617; }
        .under-tag { background: #ef4444; color: white; }
        
        .label-spread { font-size: 10px; font-weight: 900; color: #94a3b8; text-transform: uppercase; margin-bottom: 5px; display: block; }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-4xl mx-auto">
        <div class="text-center mb-10">
            <h1 class="text-6xl font-black teko tracking-widest text-white uppercase italic">PROBET <span class="text-blue-500">AI V3</span></h1>
            <p class="text-[10px] font-bold text-slate-500 tracking-[0.5em] uppercase">Manual Spread Entry • Smart Advice</p>
        </div>

        <div class="card-premium mb-8">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div>
                    <label class="label-spread text-blue-400">Home Team</label>
                    <select id="homeTeam"></select>
                </div>
                <div>
                    <label class="label-spread text-blue-400">Away Team</label>
                    <select id="awayTeam"></select>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 pt-4 border-t border-slate-700">
                <div>
                    <label class="label-spread text-emerald-400">Inserisci Spread Match Totali</label>
                    <input type="number" id="sprTotalMatch" step="0.5" value="23.5">
                </div>
                <div>
                    <label class="label-spread text-emerald-400">Spread Casa Totali</label>
                    <input type="number" id="sprTotalH" step="0.5" value="12.5">
                </div>
                <div>
                    <label class="label-spread text-emerald-400">Spread Ospite Totali</label>
                    <input type="number" id="sprTotalA" step="0.5" value="10.5">
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div>
                    <label class="label-spread text-purple-400">Inserisci Spread Match In Porta</label>
                    <input type="number" id="sprOTMatch" step="0.5" value="8.5">
                </div>
                <div>
                    <label class="label-spread text-purple-400">Spread Casa In Porta</label>
                    <input type="number" id="sprOTH" step="0.5" value="4.5">
                </div>
                <div>
                    <label class="label-spread text-purple-400">Spread Ospite In Porta</label>
                    <input type="number" id="sprOTA" step="0.5" value="3.5">
                </div>
            </div>

            <button onclick="runDeepAnalysis()" class="btn-analizza shadow-xl italic teko text-2xl tracking-widest">GENERA CONSIGLIO AI</button>
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

function calcProb(pred, spr) {
    let diff = pred - spr;
    let p = 50 + (diff * 8.5);
    return Math.min(Math.max(p, 5), 98).toFixed(1);
}

function getAdviceHtml(pred, spr) {
    const valSpr = parseFloat(spr);
    if(isNaN(valSpr)) return "";
    const p = parseFloat(calcProb(pred, valSpr));
    const label = p >= 50 ? "OVER" : "UNDER";
    const css = p >= 50 ? "over-tag" : "under-tag";
    const finalProb = p >= 50 ? p : (100 - p).toFixed(1);
    return `<span class="advice-tag ${css}">${label} ${valSpr} (${finalProb}%)</span>`;
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

        const xGH = parseFloat(dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || 0.11);
        const xGA = parseFloat(dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || 0.11);

        const cH = (rH.response?.shots?.total?.average || 12.0) * (xGH / 0.11) * 1.05;
        const cA = (rA.response?.shots?.total?.average || 10.5) * (xGA / 0.11);
        const totalM = cH + cA;

        const oH = (rH.response?.shots?.on_goal?.average || 4.0) * (xGH / 0.11) * 1.05;
        const oA = (rA.response?.shots?.on_goal?.average || 3.5) * (xGA / 0.11);
        const totalOTM = oH + oA;

        resDiv.innerHTML = `
            <div class="res-box border-l-blue-500">
                <p class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">Previsione Tiri Totali Match</p>
                <h2 class="text-6xl font-black teko text-white inline-block">${totalM.toFixed(2)}</h2>
                ${getAdviceHtml(totalM, document.getElementById('sprTotalMatch').value)}
                
                <div class="grid grid-cols-2 gap-4 mt-4 border-t border-slate-800 pt-4">
                    <div>
                        <p class="text-[10px] text-slate-400 font-bold uppercase">Casa (${document.getElementById('sprTotalH').value})</p>
                        <p class="text-xl font-bold teko text-blue-400">${cH.toFixed(2)} ${getAdviceHtml(cH, document.getElementById('sprTotalH').value)}</p>
                    </div>
                    <div class="text-right">
                        <p class="text-[10px] text-slate-400 font-bold uppercase">Ospite (${document.getElementById('sprTotalA').value})</p>
                        <p class="text-xl font-bold teko text-blue-400">${getAdviceHtml(cA, document.getElementById('sprTotalA').value)} ${cA.toFixed(2)}</p>
                    </div>
                </div>
            </div>

            <div class="res-box border-l-purple-500">
                <p class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">Previsione Tiri In Porta Match</p>
                <h2 class="text-6xl font-black teko text-white inline-block">${totalOTM.toFixed(2)}</h2>
                ${getAdviceHtml(totalOTM, document.getElementById('sprOTMatch').value)}

                <div class="grid grid-cols-2 gap-4 mt-4 border-t border-slate-800 pt-4">
                    <div>
                        <p class="text-[10px] text-slate-400 font-bold uppercase">Casa (${document.getElementById('sprOTH').value})</p>
                        <p class="text-xl font-bold teko text-purple-400">${oH.toFixed(2)} ${getAdviceHtml(oH, document.getElementById('sprOTH').value)}</p>
                    </div>
                    <div class="text-right">
                        <p class="text-[10px] text-slate-400 font-bold uppercase">Ospite (${document.getElementById('sprOTA').value})</p>
                        <p class="text-xl font-bold teko text-purple-400">${getAdviceHtml(oA, document.getElementById('sprOTA').value)} ${oA.toFixed(2)}</p>
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
