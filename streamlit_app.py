import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI - SERIE A 2025", layout="wide")

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
        .card-premium { background: #1e293b; border-radius: 20px; padding: 25px; border: 1px solid #334155; }
        select { background: #0f172a; border: 1px solid #475569; color: white; padding: 12px; width: 100%; border-radius: 12px; font-weight: bold; }
        .btn-analizza { background: #3b82f6; width: 100%; padding: 18px; border-radius: 15px; font-weight: 900; text-transform: uppercase; cursor: pointer; }
        .res-box { background: #0f172a; border-radius: 16px; padding: 20px; border-left: 5px solid #3b82f6; text-align: center; }
    </style>
</head>
<body class="p-4">
    <div class="max-w-xl mx-auto">
        <div class="text-center mb-8">
            <h1 class="text-5xl font-black teko tracking-tighter text-white">PROBET <span class="text-blue-500">AI V3</span></h1>
            <p class="text-[10px] font-bold text-slate-500 tracking-[0.3em] uppercase">Data Season 2025 - Official API Integration</p>
        </div>

        <div class="card-premium mb-6">
            <div class="grid grid-cols-1 gap-4 mb-6">
                <div>
                    <label class="text-[10px] font-bold text-blue-400 mb-2 block uppercase">Squadra Casa</label>
                    <select id="homeTeam"></select>
                </div>
                <div>
                    <label class="text-[10px] font-bold text-blue-400 mb-2 block uppercase">Squadra Ospite</label>
                    <select id="awayTeam"></select>
                </div>
            </div>
            <button onclick="runAnalysis()" class="btn-analizza">Analizza Stagione 2025</button>
        </div>

        <div id="results" class="space-y-4 hidden pb-10"></div>
    </div>

<script>
const API_KEY = "aa5e53f893088010cc7c47af17f306e9";
const DB_URL = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/DATABASE_AVANZATO_2025.csv";

let dbXG = [];

// Carica il tuo database xG WhoScored da GitHub
Papa.parse(DB_URL, {
    download: true, header: true, skipEmptyLines: true,
    complete: function(r) { 
        dbXG = r.data; 
        loadTeams(); 
    }
});

async function loadTeams() {
    try {
        // Carichiamo le squadre della Serie A (135) per la stagione 2025
        const res = await fetch("https://v3.football.api-sports.io/teams?league=135&season=2025", {
            headers: { "x-apisports-key": API_KEY }
        });
        const data = await res.json();
        const h = document.getElementById('homeTeam');
        const a = document.getElementById('awayTeam');
        
        // Visualizziamo le squadre in ordine alfabetico
        data.response.sort((x,y) => x.team.name.localeCompare(y.team.name)).forEach(t => {
            h.add(new Option(t.team.name, t.team.id));
            a.add(new Option(t.team.name, t.team.id));
        });
    } catch(e) { console.error("Errore lista teams:", e); }
}

async function runAnalysis() {
    const idH = document.getElementById('homeTeam').value;
    const idA = document.getElementById('awayTeam').value;
    const resDiv = document.getElementById('results');
    
    resDiv.innerHTML = "<div class='text-center py-8 animate-pulse text-blue-400 font-bold uppercase text-xs'>Recupero statistiche 2025...</div>";
    resDiv.classList.remove('hidden');

    try {
        // Interrogazione API secondo le tue specifiche: league 135 e season 2025
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
        ]);

        const sH = rH.response;
        const sA = rA.response;

        // Recupero xG dal tuo file CSV per gli ID selezionati
        const valXGH = parseFloat(dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || 0.11);
        const valXGA = parseFloat(dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || 0.11);

        // Estrazione Tiri Totali (Total Shots) con protezione dati
        const shotsH = sH?.shots?.total?.average || 11.0;
        const shotsA = sA?.shots?.total?.average || 10.0;

        // Calcolo Algoritmo: Media Tiri * (Tuo xG / Media Lega 0.11)
        const calcoloFinale = (shotsH * (valXGH / 0.11)) + (shotsA * (valXGA / 0.11));

        resDiv.innerHTML = `
            <div class="res-box">
                <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Tiri Totali Previsti (Stagione 2025)</p>
                <h2 class="text-6xl font-black teko text-white">${calcoloFinale.toFixed(2)}</h2>
                <p class="text-[9px] text-blue-400 mt-2 font-bold uppercase">Correttore xG: ${valXGH} (Casa) | ${valXGA} (Ospite)</p>
            </div>
            <div class="grid grid-cols-2 gap-4">
                <div class="res-box border-l-emerald-500">
                    <p class="text-[10px] font-bold text-slate-400 uppercase">Corner Avg</p>
                    <p class="text-2xl font-bold teko">${((sH?.corners?.for?.average || 5.0) + (sA?.corners?.for?.average || 4.5)).toFixed(2)}</p>
                </div>
                <div class="res-box border-l-amber-500">
                    <p class="text-[10px] font-bold text-slate-400 uppercase">Gialli Avg</p>
                    <p class="text-2xl font-bold teko">${((sH?.cards?.yellow?.average || 2.2) + (sA?.cards?.yellow?.average || 2.2)).toFixed(2)}</p>
                </div>
            </div>
        `;
    } catch(e) {
        resDiv.innerHTML = `<div class='p-4 bg-red-900/30 text-red-400 rounded-lg text-center font-bold'>ERRORE: ${e.message}</div>`;
    }
}
</script>
</body>
</html>
"""
components.html(html_code, height=900, scrolling=True)
