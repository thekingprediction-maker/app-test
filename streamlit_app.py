import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI V4 - FULL LEAGUE", layout="wide")

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
        select, input { background: #0f172a; border: 1px solid #475569; color: white; padding: 10px; width: 100%; border-radius: 12px; font-weight: bold; outline: none; }
        .btn-analizza { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); width: 100%; padding: 20px; border-radius: 15px; font-weight: 900; text-transform: uppercase; cursor: pointer; border: none; color: white; margin-top: 20px; }
        .res-box { background: #0f172a; border-radius: 20px; padding: 20px; border-left: 5px solid #3b82f6; margin-bottom: 20px; }
        .advice-tag { display: inline-block; padding: 2px 10px; border-radius: 6px; font-size: 12px; font-weight: 900; margin-left: 10px; }
        .over-tag { background: #10b981; color: #020617; }
        .under-tag { background: #ef4444; color: white; }
        .label-spread { font-size: 10px; font-weight: 900; color: #94a3b8; text-transform: uppercase; margin-bottom: 5px; display: block; }
        .league-grid { display: grid; grid-template-cols: repeat(4, 1fr); gap: 10px; margin-bottom: 20px; }
        .league-btn { cursor: pointer; padding: 12px; border-radius: 10px; font-weight: 900; border: 1px solid #334155; text-align: center; font-size: 12px; }
        .active { background: #3b82f6; border-color: #3b82f6; }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-5xl mx-auto">
        <div class="text-center mb-8">
            <h1 class="text-5xl font-black teko tracking-widest uppercase italic">PROBET <span class="text-blue-500">AI V4 GOLD</span></h1>
        </div>

        <div class="league-grid">
            <div id="l135" class="league-btn active" onclick="switchL(135)">SERIE A</div>
            <div id="l39" class="league-btn" onclick="switchL(39)">PREMIER</div>
            <div id="l78" class="league-btn" onclick="switchL(78)">BUNDES</div>
            <div id="l140" class="league-btn" onclick="switchL(140)">LA LIGA</div>
        </div>

        <div class="card-premium">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div><label class="label-spread text-blue-400">Home Team</label><select id="hTeam"></select></div>
                <div><label class="label-spread text-blue-400">Away Team</label><select id="aTeam"></select></div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 border-t border-slate-700 pt-4">
                <div><label class="label-spread text-emerald-400">Spread Tiri Match</label><input type="number" id="sTm" step="0.5" value="24.5"></div>
                <div><label class="label-spread text-purple-400">Spread In Porta Match</label><input type="number" id="sOm" step="0.5" value="8.5"></div>
                <div id="f-box"><label class="label-spread text-orange-400">Spread Falli (A)</label><input type="number" id="sFm" step="0.5" value="25.5"></div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div><label class="label-spread text-yellow-400">Spread Angoli Match</label><input type="number" id="sAm" step="0.5" value="9.5"></div>
                <div><label class="label-spread text-red-400">Spread Cartellini Match</label><input type="number" id="sCm" step="0.5" value="4.5"></div>
            </div>

            <button onclick="analyze()" class="btn-analizza teko text-2xl tracking-widest">ANALIZZA MATCH</button>
        </div>

        <div id="results" class="mt-8 space-y-4 hidden pb-20"></div>
    </div>

<script>
const K = "aa5e53f893088010cc7c47af17f306e9";
const URL_BASE = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/";
let curL = 135;
let db = [];

const files = {
    135: "DATABASE_AVANZATO_SERIEA_2025.csv",
    39: "DATABASE_AVANZATO_PREMIER_2025.csv",
    78: "DATABASE_AVANZATO_BUNDES_2025.csv",
    140: "DATABASE_AVANZATO_LALIGA_2025.csv"
};

function switchL(id) {
    curL = id;
    document.querySelectorAll('.league-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('l'+id).classList.add('active');
    document.getElementById('f-box').style.opacity = (id === 135) ? "1" : "0.3";
    load();
}

function load() {
    Papa.parse(URL_BASE + files[curL], {
        download: true, header: true, skipEmptyLines: true,
        complete: function(r) { db = r.data; fetchTeams(); }
    });
}

async function fetchTeams() {
    const r = await fetch(`https://v3.football.api-sports.io/teams?league=${curL}&season=2025`, {headers:{"x-apisports-key":K}});
    const d = await r.json();
    const h = document.getElementById('hTeam'), a = document.getElementById('aTeam');
    h.innerHTML = ""; a.innerHTML = "";
    d.response.sort((x,y)=>x.team.name.localeCompare(y.team.name)).forEach(t => {
        h.add(new Option(t.team.name, t.team.id)); a.add(new Option(t.team.name, t.team.id));
    });
}

function getBadge(pred, spr) {
    let p = 50 + ((pred - spr) * 8.5);
    p = Math.min(Math.max(p, 5), 98);
    const label = p >= 50 ? "OVER" : "UNDER";
    const css = p >= 50 ? "over-tag" : "under-tag";
    const val = p >= 50 ? p : (100-p);
    return `<span class="advice-tag ${css}">${label} ${spr} (${val.toFixed(1)}%)</span>`;
}

async function analyze() {
    const idH = document.getElementById('hTeam').value, idA = document.getElementById('aTeam').value;
    const res = document.getElementById('results');
    res.innerHTML = "<p class='text-center teko text-2xl animate-pulse'>ELABORAZIONE AI...</p>";
    res.classList.remove('hidden');

    const [rH, rA] = await Promise.all([
        fetch(`https://v3.football.api-sports.io/teams/statistics?league=${curL}&season=2025&team=${idH}`, {headers:{"x-apisports-key":K}}).then(r=>r.json()),
        fetch(`https://v3.football.api-sports.io/teams/statistics?league=${curL}&season=2025&team=${idA}`, {headers:{"x-apisports-key":K}}).then(r=>r.json())
    ]);

    const xH = parseFloat(db.find(x => x.TeamID == idH)?.xG_Per_Shot || 0.11);
    const xA = parseFloat(db.find(x => x.TeamID == idA)?.xG_Per_Shot || 0.11);

    // Tiri & Porta
    const tH = (rH.response.shots.total.average || 12) * (xH/0.11);
    const tA = (rA.response.shots.total.average || 11) * (xA/0.11);
    const oH = (rH.response.shots.on_goal.average || 4) * (xH/0.11);
    const oA = (rA.response.shots.on_goal.average || 3.5) * (xA/0.11);
    
    // Angoli & Cartellini
    const angH = rH.response.corners.average || 5;
    const angA = rA.response.corners.average || 4.5;
    const cardH = (rH.response.cards.yellow.average || 2) + (rH.response.cards.red.average || 0.1);
    const cardA = (rA.response.cards.yellow.average || 2) + (rA.response.cards.red.average || 0.1);

    let html = `
        <div class="res-box border-l-emerald-500">
            <p class="label-spread">Tiri Totali Match: ${(tH+tA).toFixed(2)}</p>
            ${getBadge(tH+tA, document.getElementById('sTm').value)}
        </div>
        <div class="res-box border-l-purple-500">
            <p class="label-spread">Tiri In Porta Match: ${(oH+oA).toFixed(2)}</p>
            ${getBadge(oH+oA, document.getElementById('sOm').value)}
        </div>
        <div class="res-box border-l-yellow-500">
            <p class="label-spread">Angoli Totali Match: ${(angH+angA).toFixed(2)}</p>
            ${getBadge(angH+angA, document.getElementById('sAm').value)}
        </div>
        <div class="res-box border-l-red-500">
            <p class="label-spread">Cartellini Totali Match: ${(cardH+cardA).toFixed(2)}</p>
            ${getBadge(cardH+cardA, document.getElementById('sCm').value)}
        </div>
    `;

    if(curL === 135) {
        const fH = rH.response.fouls.committed.average || 12;
        const fA = rA.response.fouls.committed.average || 12;
        html += `<div class="res-box border-l-orange-500">
            <p class="label-spread">Falli Commessi Match: ${(fH+fA).toFixed(2)}</p>
            ${getBadge(fH+fA, document.getElementById('sFm').value)}
        </div>`;
    }

    res.innerHTML = html;
}
switchL(135);
</script>
</body>
</html>
"""
components.html(html_code, height=1000, scrolling=True)
