import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI - PREDICTOR", layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
        body { background: #0b0f1a; color: white; font-family: 'Inter', sans-serif; }
        .main-container { max-width: 800px; margin: auto; padding: 20px; }
        .header-logo { font-size: 24px; font-weight: 900; letter-spacing: 1px; margin-bottom: 30px; text-transform: uppercase; }
        .header-logo span { color: #3b82f6; }
        
        .input-card { background: #161b2c; border-radius: 12px; padding: 25px; border: 1px solid #2d334a; }
        .field-label { font-size: 10px; font-weight: 800; color: #64748b; text-transform: uppercase; margin-bottom: 8px; display: block; }
        
        select, input { 
            background: #1e2538; border: 1px solid #2d334a; color: white; padding: 12px; 
            width: 100%; border-radius: 8px; margin-bottom: 20px; outline: none; font-weight: 600;
        }

        .quote-grid { background: #0f1423; border-radius: 12px; padding: 20px; margin-top: 10px; border: 1px solid #2d334a; }
        .bookmaker-section { display: grid; grid-template-cols: 1fr 1fr 1fr; gap: 15px; }
        .stat-column { text-align: center; }
        .line-main { background: #1e2538; padding: 15px; border-radius: 8px; font-weight: 900; font-size: 18px; margin-bottom: 10px; border: 1px solid #3b82f6; color: white; }
        .line-sub-grid { display: grid; grid-template-cols: 1fr 1fr; gap: 8px; }
        .line-sub { background: #1e2538; padding: 8px; border-radius: 6px; font-size: 12px; color: #94a3b8; border: 1px solid #2d334a; }

        .btn-analizza { 
            background: #3b82f6; color: white; width: 100%; padding: 18px; border-radius: 10px; 
            font-weight: 900; text-transform: uppercase; cursor: pointer; margin-top: 25px;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4); border: none; transition: 0.2s;
        }
        .btn-analizza:hover { background: #2563eb; }

        .res-box { background: #161b2c; border-radius: 12px; padding: 25px; margin-top: 20px; border-left: 5px solid #10b981; }
        .prob-value { font-size: 42px; font-weight: 900; color: white; line-height: 1; }
        .badge-confidence { background: #10b981; color: white; padding: 4px 12px; border-radius: 4px; font-size: 10px; font-weight: 900; margin-bottom: 10px; display: inline-block; }
    </style>
</head>
<body>
    <div class="main-container">
        <div class="header-logo italic">PROBET <span>AI</span></div>

        <div class="input-card">
            <label class="field-label">Casa</label>
            <select id="homeTeam"></select>

            <label class="field-label">Ospite</label>
            <select id="awayTeam"></select>

            <label class="field-label">Arbitro (Opzionale)</label>
            <select id="referee">
                <option value="none">Seleziona Arbitro</option>
                <option value="1">Maresca</option>
                <option value="2">Orsato</option>
                <option value="3">Guida</option>
            </select>

            <div class="quote-grid">
                <div class="field-label mb-4">✎ Quote Bookmaker</div>
                <div class="bookmaker-section">
                    <div class="stat-column">
                        <div class="field-label" style="color:#ef4444">Linee Falli</div>
                        <input type="text" class="line-main text-center" id="lineF" value="24.5">
                        <div class="line-sub-grid">
                            <input type="text" class="line-sub text-center" value="11.5">
                            <input type="text" class="line-sub text-center" value="11.5">
                        </div>
                    </div>
                    <div class="stat-column">
                        <div class="field-label" style="color:#3b82f6">Tiri Totali</div>
                        <input type="text" class="line-main text-center" id="lineT" value="23.5">
                        <div class="line-sub-grid">
                            <input type="text" class="line-sub text-center" id="lineT_H" value="12.5">
                            <input type="text" class="line-sub text-center" id="lineT_A" value="10.5">
                        </div>
                    </div>
                    <div class="stat-column">
                        <div class="field-label" style="color:#a855f7">In Porta</div>
                        <input type="text" class="line-main text-center" id="lineP" value="8.5">
                        <div class="line-sub-grid">
                            <input type="text" class="line-sub text-center" id="lineP_H" value="4.5">
                            <input type="text" class="line-sub text-center" id="lineP_A" value="3.5">
                        </div>
                    </div>
                </div>
            </div>

            <button onclick="runAnalysis()" class="btn-analizza italic">⚡ ANALIZZA DATI</button>
        </div>

        <div id="results" class="hidden"></div>
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

// Funzione sicura per estrarre la media o calcolarla dai totali
function getAvg(stat) {
    if (!stat) return 0;
    if (stat.average) return parseFloat(stat.average);
    if (stat.total && stat.played) return parseFloat(stat.total / stat.played);
    return 0;
}

async function runAnalysis() {
    const idH = document.getElementById('homeTeam').value, idA = document.getElementById('awayTeam').value;
    const lT = parseFloat(document.getElementById('lineT').value);
    const lP = parseFloat(document.getElementById('lineP').value);
    
    const resDiv = document.getElementById('results');
    resDiv.innerHTML = "<div class='text-center py-10 animate-pulse text-blue-500 font-bold'>ESTRAZIONE DATI 2025...</div>";
    resDiv.classList.remove('hidden');

    try {
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
        ]);

        const sH = rH.response, sA = rA.response;
        const xGH = parseFloat(dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || 0.11);
        const xGA = parseFloat(dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || 0.11);

        // Algoritmo Tiri
        const shotsH = getAvg(sH.shots.total) || 12.5;
        const shotsA = getAvg(sA.shots.total) || 11.0;
        const totalT = (shotsH * (xGH/0.11) * 1.05) + (shotsA * (xGA/0.11));
        
        // Algoritmo In Porta
        const ogH = getAvg(sH.shots.on_goal) || 4.2;
        const ogA = getAvg(sA.shots.on_goal) || 3.8;
        const totalP = (ogH * (xGH/0.11) * 1.05) + (ogA * (xGA/0.11));

        // Calcolo Probabilità basato sulle linee inserite
        const probT = Math.min(Math.max(50 + ((totalT - lT) * 6), 30), 92);
        const probP = Math.min(Math.max(50 + ((totalP - lP) * 8), 30), 92);

        resDiv.innerHTML = `
            <div class="res-box">
                <div class="badge-confidence">HIGH CONFIDENCE</div>
                <div class="flex justify-between items-end">
                    <div>
                        <p class="field-label text-blue-400">Previsione Tiri Totali</p>
                        <div class="prob-value">${totalT.toFixed(2)}</div>
                    </div>
                    <div class="text-right">
                        <p class="field-label">Probabilità Over ${lT}</p>
                        <p class="text-3xl font-black text-emerald-400">${probT.toFixed(1)}%</p>
                    </div>
                </div>
            </div>

            <div class="res-box" style="border-left-color: #a855f7;">
                <div class="badge-confidence" style="background: #a855f7;">ON TARGET ANALYSIS</div>
                <div class="flex justify-between items-end">
                    <div>
                        <p class="field-label text-purple-400">Previsione In Porta</p>
                        <div class="prob-value">${totalP.toFixed(2)}</div>
                    </div>
                    <div class="text-right">
                        <p class="field-label">Probabilità Over ${lP}</p>
                        <p class="text-3xl font-black text-purple-400">${probP.toFixed(1)}%</p>
                    </div>
                </div>
            </div>
        `;
    } catch(e) { 
        resDiv.innerHTML = "<div class='p-5 bg-red-900/20 text-red-400 text-center font-bold'>ERRORE: Dati API non disponibili per queste squadre.</div>";
    }
}
</script>
</body>
</html>
"""
components.html(html_code, height=1000, scrolling=True)
