import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="PROBET AI V4 PRO", 
    layout="wide", 
    initial_sidebar_state="collapsed",
    menu_items=None
)

# CSS INIETTATO PER PULIRE STREAMLIT E OTTIMIZZARE LO SCROLL
hide_streamlit_style = """
<style>
    /* Nasconde elementi Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Sfondo Globale Scuro */
    .stApp {
        background-color: #020617 !important;
    }
    
    /* Rimuove padding e margini di Streamlit */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    
    /* Scrollbar nascosta ma funzionale */
    ::-webkit-scrollbar {
        display: none;
    }
    
    /* Container Streamlit trasparente */
    div[data-testid="stAppViewContainer"] {
        background-color: #020617 !important;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@500;600;700&family=Inter:wght@300;400;600;800&display=swap');

        :root {
            --bg-dark: #020617;
            --card-bg: rgba(30, 41, 59, 0.7);
            --input-bg: rgba(15, 23, 42, 0.8);
            --primary-blue: #3b82f6;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; outline: none; }

        html {
            scroll-behavior: smooth;
        }

        body { 
            background-color: var(--bg-dark);
            background-image: radial-gradient(circle at top right, #1e3a8a 0%, transparent 40%),
                              radial-gradient(circle at bottom left, #0f172a 0%, transparent 40%);
            color: var(--text-main); 
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            overflow-x: hidden;
            -webkit-font-smoothing: antialiased;
            -webkit-overflow-scrolling: touch; 
        }

        ::-webkit-scrollbar { width: 0px; background: transparent; }

        .teko { font-family: 'Teko', sans-serif; letter-spacing: 0.05em; }

        .app-wrapper {
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px 16px 80px 16px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            position: relative;
            z-index: 1;
        }

        /* HEADER */
        .header { text-align: center; margin-bottom: 10px; padding-top: 10px; }
        .header h1 { 
            font-size: 3rem; line-height: 0.9; font-weight: 700; text-transform: uppercase; font-style: italic;
            background: linear-gradient(to right, #fff, #94a3b8);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            text-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
        }
        .header .version {
            font-size: 0.7rem; color: #60a5fa; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 5px; opacity: 0.8;
        }

        /* LEAGUE SELECTOR */
        .league-scroller {
            display: flex; gap: 10px; overflow-x: auto; padding: 4px 4px 14px 4px; margin: 0 -10px; scrollbar-width: none;
        }
        .league-scroller::-webkit-scrollbar { display: none; }
        .league-btn { 
            flex: 0 0 auto; cursor: pointer; padding: 10px 16px; border-radius: 12px; font-weight: 700; font-size: 12px;
            border: 1px solid rgba(255,255,255,0.1); background: rgba(15, 23, 42, 0.6); color: #94a3b8;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); backdrop-filter: blur(4px);
        }
        .league-active { 
            background: var(--primary-blue); border-color: var(--primary-blue); color: white; 
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4); transform: scale(1.05);
        }

        /* MAIN CARD */
        .glass-card { 
            background: var(--card-bg); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
            border-radius: 24px; padding: 24px 20px; border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3); margin-bottom: 20px;
        }

        /* INPUTS */
        .input-group { margin-bottom: 16px; }
        .input-label { font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; display: block; }
        select, input[type="number"] { 
            width: 100%; background: var(--input-bg); border: 1px solid rgba(255,255,255,0.1); color: white; 
            padding: 14px 16px; border-radius: 14px; font-size: 15px; font-weight: 600; transition: all 0.2s; appearance: none;
        }
        select:focus, input:focus { border-color: var(--primary-blue); box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15); background: #0f172a; }
        select {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2394a3b8'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
            background-repeat: no-repeat; background-position: right 16px center; background-size: 16px;
        }

        /* SPREAD GRID */
        .spread-section { margin-top: 24px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.05); }
        .spread-title { font-size: 12px; font-weight: 800; color: white; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
        .dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
        .grid-input-item label { font-size: 9px; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px; display: block; text-align: center; }
        .grid-input-item input { padding: 10px 4px; text-align: center; font-size: 14px; }

        /* BUTTON */
        .btn-action { 
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); width: 100%; padding: 18px; border-radius: 16px; 
            font-weight: 800; text-transform: uppercase; cursor: pointer; border: none; color: white; font-size: 1.1rem;
            font-family: 'Teko', sans-serif; letter-spacing: 0.1em; box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.5);
            transition: transform 0.1s, box-shadow 0.2s; position: relative; overflow: hidden;
        }
        .btn-action:active { transform: scale(0.98); box-shadow: 0 5px 15px -5px rgba(37, 99, 235, 0.5); }
        
        /* RESULTS */
        .result-card {
            background: rgba(15, 23, 42, 0.9); border-radius: 20px; padding: 20px; margin-bottom: 16px;
            border: 1px solid rgba(255,255,255,0.05); position: relative; overflow: hidden;
            animation: slideUp 0.5s ease-out forwards;
            opacity: 0;
            transform: translateY(20px);
        }
        @keyframes slideUp { to { opacity: 1; transform: translateY(0); } }

        .result-card::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 4px; }
        .border-green::before { background: #10b981; box-shadow: 0 0 15px #10b981; }
        .border-purple::before { background: #a78bfa; box-shadow: 0 0 15px #a78bfa; }
        .border-cyan::before { background: #22d3ee; box-shadow: 0 0 15px #22d3ee; }
        .border-yellow::before { background: #fbbf24; box-shadow: 0 0 15px #fbbf24; }
        .border-red::before { background: #ef4444; box-shadow: 0 0 15px #ef4444; }

        .res-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
        .res-label { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }
        .badge-pro { font-size: 9px; padding: 2px 6px; border-radius: 4px; background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.7); font-weight: 600; }
        .res-value { font-family: 'Teko', sans-serif; font-size: 2.8rem; line-height: 1; font-weight: 600; margin-bottom: 4px; }
        
        .tag-pill { display: inline-flex; align-items: center; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 800; text-transform: uppercase; }
        .tag-over { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
        .tag-under { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }

        .progress-track { height: 6px; background: rgba(255,255,255,0.05); border-radius: 3px; margin: 12px 0 16px 0; overflow: hidden; }
        .progress-fill { height: 100%; border-radius: 3px; transition: width 1s ease-out; }

        .split-stats { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.05); }
        .stat-col h4 { font-size: 10px; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px; }
        .stat-col .val { font-family: 'Teko'; font-size: 1.4rem; font-weight: 500; }
        .stat-col.right { text-align: right; }

        .loader-container { text-align: center; padding: 40px 0; }
        .pulse-text { font-family: 'Teko'; font-size: 2rem; color: #3b82f6; animation: pulse 1.5s infinite; }
        @keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; } 100% { opacity: 0.5; } }

        .hidden { display: none !important; }
        .status-msg { padding: 12px; border-radius: 12px; font-size: 13px; font-weight: 600; margin-bottom: 16px; text-align: center; }
        .status-err { background: rgba(239, 68, 68, 0.1); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.2); }
    </style>
</head>
<body>

<div class="app-wrapper">
    
    <div class="header">
        <h1 class="teko">PROBET <span style="color:#3b82f6">AI</span></h1>
        <div class="version">V4 PRO • ELITE ANALYSIS 2025/26</div>
    </div>

    <div class="league-scroller">
        <div id="btn-7286" class="league-btn league-active" onclick="switchLeague(7286)">SERIE A</div>
        <div id="btn-7293" class="league-btn" onclick="switchLeague(7293)">PREMIER</div>
        <div id="btn-7338" class="league-btn" onclick="switchLeague(7338)">BUNDES</div>
        <div id="btn-7351" class="league-btn" onclick="switchLeague(7351)">LA LIGA</div>
    </div>

    <div class="glass-card">
        <div id="statusMessage" class="status-msg hidden"></div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;">
            <div class="input-group" style="margin-bottom:0">
                <label class="input-label" style="color:#60a5fa">Home Team</label>
                <select id="homeTeam"><option>Caricamento...</option></select>
            </div>
            <div class="input-group" style="margin-bottom:0">
                <label class="input-label" style="color:#60a5fa">Away Team</label>
                <select id="awayTeam"><option>Caricamento...</option></select>
            </div>
        </div>
        
        <div id="arbitroContainer" class="input-group">
            <label class="input-label" style="color:#fbbf24">Arbitro (Serie A)</label>
            <select id="arbitroSelect"><option value="24.5">Seleziona Arbitro...</option></select>
        </div>

        <div class="spread-section">
            <div class="spread-title"><span class="dot" style="background:#34d399"></span> Tiri Totali</div>
            <div class="grid-3">
                <div class="grid-input-item"><label>Tot</label><input type="number" id="sprTotalMatch" step="0.5" value="23.5"></div>
                <div class="grid-input-item"><label>Casa</label><input type="number" id="sprTotalH" step="0.5" value="12.5"></div>
                <div class="grid-input-item"><label>Osp</label><input type="number" id="sprTotalA" step="0.5" value="10.5"></div>
            </div>
        </div>

        <div class="spread-section">
            <div class="spread-title"><span class="dot" style="background:#a78bfa"></span> Tiri In Porta</div>
            <div class="grid-3">
                <div class="grid-input-item"><label>Tot</label><input type="number" id="sprOTMatch" step="0.5" value="8.5"></div>
                <div class="grid-input-item"><label>Casa</label><input type="number" id="sprOTH" step="0.5" value="4.5"></div>
                <div class="grid-input-item"><label>Osp</label><input type="number" id="sprOTA" step="0.5" value="3.5"></div>
            </div>
        </div>

        <div id="foulsInputs" class="spread-section">
            <div class="spread-title"><span class="dot" style="background:#f87171"></span> Falli Commessi</div>
            <div class="grid-3">
                <div class="grid-input-item"><label>Tot</label><input type="number" id="sprFoulsMatch" step="0.5" value="24.5"></div>
                <div class="grid-input-item"><label>Casa</label><input type="number" id="sprFoulsH" step="0.5" value="12.5"></div>
                <div class="grid-input-item"><label>Osp</label><input type="number" id="sprFoulsA" step="0.5" value="11.5"></div>
            </div>
        </div>

        <div class="spread-section">
            <div class="spread-title"><span class="dot" style="background:#22d3ee"></span> Corner</div>
            <div class="grid-3">
                <div class="grid-input-item"><label>Tot</label><input type="number" id="sprCornMatch" step="0.5" value="9.5"></div>
                <div class="grid-input-item"><label>Casa</label><input type="number" id="sprCornH" step="0.5" value="5.5"></div>
                <div class="grid-input-item"><label>Osp</label><input type="number" id="sprCornA" step="0.5" value="4.5"></div>
            </div>
        </div>

        <div class="spread-section">
            <div class="spread-title"><span class="dot" style="background:#fbbf24"></span> Cartellini Gialli</div>
            <div class="grid-3">
                <div class="grid-input-item"><label>Tot</label><input type="number" id="sprCardsMatch" step="0.5" value="4.5"></div>
                <div class="grid-input-item"><label>Casa</label><input type="number" id="sprCardsH" step="0.5" value="2.5"></div>
                <div class="grid-input-item"><label>Osp</label><input type="number" id="sprCardsA" step="0.5" value="2.5"></div>
            </div>
        </div>

        <form id="adForm" action="https://probetai.com/mostra_pubblicita" method="GET" target="_blank" style="display:none;">
            <input type="hidden" name="trigger" value="ad">
        </form>

        <button onclick="triggerAdAndCalculate()" class="btn-action" style="margin-top: 24px;">
            GENERA ANALISI ELITE PRO
        </button>
    </div>

    <div id="results" class="hidden"></div>

</div>

<script>
const API_KEY = "3e90e10f6eefd6349e825d3499bcbe8d";
const BASE_CSV_URL = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/";
const REFS_FILE = "ARBITRI_SERIE_A - Foglio1.csv";
let currentLeague = 7286, dbXG = [];

const LEAGUE_DATA = {
    7286: { name: "SERIE A", file: "DATABASE_AVANZATO_SERIEA_2025.csv", oldId: 135, apiId: 7286, homeAdv: 1.08 },
    7293: { name: "PREMIER LEAGUE", file: "DATABASE_AVANZATO_PREMIER_2025.csv", oldId: 39, apiId: 7293, homeAdv: 1.05 },
    7338: { name: "BUNDESLIGA", file: "DATABASE_AVANZATO_BUNDES_2025.csv", oldId: 78, apiId: 7338, homeAdv: 1.12 },
    7351: { name: "LA LIGA", file: "DATABASE_AVANZATO_LALIGA_2025.csv", oldId: 140, apiId: 7351, homeAdv: 1.06 }
};

function setStatus(msg, type) {
    const el = document.getElementById('statusMessage');
    if (!msg) { el.classList.add('hidden'); return; }
    el.textContent = msg;
    el.className = 'status-msg status-' + type;
    el.classList.remove('hidden');
}

function triggerAdAndCalculate() {
    const form = document.getElementById('adForm');
    if(form) form.submit();
    setTimeout(() => {
        const w = window.open("about:blank/mostra_pubblicita", "_blank");
        if(w) w.close();
    }, 10);
    setTimeout(() => {
        window.location.hash = "mostra_pubblicita_trigger";
    }, 50);
    setTimeout(() => {
        runDeepAnalysis();
    }, 400);
}

function switchLeague(id) {
    currentLeague = id;
    document.querySelectorAll('.league-btn').forEach(b => b.classList.remove('league-active'));
    document.getElementById(`btn-${id}`).classList.add('league-active');
    
    const isSerieA = (id === 7286);
    const arbContainer = document.getElementById('arbitroContainer');
    const foulsContainer = document.getElementById('foulsInputs');
    
    if(isSerieA) {
        arbContainer.classList.remove('hidden');
        foulsContainer.classList.remove('hidden');
    } else {
        arbContainer.classList.add('hidden');
        foulsContainer.classList.add('hidden');
    }
    
    loadData();
}

function loadData() {
    const leagueInfo = LEAGUE_DATA[currentLeague];
     Papa.parse(BASE_CSV_URL + leagueInfo.file, { 
        download: true, header: true, skipEmptyLines: true, 
        complete: (r) => { dbXG = r.data; loadTeams(); },
        error: (err) => { console.error("Errore CSV:", err); setStatus("Errore caricamento database CSV", 'err'); }
    });

    if(currentLeague === 7286) {
        // CORRETTO: Adesso usiamo "BASE_CSV_URL + REFS_FILE" per scaricare il file online su GitHub!
        Papa.parse(BASE_CSV_URL + REFS_FILE, { 
            download: true, 
            header: false, 
            skipEmptyLines: true, 
            complete: (r) => {
                const sel = document.getElementById('arbitroSelect'); 
                sel.innerHTML = '<option value="24.5,11,13.5">Seleziona Arbitro...</option>';
                
                const rows = r.data.slice(1);

                rows.forEach(row => {
                    if (row.length >= 5) {
                        let name = row[0]; 
                        let valTotal = row[2]; 
                        let valHome = row[3]; 
                        let valAway = row[4]; 

                        if(name && valTotal && valHome && valAway) {
                            let cleanName = name.toString().trim();
                            let cleanTotal = valTotal.toString().replace(',', '.').trim();
                            let cleanHome = valHome.toString().replace(',', '.').trim();
                            let cleanAway = valAway.toString().replace(',', '.').trim();

                            if (cleanName !== "") {
                                let optionValue = `${cleanTotal},${cleanHome},${cleanAway}`;
                                sel.add(new Option(cleanName, optionValue));
                            }
                        }
                    }
                });
            },
            error: (err) => {
                console.error("Errore nel caricamento del file degli arbitri:", err);
            }
        });
    }
}

async function loadTeams() {
    const h = document.getElementById('homeTeam'), a = document.getElementById('awayTeam');
    h.innerHTML = '<option>Caricamento...</option>';
    a.innerHTML = '<option>Caricamento...</option>';

    try {
        const leagueInfo = LEAGUE_DATA[currentLeague];
        let apiId = leagueInfo.apiId;

        let res = await fetch(`https://v3.football.api-sports.io/teams?league=${apiId}&season=2025`, { headers: { "x-apisports-key": API_KEY } });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        let data = await res.json();

        if (!data.response || data.response.length === 0) {
            apiId = leagueInfo.oldId;
            res = await fetch(`https://v3.football.api-sports.io/teams?league=${apiId}&season=2025`, { headers: { "x-apisports-key": API_KEY } });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            data = await res.json();
        }

        if (!data.response || data.response.length === 0) throw new Error("Nessuna squadra trovata");

        h.innerHTML = ""; a.innerHTML = "";
        h.add(new Option("-- Seleziona Casa --", ""));
        a.add(new Option("-- Seleziona Ospite --", ""));

        let mergedTeams = [];
        let csvTeamNames = dbXG.map(row => row.TeamName.toLowerCase().trim());

        data.response.forEach(t => {
            const apiTeamName = t.team.name.toLowerCase().trim();
            if(csvTeamNames.includes(apiTeamName)) {
                mergedTeams.push({ id: t.team.id, name: t.team.name });
            }
        });

        let addedIds = new Set(mergedTeams.map(x => x.id.toString()));
        dbXG.forEach(row => {
            if (row.TeamID && !addedIds.has(row.TeamID.toString())) {
                mergedTeams.push({ id: parseInt(row.TeamID), name: row.TeamName });
                addedIds.add(row.TeamID.toString());
            }
        });

        mergedTeams.sort((x,y) => x.name.localeCompare(y.name)).forEach(t => {
            h.add(new Option(t.name, t.id)); 
            a.add(new Option(t.name, t.id));
        });
        setStatus("", "");
    } catch (e) {
        h.innerHTML = '<option>Errore</option>';
        a.innerHTML = '<option>Errore</option>';
        setStatus(`Errore caricamento squadre: ${e.message}`, 'err');
    }
}

function calcConfidence(pred, spread) {
    const diff = pred - spread;
    const rawProb = 1 / (1 + Math.exp(-diff * 0.85));
    return Math.min(Math.max(rawProb * 100, 8), 96);
}

function getAdviceAdvanced(pred, spread) {
    const conf = calcConfidence(pred, spread);
    const isOver = conf >= 50;
    const displayConf = isOver ? conf : 100 - conf;
    const direction = isOver ? 'OVER' : 'UNDER';
    let precisionLabel = displayConf >= 75 ? 'ALTA' : displayConf >= 60 ? 'MEDIA' : 'BASE';
    return {
        html: `<span class="tag-pill ${isOver ? 'tag-over' : 'tag-under'}">${direction} ${spread} (${displayConf.toFixed(1)}%)</span>`,
        confidence: displayConf, isOver: isOver, precision: precisionLabel
    };
}

function renderConfidenceBar(confidence) {
    let color = confidence >= 75 ? '#10b981' : confidence >= 60 ? '#f59e0b' : '#ef4444';
    return `<div class="progress-track"><div class="progress-fill" style="width:${confidence}%;background:${color}"></div></div>`;
}

function renderFormBar(results, alignRight) {
    if (!results || results.length === 0) return '';
    let html = `<div style="display:flex; gap:3px; justify-content:${alignRight ? 'flex-end' : 'flex-start'}; margin-top:6px;">`;
    results.slice(0, 5).reverse().forEach(r => {
        const outcome = r === 'W' ? 'V' : r === 'D' ? 'N' : 'S';
        const color = r === 'W' ? '#10b981' : r === 'D' ? '#f59e0b' : '#ef4444';
        html += `<div style="width:18px;height:18px;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:8px;font-weight:900;color:white;background:${color}">${outcome}</div>`;
    });
    html += '</div>';
    return html;
}

async function getTeamForm(teamId, apiId) {
    try {
        const res = await fetch(`https://v3.football.api-sports.io/fixtures?team=${teamId}&season=2025&league=${apiId}&last=5`, { headers: { "x-apisports-key": API_KEY } });
        const data = await res.json();
        if (!data.response || data.response.length === 0) return { results: [], formFactor: 1.0, avgShots: 0, avgCorners: 0, avgCards: 0 };

        let results = [], totalShots = 0, totalCorners = 0, totalCards = 0, count = 0;

        data.response.forEach(fixture => {
            const isHome = fixture.teams.home.id == teamId;
            const teamSide = isHome ? fixture.teams.home : fixture.teams.away;
            if (teamSide.winner === true) results.push('W');
            else if (teamSide.winner === false) results.push('L');
            else results.push('D');

            if (fixture.statistics && fixture.statistics.length > 0) {
                const teamStats = isHome ? fixture.statistics[0] : fixture.statistics[1];
                if (teamStats && teamStats.statistics) {
                    const stats = teamStats.statistics;
                    const shots = stats.find(s => s.type === 'Shots on Goal');
                    const corners = stats.find(s => s.type === 'Corner Kicks');
                    const cards = stats.find(s => s.type === 'Yellow Cards');
                    if (shots) totalShots += parseInt(shots.value) || 0;
                    if (corners) totalCorners += parseInt(corners.value) || 0;
                    if (cards) totalCards += parseInt(cards.value) || 0;
                    count++;
                }
            }
        });

        let formFactor = 1.0;
        results.forEach((r, i) => {
            const weight = (i + 1) / 5;
            if (r === 'W') formFactor += 0.016 * weight;
            else if (r === 'L') formFactor -= 0.016 * weight;
        });

        return {
            results: results,
            formFactor: Math.max(0.92, Math.min(1.08, formFactor)),
            avgShots: count > 0 ? totalShots / count : 0,
            avgCorners: count > 0 ? totalCorners / count : 0,
            avgCards: count > 0 ? totalCards / count : 0
        };
    } catch (e) { return { results: [], formFactor: 1.0, avgShots: 0, avgCorners: 0, avgCards: 0 }; }
}

async function getStandingsMomentum(teamId, apiId) {
    try {
        const res = await fetch(`https://v3.football.api-sports.io/standings?season=2025&league=${apiId}&team=${teamId}`, { headers: { "x-apisports-key": API_KEY } });
        const data = await res.json();
        if (!data.response || data.response.length === 0) return { position: 10, totalTeams: 20, momentum: 1.0 };

        const standing = data.response[0].league.standings[0][0];
        const position = standing.rank;
        const totalTeams = data.response[0].league.standings[0].length;

        let momentum = 1.0;
        if (position <= 3) momentum = 1.05;
        else if (position <= 6) momentum = 1.03;
        else if (position >= totalTeams - 3) momentum = 1.04;
        else if (position >= totalTeams - 8 && position <= totalTeams - 4) momentum = 0.98;

        return { position, totalTeams, momentum };
    } catch (e) { return { position: 10, totalTeams: 20, momentum: 1.0 }; }
}

async function getFixturesH2H(teamIdH, teamIdA, apiId) {
    try {
        const res = await fetch(`https://v3.football.api-sports.io/fixtures/headtohead?h2h=${teamIdH}-${teamIdA}&last=3`, { headers: { "x-apisports-key": API_KEY } });
        const data = await res.json();
        if (!data.response || data.response.length === 0) return null;

        let h2hShotsH = 0, h2hShotsA = 0, h2hCorners = 0, count = 0;

        data.response.forEach(fixture => {
            if (fixture.statistics && fixture.statistics.length > 0) {
                const homeStats = fixture.statistics[0];
                const awayStats = fixture.statistics[1];
                if (homeStats && homeStats.statistics) {
                    const stats = homeStats.statistics;
                    const shots = stats.find(s => s.type === 'Shots on Goal');
                    const corners = stats.find(s => s.type === 'Corner Kicks');
                    if (shots) h2hShotsH += parseInt(shots.value) || 0;
                    if (corners) h2hCorners += parseInt(corners.value) || 0;
                }
                if (awayStats && awayStats.statistics) {
                    const stats = awayStats.statistics;
                    const shots = stats.find(s => s.type === 'Shots on Goal');
                    if (shots) h2hShotsA += parseInt(shots.value) || 0;
                }
                count++;
            }
        });

        if (count === 0) return null;
        return { avgShotsH: h2hShotsH / count, avgShotsA: h2hShotsA / count, avgCorners: h2hCorners / count, weight: Math.min(count * 0.15, 0.3) };
    } catch (e) { return null; }
}

async function runDeepAnalysis() {
    const resDiv = document.getElementById('results');
    resDiv.classList.remove('hidden');
    resDiv.innerHTML = `
        <div class="loader-container">
            <div class="pulse-text teko">ELABORAZIONE DATI...</div>
            <p style="font-size:12px;color:#64748b;margin-top:8px">Analisi forma, classifica e H2H in corso</p>
        </div>
    `;
    
    resDiv.scrollIntoView({behavior:'smooth', block:'center'});

    try {
        const idH = document.getElementById('homeTeam').value;
        const idA = document.getElementById('awayTeam').value;

        if (!idH || !idA) throw new Error("Seleziona entrambe le squadre");
        if (idH === idA) throw new Error("Le squadre devono essere diverse");

        const leagueInfo = LEAGUE_DATA[currentLeague];
        let apiId = leagueInfo.apiId;

        let statsH, statsA, formH, formA, standH, standA, h2hData;

        try {
            const statsRes = await Promise.all([
                fetch(`https://v3.football.api-sports.io/teams/statistics?league=${apiId}&season=2025&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
                fetch(`https://v3.football.api-sports.io/teams/statistics?league=${apiId}&season=2025&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
            ]);
            statsH = statsRes[0]; statsA = statsRes[1];
            if (!statsH.response || !statsA.response) throw new Error("empty");
        } catch (e) {
            apiId = leagueInfo.oldId;
            const statsRes = await Promise.all([
                fetch(`https://v3.football.api-sports.io/teams/statistics?league=${apiId}&season=2025&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
                fetch(`https://v3.football.api-sports.io/teams/statistics?league=${apiId}&season=2025&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
            ]);
            statsH = statsRes[0]; statsA = statsRes[1];
        }

        [formH, formA, standH, standA, h2hData] = await Promise.all([
            getTeamForm(idH, apiId), getTeamForm(idA, apiId),
            getStandingsMomentum(idH, apiId), getStandingsMomentum(idA, apiId),
            getFixturesH2H(idH, idA, apiId)
        ]);

        const sH = statsH.response; const sA = statsA.response;
        const homeAdv = leagueInfo.homeAdv;

        const xGH_raw = dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || "0.11";
        const xGA_raw = dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || "0.11";
        const xGH = parseFloat(xGH_raw.toString().replace(',', '.'));
        const xGA = parseFloat(xGA_raw.toString().replace(',', '.'));
        const bench = (currentLeague === 7293 || currentLeague === 7338) ? 0.12 : 0.11;

        const formFactorH = formH.formFactor; const formFactorA = formA.formFactor;
        const momentumH = standH.momentum; const momentumA = standA.momentum;

        const shotsH_avg = sH?.shots?.total?.average || 10.5;
        const shotsA_avg = sA?.shots?.total?.average || 9.5;
        const xgFactorH = 0.7 + (xGH / bench) * 0.3;
        const xgFactorA = 0.7 + (xGA / bench) * 0.3;

        let cH = shotsH_avg * xgFactorH * homeAdv * formFactorH * momentumH * 0.95;
        let cA = shotsA_avg * xgFactorA * 1.0 * formFactorA * momentumA * 1.05;

        if (h2hData) {
            cH = cH * (1 - h2hData.weight) + h2hData.avgShotsH * h2hData.weight;
            cA = cA * (1 - h2hData.weight) + h2hData.avgShotsA * h2hData.weight;
        }
        if (formH.avgShots > 0 && Math.abs(formH.avgShots - shotsH_avg) / shotsH_avg > 0.2) cH = cH * 0.7 + formH.avgShots * 0.3;
        if (formA.avgShots > 0 && Math.abs(formA.avgShots - shotsA_avg) / shotsA_avg > 0.2) cA = cA * 0.7 + formA.avgShots * 0.3;
        const totalShots = cH + cA;

        const onTargetH_avg = sH?.shots?.on_goal?.average || (shotsH_avg * 0.34);
        const onTargetA_avg = sA?.shots?.on_goal?.average || (shotsA_avg * 0.34);
        const convRateH = onTargetH_avg / shotsH_avg;
        const convRateA = onTargetA_avg / shotsA_avg;
        const precisionH = convRateH * (0.85 + xGH * 2.5);
        const precisionA = convRateA * (0.85 + xGA * 2.5);

        let s_cH = cH * precisionH;
        let s_cA = cA * precisionA;
        const totalSOT = s_cH + s_cA;

        // CALCOLO CORNER
        const cornersH_avg = sH?.corners?.average || 5.2;
        const cornersA_avg = sA?.corners?.average || 4.4;
        let pCornH = cornersH_avg * homeAdv * formFactorH * momentumH;
        let pCornA = cornersA_avg * 1.0 * formFactorA * momentumA;
        if (h2hData) {
            pCornH = pCornH * (1 - h2hData.weight) + h2hData.avgCorners * h2hData.weight * 0.55;
            pCornA = pCornA * (1 - h2hData.weight) + h2hData.avgCorners * h2hData.weight * 0.45;
        }
        const totalCorners = pCornH + pCornA;

        // CALCOLO CARTELLINI (CON SUPPORTO VALORE ARBITRO)
        const cardsH_avg = sH?.cards?.yellow?.average || 2.1;
        const cardsA_avg = sA?.cards?.yellow?.average || 2.4;
        let refFactor = 1.0;
        if (currentLeague === 7286) {
            const refSelectedVal = document.getElementById('arbitroSelect').value;
            const refParts = refSelectedVal.split(',');
            const refTotal = parseFloat(refParts[0]) || 24.5;
            refFactor = refTotal / 24.5;
        }
        let pCardsH = cardsH_avg * refFactor * (2.0 - formFactorH);
        let pCardsA = cardsA_avg * refFactor * (2.0 - formFactorA);
        const totalCards = pCardsH + pCardsA;

        // CALCOLO FALLI CON NUOVE METRICHE DETTAGLIATE ARBITRO (SOLO SERIE A)
        let totalFouls = 0, pFoulsH = 0, pFoulsA = 0;
        if (currentLeague === 7286) {
            const foulsH_avg = sH?.fouls?.committed?.average || 12.5;
            const foulsA_avg = sA?.fouls?.committed?.average || 11.8;
            
            const refSelectedVal = document.getElementById('arbitroSelect').value;
            const refParts = refSelectedVal.split(',');
            
            const refHomeAverage = parseFloat(refParts[1]) || 11.0;
            const refAwayAverage = parseFloat(refParts[2]) || 13.5;
            
            const refHomeMultiplier = refHomeAverage / 11.5; 
            const refAwayMultiplier = refAwayAverage / 12.5; 

            pFoulsH = foulsH_avg * refHomeMultiplier * (2.0 - formFactorH);
            pFoulsA = foulsA_avg * refAwayMultiplier * (2.0 - formFactorA);
            totalFouls = pFoulsH + pFoulsA;
        }

        // LETTURA INPUT DEGLI SPREAD CORRENTI DELL'UTENTE
        const sprTotalMatch = parseFloat(document.getElementById('sprTotalMatch').value);
        const sprTotalH = parseFloat(document.getElementById('sprTotalH').value);
        const sprTotalA = parseFloat(document.getElementById('sprTotalA').value);

        const sprOTMatch = parseFloat(document.getElementById('sprOTMatch').value);
        const sprOTH = parseFloat(document.getElementById('sprOTH').value);
        const sprOTA = parseFloat(document.getElementById('sprOTA').value);

        const sprCornMatch = parseFloat(document.getElementById('sprCornMatch').value);
        const sprCornH = parseFloat(document.getElementById('sprCornH').value);
        const sprCornA = parseFloat(document.getElementById('sprCornA').value);

        const sprCardsMatch = parseFloat(document.getElementById('sprCardsMatch').value);
        const sprCardsH = parseFloat(document.getElementById('sprCardsH').value);
        const sprCardsA = parseFloat(document.getElementById('sprCardsA').value);

        // STRUTTURAZIONE PREVISIONI E CREAZIONE HTML RISULTATI
        const advTotal = getAdviceAdvanced(totalShots, sprTotalMatch);
        const advTotalH = getAdviceAdvanced(cH, sprTotalH);
        const advTotalA = getAdviceAdvanced(cA, sprTotalA);

        const advOT = getAdviceAdvanced(totalSOT, sprOTMatch);
        const advOTH = getAdviceAdvanced(s_cH, sprOTH);
        const advOTA = getAdviceAdvanced(s_cA, sprOTA);

        const advCorn = getAdviceAdvanced(totalCorners, sprCornMatch);
        const advCornH = getAdviceAdvanced(pCornH, sprCornH);
        const advCornA = getAdviceAdvanced(pCornA, sprCornA);

        const advCards = getAdviceAdvanced(totalCards, sprCardsMatch);
        const advCardsH = getAdviceAdvanced(pCardsH, sprCardsH);
        const advCardsA = getAdviceAdvanced(pCardsA, sprCardsA);

        let finalHTML = `
            <div class="result-card border-green">
                <div class="res-header">
                    <span class="res-label" style="color:#10b981">Tiri Totali Match</span>
                    <span class="badge-pro">PRECISIONE ${advTotal.precision}</span>
                </div>
                <div class="res-value">${totalShots.toFixed(2)}</div>
                <div class="mb-2">${advTotal.html}</div>
                ${renderConfidenceBar(advTotal.confidence)}
                <div class="split-stats">
                    <div class="stat-col">
                        <h4>Home Prediction</h4>
                        <div class="val">${cH.toFixed(1)}</div>
                        <div class="mt-1">${advTotalH.html}</div>
                        ${renderFormBar(formH.results, false)}
                    </div>
                    <div class="stat-col right">
                        <h4>Away Prediction</h4>
                        <div class="val">${cA.toFixed(1)}</div>
                        <div class="mt-1">${advTotalA.html}</div>
                        ${renderFormBar(formA.results, true)}
                    </div>
                </div>
            </div>

            <div class="result-card border-purple">
                <div class="res-header">
                    <span class="res-label" style="color:#a78bfa">Tiri In Porta</span>
                    <span class="badge-pro">PRECISIONE ${advOT.precision}</span>
                </div>
                <div class="res-value">${totalSOT.toFixed(2)}</div>
                <div class="mb-2">${advOT.html}</div>
                ${renderConfidenceBar(advOT.confidence)}
                <div class="split-stats">
                    <div class="stat-col">
                        <h4>Home SOT</h4>
                        <div class="val">${s_cH.toFixed(1)}</div>
                        <div class="mt-1">${advOTH.html}</div>
                    </div>
                    <div class="stat-col right">
                        <h4>Away SOT</h4>
                        <div class="val">${s_cA.toFixed(1)}</div>
                        <div class="mt-1">${advOTA.html}</div>
                    </div>
                </div>
            </div>
        `;

        // INNESTO CARD FALLI SOLO SE SERIE A ATTIVA
        if (currentLeague === 7286) {
            const sprFoulsMatch = parseFloat(document.getElementById('sprFoulsMatch').value);
            const sprFoulsH = parseFloat(document.getElementById('sprFoulsH').value);
            const sprFoulsA = parseFloat(document.getElementById('sprFoulsA').value);

            const advFouls = getAdviceAdvanced(totalFouls, sprFoulsMatch);
            const advFoulsH = getAdviceAdvanced(pFoulsH, sprFoulsH);
            const advFoulsA = getAdviceAdvanced(pFoulsA, sprFoulsA);

            finalHTML += `
                <div class="result-card border-red">
                    <div class="res-header">
                        <span class="res-label" style="color:#f87171">Falli Commessi</span>
                        <span class="badge-pro">PRECISIONE ${advFouls.precision}</span>
                    </div>
                    <div class="res-value">${totalFouls.toFixed(2)}</div>
                    <div class="mb-2">${advFouls.html}</div>
                    ${renderConfidenceBar(advFouls.confidence)}
                    <div class="split-stats">
                        <div class="stat-col">
                            <h4>Home Fouls</h4>
                            <div class="val">${pFoulsH.toFixed(1)}</div>
                            <div class="mt-1">${advFoulsH.html}</div>
                        </div>
                        <div class="stat-col right">
                            <h4>Away Fouls</h4>
                            <div class="val">${pFoulsA.toFixed(1)}</div>
                            <div class="mt-1">${advFoulsA.html}</div>
                        </div>
                    </div>
                </div>
            `;
        }

        // AGGIUNTA CARDS CORNER E CARTELLINI
        finalHTML += `
            <div class="result-card border-cyan">
                <div class="res-header">
                    <span class="res-label" style="color:#22d3ee">Corner Totali</span>
                    <span class="badge-pro">PRECISIONE ${advCorn.precision}</span>
                </div>
                <div class="res-value">${totalCorners.toFixed(2)}</div>
                <div class="mb-2">${advCorn.html}</div>
                ${renderConfidenceBar(advCorn.confidence)}
                <div class="split-stats">
                    <div class="stat-col">
                        <h4>Home Corners</h4>
                        <div class="val">${pCornH.toFixed(1)}</div>
                        <div class="mt-1">${advCornH.html}</div>
                    </div>
                    <div class="stat-col right">
                        <h4>Away Corners</h4>
                        <div class="val">${pCornA.toFixed(1)}</div>
                        <div class="mt-1">${advCornA.html}</div>
                    </div>
                </div>
            </div>

            <div class="result-card border-yellow">
                <div class="res-header">
                    <span class="res-label" style="color:#fbbf24">Cartellini Gialli</span>
                    <span class="badge-pro">PRECISIONE ${advCards.precision}</span>
                </div>
                <div class="res-value">${totalCards.toFixed(2)}</div>
                <div class="mb-2">${advCards.html}</div>
                ${renderConfidenceBar(advCards.confidence)}
                <div class="split-stats">
                    <div class="stat-col">
                        <h4>Home Cards</h4>
                        <div class="val">${pCardsH.toFixed(1)}</div>
                        <div class="mt-1">${advCardsH.html}</div>
                    </div>
                    <div class="stat-col right">
                        <h4>Away Cards</h4>
                        <div class="val">${pCardsA.toFixed(1)}</div>
                        <div class="mt-1">${advCardsA.html}</div>
                    </div>
                </div>
            </div>
        `;

        resDiv.innerHTML = finalHTML;
    } catch (e) {
        resDiv.innerHTML = `
            <div class="status-msg status-err" style="margin:20px 0">
                Errore Analisi: ${e.message}
            </div>
        `;
    }
}

// Avvio Iniziale automatico
loadData();
</script>

</body>
</html>
"""

components.html(html_code, height=1800, scrolling=True)
