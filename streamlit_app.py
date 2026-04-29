import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI V4 - ELITE", layout="wide")

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
        .btn-analizza:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3); }
        
        .res-box { background: #0f172a; border-radius: 20px; padding: 20px; border-left: 5px solid #3b82f6; position: relative; margin-bottom: 20px; }
        
        .advice-tag { display: inline-block; padding: 2px 10px; border-radius: 6px; font-size: 12px; font-weight: 900; margin-left: 10px; vertical-align: middle; }
        .over-tag { background: #10b981; color: #020617; }
        .under-tag { background: #ef4444; color: white; }
        
        .label-spread { font-size: 10px; font-weight: 900; color: #94a3b8; text-transform: uppercase; margin-bottom: 5px; display: block; }

        .league-btn { cursor: pointer; padding: 12px; border-radius: 10px; font-weight: 900; border: 1px solid #334155; text-align: center; transition: 0.3s; font-size: 12px; color: #64748b; }
        .league-active { background: #3b82f6; border-color: #3b82f6; color: white; }

        .status-bar { display: flex; justify-content: center; gap: 20px; margin-bottom: 20px; font-size: 10px; font-weight: bold; text-transform: uppercase; }
        .dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: 5px; }
        .dot-green { background: #10b981; box-shadow: 0 0 5px #10b981; }
        .dot-red { background: #ef4444; }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-4xl mx-auto">
        <div class="text-center mb-6">
            <h1 class="text-6xl font-black teko tracking-widest text-white uppercase italic">PROBET <span class="text-blue-500">AI V4</span></h1>
            <p class="text-[10px] font-bold text-slate-500 tracking-[0.5em] uppercase mb-4">Elite Defense Adjusted Analysis • Precision Mode</p>
            
            <div class="status-bar">
                <span><span id="s-xg" class="dot"></span> Database xG</span>
                <span><span id="s-ref" class="dot"></span> Arbitri CSV</span>
                <span><span id="s-api" class="dot"></span> API Football</span>
            </div>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div id="btn-135" class="league-btn league-active" onclick="switchLeague(135)">SERIE A</div>
            <div id="btn-39" class="league-btn" onclick="switchLeague(39)">PREMIER LEAGUE</div>
            <div id="btn-78" class="league-btn" onclick="switchLeague(78)">BUNDESLIGA</div>
            <div id="btn-140" class="league-btn" onclick="switchLeague(140)">LA LIGA</div>
        </div>

        <div class="card-premium mb-8 shadow-2xl">
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
                    <label class="label-spread text-yellow-500 italic">Arbitro (Serie A Only)</label>
                    <select id="arbitroSelect"><option value="24.5">Seleziona...</option></select>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 pt-4 border-t border-slate-700">
                <div>
                    <label class="label-spread text-emerald-400">Spread Match Falli</label>
                    <input type="number" id="sprFoulsMatch" step="0.5" value="24.5">
                </div>
                <div>
                    <label class="label-spread text-emerald-400">Spread Match Tiri</label>
                    <input type="number" id="sprTotalMatch" step="0.5" value="23.5">
                </div>
                <div>
                    <label class="label-spread text-emerald-400">Spread Match Porta</label>
                    <input type="number" id="sprOTMatch" step="0.5" value="8.5">
                </div>
            </div>

            <button onclick="runDeepAnalysis()" class="btn-analizza shadow-xl italic teko text-3xl tracking-widest">GENERA ANALISI ELITE</button>
        </div>

        <div id="results" class="space-y-6 hidden pb-20"></div>
    </div>

<script>
const API_KEY = "75e4107623c05bb4bca2ac8b78b28dca";
const BASE_CSV_URL = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/";
const FILE_REFS = "ARBITRI_SERIE_A%20-%20Foglio1.csv";

let currentLeague = 135;
let dbXG = [];
let dbRef = [];

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
    // Carica xG
    Papa.parse(BASE_CSV_URL + leagueFiles[currentLeague], {
        download: true, header: true, skipEmptyLines: true,
        complete: function(r) { 
            dbXG = r.data; 
            document.getElementById('s-xg').className = "dot dot-green";
            loadTeams(); 
        },
        error: () => document.getElementById('s-xg').className = "dot dot-red"
    });

    // Carica Arbitri (Solo se Serie A)
    if(currentLeague === 135) {
        Papa.parse(BASE_CSV_URL + FILE_REFS, {
            download: true, header: true, skipEmptyLines: true,
            complete: function(r) {
                dbRef = r.data;
                const sel = document.getElementById('arbitroSelect');
                sel.innerHTML = '<option value="24.5">Seleziona Arbitro...</option>';
                dbRef.forEach(row => {
                    let nome = row.Arbitro || Object.values(row)[0];
                    let media = row["Media Totale"] || Object.values(row)[1];
                    if(nome) {
                        let val = media ? media.toString().replace(',', '.') : "24.5";
                        sel.add(new Option(nome, val));
                    }
                });
                document.getElementById('s-ref').className = "dot dot-green";
            },
            error: () => document.getElementById('s-ref').className = "dot dot-red"
        });
    } else {
        document.getElementById('arbitroSelect').innerHTML = '<option value="24.5">Non disp. per questa lega</option>';
        document.getElementById('s-ref').className = "dot";
    }
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
        document.getElementById('s-api').className = "dot dot-green";
    } catch(e) { document.getElementById('s-api').className = "dot dot-red"; }
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
    const refVal = parseFloat(document.getElementById('arbitroSelect').value);
    const resDiv = document.getElementById('results');
    
    resDiv.innerHTML = "<div class='text-center py-20 animate-pulse text-blue-500 font-black teko text-4xl uppercase tracking-widest tracking-tighter'>Computing Elite Stats...</div>";
    resDiv.classList.remove('hidden');

    try {
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${currentLeague}&season=2025&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${currentLeague}&season=2025&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
        ]);

        const sH = rH.response; const sA = rA.response;
        const xGH = parseFloat(dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || 0.11);
        const xGA = parseFloat(dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || 0.11);
        const bench = (currentLeague === 39 || currentLeague === 78) ? 0.12 : 0.11;

        // Calcolo TIRI
        const cH = (sH.shots.total.average || 12) * (xGH / bench) * 1.05;
        const cA = (sA.shots.total.average || 10) * (xGA / bench);
        const totalTiri = cH + cA;

        // Calcolo TIRI IN PORTA
        const oH = (sH.shots.on_goal.average || 4) * (xGH / bench);
        const oA = (sA.shots.on_goal.average || 3.5) * (xGA / bench);
        const totalPorta = oH + oA;

        // Calcolo FALLI (60% Team + 40% Arbitro)
        const teamFouls = ((sH.fouls.for.average + sA.fouls.against.average)/2 + (sA.fouls.for.average + sH.fouls.against.average)/2);
        const finalFouls = (teamFouls * 0.6) + (refVal * 0.4);

        resDiv.innerHTML = `
            <div class="res-box border-l-yellow-500">
                <p class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">Previsione Falli Totali (Team + Arbitro Adj.)</p>
                <h2 class="text-6xl font-black teko text-white inline-block">${finalFouls.toFixed(2)}</h2>
                ${getAdviceHtml(finalFouls, document.getElementById('sprFoulsMatch').value)}
                <p class="text-[9px] text-yellow-500 font-bold mt-2">TREND ARBITRO: ${refVal} | TREND SQUADRE: ${teamFouls.toFixed(1)}</p>
            </div>

            <div class="res-box border-l-blue-500">
                <p class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">Previsione Tiri Totali (Defense Adjusted)</p>
                <h2 class="text-6xl font-black teko text-white inline-block">${totalTiri.toFixed(2)}</h2>
                ${getAdviceHtml(totalTiri, document.getElementById('sprTotalMatch').value)}
            </div>

            <div class="res-box border-l-purple-500">
                <p class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">Previsione In Porta (Quality Adjusted)</p>
                <h2 class="text-6xl font-black teko text-white inline-block">${totalPorta.toFixed(2)}</h2>
                ${getAdviceHtml(totalPorta, document.getElementById('sprOTMatch').value)}
            </div>
        `;
    } catch(e) { console.error(e); }
}

switchLeague(135);
</script>
</body>
</html>
"""
components.html(html_code, height=1100, scrolling=True)
