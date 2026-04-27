import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI - PREMIUM DASHBOARD", layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600;700&family=Inter:wght@400;900&display=swap');
        body { background: #020617; color: #f8fafc; font-family: 'Inter', sans-serif; }
        .teko { font-family: 'Teko', sans-serif; }
        .card-premium { background: #1e293b; border: 1px solid #334155; border-radius: 20px; padding: 25px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); }
        .stat-card { background: #0f172a; border-radius: 15px; padding: 20px; border-left: 4px solid #3b82f6; }
        select { background: #0f172a; border: 1px solid #475569; color: white; padding: 12px; width: 100%; border-radius: 12px; font-weight: 800; appearance: none; }
        .btn-glow { background: #3b82f6; transition: 0.3s; font-weight: 900; letter-spacing: 1px; }
        .btn-glow:hover { background: #2563eb; box-shadow: 0 0 20px rgba(59, 130, 246, 0.5); transform: translateY(-1px); }
    </style>
</head>
<body class="p-6">
    <div class="max-w-2xl mx-auto">
        <div class="text-center mb-10">
            <h1 class="text-5xl font-bold teko tracking-widest text-white">PROBET <span class="text-blue-500">AI V3</span></h1>
            <p class="text-[10px] font-black text-slate-500 uppercase tracking-[0.3em]">Advanced Data Analytics Engine</p>
        </div>

        <div class="card-premium mb-8">
            <div class="grid grid-cols-2 gap-6 mb-6">
                <div>
                    <label class="text-[10px] font-bold text-blue-400 uppercase mb-2 block">Home Team</label>
                    <select id="homeTeam"></select>
                </div>
                <div>
                    <label class="text-[10px] font-bold text-blue-400 uppercase mb-2 block">Away Team</label>
                    <select id="awayTeam"></select>
                </div>
            </div>
            <button onclick="calculate()" class="btn-glow w-full py-4 rounded-xl text-white uppercase text-sm">Esegui Analisi Predittiva</button>
        </div>

        <div id="results" class="grid grid-cols-1 gap-4 hidden pb-10"></div>
    </div>

<script>
const API_KEY = "aa5e53f893088010cc7c47af17f306e9";
const GITHUB_CSV = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/DATABASE_AVANZATO_2025.csv";

let dbXG = [];

// Caricamento dati manuali
Papa.parse(GITHUB_CSV, {
    download: true, header: true, skipEmptyLines: true,
    complete: (r) => { dbXG = r.data; loadTeams(); }
});

async function loadTeams() {
    const res = await fetch("https://v3.football.api-sports.io/teams?league=135&season=2024", { headers: {"x-apisports-key": API_KEY} });
    const data = await res.json();
    const h = document.getElementById('homeTeam');
    const a = document.getElementById('awayTeam');
    data.response.sort((x,y)=>x.team.name.localeCompare(y.team.name)).forEach(t => {
        h.add(new Option(t.team.name, t.team.id));
        a.add(new Option(t.team.name, t.team.id));
    });
}

async function calculate() {
    const idH = document.getElementById('homeTeam').value;
    const idA = document.getElementById('awayTeam').value;
    const resDiv = document.getElementById('results');
    resDiv.innerHTML = "<div class='col-span-full text-center py-10 animate-pulse text-blue-400 font-bold uppercase text-xs tracking-widest'>Analisi in corso...</div>";
    resDiv.classList.remove('hidden');

    try {
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2024&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2024&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
        ]);

        const sH = rH.response;
        const sA = rA.response;

        // Recupero xG con Fallback
        const xGH = parseFloat(dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || 0.11);
        const xGA = parseFloat(dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || 0.11);

        // Estrazione sicura Tiri (Gestisce l'errore undefined 'total')
        const avgTiriH = sH?.shots?.total?.average || 11.5;
        const avgTiriA = sA?.shots?.total?.average || 9.5;

        // Calcolo Algoritmico Tiri
        const totTiri = (avgTiriH * (xGH / 0.11)) + (avgTiriA * (xGA / 0.11));

        resDiv.innerHTML = `
            <div class="stat-card border-l-blue-500">
                <p class="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Previsione Tiri Match</p>
                <h2 class="text-5xl font-black teko text-white">${totTiri.toFixed(2)}</h2>
                <p class="text-[9px] text-blue-400 mt-2">Dati elaborati con correttore xG WhoScored: ${xGH} / ${xGA}</p>
            </div>
            <div class="grid grid-cols-2 gap-4">
                <div class="stat-card border-l-emerald-500">
                    <p class="text-[10px] font-bold text-slate-500 uppercase">Corner Media</p>
                    <h3 class="text-3xl font-bold teko text-white">${((sH?.corners?.for?.average || 5) + (sA?.corners?.for?.average || 4)).toFixed(2)}</h3>
                </div>
                <div class="stat-card border-l-amber-500">
                    <p class="text-[10px] font-bold text-slate-500 uppercase">Gialli Media</p>
                    <h3 class="text-3xl font-bold teko text-white">${((sH?.cards?.yellow?.average || 2.1) + (sA?.cards?.yellow?.average || 2.3)).toFixed(2)}</h3>
                </div>
            </div>
        `;
    } catch(e) {
        resDiv.innerHTML = `<div class="text-red-500 text-center font-bold">ERRORE DI COMUNICAZIONE: Verifica la tua connessione o il piano API</div>`;
    }
}
</script>
</body>
</html>
"""
components.html(html_code, height=900, scrolling=True)
