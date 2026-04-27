import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

st.set_page_config(page_title="PROBET AI V4 - FINAL", layout="wide")

# Caricamento file con pulizia immediata dei nomi colonne
try:
    df_arbitri = pd.read_csv('ARBITRI_SERIE_A - Foglio1.csv', sep=';').fillna("0")
    df_arbitri.columns = df_arbitri.columns.str.strip() # Toglie spazi dai nomi colonne
    
    df_falli_curr = pd.read_csv('FALLI_CURR_SERIE_A - Foglio1.csv', sep=';').fillna("0")
    df_falli_curr.columns = df_falli_curr.columns.str.strip()
    
    df_falli_prev = pd.read_csv('FALLI_PREV_SERIE_A - DATI STAGIONE 2024_2025 .csv', sep=',').fillna("0")
    df_falli_prev.columns = df_falli_prev.columns.str.strip()
except Exception as e:
    st.error(f"Errore caricamento CSV: {e}")

html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600&family=Inter:wght@400;900&display=swap');
        body {{ background: #020617; color: white; font-family: 'Inter', sans-serif; padding: 20px; }}
        .card {{ background: #1e293b; border-radius: 15px; padding: 20px; border: 1px solid #334155; }}
        select, input {{ background: #0f172a; border: 1px solid #475569; color: white; padding: 8px; width: 100%; border-radius: 8px; font-size: 14px; }}
        .btn {{ background: #3b82f6; width: 100%; padding: 15px; border-radius: 10px; font-weight: bold; cursor: pointer; margin-top: 20px; border: none; color: white; }}
        .res-box {{ background: #0f172a; padding: 15px; border-radius: 10px; border-left: 4px solid #3b82f6; margin-top: 15px; }}
        .teko {{ font-family: 'Teko', sans-serif; text-transform: uppercase; }}
    </style>
</head>
<body>
    <div class="max-w-4xl mx-auto">
        <h2 class="text-3xl teko mb-4 text-center">ProBet AI <span class="text-blue-500 italic">Hybrid Edition</span></h2>
        <div class="card">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div><label class="text-xs font-bold text-slate-400 uppercase">Casa</label><select id="hT"></select></div>
                <div><label class="text-xs font-bold text-slate-400 uppercase">Ospite</label><select id="aT"></select></div>
                <div><label class="text-xs font-bold text-slate-400 uppercase">Arbitro</label><select id="refS"></select></div>
            </div>
            <div class="grid grid-cols-5 gap-2 mt-4">
                <input type="number" id="sFalli" value="24.5" placeholder="Falli">
                <input type="number" id="sTiri" value="23.5" placeholder="Tiri">
                <input type="number" id="sPorta" value="8.5" placeholder="Porta">
                <input type="number" id="sGialli" value="4.5" placeholder="Gialli">
                <input type="number" id="sCorners" value="9.5" placeholder="Angoli">
            </div>
            <button onclick="run()" class="btn teko text-xl">Calcola Previsione</button>
        </div>
        <div id="results" class="hidden"></div>
    </div>

<script>
const K = "aa5e53f893088010cc7c47af17f306e9";
const arbData = {df_arbitri.to_json(orient='records')};
const currF = {df_falli_curr.to_json(orient='records')};
const prevF = {df_falli_prev.to_json(orient='records')};

// Mapping Nomi: Traduce API -> Tuo CSV
const mapName = (n) => {{
    const d = {{ 'AC Milan': 'Milan', 'AS Roma': 'Roma', 'Hellas Verona': 'Hellas Verona', 'Inter': 'Inter' }};
    return d[n] || n.replace('AC ', '').replace('AS ', '').trim();
}};

const clean = (v) => {{
    if(!v) return 0;
    return parseFloat(v.toString().replace(',', '.')) || 0;
}};

async function init() {{
    const res = await fetch("https://v3.football.api-sports.io/teams?league=135&season=2025", {{headers:{{"x-apisports-key":K}}}});
    const d = await res.json();
    d.response.forEach(t => {{
        document.getElementById('hT').add(new Option(t.team.name, t.team.id));
        document.getElementById('aT').add(new Option(t.team.name, t.team.id));
    }});
    // Popolamento Arbitri sicuro
    arbData.forEach(r => {{
        if(r.Arbitro) document.getElementById('refS').add(new Option(r.Arbitro, r.Arbitro));
    }});
}}

async function run() {{
    const idH = document.getElementById('hT').value, idA = document.getElementById('aT').value;
    const nH = mapName(document.getElementById('hT').options[document.getElementById('hT').selectedIndex].text);
    const nA = mapName(document.getElementById('aT').options[document.getElementById('aT').selectedIndex].text);
    const ref = document.getElementById('refS').value;

    const [rH, rA] = await Promise.all([
        fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${{idH}}`, {{headers:{{"x-apisports-key":K}}}}).then(r=>r.json()),
        fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${{idA}}`, {{headers:{{"x-apisports-key":K}}}}).then(r=>r.json())
    ]);

    // LOGICA FALLI (Mappa esatta sui tuoi file)
    const fCH = currF.find(x => x.Squadra === nH && JSON.stringify(x).includes("Casa")) || {{}};
    const fCA = currF.find(x => x.Squadra === nA && JSON.stringify(x).includes("Fuori")) || {{}};
    const fPH = prevF.find(x => x.Squadra === nH && JSON.stringify(x).includes("Casa")) || {{}};
    const fPA = prevF.find(x => x.Squadra === nA && JSON.stringify(x).includes("Fuori")) || {{}};
    const rO = arbData.find(x => x.Arbitro === ref) || {{}};

    const cH = (clean(fCH["Falli Commessi"])*0.7 + clean(fPH["Falli Commessi"])*0.3) || 12;
    const sA = (clean(fCA["Falli Subiti"])*0.7 + clean(fPA["Falli Subiti"])*0.3) || 12;
    const cA = (clean(fCA["Falli Commessi"])*0.7 + clean(fPA["Falli Commessi"])*0.3) || 12;
    const sH = (clean(fCH["Falli Subiti"])*0.7 + clean(fPH["Falli Subiti"])*0.3) || 12;
    
    const pFalli = (((cH+sA+cA+sH)/2)*0.6) + (clean(rO["Media Totale"])*0.4);

    document.getElementById('results').innerHTML = `
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="res-box"><p class="text-xs font-bold text-red-400">FALLI (CSV)</p><p class="text-4xl teko">${{pFalli.toFixed(2)}}</p></div>
            <div class="res-box"><p class="text-xs font-bold text-blue-400">TIRI (API)</p><p class="text-4xl teko">${{(clean(rH.response.shots.total.average)+clean(rA.response.shots.total.average)).toFixed(2)}}</p></div>
        </div>
    `;
    document.getElementById('results').classList.remove('hidden');
}}
init();
</script>
</body>
</html>
"""
components.html(html_code, height=600)
