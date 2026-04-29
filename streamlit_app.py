import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI V4 - ELITE HYBRID", layout="wide")

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
        .res-box { background: #0f172a; border-radius: 20px; padding: 20px; border-left: 5px solid #3b82f6; position: relative; margin-bottom: 20px; }
        
        .advice-tag { display: inline-block; padding: 2px 10px; border-radius: 6px; font-size: 12px; font-weight: 900; margin-left: 10px; vertical-align: middle; }
        .over-tag { background: #10b981; color: #020617; }
        .under-tag { background: #ef4444; color: white; }
        
        .label-spread { font-size: 10px; font-weight: 900; color: #94a3b8; text-transform: uppercase; margin-bottom: 5px; display: block; }

        .league-btn { cursor: pointer; padding: 12px; border-radius: 10px; font-weight: 900; border: 1px solid #334155; text-align: center; transition: 0.3s; font-size: 12px; }
        .league-active { background: #3b82f6; border-color: #3b82f6; color: white; }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-4xl mx-auto">
        <div class="text-center mb-10">
            <h1 class="text-6xl font-black teko tracking-widest text-white uppercase italic">PROBET <span class="text-blue-500">AI V4</span></h1>
            <p class="text-[10px] font-bold text-slate-500 tracking-[0.5em] uppercase">Hybrid GitHub-API Analysis • Referee Adjusted</p>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div id="btn-135" class="league-btn league-active" onclick="switchLeague(135)">SERIE A</div>
            <div id="btn-39" class="league-btn" onclick="switchLeague(39)">PREMIER LEAGUE</div>
            <div id="btn-78" class="league-btn" onclick="switchLeague(78)">BUNDESLIGA</div>
            <div id="btn-140" class="league-btn" onclick="switchLeague(140)">LA LIGA</div>
        </div>

        <div class="card-premium mb-8">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div>
                    <label class="label-spread text-blue-400">Home Team</label>
                    <select id="homeTeam"></select>
                </div>
                <div>
                    <label class="label-spread text-blue-400">Away Team</label>
                    <select id="awayTeam"></select>
                </div>
                <div>
                    <label class="label-spread text-yellow-500">Arbitro (da GitHub)</label>
                    <select id="arbitroSelect">
                        <option value="24.5">Seleziona Arbitro...</option>
                    </select>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 pt-4 border-t border-slate-700">
                <div><label class="label-spread text-emerald-400">Spread Tiri Match</label><input type="number" id="sprTotalMatch" step="0.5" value="23.5"></div>
                <div><label class="label-spread text-emerald-400">Spread Tiri Casa</label><input type="number" id="sprTotalH" step="0.5" value="12.5"></div>
                <div><label class="label-spread text-emerald-400">Spread Tiri Ospite</label><input type="number" id="sprTotalA" step="0.5" value="10.5"></div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 pt-4 border-t border-slate-700">
                <div><label class="label-spread text-red-400">Spread Falli Match</label><input type="number" id="sprFoulsMatch" step="0.5" value="24.5"></div>
                <div><label class="label-spread text-red-400">Spread Falli Casa</label><input type="number" id="sprFoulsH" step="0.5" value="12.5"></div>
                <div><label class="label-spread text-red-400">Spread Falli Ospite</label><input type="number" id="sprFoulsA" step="0.5" value="12.5"></div>
            </div>

            <button onclick="runDeepAnalysis()" class="btn-analizza shadow-xl italic teko text-2xl tracking-widest">GENERA ANALISI ELITE</button>
        </div>

        <div id="results" class="space-y-6 hidden pb-20"></div>
    </div>

<script>
const API_KEY = "75e4107623c05bb4bca2ac8b78b28dca";
const BASE_CSV_URL = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/";

let currentLeague = 135;
let dbXG = [];
let dbRefs = [];

const leagueFiles = {
    135: "DATABASE_AVANZATO_SERIEA_2025.csv",
    39: "DATABASE_AVANZATO_PREMIER_2025.csv",
    78: "DATABASE_AVANZATO_BUNDES_2025.csv",
    140: "DATABASE_AVANZATO_LALIGA_2025.csv"
};

function switchLeague(id) {
    currentLeague = id;
    document.querySelectorAll('.league-btn').forEach(b => b.classList.remove('league-active'));
    document.getElementById(`btn-${id}`).classList.add('league-active');
    loadData();
}

function loadData() {
    // Caricamento xG
    Papa.parse(BASE_CSV_URL + leagueFiles[currentLeague], {
        download: true, header: true, skipEmptyLines: true,
        complete: function(r) { 
            dbXG = r.data; 
            // Caricamento Arbitri (Nome file ipotizzato su GitHub)
            Papa.parse(BASE_CSV_URL + "ARBITRI_SERIEA_2025.csv", {
                download: true, header: true, skipEmptyLines: true,
                complete: function(r2) {
                    dbRefs = r2.data;
                    populateRefs();
                    loadTeams(); 
                }
            });
        }
    });
}

function populateRefs() {
    const sel = document.getElementById('arbitroSelect');
    sel.innerHTML = '<option value="24.5">Seleziona Arbitro...</option>';
    dbRefs.forEach(ref => {
        if(ref.Arbitro) {
            let val = ref["Media Totale"] ? ref["Media Totale"].replace(',', '.') : "24.5";
            let opt = new Option(ref.Arbitro, val);
            sel.add(opt);
        }
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

function calcProb(pred, spr) {
    let diff = pred - spr;
    let p = 50 + (diff * 9.2);
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
    const refAvg = parseFloat(document.getElementById('arbitroSelect').value);
    const resDiv = document.getElementById('results');
    resDiv.innerHTML = "<div class='text-center py-20 animate-pulse text-blue-500 font-black teko text-3xl uppercase tracking-widest'>Analyzing Combined Data...</div>";
    resDiv.classList.remove('hidden');

    try {
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${currentLeague}&season=2025&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${currentLeague}&season=2025&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
        ]);

        // xG logic
        const xGH = parseFloat(dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || 0.11);
        const xGA = parseFloat(dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || 0.11);
        const bench = (currentLeague === 39 || currentLeague === 78) ? 0.12 : 0.11;

        // Tiri logic
        const cH = ((rH.response?.shots?.total?.average || 12.0) + 11.5) / 2 * (xGH / bench) * 1.05;
        const cA = ((rA.response?.shots?.total?.average || 10.5) + 11.0) / 2 * (xGA / bench);
        const totalM = cH + cA;

        // Falli logic: API (60%) + Arbitro (40%)
        const fCommH = rH.response?.fouls?.for?.average || 12.5;
        const fSubH = rH.response?.fouls?.against?.average || 12.0;
        const fCommA = rA.response?.fouls?.for?.average || 13.0;
        const fSubA = rA.response?.fouls?.against?.average || 11.5;

        const baseH = (fCommH + fSubA) / 2;
        const baseA = (fCommA + fSubH) / 2;
        
        // Applichiamo il peso dell'arbitro sulla proiezione totale
        const totalFoulsRaw = baseH + baseA;
        const totalFoulsMatch = (totalFoulsRaw * 0.6) + (refAvg * 0.4);
        
        // Ricalcoliamo le quote casa/ospite in proporzione al nuovo totale
        const ratio = totalFoulsMatch / totalFoulsRaw;
        const finalFoulsH = baseH * ratio;
        const finalFoulsA = baseA * ratio;

        resDiv.innerHTML = `
            <div class="res-box border-l-red-500">
                <p class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">Previsione Falli Totali (Team API + Arbitro GitHub)</p>
                <h2 class="text-6xl font-black teko text-white inline-block">${totalFoulsMatch.toFixed(2)}</h2>
                ${getAdviceHtml(totalFoulsMatch, document.getElementById('sprFoulsMatch').value)}
                
                <div class="grid grid-cols-2 gap-4 mt-4 border-t border-slate-800 pt-4">
                    <div>
                        <p class="text-[10px] text-slate-400 font-bold uppercase">Casa (${document.getElementById('sprFoulsH').value})</p>
                        <p class="text-xl font-bold teko text-red-400">${finalFoulsH.toFixed(2)} ${getAdviceHtml(finalFoulsH, document.getElementById('sprFoulsH').value)}</p>
                    </div>
                    <div class="text-right">
                        <p class="text-[10px] text-slate-400 font-bold uppercase">Ospite (${document.getElementById('sprFoulsA').value})</p>
                        <p class="text-xl font-bold teko text-red-400">${getAdviceHtml(finalFoulsA, document.getElementById('sprFoulsA').value)} ${finalFoulsA.toFixed(2)}</p>
                    </div>
                </div>
            </div>

            <div class="res-box border-l-blue-500">
                <p class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">Previsione Tiri Totali (xG Adjusted)</p>
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
        `;
    } catch(e) { console.error(e); }
}

loadData();
</script>
</body>
</html>
"""
components.html(html_code, height=1200, scrolling=True)
