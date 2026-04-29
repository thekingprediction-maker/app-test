import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI V4 - RAW FIXED", layout="wide")

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
        .card-premium { background: #1e293b; border-radius: 24px; padding: 30px; border: 1px solid #334155; }
        select, input { background: #0f172a; border: 1px solid #475569; color: white; padding: 12px; width: 100%; border-radius: 12px; font-weight: bold; outline: none; }
        .btn-analizza { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); width: 100%; padding: 20px; border-radius: 15px; font-weight: 900; text-transform: uppercase; cursor: pointer; border: none; color: white; }
        .status-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; margin-right: 5px; }
        .bg-wait { background: #64748b; }
        .bg-ok { background: #10b981; }
        .bg-err { background: #ef4444; }
    </style>
</head>
<body class="p-4">
    <div class="max-w-4xl mx-auto">
        <div class="text-center mb-8">
            <h1 class="text-6xl font-black teko tracking-widest text-white uppercase italic">PROBET <span class="text-blue-500">AI V4</span></h1>
            <div class="flex justify-center gap-6 mt-4">
                <div class="flex items-center text-[10px] font-bold uppercase"><span id="dot-xg" class="status-dot bg-wait"></span> GitHub xG</div>
                <div class="flex items-center text-[10px] font-bold uppercase"><span id="dot-ref" class="status-dot bg-wait"></span> GitHub Arbitri</div>
                <div class="flex items-center text-[10px] font-bold uppercase"><span id="dot-api" class="status-dot bg-wait"></span> API Teams</div>
            </div>
        </div>

        <div class="card-premium">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div>
                    <label class="block text-[10px] font-black text-blue-400 uppercase mb-2">Home Team</label>
                    <select id="homeTeam"><option>Loading...</option></select>
                </div>
                <div>
                    <label class="block text-[10px] font-black text-blue-400 uppercase mb-2">Away Team</label>
                    <select id="awayTeam"><option>Loading...</option></select>
                </div>
                <div>
                    <label class="block text-[10px] font-black text-yellow-500 uppercase mb-2">Arbitro (GitHub CSV)</label>
                    <select id="arbitroSelect"><option value="24.5">Seleziona Arbitro...</option></select>
                </div>
            </div>

            <button onclick="runAnalysis()" class="btn-analizza teko text-2xl tracking-widest shadow-2xl">AVVIA ANALISI</button>
        </div>

        <div id="results" class="mt-8 space-y-4 hidden pb-20"></div>
    </div>

<script>
const API_KEY = "75e4107623c05bb4bca2ac8b78b28dca";
// URL RAW - Questo punta ai dati reali
const RAW_BASE = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/";

let dbXG = [];
let dbRef = [];

function updateStatus(id, status) {
    const dot = document.getElementById(id);
    dot.className = "status-dot " + (status === 'ok' ? 'bg-ok' : 'bg-err');
}

async function init() {
    // 1. CARICA xG
    Papa.parse(RAW_BASE + "DATABASE_AVANZATO_SERIEA_2025.csv", {
        download: true, header: true, skipEmptyLines: true,
        complete: (results) => {
            dbXG = results.data;
            updateStatus('dot-xg', 'ok');
            loadTeams();
        },
        error: () => updateStatus('dot-xg', 'err')
    });

    // 2. CARICA ARBITRI (Usiamo il delimitatore ; visto nel tuo file)
    Papa.parse(RAW_BASE + "ARBITRI_SERIEA_2025.csv", {
        download: true, header: true, skipEmptyLines: true, delimiter: ";",
        complete: (results) => {
            dbRef = results.data;
            const sel = document.getElementById('arbitroSelect');
            sel.innerHTML = '<option value="24.5">Seleziona Arbitro...</option>';
            dbRef.forEach(r => {
                if(r.Arbitro) {
                    let val = r["Media Totale"] ? r["Media Totale"].toString().replace(',', '.') : "24.5";
                    sel.add(new Option(r.Arbitro, val));
                }
            });
            updateStatus('dot-ref', 'ok');
        },
        error: () => updateStatus('dot-ref', 'err')
    });
}

async function loadTeams() {
    try {
        const res = await fetch("https://v3.football.api-sports.io/teams?league=135&season=2025", {
            headers: { "x-apisports-key": API_KEY }
        });
        const data = await res.json();
        const h = document.getElementById('homeTeam'), a = document.getElementById('awayTeam');
        h.innerHTML = ""; a.innerHTML = "";
        data.response.sort((x,y) => x.team.name.localeCompare(y.team.name)).forEach(t => {
            h.add(new Option(t.team.name, t.team.id));
            a.add(new Option(t.team.name, t.team.id));
        });
        updateStatus('dot-api', 'ok');
    } catch(e) { updateStatus('dot-api', 'err'); }
}

async function runAnalysis() {
    const idH = document.getElementById('homeTeam').value;
    const idA = document.getElementById('awayTeam').value;
    const refVal = parseFloat(document.getElementById('arbitroSelect').value);
    const resDiv = document.getElementById('results');
    
    resDiv.innerHTML = "<div class='text-center py-10 teko text-3xl animate-pulse'>ANALISI IN CORSO...</div>";
    resDiv.classList.remove('hidden');

    const [rH, rA] = await Promise.all([
        fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
        fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
    ]);

    const sH = rH.response; const sA = rA.response;
    
    // Calcolo Ibrido Falli
    const teamAvg = ((sH.fouls.for.average + sA.fouls.against.average)/2 + (sA.fouls.for.average + sH.fouls.against.average)/2);
    const finalFouls = (teamAvg * 0.6) + (refVal * 0.4);

    resDiv.innerHTML = `
        <div class="bg-[#0f172a] p-8 rounded-3xl border-l-8 border-red-500 shadow-2xl">
            <p class="text-xs font-bold text-slate-500 uppercase mb-2">Previsione Falli (60% Team + 40% Arbitro)</p>
            <h2 class="text-7xl font-black teko">${finalFouls.toFixed(2)}</h2>
        </div>
    `;
}

init();
</script>
</body>
</html>
"""
components.html(html_code, height=900, scrolling=True)
