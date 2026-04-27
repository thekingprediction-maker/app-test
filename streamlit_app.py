import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE STREAMLIT ---
st.set_page_config(page_title="PROBET AI - TEST 2025", layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600&display=swap');
        body { background: #0f172a; color: white; font-family: sans-serif; }
        .teko { font-family: 'Teko', sans-serif; }
        .card { background: #1e293b; border-radius: 12px; padding: 15px; border: 1px solid #334155; }
        .result-box { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border-radius: 10px; padding: 15px; text-align: center; border-left: 4px solid #3b82f6; }
        select { background: #0f172a; border: 1px solid #334155; color: white; padding: 8px; width: 100%; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="p-4 max-w-2xl mx-auto">
        <h1 class="text-3xl font-black teko text-blue-500 tracking-wider mb-4">TEST STAGIONE 2025 - SERIE A</h1>
        
        <div class="card space-y-4">
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="text-[10px] font-bold text-slate-400">SQUADRA CASA</label>
                    <select id="homeTeam"></select>
                </div>
                <div>
                    <label class="text-[10px] font-bold text-slate-400">SQUADRA OSPITE</label>
                    <select id="awayTeam"></select>
                </div>
            </div>
            <button onclick="startAnalysis()" class="w-full bg-blue-600 hover:bg-blue-500 py-3 rounded-lg font-bold transition-all">
                ANALIZZA (API + xG WHOSCORED)
            </button>
        </div>

        <div id="results" class="mt-6 space-y-4 hidden"></div>
    </div>

<script>
const API_KEY = "aa5e53f893088010cc7c47af17f306e9";
// Il tuo link Raw corretto
const DB_URL = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/DATABASE_AVANZATO_2025.csv";

let manualData = [];

// Caricamento DB xG da GitHub
Papa.parse(DB_URL, {
    download: true,
    header: true,
    complete: function(results) {
        manualData = results.data;
        console.log("DB xG caricato con successo");
        loadTeams();
    }
});

async function loadTeams() {
    const res = await fetch(`https://v3.football.api-sports.io/teams?league=135&season=2024`, {
        headers: { "x-apisports-key": API_KEY }
    });
    const data = await res.json();
    const h = document.getElementById('homeTeam');
    const a = document.getElementById('awayTeam');
    
    data.response.sort((x,y) => x.team.name.localeCompare(y.team.name)).forEach(t => {
        h.add(new Option(t.team.name, t.team.id));
        a.add(new Option(t.team.name, t.team.id));
    });
}

async function startAnalysis() {
    const idH = document.getElementById('homeTeam').value;
    const idA = document.getElementById('awayTeam').value;
    const resDiv = document.getElementById('results');
    
    resDiv.innerHTML = "<p class='text-center animate-pulse'>Calcolo in corso...</p>";
    resDiv.classList.remove('hidden');

    try {
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2024&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2024&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
        ]);

        const sH = rH.response;
        const sA = rA.response;

        // Trova lo xG nel tuo CSV
        const mH = manualData.find(x => x.TeamID == idH) || { xG_Per_Shot: 0.11 };
        const mA = manualData.find(x => x.TeamID == idA) || { xG_Per_Shot: 0.11 };

        // FORMULA TIRI PESATA CON xG
        // Se lo xG è 0.13 (alto), aumenta la proiezione tiri. Se è 0.09 (basso), la diminuisce.
        const baseTiriH = sH.shots.total.average || 12;
        const baseTiriA = sA.shots.total.average || 10;
        
        const pesoH = parseFloat(mH.xG_Per_Shot) / 0.11;
        const pesoA = parseFloat(mA.xG_Per_Shot) / 0.11;

        const finaleTiri = (baseTiriH * pesoH) + (baseTiriA * pesoA);

        resDiv.innerHTML = `
            <div class="result-box">
                <div class="text-[10px] text-blue-400 font-bold uppercase">Proiezione Tiri Totali (xG Weighted)</div>
                <div class="text-4xl font-black teko">${finaleTiri.toFixed(2)}</div>
                <div class="text-[9px] text-slate-500 mt-1">
                    xG Casa: ${mH.xG_Per_Shot} | xG Ospite: ${mA.xG_Per_Shot}
                </div>
            </div>
            <div class="grid grid-cols-2 gap-4">
                <div class="result-box border-l-green-500">
                    <div class="text-[10px] text-slate-400">CORNER MEDIA</div>
                    <div class="text-2xl font-bold teko">${(sH.corners.for.average + sA.corners.for.average).toFixed(2)}</div>
                </div>
                <div class="result-box border-l-yellow-500">
                    <div class="text-[10px] text-slate-400">CARTELLINI MEDIA</div>
                    <div class="text-2xl font-bold teko">${(sH.cards.yellow.average + sA.cards.yellow.average).toFixed(2)}</div>
                </div>
            </div>
        `;
    } catch(e) {
        resDiv.innerHTML = "<p class='text-red-500'>Errore durante il recupero dati API.</p>";
    }
}
</script>
</body>
</html>
"""
components.html(html_code, height=600)
