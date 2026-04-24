import streamlit as st

# File: probetai_streamlit.py

st.set_page_config(page_title="ProBet AI V3 - FULL API AUTO", layout="wide")

# CSS PERSONALIZZATO PER LOOK PROFESSIONALE
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Teko:wght@400;600&family=Inter:wght@400;600;700;800&display=swap');
    
    .main { background: #0b1120; color: #f8fafc; font-family: 'Inter', sans-serif; }
    
    /* Loader */
    .loader {
        border: 2px solid #1e293b;
        border-top: 2px solid #3b82f6;
        border-radius: 50%;
        width: 14px;
        height: 14px;
        animation: spin 1s linear infinite;
        display: inline-block;
        margin-right: 8px;
    }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

    /* Cards Risultati */
    .value-box {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .val-top { background: linear-gradient(145deg, rgba(16, 185, 129, 0.1), rgba(30, 41, 59, 0.5)); border-color: #10b981; box-shadow: 0 0 20px rgba(16, 185, 129, 0.15); }
    .val-good { background: linear-gradient(145deg, rgba(59, 130, 246, 0.1), rgba(30, 41, 59, 0.5)); border-color: #3b82f6; }
    
    .res-text { font-family: 'Teko', sans-serif; font-size: 38px; line-height: 1; margin: 8px 0; letter-spacing: 1px; font-weight: 600; }
    
    .tag-pill {
        position: absolute; top: 12px; right: 12px;
        background: #10b981; color: white; padding: 2px 8px;
        border-radius: 6px; font-size: 9px; font-weight: 900; letter-spacing: 1px;
    }
</style>

<div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:40px;">
    <div style="display:flex; align-items:center; gap:15px;">
        <h1 style="font-family:'Teko'; font-size:48px; margin:0; letter-spacing:2px; color:white;">PROBET <span style="color:#3b82f6">AI</span></h1>
        <div style="background:#1e293b; padding:4px 10px; border-radius:6px; font-size:12px; font-weight:900; color:#94a3b8; border:1px solid #334155;">V3.1</div>
    </div>
    <div id="status-display" style="display:flex; align-items:center; gap:10px; background:rgba(30,41,59,0.5); padding:8px 16px; border-radius:100px; border:1px solid #334155;">
        <div class="loader"></div> <span style="font-size:11px; font-weight:900; color:#94a3b8; text-transform:uppercase;">Inizializzazione...</span>
    </div>
</div>

<!-- LEAGUE SWITCHER -->
<div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:12px; margin-bottom:30px;">
    <button onclick="switchLeague('SERIE_A')" id="btn-ser" style="background:#3b82f6; color:white; border:none; padding:12px; border-radius:12px; font-weight:800; font-size:12px; cursor:pointer;">SERIE A</button>
    <button onclick="switchLeague('PREMIER')" id="btn-pre" style="background:#1e293b; color:#94a3b8; border:none; padding:12px; border-radius:12px; font-weight:800; font-size:12px; cursor:pointer;">PREMIER</button>
    <button onclick="switchLeague('LIGA')" id="btn-lig" style="background:#1e293b; color:#94a3b8; border:none; padding:12px; border-radius:12px; font-weight:800; font-size:12px; cursor:pointer;">LIGA</button>
</div>

<!-- INPUT PANEL -->
<div style="background:rgba(15, 23, 42, 0.5); border:1px solid #1e293b; border-radius:24px; padding:30px; margin-bottom:40px;">
    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:25px; margin-bottom:25px;">
        <div>
            <label style="font-size:10px; font-weight:900; color:#64748b; text-transform:uppercase; margin-bottom:8px; display:block; letter-spacing:1px;">Match Home</label>
            <select id="home-team" style="width:100%; background:#0f172a; border:2px solid #1e293b; color:white; padding:14px; border-radius:14px; font-weight:700; outline:none;"></select>
        </div>
        <div>
            <label style="font-size:10px; font-weight:900; color:#64748b; text-transform:uppercase; margin-bottom:8px; display:block; letter-spacing:1px;">Match Away</label>
            <select id="away-team" style="width:100%; background:#0f172a; border:2px solid #1e293b; color:white; padding:14px; border-radius:14px; font-weight:700; outline:none;"></select>
        </div>
    </div>

    <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:20px; margin-bottom:30px;">
        <div style="background:#0f172a; padding:15px; border-radius:16px; border:1px solid #1e293b;">
             <label style="font-size:9px; font-weight:900; color:#475569; display:block; text-transform:uppercase; margin-bottom:5px;">Bookmaker Line Falli</label>
             <input type="number" id="line-f-match" value="23.5" step="1" style="background:none; border:none; color:white; font-size:20px; font-family:'Teko'; width:100%; outline:none;">
        </div>
        <div style="background:#0f172a; padding:15px; border-radius:16px; border:1px solid #1e293b;">
             <label style="font-size:9px; font-weight:900; color:#475569; display:block; text-transform:uppercase; margin-bottom:5px;">Bookmaker Line Tiri</label>
             <input type="number" id="line-t-match" value="24.5" step="1" style="background:none; border:none; color:white; font-size:20px; font-family:'Teko'; width:100%; outline:none;">
        </div>
        <div style="background:#0f172a; padding:15px; border-radius:16px; border:1px solid #1e293b;">
             <label style="font-size:9px; font-weight:900; color:#475569; display:block; text-transform:uppercase; margin-bottom:5px;">Bookmaker Line Porta</label>
             <input type="number" id="line-tp-match" value="8.5" step="1" style="background:none; border:none; color:white; font-size:20px; font-family:'Teko'; width:100%; outline:none;">
        </div>
    </div>

    <button id="btn-calc" onclick="processAnalysis()" style="width:100%; background:#2563eb; color:white; border:none; padding:18px; border-radius:16px; font-family:'Inter'; font-weight:800; font-size:15px; text-transform:uppercase; letter-spacing:1px; cursor:pointer; transition:all 0.2s;">Analizza Dati</button>
</div>

<!-- RESULTS AREA -->
<div id="results-area" class="hidden">
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
        <div style="width:4px; height:20px; background:#ef4444; border-radius:2px;"></div>
        <h3 style="font-family:'Teko'; font-size:24px; text-transform:uppercase; margin:0; letter-spacing:1px;">Analisi Falli</h3>
    </div>
    <div id="res-grid-falli" style="display:grid; grid-template-columns: repeat(3, 1fr); gap:20px; margin-bottom:40px;"></div>

    <div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
        <div style="width:4px; height:20px; background:#3b82f6; border-radius:2px;"></div>
        <h3 style="font-family:'Teko'; font-size:24px; text-transform:uppercase; margin:0; letter-spacing:1px;">Analisi Tiri</h3>
    </div>
    <div id="res-grid-tiri" style="display:grid; grid-template-columns: repeat(3, 1fr); gap:20px; margin-bottom:20px;"></div>
    <div id="res-grid-tp" style="display:grid; grid-template-columns: repeat(3, 1fr); gap:20px; margin-bottom:40px;"></div>
</div>

<script src="https://unpkg.com/lucide@latest"></script>
<script>
// ==========================================
// 🟢 CONFIG API & LOGICA
// ==========================================
const API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3"; 
const LEAGUE_IDS = { SERIE_A: 135, LIGA: 140, PREMIER: 39 };

let DB = { teams: [], statsCache: {} };
let CUR_L = 'SERIE_A';
let SEASON = 2025;

document.addEventListener('DOMContentLoaded', () => {
    switchLeague('SERIE_A');
    lucide.createIcons();
});

async function switchLeague(l) {
    CUR_L = l;
    const status = document.getElementById('status-display');
    const resultArea = document.getElementById('results-area');
    if(resultArea) resultArea.classList.add('hidden');
    
    // UI Feedback
    ['btn-ser','btn-pre','btn-lig'].forEach(id => {
        const b = document.getElementById(id);
        b.style.background = '#1e293b';
        b.style.color = '#94a3b8';
    });
    const activeBtn = document.getElementById(`btn-${l.substring(0,3).toLowerCase()}`);
    activeBtn.style.background = '#3b82f6';
    activeBtn.style.color = 'white';

    status.innerHTML = `<div class="loader"></div> <span style="font-size:11px; font-weight:900; color:#94a3b8; text-transform:uppercase;">Connessione ${l}...</span>`;
    
    const trySeason = async (year) => {
        try {
            const url = `https://v3.football.api-sports.io/teams?league=${LEAGUE_IDS[l]}&season=${year}`;
            const res = await fetch(url, { headers: { "x-apisports-key": API_KEY } });
            const data = await res.json();
            return (data.response && data.response.length > 0) ? data.response : null;
        } catch (e) { return null; }
    };

    try {
        let res = await trySeason(2025);
        SEASON = 2025;
        if (!res) {
            res = await trySeason(2024);
            SEASON = 2024;
        }
        if (!res) throw new Error("Dati non trovati su API Sports");

        DB.teams = res.map(r => ({ id: r.team.id, name: r.team.name })).sort((a,b) => a.name.localeCompare(b.name));

        const h = document.getElementById('home-team'), a = document.getElementById('away-team');
        h.innerHTML = ''; a.innerHTML = '';
        DB.teams.forEach(t => { 
            h.add(new Option(t.name.toUpperCase(), t.id)); 
            a.add(new Option(t.name.toUpperCase(), t.id)); 
        });
        if (DB.teams.length > 1) a.selectedIndex = 1;

        status.innerHTML = `<span style="width:10px; height:10px; background:#10b981; border-radius:50%;"></span><span style="font-size:11px; font-weight:900; color:#10b981; text-transform:uppercase;">${l} ${SEASON} OK</span>`;
    } catch(err) {
        status.innerHTML = `<span style="font-size:11px; font-weight:900; color:#ef4444; text-transform:uppercase;">ERRORE API</span>`;
    }
}

async function fetchStats(teamId) {
    const cacheKey = `${CUR_L}_${SEASON}_${teamId}`;
    if (DB.statsCache[cacheKey]) return DB.statsCache[cacheKey];

    const res = await fetch(`https://v3.football.api-sports.io/teams/statistics?league=${LEAGUE_IDS[CUR_L]}&season=${SEASON}&team=${teamId}`, {
        headers: { "x-apisports-key": API_KEY }
    });
    const data = await res.json();
    DB.statsCache[cacheKey] = data.response;
    return data.response;
}

async function processAnalysis() {
    const btn = document.getElementById('btn-calc');
    const hId = document.getElementById('home-team').value;
    const aId = document.getElementById('away-team').value;
    const hName = document.getElementById('home-team').options[document.getElementById('home-team').selectedIndex].text;
    const aName = document.getElementById('away-team').options[document.getElementById('away-team').selectedIndex].text;

    btn.disabled = true;
    btn.innerHTML = `<div class="loader"></div> ELABORAZIONE...`;

    try {
        const [hStats, aStats] = await Promise.all([fetchStats(hId), fetchStats(aId)]);

        if (!hStats || !aStats || !hStats.fixtures || !aStats.fixtures) {
            throw new Error("Dati non disponibili per questa stagione");
        }

        // Calcolo Medie Reali Casa / Fuori
        const gH = hStats.fixtures.played.home || 1;
        const gA = aStats.fixtures.played.away || 1;

        // ESTRAZIONE DATI FALLI
        const fCommH = (hStats.fouls?.committed?.total?.home || 12 * gH) / gH;
        const fSubA = (aStats.fouls?.drawn?.total?.away || 12 * gA) / gA;
        const eFH = (fCommH + fSubA) / 2;

        const fCommA = (aStats.fouls?.committed?.total?.away || 12 * gA) / gA;
        const fSubH = (hStats.fouls?.drawn?.total?.home || 12 * gH) / gH;
        const eFA = (fCommA + fSubH) / 2;

        // ESTRAZIONE DATI TIRI (Se API non dà i subiti per team stats, usiamo medie prudenti)
        const tFattiH = (hStats.shots?.total?.home || 13 * gH) / gH;
        const tSubA = (aStats.shots?.total?.away || 12 * gA) * 0.95 / gA; 
        const eTH = (tFattiH + tSubA) / 2;

        const tFattiA = (aStats.shots?.total?.away || 11 * gA) / gA;
        const tSubH = (hStats.shots?.total?.home || 12 * gH) * 0.9 / gH;
        const eTA = (tFattiA + tSubH) / 2;

        // ESTRAZIONE DATI IN PORTA
        const tpFattiH = (hStats.shots?.on_goal?.home || 4.5 * gH) / gH;
        const tpSubA = (aStats.shots?.on_goal?.away || 4 * gA) * 0.85 / gA;
        const ePH = (tpFattiH + tpSubA) / 2;

        const tpFattiA = (aStats.shots?.on_goal?.away || 3.5 * gA) / gA;
        const tpSubH = (hStats.shots?.on_goal?.home || 4 * gH) * 0.8 / gH;
        const ePA = (tpFattiA + tpSubH) / 2;

        renderResults(hName, aName, eFH, eFA, eTH, eTA, ePH, ePA);
        document.getElementById('results-area').classList.remove('hidden');
        lucide.createIcons();
    } catch(err) {
        alert("Errore API Sports: Dati non ancora disponibili per questa stagione.");
    } finally {
        btn.disabled = false;
        btn.innerHTML = "Analizza Dati";
    }
}

function renderResults(h, a, efh, efa, eth, eta, eph, epa) {
    const lF = parseFloat(document.getElementById('line-f-match').value);
    const lT = parseFloat(document.getElementById('line-t-match').value);
    const lP = parseFloat(document.getElementById('line-tp-match').value);

    document.getElementById('res-grid-falli').innerHTML = createCard("MATCH FALLI", efh+efa, lF) + createCard(h, efh, lF/2) + createCard(a, efa, lF/2);
    document.getElementById('res-grid-tiri').innerHTML = createCard("MATCH TIRI TOT", eth+eta, lT) + createCard(h, eth, 12.5) + createCard(a, eta, 11.5);
    document.getElementById('res-grid-tp').innerHTML = createCard("PORTA TOTALE", eph+epa, lP) + createCard(h, eph, 4.5) + createCard(a, epa, 3.5);
}

function createCard(title, val, line) {
    const diff = val - line;
    let style = "", tag = "", rec = "NO EDGE";
    
    if(diff >= 1.5) { style = "val-top"; tag = "TOP"; rec = "OVER " + line; }
    else if(diff >= 0.4) { style = "val-good"; tag = "GOOD"; rec = "OVER " + line; }
    else if(diff <= -1.5) { style = "val-top"; tag = "TOP"; rec = "UNDER " + line; }
    else if(diff <= -0.4) { style = "val-good"; tag = "GOOD"; rec = "UNDER " + line; }

    return `
        <div class="value-box ${style}">
            ${tag ? `<div class="tag-pill">${tag}</div>` : ''}
            <div style="font-size:10px; font-weight:900; color:#64748b; text-transform:uppercase; letter-spacing:1px; margin-bottom:5px;">${title}</div>
            <div class="res-text">${rec}</div>
            <div style="font-size:11px; font-weight:800; color:#94a3b8; opacity:0.8;">AI: ${val.toFixed(2)}</div>
        </div>
    `;
}
</script>
""", unsafe_allow_html=True)
