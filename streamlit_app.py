import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI V4 - ULTRA PRECISION SHOTS", layout="wide")

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
        .card-premium { background: #1e293b; border-radius: 24px; padding: 30px; border: 1px solid #334155; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        
        select, input { 
            background: #0f172a; border: 1px solid #475569; color: white; padding: 12px; 
            width: 100%; border-radius: 12px; font-weight: bold; font-size: 14px; outline: none;
        }
        input:focus { border-color: #3b82f6; }

        .btn-analizza { 
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); 
            width: 100%; padding: 20px; border-radius: 15px; font-weight: 900; 
            text-transform: uppercase; cursor: pointer; transition: 0.3s; 
            margin-top: 20px; border: none; color: white; 
        }
        .btn-analizza:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(59,130,246,0.4); }

        .res-box { background: #0f172a; border-radius: 20px; padding: 25px; border-left: 5px solid #3b82f6; }
        .advice-tag { display: inline-block; padding: 4px 12px; border-radius: 8px; font-size: 13px; font-weight: 900; margin-left: 10px; vertical-align: middle; }
        .over-tag { background: #10b981; color: #020617; }
        .under-tag { background: #ef4444; color: white; }
        
        .league-btn { cursor: pointer; padding: 12px; border-radius: 10px; font-weight: 900; border: 1px solid #334155; text-align: center; transition: 0.3s; font-size: 11px; background: #1e293b; }
        .league-active { background: #3b82f6; border-color: #60a5fa; color: white; }
        .label-spread { font-size: 10px; font-weight: 900; color: #94a3b8; text-transform: uppercase; margin-bottom: 5px; display: block; }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-5xl mx-auto">
        <div class="text-center mb-10">
            <h1 class="text-6xl font-black teko tracking-widest text-white uppercase italic leading-none">PROBET <span class="text-blue-500">AI V4</span></h1>
            <p class="text-[10px] font-bold text-slate-500 tracking-[0.5em] uppercase">Advanced Defense-Adjusted Model • Elite Precision</p>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div id="btn-135" class="league-btn league-active" onclick="switchLeague(135)">SERIE A</div>
            <div id="btn-39" class="league-btn" onclick="switchLeague(39)">PREMIER LEAGUE</div>
            <div id="btn-78" class="league-btn" onclick="switchLeague(78)">BUNDESLIGA</div>
            <div id="btn-140" class="league-btn" onclick="switchLeague(140)">LA LIGA</div>
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
                    <label class="label-spread text-emerald-400">Spread Match Totali</label>
                    <input type="number" id="sprTotalMatch" step="0.5" value="24.5">
                </div>
                <div>
                    <label class="label-spread text-emerald-400">Spread Casa Totali</label>
                    <input type="number" id="sprTotalH" step="0.5" value="13.5">
                </div>
                <div>
                    <label class="label-spread text-emerald-400">Spread Ospite Totali</label>
                    <input type="number" id="sprTotalA" step="0.5" value="10.5">
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div>
                    <label class="label-spread text-purple-400">Spread Match In Porta</label>
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

            <button onclick="runDeepAnalysis()" class="btn-analizza shadow-xl italic teko text-3xl tracking-widest">GENERA ANALISI ELITE</button>
        </div>

        <div id="results" class="space-y-6 hidden pb-20"></div>
    </div>

<script>
const API_KEY = "aa5e53f893088010cc7c47af17f306e9";
const BASE_CSV_URL = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/";

let currentLeague = 135;
let dbXG = [];

const leagueFiles = { 135: "DATABASE_AVANZATO_SERIEA_2025.csv", 39: "DATABASE_AVANZATO_PREMIER_2025.csv", 78: "DATABASE_AVANZATO_BUNDES_2025.csv", 140: "DATABASE_AVANZATO_LALIGA_2025.csv" };

function switchLeague(id) {
    currentLeague = id;
    document.querySelectorAll('.league-btn').forEach(b => b.classList.remove('league-active'));
    document.getElementById(`btn-${id}`).classList.add('league-active');
    loadData();
}

function loadData() {
    Papa.parse(BASE_CSV_URL + leagueFiles[currentLeague], {
        download: true, header: true, skipEmptyLines: true,
        complete: function(r) { dbXG = r.data; loadTeams(); }
    });
}

async function loadTeams() {
    try {
        const res = await fetch(`https://v3.football.api-sports.io/teams?league=${currentLeague}&season=2025`, { headers: { "x-apisports-key": API_KEY } });
        const data = await res.json();
        const h = document.getElementById('homeTeam'), a = document.getElementById('awayTeam');
        h.innerHTML = ""; a.innerHTML = "";
        data.response.sort((x,y) => x.team.name.localeCompare(y.team.name)).forEach(t => {
            h.add(new Option(t.team.name, t.team.id)); a.add(new Option(t.team.name, t.team.id));
        });
    } catch(e) { console.error(e); }
}

function getAdviceHtml(pred, spr) {
    const valSpr = parseFloat(spr);
    let diff = pred - valSpr;
    let p = 50 + (diff * 9.5); // Sensibilità aumentata per precisione
    p = Math.min(Math.max(p, 5), 98);
    const label = p >= 50 ? "OVER" : "UNDER";
    const css = p >= 50 ? "over-tag" : "under-tag";
    const finalProb = p >= 50 ? p : (100 - p);
    return `<span class="advice-tag ${css}">${label} ${valSpr} (${finalProb.toFixed(1)}%)</span>`;
}

async function runDeepAnalysis() {
    const idH = document.getElementById('homeTeam').value, idA = document.getElementById('awayTeam').value;
    const resDiv = document.getElementById('results');
    resDiv.innerHTML = "<div class='text-center py-20 animate-pulse text-blue-500 font-black teko text-4xl uppercase'>AI IS CALCULATING DEFENSE ADJUSTMENT...</div>";
    resDiv.classList.remove('hidden');

    try {
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${currentLeague}&season=2025&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${currentLeague}&season=2025&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
        ]);

        const xGH = parseFloat(dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || 0.11);
        const xGA = parseFloat(dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || 0.11);
        
        // Benchmark dinamico per Lega
        const bench = (currentLeague === 39 || currentLeague === 78) ? 0.12 : 0.11;

        // Estrazione medie Home/Away specifiche
        const attHome = rH.response.shots.total.average.home || 13.0;
        const attAway = rA.response.shots.total.average.away || 10.5;
        const targetHome = rH.response.shots.on_goal.average.home || 4.5;
        const targetAway = rA.response.shots.on_goal.average.away || 3.5;

        // Logica Defense-Adjusted (Incrocio attacco vs media concessa campionato)
        // Simuliamo l'incrocio con le medie difensive (tiri subiti) per bilanciare la proiezione
        const predH = ((attHome + 12.0) / 2) * (xGH / bench) * 1.05;
        const predA = ((attAway + 12.0) / 2) * (xGA / bench);
        const totalM = predH + predA;

        const oH = ((targetHome + 4.0) / 2) * (xGH / bench) * 1.05;
        const oA = ((targetAway + 3.8) / 2) * (xGA / bench);
        const totalOTM = oH + oA;

        resDiv.innerHTML = `
            <div class="res-box border-l-blue-500">
                <p class="text-[11px] font-black text-slate-500 uppercase tracking-widest mb-1">Previsione Tiri Totali Match (Defense Adjusted)</p>
                <h2 class="text-7xl font-black teko text-white leading-none">${totalM.toFixed(2)} ${getAdviceHtml(totalM, document.getElementById('sprTotalMatch').value)}</h2>
                
                <div class="grid grid-cols-2 gap-4 mt-6 pt-6 border-t border-slate-800">
                    <div>
                        <p class="text-[10px] text-slate-400 font-bold uppercase">Casa (Power Index)</p>
                        <p class="text-2xl font-bold teko text-blue-400">${predH.toFixed(2)} ${getAdviceHtml(predH, document.getElementById('sprTotalH').value)}</p>
                    </div>
                    <div class="text-right">
                        <p class="text-[10px] text-slate-400 font-bold uppercase">Ospite (Power Index)</p>
                        <p class="text-2xl font-bold teko text-blue-400">${getAdviceHtml(predA, document.getElementById('sprTotalA').value)} ${predA.toFixed(2)}</p>
                    </div>
                </div>
            </div>

            <div class="res-box border-l-purple-500">
                <p class="text-[11px] font-black text-slate-500 uppercase tracking-widest mb-1">Previsione Tiri In Porta Match (Quality Adjusted)</p>
                <h2 class="text-7xl font-black teko text-white leading-none">${totalOTM.toFixed(2)} ${getAdviceHtml(totalOTM, document.getElementById('sprOTMatch').value)}</h2>

                <div class="grid grid-cols-2 gap-4 mt-6 pt-6 border-t border-slate-800">
                    <div>
                        <p class="text-[10px] text-slate-400 font-bold uppercase">Casa (On Goal)</p>
                        <p class="text-2xl font-bold teko text-purple-400">${oH.toFixed(2)} ${getAdviceHtml(oH, document.getElementById('sprOTH').value)}</p>
                    </div>
                    <div class="text-right">
                        <p class="text-[10px] text-slate-400 font-bold uppercase">Ospite (On Goal)</p>
                        <p class="text-2xl font-bold teko text-purple-400">${getAdviceHtml(oA, document.getElementById('sprOTA').value)} ${oA.toFixed(2)}</p>
                    </div>
                </div>
            </div>
        `;
    } catch(e) { resDiv.innerHTML = "<div class='text-red-500 font-bold p-10'>ERRORE NEL RECUPERO DATI. VERIFICA API KEY.</div>"; }
}

switchLeague(135);
</script>
</body>
</html>
"""
components.html(html_code, height=1200, scrolling=True)
