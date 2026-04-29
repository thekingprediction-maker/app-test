import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI V4 - FILENAME FIXED", layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600&family=Inter:wght@400;900&display=swap');
        body { background: #020617; color: white; font-family: 'Inter', sans-serif; }
        .teko { font-family: 'Teko', sans-serif; }
        .card-premium { background: #1e293b; border-radius: 24px; padding: 30px; border: 1px solid #334155; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
        select, input { background: #0f172a; border: 1px solid #475569; color: white; padding: 12px; width: 100%; border-radius: 12px; font-weight: bold; outline: none; }
        .btn-analizza { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); width: 100%; padding: 20px; border-radius: 15px; font-weight: 900; text-transform: uppercase; cursor: pointer; border: none; color: white; transition: 0.3s; }
        .btn-analizza:hover { transform: scale(1.02); brightness: 1.1; }
        .status-dot { width: 12px; height: 12px; border-radius: 50%; display: inline-block; margin-right: 6px; }
        .bg-ok { background: #10b981; box-shadow: 0 0 15px #10b981; }
        .bg-err { background: #ef4444; box-shadow: 0 0 15px #ef4444; }
        .bg-wait { background: #64748b; }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-4xl mx-auto">
        <div class="text-center mb-10">
            <h1 class="text-7xl font-black teko tracking-widest text-white uppercase italic leading-none">PROBET <span class="text-blue-500">AI V4</span></h1>
            <div class="flex justify-center gap-6 mt-6 bg-slate-900/80 p-4 rounded-3xl border border-slate-700">
                <div class="flex items-center text-[10px] font-black uppercase tracking-widest text-slate-300">
                    <span id="dot-xg" class="status-dot bg-wait"></span> Database xG
                </div>
                <div class="flex items-center text-[10px] font-black uppercase tracking-widest text-slate-300">
                    <span id="dot-ref" class="status-dot bg-wait"></span> Arbitri Serie A
                </div>
                <div class="flex items-center text-[10px] font-black uppercase tracking-widest text-slate-300">
                    <span id="dot-api" class="status-dot bg-wait"></span> API Football
                </div>
            </div>
        </div>

        <div class="card-premium">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div>
                    <label class="block text-[10px] font-black text-blue-400 uppercase mb-2 tracking-widest">Home Team</label>
                    <select id="homeTeam"><option>Attendere...</option></select>
                </div>
                <div>
                    <label class="block text-[10px] font-black text-blue-400 uppercase mb-2 tracking-widest">Away Team</label>
                    <select id="awayTeam"><option>Attendere...</option></select>
                </div>
                <div>
                    <label class="block text-[10px] font-black text-yellow-500 uppercase mb-2 tracking-widest">Arbitro Designato</label>
                    <select id="arbitroSelect"><option value="24.5">Caricamento CSV...</option></select>
                </div>
            </div>
            
            <button onclick="runAnalysis()" class="btn-analizza teko text-3xl tracking-widest italic">GENERA REPORT PRO</button>
        </div>

        <div id="results" class="mt-8 space-y-6 hidden pb-20"></div>
    </div>

<script>
const API_KEY = "75e4107623c05bb4bca2ac8b78b28dca";
const BASE_URL = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/";

// NOME FILE ESATTO CON CODIFICA SPAZI PER GITHUB
const FILE_REFS = "ARBITRI_SERIE_A%20-%20Foglio1.csv";
const FILE_XG = "DATABASE_AVANZATO_SERIEA_2025.csv";

let dbXG = [];
let dbRef = [];

function setDot(id, status) {
    const d = document.getElementById(id);
    if(d) d.className = "status-dot " + (status === 'ok' ? 'bg-ok' : 'bg-err');
}

async function init() {
    // 1. CARICA xG
    Papa.parse(BASE_URL + FILE_XG, {
        download: true, header: true, skipEmptyLines: true,
        complete: (r) => { 
            dbXG = r.data; 
            setDot('dot-xg', 'ok');
            loadTeams(); 
        },
        error: () => setDot('dot-xg', 'err')
    });

    // 2. CARICA ARBITRI (Gestione Nome File Complesso e Delimitatore)
    Papa.parse(BASE_URL + FILE_REFS, {
        download: true, 
        header: true, 
        skipEmptyLines: true,
        complete: (r) => {
            dbRef = r.data;
            const sel = document.getElementById('arbitroSelect');
            sel.innerHTML = '<option value="24.5">Scegli Arbitro...</option>';
            
            dbRef.forEach(row => {
                let nome = row.Arbitro || row["Arbitro "] || Object.values(row)[0];
                let mediaRaw = row["Media Totale"] || row["Media Totale "] || Object.values(row)[1];
                
                if(nome && nome.trim() !== "") {
                    let media = mediaRaw ? mediaRaw.toString().replace(',', '.') : "24.5";
                    sel.add(new Option(nome.trim(), media));
                }
            });
            setDot('dot-ref', 'ok');
        },
        error: (err) => {
            console.error("Errore Arbitri:", err);
            setDot('dot-ref', 'err');
        }
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
        setDot('dot-api', 'ok');
    } catch(e) { setDot('dot-api', 'err'); }
}

async function runAnalysis() {
    const idH = document.getElementById('homeTeam').value;
    const idA = document.getElementById('awayTeam').value;
    const refVal = parseFloat(document.getElementById('arbitroSelect').value);
    const resDiv = document.getElementById('results');
    
    resDiv.innerHTML = "<div class='text-center py-20 teko text-5xl animate-pulse text-blue-500 tracking-widest'>ANALYZING DATA...</div>";
    resDiv.classList.remove('hidden');

    try {
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=135&season=2025&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
        ]);

        const sH = rH.response; const sA = rA.response;
        const teamAvg = ((sH.fouls.for.average + sA.fouls.against.average)/2 + (sA.fouls.for.average + sH.fouls.against.average)/2);
        const finalFouls = (teamAvg * 0.6) + (refVal * 0.4);

        resDiv.innerHTML = `
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-[#0f172a] p-8 rounded-3xl border-l-8 border-red-500 shadow-2xl">
                    <p class="text-[10px] font-black text-slate-500 uppercase tracking-[0.3em] mb-2">Previsione Falli Match</p>
                    <h2 class="text-8xl font-black teko text-white leading-none">${finalFouls.toFixed(2)}</h2>
                    <p class="text-red-500 text-xs mt-4 font-bold uppercase italic">Parametro Arbitro: ${refVal}</p>
                </div>
                <div class="bg-[#0f172a] p-8 rounded-3xl border-l-8 border-blue-500 shadow-2xl">
                    <p class="text-[10px] font-black text-slate-500 uppercase tracking-[0.3em] mb-2">Previsione Tiri Match</p>
                    <h2 class="text-8xl font-black teko text-white leading-none">${(sH.shots.total.average + sA.shots.total.average).toFixed(2)}</h2>
                </div>
            </div>
        `;
    } catch(e) {
        resDiv.innerHTML = "<div class='text-red-500 font-bold'>Errore API: Verifica la connessione.</div>";
    }
}

init();
</script>
</body>
</html>
"""
components.html(html_code, height=1000, scrolling=True)
