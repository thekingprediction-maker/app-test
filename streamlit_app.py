import streamlit as st
import streamlit.components.v1 as components

# 1. Configurazione Pagina (Forza il layout Wide e collassa la sidebar)
st.set_page_config(
    page_title="PROBET AI V4 PRO", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. Pulizia Totale Interfaccia Streamlit (CSS Injection)
st.markdown("""
<style>
    /* Nasconde header, footer e menu di Streamlit */
    #MainMenu, header, footer {visibility: hidden;}
    
    /* Forza il background scuro su tutta l'app */
    .stApp {
        background-color: #020617 !important;
    }
    
    /* Rimuove i padding predefiniti per far occupare all'HTML il 100% dello spazio */
    .block-container {
        padding: 0px !important; 
        max-width: 100% !important;
        height: 100vh !important;
    }

    /* Nasconde le scrollbar per un look più "App" */
    ::-webkit-scrollbar {display: none;}
    
    /* Rimuove lo spazio extra in alto */
    .main .block-container {
        padding-top: 0rem !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Codice Applicazione (Interfaccia Grafica Potenziata)
html_code = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600&family=Inter:wght@400;700&display=swap');
        
        body { 
            background: #020617; 
            color: white; 
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .teko { font-family: 'Teko', sans-serif; text-transform: uppercase; }
        
        .main-container {
            width: 100%;
            max-width: 450px;
            padding: 40px 20px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .glass-card {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 28px;
            padding: 30px;
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
        }

        .btn-action {
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            width: 100%;
            padding: 18px;
            border-radius: 16px;
            font-weight: 800;
            margin-top: 24px;
            cursor: pointer;
            border: none;
            color: white;
            transition: all 0.3s ease;
            box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .btn-action:active {
            transform: scale(0.98);
            filter: brightness(1.1);
        }

        select {
            width: 100%; 
            background: #0f172a; 
            color: white; 
            padding: 14px; 
            border-radius: 12px; 
            margin-bottom: 20px; 
            border: 1px solid rgba(255,255,255,0.15);
            font-weight: 600;
            appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='white'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 12px center;
            background-size: 16px;
        }

        label {
            font-size: 11px; 
            color: #60a5fa; 
            text-transform: uppercase; 
            letter-spacing: 0.1em;
            margin-bottom: 8px;
            display: block;
            font-weight: 700;
        }

        .badge {
            background: rgba(59, 130, 246, 0.1);
            color: #60a5fa;
            padding: 4px 12px;
            border-radius: 100px;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1px;
            display: inline-block;
            margin-bottom: 8px;
            border: 1px solid rgba(59, 130, 246, 0.2);
        }
    </style>
</head>
<body>
    <div class="main-container">
        <div style="text-align: center; margin-bottom: 20px;">
            <div class="badge">ELITE SYSTEM ACTIVE</div>
            <h1 class="teko" style="font-size: 4rem; line-height: 0.9; font-style: italic; margin-bottom: 5px;">PROBET <span style="color:#3b82f6">AI</span></h1>
            <p style="color: #94a3b8; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.3em; margin-bottom: 10px;">V4 PRO • ENGINE V2.0</p>
        </div>
        
        <div class="glass-card">
            <div>
                <label>SQUADRA CASA</label>
                <select>
                    <option>Seleziona Squadra...</option>
                </select>
            </div>
            
            <div>
                <label>SQUADRA OSPITE</label>
                <select>
                    <option>Seleziona Squadra...</option>
                </select>
            </div>
            
            <button class="btn-action teko" style="font-size: 1.4rem;">GENERA ANALISI ELITE PRO</button>
        </div>

        <p style="text-align: center; font-size: 10px; color: #475569; margin-top: 20px;">
            Dati statistici in tempo reale elaborati da PROBET AI Engine
        </p>
    </div>
</body>
</html>
"""

# 4. Esecuzione (Forza l'altezza per coprire lo schermo)
components.html(html_code, height=900, scrolling=False)
