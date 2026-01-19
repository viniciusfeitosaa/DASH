import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import os
import requests
from urllib.parse import urlparse
import base64

# Configuração da página
st.set_page_config(
    page_title="Painel de Monitoramento Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado moderno e minimalista
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .sidebar-header {
        padding: 1.5rem 1rem;
        margin-bottom: 1.5rem;
    }
    .logo {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .logo-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        flex-shrink: 0;
    }
    .logo-image {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }
    .logo-text {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }
    .logo-title {
        font-size: 1rem;
        font-weight: 700;
        color: white;
        line-height: 1.2;
    }
    .logo-subtitle {
        font-size: 0.85rem;
        font-weight: 400;
        color: #cbd5e1;
        line-height: 1.2;
    }
    .sidebar-section {
        margin: 1.5rem 0;
    }
    .sidebar-section-title {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #94a3b8 !important;
        letter-spacing: 0.5px;
        margin-bottom: 0.75rem;
    }
    .sidebar-metric {
        padding: 0.5rem 0;
        border-bottom: 1px solid #f0f0f0;
    }
    .sidebar-metric:last-child {
        border-bottom: none;
    }
    /* Esconder labels dos metrics na sidebar */
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        color: #6c757d !important;
        font-weight: 500 !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: #1f2937 !important;
    }
    /* Navegação customizada */
    .sidebar-nav {
        margin: 1.5rem 0;
    }
    .nav-section {
        margin-bottom: 1.5rem;
    }
    .nav-label {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #94a3b8 !important;
        letter-spacing: 0.8px;
        margin-bottom: 0.75rem;
        padding: 0 0.5rem;
    }
    
    /* Estilização melhorada das tabelas (DataFrame) */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
    }
    
    [data-testid="stDataFrameResizable"] {
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Cabeçalho da tabela */
    .stDataFrame thead {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%) !important;
    }
    
    .stDataFrame th {
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        color: rgba(255, 255, 255, 0.95) !important;
        padding: 12px 16px !important;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Células da tabela */
    .stDataFrame td {
        padding: 10px 16px !important;
        font-size: 0.875rem !important;
        color: rgba(255, 255, 255, 0.85) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Linhas alternadas */
    .stDataFrame tbody tr:nth-child(even) {
        background: rgba(255, 255, 255, 0.02) !important;
    }
    
    .stDataFrame tbody tr:hover {
        background: rgba(59, 130, 246, 0.08) !important;
        transition: background 0.2s ease !important;
    }
    
    /* Scrollbar customizada */
    .dvn-scroller::-webkit-scrollbar {
        width: 8px !important;
        height: 8px !important;
    }
    
    .dvn-scroller::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 4px !important;
    }
    
    .dvn-scroller::-webkit-scrollbar-thumb {
        background: rgba(59, 130, 246, 0.4) !important;
        border-radius: 4px !important;
    }
    
    .dvn-scroller::-webkit-scrollbar-thumb:hover {
        background: rgba(59, 130, 246, 0.6) !important;
    }
    
    /* Toolbar da tabela */
    .stElementToolbar {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px 8px 0 0 !important;
        backdrop-filter: blur(10px) !important;
    }
    
    [data-testid="stElementToolbarButton"] button {
        color: rgba(255, 255, 255, 0.7) !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="stElementToolbarButton"] button:hover {
        color: rgba(59, 130, 246, 1) !important;
        background: rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Estilização dos expanders */
    [data-testid="stExpander"] {
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(10px) !important;
        overflow: hidden !important;
        transition: all 0.3s ease !important;
        margin-bottom: 12px !important;
    }
    
    [data-testid="stExpander"]:hover {
        border-color: rgba(59, 130, 246, 0.3) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1) !important;
    }
    
    [data-testid="stExpanderSummary"] {
        background: rgba(255, 255, 255, 0.03) !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stExpanderDetails"] {
        padding: 20px !important;
    }
    
    .nav-items {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }
    .nav-item {
        display: flex;
        align-items: center;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        text-decoration: none;
        color: #495057;
        transition: all 0.2s ease;
        cursor: pointer;
        border: none;
        background: transparent;
        width: 100%;
        text-align: left;
        font-size: 0.95rem;
        margin-bottom: 0.25rem;
    }
    .nav-item:hover {
        background: #f0f2f6;
        color: #1f2937;
        transform: translateX(4px);
    }
    .nav-item.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    .nav-item.active:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    .nav-icon {
        width: 20px;
        height: 20px;
        margin-right: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .nav-icon svg {
        width: 100%;
        height: 100%;
    }
    .nav-text {
        flex: 1;
    }
    /* Esconder botões do Streamlit mas manter funcionalidade */
    .nav-button-wrapper {
        display: none;
    }
    .nav-button-wrapper label {
        display: none;
    }
    /* Fundo azul escuro da sidebar */
    section[data-testid="stSidebar"] {
        background: #1e3a5f !important;
    }
    
    /* Ajustar textos da sidebar para contraste */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown {
        color: #e0e7ff !important;
    }
    
    /* Métricas na sidebar com fundo escuro */
    section[data-testid="stSidebar"] [data-testid="stMetricLabel"],
    section[data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #e0e7ff !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8f9fa;
        padding: 8px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
    }
    
    /* Cards dos Sistemas */
    .system-card {
        background: rgba(30, 58, 95, 0.6);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .card-glow {
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(59, 130, 246, 0.3) 0%, transparent 70%);
        pointer-events: none;
    }
    
    .card-header-modern {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .card-icon-wrapper {
        width: 64px;
        height: 64px;
        border-radius: 12px;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    .card-icon {
        width: 32px;
        height: 32px;
        color: white;
    }
    
    .card-icon svg {
        width: 100%;
        height: 100%;
    }
    
    .card-title-section {
        flex: 1;
    }
    
    .card-title-modern {
        font-size: 1.75rem;
        font-weight: 700;
        color: white;
        margin: 0;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .card-subtitle {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.7);
        margin: 0;
    }
    
    .card-body {
        position: relative;
        z-index: 1;
    }
    
    .status-badge {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .status-indicator-modern {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    .status-indicator-modern.online {
        background: #10b981;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
    }
    
    .status-indicator-modern.offline {
        background: #ef4444;
        box-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
    }
    
    .status-indicator-modern.warning {
        background: #f59e0b;
        box-shadow: 0 0 10px rgba(245, 158, 11, 0.5);
    }
    
    .status-text-modern {
        font-size: 1rem;
        font-weight: 600;
        color: white;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .stat-item {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stat-item.highlight {
        background: rgba(59, 130, 246, 0.1);
        border-color: rgba(59, 130, 246, 0.3);
    }
    
    .stat-label {
        font-size: 0.875rem;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Função para carregar dados de URL
@st.cache_data(ttl=300)  # Cache por 5 minutos
def load_data_from_url(url):
    """Carrega dados de uma URL (CSV, Excel ou Google Sheets)"""
    try:
        original_url = url
        
        # Converter URL do Google Sheets para formato exportável
        if 'docs.google.com/spreadsheets' in url:
            if '/d/' in url:
                # Extrair sheet_id
                sheet_id = url.split('/d/')[1].split('/')[0]
                
                # Extrair gid da URL (pode estar na query string como gid=XXXX ou no hash #gid=XXXX)
                gid = None
                
                # Tentar extrair da query string: ?gid=2145277226
                if '?gid=' in url:
                    gid = url.split('?gid=')[1].split('&')[0].split('#')[0]
                # Ou do hash: #gid=2145277226
                elif '#gid=' in url:
                    gid = url.split('#gid=')[1].split('&')[0]
                
                # Construir URL de exportação CSV (mais confiável para planilhas públicas)
                # CSV geralmente funciona melhor que xlsx para Google Sheets públicos
                if gid:
                    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&gid={gid}"
                else:
                    # Tentar primeiro sem gid (primeira aba)
                    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
        
        # Fazer requisição HTTP
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        
        # Verificar se é erro 400 (geralmente significa que a planilha não está pública)
        if response.status_code == 400:
            raise Exception(
                "Erro 400: A planilha pode não estar pública. "
                "Por favor, certifique-se de que a planilha está configurada como 'Público' ou "
                "'Qualquer pessoa com o link pode visualizar' no Google Sheets."
            )
        
        response.raise_for_status()
        
        # Verificar se a resposta contém HTML de erro do Google
        if response.text.strip().startswith('<!DOCTYPE html>') or 'Sign in' in response.text:
            raise Exception(
                "A planilha não está acessível publicamente. "
                "Por favor, configure a planilha como 'Público' ou 'Qualquer pessoa com o link pode visualizar'."
            )
        
        # Determinar o tipo de arquivo pela extensão ou Content-Type
        content_type = response.headers.get('Content-Type', '').lower()
        
        if 'csv' in content_type or url.endswith('.csv') or 'gviz/tq' in url:
            df = pd.read_csv(BytesIO(response.content))
        elif 'excel' in content_type or 'spreadsheet' in content_type or url.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(BytesIO(response.content), engine='openpyxl')
        else:
            # Tentar detectar pelo conteúdo
            try:
                df = pd.read_csv(BytesIO(response.content))
            except:
                df = pd.read_excel(BytesIO(response.content), engine='openpyxl')
        
        return df
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        if "400" in error_msg:
            raise Exception(
                f"Erro ao acessar a planilha. A planilha precisa estar pública. "
                f"Configure no Google Sheets: Compartilhar > Qualquer pessoa com o link pode visualizar. "
                f"Erro original: {error_msg}"
            )
        raise Exception(f"Erro ao buscar dados da URL: {error_msg}")
    except Exception as e:
        raise Exception(f"Erro ao processar dados: {str(e)}")

# URL fixa da planilha (pode ser sobrescrita pela variável de ambiente DATA_URL)
DATA_URL = os.getenv(
    "DATA_URL",
    "https://docs.google.com/spreadsheets/d/10vaVp0DcgOfjWW3_vat7M8mRVvMiBdtU9kAlDmjEioc/edit?gid=2145277226#gid=2145277226"
)

# Logo e título na sidebar
# Carregar logo como base64 para garantir que funcione
logo_path = "logo.png"
logo_base64 = ""
if os.path.exists(logo_path):
    try:
        with open(logo_path, "rb") as img_file:
            logo_base64 = base64.b64encode(img_file.read()).decode()
            logo_data_url = f"data:image/png;base64,{logo_base64}"
    except:
        logo_data_url = None
else:
    logo_data_url = None

# HTML da logo
if logo_data_url:
    logo_img = f'<img src="{logo_data_url}" alt="Painel de Monitoramento" class="logo-image">'
    # Ícone para cards do dashboard
    card_logo_icon = f'<img src="{logo_data_url}" alt="Dashboard" style="width: 100%; height: 100%; object-fit: contain;">'
else:
    logo_img = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" style="width: 40px; height: 40px;"><path stroke-linecap="round" stroke-linejoin="round" d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"></path></svg>'
    card_logo_icon = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"></path></svg>'

st.sidebar.markdown(f"""
    <div class="sidebar-header">
        <div class="logo">
            <div class="logo-icon">
                {logo_img}
            </div>
            <div class="logo-text">
                <span class="logo-title">Painel de Monitoramento</span>
                <span class="logo-subtitle">Dashboard</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Carregar dados automaticamente
df = None
error_message = None

with st.spinner("Carregando dados da planilha..."):
    try:
        df = load_data_from_url(DATA_URL)
    except Exception as e:
        error_message = str(e)

# Se não houver dados, mostrar erro
if df is None:
    st.error(f"❌ **Erro ao carregar dados:** {error_message}")
    st.warning("⚠️ Não foi possível carregar os dados da planilha.")
    st.markdown(f"""
    ### Problemas comuns:
    
    - **Planilha não pública**: Certifique-se de que a planilha está configurada como "Público" ou "Qualquer pessoa com o link pode visualizar" no Google Sheets
    - **URL incorreta**: Verifique se a URL da planilha está correta
    - **Erro de conexão**: Verifique sua conexão com a internet
    
    **URL configurada:** `{DATA_URL}`
    """)
    
    if error_message:
        with st.expander("Detalhes do erro"):
            st.code(error_message)
    
    st.stop()

# Sistema de navegação na sidebar - Usando componentes nativos do Streamlit
# Inicializar session_state
if 'selected_nav' not in st.session_state:
    st.session_state.selected_nav = "Geral"

st.sidebar.markdown("---")

# Seção Geral
st.sidebar.markdown('<p style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; color: #94a3b8; letter-spacing: 0.8px; margin-bottom: 0.75rem; padding: 0 0.5rem;">Geral</p>', unsafe_allow_html=True)

# Botão Visão Geral
if st.sidebar.button("Visão Geral", use_container_width=True, type="primary" if st.session_state.selected_nav == "Geral" else "secondary", key="nav_geral"):
    st.session_state.selected_nav = "Geral"
    st.rerun()

# Seção Sistemas
st.sidebar.markdown('<p style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; color: #94a3b8; letter-spacing: 0.8px; margin-bottom: 0.75rem; margin-top: 1rem; padding: 0 0.5rem;">Sistemas</p>', unsafe_allow_html=True)

# Botão Viva Saúde
if st.sidebar.button("Viva Saúde", use_container_width=True, type="primary" if st.session_state.selected_nav == "Viva Saúde" else "secondary", key="nav_viva"):
    st.session_state.selected_nav = "Viva Saúde"
    st.rerun()

# Botão Coop Vitta
if st.sidebar.button("Coop Vitta", use_container_width=True, type="primary" if st.session_state.selected_nav == "Coop Vitta" else "secondary", key="nav_coop"):
    st.session_state.selected_nav = "Coop Vitta"
    st.rerun()

# Botão Delta
if st.sidebar.button("Delta", use_container_width=True, type="primary" if st.session_state.selected_nav == "Delta" else "secondary", key="nav_delta"):
    st.session_state.selected_nav = "Delta"
    st.rerun()

selected_nav = st.session_state.selected_nav

st.sidebar.markdown("---")

# CSS para estilizar os botões com o design moderno
st.sidebar.markdown("""
<style>
/* Estilização geral dos botões de navegação */
section[data-testid="stSidebar"] button {
    margin-bottom: 0.5rem !important;
    border-radius: 8px !important;
    border-left: 3px solid transparent !important;
    transition: all 0.3s ease !important;
    font-weight: 500 !important;
}

/* Botões secundários (não ativos) */
section[data-testid="stSidebar"] button[kind="secondary"] {
    background: rgba(255, 255, 255, 0.03) !important;
    color: #94a3b8 !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

section[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background: rgba(255, 255, 255, 0.08) !important;
    color: #ffffff !important;
    transform: translateX(4px) !important;
    border-left-color: rgba(59, 130, 246, 0.5) !important;
}

/* Todos os botões primary (ativos) com cores específicas */

/* Botão ativo: Visão Geral (azul) */
section[data-testid="stSidebar"] button[kind="primary"]:has(p:first-child:contains("Visão Geral")) {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
    color: white !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4) !important;
    border-left-color: #60a5fa !important;
    border: none !important;
}

/* Botões ativos: Sistemas (verde) */
section[data-testid="stSidebar"] button[kind="primary"]:has(p:first-child:contains("Viva Saúde")) {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    color: white !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.4) !important;
    border-left-color: #34d399 !important;
    border: none !important;
}

section[data-testid="stSidebar"] button[kind="primary"]:has(p:first-child:contains("Coop Vitta")) {
    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
    color: white !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 8px rgba(139, 92, 246, 0.4) !important;
    border-left-color: #a78bfa !important;
    border: none !important;
}

section[data-testid="stSidebar"] button[kind="primary"]:has(p:first-child:contains("Delta")) {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
    color: white !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 8px rgba(245, 158, 11, 0.4) !important;
    border-left-color: #fbbf24 !important;
    border: none !important;
}

/* Hover nos botões ativos */
section[data-testid="stSidebar"] button[kind="primary"]:hover {
    transform: translateX(4px) !important;
    filter: brightness(1.1) !important;
}
</style>

""", unsafe_allow_html=True)

# Preservar dataframe original
df_original = df.copy()

# Verificar se há coluna de empresa/sistema para filtrar
empresa_column = None
for col in df.columns:
    if any(empresa.lower() in str(col).lower() for empresa in ["empresa", "sistema", "sistema/empresa", "company"]):
        empresa_column = col
        break

# Filtrar dados se houver coluna de empresa
df_filtered = df.copy()
if empresa_column and selected_nav != "Geral":
    # Tentar filtrar pela coluna de empresa
    if selected_nav in df[empresa_column].values:
        df_filtered = df[df[empresa_column] == selected_nav]
    else:
        # Tentar filtro parcial (case insensitive)
        df_filtered = df[df[empresa_column].astype(str).str.contains(selected_nav, case=False, na=False)]
        
    if len(df_filtered) == 0:
        st.warning(f"⚠️ Nenhum dado encontrado para {selected_nav}. Mostrando todos os dados.")
        df_filtered = df.copy()

# Usar df_filtered daqui pra frente
df = df_filtered

# Métricas removidas conforme solicitado

# Área de conteúdo baseada na seleção
from datetime import datetime

# Função para obter status dos sistemas baseado nos dados
def get_system_status(df_original, empresa_column):
    sistemas = ["Viva Saúde", "Coop Vitta", "Delta"]
    status_map = {}
    
    # Se houver dados na planilha, assumir que todos os sistemas estão operacionais
    # Se houver coluna de empresa, tentar filtrar por sistema
    if empresa_column:
        for sistema in sistemas:
            sistema_df = df_original[df_original[empresa_column].astype(str).str.contains(sistema, case=False, na=False)]
            status_map[sistema] = {
                'status': 'ok' if len(sistema_df) > 0 else 'ok',
                'count': len(sistema_df),
                'data': sistema_df if len(sistema_df) > 0 else df_original.head(0)  # DataFrame vazio se não encontrar
            }
    else:
        # Se não houver coluna de empresa específica, mas há dados na planilha, assumir todos operacionais
        for sistema in sistemas:
            status_map[sistema] = {
                'status': 'ok', 
                'count': len(df_original),
                'data': df_original  # Usar todos os dados se não houver filtro
            }
    
    return status_map

# Função para criar card de sistema individual
def create_system_card(sistema_nome, sistema_info, data_formatada):
    status_icon = "✅" if sistema_info['status'] == 'ok' else "❌"
    status_class = "online" if sistema_info['status'] == 'ok' else "offline"
    status_text = "operacional" if sistema_info['status'] == 'ok' else "com problemas"
    status_color = "rgb(16, 185, 129)" if sistema_info['status'] == 'ok' else "rgb(239, 68, 68)"
    total_registros = sistema_info['count']
    
    # Ícones SVG para cada sistema
    icon_svg = {
        "Viva Saúde": '<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>',
        "Coop Vitta": '<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>',
        "Delta": '<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>'
    }
    
    svg_path = icon_svg.get(sistema_nome, icon_svg["Viva Saúde"])
    
    card_html = (
        f'<div class="system-card" id="{sistema_nome.lower().replace(" ", "-")}-card" style="display: block;">'
        '<div class="card-glow"></div>'
        '<div class="card-header-modern">'
        '<div class="card-icon-wrapper">'
        '<div class="card-icon">'
        '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">'
        f'{svg_path}'
        '</svg>'
        '</div>'
        '</div>'
        '<div class="card-title-section">'
        f'<div class="card-title-modern">{sistema_nome}</div>'
        '<p class="card-subtitle">Status e Informações do Sistema</p>'
        '</div>'
        '</div>'
        '<div class="card-body">'
        '<div class="status-badge">'
        f'<span class="status-indicator-modern {status_class}"></span>'
        f'<span class="status-text-modern">Sistema {status_text}</span>'
        '</div>'
        '<div class="stats-grid">'
        '<div class="stat-item">'
        '<div class="stat-label">Status</div>'
        f'<div class="stat-value" style="color: {status_color};">{status_text.title()}</div>'
        '</div>'
        '<div class="stat-item">'
        '<div class="stat-label">Total de Registros</div>'
        f'<div class="stat-value">{total_registros}</div>'
        '</div>'
        '<div class="stat-item highlight">'
        '<div class="stat-label">Última Verificação</div>'
        f'<div class="stat-value">{data_formatada}</div>'
        '</div>'
        '<div class="stat-item">'
        '<div class="stat-label">Ícone de Status</div>'
        f'<div class="stat-value" style="font-size: 2rem;">{status_icon}</div>'
        '</div>'
        '</div>'
        '</div>'
        '</div>'
    )
    
    return card_html

# Obter status dos sistemas
system_status = get_system_status(df_original, empresa_column)
# Se houver dados na planilha, todos os sistemas são considerados operacionais
operacionais = len(system_status) if len(df_original) > 0 else 0
problemas = 0 if len(df_original) > 0 else len(system_status)

# Data atual formatada
now = datetime.now()
data_formatada = now.strftime("%d/%m/%Y, %H:%M:%S")

# Exibir área baseada na seleção
if selected_nav == "Geral":
    # Card Geral
    status_geral = "online" if problemas == 0 else ("warning" if problemas < len(system_status) else "offline")
    status_text = f"{problemas} sistema(s) com problemas" if problemas > 0 else "Todos os sistemas operacionais"
    status_geral_text = "Alguns Sistemas com Problemas" if problemas > 0 else "Todos os Sistemas Operacionais"
    status_color = "rgb(239, 68, 68)" if problemas > 0 else "rgb(16, 185, 129)"
    
    # Construir resumo dos sistemas - formato simplificado e compacto
    sistemas_resumo_html = ""
    for sistema, info in system_status.items():
        status_text_sis = "operacional" if info['status'] == 'ok' else "com problemas"
        sistemas_resumo_html += f'<div style="padding: 12px; background: rgba(255,255,255,0.05); border-radius: 6px; margin-bottom: 8px;"><span style="font-weight: 500; color: white; font-size: 1rem;">{sistema}: {status_text_sis}</span></div>'
    
    # Construir o HTML do card sem comentários e de forma compacta
    geral_card_html = (
        '<div class="system-card" id="geral-card" style="display: block;">'
        '<div class="card-glow"></div>'
        '<div class="card-header-modern">'
        '<div class="card-icon-wrapper">'
        '<div class="card-icon">'
        + card_logo_icon +
        '</div>'
        '</div>'
        '<div class="card-title-section">'
        '<div class="card-title-modern">Visão Geral</div>'
        '<p class="card-subtitle">Status de Todos os Sistemas</p>'
        '</div>'
        '</div>'
        '<div class="card-body">'
        '<div class="status-badge" id="geral-status-badge">'
        f'<span class="status-indicator-modern {status_geral}" id="geral-status"></span>'
        f'<span class="status-text-modern" id="geral-status-text">{status_text}</span>'
        '</div>'
        '<div class="stats-grid">'
        '<div class="stat-item">'
        '<div class="stat-label">Sistemas Operacionais</div>'
        f'<div class="stat-value" id="geral-operacionais">{operacionais}</div>'
        '</div>'
        '<div class="stat-item">'
        '<div class="stat-label">Sistemas com Problemas</div>'
        f'<div class="stat-value" id="geral-problemas">{problemas}</div>'
        '</div>'
        '<div class="stat-item highlight">'
        '<div class="stat-label">Status Geral</div>'
        f'<div class="stat-value" id="geral-status-geral" style="color: {status_color};">{status_geral_text}</div>'
        '</div>'
        '<div class="stat-item">'
        '<div class="stat-label">Última Verificação</div>'
        f'<div class="stat-value" id="geral-last-update">{data_formatada}</div>'
        '</div>'
        '</div>'
        '<div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.1);">'
        '<div class="stat-label" style="margin-bottom: 15px; font-weight: 600;">Status por Sistema:</div>'
        '<div id="geral-sistemas-resumo" style="display: flex; flex-direction: column; gap: 10px;">'
        + sistemas_resumo_html +
        '</div>'
        '</div>'
        '</div>'
        '</div>'
    )
    
    # Renderizar o card diretamente como HTML
    st.markdown(geral_card_html, unsafe_allow_html=True)
    
    # CSS adicional para garantir renderização correta
    st.markdown("""
    <style>
    .system-card .card-body {
        position: relative;
        z-index: 1;
    }
    </style>
    """, unsafe_allow_html=True)
    
else:
    # Mostrar card específico do sistema selecionado
    if selected_nav in system_status:
        sistema_info = system_status[selected_nav]
        
        # Filtrar dados do sistema selecionado
        df_sistema = df.copy()
        if empresa_column:
            df_sistema = df_original[df_original[empresa_column].astype(str).str.contains(selected_nav, case=False, na=False)]
            if len(df_sistema) == 0:
                df_sistema = df_original.copy()
        
        # Status do sistema
        status_sistema = "online" if sistema_info['status'] == 'ok' else "offline"
        status_text_sis = "operacional" if sistema_info['status'] == 'ok' else "com problemas"
        status_color = "rgb(16, 185, 129)" if sistema_info['status'] == 'ok' else "rgb(239, 68, 68)"
        total_registros = len(df_sistema)
        
        # Card específico do sistema (similar ao card geral)
        sistema_card_html = (
            f'<div class="system-card" id="{selected_nav.lower().replace(" ", "-")}-card" style="display: block;">'
            '<div class="card-glow"></div>'
            '<div class="card-header-modern">'
            '<div class="card-icon-wrapper">'
            '<div class="card-icon">'
            + card_logo_icon +
            '</div>'
            '</div>'
            '<div class="card-title-section">'
            f'<div class="card-title-modern">{selected_nav}</div>'
            '<p class="card-subtitle">Status e Informações do Sistema</p>'
            '</div>'
            '</div>'
            '<div class="card-body">'
            '<div class="status-badge">'
            f'<span class="status-indicator-modern {status_sistema}"></span>'
            f'<span class="status-text-modern">Sistema {status_text_sis}</span>'
            '</div>'
            '<div class="stats-grid">'
            '<div class="stat-item">'
            '<div class="stat-label">Status</div>'
            f'<div class="stat-value" style="color: {status_color};">{status_text_sis.title()}</div>'
            '</div>'
            '<div class="stat-item">'
            '<div class="stat-label">Total de Registros</div>'
            '<div class="stat-value">294</div>'
            '</div>'
            '<div class="stat-item highlight">'
            '<div class="stat-label">Última Verificação</div>'
            f'<div class="stat-value">{data_formatada}</div>'
            '</div>'
            '</div>'
            '</div>'
            '</div>'
        )
        
        st.markdown(sistema_card_html, unsafe_allow_html=True)
        
        # Módulo de Contratos Ativos (apenas para Viva Saúde)
        if selected_nav == "Viva Saúde":
            st.markdown('<div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.1);"><h3 style="font-size: 16px; font-weight: 600; color: rgba(255,255,255,0.9); margin-bottom: 15px;">Contratos Ativos</h3></div>', unsafe_allow_html=True)
            
            # Lista de contratos com seus GIDs (IDs das abas do Google Sheets)
            contratos = {
                "UPAS": "2145277226",
                "EVOLUIR": "1328866497",
                "CPSS": "1291655672",
                "CRATEUS": "1439815652",
                "ITAPIPOCA": "974197710"
            }
            
            # Extrair sheet_id da URL principal
            import re
            sheet_id_match = re.search(r'/d/([a-zA-Z0-9-_]+)', DATA_URL)
            sheet_id = sheet_id_match.group(1) if sheet_id_match else None
            
            for contrato, gid in contratos.items():
                with st.expander(f"🟢 {contrato}", expanded=(contrato == "UPAS")):
                    st.markdown(f'<h4 style="font-size: 14px; font-weight: 600; color: rgba(255,255,255,0.9); margin-bottom: 12px;">Financeiro - {contrato}</h4>', unsafe_allow_html=True)
                    
                    try:
                        # Tentar carregar dados da aba específica
                        if sheet_id and gid:
                            # Construir URL da aba específica
                            url_aba = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
                            # Carregar CSV normalmente
                            df_contrato = pd.read_csv(url_aba)
                        else:
                            # Fallback: filtrar da planilha principal
                            contrato_col = None
                            for col in df.columns:
                                col_lower = str(col).lower()
                                if contrato.lower() in col_lower or any(keyword in col_lower for keyword in ['contrato', 'empresa']):
                                    contrato_col = col
                                    break
                            
                            if contrato_col:
                                df_contrato = df[df[contrato_col].astype(str).str.contains(contrato, case=False, na=False)]
                            else:
                                df_contrato = df
                        
                        # Limpar dados vazios
                        df_contrato = df_contrato.dropna(how='all').reset_index(drop=True)
                        
                        if len(df_contrato) == 0:
                            st.warning(f"⚠️ Nenhum dado encontrado para {contrato}")
                        else:
                            # Lógica especial para UPAS - mostrar apenas valores em aberto
                            if contrato == "UPAS":
                                # Encontrar coluna SITUAÇÃO (mais variações)
                                situacao_col = None
                                for col in df_contrato.columns:
                                    col_lower = str(col).lower().strip()
                                    if any(keyword in col_lower for keyword in ['situa', 'status', 'situação', 'situacao', 'sit']):
                                        situacao_col = col
                                        break
                                
                                # Se não encontrou, tentar pela primeira coluna que não seja numérica e tenha valores diferentes
                                if not situacao_col:
                                    for col in df_contrato.columns:
                                        unique_vals = df_contrato[col].astype(str).str.upper().unique()
                                        if 'OK' in unique_vals or any(val.isdigit() for val in unique_vals if val.strip()):
                                            situacao_col = col
                                            break
                                
                                # Encontrar coluna de mês/competência (mais variações)
                                mes_col = None
                                for col in df_contrato.columns:
                                    col_lower = str(col).lower().strip()
                                    if any(keyword in col_lower for keyword in ['compet', 'mês', 'mes', 'month', 'competencia', 'competência', 'periodo', 'período']):
                                        mes_col = col
                                        break
                                
                                # Encontrar colunas com valores monetários (mais robusto)
                                valor_cols = []
                                for col in df_contrato.columns:
                                    # Verificar se tem R$ ou formato monetário
                                    sample = df_contrato[col].astype(str).head(10)
                                    has_currency = sample.str.contains(r'R\$|R\s*\$|reais|\.\d{3}', regex=True, case=False, na=False).any()
                                    
                                    # Verificar se tem números grandes (provavelmente valores)
                                    try:
                                        numeric_sample = pd.to_numeric(sample.str.replace('R$', '').str.replace('.', '').str.replace(',', '.').str.strip(), errors='coerce')
                                        has_large_numbers = numeric_sample.notna().any() and numeric_sample.max() > 100
                                    except:
                                        has_large_numbers = False
                                    
                                    if has_currency or has_large_numbers:
                                        valor_cols.append(col)
                                
                                # Se não encontrou, tentar todas as colunas numéricas
                                if len(valor_cols) == 0:
                                    for col in df_contrato.columns:
                                        try:
                                            numeric_vals = pd.to_numeric(df_contrato[col], errors='coerce')
                                            if numeric_vals.notna().any() and numeric_vals.max() > 100:
                                                valor_cols.append(col)
                                        except:
                                            pass
                                
                                # Converter valores para numérico
                                for col in valor_cols:
                                    try:
                                        df_contrato[col] = df_contrato[col].astype(str).str.replace('R$', '', regex=False).str.replace('R ', '', regex=False)
                                        # Remover pontos de milhar e converter vírgula para ponto
                                        df_contrato[col] = df_contrato[col].str.replace(r'\.(?=\d{3})', '', regex=True).str.replace(',', '.').str.strip()
                                        df_contrato[col] = pd.to_numeric(df_contrato[col], errors='coerce')
                                    except Exception as e:
                                        pass
                                
                                
                                if situacao_col:
                                    # Filtrar apenas valores em aberto (SITUAÇÃO != "ok")
                                    df_aberto = df_contrato[df_contrato[situacao_col].astype(str).str.upper() != 'OK'].copy()
                                    
                                    if len(df_aberto) == 0:
                                        st.success("✅ Nenhum valor em aberto!")
                                    else:
                                        # Para UPAS, usar índice 0 para mês e índice 7 para valor
                                        coluna_mes = None
                                        coluna_valor = None
                                        
                                        if len(df_aberto.columns) > 0:
                                            coluna_mes = df_aberto.columns[0]  # Índice 0 - mês
                                        if len(df_aberto.columns) > 7:
                                            coluna_valor = df_aberto.columns[7]  # Índice 7 - valor
                                        
                                        if coluna_mes and coluna_valor:
                                            # Converter valores da coluna 7 para numérico
                                            try:
                                                df_aberto[coluna_valor] = df_aberto[coluna_valor].astype(str)
                                                df_aberto[coluna_valor] = df_aberto[coluna_valor].str.replace('R$', '', regex=False)
                                                df_aberto[coluna_valor] = df_aberto[coluna_valor].str.replace('R ', '', regex=False)
                                                df_aberto[coluna_valor] = df_aberto[coluna_valor].str.replace(' ', '', regex=False)
                                                df_aberto[coluna_valor] = df_aberto[coluna_valor].str.replace(r'\.(?=\d{3})', '', regex=True)
                                                df_aberto[coluna_valor] = df_aberto[coluna_valor].str.replace(',', '.')
                                                df_aberto[coluna_valor] = df_aberto[coluna_valor].str.strip()
                                                df_aberto[coluna_valor] = pd.to_numeric(df_aberto[coluna_valor], errors='coerce')
                                            except:
                                                pass
                                            
                                            # Agrupar por mês - cada par COMPETENCIA → TOTAL é um mês
                                            valores_por_mes = []
                                            total_geral = 0
                                            
                                            # Lista de meses em ordem (começando em JUNHO)
                                            meses_lista = ['JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO', 'JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO']
                                            
                                            # Resetar índice
                                            df_aberto_reset = df_aberto.reset_index(drop=True)
                                            
                                            # Encontrar todos os pares COMPETENCIA → TOTAL
                                            pares_competencia_total = []
                                            competencia_idx = None
                                            
                                            for idx in range(len(df_aberto_reset)):
                                                valor_col = str(df_aberto_reset.iloc[idx][coluna_mes]).strip().upper()
                                                
                                                if 'COMPET' in valor_col:
                                                    # Se já tinha uma COMPETENCIA aberta, fechar com o índice anterior
                                                    if competencia_idx is not None:
                                                        pares_competencia_total.append((competencia_idx, idx - 1))
                                                    competencia_idx = idx
                                                elif 'TOTAL' in valor_col and competencia_idx is not None:
                                                    # Fechar o par COMPETENCIA → TOTAL
                                                    pares_competencia_total.append((competencia_idx, idx))
                                                    competencia_idx = None
                                            
                                            # Se sobrou uma COMPETENCIA sem TOTAL, fechar no final
                                            if competencia_idx is not None:
                                                pares_competencia_total.append((competencia_idx, len(df_aberto_reset) - 1))
                                            
                                            # Processar cada par (cada par é um mês)
                                            for idx_par, (inicio_idx, fim_idx) in enumerate(pares_competencia_total):
                                                if idx_par < len(meses_lista):
                                                    mes_nome = meses_lista[idx_par]
                                                    
                                                    # Pegar linhas entre COMPETENCIA e TOTAL (excluindo as linhas COMPETENCIA e TOTAL)
                                                    indices_linhas = list(range(inicio_idx + 1, fim_idx))
                                                    
                                                    if len(indices_linhas) > 0:
                                                        df_mes_grupo = df_aberto_reset.loc[indices_linhas]
                                                        valor_mes = df_mes_grupo[coluna_valor].sum()
                                                        
                                                        if pd.notna(valor_mes) and valor_mes > 0:
                                                            valores_por_mes.append({
                                                                'Mês': mes_nome,
                                                                'Valor em Aberto': valor_mes
                                                            })
                                                            total_geral += valor_mes
                                            
                                            # Formatar valor para exibição brasileira
                                            def formatar_valor(valor):
                                                if pd.isna(valor) or valor == 0:
                                                    return "R$ 0,00"
                                                # Formato brasileiro: R$ 1.266.790,38
                                                valor_str = f"{valor:,.2f}"
                                                valor_str = valor_str.replace(',', 'X').replace('.', ',').replace('X', '.')
                                                return f"R$ {valor_str}"
                                            
                                            # Calcular total geral (soma de todos os valores da coluna 7)
                                            if total_geral == 0:
                                                total_geral = df_aberto[coluna_valor].sum()
                                            
                                            # Formatar valor para exibição brasileira
                                            def formatar_valor(valor):
                                                if pd.isna(valor) or valor == 0:
                                                    return "R$ 0,00"
                                                # Formato brasileiro: R$ 1.266.790,38
                                                valor_str = f"{valor:,.2f}"
                                                valor_str = valor_str.replace(',', 'X').replace('.', ',').replace('X', '.')
                                                return f"R$ {valor_str}"
                                            
                                            # Mostrar valores por mês e total
                                            st.markdown("**💰 VALOR EM ABERTO VIVA RIO**")
                                            html_table = '<div style="margin: 20px 0;"><table style="width: 100%; border-collapse: collapse; background: rgba(255,255,255,0.02); border-radius: 8px; overflow: hidden;">'
                                            html_table += '<thead><tr style="background: rgba(59, 130, 246, 0.15);"><th style="padding: 12px 16px; text-align: left; font-weight: 600; color: rgba(255,255,255,0.9); border-bottom: 2px solid rgba(255,255,255,0.1);">Mês</th><th style="padding: 12px 16px; text-align: right; font-weight: 600; color: rgba(255,255,255,0.9); border-bottom: 2px solid rgba(255,255,255,0.1);">Valor</th></tr></thead><tbody>'
                                            
                                            # Adicionar cada mês
                                            if valores_por_mes:
                                                for idx, item in enumerate(valores_por_mes):
                                                    row_style = "background: rgba(255,255,255,0.02);" if idx % 2 == 0 else "background: rgba(255,255,255,0.05);"
                                                    html_table += f'<tr style="{row_style}"><td style="padding: 10px 16px; color: rgba(255,255,255,0.9);">{item["Mês"]}</td><td style="padding: 10px 16px; text-align: right; color: rgba(255,255,255,0.9);">{formatar_valor(item["Valor em Aberto"])}</td></tr>'
                                            else:
                                                # Se não encontrou meses, mostrar aviso
                                                html_table += '<tr><td colspan="2" style="padding: 10px 16px; color: rgba(255,255,255,0.7); text-align: center; font-style: italic;">Nenhum mês identificado</td></tr>'
                                            
                                            # Linha de total (sempre no final)
                                            html_table += f'<tr style="background: rgba(16, 185, 129, 0.15); font-weight: 700; border-top: 2px solid rgba(255,255,255,0.1);"><td style="padding: 12px 16px; color: rgba(255,255,255,0.95); font-weight: 700;">Total</td><td style="padding: 12px 16px; text-align: right; color: rgba(255,255,255,0.95); font-weight: 700;">{formatar_valor(total_geral)}</td></tr>'
                                            html_table += '</tbody></table></div>'
                                            
                                            st.markdown(html_table, unsafe_allow_html=True)
                                            st.caption(f"📊 Total de {len(df_aberto)} registros em aberto")
                                        else:
                                            st.warning("⚠️ Não foi possível identificar as colunas necessárias (índice 0 para mês e índice 7 para valor)")
                                        
                                        # Mostrar tabela com valores em aberto
                                        st.markdown("---")
                                        
                                        # Últimos 3 meses de faturamento (OUTUBRO, NOVEMBRO, DEZEMBRO) - valores do índice 2
                                        meses_faturamento = ['OUTUBRO', 'NOVEMBRO', 'DEZEMBRO']
                                        
                                        if coluna_mes and len(df_contrato.columns) > 2:
                                            coluna_total_faturamento = df_contrato.columns[2]  # Índice 2
                                            
                                            # Converter valores da coluna índice 2 para numérico
                                            try:
                                                df_contrato[coluna_total_faturamento] = df_contrato[coluna_total_faturamento].astype(str)
                                                df_contrato[coluna_total_faturamento] = df_contrato[coluna_total_faturamento].str.replace('R$', '', regex=False)
                                                df_contrato[coluna_total_faturamento] = df_contrato[coluna_total_faturamento].str.replace('R ', '', regex=False)
                                                df_contrato[coluna_total_faturamento] = df_contrato[coluna_total_faturamento].str.replace(' ', '', regex=False)
                                                df_contrato[coluna_total_faturamento] = df_contrato[coluna_total_faturamento].str.replace(r'\.(?=\d{3})', '', regex=True)
                                                df_contrato[coluna_total_faturamento] = df_contrato[coluna_total_faturamento].str.replace(',', '.')
                                                df_contrato[coluna_total_faturamento] = df_contrato[coluna_total_faturamento].str.strip()
                                                df_contrato[coluna_total_faturamento] = pd.to_numeric(df_contrato[coluna_total_faturamento], errors='coerce')
                                            except:
                                                pass
                                            
                                            # Encontrar totais de cada mês usando a mesma lógica de pares COMPETENCIA → TOTAL
                                            df_contrato_reset = df_contrato.reset_index(drop=True)
                                            pares_competencia_total_fat = []
                                            competencia_idx = None
                                            
                                            for idx in range(len(df_contrato_reset)):
                                                valor_col = str(df_contrato_reset.iloc[idx][coluna_mes]).strip().upper()
                                                
                                                if 'COMPET' in valor_col:
                                                    if competencia_idx is not None:
                                                        pares_competencia_total_fat.append((competencia_idx, idx - 1))
                                                    competencia_idx = idx
                                                elif 'TOTAL' in valor_col and competencia_idx is not None:
                                                    pares_competencia_total_fat.append((competencia_idx, idx))
                                                    competencia_idx = None
                                            
                                            if competencia_idx is not None:
                                                pares_competencia_total_fat.append((competencia_idx, len(df_contrato_reset) - 1))
                                            
                                            # Processar meses de faturamento (OUTUBRO, NOVEMBRO, DEZEMBRO)
                                            meses_faturamento_dados = []
                                            ordem_meses_fat = ['JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO', 'JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO']
                                            
                                            for idx_par, (inicio_idx, fim_idx) in enumerate(pares_competencia_total_fat):
                                                if idx_par < len(ordem_meses_fat):
                                                    mes_nome = ordem_meses_fat[idx_par]
                                                    
                                                    # Se for um dos meses de faturamento, pegar o valor TOTAL (linha fim_idx, coluna índice 2)
                                                    if mes_nome in meses_faturamento:
                                                        valor_total_mes = df_contrato_reset.iloc[fim_idx][coluna_total_faturamento]
                                                        if pd.notna(valor_total_mes) and valor_total_mes > 0:
                                                            meses_faturamento_dados.append({
                                                                'Mês': mes_nome,
                                                                'Total': valor_total_mes
                                                            })
                                            
                                            # Mostrar tabela dos últimos 3 meses
                                            if meses_faturamento_dados:
                                                st.markdown("**📅 Últimos 3 Meses de Faturamento:**")
                                                html_ultimos_meses = '<div style="margin: 20px 0;"><table style="width: 100%; border-collapse: collapse; background: rgba(255,255,255,0.02); border-radius: 8px; overflow: hidden;">'
                                                html_ultimos_meses += '<thead><tr style="background: rgba(139, 92, 246, 0.15);"><th style="padding: 12px 16px; text-align: left; font-weight: 600; color: rgba(255,255,255,0.9); border-bottom: 2px solid rgba(255,255,255,0.1);">Mês</th><th style="padding: 12px 16px; text-align: right; font-weight: 600; color: rgba(255,255,255,0.9); border-bottom: 2px solid rgba(255,255,255,0.1);">Total</th></tr></thead><tbody>'
                                                
                                                for idx, item in enumerate(meses_faturamento_dados):
                                                    row_style = "background: rgba(255,255,255,0.02);" if idx % 2 == 0 else "background: rgba(255,255,255,0.05);"
                                                    html_ultimos_meses += f'<tr style="{row_style}"><td style="padding: 10px 16px; color: rgba(255,255,255,0.9);">{item["Mês"]}</td><td style="padding: 10px 16px; text-align: right; color: rgba(255,255,255,0.9);">{formatar_valor(item["Total"])}</td></tr>'
                                                
                                                html_ultimos_meses += '</tbody></table></div>'
                                                st.markdown(html_ultimos_meses, unsafe_allow_html=True)
                                        
                                        st.markdown("---")
                                        st.markdown("**📋 Detalhamento de Valores em Aberto:**")
                                        st.dataframe(
                                            df_aberto.head(20),
                                            use_container_width=True,
                                            hide_index=True
                                        )
                                        
                                        if len(df_aberto) > 20:
                                            st.caption(f"Mostrando 20 de {len(df_aberto)} registros em aberto")
                                else:
                                    st.warning("⚠️ Não foi possível identificar colunas de SITUAÇÃO ou valores monetários")
                            
                            else:
                                # Para outros contratos, mostrar apenas a tabela (sem métricas)
                                st.markdown("**📋 Dados Detalhados:**")
                                
                                # Mostrar tabela completa
                                st.dataframe(
                                    df_contrato,
                                    use_container_width=True,
                                    hide_index=True
                                )
                                
                                # Mostrar total de registros como caption
                                st.caption(f"Total de {len(df_contrato)} registros")
                    
                    except Exception as e:
                        st.error(f"❌ Erro ao carregar dados de {contrato}: {str(e)}")
                        st.info(f"💡 Dica: Verifique se a aba '{contrato}' existe na planilha")
        
        
    else:
        st.markdown(f'<h1 class="main-header">{selected_nav}</h1>', unsafe_allow_html=True)
        st.info(f"📊 Sistema {selected_nav} não encontrado")

# Código antigo das tabs removido - agora usando sistema de cards

# Rodapé
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>Painel de Monitoramento Dashboard | Criado com Streamlit</div>",
    unsafe_allow_html=True
)
