import streamlit as st
import streamlit.components.v1 as components

# Configurazione Streamlit per l'app di TEST
st.set_page_config(page_title="PROBET AI - TEST API", layout="wide", initial_sidebar_state="collapsed")

# CSS per pulire l'interfaccia
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container { padding: 0 !important; }
iframe { width: 100vw; height: 100vh; border: none; }
</style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@400;700&family=Inter:wght@400;900&display=swap');
        body { background-color: #0f172a; color: #e2e8f0; font-family: 'Inter', sans-serif; }
        .teko { font-family: 'Teko', sans-serif; }
        .input-dark { background:#1e293b; border:1px solid #334155; color:white; padding:12px; border-radius:12px; width:100%; text-align:center; font-weight:bold; outline:none; font-size: 16px; }
        .btn-league { padding: 12px; border-radius: 12px; font-weight: 800; font-size: 12px; transition: 0.3s; background: #1e293b; color: #94a3b8; border: 1px solid #334155; }
        .btn-active { background: #3b82f6; color: white; border-color: #60a5fa; box-shadow: 0 0 20px rgba(59,130,246,0.3); }
        .card-res { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border-radius: 20px; padding: 25px; border: 1px solid #334155; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        .loader { width:20px; height:20px; border:3px solid #334155; border-bottom-color:#3b82f6; border-radius:50%; display:inline-block; animation: rot 1s linear infinite; }
        @keyframes rot { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .prob-badge { background: rgba(59,130,246,0.2); color: #60a5fa; padding: 5px 15px; border-radius: 99px; font-weight: 900; font-size: 14px; margin-top: 10px; display: inline-block; border: 1px solid rgba(96,165,250,0.3); }
    </style>
</head>
<body>
    <header class="p-4 border-b border-slate-800 flex justify-between items-center bg-slate-900/80 backdrop-blur-md sticky top-0 z-50">
        <div class="text-2xl font-bold teko tracking-widest uppercase">PROBET <span class="text-blue-500">AI TEST</span></div>
        <div id="status" class="text-[10px] font-black bg-slate-800 px-4 py-1.5 rounded-full border border-slate-700 flex items-center gap-2">
            <div id="status-icon" class="w-2 h-2 bg-yellow-500 rounded-full"></div> <span id="status-text">AVVIO...</span>
        </div>
    </header>

    <main class="p-4 max-w-4xl mx-auto pb-20">
        <div class="grid grid-cols-3 gap-2 mb-8">
            <button onclick="changeLeague(135, 'b-sa')" id="b-sa" class="btn-league btn-active text-white">SERIE A</button>
            <button onclick="changeLeague(39, 'b-pl')" id="b-pl" class="btn-league">PREMIER</button>
            <button onclick="changeLeague(140, 'b-lg')" id="b-lg" class="btn-league">LA LIGA</button>
        </div>

        <div class="bg-slate-900/50 p-6 rounded-3xl border border-slate-800 shadow-2xl mb-8">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div>
                    <label class="text-[10px] font-black text-slate-500 uppercase ml-2">CASA</label>
                    <select id="home" class="input-dark mt-1"></select>
                </div>
                <div>
                    <label class="text-[10px] font-black text-slate-500 uppercase ml-2">OSPITE</label>
                    <select id="away" class="input-dark mt-1"></select>
                </div>
            </div>

            <div class="grid grid-cols-2 gap-4 mb-8">
                <div>
                    <label class="text-[10px] font-black text-slate-500 uppercase ml-2">LINEA TIRI TOT.</label>
                    <input type="number" id="line-t" value="23.5" step="0.5" class="input-dark mt-1">
                </div>
                <div>
                    <label class="text-[10px] font-black text-slate-500 uppercase ml-2">LINEA IN PORTA</label>
                    <input type="number" id="line-tp" value="8.5" step="0.5" class="input-dark mt-1">
                </div>
            </div>

            <button onclick="analyze()" id="main-btn" class="w-full py-5 bg-blue-600 hover:bg-blue-500 rounded-2xl font-black text-xl transition-all shadow-lg active:scale-95">
                ELABORA DATI API LIVE
            </button>
        </div>

        <div id="results" class="hidden space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div id="res-tiri" class="card-res"></div>
                <div id="res-tp" class="card-res"></div>
            </div>
        </div>
    </main>

<script>
const API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3";
const HOST = "v3.football.api-sports.io";
const SEASON = "2025"; 

let currentLeague = 135;

async function changeLeague(id, btnId) {
    currentLeague = id;
    document.querySelectorAll('.btn-league').forEach(b => b.classList.remove('btn-active', 'text-white'));
    document.getElementById(btnId).classList.add('btn-active', 'text-white');
    await loadTeams();
}

async function loadTeams() {
    updateStatus('yellow', 'CARICAMENTO SQUADRE...');
    try {
        const res = await fetch(`https://${HOST}/teams?league=${currentLeague}&season=${SEASON}`, {
            headers: { "x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST }
        });
        const data = await res.json();
        
        const h = document.getElementById('home');
        const a = document.getElementById('away');
        h.innerHTML = ''; a.innerHTML = '';
        
        data.response.forEach(item => {
            const opt = new Option(item.team.name, item.team.id);
            h.add(opt.cloneNode(true));
            a.add(opt);
        });
        updateStatus('green', 'API PRONTA');
    } catch(e) {
        updateStatus('red', 'ERRORE CONNESSIONE');
    }
}

async function analyze() {
    const btn = document.getElementById('main-btn');
    const idHome = document.getElementById('home').value;
    const idAway = document.getElementById('away').value;
    
    btn.disabled = true;
    btn.innerHTML = '<div class="loader"></div> ELABORAZIONE...';
    
    try {
        const [resH, resA] = await Promise.all([
            fetch(`https://${HOST}/teams/statistics?league=${currentLeague}&season=${SEASON}&team=${idHome}`, {
                headers: { "x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST }
            }).then(r => r.json()),
            fetch(`https://${HOST}/teams/statistics?league=${currentLeague}&season=${SEASON}&team=${idAway}`, {
                headers: { "x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST }
            }).then(r => r.json())
        ]);

        if (!resH.response || !resA.response) {
            throw new Error("Dati non disponibili per questa stagione");
        }

        const sH = resH.response;
        const sA = resA.response;

        // Estrazione dati con paracadute se mancano valori
        const tfC = (sH.shots?.total?.home) || 0;
        const tfF = (sA.shots?.total?.away) || 0;
        const tpfC = (sH.shots?.on_goal?.home) || 0;
        const tpfF = (sA.shots?.on_goal?.away) || 0;
        
        const pC = (sH.fixtures?.played?.home) || 1;
        const pF = (sA.fixtures?.played?.away) || 1;
        
        const mediaT = (tfC / pC) + (tfF / pF);
        const mediaTP = (tpfC / pC) + (tpfF / pF);

        if (mediaT === 0) {
            alert("L'API non ha ancora dati sui tiri per queste squadre in questa stagione.");
            return;
        }

        renderResults(mediaT, mediaTP);
        document.getElementById('results').classList.remove('hidden');
    } catch(e) {
        alert("Errore API: " + e.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = 'ELABORA DATI API LIVE';
    }
}

function renderResults(mt, mtp) {
    const lineT = parseFloat(document.getElementById('line-t').value);
    const lineTP = parseFloat(document.getElementById('line-tp').value);
    
    const getProb = (m, l) => {
        const type = m > l ? 'OVER' : 'UNDER';
        let p = m > l ? (m / l) * 45 : (l / m) * 45;
        if (p > 92) p = 92; if (p < 55) p = 55;
        return { type, p };
    };

    const resT = getProb(mt, lineT);
    const resTP = getProb(mtp, lineTP);

    document.getElementById('res-tiri').innerHTML = `
        <div class="text-[10px] font-bold text-blue-400 uppercase">Tiri Totali Previsti</div>
        <div class="text-5xl font-black my-2 text-white">${mt.toFixed(2)}</div>
        <div class="text-xl font-bold text-blue-500">${resT.type} ${lineT}</div>
        <div class="prob-badge">PROBABILITÀ ${resT.p.toFixed(1)}%</div>
    `;

    document.getElementById('res-tp').innerHTML = `
        <div class="text-[10px] font-bold text-purple-400 uppercase">Tiri in Porta Previsti</div>
        <div class="text-5xl font-black my-2 text-white">${mtp.toFixed(2)}</div>
        <div class="text-xl font-bold text-purple-500">${resTP.type} ${lineTP}</div>
        <div class="prob-badge">PROBABILITÀ ${resTP.p.toFixed(1)}%</div>
    `;
}

function updateStatus(color, text) {
    const colors = { green: 'bg-green-500', yellow: 'bg-yellow-500', red: 'bg-red-500' };
    document.getElementById('status-icon').className = `w-2 h-2 rounded-full ${colors[color]}`;
    document.getElementById('status-text').innerText = text;
}

window.onload = loadTeams;
</script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)
