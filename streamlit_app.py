import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI V4", layout="wide")

st.markdown("""
    <style>
        [data-testid="stHeader"], footer {display: none !important;}
        .main .block-container { padding: 5px !important; }
        iframe { border: none !important; }
    </style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600&family=Inter:wght@400;900&display=swap');
        body { background: #020617; color: white; font-family: 'Inter', sans-serif; padding: 10px; }
        .teko { font-family: 'Teko', sans-serif; }
        .card { background: #1e293b; border-radius: 20px; padding: 15px; border: 1px solid #334155; }
        select, input { background: #0f172a; border: 1px solid #475569; color: white; padding: 10px; width: 100%; border-radius: 10px; margin-bottom: 8px; font-weight: bold; font-size: 14px; }
        .btn { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); width: 100%; padding: 16px; border-radius: 12px; font-weight: 900; color: white; border: none; cursor: pointer; }
        .league-btn { cursor: pointer; padding: 10px; border-radius: 8px; border: 1px solid #334155; text-align: center; font-size: 11px; background: #0f172a; font-weight: bold; }
        .active { background: #3b82f6; border-color: #3b82f6; }
        .label-sm { font-size: 10px; color: #94a3b8; text-transform: uppercase; font-weight: 800; margin-bottom: 3px; display: block; }
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 5px; border-top: 1px solid #334155; padding-top: 8px; }
        .res-box { background: #0f172a; border-radius: 15px; padding: 15px; border-left: 5px solid #3b82f6; margin-top: 12px; }
    </style>
</head>
<body>
    <div id="app">
        <h1 class="text-5xl font-black teko text-center italic mb-4 uppercase">PROBET <span class="text-blue-500">AI V4</span></h1>
        
        <div class="grid grid-cols-4 gap-2 mb-4">
            <div id="l135" class="league-btn active" onclick="setL(135)">SERIE A</div>
            <div id="l39" class="league-btn" onclick="setL(39)">PREMIER</div>
            <div id="l78" class="league-btn" onclick="setL(78)">BUNDES</div>
            <div id="l140" class="league-btn" onclick="setL(140)">LA LIGA</div>
        </div>

        <div class="card">
            <div class="grid grid-cols-1 gap-2">
                <div><label class="label-sm">Home Team</label><select id="hTeam"></select></div>
                <div><label class="label-sm">Away Team</label><select id="aTeam"></select></div>
                <div id="refBox"><label class="label-sm text-yellow-500 italic">Arbitro (Serie A)</label><select id="refSel"></select></div>
            </div>

            <div class="grid-3">
                <div><label class="label-sm text-emerald-400">Tiri Tot</label><input type="number" id="s_tt" step="0.5" value="23.5"></div>
                <div><label class="label-sm text-emerald-400">Casa</label><input type="number" id="s_th" step="0.5" value="12.5"></div>
                <div><label class="label-sm text-emerald-400">Ospite</label><input type="number" id="s_ta" step="0.5" value="10.5"></div>
            </div>

            <div class="grid-3">
                <div><label class="label-sm text-purple-400">Porta Tot</label><input type="number" id="s_pt" step="0.5" value="8.5"></div>
                <div><label class="label-sm text-purple-400">Casa</label><input type="number" id="s_ph" step="0.5" value="4.5"></div>
                <div><label class="label-sm text-purple-400">Ospite</label><input type="number" id="s_pa" step="0.5" value="3.5"></div>
            </div>

            <div class="grid-3" id="foulGrid">
                <div><label class="label-sm text-red-400">Falli Tot</label><input type="number" id="s_ft" step="0.5" value="24.5"></div>
                <div><label class="label-sm text-red-400">Casa</label><input type="number" id="s_fh" step="0.5" value="12.5"></div>
                <div><label class="label-sm text-red-400">Ospite</label><input type="number" id="s_fa" step="0.5" value="11.5"></div>
            </div>

            <div class="grid-3">
                <div><label class="label-sm text-cyan-400">Corner Tot</label><input type="number" id="s_ct" step="0.5" value="9.5"></div>
                <div><label class="label-sm text-cyan-400">Casa</label><input type="number" id="s_ch" step="0.5" value="5.5"></div>
                <div><label class="label-sm text-cyan-400">Ospite</label><input type="number" id="s_ca" step="0.5" value="4.5"></div>
            </div>

            <div class="grid-3">
                <div><label class="label-sm text-yellow-400">Gialli Tot</label><input type="number" id="s_gt" step="0.5" value="4.5"></div>
                <div><label class="label-sm text-yellow-400">Casa</label><input type="number" id="s_gh" step="0.5" value="2.5"></div>
                <div><label class="label-sm text-yellow-400">Ospite</label><input type="number" id="s_ga" step="0.5" value="2.5"></div>
            </div>

            <button onclick="run()" class="btn teko text-2xl italic mt-4 tracking-widest">GENERA ANALISI ELITE</button>
        </div>

        <div id="results" class="pb-20"></div>
    </div>

<script>
const K = "75e4107623c05bb4bca2ac8b78b28dca";
const B = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/";
let curL = 135, dbX = [];

function setL(id) {
    curL = id;
    document.querySelectorAll('.league-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('l'+id).classList.add('active');
    document.getElementById('refBox').style.display = (id==135)?'block':'none';
    document.getElementById('foulGrid').style.display = (id==135)?'grid':'none';
    load();
}

function load() {
    const f = {135:"DATABASE_AVANZATO_SERIEA_2025.csv", 39:"DATABASE_AVANZATO_PREMIER_2025.csv", 78:"DATABASE_AVANZATO_BUNDES_2025.csv", 140:"DATABASE_AVANZATO_LALIGA_2025.csv"};
    Papa.parse(B + f[curL], { download: true, header: true, complete: (r) => { dbX = r.data; fetchTeams(); } });
    if(curL==135) Papa.parse(B + "ARBITRI_SERIE_A%20-%20Foglio1.csv", { download: true, header: true, delimiter: ";", complete: (r) => {
        const s = document.getElementById('refSel'); s.innerHTML = "";
        r.data.forEach(x => { let n = x.Arbitro || Object.values(x)[0]; if(n) s.add(new Option(n, (x["Media Totale"]||"24.5").toString().replace(',','.'))); });
    }});
}

async function fetchTeams() {
    const r = await fetch(`https://v3.football.api-sports.io/standings?league=${curL}&season=2024`, {headers:{"x-apisports-key":K}});
    const d = await r.json();
    const h = document.getElementById('hTeam'), a = document.getElementById('aTeam');
    h.innerHTML = ""; a.innerHTML = "";
    if(d.response && d.response[0]) {
        const teams = d.response[0].league.standings[0];
        teams.sort((x,y)=>x.team.name.localeCompare(y.team.name)).forEach(t => {
            h.add(new Option(t.team.name, t.team.id)); a.add(new Option(t.team.name, t.team.id));
        });
    }
}

function getB(val, id) {
    const el = document.getElementById(id);
    if (!el || el.offsetParent === null) return ""; 
    const s = parseFloat(el.value);
    const p = Math.min(Math.max(50 + (val-s)*9, 5), 98);
    return `<br><span class="text-[10px] px-2 py-1 rounded font-black ${val>=s?'bg-emerald-500 text-black':'bg-red-500 text-white'}">${val>=s?'OVER':'UNDER'} ${s} (${(val>=s?p:100-p).toFixed(1)}%)</span>`;
}

async function run() {
    const res = document.getElementById('results');
    res.innerHTML = "<p class='text-center py-10 teko text-2xl animate-pulse text-blue-400'>ANALISI IN CORSO...</p>";
    
    try {
        const idH = document.getElementById('hTeam').value, idA = document.getElementById('aTeam').value;
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${curL}&season=2024&team=${idH}`, {headers:{"x-apisports-key":K}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${curL}&season=2024&team=${idA}`, {headers:{"x-apisports-key":K}}).then(r=>r.json())
        ]);

        if(!rH.response || !rA.response) throw new Error("Dati mancanti");

        const sH = rH.response, sA = rA.response;
        const xGH = parseFloat((dbX.find(x=>x.TeamID==idH)?.xG_Per_Shot || "0.11").toString().replace(',','.'));
        const xGA = parseFloat((dbX.find(x=>x.TeamID==idA)?.xG_Per_Shot || "0.11").toString().replace(',','.'));
        const mH = xGH/0.11, mA = xGA/0.11;

        const ttH = (sH.shots.total.average || 12) * mH;
        const ttA = (sA.shots.total.average || 10) * mA;
        const ptH = (sH.shots.on_goal.average || 4) * mH;
        const ptA = (sA.shots.on_goal.average || 3) * mA;
        const cor = (sH.corners.for.average || 5) + (sA.corners.for.average || 4.5);
        const gia = (sH.cards.yellow.average || 2) + (sA.cards.yellow.average || 2);

        let h = `<div class="res-box"><div>TIRI TOTALI</div><div class="text-4xl font-black teko">${(ttH+ttA).toFixed(2)} ${getB(ttH+ttA, 's_tt')}</div></div>`;
        h += `<div class="res-box border-l-emerald-500"><div>CASA: ${ttH.toFixed(2)} ${getB(ttH, 's_th')}</div><div>OSPITE: ${ttA.toFixed(2)} ${getB(ttA, 's_ta')}</div></div>`;
        h += `<div class="res-box border-l-purple-500"><div>IN PORTA</div><div class="text-4xl font-black teko">${(ptH+ptA).toFixed(2)} ${getB(ptH+ptA, 's_pt')}</div></div>`;
        
        if(curL==135) {
            const rf = parseFloat(document.getElementById('refSel').value) || 24.5;
            const ft = (sH.fouls.for.average + sA.fouls.for.average) * 0.7 + (rf * 0.3);
            h += `<div class="res-box border-l-red-500"><div>FALLI</div><div class="text-4xl font-black teko">${ft.toFixed(2)} ${getB(ft, 's_ft')}</div></div>`;
        }

        h += `<div class="res-box border-l-cyan-500"><div>CORNER</div><div class="text-4xl font-black teko">${cor.toFixed(2)} ${getB(cor, 's_ct')}</div></div>`;
        h += `<div class="res-box border-l-yellow-500"><div>GIALLI</div><div class="text-4xl font-black teko">${gia.toFixed(2)} ${getB(gia, 's_gt')}</div></div>`;

        res.innerHTML = h;
    } catch(e) { res.innerHTML = "<p class='text-red-500 text-center font-bold p-4 bg-red-900/20 rounded-lg'>API NON TROVATA O DATI MANCANTI PER QUESTA STAGIONE.</p>"; }
}
load();
</script>
</body>
</html>
"""

components.html(html_code, height=1400, scrolling=True)
