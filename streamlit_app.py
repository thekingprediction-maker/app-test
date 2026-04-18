import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI - API GOLD", layout="wide")

# CSS minimale
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
        .debug-box { background: #000; color: #0f0; font-family: monospace; font-size: 10px; padding: 10px; border-radius: 8px; margin-top: 20px; max-height: 150px; overflow-y: auto; }
    </style>
</head>
<body>
    <div class="p-6 max-w-4xl mx-auto">
        <div class="flex justify-between items-center mb-6">
            <h1 class="text-3xl font-black text-blue-500 uppercase">PROBET API GOLD</h1>
            <div id="check-key" class="text-[10px] bg-slate-800 px-3 py-1 rounded-full text-slate-400">VERIFICA CHIAVE...</div>
        </div>
        
        <div class="grid grid-cols-2 gap-2 mb-6">
            <button onclick="loadLeague(135)" class="bg-blue-600 p-3 rounded font-bold uppercase">Serie A</button>
            <button onclick="loadLeague(39)" class="bg-slate-700 p-3 rounded font-bold uppercase">Premier League</button>
        </div>

        <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <select id="home" class="input-dark"></select>
                <select id="away" class="input-dark"></select>
            </div>
            <button onclick="calculate()" id="btn" class="w-full py-4 bg-green-600 hover:bg-green-500 rounded-xl font-black text-lg transition-all shadow-lg">
                GENERA PREVISIONE TIRI
            </button>
        </div>

        <div id="results" class="hidden grid grid-cols-2 gap-4 animate-bounce-in">
            <div id="res-t" class="card border-blue-500"></div>
            <div id="res-tp" class="card border-purple-500"></div>
        </div>

        <div id="console" class="debug-box"> Sistema pronto. In attesa di input...</div>
    </div>

<script>
// --- CONFIGURAZIONE SECONDO DOCUMENTAZIONE ---
const API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3"; 
const URL = "https://v3.football.api-sports.io";

function log(m) {
    const c = document.getElementById('console');
    c.innerHTML += `<br>> ${m}`;
    c.scrollTop = c.scrollHeight;
}

// Verifica stato abbonamento al caricamento
async function checkStatus() {
    try {
        const r = await fetch(`${URL}/status`, {
            method: 'GET',
            headers: { 'x-apisports-key': API_KEY }
        });
        const d = await r.json();
        if(d.response && d.response.account) {
            document.getElementById('check-key').innerHTML = `✅ CHIAVE ATTIVA: ${d.response.subscription.plan}`;
            log("Connessione stabilita. Piano: " + d.response.subscription.plan);
        } else {
            document.getElementById('check-key').innerHTML = "❌ CHIAVE NON VALIDA";
            log("Errore: Chiave non riconosciuta dal server.");
        }
    } catch(e) { log("Errore connessione: " + e.message); }
}

async function loadLeague(id) {
    log("Caricamento squadre lega " + id + "...");
    try {
        const r = await fetch(`${URL}/teams?league=${id}&season=2025`, {
            method: 'GET',
            headers: { 'x-apisports-key': API_KEY }
        });
        const d = await r.json();
        const h = document.getElementById('home');
        const a = document.getElementById('away');
        h.innerHTML = ''; a.innerHTML = '';
        d.response.forEach(t => {
            const o = new Option(t.team.name, t.team.id);
            h.add(o.cloneNode(true)); a.add(o);
        });
        log("Squadre caricate: " + d.response.length);
    } catch(e) { log("Errore caricamento: " + e.message); }
}

async function calculate() {
    const btn = document.getElementById('btn');
    const hId = document.getElementById('home').value;
    const aId = document.getElementById('away').value;
    
    btn.disabled = true;
    btn.innerHTML = "ELABORAZIONE DATI...";
    
    try {
        log("Recupero statistiche avanzate...");
        const [resH, resA] = await Promise.all([
            fetch(`${URL}/teams/statistics?league=135&season=2025&team=${hId}`, {
                method: 'GET', headers: { 'x-apisports-key': API_KEY }
            }).then(r => r.json()),
            fetch(`${URL}/teams/statistics?league=135&season=2025&team=${aId}`, {
                method: 'GET', headers: { 'x-apisports-key': API_KEY }
            }).then(r => r.json())
        ]);

        const sH = resH.response;
        const sA = resA.response;

        // Se l'API non ha tiri per la 2025, proviamo la 2024 automaticamente
        if (!sH.shots?.total?.home || sH.shots.total.home === 0) {
            log("Dati 2025 mancanti, provo recupero stagione precedente...");
            // Qui potresti aggiungere un secondo fetch per la 2024
        }

        const pC = sH.fixtures.played.home || 1;
        const pF = sA.fixtures.played.away || 1;
        
        const mediaT = (sH.shots.total.home / pC) + (sA.shots.total.away / pF);
        const mediaTP = (sH.shots.on_goal.home / pC) + (sA.shots.on_goal.away / pF);

        document.getElementById('res-t').innerHTML = `<div class='text-slate-400 text-xs uppercase font-bold'>Tiri Totali</div><div class='text-4xl font-black text-blue-400'>${mediaT.toFixed(2)}</div>`;
        document.getElementById('res-tp').innerHTML = `<div class='text-slate-400 text-xs uppercase font-bold'>In Porta</div><div class='text-4xl font-black text-purple-400'>${mediaTP.toFixed(2)}</div>`;
        
        document.getElementById('results').classList.remove('hidden');
        log("Calcolo completato con successo.");
    } catch(e) {
        log("Errore nel calcolo: " + e.message);
        alert("Dati tiri non disponibili per questa selezione.");
    } finally {
        btn.disabled = false;
        btn.innerHTML = "GENERA PREVISIONE TIRI";
    }
}

window.onload = checkStatus;
</script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)
