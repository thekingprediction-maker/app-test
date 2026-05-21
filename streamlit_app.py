import streamlit as st
import streamlit.components.v1 as components

# 1. Configurazione Pagina
st.set_page_config(
    page_title="PROBET AI V4 PRO", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. Pulizia Interfaccia Streamlit
st.markdown("""
<style>
    #MainMenu, header, footer {visibility: hidden;}
    .stApp {background-color: #020617 !important;}
    .block-container {padding: 0px !important; max-width: 100% !important;}
    ::-webkit-scrollbar {display: none;}
</style>
""", unsafe_allow_html=True)

# 3. Codice Applicazione (HTML/JS)
html_code = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600&family=Inter:wght@400;700&display=swap');
        body { 
            background: #020617; 
            color: white; 
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .teko { font-family: 'Teko', sans-serif; text-transform: uppercase; }
        .glass-card {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            padding: 24px;
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        .btn-action {
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            width: 100%;
            padding: 16px;
            border-radius: 14px;
            font-weight: 800;
            margin-top: 20px;
            cursor: pointer;
            border: none;
            color: white;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        }
        select {
            width:100%; 
            background:#0f172a; 
            color:white; 
            padding:12px; 
            border-radius:10px; 
            margin-bottom:16px; 
            border: 1px solid rgba(255,255,255,0.1);
            font-weight: 600;
        }
        label {
            font-size: 10px; 
            color: #94a3b8; 
            text-transform: uppercase; 
            letter-spacing: 0.05em;
            margin-bottom: 4px;
            display: block;
        }
    </style>
</head>
<body>
    <div style="max-width: 500px; margin: auto;">
        <h1 class="teko" style="font-size: 3.5rem; text-align: center; font-style: italic; margin-bottom: 0;">PROBET <span style="color:#3b82f6">AI</span></h1>
        <p style="text-align: center; color: #60a5fa; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.2em; margin-bottom: 30px;">V4 PRO • ELITE ENGINE</p>
        
        <div class="glass-card">
            <label>SQUADRA CASA</label>
            <select>
                <option>Seleziona Squadra...</option>
            </select>
            
            <label>SQUADRA OSPITE</label>
            <select>
                <option>Seleziona Squadra...</option>
            </select>
            
            <button class="btn-action teko" style="font-size: 1.25rem;">GENERA ANALISI ELITE PRO</button>
        </div>
    </div>
</body>
</html>
"""

# 4. Esecuzione
components.html(html_code, height=1000, scrolling=True)
