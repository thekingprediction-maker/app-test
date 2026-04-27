import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json

st.set_page_config(page_title="PROBET AI V4 - FIX", layout="wide")

# Caricamento dati dai tuoi file CSV
try:
    # Specifichiamo i separatori corretti per i tuoi file
    df_arbitri = pd.read_csv('ARBITRI_SERIE_A - Foglio1.csv', sep=';')
    df_falli_curr = pd.read_csv('FALLI_CURR_SERIE_A - Foglio1.csv', sep=';')
    df_falli_prev = pd.read_csv('FALLI_PREV_SERIE_A - DATI STAGIONE 2024_2025 .csv', sep=',')
except Exception as e:
    st.error(f"Errore caricamento CSV: {e}")

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
        .card-premium { background: #1e293b; border-radius: 20px; padding: 25px; border: 1px solid #334155; margin-bottom: 20px; }
        select, input { background: #0f172a; border: 1px solid #475569; color: white; padding: 10px; width: 100%; border-radius: 10px; font-weight: bold; outline: none; }
        .label-sm { font-size: 10px; font-weight: 900; color: #94a3b8; text-transform: uppercase; margin-bottom: 4px; display: block; }
        .btn-analizza { background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); width: 100%; padding: 18px; border-radius: 12px; font-weight: 900; text-transform: uppercase; cursor: pointer; border: none; color: white; }
        .res-box { background: #0f172a; border-radius: 15px; padding: 15px; border-left: 4px solid #3b82f6; margin-bottom: 15px; }
        .tag { padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: 900; margin-left: 5px; }
        .over { background: #10b981; color: #020617; }
        .under { background: #ef4444; color: white; }
    </style>
</head>
<body class="p-4">
    <div class="max-w-6xl mx-auto">
        <div class="text-center mb-8">
            <h1 class="text-5xl font-black teko italic uppercase text-white tracking-widest">PROBET <span class="text-blue-500">AI V4 FIXED</span></h1>
        </div>

        <div class="card-premium">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div><label class="label-sm text-blue-400">Home Team</label><select id="hT"></select></div>
                <div><label class="label-sm text-blue-400">Away Team</label><select id="aT"></select></div>
                <div><label class="label-sm text-red-400">Arbitro</label><select id="refS"></select></div>
            </div>

            <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
                <div><label class="label-sm">Spread Tiri</label><input type="number" id="sTiri" step="0.5" value="23.5"></div>
                <div><label class="label-sm">Spread Porta</label><input type="number" id="sPorta" step="0.5" value="8.5"></div>
                <div><label class="label-sm text-red-400">Spread Falli</label><input type="number" id="sFalli" step="0.5" value="24.5"></div>
                <div><label class="label-sm text-yellow-400">Spread Gialli</label><input type="number" id="sGialli" step="0.5" value="4.5"></div>
                <div><label class="label-sm text-emerald-400">Spread Angoli</label><input type="number" id="sCorners" step="0.5" value="9.5"></div>
            </div>
            
            <button onclick="runAnalysis()" class="btn-analizza teko text-2xl tracking-widest mt-6 italic">ANALIZZA PARTITA</button>
        </div>

        <div id="results" class="hidden"></div>
    </div>

<script>
const K = "aa5e53f893088010cc7c47af17f306e9";
const CSV_XG = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/DATABASE_AVANZATO_SERIEA_2025.csv";

const dataRef = """ + df_arbitri.to_json(orient='records') + """;
const dataFcurr = """ + df_falli_curr.to_json(orient='records') + """;
const dataFprev = """ + df_falli_prev.to_json(orient='records') + """;

let dbXG = [];

// Helper per pulire i numeri con la virgola (es: "10,9" -> 10.9)
const cleanN = (val) => {
    if (!val) return 0;
    return parseFloat(val.toString().replace(',', '.'));
};

async function init() {
    Papa.parse(CSV_XG, { download: true, header: true, complete: r => dbXG = r.data });
    const res = await fetch(`https://v3.football.api-sports.io/teams?league=135&season=2025`, {headers:{"x-apisports-key":K}});
    const d = await res.json();
    const h = document.getElementById('hT'), a = document.getElementById('aT');
    d.response.sort((x,y)=>x.team.name.localeCompare(y.team.name)).forEach(t => {
        h.add(new Option(t.team.name, t.team.id)); a.add(new Option(t.team.name, t.team.id));
    });
    const rs = document.getElementById('refS');
    JSON.parse(dataRef).forEach(r => rs.add(new Option(r.Arbitro, r.Arbitro)));
}

function getTag(pred, spr) {
    const diff = pred - spr;
    const p = Math.min(Math.max(50 + (diff * 8.5), 5), 98);
    return `<span class="tag ${p>=50?'over':'under'}">${p>=50?'OVER':'UNDER'} ${spr} (${(p>=50?p:100-p).toFixed(1)}%)</span>`;
}

async function runAnalysis() {
    const idH = document.getElementById('hT').value, idA = document.getElementById('aT').value;
    const nameH = document.getElementById('hT').options[document.getElementById('hT').selectedIndex].text;
    const nameA = document.getElementById('aT').options[document.getElementById('aT').selectedIndex].text;
    const refN = document.getElementById('refS').value;
    const resDiv = document.getElementById('results');

    resDiv.innerHTML = "<p class='text-center py-10 teko text-2xl animate-pulse'>CALCOLO IN CORSO...</p>";
    resDiv.classList.remove('hidden');

    try {
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${idH}`, {headers:{"x-apisports-key":K}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${idA}`, {headers:{"x-apisports-key":K}}).then(r=>r.json())
        ]);

        // 1. TIRI
        const xGH = cleanN(dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || 0.11);
        const xGA = cleanN(dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || 0.11);
        const pT = ((rH.response.shots.total.average || 12) + (rA.response.shots.total.average || 11)) * ((xGH+xGA)/0.22);
        const pP = ((rH.response.shots.on_goal.average || 4) + (rA.response.shots.on_goal.average || 3.5)) * ((xGH+xGA)/0.22);

        // 2. FALLI (Logica Robusta sui nomi)
        const fCH = JSON.parse(dataFcurr).find(x => x.Squadra === nameH && x.Unnamed_2 === "Casa") || {Falli_Commessi: "12", Falli_Subiti: "12"};
        const fCA = JSON.parse(dataFcurr).find(x => x.Squadra === nameA && x.Unnamed_2 === "Fuori") || {Falli_Commessi: "12", Falli_Subiti: "12"};
        const fPH = JSON.parse(dataFprev).find(x => x.Squadra === nameH && x.Unnamed_2 === "Casa") || {Falli_Commessi: "12", Falli_Subiti: "12"};
        const fPA = JSON.parse(dataFprev).find(x => x.Squadra === nameA && x.Unnamed_2 === "Fuori") || {Falli_Commessi: "12", Falli_Subiti: "12"};
        const rO = JSON.parse(dataRef).find(x => x.Arbitro === refN);

        const commH = (cleanN(fCH.Falli_Commessi) * 0.7) + (cleanN(fPH.Falli_Commessi) * 0.3);
        const subA = (cleanN(fCA.Falli_Subiti) * 0.7) + (cleanN(fPA.Falli_Subiti) * 0.3);
        const commA = (cleanN(fCA.Falli_Commessi) * 0.7) + (cleanN(fPA.Falli_Commessi) * 0.3);
        const subH = (cleanN(fCH.Falli_Subiti) * 0.7) + (cleanN(fPH.Falli_Subiti) * 0.3);
        
        const mFalliRef = cleanN(rO["Media Totale"]);
        const pFalli = ((commH + subA + commA + subH) / 2 * 0.6) + (mFalliRef * 0.4);

        // 3. API DATA
        const pGialli = (parseFloat(rH.response.cards.yellow.average) || 2.2) + (parseFloat(rA.response.cards.yellow.average) || 2.2);
        const pCorners = (parseFloat(rH.response.goals.for.average) + parseFloat(rA.response.goals.for.average)) * 2.8 + 1.5;

        resDiv.innerHTML = `
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="res-box">
                    <p class="label-sm">Tiri Totali & Porta</p>
                    <div class="text-3xl font-bold teko">TIRI: ${pT.toFixed(2)} ${getTag(pT, document.getElementById('sTiri').value)}</div>
                    <div class="text-3xl font-bold teko text-blue-400">PORTA: ${pP.toFixed(2)} ${getTag(pP, document.getElementById('sPorta').value)}</div>
                </div>
                <div class="res-box border-l-red-500">
                    <p class="label-sm">Falli (CSV + Arbitro: ${refN})</p>
                    <div class="text-5xl font-bold teko text-red-500">${pFalli.toFixed(2)}</div>
                    <div class="mt-1">${getTag(pFalli, document.getElementById('sFalli').value)}</div>
                </div>
                <div class="res-box border-l-yellow-500">
                    <p class="label-sm">Cartellini (API)</p>
                    <div class="text-4xl font-bold teko text-yellow-500">${pGialli.toFixed(2)} ${getTag(pGialli, document.getElementById('sGialli').value)}</div>
                </div>
                <div class="res-box border-l-emerald-500">
                    <p class="label-sm">Angoli (API)</p>
                    <div class="text-4xl font-bold teko text-emerald-500">${pCorners.toFixed(2)} ${getTag(pCorners, document.getElementById('sCorners').value)}</div>
                </div>
            </div>
        `;
    } catch(e) { 
        resDiv.innerHTML = "<div class='p-4 bg-red-900/50 rounded-xl'>Errore: " + e.message + "</div>"; 
    }
}
init();
</script>
</body>
</html>
"""
components.html(html_code, height=900, scrolling=True)
