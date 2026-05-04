import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI V4 - TOTAL ANALYST", layout="wide")

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
        .res-box { background: #0f172a; border-radius: 20px; padding: 20px; border-left: 5px solid #3b82f6; margin-bottom: 15px; }
        .advice-tag { display: inline-block; padding: 2px 10px; border-radius: 6px; font-size: 12px; font-weight: 900; margin-left: 10px; }
        .over-tag { background: #10b981; color: #020617; }
        .under-tag { background: #ef4444; color: white; }
        .label-spread { font-size: 10px; font-weight: 900; color: #94a3b8; text-transform: uppercase; margin-bottom: 5px; display: block; }
        .league-btn { cursor: pointer; padding: 12px; border-radius: 10px; font-weight: 900; border: 1px solid #334155; text-align: center; font-size: 11px; }
        .league-active { background: #3b82f6; border-color: #3b82f6; color: white; box-shadow: 0 0 15px rgba(59, 130, 246, 0.5); }
        .grid-spreads { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; padding-top: 15px; border-top: 1px solid #334155; margin-bottom: 15px; }
        .status-msg { font-size: 12px; font-weight: 700; padding: 8px 12px; border-radius: 8px; margin-bottom: 10px; }
        .status-ok { background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid #10b981; }
        .status-err { background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid #ef4444; }
        .status-warn { background: rgba(245, 158, 11, 0.2); color: #f59e0b; border: 1px solid #f59e0b; }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-5xl mx-auto">
        <div class="text-center mb-10">
            <h1 class="text-6xl font-black teko tracking-widest text-white uppercase italic">PROBET <span class="text-blue-500">AI V4</span></h1>
            <p class="text-blue-400 font-bold text-xs tracking-widest uppercase italic">Elite Multi-League Analysis System - Stagione 2025/2026</p>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div id="btn-7286" class="league-btn league-active" onclick="switchLeague(7286)">SERIE A</div>
            <div id="btn-7293" class="league-btn" onclick="switchLeague(7293)">PREMIER LEAGUE</div>
            <div id="btn-7338" class="league-btn" onclick="switchLeague(7338)">BUNDESLIGA</div>
            <div id="btn-7351" class="league-btn" onclick="switchLeague(7351)">LA LIGA</div>
        </div>

        <div class="card-premium mb-8">
            <div id="statusMessage" class="status-msg status-warn">Inizializzazione...</div>

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
const API_KEY = "8546a3b44515070cb8e4b6a8f620ab5b";
const BASE_CSV_URL = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/";
const REFS_FILE = "ARBITRI_SERIE_A%20-%20Foglio1.csv";
let currentLeague = 7286, dbXG = [];

// Mappatura campionati con ID nuovi (v3 stagione 2025) e ID standard fallback
const LEAGUE_DATA = {
    7286: { name: "SERIE A", file: "DATABASE_AVANZATO_SERIEA_2025.csv", oldId: 135, apiId: 7286 },
    7293: { name: "PREMIER LEAGUE", file: "DATABASE_AVANZATO_PREMIER_2025.csv", oldId: 39, apiId: 7293 },
    7338: { name: "BUNDESLIGA", file: "DATABASE_AVANZATO_BUNDES_2025.csv", oldId: 78, apiId: 7338 },
    7351: { name: "LA LIGA", file: "DATABASE_AVANZATO_LALIGA_2025.csv", oldId: 140, apiId: 7351 }
};

function setStatus(msg, type) {
    const el = document.getElementById('statusMessage');
    el.textContent = msg;
    el.className = 'status-msg status-' + type;
}

// FUNZIONE PUBBLICITÀ
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
    setStatus(`Caricamento dati ${leagueInfo.name}...`, 'warn');

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
    h.innerHTML = '<option>Caricamento squadre...</option>';
    a.innerHTML = '<option>Caricamento squadre...</option>';

    try {
        const leagueInfo = LEAGUE_DATA[currentLeague];
        let apiId = leagueInfo.apiId;

        // TENTATIVO 1: ID nuovo (v3 stagione 2025)
        setStatus(`Chiamata API con ID ${apiId}...`, 'warn');
        let res = await fetch(`https://v3.football.api-sports.io/teams?league=${apiId}&season=2025`, { 
            headers: { "x-apisports-key": API_KEY } 
        });

        if (!res.ok) {
            throw new Error(`HTTP ${res.status}`);
        }

        let data = await res.json();

        // TENTATIVO 2: Fallback a ID standard se nuovo ID restituisce vuoto
        if (!data.response || data.response.length === 0) {
            apiId = leagueInfo.oldId;
            setStatus(`ID ${leagueInfo.apiId} vuoto, provo ID standard ${apiId}...`, 'warn');
            res = await fetch(`https://v3.football.api-sports.io/teams?league=${apiId}&season=2025`, { 
                headers: { "x-apisports-key": API_KEY } 
            });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            data = await res.json();
        }

        if (!data.response || data.response.length === 0) {
            throw new Error("Nessuna squadra trovata per questo campionato");
        }

        // Popola select
        h.innerHTML = ""; a.innerHTML = "";
        h.add(new Option("-- Seleziona Casa --", ""));
        a.add(new Option("-- Seleziona Ospite --", ""));

        data.response.sort((x,y) => x.team.name.localeCompare(y.team.name)).forEach(t => {
            h.add(new Option(t.team.name, t.team.id)); 
            a.add(new Option(t.team.name, t.team.id));
        });

        setStatus(`✓ ${data.response.length} squadre caricate (${leagueInfo.name})`, 'ok');

    } catch (e) {
        console.error("Errore loadTeams:", e);
        h.innerHTML = '<option>Errore caricamento squadre</option>';
        a.innerHTML = '<option>Errore caricamento squadre</option>';
        setStatus(`✗ Errore API: ${e.message}`, 'err');
    }
}

function getAdvice(pred, elementId) {
    const el = document.getElementById(elementId);
    if(!el || el.offsetParent === null) return "";
    const s = parseFloat(el.value);
    const p = Math.min(Math.max(50 + (pred - s) * 9.2, 5), 98);
    return `<span class="advice-tag ${p >= 50 ? 'over-tag' : 'under-tag'}">${p >= 50 ? 'OVER' : 'UNDER'} ${s} (${(p >= 50 ? p : 100-p).toFixed(1)}%)</span>`;
}

async function runDeepAnalysis() {
    const resDiv = document.getElementById('results');
    resDiv.innerHTML = "<div class='text-center py-20 animate-pulse text-blue-500 font-black teko text-3xl uppercase tracking-widest'>ANALISI IN CORSO...</div>";
    resDiv.classList.remove('hidden');

    try {
        const idH = document.getElementById('homeTeam').value;
        const idA = document.getElementById('awayTeam').value;

        if (!idH || !idA) {
            throw new Error("Seleziona entrambe le squadre");
        }
        if (idH === idA) {
            throw new Error("Le squadre devono essere diverse");
        }

        const leagueInfo = LEAGUE_DATA[currentLeague];
        let apiId = leagueInfo.apiId;

        // Verifica quale ID funziona per le statistiche
        let statsH, statsA;
        try {
            [statsH, statsA] = await Promise.all([
                fetch(`https://v3.football.api-sports.io/teams/statistics?league=${apiId}&season=2025&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
                fetch(`https://v3.football.api-sports.io/teams/statistics?league=${apiId}&season=2025&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
            ]);
            if (!statsH.response || !statsA.response) throw new Error("empty");
        } catch (e) {
            // Fallback a ID standard
            apiId = leagueInfo.oldId;
            [statsH, statsA] = await Promise.all([
                fetch(`https://v3.football.api-sports.io/teams/statistics?league=${apiId}&season=2025&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
                fetch(`https://v3.football.api-sports.io/teams/statistics?league=${apiId}&season=2025&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
            ]);
        }

        const sH = statsH.response; 
        const sA = statsA.response;

        const xGH = parseFloat((dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || "0.11").toString().replace(',', '.'));
        const xGA = parseFloat((dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || "0.11").toString().replace(',', '.'));
        const bench = (currentLeague === 7293 || currentLeague === 7338) ? 0.12 : 0.11;

        const cH = (sH.shots?.total?.average || 12) * (xGH / bench);
        const cA = (sA.shots?.total?.average || 10) * (xGA / bench);
        const oH = (sH.shots?.on_goal?.average || 4) * (xGH / bench);
        const oA = (sA.shots?.on_goal?.average || 3.5) * (xGA / bench);
        const pCH = ((sH.corners?.for?.average || 5) + (sA.corners?.against?.average || 4.5)) / 2;
        const pCA = ((sA.corners?.for?.average || 4.5) + (sH.corners?.against?.average || 4)) / 2;
        const cardH = (sH.cards?.yellow?.average || 2.1);
        const cardA = (sA.cards?.yellow?.average || 2.3);

        let html = "";

        if(currentLeague === 7286) {
            const refVal = parseFloat(document.getElementById('arbitroSelect').value) || 24.5;
            const fH = ((sH.fouls?.for?.average || 12.5) + (sA.fouls?.against?.average || 11.5)) / 2 * 0.6 + (refVal/2 * 0.4);
            const fA = ((sA.fouls?.for?.average || 13) + (sH.fouls?.against?.average || 12)) / 2 * 0.6 + (refVal/2 * 0.4);
            html += `<div class="res-box border-l-red-500"><p class="label-spread">Falli Commessi (Serie A)</p><h2 class="text-5xl font-black teko">${(fH+fA).toFixed(2)} ${getAdvice(fH+fA, 'sprFoulsMatch')}</h2><div class="grid grid-cols-2 mt-2 pt-2 border-t border-slate-800"><div><p class="label-spread">Casa</p><p class="text-xl teko text-red-400">${fH.toFixed(2)} ${getAdvice(fH, 'sprFoulsH')}</p></div><div class="text-right"><p class="label-spread">Ospite</p><p class="text-xl teko text-red-400">${fA.toFixed(2)} ${getAdvice(fA, 'sprFoulsA')}</p></div></div></div>`;
        }

        html += `<div class="res-box border-l-emerald-500"><p class="label-spread">Tiri Totali</p><h2 class="text-5xl font-black teko">${(cH+cA).toFixed(2)} ${getAdvice(cH+cA, 'sprTotalMatch')}</h2><div class="grid grid-cols-2 mt-2 pt-2 border-t border-slate-800"><div><p class="label-spread">Casa</p><p class="text-xl teko text-emerald-400">${cH.toFixed(2)} ${getAdvice(cH, 'sprTotalH')}</p></div><div class="text-right"><p class="label-spread">Ospite</p><p class="text-xl teko text-emerald-400">${cA.toFixed(2)} ${getAdvice(cA, 'sprTotalA')}</p></div></div></div>`;
        html += `<div class="res-box border-l-purple-500"><p class="label-spread">Tiri In Porta</p><h2 class="text-5xl font-black teko">${(oH+oA).toFixed(2)} ${getAdvice(oH+oA, 'sprOTMatch')}</h2><div class="grid grid-cols-2 mt-2 pt-2 border-t border-slate-800"><div><p class="label-spread">Casa</p><p class="text-xl teko text-purple-400">${oH.toFixed(2)} ${getAdvice(oH, 'sprOTH')}</p></div><div class="text-right"><p class="label-spread">Ospite</p><p class="text-xl teko text-purple-400">${oA.toFixed(2)} ${getAdvice(oA, 'sprOTA')}</p></div></div></div>`;
        html += `<div class="res-box border-l-cyan-500"><p class="label-spread">Calci d'Angolo</p><h2 class="text-5xl font-black teko">${(pCH+pCA).toFixed(2)} ${getAdvice(pCH+pCA, 'sprCornMatch')}</h2><div class="grid grid-cols-2 mt-2 pt-2 border-t border-slate-800"><div><p class="label-spread">Casa</p><p class="text-xl teko text-cyan-400">${pCH.toFixed(2)} ${getAdvice(pCH, 'sprCornH')}</p></div><div class="text-right"><p class="label-spread">Ospite</p><p class="text-xl teko text-cyan-400">${pCA.toFixed(2)} ${getAdvice(pCA, 'sprCornA')}</p></div></div></div>`;
        html += `<div class="res-box border-l-yellow-500"><p class="label-spread">Gialli Previsti</p><h2 class="text-5xl font-black teko">${(cardH+cardA).toFixed(2)} ${getAdvice(cardH+cardA, 'sprCardsMatch')}</h2><div class="grid grid-cols-2 mt-2 pt-2 border-t border-slate-800"><div><p class="label-spread">Casa</p><p class="text-xl teko text-yellow-400">${cardH.toFixed(2)} ${getAdvice(cardH, 'sprCardsH')}</p></div><div class="text-right"><p class="label-spread">Ospite</p><p class="text-xl teko text-yellow-400">${cardA.toFixed(2)} ${getAdvice(cardA, 'sprCardsA')}</p></div></div></div>`;

        resDiv.innerHTML = html;
        resDiv.scrollIntoView({behavior:'smooth'});
    } catch(e) { 
        resDiv.innerHTML = `<div class='p-4 bg-red-900 rounded-xl border border-red-500'><p class="font-bold text-red-400">ERRORE ANALISI</p><p class="text-white">${e.message}</p></div>`; 
    }
}

// Avvio
loadData();
</script>
</body>
</html>
"""
components.html(html_code, height=1800, scrolling=True)
