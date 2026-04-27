import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

st.set_page_config(page_title="PROBET AI V4 - SERIE A", layout="wide")

# Caricamento robusto
try:
    # Carichiamo i file forzando le stringhe per evitare errori di virgole
    df_arbitri = pd.read_csv('ARBITRI_SERIE_A - Foglio1.csv', sep=';', dtype=str)
    df_falli_curr = pd.read_csv('FALLI_CURR_SERIE_A - Foglio1.csv', sep=';', dtype=str)
    df_falli_prev = pd.read_csv('FALLI_PREV_SERIE_A - DATI STAGIONE 2024_2025 .csv', sep=',', dtype=str)
    
    # Pulizia nomi colonne per evitare spazi bianchi invisibili
    df_falli_curr.columns = df_falli_curr.columns.str.strip()
    df_falli_prev.columns = df_falli_prev.columns.str.strip()
except Exception as e:
    st.error(f"Errore caricamento file: {e}")

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
        .card-premium {{ background: #1e293b; border-radius: 20px; padding: 25px; border: 1px solid #334155; margin-bottom: 20px; }}
        select, input {{ background: #0f172a; border: 1px solid #475569; color: white; padding: 10px; width: 100%; border-radius: 10px; font-weight: bold; outline: none; }}
        .label-sm {{ font-size: 10px; font-weight: 900; color: #3b82f6; text-transform: uppercase; margin-bottom: 4px; display: block; }}
        .btn-analizza {{ background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); width: 100%; padding: 18px; border-radius: 12px; font-weight: 900; text-transform: uppercase; cursor: pointer; border: none; color: white; }}
        .res-box {{ background: #0f172a; border-radius: 15px; padding: 15px; border-left: 4px solid #3b82f6; margin-bottom: 15px; }}
        .tag {{ padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: 900; margin-left: 5px; }}
        .over {{ background: #10b981; color: #020617; }}
        .under {{ background: #ef4444; color: white; }}
    </style>
</head>
<body class="p-4">
    <div class="max-w-6xl mx-auto">
        <div class="card-premium">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div><label class="label-sm">Home Team</label><select id="hT"></select></div>
                <div><label class="label-sm">Away Team</label><select id="aT"></select></div>
                <div><label class="label-sm">Arbitro</label><select id="refS"></select></div>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
                <div><label class="label-sm">Spread Tiri</label><input type="number" id="sTiri" step="0.5" value="23.5"></div>
                <div><label class="label-sm">Spread Porta</label><input type="number" id="sPorta" step="0.5" value="8.5"></div>
                <div><label class="label-sm">Spread Falli</label><input type="number" id="sFalli" step="0.5" value="24.5"></div>
                <div><label class="label-sm">Spread Gialli</label><input type="number" id="sGialli" step="0.5" value="4.5"></div>
                <div><label class="label-sm">Spread Angoli</label><input type="number" id="sCorners" step="0.5" value="9.5"></div>
            </div>
            <button onclick="runAnalysis()" class="btn-analizza teko text-2xl tracking-widest mt-6 italic">AVVIA ANALISI</button>
        </div>
        <div id="results" class="hidden"></div>
    </div>

<script>
const K = "aa5e53f893088010cc7c47af17f306e9";
const CSV_XG = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/DATABASE_AVANZATO_SERIEA_2025.csv";

const dRef = {df_arbitri.to_json(orient='records')};
const dFc = {df_falli_curr.to_json(orient='records')};
const dFp = {df_falli_prev.to_json(orient='records')};

let dbXG = [];

const clean = (v) => {{
    if (!v) return 0;
    return parseFloat(v.toString().replace(',', '.')) || 0;
}};

// Funzione di ricerca flessibile
const findTeam = (db, name, pos) => {{
    const n = name.toLowerCase().trim();
    return db.find(x => {{
        const csvName = (x.Squadra || "").toLowerCase().trim();
        const csvPos = Object.values(x).join("|");
        return (n.includes(csvName) || csvName.includes(n)) && csvPos.includes(pos);
    }}) || {{}};
}};

async function init() {{
    Papa.parse(CSV_XG, {{ download: true, header: true, complete: r => dbXG = r.data }});
    const res = await fetch(`https://v3.football.api-sports.io/teams?league=135&season=2025`, {{headers:{{"x-apisports-key":K}}}});
    const d = await res.json();
    const h = document.getElementById('hT'), a = document.getElementById('aT');
    d.response.sort((x,y)=>x.team.name.localeCompare(y.team.name)).forEach(t => {{
        h.add(new Option(t.team.name, t.team.id)); a.add(new Option(t.team.name, t.team.id));
    }});
    const rs = document.getElementById('refS');
    dRef.forEach(r => rs.add(new Option(r.Arbitro, r.Arbitro)));
}}

function getTag(pred, spr) {{
    const diff = pred - spr;
    const p = Math.min(Math.max(50 + (diff * 8.5), 5), 98);
    return `<span class="tag ${{p>=50?'over':'under'}}">${{p>=50?'OVER':'UNDER'}} ${{spr}} (${{(p>=50?p:100-p).toFixed(1)}}%)</span>`;
}}

async function runAnalysis() {{
    const idH = document.getElementById('hT').value, idA = document.getElementById('aT').value;
    const nH = document.getElementById('hT').options[document.getElementById('hT').selectedIndex].text;
    const nA = document.getElementById('aT').options[document.getElementById('aT').selectedIndex].text;
    const refN = document.getElementById('refS').value;
    const resDiv = document.getElementById('results');

    resDiv.innerHTML = "<p class='text-center py-10 teko text-2xl animate-pulse'>ELABORAZIONE IBRIDA...</p>";
    resDiv.classList.remove('hidden');

    try {{
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${{idH}}`, {{headers:{{"x-apisports-key":K}}}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${{idA}}`, {{headers:{{"x-apisports-key":K}}}}).then(r=>r.json())
        ]);

        // 1. TIRI (API + CSV)
        const xGH = clean(dbXG.find(x => nH.includes(x.TeamName))?.xG_Per_Shot || 0.11);
        const xGA = clean(dbXG.find(x => nA.includes(x.TeamName))?.xG_Per_Shot || 0.11);
        const pT = ((rH.response.shots.total.average || 12) + (rA.response.shots.total.average || 11)) * ((xGH+xGA)/0.22);
        const pP = ((rH.response.shots.on_goal.average || 4) + (rA.response.shots.on_goal.average || 3.5)) * ((xGH+xGA)/0.22);

        // 2. FALLI (DATI TUOI CSV)
        const fCH = findTeam(dFc, nH, "Casa");
        const fCA = findTeam(dFc, nA, "Fuori");
        const fPH = findTeam(dFp, nH, "Casa");
        const fPA = findTeam(dFp, nA, "Fuori");
        const rO = dRef.find(x => x.Arbitro === refN);

        const commH = (clean(fCH["Falli Commessi"]) * 0.7) + (clean(fPH["Falli Commessi"]) * 0.3) || 12;
        const subA = (clean(fCA["Falli Subiti"]) * 0.7) + (clean(fPA["Falli Subiti"]) * 0.3) || 12;
        const commA = (clean(fCA["Falli Commessi"]) * 0.7) + (clean(fPA["Falli Commessi"]) * 0.3) || 12;
        const subH = (clean(fCH["Falli Subiti"]) * 0.7) + (clean(fPH["Falli Subiti"]) * 0.3) || 12;
        
        const mFRef = clean(rO["Media Totale"]) || 24;
        const pFalli = ((commH + subA + commA + subH) / 2 * 0.6) + (mFRef * 0.4);

        // 3. CARTELLINI E ANGOLI (API)
        const pG = (parseFloat(rH.response.cards.yellow.average) || 2.2) + (parseFloat(rA.response.cards.yellow.average) || 2.2);
        const pC = (parseFloat(rH.response.goals.for.average) + parseFloat(rA.response.goals.for.average)) * 2.8 + 1.5;

        resDiv.innerHTML = `
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="res-box">
                    <p class="label-sm">Tiri & Porta (API+xG)</p>
                    <div class="text-3xl font-bold teko">MATCH: ${{pT.toFixed(2)}} ${{getTag(pT, document.getElementById('sTiri').value)}}</div>
                    <div class="text-3xl font-bold teko text-blue-400">PORTA: ${{pP.toFixed(2)}} ${{getTag(pP, document.getElementById('sPorta').value)}}</div>
                </div>
                <div class="res-box border-l-red-500">
                    <p class="label-sm">Falli (Tuoi CSV - Arbitro: ${{refN}})</p>
                    <div class="text-5xl font-bold teko text-red-500">${{pFalli.toFixed(2)}} ${{getTag(pFalli, document.getElementById('sFalli').value)}}</div>
                </div>
                <div class="res-box border-l-yellow-500">
                    <p class="label-sm">Gialli (API)</p>
                    <div class="text-4xl font-bold teko text-yellow-500">${{pG.toFixed(2)}} ${{getTag(pG, document.getElementById('sGialli').value)}}</div>
                </div>
                <div class="res-box border-l-emerald-500">
                    <p class="label-sm">Angoli (API)</p>
                    <div class="text-4xl font-bold teko text-emerald-500">${{pC.toFixed(2)}} ${{getTag(pC, document.getElementById('sCorners').value)}}</div>
                </div>
            </div>
        `;
    }} catch(e) {{ 
        resDiv.innerHTML = "<div class='p-4 bg-red-900 rounded-lg'>Errore: " + e.message + "</div>"; 
    }}
}}
init();
</script>
</body>
</html>
"""
components.html(html_code, height=900, scrolling=True)
