import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

st.set_page_config(page_title="PROBET AI V4 - HYBRID ELITE", layout="wide")

# Caricamento dati Arbitri dal Server (CSV caricato)
try:
    # Puliamo subito i nomi delle colonne per evitare errori di spazi
    df_arbitri = pd.read_csv('ARBITRI_SERIE_A - Foglio1.csv', sep=';')
    df_arbitri.columns = df_arbitri.columns.str.strip()
    # Trasformiamo in JSON per passarlo al Javascript
    arbitri_json = df_arbitri.to_json(orient='records')
except Exception as e:
    st.error(f"Errore caricamento file arbitri: {e}")
    arbitri_json = "[]"

html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600&family=Inter:wght@400;900&display=swap');
        body {{ background: #020617; color: white; font-family: 'Inter', sans-serif; }}
        .teko {{ font-family: 'Teko', sans-serif; }}
        .card-premium {{ background: #1e293b; border-radius: 24px; padding: 30px; border: 1px solid #334155; }}
        select, input {{ background: #0f172a; border: 1px solid #475569; color: white; padding: 12px; width: 100%; border-radius: 12px; font-weight: bold; outline: none; }}
        .btn-analizza {{ background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); width: 100%; padding: 20px; border-radius: 15px; font-weight: 900; text-transform: uppercase; cursor: pointer; border: none; color: white; }}
        .res-box {{ background: #0f172a; border-radius: 20px; padding: 20px; border-left: 5px solid #3b82f6; }}
        .advice-tag {{ padding: 2px 10px; border-radius: 6px; font-size: 12px; font-weight: 900; margin-left: 10px; vertical-align: middle; }}
        .over-tag {{ background: #10b981; color: #020617; }}
        .under-tag {{ background: #ef4444; color: white; }}
        .label-spread {{ font-size: 10px; font-weight: 900; color: #94a3b8; text-transform: uppercase; margin-bottom: 5px; display: block; }}
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-4xl mx-auto">
        <div class="text-center mb-10">
            <h1 class="text-6xl font-black teko tracking-widest text-white uppercase italic">PROBET <span class="text-blue-500">AI V4</span></h1>
            <p class="text-[10px] font-bold text-slate-500 tracking-[0.5em] uppercase">Arbitro & xG Integrated • Season 2025</p>
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
                    <label class="label-spread text-yellow-400">Arbitro (da CSV)</label>
                    <select id="arbitroSelect"></select>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 pt-4 border-t border-slate-700">
                <div>
                    <label class="label-spread text-emerald-400">Spread Falli Match</label>
                    <input type="number" id="sprFouls" step="0.5" value="24.5">
                </div>
                <div>
                    <label class="label-spread text-blue-400">Spread Tiri Match</label>
                    <input type="number" id="sprShots" step="0.5" value="23.5">
                </div>
                <div>
                    <label class="label-spread text-purple-400">Spread Porta Match</label>
                    <input type="number" id="sprOnGoal" step="0.5" value="8.5">
                </div>
            </div>

            <button onclick="runDeepAnalysis()" class="btn-analizza shadow-xl italic teko text-2xl tracking-widest">GENERA ANALISI INTEGRATA</button>
        </div>

        <div id="results" class="space-y-6 hidden pb-20"></div>
    </div>

<script>
const API_KEY = "75e4107623c05bb4bca2ac8b78b28dca";
const CSV_XG = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/DATABASE_AVANZATO_SERIEA_2025.csv";
const dataArbitri = {arbitri_json};

let dbXG = [];

async function init() {{
    // 1. Carica xG da GitHub
    Papa.parse(CSV_XG, {{
        download: true, header: true, complete: function(r) {{ dbXG = r.data; loadTeams(); }}
    }});

    // 2. Carica Arbitri nel Select
    const aSel = document.getElementById('arbitroSelect');
    dataArbitri.forEach(a => {{
        if(a.Arbitro) aSel.add(new Option(a.Arbitro, a["Media Totale"]));
    }});
}}

async function loadTeams() {{
    const res = await fetch(`https://v3.football.api-sports.io/teams?league=135&season=2025`, {{ headers: {{ "x-apisports-key": API_KEY }} }});
    const data = await res.json();
    const h = document.getElementById('homeTeam'), a = document.getElementById('awayTeam');
    data.response.sort((x,y) => x.team.name.localeCompare(y.team.name)).forEach(t => {{
        h.add(new Option(t.team.name, t.team.id)); a.add(new Option(t.team.name, t.team.id));
    }});
}}

function getAdvice(pred, spr) {{
    const p = (50 + (pred - spr) * 9).toFixed(1);
    const label = p >= 50 ? "OVER" : "UNDER";
    const css = p >= 50 ? "over-tag" : "under-tag";
    return `<span class="advice-tag ${{css}}">${{label}} ${{spr}} (${{p>=50?p:100-p}}%)</span>`;
}}

async function runDeepAnalysis() {{
    const idH = document.getElementById('homeTeam').value, idA = document.getElementById('awayTeam').value;
    const mediaArbitro = parseFloat(document.getElementById('arbitroSelect').value) || 24;
    const resDiv = document.getElementById('results');
    resDiv.innerHTML = "<div class='text-center py-20 teko text-3xl animate-pulse text-blue-500'>CALCOLO IBRIDO IN CORSO...</div>";
    resDiv.classList.remove('hidden');

    try {{
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${{idH}}`, {{headers:{{"x-apisports-key":API_KEY}}}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${{idA}}`, {{headers:{{"x-apisports-key":API_KEY}}}}).then(r=>r.json())
        ]);

        const sH = rH.response; const sA = rA.response;
        const xGH = parseFloat(dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || 0.11);
        const xGA = parseFloat(dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || 0.11);

        // 1. CALCOLO FALLI (API + MEDIA ARBITRO CSV)
        const fCommH = sH.fouls.for.average || 12;
        const fSubH = sH.fouls.against.average || 12;
        const fCommA = sA.fouls.for.average || 12;
        const fSubA = sA.fouls.against.average || 12;
        
        // Peso: 60% statistiche squadre, 40% tendenza arbitro
        const predFalli = (((fCommH + fSubA) / 2) + ((fCommA + fSubH) / 2)) * 0.6 + (mediaArbitro * 0.4);

        // 2. CALCOLO TIRI (API + xG)
        const pTiri = ((sH.shots.total.average + sA.shots.total.average)) * (xGH + xGA) / 0.22;
        const pPorta = ((sH.shots.on_goal.average + sA.shots.on_goal.average)) * (xGH + xGA) / 0.22;

        resDiv.innerHTML = `
            <div class="res-box border-l-red-500">
                <p class="label-spread">Previsione Falli (Teams 60% + Arbitro 40%)</p>
                <h2 class="text-6xl font-black teko text-white inline-block">${{predFalli.toFixed(2)}}</h2>
                ${{getAdvice(predFalli, document.getElementById('sprFouls').value)}}
            </div>

            <div class="res-box border-l-blue-500">
                <p class="label-spread">Previsione Tiri Match (Quality Adjusted)</p>
                <h2 class="text-6xl font-black teko text-white inline-block">${{pTiri.toFixed(2)}}</h2>
                ${{getAdvice(pTiri, document.getElementById('sprShots').value)}}
            </div>

            <div class="res-box border-l-purple-500">
                <p class="label-spread">Previsione In Porta Match</p>
                <h2 class="text-6xl font-black teko text-white inline-block">${{pPorta.toFixed(2)}}</h2>
                ${{getAdvice(pPorta, document.getElementById('sprOnGoal').value)}}
            </div>
        `;
    }} catch(e) {{ console.error(e); }}
}}
init();
</script>
</body>
</html>
"""
components.html(html_code, height=1000, scrolling=True)
