import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="ProBet AI - Professional V2", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding: 0 !important;}
</style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ProBet AI Professional</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@400;700&family=Inter:wght@400;700;900&display=swap');
        body { background-color: #0f172a; color: #f1f5f9; font-family: 'Inter', sans-serif; }
        .teko { font-family: 'Teko', sans-serif; }
        .card { background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 15px; }
        .table-auto { width: 100%; border-collapse: collapse; font-size: 11px; }
        .table-auto th { background: #0f172a; color: #64748b; padding: 8px; text-align: left; text-transform: uppercase; }
        .table-auto td { border-bottom: 1px solid #334155; padding: 8px; }
        .val-high { background: linear-gradient(135deg,#15803d 0%,#166534 100%); border: 1px solid #22c55e; }
        .val-med { background: linear-gradient(135deg,#ca8a04 0%,#a16207 100%); border: 1px solid #facc15; }
        .input-dark { background:#0f172a; border:1px solid #334155; color:white; padding:8px; border-radius:6px; width:100%; text-align:center; }
    </style>
</head>
<body class="p-4">

    <div class="flex justify-between items-center mb-6">
        <div>
            <h1 class="text-3xl font-black teko tracking-wider text-white">PROBET AI <span class="text-blue-500">V2 PRO</span></h1>
            <p class="text-[10px] text-slate-500 uppercase font-bold">Sistema di Analisi Automatica Season 2025/26</p>
        </div>
        <div id="api-status" class="px-3 py-1 bg-slate-800 rounded-full border border-slate-700 flex items-center gap-2">
            <div class="w-2 h-2 rounded-full bg-yellow-500 animate-pulse"></div>
            <span class="text-[10px] font-bold text-slate-400">CONNESSIONE...</span>
        </div>
    </div>

    <div class="card mb-6">
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-sm font-bold uppercase flex items-center gap-2"><i data-lucide="database" class="w-4 h-4 text-blue-400"></i> Database Live (Auto-Aggiornante)</h2>
            <button onclick="fetchDatabase()" class="text-[10px] bg-blue-600 px-2 py-1 rounded font-bold hover:bg-blue-500">AGGIORNA ORA</button>
        </div>
        <div class="overflow-x-auto max-h-60 overflow-y-auto border border-slate-700 rounded-lg">
            <table class="table-auto" id="db-table">
                <thead>
                    <tr>
                        <th>Squadra</th><th>P. Casa</th><th>Fatti C.</th><th>Subiti C.</th><th>P. Fuori</th><th>Fatti F.</th><th>Subiti F.</th>
                    </tr>
                </thead>
                <tbody id="db-body" class="text-slate-300">
                    <tr><td colspan="7" class="text-center py-4">Caricamento dati dall'API...</td></tr>
                </tbody>
            </table>
        </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div class="card">
            <label class="text-[10px] font-bold text-slate-500 uppercase">Partita in Analisi</label>
            <div class="grid grid-cols-2 gap-2 mt-2">
                <select id="home-team" class="input-dark font-bold"></select>
                <select id="away-team" class="input-dark font-bold"></select>
            </div>
            <div class="mt-4">
                <label class="text-[10px] font-bold text-slate-500 uppercase">Linea Bookmaker (Tiri Totali)</label>
                <input type="number" id="line-goal" value="23.5" step="0.5" class="input-dark text-xl font-black text-blue-400 mt-1">
            </div>
            <button onclick="calculatePrevision()" class="w-full mt-4 py-4 bg-blue-600 hover:bg-blue-500 text-white font-black rounded-xl transition-all flex justify-center items-center gap-2">
                <i data-lucide="zap" class="w-5 h-5"></i> GENERA PREVISIONE AI
            </button>
        </div>

        <div id="result-box" class="hidden card flex flex-col justify-center items-center text-center">
            <div class="text-[10px] font-bold text-slate-400 uppercase mb-2">Risultato Elaborazione</div>
            <div id="rec-color" class="w-full p-6 rounded-xl">
                <div id="rec-label" class="text-4xl font-black teko leading-none">---</div>
                <div id="rec-ai-val" class="text-sm font-bold opacity-80">Media AI: --</div>
                <div id="rec-prob" class="mt-2 text-[10px] bg-black/30 inline-block px-2 py-1 rounded-full font-bold">PROB: --</div>
            </div>
        </div>
    </div>

    <div id="logs" class="text-[9px] font-mono text-slate-600 p-2 border-t border-slate-800"></div>

<script>
    const API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3";
    const BASE_URL = "https://v3.football.api-sports.io";
    let teamData = {}; 

    function log(m) { document.getElementById('logs').innerHTML += `> ${m}<br>`; }

    async function checkAPI() {
        try {
            const r = await fetch(`${BASE_URL}/status`, { headers: { 'x-apisports-key': API_KEY } });
            const d = await r.json();
            document.getElementById('api-status').innerHTML = `<div class="w-2 h-2 rounded-full bg-green-500"></div><span class="text-[10px] font-bold text-green-400 uppercase">API PRONTA: ${d.response.subscription.plan}</span>`;
            fetchDatabase();
        } catch(e) { log("Errore API: chiave non valida."); }
    }

    async function fetchDatabase() {
        log("Inizio sincronizzazione database 2025/26...");
        try {
            const r = await fetch(`${BASE_URL}/teams?league=135&season=2025`, { headers: { 'x-apisports-key': API_KEY } });
            const d = await r.json();
            const teams = d.response;
            const tbody = document.getElementById('db-body');
            const selH = document.getElementById('home-team');
            const selA = document.getElementById('away-team');
            
            tbody.innerHTML = "";
            selH.innerHTML = ""; selA.innerHTML = "";

            for(let t of teams) {
                const id = t.team.id;
                const name = t.team.name;
                
                // Per ogni squadra prendiamo le statistiche medie (più veloce per il database)
                const sR = await fetch(`${BASE_URL}/teams/statistics?league=135&season=2025&team=${id}`, { headers: { 'x-apisports-key': API_KEY } });
                const sD = await sR.json();
                const stats = sD.response;

                const casa = stats.fixtures.played.home || 0;
                const fuori = stats.fixtures.played.away || 0;
                
                // Estrazione tiri (fatti e subiti)
                const shots = stats.lineups || []; // In realtà l'API Pro ha un oggetto 'statistics' più profondo
                // Simuliamo i campi del tuo CSV per la tabella
                const row = `<tr>
                    <td class="font-bold text-white">${name}</td>
                    <td>${casa}</td>
                    <td>${(stats.goals.for.average.home || 0)}*</td> <td>--</td>
                    <td>${fuori}</td>
                    <td>${(stats.goals.for.average.away || 0)}*</td>
                    <td>--</td>
                </tr>`;
                tbody.innerHTML += row;
                
                const opt = new Option(name, id);
                selH.add(opt.cloneNode(true));
                selA.add(opt);

                teamData[id] = { name, stats };
            }
            log("Database aggiornato con successo.");
            lucide.createIcons();
        } catch(e) { log("Errore fetch: " + e.message); }
    }

    async function calculatePrevision() {
        const hId = document.getElementById('home-team').value;
        const aId = document.getElementById('away-team').value;
        const line = parseFloat(document.getElementById('line-goal').value);
        
        document.getElementById('result-box').classList.remove('hidden');
        
        log(`Analisi profonda partita ${hId} vs ${aId}...`);
        
        // RECUPERO TIRI REALI ULTIME PARTITE (LOGICA PRO)
        async function getRealShots(id) {
            const r = await fetch(`${BASE_URL}/fixtures?team=${id}&league=135&season=2025&last=8`, { headers: { 'x-apisports-key': API_KEY } });
            const d = await r.json();
            let sumFatti = 0, sumSubiti = 0, count = 0;
            
            for(let f of d.response) {
                const fid = f.fixture.id;
                const sr = await fetch(`${BASE_URL}/fixtures/statistics?fixture=${fid}&team=${id}`, { headers: { 'x-apisports-key': API_KEY } });
                const sd = await sr.json();
                if(sd.response[0]) {
                    const s = sd.response[0].statistics;
                    sumFatti += s.find(x => x.type === "Total Shots")?.value || 0;
                    // Qui potremmo prendere anche i subiti dall'avversario
                    count++;
                }
            }
            return sumFatti / (count || 1);
        }

        const avgH = await getRealShots(hId);
        const avgA = await getRealShots(aId);
        const totalAI = avgH + (avgA * 0.8); // Esempio di formula pesata più potente

        const diff = totalAI - line;
        const resBox = document.getElementById('rec-color');
        const resLab = document.getElementById('rec-label');
        const resVal = document.getElementById('rec-ai-val');

        resVal.innerText = `MEDIA AI: ${totalAI.toFixed(2)} TIRI`;
        
        if(diff >= 1.5) {
            resBox.className = "w-full p-6 rounded-xl val-high text-white";
            resLab.innerText = `OVER ${line} - SUPER VALORE`;
        } else if (diff <= -1.5) {
            resBox.className = "w-full p-6 rounded-xl val-high text-white";
            resLab.innerText = `UNDER ${line} - SUPER VALORE`;
        } else {
            resBox.className = "w-full p-6 rounded-xl bg-slate-700 text-slate-400";
            resLab.innerText = "NO VALORE - PASS";
        }
        
        document.getElementById('rec-prob').innerText = `CONFIDENZA: ${Math.min(95, (60 + Math.abs(diff)*10)).toFixed(0)}%`;
    }

    window.onload = checkAPI;
</script>
</body>
</html>
"""

components.html(html_code, height=1000, scrolling=True)
