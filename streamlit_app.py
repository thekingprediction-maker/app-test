import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI V4 PRO - TOTAL ANALYST", layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600;700&family=Inter:wght@400;500;700;900&display=swap');
        body { background: #020617; color: white; font-family: 'Inter', sans-serif; }
        .teko { font-family: 'Teko', sans-serif; }
        .card-premium { background: #1e293b; border-radius: 24px; padding: 30px; border: 1px solid #334155; }
        select, input { background: #0f172a; border: 1px solid #475569; color: white; padding: 12px; width: 100%; border-radius: 12px; font-weight: 700; font-size: 14px; outline: none; }
        .btn-analizza { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 50%, #1d4ed8 100%); width: 100%; padding: 22px; border-radius: 16px; font-weight: 900; text-transform: uppercase; cursor: pointer; transition: all 0.3s; margin-top: 20px; border: none; color: white; letter-spacing: 2px; }
        .btn-analizza:hover { transform: translateY(-3px); box-shadow: 0 15px 50px rgba(59,130,246,0.5); }
        .res-box { background: #0f172a; border-radius: 20px; padding: 28px; border-left: 5px solid; margin-bottom: 18px; position: relative; overflow: hidden; }
        .res-box::before { content: ''; position: absolute; top: 0; right: 0; width: 200px; height: 200px; background: radial-gradient(circle, rgba(59,130,246,0.08) 0%, transparent 70%); }
        .advice-tag { display: inline-block; padding: 5px 16px; border-radius: 10px; font-size: 14px; font-weight: 900; margin-left: 14px; text-transform: uppercase; letter-spacing: 0.5px; }
        .over-tag { background: linear-gradient(135deg, #10b981, #059669); color: white; box-shadow: 0 4px 20px rgba(16,185,129,0.4); }
        .under-tag { background: linear-gradient(135deg, #ef4444, #dc2626); color: white; box-shadow: 0 4px 20px rgba(239,68,68,0.4); }
        .label-spread { font-size: 11px; font-weight: 900; color: #94a3b8; text-transform: uppercase; margin-bottom: 6px; display: block; letter-spacing: 1.2px; }
        .league-btn { cursor: pointer; padding: 14px; border-radius: 12px; font-weight: 900; border: 1px solid #334155; text-align: center; font-size: 12px; letter-spacing: 0.5px; transition: all 0.3s; background: #0f172a; }
        .league-active { background: linear-gradient(135deg, #3b82f6, #2563eb); border-color: #3b82f6; color: white; box-shadow: 0 0 25px rgba(59, 130, 246, 0.5); }
        .grid-spreads { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; padding-top: 20px; border-top: 1px solid #334155; margin-bottom: 20px; }
        .status-msg { font-size: 12px; font-weight: 700; padding: 10px 16px; border-radius: 10px; margin-bottom: 16px; display: none; }
        .status-ok { background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid #10b981; }
        .status-err { background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid #ef4444; }
        .confidence-bar { height: 8px; border-radius: 4px; background: #1e293b; margin-top: 14px; overflow: hidden; }
        .confidence-fill { height: 100%; border-radius: 4px; transition: width 1s ease; }
        .precision-badge { position: absolute; top: 20px; right: 20px; font-size: 11px; font-weight: 900; padding: 5px 12px; border-radius: 8px; background: rgba(59,130,246,0.15); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }
        .form-indicator { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 4px; }
        .form-W { background: #10b981; }
        .form-D { background: #f59e0b; }
        .form-L { background: #ef4444; }
        .momentum-bar { display: flex; gap: 3px; margin-top: 6px; }
        .momentum-dot { width: 22px; height: 22px; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 900; }
        .standings-info { font-size: 12px; color: #94a3b8; margin-top: 8px; font-weight: 500; }
        .pro-badge { background: linear-gradient(135deg, #f59e0b, #d97706); color: #020617; font-size: 10px; font-weight: 900; padding: 3px 10px; border-radius: 6px; text-transform: uppercase; letter-spacing: 1px; }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-5xl mx-auto">
        <div class="text-center mb-10">
            <h1 class="text-6xl font-black teko tracking-widest text-white uppercase italic">PROBET <span class="text-blue-500">AI V4</span> <span class="pro-badge">PRO</span></h1>
            <p class="text-blue-400 font-bold text-xs tracking-widest uppercase italic mt-2">Elite Multi-League Analysis System - Stagione 2025/2026</p>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div id="btn-7286" class="league-btn league-active" onclick="switchLeague(7286)">SERIE A</div>
            <div id="btn-7293" class="league-btn" onclick="switchLeague(7293)">PREMIER LEAGUE</div>
            <div id="btn-7338" class="league-btn" onclick="switchLeague(7338)">BUNDESLIGA</div>
            <div id="btn-7351" class="league-btn" onclick="switchLeague(7351)">LA LIGA</div>
        </div>

        <div class="card-premium mb-8">
            <div id="statusMessage" class="status-msg"></div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div><label class="label-spread text-blue-400">Home Team</label><select id="homeTeam"></select></div>
                <div><label class="label-spread text-blue-400">Away Team</label><select id="awayTeam"></select></div>
                <div id="arbitroContainer"><label class="label-spread text-yellow-500 italic">Arbitro (Serie A)</label><select id="arbitroSelect"><option value="24.5">Scegli...</option></select></div>
            </div>

            <div class="grid-spreads">
                <div><label class="label-spread text-emerald-400">Spread Tiri Tot</label><input type="number" id="sprTotalMatch" step="0.5" value="23.5"></div>
                <div><label class="label-spread text-emerald-400">Spread Tiri Casa</label><input type="number" id="sprTotalH" step="0.5" value="12.5"></div>
                <div><label class="label-spread text-emerald-400">Spread Tiri Osp</label><input type="number" id="sprTotalA" step="0.5" value="10.5"></div>
            </div>

            <div class="grid-spreads">
                <div><label class="label-spread text-purple-400">Spread Porta Tot</label><input type="number" id="sprOTMatch" step="0.5" value="8.5"></div>
                <div><label class="label-spread text-purple-400">Spread Porta Casa</label><input type="number" id="sprOTH" step="0.5" value="4.5"></div>
                <div><label class="label-spread text-purple-400">Spread Porta Osp</label><input type="number" id="sprOTA" step="0.5" value="3.5"></div>
            </div>

            <div id="foulsInputs" class="grid-spreads">
                <div><label class="label-spread text-red-400">Spread Falli Tot</label><input type="number" id="sprFoulsMatch" step="0.5" value="24.5"></div>
                <div><label class="label-spread text-red-400">Spread Falli Casa</label><input type="number" id="sprFoulsH" step="0.5" value="12.5"></div>
                <div><label class="label-spread text-red-400">Spread Falli Osp</label><input type="number" id="sprFoulsA" step="0.5" value="11.5"></div>
            </div>

            <div class="grid-spreads">
                <div><label class="label-spread text-cyan-400">Spread Corner Tot</label><input type="number" id="sprCornMatch" step="0.5" value="9.5"></div>
                <div><label class="label-spread text-cyan-400">Spread Corner Casa</label><input type="number" id="sprCornH" step="0.5" value="5.5"></div>
                <div><label class="label-spread text-cyan-400">Spread Corner Osp</label><input type="number" id="sprCornA" step="0.5" value="4.5"></div>
            </div>

            <div class="grid-spreads">
                <div><label class="label-spread text-yellow-400">Spread Gialli Tot</label><input type="number" id="sprCardsMatch" step="0.5" value="4.5"></div>
                <div><label class="label-spread text-yellow-400">Spread Gialli Casa</label><input type="number" id="sprCardsH" step="0.5" value="2.5"></div>
                <div><label class="label-spread text-yellow-400">Spread Gialli Osp</label><input type="number" id="sprCardsA" step="0.5" value="2.5"></div>
            </div>

            <form id="adForm" action="https://probetai.com/mostra_pubblicita" method="GET" target="_blank" style="display:none;">
                <input type="hidden" name="trigger" value="ad">
            </form>

            <button onclick="triggerAdAndCalculate()" class="btn-analizza shadow-xl italic teko text-2xl tracking-widest">GENERA ANALISI ELITE PRO</button>
        </div>
        <div id="results" class="space-y-6 hidden pb-20"></div>
    </div>

<script>
const API_KEY = "8546a3b44515070cb8e4b6a8f620ab5b";
const BASE_CSV_URL = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/";
const REFS_FILE = "ARBITRI_SERIE_A%20-%20Foglio1.csv";
let currentLeague = 7286, dbXG = [];

const LEAGUE_DATA = {
    7286: { name: "SERIE A", file: "DATABASE_AVANZATO_SERIEA_2025.csv", oldId: 135, apiId: 7286, homeAdv: 1.08 },
    7293: { name: "PREMIER LEAGUE", file: "DATABASE_AVANZATO_PREMIER_2025.csv", oldId: 39, apiId: 7293, homeAdv: 1.05 },
    7338: { name: "BUNDESLIGA", file: "DATABASE_AVANZATO_BUNDES_2025.csv", oldId: 78, apiId: 7338, homeAdv: 1.12 },
    7351: { name: "LA LIGA", file: "DATABASE_AVANZATO_LALIGA_2025.csv", oldId: 140, apiId: 7351, homeAdv: 1.06 }
};

function setStatus(msg, type) {
    const el = document.getElementById('statusMessage');
    if (!msg) { el.style.display = 'none'; return; }
    el.textContent = msg;
    el.className = 'status-msg status-' + type;
    el.style.display = 'block';
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
    document.getElementById('arbitroContainer').style.display = isSerieA ? "block" : "none";
    document.getElementById('foulsInputs').style.display = isSerieA ? "grid" : "none";
    loadData();
}

function loadData() {
    const leagueInfo = LEAGUE_DATA[currentLeague];
    Papa.parse(BASE_CSV_URL + leagueInfo.file, { 
        download: true, 
        header: true, 
        skipEmptyLines: true, 
        complete: (r) => { 
            dbXG = r.data; 
            loadTeams(); 
        },
        error: (err) => {
            console.error("Errore CSV:", err);
            setStatus("Errore caricamento database CSV", 'err');
        }
    });

    if(currentLeague === 7286) {
        Papa.parse(BASE_CSV_URL + REFS_FILE, { 
            download: true, 
            header: true, 
            skipEmptyLines: true, 
            delimiter: ";", 
            complete: (r) => {
                const sel = document.getElementById('arbitroSelect'); 
                sel.innerHTML = '<option value="24.5">Scegli Arbitro...</option>';
                r.data.forEach(row => {
                    let name = row.Arbitro || Object.values(row)[0];
                    let val = row["Media Totale"] || Object.values(row)[2];
                    if(name && val) sel.add(new Option(name, val.toString().replace(',', '.')));
                });
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

        let res = await fetch(`https://v3.football.api-sports.io/teams?league=${apiId}&season=2025`, { 
            headers: { "x-apisports-key": API_KEY } 
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        let data = await res.json();

        if (!data.response || data.response.length === 0) {
            apiId = leagueInfo.oldId;
            res = await fetch(`https://v3.football.api-sports.io/teams?league=${apiId}&season=2025`, { 
                headers: { "x-apisports-key": API_KEY } 
            });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            data = await res.json();
        }

        if (!data.response || data.response.length === 0) {
            throw new Error("Nessuna squadra trovata");
        }

        h.innerHTML = ""; a.innerHTML = "";
        h.add(new Option("-- Seleziona Casa --", ""));
        a.add(new Option("-- Seleziona Ospite --", ""));

        data.response.sort((x,y) => x.team.name.localeCompare(y.team.name)).forEach(t => {
            h.add(new Option(t.team.name, t.team.id)); 
            a.add(new Option(t.team.name, t.team.id));
        });

        setStatus("", "");

    } catch (e) {
        h.innerHTML = '<option>Errore caricamento</option>';
        a.innerHTML = '<option>Errore caricamento</option>';
        setStatus(`Errore: ${e.message}`, 'err');
    }
}

// ============================================
// FUNZIONI UTILITY PRO
// ============================================

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
        html: `<span class="advice-tag ${isOver ? 'over-tag' : 'under-tag'}">${direction} ${spread} (${displayConf.toFixed(1)}%)</span>`,
        confidence: displayConf,
        isOver: isOver,
        precision: precisionLabel
    };
}

function renderConfidenceBar(confidence) {
    let color = confidence >= 75 ? '#10b981' : confidence >= 60 ? '#f59e0b' : '#ef4444';
    return `<div class="confidence-bar"><div class="confidence-fill" style="width:${confidence}%;background:${color}"></div></div>`;
}

function renderFormBar(results) {
    if (!results || results.length === 0) return '';
    let html = '<div class="momentum-bar">';
    results.slice(0, 5).reverse().forEach(r => {
        const outcome = r === 'W' ? 'V' : r === 'D' ? 'N' : 'S';
        const color = r === 'W' ? '#10b981' : r === 'D' ? '#f59e0b' : '#ef4444';
        html += `<div class="momentum-dot" style="background:${color};color:white">${outcome}</div>`;
    });
    html += '</div>';
    return html;
}

// ============================================
// RECUPERO DATI AVANZATI PRO
// ============================================

async function getTeamForm(teamId, apiId) {
    // Recupera ultime 5 partite giocate dalla squadra
    try {
        const res = await fetch(`https://v3.football.api-sports.io/fixtures?team=${teamId}&season=2025&league=${apiId}&last=5`, {
            headers: { "x-apisports-key": API_KEY }
        });
        const data = await res.json();
        if (!data.response || data.response.length === 0) return { results: [], formFactor: 1.0, avgShots: 0, avgCorners: 0, avgCards: 0 };

        let results = [];
        let totalShots = 0, totalCorners = 0, totalCards = 0;
        let count = 0;

        data.response.forEach(fixture => {
            const isHome = fixture.teams.home.id == teamId;
            const teamSide = isHome ? fixture.teams.home : fixture.teams.away;
            const opponentSide = isHome ? fixture.teams.away : fixture.teams.home;

            // Risultato
            if (teamSide.winner === true) results.push('W');
            else if (teamSide.winner === false) results.push('L');
            else results.push('D');

            // Statistiche dalla fixture se disponibili
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

        // Calcola fattore forma (W=1.08, D=1.0, L=0.92)
        let formFactor = 1.0;
        results.forEach((r, i) => {
            const weight = (i + 1) / 5; // partite recenti pesano di più
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
    } catch (e) {
        console.error("Errore forma:", e);
        return { results: [], formFactor: 1.0, avgShots: 0, avgCorners: 0, avgCards: 0 };
    }
}

async function getStandingsMomentum(teamId, apiId) {
    // Recupera posizione in classifica e momentum
    try {
        const res = await fetch(`https://v3.football.api-sports.io/standings?season=2025&league=${apiId}&team=${teamId}`, {
            headers: { "x-apisports-key": API_KEY }
        });
        const data = await res.json();
        if (!data.response || data.response.length === 0) return { position: 10, totalTeams: 20, momentum: 1.0 };

        const standing = data.response[0].league.standings[0][0];
        const position = standing.rank;
        const totalTeams = data.response[0].league.standings[0].length;

        // Momentum: squadre in zona alta hanno più motivazione
        let momentum = 1.0;
        if (position <= 3) momentum = 1.05; // lotta scudetto/Europe
        else if (position <= 6) momentum = 1.03; // zona Europa
        else if (position >= totalTeams - 3) momentum = 1.04; // lotta salvezza
        else if (position >= totalTeams - 8 && position <= totalTeams - 4) momentum = 0.98; // zona grigia

        return { position, totalTeams, momentum };
    } catch (e) {
        return { position: 10, totalTeams: 20, momentum: 1.0 };
    }
}

async function getPredictions(teamIdH, teamIdA, apiId) {
    // Recupera previsioni ML dell'API
    try {
        const res = await fetch(`https://v3.football.api-sports.io/predictions?fixture=${teamIdH}-${teamIdA}`, {
            headers: { "x-apisports-key": API_KEY }
        });
        // Nota: predictions API richiede fixture ID, non team ID. 
        // Per semplicità, usiamo un approccio alternativo con fixtures
        return null;
    } catch (e) {
        return null;
    }
}

async function getFixturesH2H(teamIdH, teamIdA, apiId) {
    // Recupera ultimi 3 incontri diretti (non 5 anni, solo stagione corrente + precedente)
    try {
        const res = await fetch(`https://v3.football.api-sports.io/fixtures/headtohead?h2h=${teamIdH}-${teamIdA}&last=3`, {
            headers: { "x-apisports-key": API_KEY }
        });
        const data = await res.json();
        if (!data.response || data.response.length === 0) return null;

        let h2hShotsH = 0, h2hShotsA = 0, h2hCorners = 0, h2hCards = 0;
        let count = 0;

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
        return {
            avgShotsH: h2hShotsH / count,
            avgShotsA: h2hShotsA / count,
            avgCorners: h2hCorners / count,
            weight: Math.min(count * 0.15, 0.3) // max 30% peso H2H
        };
    } catch (e) {
        return null;
    }
}

// ============================================
// ANALISI ELITE PRO
// ============================================

async function runDeepAnalysis() {
    const resDiv = document.getElementById('results');
    resDiv.innerHTML = "<div class='text-center py-20 animate-pulse text-blue-500 font-black teko text-3xl uppercase tracking-widest'>ANALISI ELITE PRO IN CORSO...<br><span class='text-lg font-inter text-slate-400'>Recupero forma, classifica e statistiche avanzate</span></div>";
    resDiv.classList.remove('hidden');

    try {
        const idH = document.getElementById('homeTeam').value;
        const idA = document.getElementById('awayTeam').value;

        if (!idH || !idA) throw new Error("Seleziona entrambe le squadre");
        if (idH === idA) throw new Error("Le squadre devono essere diverse");

        const leagueInfo = LEAGUE_DATA[currentLeague];
        let apiId = leagueInfo.apiId;

        // === FASE 1: Recupero parallelo di TUTTI i dati avanzati ===
        let statsH, statsA, formH, formA, standH, standA, h2hData;

        try {
            // Statistiche base
            const statsRes = await Promise.all([
                fetch(`https://v3.football.api-sports.io/teams/statistics?league=${apiId}&season=2025&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
                fetch(`https://v3.football.api-sports.io/teams/statistics?league=${apiId}&season=2025&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
            ]);
            statsH = statsRes[0]; statsA = statsRes[1];

            // Se vuoto, fallback a ID standard
            if (!statsH.response || !statsA.response) throw new Error("empty");
        } catch (e) {
            apiId = leagueInfo.oldId;
            const statsRes = await Promise.all([
                fetch(`https://v3.football.api-sports.io/teams/statistics?league=${apiId}&season=2025&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
                fetch(`https://v3.football.api-sports.io/teams/statistics?league=${apiId}&season=2025&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
            ]);
            statsH = statsRes[0]; statsA = statsRes[1];
        }

        // Recupero dati avanzati in parallelo
        [formH, formA, standH, standA, h2hData] = await Promise.all([
            getTeamForm(idH, apiId),
            getTeamForm(idA, apiId),
            getStandingsMomentum(idH, apiId),
            getStandingsMomentum(idA, apiId),
            getFixturesH2H(idH, idA, apiId)
        ]);

        const sH = statsH.response; 
        const sA = statsA.response;
        const homeAdv = leagueInfo.homeAdv;

        // === FASE 2: Calcoli con fattori PRO ===

        // xG dal CSV
        const xGH_raw = dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || "0.11";
        const xGA_raw = dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || "0.11";
        const xGH = parseFloat(xGH_raw.toString().replace(',', '.'));
        const xGA = parseFloat(xGA_raw.toString().replace(',', '.'));
        const bench = (currentLeague === 7293 || currentLeague === 7338) ? 0.12 : 0.11;

        // Fattori PRO
        const formFactorH = formH.formFactor;
        const formFactorA = formA.formFactor;
        const momentumH = standH.momentum;
        const momentumA = standA.momentum;

        // === TI TOTALI ===
        const shotsH_avg = sH.shots?.total?.average || 12.5;
        const shotsA_avg = sA.shots?.total?.average || 10.5;
        const xgFactorH = 0.7 + (xGH / bench) * 0.3;
        const xgFactorA = 0.7 + (xGA / bench) * 0.3;

        let cH = shotsH_avg * xgFactorH * homeAdv * formFactorH * momentumH * 0.95;
        let cA = shotsA_avg * xgFactorA * 1.0 * formFactorA * momentumA * 1.05;

        // H2H adjustment (se disponibile)
        if (h2hData) {
            cH = cH * (1 - h2hData.weight) + h2hData.avgShotsH * h2hData.weight;
            cA = cA * (1 - h2hData.weight) + h2hData.avgShotsA * h2hData.weight;
        }

        // Forma recente override (se media ultimi 5 > 20% diversa dalla stagionale)
        if (formH.avgShots > 0 && Math.abs(formH.avgShots - shotsH_avg) / shotsH_avg > 0.2) {
            cH = cH * 0.7 + formH.avgShots * 0.3;
        }
        if (formA.avgShots > 0 && Math.abs(formA.avgShots - shotsA_avg) / shotsA_avg > 0.2) {
            cA = cA * 0.7 + formA.avgShots * 0.3;
        }

        const totalShots = cH + cA;

        // === TI IN PORTA ===
        const onTargetH_avg = sH.shots?.on_goal?.average || 4.2;
        const onTargetA_avg = sA.shots?.on_goal?.average || 3.6;
        const convRateH = onTargetH_avg / shotsH_avg;
        const convRateA = onTargetA_avg / shotsA_avg;
        const precisionH = convRateH * (0.85 + xGH * 2.5);
        const precisionA = convRateA * (0.85 + xGA * 2.5);

        let oH = cH * precisionH * homeAdv * formFactorH;
        let oA = cA * precisionA * formFactorA;
        const totalOnTarget = oH + oA;

        // === CORNER ===
        const cornersForH = sH.corners?.for?.average || 5.2;
        const cornersAgainstH = sH.corners?.against?.average || 4.1;
        const cornersForA = sA.corners?.for?.average || 4.8;
        const cornersAgainstA = sA.corners?.against?.average || 4.4;
        const pressureH = (cornersForH + cornersAgainstA) / 2;
        const pressureA = (cornersForA + cornersAgainstH) / 2;
        const possH = sH.possession?.average || 52;
        const possA = sA.possession?.average || 48;
        const possFactorH = 0.9 + (possH / 100) * 0.2;
        const possFactorA = 0.9 + (possA / 100) * 0.2;

        let pCH = pressureH * possFactorH * homeAdv * formFactorH * 0.92;
        let pCA = pressureA * possFactorA * formFactorA * 1.08;

        // Forma recente corner
        if (formH.avgCorners > 0 && Math.abs(formH.avgCorners - cornersForH) / cornersForH > 0.15) {
            pCH = pCH * 0.8 + formH.avgCorners * 0.2;
        }
        if (formA.avgCorners > 0 && Math.abs(formA.avgCorners - cornersForA) / cornersForA > 0.15) {
            pCA = pCA * 0.8 + formA.avgCorners * 0.2;
        }

        const totalCorners = pCH + pCA;

        // === CARTELLINI ===
        const yellowH_avg = sH.cards?.yellow?.average || 2.1;
        const yellowA_avg = sA.cards?.yellow?.average || 2.3;
        const foulsH_avg = sH.fouls?.for?.average || 12.5;
        const foulsA_avg = sA.fouls?.for?.average || 13.0;
        const disciplineH = foulsH_avg / Math.max(yellowH_avg, 0.5);
        const disciplineA = foulsA_avg / Math.max(yellowA_avg, 0.5);
        const intensityFactor = 1.0 + ((foulsH_avg + foulsA_avg) - 24) / 100;

        let cardH = yellowH_avg * intensityFactor * homeAdv * formFactorH * 0.95;
        let cardA = yellowA_avg * intensityFactor * formFactorA * 1.05;

        // Forma recente cartellini
        if (formH.avgCards > 0) {
            cardH = cardH * 0.85 + formH.avgCards * 0.15;
        }
        if (formA.avgCards > 0) {
            cardA = cardA * 0.85 + formA.avgCards * 0.15;
        }

        const totalCards = cardH + cardA;

        // === FALLI SERIE A ===
        let totalFouls = 0, fH = 0, fA = 0;
        if(currentLeague === 7286) {
            const refVal = parseFloat(document.getElementById('arbitroSelect').value) || 24.5;
            const foulsAgainstH = sH.fouls?.against?.average || 11.5;
            const foulsAgainstA = sA.fouls?.against?.average || 12.0;
            fH = ((foulsH_avg + foulsAgainstA) / 2) * 0.6 + (refVal / 2 * 0.4);
            fA = ((foulsA_avg + foulsAgainstH) / 2) * 0.6 + (refVal / 2 * 0.4);
            totalFouls = fH + fA;
        }

        // === FASE 3: Rendering con dati PRO ===
        let html = "";

        // Info forma e classifica
        const formHtmlH = renderFormBar(formH.results);
        const formHtmlA = renderFormBar(formA.results);

        if(currentLeague === 7286) {
            const advFouls = getAdviceAdvanced(totalFouls, parseFloat(document.getElementById('sprFoulsMatch').value));
            const advFoulsH = getAdviceAdvanced(fH, parseFloat(document.getElementById('sprFoulsH').value));
            const advFoulsA = getAdviceAdvanced(fA, parseFloat(document.getElementById('sprFoulsA').value));
            html += `
            <div class="res-box border-l-red-500">
                <div class="precision-badge">${advFouls.precision}</div>
                <p class="label-spread text-red-400">Falli Commessi (Serie A)</p>
                <h2 class="text-5xl font-black teko">${totalFouls.toFixed(2)} ${advFouls.html}</h2>
                ${renderConfidenceBar(advFouls.confidence)}
                <div class="grid grid-cols-2 mt-4 pt-3 border-t border-slate-800">
                    <div><p class="label-spread">Casa</p><p class="text-xl teko text-red-400">${fH.toFixed(2)} ${advFoulsH.html}</p></div>
                    <div class="text-right"><p class="label-spread">Ospite</p><p class="text-xl teko text-red-400">${fA.toFixed(2)} ${advFoulsA.html}</p></div>
                </div>
            </div>`;
        }

        const advShots = getAdviceAdvanced(totalShots, parseFloat(document.getElementById('sprTotalMatch').value));
        const advShotsH = getAdviceAdvanced(cH, parseFloat(document.getElementById('sprTotalH').value));
        const advShotsA = getAdviceAdvanced(cA, parseFloat(document.getElementById('sprTotalA').value));
        html += `
        <div class="res-box border-l-emerald-500">
            <div class="precision-badge">${advShots.precision}</div>
            <p class="label-spread text-emerald-400">Tiri Totali Previsti</p>
            <h2 class="text-5xl font-black teko">${totalShots.toFixed(2)} ${advShots.html}</h2>
            ${renderConfidenceBar(advShots.confidence)}
            <div class="grid grid-cols-2 mt-4 pt-3 border-t border-slate-800">
                <div>
                    <p class="label-spread">Casa</p>
                    <p class="text-xl teko text-emerald-400">${cH.toFixed(2)} ${advShotsH.html}</p>
                    ${formHtmlH}
                    <p class="standings-info">Pos. ${standH.position}° / ${standH.totalTeams} • Forma: ${(formFactorH).toFixed(2)}x</p>
                </div>
                <div class="text-right">
                    <p class="label-spread">Ospite</p>
                    <p class="text-xl teko text-emerald-400">${cA.toFixed(2)} ${advShotsA.html}</p>
                    ${formHtmlA}
                    <p class="standings-info">Pos. ${standA.position}° / ${standA.totalTeams} • Forma: ${(formFactorA).toFixed(2)}x</p>
                </div>
            </div>
        </div>`;

        const advOT = getAdviceAdvanced(totalOnTarget, parseFloat(document.getElementById('sprOTMatch').value));
        const advOTH = getAdviceAdvanced(oH, parseFloat(document.getElementById('sprOTH').value));
        const advOTA = getAdviceAdvanced(oA, parseFloat(document.getElementById('sprOTA').value));
        html += `
        <div class="res-box border-l-purple-500">
            <div class="precision-badge">${advOT.precision}</div>
            <p class="label-spread text-purple-400">Tiri In Porta Previsti</p>
            <h2 class="text-5xl font-black teko">${totalOnTarget.toFixed(2)} ${advOT.html}</h2>
            ${renderConfidenceBar(advOT.confidence)}
            <div class="grid grid-cols-2 mt-4 pt-3 border-t border-slate-800">
                <div><p class="label-spread">Casa</p><p class="text-xl teko text-purple-400">${oH.toFixed(2)} ${advOTH.html}</p></div>
                <div class="text-right"><p class="label-spread">Ospite</p><p class="text-xl teko text-purple-400">${oA.toFixed(2)} ${advOTA.html}</p></div>
            </div>
        </div>`;

        const advCorn = getAdviceAdvanced(totalCorners, parseFloat(document.getElementById('sprCornMatch').value));
        const advCornH = getAdviceAdvanced(pCH, parseFloat(document.getElementById('sprCornH').value));
        const advCornA = getAdviceAdvanced(pCA, parseFloat(document.getElementById('sprCornA').value));
        html += `
        <div class="res-box border-l-cyan-500">
            <div class="precision-badge">${advCorn.precision}</div>
            <p class="label-spread text-cyan-400">Calci d'Angolo Previsti</p>
            <h2 class="text-5xl font-black teko">${totalCorners.toFixed(2)} ${advCorn.html}</h2>
            ${renderConfidenceBar(advCorn.confidence)}
            <div class="grid grid-cols-2 mt-4 pt-3 border-t border-slate-800">
                <div><p class="label-spread">Casa</p><p class="text-xl teko text-cyan-400">${pCH.toFixed(2)} ${advCornH.html}</p></div>
                <div class="text-right"><p class="label-spread">Ospite</p><p class="text-xl teko text-cyan-400">${pCA.toFixed(2)} ${advCornA.html}</p></div>
            </div>
        </div>`;

        const advCards = getAdviceAdvanced(totalCards, parseFloat(document.getElementById('sprCardsMatch').value));
        const advCardsH = getAdviceAdvanced(cardH, parseFloat(document.getElementById('sprCardsH').value));
        const advCardsA = getAdviceAdvanced(cardA, parseFloat(document.getElementById('sprCardsA').value));
        html += `
        <div class="res-box border-l-yellow-500">
            <div class="precision-badge">${advCards.precision}</div>
            <p class="label-spread text-yellow-400">Gialli Previsti</p>
            <h2 class="text-5xl font-black teko">${totalCards.toFixed(2)} ${advCards.html}</h2>
            ${renderConfidenceBar(advCards.confidence)}
            <div class="grid grid-cols-2 mt-4 pt-3 border-t border-slate-800">
                <div><p class="label-spread">Casa</p><p class="text-xl teko text-yellow-400">${cardH.toFixed(2)} ${advCardsH.html}</p></div>
                <div class="text-right"><p class="label-spread">Ospite</p><p class="text-xl teko text-yellow-400">${cardA.toFixed(2)} ${advCardsA.html}</p></div>
            </div>
        </div>`;

        resDiv.innerHTML = html;
        resDiv.scrollIntoView({behavior:'smooth'});
    } catch(e) { 
        resDiv.innerHTML = `<div class='p-4 bg-red-900 rounded-xl border border-red-500'><p class="font-bold text-red-400">ERRORE ANALISI</p><p class="text-white">${e.message}</p></div>`; 
    }
}

loadData();
</script>
</body>
</html>
"""
components.html(html_code, height=1800, scrolling=True)
