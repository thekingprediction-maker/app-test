import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI V4 - FIX", layout="wide")

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
        .res-box { background: #0f172a; border-radius: 20px; padding: 25px; border-left: 5px solid #3b82f6; }
        .advice-tag { display: inline-block; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 900; margin-left: 10px; }
        .over-tag { background: #10b981; color: #020617; }
        .under-tag { background: #ef4444; color: white; }
        .league-btn { cursor: pointer; padding: 12px; border-radius: 10px; font-weight: 900; border: 1px solid #334155; text-align: center; background: #1e293b; font-size: 11px; }
        .league-active { background: #3b82f6; border-color: #60a5fa; }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-4xl mx-auto">
        <div class="text-center mb-10">
            <h1 class="text-6xl font-black teko tracking-widest uppercase italic">PROBET <span class="text-blue-500">AI V4</span></h1>
            <p class="text-[10px] font-bold text-slate-500 tracking-[0.4em] uppercase">Power Stats • Defense Adjusted • Stable Version</p>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div id="btn-135" class="league-btn league-active" onclick="switchL(135)">SERIE A</div>
            <div id="btn-39" class="league-btn" onclick="switchL(39)">PREMIER LEAGUE</div>
            <div id="btn-78" class="league-btn" onclick="switchL(78)">BUNDESLIGA</div>
            <div id="btn-140" class="league-btn" onclick="switchL(140)">LA LIGA</div>
        </div>

        <div class="card-premium">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div><label class="text-[10px] font-bold text-blue-400 uppercase">Home Team</label><select id="hT"></select></div>
                <div><label class="text-[10px] font-bold text-blue-400 uppercase">Away Team</label><select id="aT"></select></div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 border-t border-slate-700 pt-6">
                <div><label class="text-[10px] font-bold text-emerald-400 uppercase">Spread Match Totali</label><input type="number" id="sTM" step="0.5" value="24.5"></div>
                <div><label class="text-[10px] font-bold text-emerald-400 uppercase">Spread Casa</label><input type="number" id="sTH" step="0.5" value="13.5"></div>
                <div><label class="text-[10px] font-bold text-emerald-400 uppercase">Spread Ospite</label><input type="number" id="sTA" step="0.5" value="10.5"></div>
            </div>

            <button onclick="run()" class="btn-analizza teko text-2xl tracking-widest mt-6">GENERA ANALISI</button>
        </div>

        <div id="results" class="mt-8 space-y-6 hidden pb-20"></div>
    </div>

<script>
const K = "aa5e53f893088010cc7c47af17f306e9";
const CSV = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/";
let curL = 135; let db = [];

const f = { 135: "DATABASE_AVANZATO_SERIEA_2025.csv", 39: "DATABASE_AVANZATO_PREMIER_2025.csv", 78: "DATABASE_AVANZATO_BUNDES_2025.csv", 140: "DATABASE_AVANZATO_LALIGA_2025.csv" };

function switchL(id) {
    curL = id;
    document.querySelectorAll('.league-btn').forEach(b => b.classList.remove('league-active'));
    document.getElementById('btn-'+id).classList.add('league-active');
    load();
}

function load() {
    Papa.parse(CSV + f[curL], { download: true, header: true, skipEmptyLines: true, complete: function(r) { db = r.data; loadT(); } });
}

async function loadT() {
    const r = await fetch(`https://v3.football.api-sports.io/teams?league=${curL}&season=2025`, {headers:{"x-apisports-key":K}});
    const d = await r.json();
    const h = document.getElementById('hT'), a = document.getElementById('aT');
    h.innerHTML = ""; a.innerHTML = "";
    d.response.sort((x,y)=>x.team.name.localeCompare(y.team.name)).forEach(t => {
        h.add(new Option(t.team.name, t.team.id)); a.add(new Option(t.team.name, t.team.id));
    });
}

function getA(pred, spr) {
    let diff = pred - spr;
    let p = 50 + (diff * 9.0);
    p = Math.min(Math.max(p, 5), 98);
    const label = p >= 50 ? "OVER" : "UNDER";
    const css = p >= 50 ? "over-tag" : "under-tag";
    const prob = p >= 50 ? p : (100 - p);
    return `<span class="advice-tag ${css}">${label} ${spr} (${prob.toFixed(1)}%)</span>`;
}

async function run() {
    const idH = document.getElementById('hT').value, idA = document.getElementById('aT').value;
    const resDiv = document.getElementById('results');
    resDiv.innerHTML = "<div class='text-center py-10 teko text-3xl animate-pulse text-blue-500'>ANALYZING DATA...</div>";
    resDiv.classList.remove('hidden');

    try {
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${curL}&season=2025&team=${idH}`, {headers:{"x-apisports-key":K}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${curL}&season=2025&team=${idA}`, {headers:{"x-apisports-key":K}}).then(r=>r.json())
        ]);

        const xH = parseFloat(db.find(x => x.TeamID == idH)?.xG_Per_Shot || 0.11);
        const xA = parseFloat(db.find(x => x.TeamID == idA)?.xG_Per_Shot || 0.11);
        const bench = (curL === 39 || curL === 78) ? 0.12 : 0.11;

        // Recupero medie totali (più stabili per le API)
        const avgH = rH.response.shots.total.average || 12.0;
        const avgA = rA.response.shots.total.average || 10.0;

        // Logica Defense-Adjusted simulata con pesi incrociati
        const predH = ((avgH + 11.8) / 2) * (xH / bench) * 1.05;
        const predA = ((avgA + 12.2) / 2) * (xA / bench);
        const total = predH + predA;

        resDiv.innerHTML = `
            <div class="res-box">
                <p class="text-[10px] font-bold text-slate-500 uppercase">Previsione Tiri Totali</p>
                <h2 class="text-7xl font-black teko">${total.toFixed(2)} ${getA(total, document.getElementById('sTM').value)}</h2>
                <div class="grid grid-cols-2 mt-6 pt-6 border-t border-slate-800">
                    <div><p class="text-[10px] text-slate-400 uppercase">Casa</p><p class="text-2xl teko text-blue-400">${predH.toFixed(2)} ${getA(predH, document.getElementById('sTH').value)}</p></div>
                    <div class="text-right"><p class="text-[10px] text-slate-400 uppercase">Ospite</p><p class="text-2xl teko text-blue-400">${predA.toFixed(2)} ${getA(predA, document.getElementById('sTA').value)}</p></div>
                </div>
            </div>
        `;
    } catch(e) { resDiv.innerHTML = "<div class='text-red-500'>Errore connessione API. Riprova.</div>"; }
}
switchL(135);
</script>
</body>
</html>
"""
components.html(html_code, height=1000, scrolling=True)
