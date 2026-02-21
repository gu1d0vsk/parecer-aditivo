<style>
    /* 1. FUNDO GERAL */
    [data-testid="stApp"] { 
        background-image: linear-gradient(rgb(2, 45, 44) 0%, rgb(0, 15, 15) 100%); 
        background-attachment: fixed; 
    }
    
    /* 2. SIDEBAR - Transparente e sem borda */
    [data-testid="stSidebar"] { 
        background-color: rgba(2, 45, 44, 0.7) !important; 
        backdrop-filter: blur(10px);
        border: none !important; 
    }

    /* 3. LARGURA DA PÁGINA (A MÁGICA ACONTECE AQUI) */
    /* Força o limite de 75% da tela e CENTRALIZA o conteúdo */
    [data-testid="block-container"] {
        max-width: 75% !important; 
        margin: 0 auto !important; /* Isso é o que centraliza a tela! */
        padding-top: 2rem !important;
    }
    
    /* LIMPEZA GERAL */
    .stDeployButton {display:none;} 
    #MainMenu {visibility: hidden;} 
    [data-testid="stHeader"] { background-color: transparent; }
    
    /* MATAR TODAS AS LINHAS DIVISÓRIAS (<hr>) DO STREAMLIT */
    hr {
        border: none !important;
        background-color: transparent !important;
        height: 0px !important;
        margin: 0px !important;
    }
    
    /* 4. AUMENTO GERAL DE TEXTOS (Zoom 120%) */
    /* Removi a restrição do H1 para o título voltar a ficar gigante */
    .stMarkdown, .stText, p, label, span, div[data-testid="stCaptionContainer"], li { 
        color: #e8e8e8 !important; 
        font-size: 1.15rem !important; 
    }
    h2 { font-size: 2.2rem !important; }
    h3 { font-size: 1.8rem !important; }
    
    /* 5. CORREÇÃO DOS INPUTS E TEXTAREAS */
    div[data-baseweb="base-input"], 
    div[data-baseweb="input"], 
    div[data-baseweb="textarea"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    input, textarea {
        background-color: rgba(0, 0, 0, 0.3) !important;
        color: #ffffff !important;
        border-radius: 1.5rem !important;
        border: none !important;
        padding: 0.8rem 1.5rem !important;
        font-size: 1.15rem !important;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.2) !important;
        outline: none !important;
        width: 100% !important;
    }
    
    textarea {
        border-radius: 1rem !important; 
        padding-top: 1rem !important;
    }

    input:focus, textarea:focus {
        background-color: rgba(0, 0, 0, 0.5) !important;
    }

    div[data-baseweb="select"] > div { 
        background-color: rgba(0, 0, 0, 0.3) !important; 
        border-radius: 1.5rem !important; 
        border: none !important;
        padding: 0.2rem 1rem !important;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.2) !important;
    }
    div[data-baseweb="select"] div { color: #e0e0e0 !important; font-size: 1.15rem !important; }

    /* 6. ESTILIZAÇÃO DAS ABAS (TABS) */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        border-bottom: none !important; 
        gap: 0.5rem; 
    }
    div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
        display: none !important; 
    }
    div[data-testid="stTabs"] button {
        background-color: rgba(0, 0, 0, 0.3) !important;
        border: none !important; 
        border-radius: 2rem !important; 
        margin-right: 0.5rem;
        padding: 0.6rem 1.5rem !important;
        font-size: 1.15rem !important;
        transition: background-color 0.3s ease;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        background-color: rgb(0, 150, 151) !important;
        color: white !important;
        font-weight: bold;
    }

    /* 7. BOTÕES GERAIS */
    div[data-testid="stButton"] > button { 
        background-color: rgb(0, 80, 81) !important; 
        color: #FFFFFF !important; 
        border-radius: 2rem !important; 
        border: none !important; 
        font-weight: bold; 
        padding: 1rem 2rem !important; 
        font-size: 1.2rem !important;
        transition: all 0.2s ease-in-out;
    }
    div[data-testid="stButton"] > button:hover { 
        transform: translateY(-2px); 
        box-shadow: 0 6px 15px rgba(0, 150, 151, 0.5); 
    }
    
    div[data-testid="stDownloadButton"] > button { 
        background-image: linear-gradient(90deg, rgb(221, 79, 5) 0%, rgb(255, 110, 30) 100%) !important; 
        color: #FFFFFF !important; 
        border-radius: 2rem !important; 
        border: none !important; 
        font-weight: bold;
        padding: 1rem 2rem !important;
        font-size: 1.2rem !important;
        box-shadow: 0 4px 10px rgba(221, 79, 5, 0.3);
    }
    div[data-testid="stDownloadButton"] > button:hover {
        transform: translateY(-2px); 
        box-shadow: 0 6px 15px rgba(221, 79, 5, 0.5);
    }
</style>
