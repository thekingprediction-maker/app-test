import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI V4", layout="wide")

st.markdown("""
    <style>
        [data-testid="stHeader"], footer {display: none !important;}
        .main .block-container { padding: 10px !important; }
    </style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600&family=Inter:wght@400;900&display=swap');
        body { background: #020617; color: white; font-family: 'Inter', sans-serif; padding: 10px; }
        .teko { font-family: 'Teko', sans-serif; }
        .card { background: #1e293b; border-radius: 15px; padding: 15px; border: 1px solid #334155; }
        select, input { background: #0f172a; border: 1px solid #475569; color: white; padding: 12px; width: 100%; border-radius: 10px; margin-bottom: 10px; font-weight: bold; }
        .btn { background: #3b82f6; width: 100%; padding: 15px; border-radius: 10px; font-weight: 900; color: white; border: none; cursor: pointer; }
        .league-btn { cursor: pointer; padding: 10px; border-radius: 8px; border: 1px solid #334155; text-align: center; font-size: 11px; background: #0f172a; font-weight: bold; }
        .active { background: #3b82f6; border-color: #3b82f6; }
        .res-box { background: #0f172a; border-radius: 12px; padding: 15px; border-left: 4px solid #3b82f6; margin-top: 10px; }
    </style>
</head>
<body>
    <div id="app">
        <h1 class="text-4xl font-black teko text-center italic mb-4 uppercase">PROBET <span class="text-blue-500">AI V4 - 2025</span></h1>
        
        <div class="grid grid-cols-4 gap-2 mb-4">
            <div id="l135" class="league-btn active" onclick="setL(135)">SERIE A</div>
            <div id="l39" class="league-btn" onclick="setL(39)">PREMIER</div>
            <div id="l78" class="league-btn" onclick="setL(78)">BUNDES</div>
            <div id="l140" class="league-btn" onclick="setL(140)">LA LIGA</div>
        </div>

        <div class="card">
            <label class="text-[10px] font-bold text-blue-400">HOME TEAM (STAGIONE 2024/25)</label>
            <select id="hTeam"><option>Caricamento...</option></select>
            
            <label class="text-[10px] font-bold text-blue-400">AWAY TEAM (STAGIONE 2024/25)</label>
            <select id="aTeam"><option>Caricamento...</option></select>
            
            <div id="refContainer">
                <label class="text-[10px] font-bold text-yellow-500">ARBITRO (SERIE A)</label>
                <select id="refSel"></select>
            </div>

            <button onclick="run()" class="btn teko text-2xl italic mt-4 tracking-wider">GENERA ANALISI ELITE</button>
        </div>

        <div id="results" class="mt-4 pb-10"></div>
    </div>

<script>
const K = "75e4107623c05bb4bca2ac8b78b28dca";
const B = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/";
let curL = 135, dbX = [];

function setL(id) {
    curL = id;
    document.querySelectorAll('.league-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('l'+id).classList.add('active');
    document.getElementById('refContainer').style.display = (id==135)?'block':'none';
    load();
}

function load() {
    const f = {135:"DATABASE_AVANZATO_SERIEA_2025.csv", 39:"DATABASE_AVANZATO_PREMIER_2025.csv", 78:"DATABASE_AVANZATO_BUNDES_2025.csv", 140:"DATABASE_AVANZATO_LALIGA_2025.csv"};
    Papa.parse(B + f[curL], { download: true, header: true, complete: (r) => { dbX = r.data; fetchTeams(); } });
    
    if(curL==135) {
        Papa.parse(B + "ARBITRI_SERIE_A%20-%20Foglio1.csv", { download: true, header: true, delimiter: ";", complete: (r) => {
            const s = document.getElementById('refSel'); s.innerHTML = "";
            r.data.forEach(x => { let n = x.Arbitro || Object.values(x)[0]; if(n) s.add(new Option(n, (x["Media Totale"]||"24.5").replace(',','.'))); });
        }});
    }
}

async function fetchTeams() {
    // STAGIONE 2024 è quella che copre l'attuale campionato 2024/2025
    const r = await fetch(`https://v3.football.api-sports.io/standings?league=${curL}&season=2024`, {headers:{"x-apisports-key":K}});
    const d = await r.json();
    
    const h = document.getElementById('hTeam'), a = document.getElementById('aTeam');
    h.innerHTML = ""; a.innerHTML = "";
    
    try {
        // Prendiamo le squadre direttamente dalla classifica ufficiale della stagione attuale
        const teams = d.response[0].league.standings[0];
        teams.sort((x,y) => x.team.name.localeCompare(y.team.name)).forEach(t => {
            h.add(new Option(t.team.name, t.team.id));
            a.add(new Option(t.team.name, t.team.id));
        });
    } catch(e) {
        h.innerHTML = "<option>Errore caricamento squadre</option>";
    }
}

async function run() {
    const res = document.getElementById('results');
    res.innerHTML = "<p class='text-center animate-pulse teko text-2xl py-10'>ANALIZZANDO DATI 2025...</p>";
    
    try {
        const idH = document.getElementById('hTeam').value, idA = document.getElementById('aTeam').value;
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${curL}&season=2024&team=${idH}`, {headers:{"x-apisports-key":K}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${curL}&season=2024&team=${idA}`, {headers:{"x-apisports-key":K}}).then(r=>r.json())
        ]);

        const sH = rH.response, sA = rA.response;
        const xG = parseFloat((dbX.find(x=>x.TeamID==idH)?.xG_Per_Shot || "0.11").toString().replace(',','.'));
        const m = xG / 0.11;

        const tt = (sH.shots.total.average + sA.shots.total.average) * m;
        const pt = (sH.shots.on_goal.average + sA.shots.on_goal.average) * m;
        const ct = (sH.corners.for.average + sA.corners.for.average);

        res.innerHTML = `
            <div class="res-box"><p class="text-[10px] text-blue-400 font-bold">TIRI TOTALI</p><h2 class="text-4xl font-black teko">${tt.toFixed(2)}</h2></div>
            <div class="res-box border-l-purple-500"><p class="text-[10px] text-purple-400 font-bold">TIRI IN PORTA</p><h2 class="text-4xl font-black teko">${pt.toFixed(2)}</h2></div>
            <div class="res-box border-l-cyan-500"><p class="text-[10px] text-cyan-400 font-bold">CORNER</p><h2 class="text-4xl font-black teko">${ct.toFixed(2)}</h2></div>
        `;
    } catch(e) { 
        res.innerHTML = "<p class='text-red-500 bg-red-900/20 p-4 rounded-lg'>Errore API: Dati non disponibili per questa selezione.</p>"; 
    }
}

load();
</script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)
