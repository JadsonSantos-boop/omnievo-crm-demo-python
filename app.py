# -*- coding: utf-8 -*-
# OMNIEVO DEMO CRM - Versao Executiva de Apresentacao
# Foco: Cosmeticos, Dermocosmeticos & Estetica B2B
import streamlit as st
import pandas as pd
import datetime
from datetime import date
import random
import time
import base64
import json
import plotly.express as px
import plotly.graph_objects as go

# Configuração de Página
st.set_page_config(
    page_title="Omnievo CRM - Demonstração Comercial",
    page_icon="assets/logo_icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS Personalizada de Alto Padrão (Dark Theme Omnievo)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background-color: #080B11;
        color: #F8FAFC;
    }
    
    /* Header & Badges */
    .metric-card {
        background: rgba(17, 24, 39, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 18px 20px;
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        border-color: rgba(124, 58, 237, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 10px 25px -5px rgba(109, 40, 217, 0.25);
    }
    
    .metric-title {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #94A3B8;
    }
    
    .metric-val {
        font-size: 26px;
        font-weight: 800;
        color: #FFFFFF;
        margin-top: 4px;
    }
    
    .metric-badge {
        display: inline-block;
        font-size: 10px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 6px;
        margin-top: 6px;
    }
    
    /* Kanban Cards */
    .kanban-col {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 14px;
        padding: 14px;
        min-height: 580px;
    }
    
    .kanban-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 12px;
        transition: all 0.2s;
    }
    .kanban-card:hover {
        border-color: #8B5CF6;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.2);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0B0F19;
        border-right: 1px solid rgba(255, 255, 255, 0.07);
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 10px;
        font-weight: 700;
        transition: all 0.2s ease;
    }
</style>
""", unsafe_allow_html=True)

# Inicialização de Dados Fictícios de Cosméticos & Dermocosméticos na Sessão
def inicializar_dados_demo(forcar=False):
    if "demo_iniciado" in st.session_state and not forcar:
        return
        
    st.session_state["demo_iniciado"] = True
    
    # 1. Catálogo Fictício Premium
    st.session_state["catalogo"] = [
        {"codigo": "SKU-101", "nome": "Sérum Clareador Vitamina C 15% (30ml)", "preco": 68.50, "estoque": 1250, "categoria": "Tratamento Facial", "lote": "L2608", "val": "11/2027", "caixa": "P"},
        {"codigo": "SKU-102", "nome": "Protetor Solar Fluido Toque Seco FPS 70 (50ml)", "preco": 54.90, "estoque": 2180, "categoria": "Fotoproteção", "lote": "L2612", "val": "03/2028", "caixa": "P"},
        {"codigo": "SKU-103", "nome": "Ácido Hialurônico Concentrado Filler (30ml)", "preco": 79.00, "estoque": 890, "categoria": "Tratamento Facial", "lote": "L2603", "val": "09/2027", "caixa": "P"},
        {"codigo": "SKU-104", "nome": "Gel de Limpeza Profunda Micelar (200ml)", "preco": 38.20, "estoque": 1640, "categoria": "Higienização", "lote": "L2605", "val": "01/2028", "caixa": "G"},
        {"codigo": "SKU-105", "nome": "Creme Reparador Noturno Retinol Puro 0.3% (50g)", "preco": 94.00, "estoque": 380, "categoria": "Anti-Idade", "lote": "L2601", "val": "08/2027", "caixa": "P"},
        {"codigo": "SKU-106", "nome": "Bruma Hidratante Termal Mineralizante (150ml)", "preco": 42.00, "estoque": 3100, "categoria": "Hidratação", "lote": "L2610", "val": "05/2028", "caixa": "G"},
        {"codigo": "SKU-107", "nome": "Máscara Purificante Argila Vulcânica (100g)", "preco": 48.00, "estoque": 740, "categoria": "Máscaras", "lote": "L2599", "val": "12/2027", "caixa": "P"},
        {"codigo": "SKU-108", "nome": "Peeling Químico Renovador Mandélico (30ml)", "preco": 115.00, "estoque": 310, "categoria": "Cabine Profissional", "lote": "L2604", "val": "10/2027", "caixa": "P"},
        {"codigo": "SKU-109", "nome": "Loção Corporal Hidratante Ceramidas 10% (400ml)", "preco": 62.00, "estoque": 1950, "categoria": "Corporal", "lote": "L2609", "val": "04/2028", "caixa": "G"},
        {"codigo": "SKU-110", "nome": "Óleo Facial Nutritivo Rosa Mosqueta Puro (30ml)", "preco": 49.90, "estoque": 860, "categoria": "Tratamento Facial", "lote": "L2602", "val": "07/2027", "caixa": "P"},
        {"codigo": "SKU-111", "nome": "Kit Cabine Estética Profissional DermoClean (5 Itens)", "preco": 385.00, "estoque": 140, "categoria": "Kits Cabine", "lote": "L2615", "val": "06/2028", "caixa": "G"},
        {"codigo": "SKU-112", "nome": "Sabonete Esfoliante Enzimático de Romã (120g)", "preco": 44.50, "estoque": 1120, "categoria": "Higienização", "lote": "L2607", "val": "02/2028", "caixa": "P"}
    ]
    
    # 2. Clientes B2B Fictícios
    st.session_state["clientes"] = [
        {"id": 101, "nome": "Drogaria Brasil & Perfumaria Matriz", "cnpj": "14.892.311/0001-92", "uf": "SP", "cidade": "São Paulo", "vendedor": "Gabriel Santos", "limite": 80000.0, "status": "Ativo", "prazo": "28/35/42 dias", "dias_sem_comprar": 12},
        {"id": 102, "nome": "Clínica Dermatológica Bella Pelle", "cnpj": "28.419.002/0001-44", "uf": "RJ", "cidade": "Rio de Janeiro", "vendedor": "Gabriel Santos", "limite": 50000.0, "status": "Ativo", "prazo": "30/60 dias", "dias_sem_comprar": 8},
        {"id": 103, "nome": "Rede Farmavida Medicamentos & Cosméticos", "cnpj": "07.129.845/0001-33", "uf": "MG", "cidade": "Belo Horizonte", "vendedor": "Lucas Mendes", "limite": 120000.0, "status": "Ativo", "prazo": "21/28/35/42 dias", "dias_sem_comprar": 18},
        {"id": 104, "nome": "Emporium Estética & Spa Curitiba", "cnpj": "19.822.450/0001-18", "uf": "PR", "cidade": "Curitiba", "vendedor": "Camila Duarte", "limite": 35000.0, "status": "Alerta Churn", "prazo": "28 dias", "dias_sem_comprar": 48},
        {"id": 105, "nome": "Dermacenter Produtos Dermatológicos", "cnpj": "33.102.778/0001-59", "uf": "BA", "cidade": "Salvador", "vendedor": "Gabriel Santos", "limite": 65000.0, "status": "Ativo", "prazo": "30/45 dias", "dias_sem_comprar": 15},
        {"id": 106, "nome": "Cosméticos & Cia Atacadista do ES", "cnpj": "09.554.120/0001-01", "uf": "ES", "cidade": "Vitória", "vendedor": "Lucas Mendes", "limite": 90000.0, "status": "Ativo", "prazo": "28/42 dias", "dias_sem_comprar": 22},
        {"id": 107, "nome": "FarmaSul Distribuidora Integrada", "cnpj": "18.239.901/0001-72", "uf": "RS", "cidade": "Porto Alegre", "vendedor": "Camila Duarte", "limite": 110000.0, "status": "Ativo", "prazo": "30/60/90 dias", "dias_sem_comprar": 5},
        {"id": 108, "nome": "BioEstética Clínicas Integradas", "cnpj": "24.671.309/0001-85", "uf": "GO", "cidade": "Goiânia", "vendedor": "Rafael Costa", "limite": 40000.0, "status": "Inativo", "prazo": "À Vista / PIX", "dias_sem_comprar": 74}
    ]
    
    # 3. Pedidos Fictícios Iniciais (Distribuídos no Kanban)
    st.session_state["pedidos"] = [
        {"numero": "#PED-9840", "cliente": "Drogaria Brasil & Perfumaria Matriz", "uf": "SP", "valor": 48900.00, "etapa": "50/60 - Faturado", "data": "02/11/2026", "vendedor": "Gabriel Santos", "transp": "Braspress", "rastreio": "CTE-84920", "status_entrega": "Em Trânsito"},
        {"numero": "#PED-9841", "cliente": "Clínica Dermatológica Bella Pelle", "uf": "RJ", "valor": 19300.00, "etapa": "50/60 - Faturado", "data": "04/11/2026", "vendedor": "Gabriel Santos", "transp": "SSW Transportes", "rastreio": "CTE-84918", "status_entrega": "Entregue"},
        {"numero": "#PED-9842", "cliente": "Rede Farmavida Medicamentos & Cosméticos", "uf": "MG", "valor": 52800.00, "etapa": "50/60 - Faturado", "data": "06/11/2026", "vendedor": "Lucas Mendes", "transp": "Braspress", "rastreio": "CTE-84915", "status_entrega": "Entregue"},
        {"numero": "#PED-9843", "cliente": "Rede Farmavida Medicamentos & Cosméticos", "uf": "MG", "valor": 28900.00, "etapa": "70 - Separação", "data": "10/11/2026", "vendedor": "Lucas Mendes", "transp": "Braspress", "rastreio": "Pendente NFe", "status_entrega": "Em Separação no Armazém"},
        {"numero": "#PED-9844", "cliente": "Cosméticos & Cia Atacadista do ES", "uf": "ES", "valor": 17500.00, "etapa": "70 - Separação", "data": "11/11/2026", "vendedor": "Lucas Mendes", "transp": "Frota Própria", "rastreio": "Expedição Direta", "status_entrega": "Conferência de Lote"},
        {"numero": "#PED-9845", "cliente": "FarmaSul Distribuidora Integrada", "uf": "RS", "valor": 31250.00, "etapa": "70 - Separação", "data": "12/11/2026", "vendedor": "Camila Duarte", "transp": "Braspress", "rastreio": "Pendente NFe", "status_entrega": "Em Separação no Armazém"},
        {"numero": "#PED-9846", "cliente": "Dermacenter Produtos Dermatológicos", "uf": "BA", "valor": 22400.00, "etapa": "20 - Análise Financeira", "data": "12/11/2026", "vendedor": "Gabriel Santos", "transp": "Braspress", "rastreio": "Aguardando", "status_entrega": "Validação de Crédito Boleto"},
        {"numero": "#PED-9847", "cliente": "Drogaria Brasil & Perfumaria Matriz", "uf": "SP", "valor": 38600.00, "etapa": "20 - Análise Financeira", "data": "13/11/2026", "vendedor": "Gabriel Santos", "transp": "Braspress", "rastreio": "Aguardando", "status_entrega": "Checagem Limite Omie ERP"},
        {"numero": "#PED-9848", "cliente": "BioEstética Clínicas Integradas", "uf": "GO", "valor": 8950.00, "etapa": "10 - Proposta", "data": "13/11/2026", "vendedor": "Rafael Costa", "transp": "Sedex", "rastreio": "Proposta", "status_entrega": "Negociação com Comprador"},
        {"numero": "#PED-9849", "cliente": "Emporium Estética & Spa Curitiba", "uf": "PR", "valor": 14200.00, "etapa": "10 - Proposta", "data": "13/11/2026", "vendedor": "Camila Duarte", "transp": "Braspress", "rastreio": "Proposta", "status_entrega": "Aguardando De Acordo"}
    ]

inicializar_dados_demo()

# SIDEBAR EXECUTIVA
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 16px 12px; background: linear-gradient(180deg, #1E1B4B 0%, #0F172A 100%); border-radius: 14px; border: 1px solid rgba(139, 92, 246, 0.3); margin-bottom: 14px;">
        <div style="font-size: 22px; font-weight: 900; letter-spacing: 0.18em; color: #FFFFFF; text-shadow: 0 0 15px rgba(167, 139, 250, 0.6);">OMNIEVO</div>
        <div style="font-size: 10px; font-weight: 800; letter-spacing: 0.22em; color: #FBBF24; text-transform: uppercase; margin-top: 4px;">COSMÉTICOS & DERMO B2B</div>
        <div style="display: inline-flex; align-items: center; gap: 6px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 20px; padding: 2px 10px; margin-top: 8px;">
            <span style="width: 6px; height: 6px; border-radius: 50%; background: #34D399;"></span>
            <span style="font-size: 10px; color: #34D399; font-weight: 700;">MODO DEMONSTRAÇÃO VIP</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Seletor de Perfil da Apresentação
    perfil = st.selectbox(
        "👤 PERFIL DE APRESENTAÇÃO:",
        ["👑 Diretor Comercial (Master Admin)", "👔 Consultor de Vendas (Gabriel Santos)"],
        index=0
    )
    is_master = "Diretor" in perfil
    
    st.markdown("---")
    
    opcoes_menu = [
        "📋  Novo Pedido B2B",
        "📊  Kanban de Vendas",
        "📈  Dashboard & Metas",
        "🏆  Pódio dos Vendedores",
        "🚚  Rastreamento & Logística",
        "🚨  Radar de Clientes & Churn",
        "📦  Estoque & Validades (FEFO)",
        "👤  Cadastrar Cliente"
    ]
    
    pagina = st.radio("NAVEGAÇÃO DO SISTEMA:", opcoes_menu)
    
    st.markdown("---")
    st.markdown("""
    <div style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 10px 12px;">
        <div style="font-size: 11px; font-weight: 700; color: #CBD5E1;">⚡ ERP INTEGRADO (0ms)</div>
        <div style="font-size: 10px; color: #94A3B8; margin-top: 2px;">Omie ERP Direct Sync Engine</div>
        <div style="font-size: 10px; color: #34D399; font-weight: 600; margin-top: 2px;">● Conexão 100% Homologada</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Restaurar Dados Iniciais", help="Reseta os dados para o padrão inicial da apresentação"):
        inicializar_dados_demo(forcar=True)
        st.toast("Dados da demonstração restaurados com sucesso!", icon="✨")
        st.rerun()

# HEADER SUPERIOR
col_h1, col_h2 = st.columns([8, 4])
with col_h1:
    st.markdown(f"### {pagina}")
    st.caption("Plataforma Comercial B2B integrada nativamente ao ERP e Operação Logística")
with col_h2:
    st.markdown("""
    <div style="text-align: right; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #94A3B8; padding-top: 6px;">
        NODE: <span style="color: #34D399; font-weight: 700;">ACTIVE_DEMO_NODE</span> | LATENCY: <span style="color: #34D399; font-weight: 700;">0.2ms</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='margin-top: 0; margin-bottom: 20px; border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 1. NOVO PEDIDO B2B
# ══════════════════════════════════════════════════════════════════════════════
if "Novo Pedido" in pagina:
    st.info("💡 **Dica de Apresentação:** Mostre a rapidez da emissão. Ao selecionar o cliente, os dados fiscais e tabela de preços carregam na hora. O frete e a cubagem 3D são calculados automaticamente!")
    
    col_c1, col_c2, col_c3 = st.columns([5, 4, 3])
    with col_c1:
        clientes_nomes = [f"{c['nome']} ({c['uf']}) - CNPJ: {c['cnpj']}" for c in st.session_state["clientes"]]
        sel_cli_str = st.selectbox("Selecione o Cliente (Digitação ou Busca de CNPJ):", clientes_nomes)
        cli_sel = next(c for c in st.session_state["clientes"] if c["nome"] in sel_cli_str)
    
    with col_c2:
        st.selectbox("Condição de Faturamento:", [cli_sel["prazo"], "Boleto 30/60 dias", "PIX Antecipado (5% Desc)", "Cartão B2B Parcelado"])
    
    with col_c3:
        st.markdown(f"""
        <div style="background: rgba(124, 58, 237, 0.15); border: 1px solid rgba(124, 58, 237, 0.35); border-radius: 10px; padding: 10px 14px;">
            <div style="font-size: 10px; font-weight: 700; color: #C4B5FD;">LIMITE DE CRÉDITO ERP:</div>
            <div style="font-size: 15px; font-weight: 800; color: #FFFFFF;">R$ {cli_sel['limite']:,.2f}</div>
            <div style="font-size: 10px; color: #34D399; font-weight: 700;">● Score Serasa: 840 (Aprovado)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 📦 Adicionar Produtos ao Pedido")
    
    if "carrinho_demo" not in st.session_state:
        st.session_state["carrinho_demo"] = [
            {"sku": "SKU-101", "nome": "Sérum Clareador Vitamina C 15% (30ml)", "preco": 68.50, "qtd": 48, "tipo": "Venda Normal"},
            {"sku": "SKU-102", "nome": "Protetor Solar Fluido Toque Seco FPS 70 (50ml)", "preco": 54.90, "qtd": 72, "tipo": "Venda Normal"},
            {"sku": "SKU-106", "nome": "Bruma Hidratante Termal Mineralizante (150ml)", "preco": 0.00, "qtd": 10, "tipo": "Bonificação (Brinde)"}
        ]
        
    col_p1, col_p2, col_p3, col_p4 = st.columns([5, 2, 3, 2])
    with col_p1:
        prod_opcoes = [f"{p['codigo']} - {p['nome']} (R$ {p['preco']:.2f}) [Estoque: {p['estoque']} un]" for p in st.session_state["catalogo"]]
        sel_prod_str = st.selectbox("Produto:", prod_opcoes)
        prod_obj = next(p for p in st.session_state["catalogo"] if p["codigo"] in sel_prod_str)
    with col_p2:
        qtd_add = st.number_input("Quantidade (un):", min_value=1, max_value=500, value=24, step=6)
    with col_p3:
        tipo_item = st.selectbox("Finalidade Fiscal:", ["Venda Normal", "Bonificação (Brinde)", "Amostra Grátis"])
    with col_p4:
        st.write("")
        st.write("")
        if st.button("➕ Inserir Item", use_container_width=True):
            p_final = 0.00 if "Bonif" in tipo_item or "Amostra" in tipo_item else prod_obj["preco"]
            st.session_state["carrinho_demo"].append({
                "sku": prod_obj["codigo"],
                "nome": prod_obj["nome"],
                "preco": p_final,
                "qtd": qtd_add,
                "tipo": tipo_item
            })
            st.toast(f"{prod_obj['nome']} adicionado ao pedido!", icon="✅")
            st.rerun()

    # Tabela do Carrinho
    st.markdown("##### Itens Selecionados no Pedido:")
    total_pedido = 0.0
    total_unidades = 0
    linhas_carrinho = []
    
    for idx, item in enumerate(st.session_state["carrinho_demo"]):
        sub = item["preco"] * item["qtd"]
        total_pedido += sub
        total_unidades += item["qtd"]
        linhas_carrinho.append({
            "Item": idx + 1,
            "SKU": item["sku"],
            "Descrição do Produto": item["nome"],
            "Finalidade": item["tipo"],
            "Quantidade": f"{item['qtd']} un",
            "Preço Unitário": f"R$ {item['preco']:.2f}",
            "Subtotal": f"R$ {sub:,.2f}"
        })
        
    df_car = pd.DataFrame(linhas_carrinho)
    st.dataframe(df_car, use_container_width=True, hide_index=True)
    
    # Resumo com Cubagem e Frete Braspress
    col_r1, col_r2 = st.columns([6, 6])
    with col_r1:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #8B5CF6;">
            <div style="font-size: 13px; font-weight: 700; color: #C4B5FD;">📦 CUBAGEM 3D & LOGÍSTICA INTELIGENTE:</div>
            <div style="font-size: 12px; color: #E2E8F0; margin-top: 6px;">
                ● <b>Volume Estimado:</b> {total_unidades} frascos/bisnagas<br>
                ● <b>Embalagem Calculada:</b> <span style="color: #FBBF24; font-weight: 700;">2x Caixa Grande (Master Padrão) + 1x Caixa Pequena</span><br>
                ● <b>Transportadora Homologada:</b> Braspress Rodoviário (Cotação Automática API)<br>
                ● <b>Prazo Previsto de Entrega:</b> 3 dias úteis para {cli_sel['uf']} (Frete CIF Cortesia Comercial)
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_r2:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #10B981; text-align: right;">
            <div style="font-size: 12px; font-weight: 700; color: #94A3B8;">VALOR TOTAL DO PEDIDO:</div>
            <div style="font-size: 32px; font-weight: 900; color: #10B981;">R$ {total_pedido:,.2f}</div>
            <div style="font-size: 11px; color: #CBD5E1;">Impostos Destacados (ST / ICMS): Inclusos | Condição: {cli_sel['prazo']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    col_b1, col_b2, col_b3 = st.columns([4, 4, 4])
    with col_b1:
        if st.button("🚀 Transmitir ao Omie ERP (1 Clique)", type="primary", use_container_width=True):
            with st.spinner("Transmitindo pedido em tempo real ao Omie ERP..."):
                time.sleep(0.6)
                novo_num = f"#PED-{random.randint(9850, 9990)}"
                st.session_state["pedidos"].insert(0, {
                    "numero": novo_num,
                    "cliente": cli_sel["nome"],
                    "uf": cli_sel["uf"],
                    "valor": total_pedido,
                    "etapa": "10 - Proposta",
                    "data": datetime.date.today().strftime("%d/%m/%Y"),
                    "vendedor": cli_sel["vendedor"],
                    "transp": "Braspress",
                    "rastreio": "Integrando...",
                    "status_entrega": "Transmitido com Sucesso ao ERP (0.4s)"
                })
                st.balloons()
                st.success(f"✨ Pedido {novo_num} gravado no Omie ERP com Sucesso em 0.4s! Estoque reservado em lote.")
                
    with col_b2:
        if st.button("📄 Gerar Proposta Comercial (PDF WhatsApp)", use_container_width=True):
            st.toast("Proposta Comercial Executiva gerada em PDF de alta resolução!", icon="📋")
            st.info("📱 **Visualização Rápida:** Proposta formatada com logo Omnievo, CNPJ, dados de frete e boletos 28/35/42 dias pronta para envio no WhatsApp do comprador!")
            
    with col_b3:
        if st.button("🗑️ Limpar Carrinho", use_container_width=True):
            st.session_state["carrinho_demo"] = []
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# 2. KANBAN DE VENDAS
# ══════════════════════════════════════════════════════════════════════════════
elif "Kanban" in pagina:
    st.info("💡 **Dica de Apresentação:** Este Kanban elimina reuniões desnecessárias. Toda a diretoria e os vendedores sabem exatamente quais pedidos estão em digitação, travados no crédito ou prontos para despachar!")
    
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    
    etapas = [
        ("📝 Etapa 10: Propostas", "10 - Proposta", col_k1, "#60A5FA"),
        ("⏳ Etapa 20: Análise Financeira", "20 - Análise Financeira", col_k2, "#FBBF24"),
        ("📦 Etapa 70: Em Separação", "70 - Separação", col_k3, "#C084FC"),
        ("🚚 Etapa 50/60: Faturados", "50/60 - Faturado", col_k4, "#34D399")
    ]
    
    for titulo, etapa_cod, col, cor in etapas:
        with col:
            pedidos_etapa = [p for p in st.session_state["pedidos"] if p["etapa"] == etapa_cod]
            total_etapa = sum(p["valor"] for p in pedidos_etapa)
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.7); border-top: 3px solid {cor}; border-radius: 12px; padding: 10px 14px; margin-bottom: 12px;">
                <div style="font-size: 13px; font-weight: 800; color: #FFFFFF;">{titulo}</div>
                <div style="font-size: 11px; color: #94A3B8; font-family: 'JetBrains Mono';">{len(pedidos_etapa)} pedidos | R$ {total_etapa:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
            
            for p in pedidos_etapa:
                st.markdown(f"""
                <div class="kanban-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-family: 'JetBrains Mono'; font-weight: 700; color: #A78BFA; font-size: 12px;">{p['numero']}</span>
                        <span style="font-size: 10px; background: rgba(255,255,255,0.08); padding: 2px 6px; border-radius: 4px; color: #CBD5E1;">{p['uf']}</span>
                    </div>
                    <div style="font-size: 13px; font-weight: 700; color: #FFFFFF; margin-top: 5px; line-height: 1.2;">{p['cliente']}</div>
                    <div style="font-size: 14px; font-weight: 800; color: #34D399; margin-top: 6px;">R$ {p['valor']:,.2f}</div>
                    <div style="font-size: 11px; color: #94A3B8; margin-top: 4px;">👔 {p['vendedor']} | 🚚 {p['transp']}</div>
                    <div style="font-size: 10px; color: #C4B5FD; margin-top: 4px; font-family: 'JetBrains Mono';">● {p['status_entrega']}</div>
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 3. DASHBOARD DE FATURAMENTO & METAS
# ══════════════════════════════════════════════════════════════════════════════
elif "Dashboard" in pagina:
    st.info("💡 **Dica de Apresentação:** Destaque que as vendas B2B (distribuidores e redes) e B2C (e-commerce) são separadas em tempo real, expurgando bonificações para não distorcer a margem do CEO!")
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">FATURAMENTO MÊS ATUAL</div>
            <div class="metric-val" style="color: #34D399;">R$ 548.920,00</div>
            <div class="metric-badge" style="background: rgba(16, 185, 129, 0.2); color: #34D399;">▲ +22.4% vs mês ant.</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">META COMERCIAL (PACING)</div>
            <div class="metric-val" style="color: #FBBF24;">91.5%</div>
            <div class="metric-badge" style="background: rgba(245, 158, 11, 0.2); color: #FBBF24;">Meta: R$ 600.000,00</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">TICKET MÉDIO B2B</div>
            <div class="metric-val" style="color: #A78BFA;">R$ 18.920,00</div>
            <div class="metric-badge" style="background: rgba(139, 92, 246, 0.2); color: #C4B5FD;">Média de 142 itens/pedido</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">ECONOMIA DE FRETE (CUBAGEM)</div>
            <div class="metric-val" style="color: #38BDF8;">R$ 12.450,00</div>
            <div class="metric-badge" style="background: rgba(56, 189, 248, 0.2); color: #38BDF8;">Otimização de Caixas 3D</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("#### 📊 Evolução de Faturamento Diário B2B vs B2C")
    
    # Gráfico Plotly
    dias = [f"{d}/11" for d in range(1, 14)]
    vendas_b2b = [28500, 34200, 48900, 31000, 52000, 41000, 64000, 38000, 49000, 58000, 32000, 45000, 26320]
    vendas_b2c = [4200, 5100, 6800, 4900, 7200, 5800, 8900, 6100, 7400, 8200, 5600, 7100, 4900]
    
    df_graf = pd.DataFrame({"Dia": dias, "Corporativo B2B (Redes)": vendas_b2b, "E-commerce B2C": vendas_b2c})
    fig = px.bar(df_graf, x="Dia", y=["Corporativo B2B (Redes)", "E-commerce B2C"], 
                 barmode="group", color_discrete_sequence=["#8B5CF6", "#38BDF8"],
                 template="plotly_dark")
    fig.update_layout(
        plot_bgcolor="rgba(15, 23, 42, 0.4)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# 4. PÓDIO DOS VENDEDORES
# ══════════════════════════════════════════════════════════════════════════════
elif "Pódio" in pagina:
    st.info("💡 **Dica de Apresentação:** O Pódio gera gamificação e engajamento. Cada vendedor acompanha suas medalhas e comissões ao vivo pelo celular!")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        st.markdown("""
        <div class="metric-card" style="border: 2px solid #F59E0B; text-align: center; background: linear-gradient(180deg, rgba(245, 158, 11, 0.15) 0%, rgba(15, 23, 42, 0.7) 100%);">
            <div style="font-size: 38px;">🥇</div>
            <div style="font-size: 18px; font-weight: 800; color: #FBBF24;">Gabriel Santos</div>
            <div style="font-size: 11px; color: #CBD5E1;">Consultor Sênior São Paulo / Sudeste</div>
            <div style="font-size: 24px; font-weight: 900; color: #34D399; margin-top: 10px;">R$ 194.850,00</div>
            <div style="font-size: 11px; color: #FBBF24; font-weight: 700; margin-top: 2px;">108.2% da Meta (R$ 180.000)</div>
            <div style="font-size: 11px; color: #94A3B8; margin-top: 6px;">💰 Comissão Estimada: <b>R$ 7.794,00</b></div>
        </div>
        """, unsafe_allow_html=True)
    with col_p2:
        st.markdown("""
        <div class="metric-card" style="border: 2px solid #94A3B8; text-align: center;">
            <div style="font-size: 38px;">🥈</div>
            <div style="font-size: 18px; font-weight: 800; color: #E2E8F0;">Lucas Mendes</div>
            <div style="font-size: 11px; color: #CBD5E1;">Representante MG & Espírito Santo</div>
            <div style="font-size: 24px; font-weight: 900; color: #34D399; margin-top: 10px;">R$ 168.420,00</div>
            <div style="font-size: 11px; color: #94A3B8; font-weight: 700; margin-top: 2px;">99.1% da Meta (R$ 170.000)</div>
            <div style="font-size: 11px; color: #94A3B8; margin-top: 6px;">💰 Comissão Estimada: <b>R$ 6.736,80</b></div>
        </div>
        """, unsafe_allow_html=True)
    with col_p3:
        st.markdown("""
        <div class="metric-card" style="border: 2px solid #B45309; text-align: center;">
            <div style="font-size: 38px;">🥉</div>
            <div style="font-size: 18px; font-weight: 800; color: #F59E0B;">Camila Duarte</div>
            <div style="font-size: 11px; color: #CBD5E1;">Representante Sul (PR / SC / RS)</div>
            <div style="font-size: 24px; font-weight: 900; color: #34D399; margin-top: 10px;">R$ 138.900,00</div>
            <div style="font-size: 11px; color: #F59E0B; font-weight: 700; margin-top: 2px;">92.6% da Meta (R$ 150.000)</div>
            <div style="font-size: 11px; color: #94A3B8; margin-top: 6px;">💰 Comissão Estimada: <b>R$ 5.556,00</b></div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 5. RASTREAMENTO & LOGÍSTICA
# ══════════════════════════════════════════════════════════════════════════════
elif "Rastreamento" in pagina:
    st.info("💡 **Dica de Apresentação:** A Torre de Controle Logístico rastreia CTEs e NFs automaticamente com Braspress, SSW e Correios, evitando que o comercial perca horas no WhatsApp perguntando onde está a carga!")
    
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">ENVIOS EM TRÂNSITO</div>
            <div class="metric-val" style="color: #60A5FA;">18 Cargas</div>
            <div class="metric-badge" style="background: rgba(96, 165, 250, 0.2); color: #60A5FA;">100% no prazo SLA</div>
        </div>
        """, unsafe_allow_html=True)
    with col_t2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">ENTREGUES NESTA SEMANA</div>
            <div class="metric-val" style="color: #34D399;">42 Cargas</div>
            <div class="metric-badge" style="background: rgba(16, 185, 129, 0.2); color: #34D399;">Comprovante Digital OK</div>
        </div>
        """, unsafe_allow_html=True)
    with col_t3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">SLA DE EXPEDIÇÃO ARMAZÉM</div>
            <div class="metric-val" style="color: #C084FC;">4.2 horas</div>
            <div class="metric-badge" style="background: rgba(192, 132, 252, 0.2); color: #C084FC;">Da NFe ao Carregamento</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("#### 🚚 Cargas Monitoradas em Tempo Real:")
    cargas = [
        {"CTE": "CTE-84920", "Transportadora": "Braspress Rodoviário", "Cliente / Destino": "Drogaria Brasil (São Paulo - SP)", "Status": "Em Trânsito (Rota Campinas)", "Previsão": "Amanhã 14:00", "Volume": "12 Caixas Padrão"},
        {"CTE": "CTE-84918", "Transportadora": "SSW Transportes", "Cliente / Destino": "Clínica Bella Pelle (Rio de Janeiro - RJ)", "Status": "Saiu para Entrega ao Destinatário", "Previsão": "Hoje até 18:00", "Volume": "4 Caixas Padrão"},
        {"CTE": "CTE-84915", "Transportadora": "Braspress Rodoviário", "Cliente / Destino": "Rede Farmavida (Belo Horizonte - MG)", "Status": "Entregue com Sucesso", "Previsão": "Finalizado", "Volume": "18 Caixas Padrão"},
        {"CTE": "CTE-84910", "Transportadora": "Sedex Express", "Cliente / Destino": "Emporium Estética (Curitiba - PR)", "Status": "Em Trânsito para o CD Curitiba", "Previsão": "16/11/2026", "Volume": "2 Caixas Pequenas"}
    ]
    st.dataframe(pd.DataFrame(cargas), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# 6. RADAR DE CLIENTES & CHURN (IA DE RECOMPRA)
# ══════════════════════════════════════════════════════════════════════════════
elif "Radar" in pagina:
    st.info("💡 **Dica de Apresentação:** Este é o módulo favorito dos Diretores. A IA detecta quais clientes compram a cada 30 dias e alerta antes que o cliente vá comprar do concorrente!")
    
    alertas_churn = [
        {"Cliente": "BioEstética Clínicas Integradas (GO)", "Última Compra": "Há 74 dias", "Frequência Habitual": "A cada 25 dias", "Risco": "🔴 CHURN CRÍTICO", "Ticket Médio": "R$ 14.500,00", "Ação Comercial Sugerida": "Ofertar Condição Especial em Lote de Peeling"},
        {"Cliente": "Emporium Estética & Spa Curitiba (PR)", "Última Compra": "Há 48 dias", "Frequência Habitual": "A cada 30 dias", "Risco": "🟠 ALERTA DE RECOMPRA", "Ticket Médio": "R$ 18.200,00", "Ação Comercial Sugerida": "Disparar Catálogo de Novidades e Kit Cabine"},
        {"Cliente": "Cosméticos & Cia Atacadista do ES (ES)", "Última Compra": "Há 22 dias", "Frequência Habitual": "A cada 20 dias", "Risco": "🟡 REABASTECIMENTO", "Ticket Médio": "R$ 22.000,00", "Ação Comercial Sugerida": "Conferir estoque de Protetor Solar FPS 70"}
    ]
    st.dataframe(pd.DataFrame(alertas_churn), use_container_width=True, hide_index=True)
    
    st.markdown("#### 📲 Ação Imediata de Reativação no WhatsApp:")
    col_w1, col_w2 = st.columns([8, 4])
    with col_w1:
        st.text_area("Mensagem Automática Sugerida pela IA do Omnievo:", 
                     "Olá Dra. Juliana! Notamos que seu estoque de Peeling Mandélico e Séruns Faciais da BioEstética está no ciclo de reposição. Conseguimos liberar para o seu pedido desta semana a condição especial de 42 dias no boleto sem juros com frete cortesia! Gostaria que eu reservasse seu lote?")
    with col_w2:
        st.write("")
        st.write("")
        if st.button("📲 Enviar Mensagem via WhatsApp Web", use_container_width=True):
            st.success("✨ Mensagem preparada para o vendedor disparar com 1 toque no WhatsApp!")

# ══════════════════════════════════════════════════════════════════════════════
# 7. ESTOQUE & VALIDADES (FEFO)
# ══════════════════════════════════════════════════════════════════════════════
elif "Estoque" in pagina:
    st.info("💡 **Dica de Apresentação:** Empresas de cosméticos e saúde precisam controlar rigorosamente validade (FEFO - Primeiro que Vence é o Primeiro que Sai) para não perder produtos no galpão!")
    
    col_e1, col_e2, col_e3 = st.columns(3)
    with col_e1:
        st.metric("Itens Ativos no Catálogo", f"{len(st.session_state['catalogo'])} SKUs", "100% Sincronizados")
    with col_e2:
        st.metric("Valor Total em Estoque (Custo)", "R$ 842.150,00", "Auditoria OK")
    with col_e3:
        st.metric("Itens Próximos ao Ponto de Pedido", "2 SKUs", "Reposição Solicitada")
        
    st.markdown("#### 📋 Tabela Geral de Estoque, Lotes e Validades:")
    df_est = pd.DataFrame(st.session_state["catalogo"])
    st.dataframe(df_est, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# 8. CADASTRAR CLIENTE
# ══════════════════════════════════════════════════════════════════════════════
elif "Cadastrar" in pagina:
    st.info("💡 **Dica de Apresentação:** O cadastro é limpo e rápido. A validação de CEP e CNPJ puxa os dados automaticamente, evitando erros de faturamento no Omie ERP!")
    
    with st.form("form_cad_cli"):
        col_cad1, col_cad2 = st.columns(2)
        with col_cad1:
            nome_novo = st.text_input("Razão Social / Nome Fantasia:", placeholder="Ex: Drogaria Dermavita Ltda")
            cnpj_novo = st.text_input("CNPJ:", placeholder="00.000.000/0001-00")
            ie_novo = st.text_input("Inscrição Estadual:", placeholder="Isento ou Número da IE")
        with col_cad2:
            cep_novo = st.text_input("CEP:", value="01310-100")
            cidade_uf = st.text_input("Cidade / UF:", value="São Paulo - SP")
            vendedor_resp = st.selectbox("Vendedor Responsável:", ["Gabriel Santos", "Lucas Mendes", "Camila Duarte", "Rafael Costa"])
            
        sub_cad = st.form_submit_button("💾 Gravar Cliente no CRM & Omie ERP", use_container_width=True)
        if sub_cad:
            if nome_novo:
                st.session_state["clientes"].append({
                    "id": random.randint(200, 999),
                    "nome": nome_novo,
                    "cnpj": cnpj_novo or "33.444.555/0001-99",
                    "uf": cidade_uf.split("-")[-1].strip() if "-" in cidade_uf else "SP",
                    "cidade": cidade_uf.split("-")[0].strip() if "-" in cidade_uf else "São Paulo",
                    "vendedor": vendedor_resp,
                    "limite": 50000.0,
                    "status": "Ativo",
                    "prazo": "28/35 dias",
                    "dias_sem_comprar": 0
                })
                st.success(f"✨ Cliente '{nome_novo}' cadastrado com sucesso e sincronizado no ERP!")
            else:
                st.warning("Por favor, informe a Razão Social do cliente.")
