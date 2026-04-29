import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI V4 - TOTAL ANALYST", layout="wide")

API_KEY = "75e4107623c05bb4bca2ac8b78b28dca"
BASE_CSV_URL = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/"
REFS_FILE = "ARBITRI_SERIE_A%20-%20Foglio1.csv"

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
        select, input { background: #0f172a; border: 1px solid #475569; color: white; padding: 12px; width: 100%; border-radius: 12px; font-weight: bold; font-size: 14px; outline: none; }
        .btn-analizza { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); width: 100%; padding: 20px; border-radius: 15px; font-weight: 900; text-transform: uppercase; cursor: pointer; transition: 0.3s; margin-top: 20px; border: none; color: white; }
        .btn-analizza:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(59, 130, 246, 0.4); }
        .res-box { background: #0f172a; border-radius: 20px; padding: 20px; border-left: 5px solid #3b82f6; margin-bottom: 15px; }
        .advice-tag { display: inline-block; padding: 2px 10px; border-radius: 6px; font-size: 12px; font-weight: 900; margin-left: 10px; }
        .over-tag { background: #10b981; color: #020617; }
        .under-tag { background: #ef4444; color: white; }
        .label-spread { font-size: 10px; font-weight: 900; color: #94a3b8; text-transform: uppercase; margin-bottom: 5px; display: block; }
        .league-btn { cursor: pointer; padding: 12px; border-radius: 10px; font-weight: 900; border: 1px solid #334155; text-align: center; font-size: 11px; transition: all 0.3s; }
        .league-active { background: #3b82f6; border-color: #3b82f6; color: white; box-shadow: 0 0 15px rgba(59, 130, 246, 0.5); }
        .grid-spreads { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; padding-top: 15px; border-top: 1px solid #334155; margin-bottom: 15px; }
        .loading-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(2,6,23,0.9); display: flex; align-items: center; justify-content: center; z-index: 9999; }
        .spinner { width: 50px; height: 50px; border: 4px solid #1e293b; border-top: 4px solid #3b82f6; border-radius: 50%; animation: spin 1s linear infinite; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .error-box { background: #7f1d1d; border: 1px solid #ef4444; border-radius: 12px; padding: 16px; color: #fca5a5; }
        .stat-detail { font-size: 11px; color: #64748b; margin-top: 4px; }
    </style>
</head>
<body class="p-4 md:p-8">
    <div id="loadingOverlay" class="loading-overlay hidden">
        <div class="text-center">
            <div class="spinner mx-auto mb-4"></div>
            <p class="text-blue-400 font-bold teko text-xl tracking-widest">CARICAMENTO DATI...</p>
        </div>
    </div>

    <div class="max-w-5xl mx-auto">
        <div class="text-center mb-10">
            <h1 class="text-6xl font-black teko tracking-widest text-white uppercase italic">PROBET <span class="text-blue-500">AI V4</span></h1>
            <p class="text-blue-400 font-bold text-xs tracking-widest uppercase italic">Elite Multi-League Analysis System</p>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div id="btn-135" class="league-btn league-active" onclick="switchLeague(135)">SERIE A</div>
            <div id="btn-39" class="league-btn" onclick="switchLeague(39)">PREMIER LEAGUE</div>
            <div id="btn-78" class="league-btn" onclick="switchLeague(78)">BUNDESLIGA</div>
            <div id="btn-140" class="league-btn" onclick="switchLeague(140)">LA LIGA</div>
        </div>

        <div class="card-premium mb-8">
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

            <button onclick="triggerAdAndCalculate()" class="btn-analizza shadow-xl italic teko text-2xl tracking-widest">GENERA ANALISI ELITE</button>
        </div>
        <div id="results" class="space-y-6 hidden pb-20"></div>
    </div>

<script>
const API_KEY = "75e4107623c05bb4bca2ac8b78b28dca";
const BASE_CSV_URL = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/";
const REFS_FILE = "ARBITRI_SERIE_A%20-%20Foglio1.csv";
let currentLeague = 135, dbXG = [];
const SEASON = 2024; // Stagione 2024/25 in corso

// ===================== UTILITY =====================
function showLoading(show) {
    document.getElementById('loadingOverlay').classList.toggle('hidden', !show);
}

function setError(msg) {
    const resDiv = document.getElementById('results');
    resDiv.innerHTML = `<div class="error-box"><strong>ERRORE:</strong> ${msg}</div>`;
    resDiv.classList.remove('hidden');
    resDiv.scrollIntoView({behavior:'smooth'});
}

async function fetchWithRetry(url, options, retries = 2) {
    for (let i = 0; i <= retries; i++) {
        try {
            const res = await fetch(url, options);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const data = await res.json();
            if (data.errors && Object.keys(data.errors).length > 0) {
                throw new Error(JSON.stringify(data.errors));
            }
            return data;
        } catch (e) {
            if (i === retries) throw e;
            await new Promise(r => setTimeout(r, 1000 * (i + 1)));
        }
    }
}

// ===================== PUBBLICITÀ =====================
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

// ===================== CAMBIO CAMPIONATO =====================
function switchLeague(id) {
    currentLeague = id;
    document.querySelectorAll('.league-btn').forEach(b => b.classList.remove('league-active'));
    document.getElementById(`btn-${id}`).classList.add('league-active');
    const isSerieA = (id === 135);
    document.getElementById('arbitroContainer').style.display = isSerieA ? "block" : "none";
    document.getElementById('foulsInputs').style.display = isSerieA ? "grid" : "none";
    loadData();
}

// ===================== CARICAMENTO DATI =====================
function loadData() {
    showLoading(true);
    const files = { 
        135: "DATABASE_AVANZATO_SERIEA_2025.csv", 
        39: "DATABASE_AVANZATO_PREMIER_2025.csv", 
        78: "DATABASE_AVANZATO_BUNDES_2025.csv", 
        140: "DATABASE_AVANZATO_LALIGA_2025.csv" 
    };
    
    Papa.parse(BASE_CSV_URL + files[currentLeague], { 
        download: true, 
        header: true, 
        skipEmptyLines: true, 
        complete: (r) => { 
            dbXG = r.data; 
            loadTeams();
        },
        error: (err) => {
            console.error("Errore CSV:", err);
            dbXG = [];
            loadTeams();
        }
    });
    
    if(currentLeague === 135) {
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
                    if(name && val) {
                        sel.add(new Option(name, val.toString().replace(',', '.')));
                    }
                });
            },
            error: () => {
                document.getElementById('arbitroSelect').innerHTML = '<option value="24.5">Dati non disponibili</option>';
            }
        });
    }
}

// ===================== CARICAMENTO SQUADRE (come il primo codice) =====================
async function loadTeams() {
    try {
        // Usa teams?league=ID&season=2024 come il primo codice - filtra per campionato!
        const url = `https://v3.football.api-sports.io/teams?league=${currentLeague}&season=${SEASON}`;
        const data = await fetchWithRetry(url, { headers: { "x-apisports-key": API_KEY } });
        
        const h = document.getElementById('homeTeam'), a = document.getElementById('awayTeam');
        h.innerHTML = ""; a.innerHTML = "";
        
        if (!data.response || data.response.length === 0) {
            h.add(new Option("Nessuna squadra trovata", ""));
            a.add(new Option("Nessuna squadra trovata", ""));
            showLoading(false);
            return;
        }
        
        data.response.sort((x,y) => x.team.name.localeCompare(y.team.name)).forEach(t => {
            h.add(new Option(t.team.name, t.team.id)); 
            a.add(new Option(t.team.name, t.team.id));
        });
        
        showLoading(false);
        
    } catch (e) {
        console.error("Errore caricamento squadre:", e);
        setError("Impossibile caricare le squadre: " + e.message);
        showLoading(false);
    }
}

// ===================== STATISTICHE REALI DA FIXTURES =====================
async function getTeamStatsFromFixtures(teamId) {
    try {
        // Ottieni SOLO le partite di QUESTO campionato e QUESTO team
        const fixturesUrl = `https://v3.football.api-sports.io/fixtures?league=${currentLeague}&season=${SEASON}&team=${teamId}`;
        const fixturesData = await fetchWithRetry(fixturesUrl, { headers: { "x-apisports-key": API_KEY } });
        
        if (!fixturesData.response || fixturesData.response.length === 0) {
            return null;
        }
        
        // Filtra solo partite terminate
        const fixtures = fixturesData.response
            .filter(f => f.fixture.status.short === 'FT')
            .slice(0, 10);
        
        if (fixtures.length === 0) return null;
        
        // Per ogni partita, ottieni le statistiche
        const statsPromises = fixtures.map(async (fixture) => {
            const fixtureId = fixture.fixture.id;
            const statsUrl = `https://v3.football.api-sports.io/fixtures/statistics?fixture=${fixtureId}&team=${teamId}`;
            try {
                const statsData = await fetchWithRetry(statsUrl, { headers: { "x-apisports-key": API_KEY } });
                return statsData.response?.[0]?.statistics || [];
            } catch (e) {
                return [];
            }
        });
        
        const allStats = await Promise.all(statsPromises);
        
        // Aggrega le statistiche
        const aggregated = {
            shotsTotal: 0, shotsOn: 0, shotsOff: 0, shotsBlocked: 0,
            shotsInside: 0, shotsOutside: 0,
            fouls: 0, corners: 0, yellowCards: 0, redCards: 0,
            count: 0
        };
        
        allStats.forEach(matchStats => {
            if (!matchStats || matchStats.length === 0) return;
            aggregated.count++;
            matchStats.forEach(stat => {
                const val = parseFloat(stat.value) || 0;
                switch(stat.type) {
                    case 'Shots on Goal': aggregated.shotsOn += val; break;
                    case 'Shots off Goal': aggregated.shotsOff += val; break;
                    case 'Total Shots': aggregated.shotsTotal += val; break;
                    case 'Blocked Shots': aggregated.shotsBlocked += val; break;
                    case 'Shots insidebox': aggregated.shotsInside += val; break;
                    case 'Shots outsidebox': aggregated.shotsOutside += val; break;
                    case 'Fouls': aggregated.fouls += val; break;
                    case 'Corner Kicks': aggregated.corners += val; break;
                    case 'Yellow Cards': aggregated.yellowCards += val; break;
                    case 'Red Cards': aggregated.redCards += val; break;
                }
            });
        });
        
        if (aggregated.count === 0) return null;
        
        return {
            shotsTotal: aggregated.shotsTotal / aggregated.count,
            shotsOn: aggregated.shotsOn / aggregated.count,
            shotsOff: aggregated.shotsOff / aggregated.count,
            shotsBlocked: aggregated.shotsBlocked / aggregated.count,
            shotsInside: aggregated.shotsInside / aggregated.count,
            shotsOutside: aggregated.shotsOutside / aggregated.count,
            fouls: aggregated.fouls / aggregated.count,
            corners: aggregated.corners / aggregated.count,
            yellowCards: aggregated.yellowCards / aggregated.count,
            redCards: aggregated.redCards / aggregated.count,
            matches: aggregated.count
        };
    } catch (e) {
        console.error("Errore stats fixtures:", e);
        return null;
    }
}

// ===================== CALCOLO CONSIGLIO =====================
function getAdvice(pred, elementId) {
    const el = document.getElementById(elementId);
    if(!el || el.offsetParent === null) return "";
    const s = parseFloat(el.value);
    if (isNaN(s)) return "";
    const diff = pred - s;
    let p = Math.min(50 + Math.abs(diff) * 8, 98);
    const isOver = pred >= s;
    return `<span class="advice-tag ${isOver ? 'over-tag' : 'under-tag'}">${isOver ? 'OVER' : 'UNDER'} ${s} (${p.toFixed(1)}%)</span>`;
}

// ===================== ANALISI CARTELLINI =====================
async function getCardStats(leagueId) {
    try {
        const [yellowData, redData] = await Promise.all([
            fetchWithRetry(
                `https://v3.football.api-sports.io/players/topyellowcards?league=${leagueId}&season=${SEASON}`,
                { headers: { "x-apisports-key": API_KEY } }
            ),
            fetchWithRetry(
                `https://v3.football.api-sports.io/players/topredcards?league=${leagueId}&season=${SEASON}`,
                { headers: { "x-apisports-key": API_KEY } }
            )
        ]);
        
        const yellowByTeam = {};
        const redByTeam = {};
        
        if (yellowData.response) {
            yellowData.response.forEach(p => {
                const teamId = p.statistics?.[0]?.team?.id;
                if (teamId) {
                    yellowByTeam[teamId] = (yellowByTeam[teamId] || 0) + (p.statistics[0]?.cards?.yellow || 0);
                }
            });
        }
        
        if (redData.response) {
            redData.response.forEach(p => {
                const teamId = p.statistics?.[0]?.team?.id;
                if (teamId) {
                    redByTeam[teamId] = (redByTeam[teamId] || 0) + (p.statistics[0]?.cards?.red || 0);
                }
            });
        }
        
        return { yellowByTeam, redByTeam };
    } catch (e) {
        console.error("Errore cartellini:", e);
        return { yellowByTeam: {}, redByTeam: {} };
    }
}

// ===================== ANALISI PRINCIPALE =====================
async function runDeepAnalysis() {
    const resDiv = document.getElementById('results');
    resDiv.innerHTML = `<div class='text-center py-20 animate-pulse text-blue-500 font-black teko text-3xl uppercase tracking-widest'>ANALISI IN CORSO...</div>`;
    resDiv.classList.remove('hidden');

    try {
        const idH = document.getElementById('homeTeam').value;
        const idA = document.getElementById('awayTeam').value;
        
        if (!idH || !idA) {
            setError("Seleziona entrambe le squadre");
            return;
        }
        if (idH === idA) {
            setError("Le squadre devono essere diverse");
            return;
        }

        // Fetch parallelo
        const [statsH, statsA, cardStats] = await Promise.all([
            getTeamStatsFromFixtures(idH),
            getTeamStatsFromFixtures(idA),
            getCardStats(currentLeague)
        ]);

        if (!statsH || !statsA) {
            setError("Statistiche non disponibili per una o entrambe le squadre");
            return;
        }

        // xG dal database CSV
        const xGH = parseFloat((dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || "0.11").toString().replace(',', '.'));
        const xGA = parseFloat((dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || "0.11").toString().replace(',', '.'));
        const bench = (currentLeague === 39 || currentLeague === 78) ? 0.12 : 0.11;

        // ========== TIRI ==========
        const shotsTotalH = statsH.shotsTotal || 12;
        const shotsTotalA = statsA.shotsTotal || 10;
        const shotsOnH = statsH.shotsOn || 4;
        const shotsOnA = statsA.shotsOn || 3.5;
        
        const cH = shotsTotalH * (xGH / bench);
        const cA = shotsTotalA * (xGA / bench);
        const oH = shotsOnH * (xGH / bench);
        const oA = shotsOnA * (xGA / bench);

        // ========== CORNER ==========
        const cornForH = statsH.corners || 5;
        const cornForA = statsA.corners || 4.5;
        const cornAgainstH = statsA.corners || 4;
        const cornAgainstA = statsH.corners || 4.5;
        
        const pCH = (cornForH + cornAgainstA) / 2;
        const pCA = (cornForA + cornAgainstH) / 2;

        // ========== CARTELLINI ==========
        let cardH = statsH.yellowCards || 2.1;
        let cardA = statsA.yellowCards || 2.3;
        
        if (cardStats.yellowByTeam[idH]) {
            cardH = Math.max(cardH, cardStats.yellowByTeam[idH] / (statsH.matches || 10));
        }
        if (cardStats.yellowByTeam[idA]) {
            cardA = Math.max(cardA, cardStats.yellowByTeam[idA] / (statsA.matches || 10));
        }

        let html = "";

        // ========== FALLI (SOLO SERIE A) ==========
        if(currentLeague === 135) {
            const refVal = parseFloat(document.getElementById('arbitroSelect').value) || 24.5;
            const foulsForH = statsH.fouls || 12.5;
            const foulsForA = statsA.fouls || 13;
            
            const fH = foulsForH * 0.6 + (refVal/2 * 0.4);
            const fA = foulsForA * 0.6 + (refVal/2 * 0.4);
            
            html += `
            <div class="res-box border-l-red-500">
                <p class="label-spread">Falli Commessi (Serie A)</p>
                <h2 class="text-5xl font-black teko">${(fH+fA).toFixed(2)} ${getAdvice(fH+fA, 'sprFoulsMatch')}</h2>
                <div class="grid grid-cols-2 mt-2 pt-2 border-t border-slate-800">
                    <div>
                        <p class="label-spread">Casa</p>
                        <p class="text-xl teko text-red-400">${fH.toFixed(2)} ${getAdvice(fH, 'sprFoulsH')}</p>
                        <p class="stat-detail">Media: ${foulsForH.toFixed(1)} | Partite: ${statsH.matches}</p>
                    </div>
                    <div class="text-right">
                        <p class="label-spread">Ospite</p>
                        <p class="text-xl teko text-red-400">${fA.toFixed(2)} ${getAdvice(fA, 'sprFoulsA')}</p>
                        <p class="stat-detail">Media: ${foulsForA.toFixed(1)} | Partite: ${statsA.matches}</p>
                    </div>
                </div>
            </div>`;
        }

        // ========== TIRI TOTALI ==========
        html += `
        <div class="res-box border-l-emerald-500">
            <p class="label-spread">Tiri Totali</p>
            <h2 class="text-5xl font-black teko">${(cH+cA).toFixed(2)} ${getAdvice(cH+cA, 'sprTotalMatch')}</h2>
            <div class="grid grid-cols-2 mt-2 pt-2 border-t border-slate-800">
                <div>
                    <p class="label-spread">Casa</p>
                    <p class="text-xl teko text-emerald-400">${cH.toFixed(2)} ${getAdvice(cH, 'sprTotalH')}</p>
                    <p class="stat-detail">Media: ${shotsTotalH.toFixed(1)} | xG: ${xGH.toFixed(3)} | Partite: ${statsH.matches}</p>
                </div>
                <div class="text-right">
                    <p class="label-spread">Ospite</p>
                    <p class="text-xl teko text-emerald-400">${cA.toFixed(2)} ${getAdvice(cA, 'sprTotalA')}</p>
                    <p class="stat-detail">Media: ${shotsTotalA.toFixed(1)} | xG: ${xGA.toFixed(3)} | Partite: ${statsA.matches}</p>
                </div>
            </div>
        </div>`;

        // ========== TIRI IN PORTA ==========
        html += `
        <div class="res-box border-l-purple-500">
            <p class="label-spread">Tiri In Porta</p>
            <h2 class="text-5xl font-black teko">${(oH+oA).toFixed(2)} ${getAdvice(oH+oA, 'sprOTMatch')}</h2>
            <div class="grid grid-cols-2 mt-2 pt-2 border-t border-slate-800">
                <div>
                    <p class="label-spread">Casa</p>
                    <p class="text-xl teko text-purple-400">${oH.toFixed(2)} ${getAdvice(oH, 'sprOTH')}</p>
                    <p class="stat-detail">Media: ${shotsOnH.toFixed(1)} | Dentro area: ${statsH.shotsInside.toFixed(1)}</p>
                </div>
                <div class="text-right">
                    <p class="label-spread">Ospite</p>
                    <p class="text-xl teko text-purple-400">${oA.toFixed(2)} ${getAdvice(oA, 'sprOTA')}</p>
                    <p class="stat-detail">Media: ${shotsOnA.toFixed(1)} | Dentro area: ${statsA.shotsInside.toFixed(1)}</p>
                </div>
            </div>
        </div>`;

        // ========== CORNER ==========
        html += `
        <div class="res-box border-l-cyan-500">
            <p class="label-spread">Calci d'Angolo</p>
            <h2 class="text-5xl font-black teko">${(pCH+pCA).toFixed(2)} ${getAdvice(pCH+pCA, 'sprCornMatch')}</h2>
            <div class="grid grid-cols-2 mt-2 pt-2 border-t border-slate-800">
                <div>
                    <p class="label-spread">Casa</p>
                    <p class="text-xl teko text-cyan-400">${pCH.toFixed(2)} ${getAdvice(pCH, 'sprCornH')}</p>
                    <p class="stat-detail">Fatti: ${cornForH.toFixed(1)} | Subiti avv: ${cornAgainstA.toFixed(1)}</p>
                </div>
                <div class="text-right">
                    <p class="label-spread">Ospite</p>
                    <p class="text-xl teko text-cyan-400">${pCA.toFixed(2)} ${getAdvice(pCA, 'sprCornA')}</p>
                    <p class="stat-detail">Fatti: ${cornForA.toFixed(1)} | Subiti avv: ${cornAgainstH.toFixed(1)}</p>
                </div>
            </div>
        </div>`;

        // ========== CARTELLINI ==========
        html += `
        <div class="res-box border-l-yellow-500">
            <p class="label-spread">Gialli Previsti</p>
            <h2 class="text-5xl font-black teko">${(cardH+cardA).toFixed(2)} ${getAdvice(cardH+cardA, 'sprCardsMatch')}</h2>
            <div class="grid grid-cols-2 mt-2 pt-2 border-t border-slate-800">
                <div>
                    <p class="label-spread">Casa</p>
                    <p class="text-xl teko text-yellow-400">${cardH.toFixed(2)} ${getAdvice(cardH, 'sprCardsH')}</p>
                    <p class="stat-detail">Media: ${(statsH.yellowCards || 0).toFixed(1)} | Rossi: ${(statsH.redCards || 0).toFixed(1)}</p>
                </div>
                <div class="text-right">
                    <p class="label-spread">Ospite</p>
                    <p class="text-xl teko text-yellow-400">${cardA.toFixed(2)} ${getAdvice(cardA, 'sprCardsA')}</p>
                    <p class="stat-detail">Media: ${(statsA.yellowCards || 0).toFixed(1)} | Rossi: ${(statsA.redCards || 0).toFixed(1)}</p>
                </div>
            </div>
        </div>`;

        // Info
        const homeName = document.getElementById('homeTeam').options[document.getElementById('homeTeam').selectedIndex].text;
        const awayName = document.getElementById('awayTeam').options[document.getElementById('awayTeam').selectedIndex].text;
        
        html += `
        <div class="res-box" style="border-left-color: #3b82f6;">
            <p class="label-spread text-blue-400">Info Partita</p>
            <p class="text-sm text-slate-400">${homeName} vs ${awayName} | Stagione ${SEASON}/${SEASON+1} | League ID: ${currentLeague}</p>
            <p class="text-xs text-slate-500 mt-1">Dati reali dalle ultime ${statsH.matches} partite giocate</p>
        </div>`;

        resDiv.innerHTML = html;
        resDiv.scrollIntoView({behavior:'smooth'});
        
    } catch(e) { 
        console.error(e);
        setError("Errore nel caricamento dei dati: " + e.message); 
    }
}

// Avvia
loadData();
</script>
</body>
</html>
"""

components.html(html_code, height=1800, scrolling=True)
