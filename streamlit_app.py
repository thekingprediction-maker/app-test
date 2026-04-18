import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="ProBet AI V2 PRO", layout="wide", initial_sidebar_state="collapsed")

# --- QUI METTI LA TUA CHIAVE API SE SERVE PER ALTRE FUNZIONI ---
# Al momento l'app legge i CSV dai tuoi link GitHub per essere istantanea.
API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3" 

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container { padding: 0 !important; margin: 0 !important; }
iframe { width: 100vw !important; height: 100vh !important; border: none !important; }
</style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600&family=Inter:wght@400;700&display=swap');
        body { background-color: #0b1120; color: white; font-family: 'Inter', sans-serif; }
        .teko { font-family: 'Teko', sans-serif; }
        .input-dark { background:#1e293b; border:1px solid #334155; color:white; padding:10px; border-radius:8px; width:100%; text-align:center; font-weight:700; }
        .value-box { padding:15px; border-radius:12px; margin-bottom:10px; text-align:center; border:1px solid; position:relative; }
        .val-high { background: linear-gradient(180deg, #064e3b 0%, #065f46 100%); border-color: #10b981; }
        .val-med { background: linear-gradient(180deg, #78350f 0%, #92400e 100%); border-color: #f59e0b; }
        .val-low { background: #1f2937; border-color: #374151; color: #9ca3af; }
        .res { font-size:24px; font-weight:900; font-family:'Teko',sans-serif; }
    </style>
</head>
<body>
    <header class="p-4 border-b border-slate-800 flex justify-between items-center bg-slate-900/50">
        <div class="text-2xl font-bold teko tracking-widest">PROBET <span class="text-indigo-500">AI V2 PRO</span></div>
        <div class="px-3 py-1 rounded-full border border-emerald-500 text-emerald-500 text-[10px] font-bold">● SYSTEM READY</div>
    </header>

    <main class="p-4 max-w-2xl mx-auto">
        <div class="flex gap-2 mb-6">
            <button onclick="switchLeague('SERIE_A')" id="btn-sa" class="flex-1 py-3 rounded-lg bg-indigo-600 font-bold">SERIE A</button>
            <button onclick="switchLeague('PREMIER')" id="btn-pl" class="flex-1 py-3 rounded-lg bg-slate-800 text-slate-400 font-bold">PREMIER</button>
        </div>

        <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800 mb-6">
            <div class="grid grid-cols-2 gap-4 mb-4">
                <select id="home" class="input-dark"></select>
                <select id="away" class="input-dark"></select>
            </div>
            <select id="referee" class="input-dark mb-6 text-yellow-400"></select>
            
            <div class="grid grid-cols-3 gap-2 mb-6">
                <div><label class="text-[9px] text-slate-500 block text-center">LINEA FALLI</label><input type="number" id="line-f-match" value="24.5" step="0.5" class="input-dark"></div>
                <div><label class="text-[9px] text-slate-500 block text-center">LINEA TIRI</label><input type="number" id="line-t-match" value="23.5" step="0.5" class="input-dark"></div>
                <div><label class="text-[9px] text-slate-500 block text-center">LINEA PORTA</label><input type="number" id="line-tp-match" value="8.5" step="0.5" class="input-dark"></div>
            </div>

            <button onclick="calculate()" class="w-full py-4 bg-indigo-600 rounded-xl font-bold text-lg shadow-lg active:scale-95 transition-all">ANALIZZA MATCH</button>
        </div>

        <div id="results" class="hidden">
            <div id="grid-falli" class="grid grid-cols-1 gap-3 mb-6"></div>
            <div id="grid-tiri" class="grid grid-cols-1 gap-3 mb-6"></div>
            <div id="grid-tp" class="grid grid-cols-1 gap-3"></div>
        </div>
    </main>

    <script>
        // I TUOI LINK GITHUB (Quelli che l'app legge velocemente)
        const LINKS = {
            SERIE_A: {
                arb: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/ARBITRI_SERIE_A%20-%20Foglio1.csv",
                tiri: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/TIRI_SERIE_A%20%20-%20DATI%20TIRI%20TOTALI%20E%20TIRI%20IN%20PORTA%20STAGIONE%202025_26.csv"
            },
            PREMIER: {
                tiri: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/TIRI_PREMIER_LEAGUE%20-%20DATI%20TIRI%20TOTALI%20E%20TIRI%20IN%20PORTA%20STAGIONE%202025_26.csv"
            }
        };

        let DB = { refs: [], tiri: [] };

        async function switchLeague(l) {
            const r = await fetch(LINKS[l].tiri);
            const txt = await r.text();
            const d = Papa.parse(txt, {header:false}).data;
            let start = d.findIndex(row => row[0] && row[0].includes("Squadra")) + 1;
            DB.tiri = d.slice(start).map(r => ({
                Team: r[0], TFC: (r[2]/r[1]||0), TSC: (r[3]/r[1]||0), TFF: (r[7]/r[6]||0), TSF: (r[8]/r[6]||0),
                TPC: (r[4]/r[1]||0), TPF: (r[9]/r[6]||0), TPSF: (r[10]/r[6]||0), TPSC: (r[5]/r[1]||0)
            }));
            
            const h = document.getElementById('home'), a = document.getElementById('away');
            h.innerHTML = ''; a.innerHTML = '';
            [...new Set(DB.tiri.map(x=>x.Team))].sort().forEach(t => { h.add(new Option(t,t)); a.add(new Option(t,t)); });
        }

        function calculate() {
            const home = document.getElementById('home').value, away = document.getElementById('away').value;
            const hS = DB.tiri.find(x=>x.Team === home), aS = DB.tiri.find(x=>x.Team === away);
            
            const expTiri = (hS.TFC + aS.TSF)/2 + (aS.TFF + hS.TSC)/2;
            const expTP = (hS.TPC + aS.TPSF)/2 + (aS.TPF + hS.TPSC)/2;

            renderBox('grid-tiri', "TIRI TOTALI", expTiri, 'line-t-match');
            renderBox('grid-tp', "TIRI IN PORTA", expTP, 'line-tp-match');
            document.getElementById('results').classList.remove('hidden');
        }

        function renderBox(id, title, val, lineId) {
            const line = parseFloat(document.getElementById(lineId).value);
            const diff = val - line;
            let css = "val-low", txt = "PASS";
            if(diff >= 1.5) { css="val-high"; txt="OVER " + line; }
            else if(diff >= 0.5) { css="val-med"; txt="OVER " + line; }
            
            document.getElementById(id).innerHTML = `
                <div class="value-box ${css}">
                    <div class="text-[10px] uppercase font-bold opacity-60">${title}</div>
                    <div class="res">${txt}</div>
                    <div class="text-xs font-bold">AI PREV: ${val.toFixed(2)}</div>
                </div>`;
        }

        switchLeague('SERIE_A');
    </script>
</body>
</html>
"""

components.html(html_code, height=1000)
