import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json

st.set_page_config(page_title="PROBET AI V4 - HYBRID ELITE", layout="wide")

# Caricamento dati dai tuoi file CSV caricati
try:
    # Carichiamo i file usando i nomi esatti forniti
    df_arbitri = pd.read_csv('ARBITRI_SERIE_A - Foglio1.csv', sep=';')
    df_falli_curr = pd.read_csv('FALLI_CURR_SERIE_A - Foglio1.csv', sep=';')
    df_falli_prev = pd.read_csv('FALLI_PREV_SERIE_A - DATI STAGIONE 2024_2025 .csv')
except Exception as e:
    st.error(f"Errore nel caricamento dei file CSV: {e}")

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
        select, input { background: #0f172a; border: 1px solid #475569; color: white; padding: 10px; width: 100%; border-radius: 10px; font-weight: bold; outline: none; font-size: 13px;}
        .label-sm { font-size: 10px; font-weight: 900; color: #94a3b8; text-transform: uppercase; margin-bottom: 4px; display: block; }
        .btn-analizza { background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); width: 100%; padding: 18px; border-radius: 12px; font-weight: 900; text-transform: uppercase; cursor: pointer; border: none; color: white; }
        .res-box { background: #0f172a; border-radius: 15px; padding: 15px; border-left: 4px solid #3b82f6; margin-bottom: 15px; }
        .tag { padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: 900; margin-left: 5px; vertical-align: middle; }
        .over { background: #10b981; color: #020617; }
        .under { background: #ef4444; color: white; }
        .grid-res { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; }
    </style>
</head>
<body class="p-4">
    <div class="max-w-6xl mx-auto">
        <div class="text-center mb-8">
            <h1 class="text-5xl font-black teko tracking-widest italic uppercase text-white">PROBET <span class="text-blue-500">AI V4 HYBRID</span></h1>
            <p class="text-[10px] font-bold text-slate-500 tracking-[0.5em] uppercase">Serie A Discipline & Stats Integration</p>
        </div>

        <div class="card-premium">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div><label class="label-sm text-blue-400">Home Team (Casa)</label><select id="hT"></select></div>
                <div><label class="label-sm text-blue-400">Away Team (Ospite)</label><select id="aT"></select></div>
                <div><label class="label-sm text-red-400">Arbitro (Dati Manuali)</label><select id="refS"></select></div>
            </div>

            <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
                <div><label class="label-sm">Spread Tiri</label><input type="number" id="sTiri" step="0.5" value="23.5"></div>
                <div><label class="label-sm">Spread Porta</label><input type="number" id="sPorta" step="0.5" value="8.5"></div>
                <div><label class="label-sm text-red-400">Spread Falli</label><input type="number" id="sFalli" step="0.5" value="24.5"></div>
                <div><label class="label-sm text-yellow-400">Spread Gialli</label><input type="number" id="sGialli" step="0.5" value="4.5"></div>
                <div><label class="label-sm text-emerald-400">Spread Angoli</label><input type="number" id="sCorners" step="0.5" value="9.5"></div>
            </div>
            
            <button onclick="runAnalysis()" class="btn-analizza teko text-2xl tracking-widest mt-6">GENERA PREVISIONE IBRIDA</button>
        </div>

        <div id="results" class="hidden pb-20"></div>
    </div>

<script>
const K = "aa5e53f893088010cc7c47af17f306e9";
const CSV_XG = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/DATABASE_AVANZATO_SERIEA_2025.csv";

// Dati passati da Python (CSV dell'utente)
const dataRef = """ + df_arbitri.to_json(orient='records') + """;
const dataFcurr = """ + df_falli_curr.to_json(orient='records') + """;
const dataFprev = """ + df_falli_prev.to_json(orient='records') + """;

let dbXG = [];

async function init() {
    // Carica database xG
    Papa.parse(CSV_XG, { download: true, header: true, complete: r => dbXG = r.data });
    
    // Carica Squadre da API
    const res = await fetch(`https://v3.football.api-sports.io/teams?league=135&season=2025`, {headers:{"x-apisports-key":K}});
    const d = await res.json();
    const h = document.getElementById('hT'), a = document.getElementById('aT');
    
    d.response.sort((x,y)=>x.team.name.localeCompare(y.team.name)).forEach(t => {
        h.add(new Option(t.team.name, t.team.id));
        a.add(new Option(t.team.name, t.team.id));
    });

    // Popola Arbitri dal CSV manuale
    const rs = document.getElementById('refS');
    JSON.parse(dataRef).forEach(r => rs.add(new Option(r.Arbitro, r.Arbitro)));
}

function getTag(pred, spr) {
    const diff = pred - spr;
    const p = Math.min(Math.max(50 + (diff * 9), 5), 98);
    return `<span class="tag ${p>=50?'over':'under'}">${p>=50?'OVER':'UNDER'} ${spr} (${(p>=50?p:100-p).toFixed(1)}%)</span>`;
}

async function runAnalysis() {
    const idH = document.getElementById('hT').value, idA = document.getElementById('aT').value;
    const nameH = document.getElementById('hT').options[document.getElementById('hT').selectedIndex].text;
    const nameA = document.getElementById('aT').options[document.getElementById('aT').selectedIndex].text;
    const refN = document.getElementById('refS').value;
    
    const resDiv = document.getElementById('results');
    resDiv.innerHTML = "<p class='text-center py-10 teko text-3xl animate-pulse text-blue-500 uppercase'>Sincronizzazione dati in corso...</p>";
    resDiv.classList.remove('hidden');

    try {
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${idH}`, {headers:{"x-apisports-key":K}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${idA}`, {headers:{"x-apisports-key":K}}).then(r=>r.json())
        ]);

        // --- 1. LOGICA TIRI (API + CSV xG) ---
        const xGH = parseFloat(dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || 0.11);
        const xGA = parseFloat(dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || 0.11);
        const predTiri = ((rH.response.shots.total.average || 12) + (rA.response.shots.total.average || 11)) * ((xGH+xGA)/0.22);
        const predPorta = ((rH.response.shots.on_goal.average || 4) + (rA.response.shots.on_goal.average || 3.5)) * ((xGH+xGA)/0.22);

        // --- 2. LOGICA FALLI (100% CSV MANUALE) ---
        // Troviamo dati Casa e Ospite nei file (confronto nomi squadra)
        const fCurrH = JSON.parse(dataFcurr).find(x => x.Squadra === nameH && x[""] === "Casa") || {Falli_Commessi: "12", Falli_Subiti: "12"};
        const fCurrA = JSON.parse(dataFcurr).find(x => x.Squadra === nameA && x[""] === "Fuori") || {Falli_Commessi: "12", Falli_Subiti: "12"};
        const fPrevH = JSON.parse(dataFprev).find(x => x.Squadra === nameH && x[""] === "Casa") || {Falli_Commessi: "12", Falli_Subiti: "12"};
        const fPrevA = JSON.parse(dataFprev).find(x => x.Squadra === nameA && x[""] === "Fuori") || {Falli_Commessi: "12", Falli_Subiti: "12"};
        const rObj = JSON.parse(dataRef).find(x => x.Arbitro === refN);

        const comm_H = (parseFloat(fCurrH.Falli_Commessi.replace(',','.')) * 0.7) + (parseFloat(fPrevH.Falli_Commessi.replace(',','.')) * 0.3);
        const sub_A = (parseFloat(fCurrA.Falli_Subiti.replace(',','.')) * 0.7) + (parseFloat(fPrevA.Falli_Subiti.replace(',','.')) * 0.3);
        const comm_A = (parseFloat(fCurrA.Falli_Commessi.replace(',','.')) * 0.7) + (parseFloat(fPrevA.Falli_Commessi.replace(',','.')) * 0.3);
        const sub_H = (parseFloat(fCurrH.Falli_Subiti.replace(',','.')) * 0.7) + (parseFloat(fPrevH.Falli_Subiti.replace(',','.')) * 0.3);
        
        const mFalliRef = parseFloat(rObj["Media Totale"].toString().replace(',','.'));
        const predFalli = ((comm_H + sub_A + comm_A + sub_H) / 2 * 0.6) + (mFalliRef * 0.4);

        // --- 3. CARTELLINI & ANGOLI (100% API) ---
        const predGialli = (parseFloat(rH.response.cards.yellow.average) || 2.2) + (parseFloat(rA.response.cards.yellow.average) || 2.2);
        // Formula per angoli basata su attacco API
        const predCorners = (parseFloat(rH.response.goals.for.average) + parseFloat(rA.response.goals.for.average)) * 2.8 + 1.5;

        resDiv.innerHTML = `
            <div class="grid-res">
                <div class="res-box border-l-blue-500">
                    <p class="label-sm">Volume di Tiro (API + xG Qualità)</p>
                    <div class="text-3xl font-bold teko">MATCH: ${predTiri.toFixed(2)} ${getTag(predTiri, document.getElementById('sTiri').value)}</div>
                    <div class="text-3xl font-bold teko text-blue-400">PORTA: ${predPorta.toFixed(2)} ${getTag(predPorta, document.getElementById('sPorta').value)}</div>
                </div>

                <div class="res-box border-l-red-500">
                    <p class="label-sm">Falli (CSV Manuale - Arbitro: ${refN})</p>
                    <div class="text-5xl font-bold teko text-red-500">${predFalli.toFixed(2)}</div>
                    <div class="mt-2">${getTag(predFalli, document.getElementById('sFalli').value)}</div>
                </div>

                <div class="res-box border-l-yellow-500">
                    <p class="label-sm">Cartellini Gialli (Dati API)</p>
                    <div class="text-5xl font-bold teko text-yellow-500">${predGialli.toFixed(2)}</div>
                    <div class="mt-2">${getTag(predGialli, document.getElementById('sGialli').value)}</div>
                </div>

                <div class="res-box border-l-emerald-500">
                    <p class="label-sm">Calci d'Angolo (Dati API)</p>
                    <div class="text-5xl font-bold teko text-emerald-500">${predCorners.toFixed(2)}</div>
                    <div class="mt-2">${getTag(predCorners, document.getElementById('sCorners').value)}</div>
                </div>
            </div>
            <p class="text-[10px] text-slate-500 mt-4 text-center uppercase font-bold tracking-widest">Incrocio dati: API-Sports + Database Personale (Falli 24/25/26 - Arbitri - xG)</p>
        `;
    } catch(e) { 
        console.error(e); 
        resDiv.innerHTML = "<div class='card-premium text-red-500'>Errore durante l'analisi. Controlla la console o la correttezza dei nomi nei CSV.</div>"; 
    }
}

// Avvio
init();
</script>
</body>
</html>
"""
components.html(html_code, height=1000, scrolling=True)
