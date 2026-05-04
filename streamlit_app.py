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
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600&family=Inter:wght@400;700;900&display=swap');
        body { background: #020617; color: white; font-family: 'Inter', sans-serif; }
        .teko { font-family: 'Teko', sans-serif; }
        .card-premium { background: #1e293b; border-radius: 24px; padding: 30px; border: 1px solid #334155; }
        select, input { background: #0f172a; border: 1px solid #475569; color: white; padding: 12px; width: 100%; border-radius: 12px; font-weight: 700; font-size: 14px; outline: none; }
        .btn-analizza { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); width: 100%; padding: 20px; border-radius: 15px; font-weight: 900; text-transform: uppercase; cursor: pointer; transition: 0.3s; margin-top: 20px; border: none; color: white; }
        .btn-analizza:hover { transform: translateY(-2px); box-shadow: 0 10px 40px rgba(59,130,246,0.4); }
        .res-box { background: #0f172a; border-radius: 20px; padding: 24px; border-left: 5px solid; margin-bottom: 15px; position: relative; overflow: hidden; }
        .res-box::before { content: ''; position: absolute; top: 0; right: 0; width: 150px; height: 150px; background: radial-gradient(circle, rgba(59,130,246,0.1) 0%, transparent 70%); }
        .advice-tag { display: inline-block; padding: 4px 14px; border-radius: 8px; font-size: 13px; font-weight: 900; margin-left: 12px; text-transform: uppercase; letter-spacing: 0.5px; }
        .over-tag { background: linear-gradient(135deg, #10b981, #059669); color: white; box-shadow: 0 4px 15px rgba(16,185,129,0.3); }
        .under-tag { background: linear-gradient(135deg, #ef4444, #dc2626); color: white; box-shadow: 0 4px 15px rgba(239,68,68,0.3); }
        .label-spread { font-size: 11px; font-weight: 900; color: #94a3b8; text-transform: uppercase; margin-bottom: 6px; display: block; letter-spacing: 1px; }
        .league-btn { cursor: pointer; padding: 14px; border-radius: 12px; font-weight: 900; border: 1px solid #334155; text-align: center; font-size: 12px; letter-spacing: 0.5px; transition: all 0.3s; background: #0f172a; }
        .league-active { background: linear-gradient(135deg, #3b82f6, #2563eb); border-color: #3b82f6; color: white; box-shadow: 0 0 20px rgba(59, 130, 246, 0.4); }
        .grid-spreads { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; padding-top: 18px; border-top: 1px solid #334155; margin-bottom: 18px; }
        .status-msg { font-size: 12px; font-weight: 700; padding: 10px 16px; border-radius: 10px; margin-bottom: 16px; display: none; }
        .status-ok { background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid #10b981; }
        .status-err { background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid #ef4444; }
        .confidence-bar { height: 6px; border-radius: 3px; background: #1e293b; margin-top: 12px; overflow: hidden; }
        .confidence-fill { height: 100%; border-radius: 3px; transition: width 0.8s ease; }
        .metric-detail { font-size: 13px; color: #94a3b8; margin-top: 8px; font-weight: 500; }
        .precision-badge { position: absolute; top: 16px; right: 16px; font-size: 11px; font-weight: 900; padding: 4px 10px; border-radius: 6px; background: rgba(59,130,246,0.2); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-5xl mx-auto">
        <div class="text-center mb-10">
            <h1 class="text-6xl font-black teko tracking-widest text-white uppercase italic">PROBET <span class="text-blue-500">AI V4</span></h1>
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

            <button onclick="triggerAdAndCalculate()" class="btn-analizza shadow-xl italic teko text-2xl tracking-widest">GENERA ANALISI ELITE</button>
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
// ALGORITMI DI CALCOLO AVANZATI - PRECISIONE MASSIMA
// ============================================

function calcConfidence(pred, spread) {
    // Modello logistico per calibrare la confidenza
    const diff = pred - spread;
    const rawProb = 1 / (1 + Math.exp(-diff * 0.85));
    const confidence = Math.min(Math.max(rawProb * 100, 8), 96);
    return confidence;
}

function getAdviceAdvanced(pred, spread, metricName) {
    const conf = calcConfidence(pred, spread);
    const isOver = conf >= 50;
    const displayConf = isOver ? conf : 100 - conf;
    const direction = isOver ? 'OVER' : 'UNDER';

    // Determina colore e precisione basata sulla confidenza
    let precisionClass = isOver ? 'over-tag' : 'under-tag';
    let precisionLabel = displayConf >= 75 ? 'ALTA' : displayConf >= 60 ? 'MEDIA' : 'BASE';

    return {
        html: `<span class="advice-tag ${precisionClass}">${direction} ${spread} (${displayConf.toFixed(1)}%)</span>`,
        confidence: displayConf,
        isOver: isOver,
        precision: precisionLabel
    };
}

function renderConfidenceBar(confidence) {
    let color = confidence >= 75 ? '#10b981' : confidence >= 60 ? '#f59e0b' : '#ef4444';
    return `<div class="confidence-bar"><div class="confidence-fill" style="width:${confidence}%;background:${color}"></div></div>`;
}

async function runDeepAnalysis() {
    const resDiv = document.getElementById('results');
    resDiv.innerHTML = "<div class='text-center py-20 animate-pulse text-blue-500 font-black teko text-3xl uppercase tracking-widest'>ANALISI ELITE IN CORSO...</div>";
    resDiv.classList.remove('hidden');

    try {
        const idH = document.getElementById('homeTeam').value;
        const idA = document.getElementById('awayTeam').value;

        if (!idH || !idA) throw new Error("Seleziona entrambe le squadre");
        if (idH === idA) throw new Error("Le squadre devono essere diverse");

        const leagueInfo = LEAGUE_DATA[currentLeague];
        let apiId = leagueInfo.apiId;

        // Recupero statistiche avanzate
        let statsH, statsA;
        try {
            [statsH, statsA] = await Promise.all([
                fetch(`https://v3.football.api-sports.io/teams/statistics?league=${apiId}&season=2025&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
                fetch(`https://v3.football.api-sports.io/teams/statistics?league=${apiId}&season=2025&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
            ]);
            if (!statsH.response || !statsA.response) throw new Error("empty");
        } catch (e) {
            apiId = leagueInfo.oldId;
            [statsH, statsA] = await Promise.all([
                fetch(`https://v3.football.api-sports.io/teams/statistics?league=${apiId}&season=2025&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
                fetch(`https://v3.football.api-sports.io/teams/statistics?league=${apiId}&season=2025&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
            ]);
        }

        const sH = statsH.response; 
        const sA = statsA.response;
        const homeAdv = leagueInfo.homeAdv;

        // ============================================
        // 1. TI TOTALI (SHOTS) - Modello xG Avanzato
        // ============================================
        // xG per shot dal database + correzione qualità
        const xGH_raw = dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || "0.11";
        const xGA_raw = dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || "0.11";
        const xGH = parseFloat(xGH_raw.toString().replace(',', '.'));
        const xGA = parseFloat(xGA_raw.toString().replace(',', '.'));

        // Benchmark xG per campionato (Premier/Bundes più offensivi)
        const bench = (currentLeague === 7293 || currentLeague === 7338) ? 0.12 : 0.11;

        // Tiri medi stagionali con peso forma
        const shotsH_avg = sH.shots?.total?.average || 12.5;
        const shotsA_avg = sA.shots?.total?.average || 10.5;

        // Fattore xG: squadre con xG alto tendono a tirare di più e meglio
        const xgFactorH = 0.7 + (xGH / bench) * 0.3;
        const xgFactorA = 0.7 + (xGA / bench) * 0.3;

        // Calcolo tiri con home advantage e matchup
        const cH = shotsH_avg * xgFactorH * homeAdv * 0.95;
        const cA = shotsA_avg * xgFactorA * 1.0 * 1.05; // away leggermente stimolata
        const totalShots = cH + cA;

        // ============================================
        // 2. TI IN PORTA (SHOTS ON TARGET) - Modello Precisione
        // ============================================
        const onTargetH_avg = sH.shots?.on_goal?.average || 4.2;
        const onTargetA_avg = sA.shots?.on_goal?.average || 3.6;

        // Conversion rate tiri in porta
        const convRateH = onTargetH_avg / shotsH_avg;
        const convRateA = onTargetA_avg / shotsA_avg;

        // xG influisce sulla precisione (squadre con xG alto tirano meglio)
        const precisionH = convRateH * (0.85 + xGH * 2.5);
        const precisionA = convRateA * (0.85 + xGA * 2.5);

        const oH = cH * precisionH * homeAdv;
        const oA = cA * precisionA;
        const totalOnTarget = oH + oA;

        // ============================================
        // 3. CORNER - Modello Pressione + Possesso
        // ============================================
        const cornersForH = sH.corners?.for?.average || 5.2;
        const cornersAgainstH = sH.corners?.against?.average || 4.1;
        const cornersForA = sA.corners?.for?.average || 4.8;
        const cornersAgainstA = sA.corners?.against?.average || 4.4;

        // Pressione offensiva combinata
        const pressureH = (cornersForH + cornersAgainstA) / 2;
        const pressureA = (cornersForA + cornersAgainstH) / 2;

        // Fattore possesso (più possesso = più corner)
        const possH = sH.possession?.average || 52;
        const possA = sA.possession?.average || 48;
        const possFactorH = 0.9 + (possH / 100) * 0.2;
        const possFactorA = 0.9 + (possA / 100) * 0.2;

        const pCH = pressureH * possFactorH * homeAdv * 0.92;
        const pCA = pressureA * possFactorA * 1.08;
        const totalCorners = pCH + pCA;

        // ============================================
        // 4. CARTELLINI GIALLI - Modello Disciplina
        // ============================================
        const yellowH_avg = sH.cards?.yellow?.average || 2.1;
        const yellowA_avg = sA.cards?.yellow?.average || 2.3;
        const foulsH_avg = sH.fouls?.for?.average || 12.5;
        const foulsA_avg = sA.fouls?.for?.average || 13.0;

        // Rapporto falli/giallo (disciplina)
        const disciplineH = foulsH_avg / Math.max(yellowH_avg, 0.5);
        const disciplineA = foulsA_avg / Math.max(yellowA_avg, 0.5);

        // Intensità match (più falli = più gialli probabili)
        const intensityFactor = 1.0 + ((foulsH_avg + foulsA_avg) - 24) / 100;

        const cardH = yellowH_avg * intensityFactor * homeAdv * 0.95;
        const cardA = yellowA_avg * intensityFactor * 1.05;
        const totalCards = cardH + cardA;

        // ============================================
        // 5. FALLI (SOLO SERIE A) - Modello Arbitro
        // ============================================
        let totalFouls = 0, fH = 0, fA = 0;
        if(currentLeague === 7286) {
            const refVal = parseFloat(document.getElementById('arbitroSelect').value) || 24.5;
            const foulsAgainstH = sH.fouls?.against?.average || 11.5;
            const foulsAgainstA = sA.fouls?.against?.average || 12.0;

            // Media ponderata: 60% comportamento squadre, 40% stile arbitro
            fH = ((foulsH_avg + foulsAgainstA) / 2) * 0.6 + (refVal / 2 * 0.4);
            fA = ((foulsA_avg + foulsAgainstH) / 2) * 0.6 + (refVal / 2 * 0.4);
            totalFouls = fH + fA;
        }

        // ============================================
        // RENDERING RISULTATI CON PRECISIONE
        // ============================================
        let html = "";

        // FALLI (Serie A)
        if(currentLeague === 7286) {
            const advFouls = getAdviceAdvanced(totalFouls, parseFloat(document.getElementById('sprFoulsMatch').value), 'falli');
            const advFoulsH = getAdviceAdvanced(fH, parseFloat(document.getElementById('sprFoulsH').value), 'falliH');
            const advFoulsA = getAdviceAdvanced(fA, parseFloat(document.getElementById('sprFoulsA').value), 'falliA');

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
                <p class="metric-detail">Modello: 60% comportamento squadre + 40% stile arbitro • xG H: ${xGH.toFixed(3)} • xG A: ${xGA.toFixed(3)}</p>
            </div>`;
        }

        // TI TOTALI
        const advShots = getAdviceAdvanced(totalShots, parseFloat(document.getElementById('sprTotalMatch').value), 'tiri');
        const advShotsH = getAdviceAdvanced(cH, parseFloat(document.getElementById('sprTotalH').value), 'tiriH');
        const advShotsA = getAdviceAdvanced(cA, parseFloat(document.getElementById('sprTotalA').value), 'tiriA');

        html += `
        <div class="res-box border-l-emerald-500">
            <div class="precision-badge">${advShots.precision}</div>
            <p class="label-spread text-emerald-400">Tiri Totali Previsti</p>
            <h2 class="text-5xl font-black teko">${totalShots.toFixed(2)} ${advShots.html}</h2>
            ${renderConfidenceBar(advShots.confidence)}
            <div class="grid grid-cols-2 mt-4 pt-3 border-t border-slate-800">
                <div><p class="label-spread">Casa</p><p class="text-xl teko text-emerald-400">${cH.toFixed(2)} ${advShotsH.html}</p></div>
                <div class="text-right"><p class="label-spread">Ospite</p><p class="text-xl teko text-emerald-400">${cA.toFixed(2)} ${advShotsA.html}</p></div>
            </div>
            <p class="metric-detail">Modello xG: fattore ${xgFactorH.toFixed(2)} (H) / ${xgFactorA.toFixed(2)} (A) • HomeAdv: ${homeAdv} • Bench: ${bench}</p>
        </div>`;

        // TI IN PORTA
        const advOT = getAdviceAdvanced(totalOnTarget, parseFloat(document.getElementById('sprOTMatch').value), 'porta');
        const advOTH = getAdviceAdvanced(oH, parseFloat(document.getElementById('sprOTH').value), 'portaH');
        const advOTA = getAdviceAdvanced(oA, parseFloat(document.getElementById('sprOTA').value), 'portaA');

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
            <p class="metric-detail">Precisione: ${(convRateH*100).toFixed(1)}% (H) / ${(convRateA*100).toFixed(1)}% (A) • xG-adjusted: ${precisionH.toFixed(2)} / ${precisionA.toFixed(2)}</p>
        </div>`;

        // CORNER
        const advCorn = getAdviceAdvanced(totalCorners, parseFloat(document.getElementById('sprCornMatch').value), 'corner');
        const advCornH = getAdviceAdvanced(pCH, parseFloat(document.getElementById('sprCornH').value), 'cornerH');
        const advCornA = getAdviceAdvanced(pCA, parseFloat(document.getElementById('sprCornA').value), 'cornerA');

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
            <p class="metric-detail">Pressione: ${pressureH.toFixed(1)} (H) / ${pressureA.toFixed(1)} (A) • Possesso: ${possH}% / ${possA}%</p>
        </div>`;

        // CARTELLINI
        const advCards = getAdviceAdvanced(totalCards, parseFloat(document.getElementById('sprCardsMatch').value), 'cards');
        const advCardsH = getAdviceAdvanced(cardH, parseFloat(document.getElementById('sprCardsH').value), 'cardsH');
        const advCardsA = getAdviceAdvanced(cardA, parseFloat(document.getElementById('sprCardsA').value), 'cardsA');

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
            <p class="metric-detail">Disciplina: ${disciplineH.toFixed(1)} falli/giallo (H) / ${disciplineA.toFixed(1)} (A) • Intensità: ${intensityFactor.toFixed(2)}</p>
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
