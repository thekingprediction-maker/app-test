import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI - CALCOLO REALE", layout="wide")

st.markdown("""<style>#MainMenu, footer, header {visibility: hidden;} .block-container {padding:0;}</style>""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@700&family=Inter:wght@400;900&display=swap');
        body { background: #0f172a; color: white; font-family: 'Inter', sans-serif; }
        .card { background: #1e293b; border-radius: 15px; padding: 20px; border: 1px solid #334155; text-align: center; }
        .input-dark { background: #1e293b; border: 1px solid #3b82f6; color: white; padding: 10px; border-radius: 8px; width: 100%; }
        .console { background: #000; color: #0f0; font-family: monospace; font-size: 11px; padding: 10px; border-radius: 8px; margin-top: 20px; height: 150px; overflow-y: auto; border: 1px solid #050; }
    </style>
</head>
<body>
    <div class="p-6 max-w-4xl mx-auto">
        <div class="flex justify-between items-center mb-6">
            <h1 class="text-3xl font-black text-blue-500 uppercase tracking-tighter">ProBet AI <span class="text-white">PRO</span></h1>
            <div id="status" class="text-[10px] bg-slate-800 px-3 py-1 rounded-full text-green-400 font-bold">VERIFICA...</div>
        </div>
        
        <div class="grid grid-cols-2 gap-2 mb-6">
            <button onclick="loadLeague(135)" class="bg-blue-600 p-3 rounded font-bold uppercase hover:bg-blue-500">Serie A</button>
            <button onclick="loadLeague(39)" class="bg-slate-700 p-3 rounded font-bold uppercase hover:bg-slate-600">Premier League</button>
        </div>

        <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800 mb-6 shadow-2xl">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div><label class="text-[10px] text-slate-500 ml-1">CASA</label><select id="home" class="input-dark"></select></div>
                <div><label class="text-[10px] text-slate-500 ml-1">OSPITE</label><select id="away" class="input-dark"></select></div>
            </div>
            <button onclick="runDeepAnalysis()" id="btn" class="w-full py-5 bg-green-600 hover:bg-green-500 rounded-xl font-black text-xl transition-all shadow-lg active:scale-95">
                GENERA PREVISIONE (LIVE DATA)
            </button>
        </div>

        <div id="results" class="hidden grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="card border-blue-500/50">
                <div class="text-xs text-slate-400 uppercase">Media Tiri Totali</div>
                <div id="res-t" class="text-5xl font-black text-blue-400 my-2">--</div>
            </div>
            <div class="card border-purple-500/50">
                <div class="text-xs text-slate-400 uppercase">Media Tiri In Porta</div>
                <div id="res-tp" class="text-5xl font-black text-purple-400 my-2">--</div>
            </div>
        </div>

        <div id="console" class="console text-green-500">Inizializzazione sistema...</div>
    </div>

<script>
const API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3"; 
const URL = "https://v3.football.api-sports.io";
let leagueId = 135;

function log(msg) {
    const c = document.getElementById('console');
    c.innerHTML += `<br>> ${msg}`;
    c.scrollTop = c.scrollHeight;
}

async function check() {
    try {
        const r = await fetch(`${URL}/status`, { headers: { 'x-apisports-key': API_KEY } });
        const d = await r.json();
        document.getElementById('status').innerText = "PIANO: " + d.response.subscription.plan.toUpperCase();
        log("Sistema pronto. Piano rilevato: " + d.response.subscription.plan);
    } catch(e) { log("Errore connessione: " + e.message); }
}

async function loadLeague(id) {
    leagueId = id;
    log("Caricamento squadre lega " + id + "...");
    try {
        const r = await fetch(`${URL}/teams?league=${id}&season=2025`, { headers: { 'x-apisports-key': API_KEY } });
        const d = await r.json();
        const h = document.getElementById('home');
        const a = document.getElementById('away');
        h.innerHTML = ''; a.innerHTML = '';
        d.response.forEach(t => {
            const o = new Option(t.team.name, t.team.id);
            h.add(o.cloneNode(true)); a.add(o);
        });
        log("Squadre caricate: " + d.response.length);
    } catch(e) { log("Errore: " + e.message); }
}

async function getStats(teamId) {
    log("Analisi ultime partite per team " + teamId + "...");
    // Prendiamo le ultime 10 partite giocate
    const r = await fetch(`${URL}/fixtures?team=${teamId}&league=${leagueId}&season=2025&last=10`, {
        headers: { 'x-apisports-key': API_KEY }
    });
    const d = await r.json();
    
    let shots = 0, onGoal = 0, count = 0;

    for (const fix of d.response) {
        const fid = fix.fixture.id;
        const sr = await fetch(`${URL}/fixtures/statistics?fixture=${fid}&team=${teamId}`, {
            headers: { 'x-apisports-key': API_KEY }
        });
        const sd = await sr.json();
        if (sd.response && sd.response[0]) {
            const s = sd.response[0].statistics;
            shots += s.find(x => x.type === "Total Shots")?.value || 0;
            onGoal += s.find(x => x.type === "Shots on Goal")?.value || 0;
            count++;
        }
    }
    return { shots: shots / (count || 1), onGoal: onGoal / (count || 1) };
}

async function runDeepAnalysis() {
    const btn = document.getElementById('btn');
    btn.disabled = true; btn.innerText = "CALCOLO IN CORSO (MATRICE PARTITE)...";
    
    try {
        const hId = document.getElementById('home').value;
        const aId = document.getElementById('away').value;
        
        const homeS = await getStats(hId);
        const awayS = await getStats(aId);
        
        const totalT = homeS.shots + awayS.shots;
        const totalTP = homeS.onGoal + awayS.onGoal;

        document.getElementById('res-t').innerText = totalT.toFixed(2);
        document.getElementById('res-tp').innerText = totalTP.toFixed(2);
        document.getElementById('results').classList.remove('hidden');
        log("Previsione generata con successo.");
    } catch(e) {
        log("ERRORE: " + e.message);
        alert("Errore durante il recupero dei dati delle partite.");
    } finally {
        btn.disabled = false; btn.innerText = "GENERA PREVISIONE (LIVE DATA)";
    }
}

window.onload = () => { check(); loadLeague(135); };
</script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)
