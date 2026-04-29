import streamlit as st
import streamlit.components.v1 as components

# Configurazione Pagina per Mobile
st.set_page_config(page_title="PROBET AI V4", layout="wide", initial_sidebar_state="collapsed")

# CSS per eliminare header e margini di Streamlit (Fix Taglio Superiore)
st.markdown("""
    <style>
        [data-testid="stHeader"], footer {display: none !important;}
        .main .block-container { padding: 0 !important; margin: 0 !important; }
        iframe { border: none !important; margin-top: -30px !important; }
    </style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600&family=Inter:wght@400;900&display=swap');
        body { background: #020617; color: white; font-family: 'Inter', sans-serif; margin: 0; padding: 10px; overflow-x: hidden; }
        .teko { font-family: 'Teko', sans-serif; }
        .card-input { background: #1e293b; border-radius: 20px; padding: 15px; border: 1px solid #334155; margin-bottom: 15px; }
        select, input { background: #0f172a; border: 1px solid #475569; color: white; padding: 10px; width: 100%; border-radius: 10px; font-size: 15px; outline: none; appearance: none; }
        .btn-main { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); width: 100%; padding: 18px; border-radius: 15px; font-weight: 900; color: white; border: none; cursor: pointer; margin-top: 10px; }
        .res-card { background: #0f172a; border-radius: 15px; padding: 15px; border-left: 5px solid #3b82f6; margin-top: 12px; }
        .label-sm { font-size: 10px; color: #94a3b8; text-transform: uppercase; font-weight: 800; margin-bottom: 4px; display: block; }
        .league-btn { cursor: pointer; padding: 10px; border-radius: 8px; font-weight: 800; border: 1px solid #334155; text-align: center; font-size: 11px; background: #0f172a; }
        .league-active { background: #3b82f6; border-color: #3b82f6; color: white; box-shadow: 0 0 10px rgba(59, 130, 246, 0.4); }
        .grid-inputs { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 10px; padding-top: 10px; border-top: 1px solid #334155; }
        .advice-badge { display: inline-block; padding: 2px 8px; border-radius: 5px; font-size: 11px; font-weight: 900; margin-top: 5px; }
    </style>
</head>
<body>
    <div id="main-container">
        <div class="text-center pt-4 pb-4">
            <h1 class="text-5xl font-black teko italic leading-none tracking-tighter">PROBET <span class="text-blue-500">AI V4</span></h1>
            <p class="text-blue-400 font-bold text-[10px] uppercase tracking-widest italic">Elite Multi-League Analyst</p>
        </div>

        <div class="grid grid-cols-2 gap-2 mb-4">
            <div id="l135" class="league-btn league-active" onclick="changeL(135)">SERIE A</div>
            <div id="l39" class="league-btn" onclick="changeL(39)">PREMIER</div>
            <div id="l78" class="league-btn" onclick="changeL(78)">BUNDES</div>
            <div id="l140" class="league-btn" onclick="changeL(140)">LA LIGA</div>
        </div>

        <div class="card-input">
            <div class="space-y-4">
                <div><label class="label-sm">Home Team</label><select id="hTeam"></select></div>
                <div><label class="label-sm">Away Team</label><select id="aTeam"></select></div>
                <div id="refBox"><label class="label-sm text-yellow-500 italic">Arbitro (Serie A)</label><select id="refSel"></select></div>
            </div>

            <div class="grid-inputs">
                <div><label class="label-sm">Tiri Tot</label><input type="number" id="s_tt" step="0.5" value="23.5"></div>
                <div><label class="label-sm">Casa</label><input type="number" id="s_th" step="0.5" value="12.5"></div>
                <div><label class="label-sm">Ospite</label><input type="number" id="s_ta" step="0.5" value="10.5"></div>
            </div>

            <div class="grid-inputs">
                <div><label class="label-sm text-purple-400">Porta Tot</label><input type="number" id="s_pt" step="0.5" value="8.5"></div>
                <div><label class="label-sm text-purple-400">Casa</label><input type="number" id="s_ph" step="0.5" value="4.5"></div>
                <div><label class="label-sm text-purple-400">Ospite</label><input type="number" id="s_pa" step="0.5" value="3.5"></div>
            </div>

            <div class="grid-inputs" id="foulGrid">
                <div><label class="label-sm text-red-400">Falli Tot</label><input type="number" id="s_ft" step="0.5" value="24.5"></div>
                <div><label class="label-sm text-red-400">Casa</label><input type="number" id="s_fh" step="0.5" value="12.5"></div>
                <div><label class="label-sm text-red-400">Ospite</label><input type="number" id="s_fa" step="0.5" value="11.5"></div>
            </div>

            <div class="grid-inputs">
                <div><label class="label-sm text-cyan-400">Corner Tot</label><input type="number" id="s_ct" step="0.5" value="9.5"></div>
                <div><label class="label-sm text-cyan-400">Casa</label><input type="number" id="s_ch" step="0.5" value="5.5"></div>
                <div><label class="label-sm text-cyan-400">Ospite</label><input type="number" id="s_ca" step="0.5" value="4.5"></div>
            </div>

            <div class="grid-inputs">
                <div><label class="label-sm text-yellow-400">Gialli Tot</label><input type="number" id="s_gt" step="0.5" value="4.5"></div>
                <div><label class="label-sm text-yellow-400">Casa</label><input type="number" id="s_gh" step="0.5" value="2.5"></div>
                <div><label class="label-sm text-yellow-400">Ospite</label><input type="number" id="s_ga" step="0.5" value="2.5"></div>
            </div>

            <button onclick="startAnalisi()" class="btn-main teko text-2xl italic tracking-widest">GENERA ANALISI</button>
        </div>

        <div id="results" class="pb-10"></div>
    </div>

<script>
const KEY = "75e4107623c05bb4bca2ac8b78b28dca";
const BASE = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/";
let curL = 135, dbXG = [];

function resize() {
    const h = document.getElementById('main-container').scrollHeight + 30;
    window.parent.postMessage({type: 'streamlit:setFrameHeight', height: h}, '*');
}

function changeL(id) {
    curL = id;
    document.querySelectorAll('.league-btn').forEach(b => b.classList.remove('league-active'));
    document.getElementById('l'+id).classList.add('league-active');
    document.getElementById('refBox').style.display = (id==135)?'block':'none';
    document.getElementById('foulGrid').style.display = (id==135)?'grid':'none';
    load();
}

function load() {
    const files = {135:"DATABASE_AVANZATO_SERIEA_2025.csv", 39:"DATABASE_AVANZATO_PREMIER_2025.csv", 78:"DATABASE_AVANZATO_BUNDES_2025.csv", 140:"DATABASE_AVANZATO_LALIGA_2025.csv"};
    Papa.parse(BASE + files[curL], { download: true, header: true, complete: (r) => { dbXG = r.data; loadT(); } });
    if(curL==135) Papa.parse(BASE + "ARBITRI_SERIE_A%20-%20Foglio1.csv", { download: true, header: true, delimiter: ";", complete: (r) => {
        const s = document.getElementById('refSel'); s.innerHTML = '<option value="24.5">Scegli Arbitro...</option>';
        r.data.forEach(x => { let n = x.Arbitro || Object.values(x)[0]; let v = (x["Media Totale"]||"24.5").toString().replace(',','.'); if(n) s.add(new Option(n, v)); });
    }});
}

async function loadT() {
    const r = await fetch(`https://v3.football.api-sports.io/teams?league=${curL}&season=2024`, {headers:{"x-apisports-key":KEY}});
    const d = await r.json();
    const h = document.getElementById('hTeam'), a = document.getElementById('aTeam');
    h.innerHTML = ""; a.innerHTML = "";
    // Filtro stretto: carichiamo solo le squadre che appartengono realmente alla lega scelta per evitare Serie B
    d.response.sort((x,y)=>x.team.name.localeCompare(y.team.name)).forEach(t => {
        h.add(new Option(t.team.name, t.team.id)); a.add(new Option(t.team.name, t.team.id));
    });
    setTimeout(resize, 400);
}

function getBadge(val, id) {
    const s = parseFloat(document.getElementById(id).value);
    const p = Math.min(Math.max(50 + (val-s)*9, 5), 98);
    return `<br><span class="advice-badge ${val>=s?'bg-emerald-500':'bg-red-500'}">${val>=s?'OVER':'UNDER'} ${s} (${(val>=s?p:100-p).toFixed(1)}%)</span>`;
}

async function startAnalisi() {
    const out = document.getElementById('results');
    out.innerHTML = "<div class='text-center py-10 teko text-2xl animate-pulse text-blue-500'>ANALISI IN CORSO...</div>";
    resize();

    try {
        const idH = document.getElementById('hTeam').value, idA = document.getElementById('aTeam').value;
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${curL}&season=2024&team=${idH}`, {headers:{"x-apisports-key":KEY}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${curL}&season=2024&team=${idA}`, {headers:{"x-apisports-key":KEY}}).then(r=>r.json())
        ]);

        const sH = rH.response, sA = rA.response;
        const xG = parseFloat((dbXG.find(x=>x.TeamID==idH)?.xG_Per_Shot || "0.11").toString().replace(',','.'));
        const m = xG / 0.11;

        const tt = (sH.shots.total.average + sA.shots.total.average) * m;
        const pt = (sH.shots.on_goal.average + sA.shots.on_goal.average) * m;
        const ct = (sH.corners.for.average + sA.corners.for.average);
        const gt = (sH.cards.yellow.average || 2) + (sA.cards.yellow.average || 2.2);

        let h = `<div class="res-card"><div>TIRI TOTALI</div><div class="text-4xl font-black teko">${tt.toFixed(2)} ${getBadge(tt, 's_tt')}</div></div>`;
        h += `<div class="res-card border-l-purple-500"><div>IN PORTA</div><div class="text-4xl font-black teko">${pt.toFixed(2)} ${getBadge(pt, 's_pt')}</div></div>`;
        
        if(curL==135) {
            const ref = parseFloat(document.getElementById('refSel').value);
            const ft = (sH.fouls.for.average + sA.fouls.for.average) * 0.7 + (ref * 0.3);
            h += `<div class="res-card border-l-red-500"><div>FALLI</div><div class="text-4xl font-black teko">${ft.toFixed(2)} ${getBadge(ft, 's_ft')}</div></div>`;
        }

        h += `<div class="res-card border-l-cyan-500"><div>CORNER</div><div class="text-4xl font-black teko">${ct.toFixed(2)} ${getBadge(ct, 's_ct')}</div></div>`;
        h += `<div class="res-card border-l-yellow-500"><div>GIALLI</div><div class="text-4xl font-black teko">${gt.toFixed(2)} ${getBadge(gt, 's_gt')}</div></div>`;

        out.innerHTML = h;
        setTimeout(resize, 300);
    } catch(e) { out.innerHTML = "<div class='text-red-500'>Errore caricamento dati API</div>"; }
}
load();
</script>
</body>
</html>
"""

components.html(html_code, height=1500, scrolling=False)
