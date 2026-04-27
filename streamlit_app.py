import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE STREAMLIT ---
st.set_page_config(page_title="PROBET AI - PREMIUM ENGINE", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container { padding: 0 !important; margin: 0 !important; }
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
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600;700&family=Inter:wght@400;800&display=swap');
        body { background: #020617; color: #f8fafc; font-family: 'Inter', sans-serif; overflow-x: hidden; }
        .teko { font-family: 'Teko', sans-serif; }
        .glass { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; }
        select { background: #0f172a; border: 1px solid #334155; color: white; padding: 12px; width: 100%; border-radius: 12px; font-weight: bold; appearance: none; }
        .res-card { background: linear-gradient(145deg, #1e293b, #0f172a); border-radius: 16px; padding: 20px; border-left: 6px solid #3b82f6; shadow: 0 10px 15px -3px rgba(0,0,0,0.5); }
        .btn-glow { background: #3b82f6; transition: all 0.3s; box-shadow: 0 0 20px rgba(59, 130, 246, 0.4); }
        .btn-glow:hover { background: #2563eb; transform: translateY(-2px); box-shadow: 0 0 30px rgba(59, 130, 246, 0.6); }
    </style>
</head>
<body class="p-4 md:p-10">
    <div class="max-w-3xl mx-auto">
        <div class="text-center mb-10">
            <h1 class="text-5xl font-bold teko text-white tracking-tighter">PROBET <span class="text-blue-500">AI PREMIUM</span></h1>
            <div class="inline-block px-3 py-1 bg-blue-500/10 border border-blue-500/20 rounded-full">
                <span class="text-[10px] font-bold text-blue-400 tracking-widest uppercase">Season 2025 Prediction Engine</span>
            </div>
        </div>

        <div class="glass p-6 mb-8">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div>
                    <label class="text-[10px] font-bold text-slate-400 ml-2 mb-1 block uppercase">Home Team</label>
                    <select id="homeTeam"></select>
                </div>
                <div>
                    <label class="text-[10px] font-bold text-slate-400 ml-2 mb-1 block uppercase">Away Team</label>
                    <select id="awayTeam"></select>
                </div>
            </div>
            <button onclick="runAnalysis()" class="btn-glow w-full py-4 rounded-xl font-black text-lg uppercase tracking-tight">
                Analizza Dati Avanzati
            </button>
        </div>

        <div id="results" class="space-y-4 hidden pb-20">
            </div>
    </div>

<script>
const API_KEY = "aa5e53f893088010cc7c47af17f306e9";
const DB_XG_URL = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/DATABASE_AVANZATO_2025.csv";

let dbXG = [];

// 1. Carica il tuo Database xG da GitHub
Papa.parse(DB_XG_URL, {
    download: true,
    header: true,
    skipEmptyLines: true,
    complete: function(results) {
        dbXG = results.data;
        console.log("Database xG caricato. Righe:", dbXG.length);
        loadTeams();
    }
});

// 2. Carica le squadre dall'API
async function loadTeams() {
    try {
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
    } catch(e) { console.error("Errore caricamento team:", e); }
}

// 3. Analisi principale
async function runAnalysis() {
    const idH = document.getElementById('homeTeam').value;
    const idA = document.getElementById('awayTeam').value;
    const resDiv = document.getElementById('results');
    
    resDiv.innerHTML = "<div class='text-center py-10'><div class='animate-spin inline-block w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full mb-4'></div><p class='text-sm font-bold text-blue-400'>ELABORAZIONE POISSON & xG WEIGHT...</p></div>";
    resDiv.classList.remove('hidden');

    try {
        // Chiamata API Statistiche (Proviamo 2024 che è la stagione corrente più stabile)
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2024&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2024&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
        ]);

        if (!rH.response || !rA.response) throw new Error("Dati API non disponibili");

        const sH = rH.response;
        const sA = rA.response;

        // Recupero xG dal tuo CSV
        const csvH = dbXG.find(x => x.TeamID == idH) || { xG_Per_Shot: 0.11 };
        const csvA = dbXG.find(x => x.TeamID == idA) || { xG_Per_Shot: 0.11 };

        // LOGICA TIRI (Peso xG)
        const avgTiriH = sH.shots.total.average || 12;
        const avgTiriA = sA.shots.total.average || 10;
        const xG_H = parseFloat(csvH.xG_Per_Shot);
        const xG_A = parseFloat(csvA.xG_Per_Shot);

        // Calcolo finale pesato: (Media Tiri * (xG_Team / xG_Medio_Lega))
        const finaleTiri = (avgTiriH * (xG_H / 0.11)) + (avgTiriA * (xG_A / 0.11));

        resDiv.innerHTML = `
            <div class="res-card">
                <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Previsione Tiri Totali</p>
                <h2 class="text-5xl font-black teko text-white">${finaleTiri.toFixed(2)}</h2>
                <div class="flex justify-between mt-4 text-[9px] font-bold text-blue-400 border-t border-white/5 pt-2 uppercase">
                    <span>xG Index Casa: ${xG_H}</span>
                    <span>xG Index Ospite: ${xG_A}</span>
                </div>
            </div>
            
            <div class="grid grid-cols-2 gap-4">
                <div class="res-card border-l-emerald-500">
                    <p class="text-[9px] font-bold text-slate-400 uppercase mb-1">Corner Previsti</p>
                    <p class="text-3xl font-bold teko text-white">${(sH.corners.for.average + sA.corners.for.average).toFixed(2)}</p>
                </div>
                <div class="res-card border-l-amber-500">
                    <p class="text-[9px] font-bold text-slate-400 uppercase mb-1">Gialli Previsti</p>
                    <p class="text-3xl font-bold teko text-white">${(sH.cards.yellow.average + sA.cards.yellow.average).toFixed(2)}</p>
                </div>
            </div>
            
            <div class="text-center p-4 bg-blue-500/5 rounded-xl border border-blue-500/10">
                <p class="text-[10px] text-slate-500 font-medium">Dati calcolati incrociando API-Football Premium con Database manuale WhoScored.</p>
            </div>
        `;

    } catch(e) {
        resDiv.innerHTML = `<div class='bg-red-500/10 border border-red-500/20 p-4 rounded-xl text-red-400 text-sm text-center font-bold'>ERRORE: ${e.message}</div>`;
    }
}
</script>
</body>
</html>
"""
components.html(html_code, height=900, scrolling=True)
