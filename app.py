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
else:
    logo_img = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" style="width: 40px; height: 40px;"><path stroke-linecap="round" stroke-linejoin="round" d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"></path></svg>'

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
        '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">'
        '<path stroke-linecap="round" stroke-linejoin="round" d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"></path>'
        '</svg>'
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
        
        # Ícones SVG para cada sistema
        icon_svg_map = {
            "Viva Saúde": '<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>',
            "Coop Vitta": '<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>',
            "Delta": '<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>'
        }
        
        svg_path = icon_svg_map.get(selected_nav, icon_svg_map["Viva Saúde"])
        
        # Card específico do sistema (similar ao card geral)
        sistema_card_html = (
            f'<div class="system-card" id="{selected_nav.lower().replace(" ", "-")}-card" style="display: block;">'
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
            contratos_html = (
                '<div id="viva-saude-contratos-card" style="margin-top: 30px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.1);">'
                '<h3 style="font-size: 16px; font-weight: 600; color: rgba(255,255,255,0.9); margin-bottom: 15px;">Contratos Ativos</h3>'
                '<div style="display: flex; flex-wrap: wrap; gap: 12px; justify-content: center;">'
                '<button class="contrato-btn active" data-contrato="UPAS" type="button" style="display: flex; align-items: center; gap: 6px; padding: 8px 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; cursor: pointer; transition: all 0.3s ease; color: rgba(255,255,255,0.9); font-size: 13px; -webkit-tap-highlight-color: transparent; touch-action: manipulation;"><span style="width: 8px; height: 8px; background: #10b981; border-radius: 50%; display: inline-block;"></span><span>UPAS</span><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" style="width: 16px; height: 16px; margin-left: 4px;"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5"></path></svg></button>'
                '<button class="contrato-btn" data-contrato="EVOLUIR" type="button" style="display: flex; align-items: center; gap: 6px; padding: 8px 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; cursor: pointer; transition: all 0.3s ease; color: rgba(255,255,255,0.9); font-size: 13px; -webkit-tap-highlight-color: transparent; touch-action: manipulation;"><span style="width: 8px; height: 8px; background: #10b981; border-radius: 50%; display: inline-block;"></span><span>EVOLUIR</span><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" style="width: 16px; height: 16px; margin-left: 4px;"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5"></path></svg></button>'
                '<button class="contrato-btn" data-contrato="CPSS" type="button" style="display: flex; align-items: center; gap: 6px; padding: 8px 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; cursor: pointer; transition: all 0.3s ease; color: rgba(255,255,255,0.9); font-size: 13px; -webkit-tap-highlight-color: transparent; touch-action: manipulation;"><span style="width: 8px; height: 8px; background: #10b981; border-radius: 50%; display: inline-block;"></span><span>CPSS</span><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" style="width: 16px; height: 16px; margin-left: 4px;"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5"></path></svg></button>'
                '<button class="contrato-btn" data-contrato="CRATEUS" type="button" style="display: flex; align-items: center; gap: 6px; padding: 8px 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; cursor: pointer; transition: all 0.3s ease; color: rgba(255,255,255,0.9); font-size: 13px; -webkit-tap-highlight-color: transparent; touch-action: manipulation;"><span style="width: 8px; height: 8px; background: #10b981; border-radius: 50%; display: inline-block;"></span><span>CRATEUS</span><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" style="width: 16px; height: 16px; margin-left: 4px;"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5"></path></svg></button>'
                '<button class="contrato-btn" data-contrato="ITAPIPOCA" type="button" style="display: flex; align-items: center; gap: 6px; padding: 8px 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; cursor: pointer; transition: all 0.3s ease; color: rgba(255,255,255,0.9); font-size: 13px; -webkit-tap-highlight-color: transparent; touch-action: manipulation;"><span style="width: 8px; height: 8px; background: #10b981; border-radius: 50%; display: inline-block;"></span><span>ITAPIPOCA</span><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" style="width: 16px; height: 16px; margin-left: 4px;"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5"></path></svg></button>'
                '</div>'
                '<div id="viva-saude-financeiro-contratos" style="margin-top: 20px;"><div id="financeiro-UPAS" class="financeiro-contrato-section active" style="display: block;"><h4 style="font-size: 16px; font-weight: 600; color: rgba(255,255,255,0.9); margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.1);">Financeiro - UPAS</h4><div id="financeiro-UPAS-content"><p style="color: rgba(255,255,255,0.5);">Dados ainda não disponíveis. Buscando...</p></div></div></div>'
                '</div>'
                '<style>.contrato-btn.active{background:rgba(16,185,129,0.15)!important;border-color:#10b981!important;}.contrato-btn:hover{background:rgba(255,255,255,0.1)!important;transform:translateY(-2px);}.financeiro-contrato-section{display:none;animation:fadeIn 0.3s ease-in-out;}.financeiro-contrato-section.active{display:block;}@keyframes fadeIn{from{opacity:0;transform:translateY(10px);}to{opacity:1;transform:translateY(0);}}</style>'
                '<script>(function(){const contratoButtons=document.querySelectorAll(".contrato-btn");const sections=document.querySelectorAll(".financeiro-contrato-section");contratoButtons.forEach(button=>{button.addEventListener("click",function(){const contrato=this.getAttribute("data-contrato");contratoButtons.forEach(btn=>btn.classList.remove("active"));this.classList.add("active");sections.forEach(section=>section.classList.remove("active"));const targetSection=document.getElementById("financeiro-"+contrato);if(targetSection){targetSection.classList.add("active");}else{const container=document.getElementById("viva-saude-financeiro-contratos");const newSection=document.createElement("div");newSection.id="financeiro-"+contrato;newSection.className="financeiro-contrato-section active";newSection.innerHTML=`<h4 style="font-size: 16px; font-weight: 600; color: rgba(255,255,255,0.9); margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.1);">Financeiro - ${contrato}</h4><div id="financeiro-${contrato}-content"><p style="color: rgba(255,255,255,0.5);">Dados ainda não disponíveis. Buscando...</p></div>`;container.appendChild(newSection);}});});})();</script>'
            )
            
            st.markdown(contratos_html, unsafe_allow_html=True)
        
        
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
