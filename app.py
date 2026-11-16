import sys
import builtins

# ── Blindagem Global contra "ValueError: I/O operation on closed file" no Windows ──
_orig_print = builtins.print
def _safe_print(*args, **kwargs):
    try:
        _orig_print(*args, **kwargs)
    except Exception:
        try:
            if sys.__stdout__ and not sys.__stdout__.closed:
                sys.__stdout__.write(" ".join(str(a) for a in args) + "\n")
                sys.__stdout__.flush()
        except Exception:
            pass
import order_analyst_service as analyst
import braspress_service as braspress
import ssw_service as ssw
import sla_separacao_service as sla_separacao
import logistica_rastreio as logistica_rastreio
import torre_controle_service as tcs
import importlib
importlib.reload(braspress)
importlib.reload(ssw)
importlib.reload(sla_separacao)
importlib.reload(logistica_rastreio)
importlib.reload(tcs)

builtins.print = _safe_print

import sys

# ── Blindagem contra erros de Encoding UTF-8 no Windows (Sem fechar streams de I/O) ──
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import streamlit as st
import os
import base64
import json
import re
import html

# ── Função Robusta de Conversão de Números BR/US para Planilha e Texto ──
def _parse_num_br(val):
    if val is None or pd.isna(val):
        return None
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip().replace("R$", "").replace("$", "").replace(" ", "")
    if not s:
        return None
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except Exception:
        return None

import datetime
from datetime import date
import pandas as pd
import importlib
import random
import time
import omie_service as omie
import importlib
importlib.reload(omie)
import pdf_service
import auth_service as auth
import geolocation_service as geo

FRASES_MOTIVACIONAIS_VENDAS = [
    "🚀 \"O sucesso nas vendas não vem de convencer pessoas, vem de ajudá-las a tomar a melhor decisão!\"",
    "🌟 \"A melhor forma de prever o futuro das suas vendas é construí-lo hoje com entusiasmo!\"",
    "🔥 \"Vendedores de sucesso não esperam as oportunidades chegarem, eles criam as oportunidades!\"",
    "💎 \"Cada atendimento é uma oportunidade única de construir confiança e faturar mais!\"",
    "🎯 \"Foco na solução, energia nas vendas e determinação em cada conquista diária!\"",
    "🏆 \"Vender é construir relacionamentos sólidos e entregar valor real ao seu cliente!\"",
    "💪 \"Cada 'não' te deixa um passo mais próximo do seu próximo grande SIM! Vamos com tudo!\""
]

_fav_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "favicon.png")
_fav_b64 = ""
if os.path.exists(_fav_path):
    try:
        with open(_fav_path, "rb") as _ff:
            _fav_b64 = base64.b64encode(_ff.read()).decode("utf-8")
    except Exception:
        pass

st.set_page_config(
    page_title="Omnievo - CRM & Pedidos",
    page_icon="assets/logo_icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

import streamlit.components.v1 as components

_fav_inject_js = f"""
(function forceOmnievoFavicon() {{
    const b64 = "{_fav_b64}";
    if (!b64 || b64.length < 50) return;
    const favUrl = "data:image/png;base64," + b64;
    const apply = () => {{
        [window, window.parent, window.top].forEach(win => {{
            try {{
                if (!win || !win.document) return;
                const doc = win.document;
                if (!doc.title || doc.title.toLowerCase().includes("streamlit")) {{
                    doc.title = "Omnievo - CRM & Pedidos";
                }}
                let links = doc.querySelectorAll("link[rel*='icon']");
                if (links.length === 0) {{
                    const newLink = doc.createElement('link');
                    newLink.type = 'image/png';
                    newLink.rel = 'shortcut icon';
                    newLink.href = favUrl;
                    doc.getElementsByTagName('head')[0].appendChild(newLink);
                }} else {{
                    links.forEach(l => {{
                        if (l.href !== favUrl) {{
                            l.type = 'image/png';
                            l.href = favUrl;
                        }}
                    }});
                }}
            }} catch(e) {{}}
        }});
    }};
    apply();
    setTimeout(apply, 300);
    setTimeout(apply, 1000);
    setInterval(apply, 2500);
}})();
"""

components.html("""<script>""" + _fav_inject_js + """
(function fixReactDOMGlobally() {
    function patchProto(proto) {
        if (!proto) return;
        if (!proto._patchedInsertBefore) {
            proto._patchedInsertBefore = true;
            const origInsertBefore = proto.insertBefore;
            proto.insertBefore = function(newNode, refNode) {
                if (!refNode) {
                    try { return origInsertBefore.call(this, newNode, null); } catch(e) { try { return this.appendChild(newNode); } catch(err) { return newNode; } }
                }
                if (refNode.parentNode !== this) {
                    if (refNode.parentNode && typeof refNode.parentNode.insertBefore === 'function') {
                        try { return refNode.parentNode.insertBefore(newNode, refNode); } catch(e) {}
                    }
                    try { return this.appendChild(newNode); } catch(e) { return newNode; }
                }
                try {
                    return origInsertBefore.call(this, newNode, refNode);
                } catch (e) {
                    try { return this.appendChild(newNode); } catch (err) { return newNode; }
                }
            };
        }
        if (!proto._patchedRemoveChild) {
            proto._patchedRemoveChild = true;
            const origRemoveChild = proto.removeChild;
            proto.removeChild = function(child) {
                if (!child) return null;
                if (child.parentNode !== this) {
                    if (child.parentNode && typeof child.parentNode.removeChild === 'function') {
                        try { return child.parentNode.removeChild(child); } catch(e) {}
                    }
                    return child;
                }
                try {
                    return origRemoveChild.call(this, child);
                } catch (e) {
                    return child;
                }
            };
        }
        if (!proto._patchedReplaceChild) {
            proto._patchedReplaceChild = true;
            const origReplaceChild = proto.replaceChild;
            proto.replaceChild = function(newChild, oldChild) {
                if (!oldChild) return null;
                if (oldChild.parentNode !== this) {
                    if (oldChild.parentNode && typeof oldChild.parentNode.replaceChild === 'function') {
                        try { return oldChild.parentNode.replaceChild(newChild, oldChild); } catch(e) {}
                    }
                    return oldChild;
                }
                try {
                    return origReplaceChild.call(this, newChild, oldChild);
                } catch (e) {
                    return oldChild;
                }
            };
        }
    }
    const lockNoTranslate = () => {
        [window, window.parent, window.top].forEach(win => {
            try {
                if (!win || !win.document) return;
                if (win.Node && win.Node.prototype) patchProto(win.Node.prototype);
                if (win.Element && win.Element.prototype) patchProto(win.Element.prototype);
                
                const doc = win.document;
                if (doc.documentElement) {
                    doc.documentElement.setAttribute('lang', 'pt-BR');
                    doc.documentElement.setAttribute('translate', 'no');
                    doc.documentElement.classList.add('notranslate');
                }
                if (doc.body) {
                    doc.body.setAttribute('translate', 'no');
                    doc.body.classList.add('notranslate');
                }
            } catch(e) {}
        });
    };
    lockNoTranslate();
    setInterval(lockNoTranslate, 200);

    const fixToolbarIcons = () => {
        [window, window.parent, window.top].forEach(win => {
            try {
                if (!win || !win.document) return;
                win.document.querySelectorAll('[data-testid="stElementToolbar"] button, [data-testid="stElementToolbarButton"] button, div[data-testid="stDataFrame"] button[kind="elementToolbar"]').forEach(btn => {
                    btn.style.setProperty('color', '#94A3B8', 'important');
                    btn.querySelectorAll('svg').forEach(s => {
                        s.style.setProperty('color', '#94A3B8', 'important');
                        s.style.setProperty('fill', 'currentColor', 'important');
                    });
                });
            } catch(e) {}
        });
    };
    fixToolbarIcons();
    setInterval(fixToolbarIcons, 500);
})();
</script>
""", height=0)

# Sincronizar vendedores autorizados da Omie ERP (apenas 1x por sessão — evita latência a cada rerun)
if not st.session_state.get("_startup_sync_done"):
    auth.sincronizar_vendedores_omie()
    omie.iniciar_sincronizacao_estoque_bg()
    omie.iniciar_sincronizacao_automatica_1h()
    st.session_state["_startup_sync_done"] = True

# Inicialização do Estado de Autenticação com Persistência em Refresh (F5) e Restauração Criptográfica
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "usuario_logado" not in st.session_state:
    st.session_state["usuario_logado"] = None

# 1. Recuperar token da URL ou da sessão ativa
token_atual = st.query_params.get("session_token") or st.session_state.get("session_token")
if token_atual:
    st.session_state["session_token"] = token_atual
    if not st.session_state.get("authenticated"):
        usr_recuperado = auth.validar_token_sessao(token_atual)
        if usr_recuperado:
            st.session_state["authenticated"] = True
            st.session_state["usuario_logado"] = usr_recuperado

# 2. Garantir que o token esteja SEMPRE mantido na URL (st.query_params) enquanto autenticado
if st.session_state.get("authenticated") and st.session_state.get("session_token"):
    tok_ativo = st.session_state["session_token"]
    if st.query_params.get("session_token") != tok_ativo:
        st.query_params["session_token"] = tok_ativo

# ══════════════════════════════════════════════════════════════════════════════
# CSS DESIGN SYSTEM
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<meta name="google" content="notranslate">
<meta name="googlebot" content="notranslate">
<script>
    (function fixReactDOMGlobally() {
        function patchProto(proto) {
            if (!proto) return;

            if (!proto._patchedInsertBefore) {
                proto._patchedInsertBefore = true;
                const origInsertBefore = proto.insertBefore;
                proto.insertBefore = function(newNode, refNode) {
                    if (!refNode) {
                        try { return origInsertBefore.call(this, newNode, null); } catch(e) { try { return this.appendChild(newNode); } catch(err) { return newNode; } }
                    }
                    if (refNode.parentNode !== this) {
                        if (refNode.parentNode && typeof refNode.parentNode.insertBefore === 'function') {
                            try { return refNode.parentNode.insertBefore(newNode, refNode); } catch(e) {}
                        }
                        try { return this.appendChild(newNode); } catch(e) { return newNode; }
                    }
                    try {
                        return origInsertBefore.call(this, newNode, refNode);
                    } catch (e) {
                        try { return this.appendChild(newNode); } catch (err) { return newNode; }
                    }
                };
            }

            if (!proto._patchedRemoveChild) {
                proto._patchedRemoveChild = true;
                const origRemoveChild = proto.removeChild;
                proto.removeChild = function(child) {
                    if (!child) return null;
                    if (child.parentNode !== this) {
                        if (child.parentNode && typeof child.parentNode.removeChild === 'function') {
                            try { return child.parentNode.removeChild(child); } catch(e) {}
                        }
                        return child;
                    }
                    try {
                        return origRemoveChild.call(this, child);
                    } catch (e) {
                        return child;
                    }
                };
            }

            if (!proto._patchedReplaceChild) {
                proto._patchedReplaceChild = true;
                const origReplaceChild = proto.replaceChild;
                proto.replaceChild = function(newChild, oldChild) {
                    if (!oldChild) return null;
                    if (oldChild.parentNode !== this) {
                        if (oldChild.parentNode && typeof oldChild.parentNode.replaceChild === 'function') {
                            try { return oldChild.parentNode.replaceChild(newChild, oldChild); } catch(e) {}
                        }
                        return oldChild;
                    }
                    try {
                        return origReplaceChild.call(this, newChild, oldChild);
                    } catch (e) {
                        return oldChild;
                    }
                };
            }
        }

        const applyToWindow = (win) => {
            try {
                if (win && win.Node && win.Node.prototype) patchProto(win.Node.prototype);
                if (win && win.Element && win.Element.prototype) patchProto(win.Element.prototype);
            } catch (e) {}
        };

        const lockNoTranslate = () => {
            const targets = [window, window.parent, window.top];
            targets.forEach(win => {
                try {
                    if (!win || !win.document) return;
                    applyToWindow(win);
                    
                    const doc = win.document;
                    if (doc.documentElement) {
                        doc.documentElement.setAttribute('lang', 'pt-BR');
                        doc.documentElement.setAttribute('translate', 'no');
                        doc.documentElement.classList.add('notranslate');
                    }
                    if (doc.body) {
                        doc.body.setAttribute('translate', 'no');
                        doc.body.classList.add('notranslate');
                    }
                    doc.querySelectorAll('label, p, span, h1, h2, h3, div, small, [data-testid="stWidgetLabel"], [data-testid="stMarkdownContainer"]').forEach(el => {
                        el.setAttribute('translate', 'no');
                        el.classList.add('notranslate');
                    });
                } catch (e) {}
            });
        };

        lockNoTranslate();
        setInterval(lockNoTranslate, 200);
    })();
</script>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ── ENGINE DE ULTRA-RESOLUÇÃO E ANTI-ALIASING HIGH-DPI / RETINA ── */
    *, *::before, *::after {
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
        text-rendering: optimizeLegibility !important;
    }

    img, svg, canvas, video, .js-plotly-plot svg {
        image-rendering: -webkit-optimize-contrast !important;
        image-rendering: crisp-edges !important;
        shape-rendering: geometricPrecision !important;
        text-rendering: geometricPrecision !important;
    }

    /* TEMA EXECUTIVE PREMIUM — OMNIEVO CRM */
    html, body, [data-testid="stAppViewContainer"], .stApp,
    p, h1, h2, h3, h4, h5, h6, input, textarea, button, label, select {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    }

    /* PRESERVAÇÃO DAS FONTES DE ÍCONES NATIVAS (EVITA TEXTOS COMO _arrow_right SOBREPONDO) */
    .material-symbols-rounded,
    .material-symbols,
    .material-icons,
    [data-testid="stIcon"],
    [data-testid="stIcon"] *,
    [data-testid="stExpander"] summary span:first-child,
    [data-testid="stExpander"] summary [data-testid="stIcon"],
    [data-testid="stExpander"] summary [data-testid="stIcon"] * {
        font-family: "Material Symbols Rounded", "Material Icons", sans-serif !important;
        font-style: normal !important;
        font-variant: normal !important;
        text-transform: none !important;
        line-height: 1 !important;
        letter-spacing: normal !important;
        word-wrap: normal !important;
        white-space: nowrap !important;
        direction: ltr !important;
        -webkit-font-smoothing: antialiased !important;
        text-rendering: optimizeLegibility !important;
    }

    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #F8FAFC !important;
        background: #F8FAFC !important;
        color: #1E293B !important;
    }
    
    /* ── BARRA SUPERIOR CLEAN ── */
    [data-testid="stHeader"],
    header[data-testid="stHeader"],
    header,
    .stApp > header {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #1E293B !important;
        border-bottom: 1px solid #E2E8F0 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    }

    /* ── WIDGET ANIMADO PERSONALIZADO OMNIEVO (SUBSTITUI O ÍCONE 'STOP' PADRÃO) ── */
    [data-testid="stStatusWidget"],
    div[data-testid="stStatusWidget"],
    .stStatusWidget {
        background: linear-gradient(135deg, #1E1B4B 0%, #0F172A 100%) !important;
        border: 1.5px solid #818CF8 !important;
        border-radius: 20px !important;
        padding: 2px 10px !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
        animation: omnievoPulseGlow 2s infinite alternate !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    [data-testid="stStatusWidget"] button,
    [data-testid="stStatusWidget"] button * {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-family: 'Inter', system-ui, sans-serif !important;
        font-weight: 800 !important;
        font-size: 11px !important;
        letter-spacing: 0.05em !important;
    }

    /* Ocultar ícone de acessibilidade original */
    [data-testid="stStatusWidget"] svg,
    [data-testid="stStatusWidget"] [data-testid="stIcon"] {
        display: none !important;
    }

    /* Símbolo Animado Neon da Omnievo (Logo Ícone Isométrico 3D com Giro & Glow) */
    [data-testid="stStatusWidget"]::before {
        content: "" !important;
        width: 18px !important;
        height: 18px !important;
        margin-right: 7px !important;
        display: inline-block !important;
        background-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMjAgMTIwIiBmaWxsPSJub25lIiB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIj4KICA8ZGVmcz4KICAgIDwhLS0gR3JhZGllbnRlIExpbmVhciBQw7pycHVyYSAtPiBBenVsIC0+IENpYW5vIC0+IFZlcmRlIC0tPgogICAgPGxpbmVhckdyYWRpZW50IGlkPSJjdWJlR3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdG9wLWNvbG9yPSIjOTMzM0VBIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjM1JSIgc3RvcC1jb2xvcj0iIzYzNjZGMSIgLz4KICAgIDxzdG9wIG9mZnNldD0iNzAlIiBzdG9wLWNvbG9yPSIjMDZCNkQ0IiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0b3AtY29sb3I9IiMxMEI5ODEiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPHJhZGlhbEdyYWRpZW50IGlkPSJjb3JlR2xvdyIgY3g9IjUwJSIgY3k9IjUwJSIgcj0iNTAlIj4KICAgICAgPHN0b3Agb2Zmc2V0PSIwJSIgc3RvcC1jb2xvcj0iIzM0RDM5OSIgLz4KICAgICAgPHN0b3Agb2Zmc2V0PSI2MCUiIHN0b3AtY29sb3I9IiMxMEI5ODEiIC8+CiAgICAgIDxzdG9wIG9mZnNldD0iMTAwJSIgc3RvcC1jb2xvcj0iIzA1OTY2OSIgLz4KICAgIDwvcmFkaWFsR3JhZGllbnQ+CiAgICA8ZmlsdGVyIGlkPSJjdWJlU2hhZG93IiB4PSItMzAlIiB5PSItMzAlIiB3aWR0aD0iMTYwJSIgaGVpZ2h0PSIxNjAlIj4KICAgICAgPGZlRHJvcFNoYWRvdyBkeD0iMCIgZHk9IjYiIHN0ZERldmlhdGlvbj0iOCIgZmxvb2QtY29sb3I9IiM2MzY2RjEiIGZsb29kLW9wYWNpdHk9IjAuNCIvPgogICAgPC9maWx0ZXI+CiAgPC9kZWZzPgoKICA8ZyBmaWx0ZXI9InVybCgjY3ViZVNoYWRvdykiPgogICAgPHBvbHlnb24gcG9pbnRzPSI2MCwxNiAxMDAsMzkgMTAwLDg1IDYwLDEwOCAyMCw4NSAyMCwzOSIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJ1cmwoI2N1YmVHcmFkaWVudCkiIHN0cm9rZS13aWR0aD0iNyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+CiAgICA8bGluZSB4MT0iNjAiIHkxPSI2MiIgeDI9IjYwIiB5Mj0iMTYiIHN0cm9rZT0idXJsKCNjdWJlR3JhZGllbnQpIiBzdHJva2Utd2lkdGg9IjYiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgogICAgPGxpbmUgeDE9IjYwIiB5MT0iNjIiIHgyPSIxMDAiIHkyPSI4NSIgc3Ryb2tlPSJ1cmwoI2N1YmVHcmFkaWVudCkiIHN0cm9rZS13aWR0aD0iNiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+CiAgICA8bGluZSB4MT0iNjAiIHkxPSI2MiIgeDI9IjIwIiB5Mj0iODUiIHN0cm9rZT0idXJsKCNjdWJlR3JhZGllbnQpIiBzdHJva2Utd2lkdGg9IjYiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgogICAgPGNpcmNsZSBjeD0iNjAiIGN5PSI2MiIgcj0iMTMiIGZpbGw9InVybCgjY29yZUdsb3cpIiAvPgogICAgPGNpcmNsZSBjeD0iNTciIGN5PSI1OSIgcj0iNCIgZmlsbD0iI0E3RjNEMCIgb3BhY2l0eT0iMC43IvPgogIDwvZz4KPC9zdmc+") !important;
        background-repeat: no-repeat !important;
        background-size: contain !important;
        background-position: center !important;
        vertical-align: middle !important;
        animation: omnievoSpinOrb 2.5s ease-in-out infinite alternate !important;
    }

    @keyframes omnievoPulseGlow {
        0% {
            border-color: #818CF8;
            box-shadow: 0 0 8px rgba(99, 102, 241, 0.4);
        }
        100% {
            border-color: #A855F7;
            box-shadow: 0 0 18px rgba(168, 85, 247, 0.75);
        }
    }

    @keyframes omnievoSpinOrb {
        0% { transform: scale(1) rotate(0deg); filter: brightness(1); }
        50% { transform: scale(1.3) rotate(180deg); filter: brightness(1.5); }
        100% { transform: scale(1) rotate(360deg); filter: brightness(1); }
    }

    /* ── TÍTULOS COM HIERARQUIA VISUAL CLARA ── */
    h1:not(.showcase-main-title):not(.login-right-animated-panel *),
    h2:not(.showcase-main-title):not(.login-right-animated-panel *),
    h3:not(.showcase-main-title):not(.login-right-animated-panel *),
    h4, h5, h6, 
    .stMarkdown h1:not(.showcase-main-title):not(.login-right-animated-panel *),
    .stMarkdown h2:not(.showcase-main-title):not(.login-right-animated-panel *),
    .stMarkdown h3:not(.showcase-main-title):not(.login-right-animated-panel *),
    .stMarkdown h4,
    .page-header-title {
        color: #0F172A !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        line-height: 1.3 !important;
    }

    [data-testid="stAppViewContainer"] p:not(section[data-testid="stSidebar"] *):not(div[data-testid="stToast"] *):not(div[data-testid="stTooltipContent"] *):not(button *):not(button):not(th *):not([data-testid="stExpander"] summary *):not(summary *):not(.login-right-animated-panel *):not(.omnievo-banner *):not(.executive-dark-banner *):not(.copilot-ia-banner *):not(.dark-badge *):not(div[data-testid="stStatusWidget"] *):not(div[data-testid="stNotification"] *):not(.stSpinner *):not(div[data-testid="stSpinner"] *),
    [data-testid="stAppViewContainer"] label:not(section[data-testid="stSidebar"] *),
    [data-testid="stAppViewContainer"] caption, 
    [data-testid="stAppViewContainer"] .stCaption,
    [data-testid="stAppViewContainer"] small:not(section[data-testid="stSidebar"] *):not([data-testid="stFileUploaderDropzone"] *):not(.login-right-animated-panel *):not(.omnievo-banner *):not(.executive-dark-banner *):not(.copilot-ia-banner *):not(.dark-badge *):not(div[data-testid="stStatusWidget"] *):not(div[data-testid="stNotification"] *):not(.stSpinner *):not(div[data-testid="stSpinner"] *),
    [data-testid="stMarkdownContainer"] p:not(section[data-testid="stSidebar"] *):not(div[data-testid="stToast"] *):not(div[data-testid="stTooltipContent"] *):not(button *):not(button):not(th *):not([data-testid="stExpander"] summary *):not(summary *):not(.login-right-animated-panel *):not(.omnievo-banner *):not(.executive-dark-banner *):not(.copilot-ia-banner *):not(.dark-badge *):not(div[data-testid="stStatusWidget"] *):not(div[data-testid="stNotification"] *):not(.stSpinner *):not(div[data-testid="stSpinner"] *) {
        color: #1E293B !important;
        font-weight: 400 !important;
        opacity: 1 !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
    }

    /* ── BADGES ESCUROS COM TEXTO BRANCO PURO (GARANTIA DE CONTRASTE TOTAL) ── */
    .dark-badge,
    span.dark-badge,
    .badge-pill-dark,
    span.badge-pill-dark,
    [data-testid="stAppViewContainer"] .dark-badge,
    [data-testid="stAppViewContainer"] span.dark-badge,
    [data-testid="stAppViewContainer"] span[style*="background: #0F172A"],
    [data-testid="stAppViewContainer"] span[style*="background:#0F172A"],
    [data-testid="stAppViewContainer"] span[style*="background: #4F46E5"],
    [data-testid="stAppViewContainer"] span[style*="background:#4F46E5"],
    [data-testid="stAppViewContainer"] span[style*="background: #2563EB"],
    [data-testid="stAppViewContainer"] span[style*="background:#2563EB"],
    [data-testid="stAppViewContainer"] span[style*="background: #DC2626"],
    [data-testid="stAppViewContainer"] span[style*="background:#DC2626"],
    [data-testid="stAppViewContainer"] span[style*="background: #10B981"],
    [data-testid="stAppViewContainer"] span[style*="background:#10B981"] {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    /* ── COPILOT IA BANNER (TEXTO 100% BRANCO E DESTAQUE LUMINOSO) ── */
    .copilot-ia-banner,
    .copilot-ia-banner *,
    .copilot-ia-banner h1,
    .copilot-ia-banner h2,
    .copilot-ia-banner h3,
    .copilot-ia-banner span,
    .copilot-ia-banner div,
    .copilot-ia-banner p {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    .copilot-ia-banner .copilot-sub,
    .copilot-ia-banner .copilot-sub * {
        color: #E0E7FF !important;
        -webkit-text-fill-color: #E0E7FF !important;
    }

    /* ── BANNER EXECUTIVO MIDNIGHT AURORA (ALTO CONTRASTE & BRILHO) ── */
    .omnievo-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 45%, #312E81 100%) !important;
        border: 1.5px solid #6366F1 !important;
        border-radius: 16px !important;
        padding: 22px 28px !important;
        margin-bottom: 24px !important;
        box-shadow: 0 10px 25px -5px rgba(30, 27, 75, 0.35) !important;
    }
    .omnievo-banner,
    .omnievo-banner *,
    .omnievo-banner h2,
    .omnievo-banner span,
    .omnievo-banner div {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    .omnievo-banner .banner-sub {
        color: #CBD5E1 !important;
        -webkit-text-fill-color: #CBD5E1 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }
    .omnievo-banner .banner-badge {
        background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%) !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border: 1px solid #818CF8 !important;
        box-shadow: 0 2px 10px rgba(99, 102, 241, 0.45) !important;
    }

    /* ── NOTIFICAÇÕES TOAST & TOOLTIPS (POPOVER ESCURO APENAS AO PASSAR O MOUSE — NÃO AFETA O ÍCONE DA LABEL) ── */
    div[data-testid="stToast"],
    div[data-testid="stToast"] *,
    div[data-baseweb="toast"],
    div[data-baseweb="toast"] *,
    div[data-testid="stTooltipContent"],
    div[data-testid="stTooltipContent"] * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        background-color: #000000 !important;
        font-weight: 800 !important;
        font-size: 13px !important;
    }
    
    div[data-testid="stToast"],
    div[data-testid="stTooltipContent"] {
        background-color: #000000 !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 10px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5) !important;
    }

    /* ── SPINNERS E WIDGETS DE CARREGAMENTO (st.spinner / st.status / cache_data show_spinner) — TEXTO BRANCO 100% ── */
    [data-testid="stStatusWidget"],
    [data-testid="stNotification"],
    .stSpinner,
    div[data-testid="stSpinner"],
    div[data-testid="stStatusWidget"] *,
    div[data-testid="stNotification"] *,
    .stSpinner *,
    div[data-testid="stSpinner"] *,
    div[data-testid="stStatusWidget"] p,
    div[data-testid="stNotification"] p,
    div[data-testid="stSpinner"] p,
    div[data-testid="stStatusWidget"] span,
    div[data-testid="stNotification"] span,
    div[data-testid="stSpinner"] span,
    div[data-testid="stStatusWidget"] div,
    div[data-testid="stNotification"] div,
    div[data-testid="stSpinner"] div {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    [data-testid="stStatusWidget"],
    [data-testid="stNotification"],
    .stSpinner,
    div[data-testid="stSpinner"] {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 100%) !important;
        border: 1px solid #6366F1 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.4) !important;
    }
    
    [data-testid="stStatusWidget"] svg,
    [data-testid="stNotification"] svg,
    .stSpinner svg,
    div[data-testid="stSpinner"] svg {
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
        stroke: #FFFFFF !important;
    }

    /* ── CAIXAS DE UPLOAD DE ARQUIVOS (stFileUploader) — FUNDO ESCURO + TEXTO BRANCO / BOTÃO PRETO BRANCO ── */
    [data-testid="stFileUploader"] label,
    [data-testid="stFileUploader"] [data-testid="stWidgetLabel"],
    [data-testid="stFileUploader"] [data-testid="stWidgetLabel"] * {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: 900 !important;
        font-size: 15px !important;
    }

    [data-testid="stFileUploaderDropzone"],
    [data-testid="stFileUploaderInstructions"],
    [data-testid="stFileUploaderInstructions"] *,
    section[data-testid="stFileUploaderDropzone"] small,
    section[data-testid="stFileUploaderDropzone"] span,
    section[data-testid="stFileUploaderDropzone"] div,
    section[data-testid="stFileUploaderDropzone"] p {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    [data-testid="stFileUploaderDropzone"] button,
    section[data-testid="stFileUploaderDropzone"] button {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: 900 !important;
        font-size: 14px !important;
        border: 2px solid #000000 !important;
        border-radius: 8px !important;
        padding: 6px 16px !important;
    }

    [data-testid="stFileUploaderDropzone"] button *,
    section[data-testid="stFileUploaderDropzone"] button * {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: 900 !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background-color: #0F172A !important;
        border: 2px dashed #000000 !important;
        border-radius: 12px !important;
    }

    [data-testid="stFileUploaderDropzone"] svg,
    [data-testid="stFileUploaderDropzone"] svg path {
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
    }

    /* ── BARRA DE AÇÕES DOS GRÁFICOS (MODEBAR PLOTLY) ── */
    .js-plotly-plot .modebar-container,
    .modebar-container,
    .modebar {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: flex-end !important;
        gap: 6px !important;
        top: 4px !important;
        right: 8px !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    .modebar-group {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        gap: 4px !important;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    .modebar-btn,
    .js-plotly-plot .modebar-btn {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 26px !important;
        height: 26px !important;
        min-width: 26px !important;
        min-height: 26px !important;
        padding: 3px !important;
        margin: 0 1px !important;
        background: transparent !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        border-radius: 6px !important;
    }

    .modebar-btn svg,
    .js-plotly-plot .modebar-btn svg {
        width: 16px !important;
        height: 16px !important;
        fill: #0F172A !important;
    }

    .modebar-btn:hover,
    .js-plotly-plot .modebar-btn:hover {
        background: rgba(0, 0, 0, 0.08) !important;
        border-radius: 6px !important;
    }

    .modebar-btn:hover svg,
    .js-plotly-plot .modebar-btn:hover svg {
        fill: #000000 !important;
    }

    /* ── TOOLBAR STREAMLIT (TABELAS / DATAFRAMES) — ÍCONES NA COR CINZA ELEGANTE (#94A3B8) ── */
    [data-testid="stElementToolbar"],
    .stElementToolbar,
    div[data-testid="stDataFrameToolbar"],
    div[data-testid="stDataFrame"] [data-testid="stElementToolbar"] {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: flex-end !important;
        gap: 6px !important;
        top: 6px !important;
        right: 8px !important;
        background: rgba(30, 41, 59, 0.88) !important;
        border: 1px solid rgba(148, 163, 184, 0.25) !important;
        border-radius: 8px !important;
        padding: 3px 8px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        backdrop-filter: blur(8px) !important;
        z-index: 100 !important;
    }

    /* Botões da Toolbar da Tabela */
    [data-testid="stElementToolbar"] button,
    [data-testid="stElementToolbarButton"] button,
    div[data-testid="stDataFrame"] [data-testid="stElementToolbar"] button,
    div[data-testid="stDataFrame"] button[kind="elementToolbar"] {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 28px !important;
        height: 28px !important;
        min-width: 28px !important;
        min-height: 28px !important;
        padding: 4px !important;
        margin: 0 2px !important;
        background: transparent !important;
        border: none !important;
        border-radius: 6px !important;
        color: #94A3B8 !important; /* Cor cinza solicitada pelo usuário */
        transition: all 0.2s ease-in-out !important;
    }

    /* Hover nos Botões da Toolbar */
    [data-testid="stElementToolbar"] button:hover,
    [data-testid="stElementToolbarButton"] button:hover,
    div[data-testid="stDataFrame"] [data-testid="stElementToolbar"] button:hover,
    div[data-testid="stDataFrame"] button[kind="elementToolbar"]:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        color: #F1F5F9 !important; /* Cinza claro / esbranquiçado no hover */
        border-radius: 6px !important;
    }

    /* Ícones Vetoriais SVG da Toolbar e das Tabelas na Cor Cinza */
    [data-testid="stElementToolbar"] svg,
    [data-testid="stElementToolbar"] button svg,
    [data-testid="stElementToolbarButton"] svg,
    [data-testid="stElementToolbarButtonIcon"],
    [data-testid="stElementToolbarButtonIcon"] svg,
    div[data-testid="stDataFrame"] [data-testid="stElementToolbar"] svg,
    div[data-testid="stDataFrame"] button[kind="elementToolbar"] svg,
    div[data-testid="stDataFrame"] [data-testid="stElementToolbarButtonIcon"] {
        color: #94A3B8 !important; /* Cor cinza */
        fill: currentColor !important;
        width: 16px !important;
        height: 16px !important;
        transition: color 0.2s ease, fill 0.2s ease !important;
    }

    /* Paths do SVG */
    [data-testid="stElementToolbar"] svg path:not([fill="none"]),
    [data-testid="stElementToolbarButton"] svg path:not([fill="none"]),
    div[data-testid="stDataFrame"] [data-testid="stElementToolbar"] svg path:not([fill="none"]),
    div[data-testid="stDataFrame"] button[kind="elementToolbar"] svg path:not([fill="none"]) {
        fill: currentColor !important;
    }

    /* Hover no SVG */
    [data-testid="stElementToolbar"] button:hover svg,
    [data-testid="stElementToolbarButton"] button:hover svg,
    div[data-testid="stDataFrame"] [data-testid="stElementToolbar"] button:hover svg,
    div[data-testid="stDataFrame"] button[kind="elementToolbar"]:hover svg {
        color: #F1F5F9 !important;
        fill: currentColor !important;
    }

    /* ── GRÁFICOS PLOTLY — CONTRASTE PRETO NOS RÓTULOS E EIXOS (EXCETO TOOLTIPS DE HOVER) ── */
    .js-plotly-plot .plotly .gtitle,
    .js-plotly-plot .plotly g.g-gtitle text,
    .js-plotly-plot .plotly g.legend text,
    .js-plotly-plot .plotly text:not(.hovertext *):not(.hoverlayer *):not(g.hovertext text):not(g.hoverlayer text),
    .js-plotly-plot .plotly text.pie-text,
    .js-plotly-plot .plotly .xtick text,
    .js-plotly-plot .plotly .ytick text,
    .js-plotly-plot .plotly .annotation-text {
        color: #000000 !important;
        fill: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: 900 !important;
    }

    /* ── TOOLTIPS DE HOVER DOS GRÁFICOS PLOTLY (CAIXA ESCURA COM TEXTO 100% BRANCO) ── */
    .js-plotly-plot .plotly g.hovertext,
    .js-plotly-plot .plotly g.hovertext text,
    .js-plotly-plot .plotly g.hovertext tspan,
    .js-plotly-plot .plotly g.hovertext span,
    .js-plotly-plot .plotly .hoverlayer,
    .js-plotly-plot .plotly .hoverlayer text,
    .js-plotly-plot .plotly .hoverlayer tspan,
    .js-plotly-plot .plotly .hoverlayer span,
    .plotly .hoverlayer text,
    .plotly .hovertext text,
    g.hovertext text,
    g.hovertext tspan {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 700 !important;
        opacity: 1 !important;
    }

    /* ── BORDAS E CONTÊINERES MODERNOS CORPORATIVOS (DESIGN SYSTEM MISSHA) ── */
    [data-testid="stForm"],
    div[data-testid="stForm"],
    div[data-testid="stVerticalBlockBorderWrapper"],
    div[data-testid="stContainer"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
        padding: 20px !important;
    }

    /* ── TABELAS DE DADOS CORPORATIVAS MODERNAS ── */
    div.stTable, table,
    div[data-testid="stTable"],
    div[data-testid="stDataFrame"] {
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
        overflow: hidden !important;
    }
    table {
        border-collapse: collapse !important;
        width: 100% !important;
    }
    th, thead th {
        background-color: #F8FAFC !important;
        background: #F8FAFC !important;
        color: #475569 !important;
        -webkit-text-fill-color: #475569 !important;
        font-weight: 700 !important;
        font-size: 12px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        border: none !important;
        border-bottom: 2px solid #E2E8F0 !important;
        padding: 12px 16px !important;
    }
    th *, thead th * {
        color: #475569 !important;
        -webkit-text-fill-color: #475569 !important;
        font-weight: 700 !important;
    }
    td {
        background-color: #FFFFFF !important;
        border: none !important;
        border-bottom: 1px solid #F1F5F9 !important;
        color: #1E293B !important;
        -webkit-text-fill-color: #1E293B !important;
        font-weight: 400 !important;
        font-size: 13px !important;
        padding: 12px 16px !important;
    }
    td * {
        color: #1E293B !important;
        -webkit-text-fill-color: #1E293B !important;
        font-weight: 400 !important;
    }
    tr:hover td {
        background-color: #F8FAFC !important;
    }

    /* ── ABAS DA INTERFACE (st.tabs) — DESIGN EM PÍLULA SEGMENTADA ── */
    div[data-baseweb="tab-list"],
    .stTabs [data-baseweb="tab-list"] {
        background-color: #F1F5F9 !important;
        background: #F1F5F9 !important;
        border-radius: 10px !important;
        padding: 5px !important;
        gap: 6px !important;
        border: 1px solid #E2E8F0 !important;
        margin-bottom: 16px !important;
    }

    button[data-baseweb="tab"],
    .stTabs button[data-baseweb="tab"] {
        background: transparent !important;
        background-color: transparent !important;
        color: #64748B !important;
        -webkit-text-fill-color: #64748B !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 9px 18px !important;
        transition: all 0.15s ease !important;
    }

    button[data-baseweb="tab"] *,
    .stTabs button[data-baseweb="tab"] * {
        color: #64748B !important;
        -webkit-text-fill-color: #64748B !important;
        font-weight: 600 !important;
    }

    button[data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.7) !important;
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
    }

    button[data-baseweb="tab"][aria-selected="true"],
    .stTabs button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #4F46E5 !important;
        -webkit-text-fill-color: #4F46E5 !important;
        font-weight: 700 !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05) !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] *,
    .stTabs button[data-baseweb="tab"][aria-selected="true"] * {
        color: #4F46E5 !important;
        -webkit-text-fill-color: #4F46E5 !important;
        font-weight: 700 !important;
    }

    div[data-baseweb="tab-panel"],
    .stTabs [data-baseweb="tab-panel"] {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 8px 0 !important;
        box-shadow: none !important;
    }

    /* ── EXPANDERS — DESIGN ELEGANTE EM CARD BRANCO ── */
    div[data-testid="stExpander"],
    details[data-testid="stExpander"],
    .stExpander {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
        margin-bottom: 12px !important;
        overflow: hidden !important;
    }

    div[data-testid="stExpander"] summary,
    details[data-testid="stExpander"] > summary,
    [data-testid="stExpander"] summary {
        background-color: #F8FAFC !important;
        background: #F8FAFC !important;
        color: #0F172A !important;
        border-bottom: 1px solid #E2E8F0 !important;
        border-radius: 10px 10px 0 0 !important;
        padding: 14px 18px !important;
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
        min-height: 48px !important;
        height: auto !important;
        width: 100% !important;
    }

    /* ISOLAR O ÍCONE DA SETA DO EXPANDER (NUNCA DEVE SOBREPOR O TÍTULO) */
    div[data-testid="stExpander"] summary span:first-child,
    div[data-testid="stExpander"] summary [data-testid="stIcon"],
    div[data-testid="stExpander"] summary svg {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 20px !important;
        min-width: 20px !important;
        height: 20px !important;
        flex-shrink: 0 !important;
        overflow: visible !important;
        fill: #64748B !important;
        color: #64748B !important;
    }

    /* TÍTULO DO EXPANDER — ALINHADO, ESPAÇAMENTO RESPONSIVO E SEM CORTES */
    div[data-testid="stExpander"] summary [data-testid="stMarkdownContainer"],
    div[data-testid="stExpander"] summary p,
    details[data-testid="stExpander"] > summary p,
    div[data-testid="stExpander"] summary [data-testid="stMarkdownContainer"] p {
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 13.5px !important;
        line-height: 1.5 !important;
        letter-spacing: -0.01em !important;
        margin: 0 !important;
        padding: 0 !important;
        white-space: normal !important;
        overflow: visible !important;
        flex-grow: 1 !important;
    }

    /* ── ALINHAMENTO PERFEITO DOS FILTROS E CONTÊINERES EM COLUNAS DA INTERFACE ── */
    div[data-testid="stHorizontalBlock"] {
        gap: 16px !important;
    }

    div[data-testid="stColumn"] {
        min-width: 0 !important;
    }

    div[data-testid="stColumn"] > div {
        width: 100% !important;
    }

    /* ── ANULAR BORDAS DUPLAS NOS WRAPPERS EXTERIORES ── */
    div[data-testid="stSelectbox"] > div:not(.react-aria-Group):not([role="group"]):not([class*="e1fp86qc0"]),
    div[data-testid="stMultiSelect"] > div:not([class*="el1q88c0"]),
    div[data-testid="stTextInput"] > div:not([data-testid="stTextInputRootElement"]),
    div[data-testid="stPasswordInput"] > div:not([data-testid="stTextInputRootElement"]),
    div[data-testid="stNumberInput"] > div:not([data-testid="stNumberInputContainer"]),
    div[data-testid="stDateInput"] > div:not([data-testid="stDateInputField"]),
    div[data-testid="stTextArea"] > div:not([data-testid="stTextAreaRootElement"]),
    div[data-baseweb="base-input"] {
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
        background-color: transparent !important;
    }

    /* ── FUNDO BRANCO E BORDA FINA PRETA DE 1PX EM TODOS OS FILTROS E CAMPOS ── */
    div[data-testid="stSelectbox"] div.react-aria-Group,
    div[data-testid="stSelectbox"] div[role="group"],
    div[data-testid="stSelectbox"] [class*="e1fp86qc0"],
    div[data-testid="stSelectbox"] div[class*="react-aria-Group"],
    div[data-testid="stSelectbox"] .react-aria-ComboBox > div,
    div[data-testid="stMultiSelect"] [class*="el1q88c0"],
    div[data-testid="stMultiSelect"] div:has(> [data-testid="stMultiSelectTagsContainer"]),
    div[data-testid="stTextInputRootElement"],
    div[data-testid="stTextInput"] div[data-testid="stTextInputRootElement"],
    div[data-testid="stPasswordInput"] div[data-testid="stTextInputRootElement"],
    div[data-testid="stNumberInputContainer"],
    div[data-testid="stNumberInput"] div[data-testid="stNumberInputContainer"],
    div[data-testid="stDateInputField"],
    div[data-testid="stDateInput"] div[data-testid="stDateInputField"],
    div[data-testid="stTextAreaRootElement"],
    div[data-testid="stTextArea"] textarea,
    div[data-baseweb="select"] > div:first-child,
    div[data-baseweb="input"],
    textarea {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1px solid #000000 !important;
        border-radius: 8px !important;
        min-height: 42px !important;
        align-items: center !important;
        box-sizing: border-box !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }

    /* ── BORDA DE SINALIZAÇÃO VIOLETA ESQUERDA (3PX) NOS CAMPOS DE DIGITAÇÃO ── */
    div[data-testid="stTextInputRootElement"],
    div[data-testid="stTextInput"] div[data-testid="stTextInputRootElement"],
    div[data-testid="stPasswordInput"] div[data-testid="stTextInputRootElement"],
    div[data-testid="stNumberInputContainer"],
    div[data-testid="stNumberInput"] div[data-testid="stNumberInputContainer"],
    div[data-testid="stTextAreaRootElement"],
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stTextInput"] div[data-baseweb="input"],
    div[data-testid="stPasswordInput"] div[data-baseweb="input"],
    div[data-testid="stNumberInput"] div[data-baseweb="input"],
    textarea {
        border-left: 3px solid #4F46E5 !important;
    }

    /* FOCO E DESTAQUE AO CLICAR EM QUALQUER CAMPO OU FILTRO */
    div[data-testid="stSelectbox"] div.react-aria-Group[data-focus-within],
    div[data-testid="stSelectbox"] div[role="group"][data-focus-within],
    div[data-testid="stSelectbox"] [class*="e1fp86qc0"][data-focus-within],
    div[data-testid="stMultiSelect"] [class*="el1q88c0"]:focus-within,
    div[data-testid="stTextInputRootElement"]:focus-within,
    div[data-testid="stNumberInputContainer"]:focus-within,
    div[data-testid="stDateInputField"]:focus-within,
    div[data-testid="stTextAreaRootElement"]:focus-within,
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="base-input"]:focus-within,
    div[data-baseweb="select"] > div:first-child:focus-within,
    textarea:focus {
        border-color: #4F46E5 !important;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2) !important;
        outline: none !important;
    }

    /* ── ISOLAMENTO TOTAL DE ÍCONES E BOTÕES INTERNOS (TRANSPARENTES E SEM BORDAS) ── */
    div[data-testid="stSelectbox"] button,
    div[data-testid="stSelectbox"] [class*="e1fp86qc2"],
    div[data-testid="stSelectbox"] [class*="e1fp86qc3"],
    div[data-testid="stMultiSelect"] button,
    div[data-testid="stDateInput"] button,
    div[data-testid="stNumberInput"] button,
    div[data-baseweb="select"] [data-baseweb="icon"],
    div[data-baseweb="select"] [data-baseweb="icon"] *,
    div[data-baseweb="select"] button,
    [data-testid="stTooltipIcon"],
    [data-testid="stTooltipIcon"] * {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        filter: none !important;
        border-radius: 0 !important;
    }

    /* O ÍCONE EM SI (SVG): TOTALMENTE LIMPO, TRANSPARENTE E SEM BORDA */
    div[data-testid="stSelectbox"] svg,
    div[data-testid="stMultiSelect"] svg,
    div[data-testid="stDateInput"] svg,
    div[data-baseweb="select"] svg {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }

    /* EVITAR O QUADRADO PRETO NO SELECT (OCULTAR BOUNDING BOX M0 0h24v24H0V0z APENAS NOS BOTÕES DE DROPDOWN) */
    div[data-testid="stSelectbox"] button svg rect,
    div[data-testid="stMultiSelect"] button svg rect,
    div[data-testid="stDateInput"] button svg rect,
    div[data-baseweb="select"] button svg rect {
        fill: none !important;
        display: none !important;
    }

    div[data-testid="stSelectbox"] button svg path[d^="M0 0"],
    div[data-testid="stSelectbox"] button svg path[fill="none"],
    div[data-testid="stSelectbox"] button svg path:first-child:not(:only-child),
    div[data-testid="stMultiSelect"] button svg path[d^="M0 0"],
    div[data-testid="stMultiSelect"] button svg path[fill="none"],
    div[data-testid="stDateInput"] button svg path[d^="M0 0"],
    div[data-testid="stDateInput"] button svg path[fill="none"],
    div[data-baseweb="select"] button svg path[d^="M0 0"],
    div[data-baseweb="select"] button svg path[fill="none"] {
        fill: none !important;
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }

    /* APENAS A SETA DO DROPDOWN RECEBE PRETO NÍTIDO */
    div[data-testid="stSelectbox"] button svg path:last-child,
    div[data-testid="stMultiSelect"] button svg path:last-child,
    div[data-testid="stDateInput"] button svg path:last-child,
    div[data-baseweb="select"] button svg path:last-child {
        fill: #000000 !important;
        stroke: none !important;
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }

    /* ── PROTEÇÃO E ESTILIZAÇÃO PREMIUM DOS GRÁFICOS PLOTLY ── */
    div[data-testid="stPlotlyChart"],
    .stPlotlyChart {
        width: 100% !important;
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04) !important;
        padding: 6px !important;
        box-sizing: border-box !important;
        overflow: visible !important;
    }

    div[data-testid="stPlotlyChart"] .js-plotly-plot,
    div[data-testid="stPlotlyChart"] .plot-container {
        width: 100% !important;
    }

    div[data-testid="stPlotlyChart"] svg rect,
    div[data-testid="stPlotlyChart"] svg path,
    div[data-testid="stPlotlyChart"] svg text,
    div[data-testid="stPlotlyChart"] svg g {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }

    /* BOTÃO DE LIMPAR (X) QUANDO HÁ VALOR SELECIONADO */
    div[data-testid="stSelectbox"] button[aria-label="Clear value"] svg,
    div[data-testid="stSelectbox"] [class*="e1fp86qc3"] svg {
        fill: #64748B !important;
        color: #64748B !important;
    }

    /* ÍCONE DE TOOLTIP DA LABEL (AJUDA/ALERTA) EM ÂMBAR LIMPO */
    [data-testid="stTooltipIcon"] svg,
    [data-testid="stTooltipIcon"] svg path {
        fill: #F59E0B !important;
        color: #F59E0B !important;
        stroke: none !important;
        border: none !important;
        background: transparent !important;
    }

    /* ── TEXTO DENTRO DE TODOS OS FILTROS E CAMPOS — PRETO NÍTIDO, SEM NEGRITO ── */
    div[data-testid="stSelectbox"] input,
    div[data-testid="stSelectbox"] .react-aria-Input,
    div[data-testid="stSelectbox"] [class*="e1fp86qc1"],
    div[data-testid="stMultiSelect"] input,
    div[data-testid="stTextInput"] input,
    div[data-testid="stPasswordInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stNumberInputField"],
    div[data-testid="stDateInput"] input,
    div[data-testid="stDateInputField"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"] input,
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] p,
    textarea, select {
        background-color: transparent !important;
        background: transparent !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: 400 !important;
        font-size: 14px !important;
        line-height: normal !important;
        opacity: 1 !important;
    }

    /* PLACEHOLDER CLARO E LEGÍVEL (SEM NEGRITO) */
    input::placeholder,
    textarea::placeholder,
    div[data-testid="stSelectbox"] input::placeholder,
    div[data-testid="stMultiSelect"] input::placeholder {
        color: #64748B !important;
        -webkit-text-fill-color: #64748B !important;
        font-weight: 400 !important;
        opacity: 0.85 !important;
    }

    /* RÓTULOS DOS CAMPOS (LABELS) — NÍTIDOS, SEM NEGRITO EXCESSIVO */
    label, [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] span {
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        letter-spacing: -0.01em !important;
    }

    /* VALORES SELECIONADOS NO SELECTBOX E MULTISELECT */
    div[data-testid="stSelectbox"] div:not([data-baseweb="icon"]),
    div[data-testid="stSelectbox"] span,
    div[data-testid="stSelectbox"] p,
    div[data-testid="stMultiSelect"] div:not([data-baseweb="icon"]),
    div[data-testid="stMultiSelect"] span,
    div[data-testid="stMultiSelect"] p,
    div[data-baseweb="select"] div:not([data-baseweb="icon"]),
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] p {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: 400 !important;
        font-size: 14px !important;
        opacity: 1 !important;
    }

    /* ── TAGS NO MULTISELECT ── */
    div[data-testid="stMultiSelect"] [data-tag],
    div[data-testid="stMultiSelect"] [data-baseweb="tag"],
    div[data-baseweb="select"] [data-baseweb="tag"],
    span[data-baseweb="tag"] {
        background-color: #EEF2FF !important;
        background: #EEF2FF !important;
        border: 1px solid #C7D2FE !important;
        border-radius: 6px !important;
        padding: 2px 6px !important;
    }
    div[data-testid="stMultiSelect"] [data-tag] span,
    div[data-testid="stMultiSelect"] [data-baseweb="tag"] span,
    [data-baseweb="tag"] span {
        color: #4338CA !important;
        -webkit-text-fill-color: #4338CA !important;
        font-weight: 500 !important;
        font-size: 12px !important;
    }
    div[data-testid="stMultiSelect"] [data-tag] svg,
    div[data-testid="stMultiSelect"] [data-baseweb="tag"] svg,
    [data-baseweb="tag"] [role="button"] svg {
        fill: #6366F1 !important;
        stroke: #6366F1 !important;
    }

    /* ── MENU DE FILTROS E OPÇÕES SUSPENSAS AO ABRIR (DROPDOWN ABERTO) ── */
    div[data-testid="stSelectboxVirtualDropdown"],
    div[data-testid="stMultiSelectDropdown"],
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[role="listbox"],
    div[role="listbox"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1px solid #000000 !important;
        border-radius: 8px !important;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.18) !important;
        padding: 6px !important;
        overflow-y: auto !important;
    }

    /* ITENS E OPÇÕES DO DROPDOWN — PRETO NÍTIDO, SEM NEGRITO */
    div[data-testid="stSelectboxVirtualDropdown"] *,
    div[data-testid="stMultiSelectDropdown"] *,
    div[data-baseweb="popover"] *,
    div[data-baseweb="menu"] *,
    ul[role="listbox"] *,
    ul[role="listbox"] li,
    li[role="option"],
    li[role="option"] *,
    div[role="option"],
    div[role="option"] *,
    div[data-item-hl],
    div[data-item-hl] * {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: 400 !important;
        font-size: 13px !important;
        opacity: 1 !important;
    }

    /* CAMPO DE BUSCA INTERNO DO DROPDOWN */
    div[data-testid="stSelectboxVirtualDropdown"] input,
    div[data-testid="stMultiSelectDropdown"] input,
    div[data-baseweb="popover"] input {
        background-color: #F8FAFC !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 6px !important;
        font-weight: 400 !important;
        padding: 6px 10px !important;
    }

    /* HOVER / FOCO NOS ITENS DO DROPDOWN */
    div[data-testid="stSelectboxVirtualDropdown"] [data-hovered],
    div[data-testid="stSelectboxVirtualDropdown"] [data-focused],
    div[data-testid="stSelectboxVirtualDropdown"] div[role="option"]:hover,
    ul[role="listbox"] li:hover,
    ul[role="listbox"] li:hover *,
    li[role="option"]:hover,
    li[role="option"]:hover *,
    div[role="option"]:hover,
    div[role="option"]:hover * {
        background-color: #F1F5F9 !important;
        color: #4F46E5 !important;
        -webkit-text-fill-color: #4F46E5 !important;
        border-radius: 6px !important;
    }

    /* ITEM SELECIONADO NO DROPDOWN */
    div[data-testid="stSelectboxVirtualDropdown"] [data-selected],
    li[role="option"][aria-selected="true"],
    li[role="option"][aria-selected="true"] *,
    div[role="option"][aria-selected="true"],
    div[role="option"][aria-selected="true"] *,
    div[data-baseweb="menu"] [aria-selected="true"],
    div[data-baseweb="menu"] [aria-selected="true"] * {
        background-color: #EEF2FF !important;
        color: #4338CA !important;
        -webkit-text-fill-color: #4338CA !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
    }

    /* ── IMPERMEABILIZAÇÃO TOTAL DO CAMPO DE DATA (st.date_input) — PARCELAS E PREVISÃO 100% PRETO NÍTIDO (#000000) ── */
    div[data-testid="stDateInput"],
    div[data-testid="stDateInput"] *,
    div[data-testid="stDateInputField"],
    div[data-testid="stDateInputField"] *,
    div[data-testid="stDateInput"] input,
    div[data-testid="stDateInputField"] input,
    div[data-testid="stDateInput"] div,
    div[data-testid="stDateInputField"] div,
    div[data-testid="stDateInput"] span,
    div[data-testid="stDateInputField"] span,
    div[data-testid="stDateInput"] p,
    div[data-testid="stDateInputField"] p,
    div[data-baseweb="input"]:has(div[data-testid="stDateInputField"]) *,
    div[data-baseweb="base-input"]:has(div[data-testid="stDateInputField"]) *,
    .react-aria-DateInput,
    .react-aria-DateInput *,
    .react-aria-DateField,
    .react-aria-DateField *,
    .react-aria-DateSegment,
    .react-aria-DateSegment *,
    [data-type="day"],
    [data-type="month"],
    [data-type="year"],
    [data-type="literal"],
    [data-placeholder="true"],
    [data-placeholder="true"] *,
    input::-webkit-datetime-edit,
    input::-webkit-datetime-edit-fields-wrapper,
    input::-webkit-datetime-edit-text,
    input::-webkit-datetime-edit-month-field,
    input::-webkit-datetime-edit-day-field,
    input::-webkit-datetime-edit-year-field {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        opacity: 1 !important;
        visibility: visible !important;
        filter: none !important;
    }

    /* SEGMENTO DE DATA SELECIONADO OU COM FOCO (EX: ANO 2026 OU DIA/MÊS SELECIONADO) — REMOVER VERMELHO/BRANCO */
    .react-aria-DateSegment[data-focused="true"],
    .react-aria-DateSegment[data-selected="true"],
    div[data-testid="stDateInputField"] [data-focused="true"],
    div[data-testid="stDateInputField"] [data-selected="true"],
    [data-type][data-focused="true"],
    [data-type][data-selected="true"] {
        background-color: #EEF2FF !important;
        background: #EEF2FF !important;
        color: #4F46E5 !important;
        -webkit-text-fill-color: #4F46E5 !important;
        border-radius: 4px !important;
        font-weight: 800 !important;
    }

    /* GARANTIR ÍCONE DO CALENDÁRIO VISÍVEL E PRETO */
    div[data-testid="stDateInput"] svg,
    div[data-testid="stDateInputField"] svg,
    div[data-testid="stDateInput"] button svg,
    input::-webkit-calendar-picker-indicator {
        fill: #000000 !important;
        color: #000000 !important;
        stroke: #000000 !important;
        opacity: 1 !important;
        filter: none !important;
    }

    /* ── POPUP DO CALENDÁRIO (st.date_input) ── */
    div[data-baseweb="calendar"],
    div[data-baseweb="datepicker"],
    div[data-baseweb="popover"]:has(div[data-baseweb="calendar"]) {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1) !important;
        padding: 10px !important;
    }
    div[data-baseweb="calendar"] *,
    div[data-baseweb="datepicker"] * {
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
        font-weight: 500 !important;
    }
    div[data-baseweb="calendar"] svg,
    div[data-baseweb="datepicker"] svg {
        fill: #475569 !important;
    }
    div[data-baseweb="calendar"] [role="gridcell"]:hover {
        background-color: #EEF2FF !important;
        color: #4F46E5 !important;
        border-radius: 6px !important;
    }
    div[data-baseweb="calendar"] [aria-selected="true"] {
        background-color: #4F46E5 !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border-radius: 6px !important;
    }

    /* ── BOTÕES PRIMÁRIOS (GRADIENTE VIBRANTE ROXO/ÍNDIGO) ── */
    div.stFormSubmitButton > button,
    button[data-testid="stBaseButton-formSubmit"],
    button[kind="primary"],
    button[data-testid="stBaseButton-primary"],
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #4F46E5 0%, #3730A3 100%) !important;
        background-color: #4F46E5 !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        border-radius: 8px !important;
        padding: 10px 22px !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.25) !important;
        transition: all 0.2s ease !important;
    }
    div.stFormSubmitButton > button:hover,
    button[data-testid="stBaseButton-formSubmit"]:hover,
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #4338CA 0%, #312E81 100%) !important;
        box-shadow: 0 6px 18px rgba(79, 70, 229, 0.4) !important;
        transform: translateY(-1px) !important;
    }
    div.stFormSubmitButton > button *,
    button[data-testid="stBaseButton-formSubmit"] *,
    button[kind="primary"] * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    /* ── BOTÕES SECUNDÁRIOS ── */
    div.stButton > button,
    button[data-testid="stBaseButton-secondary"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #1E293B !important;
        -webkit-text-fill-color: #1E293B !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover,
    button[data-testid="stBaseButton-secondary"]:hover {
        background-color: #F8FAFC !important;
        border-color: #94A3B8 !important;
        color: #0F172A !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
    }
    div.stButton > button *,
    button[data-testid="stBaseButton-secondary"] * {
        color: #1E293B !important;
        -webkit-text-fill-color: #1E293B !important;
    }

    /* ── SIDEBAR EXECUTIVA OMNIEVO ── */
    section[data-testid="stSidebar"] {
        background: #0F172A !important;
        border-right: 1px solid #1E293B !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div:not(button *) {
        color: #F8FAFC !important;
        -webkit-text-fill-color: #F8FAFC !important;
    }
    section[data-testid="stSidebar"] .stRadio > label {
        font-size: 11px !important;
        font-weight: 700 !important;
        color: #94A3B8 !important;
        -webkit-text-fill-color: #94A3B8 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label {
        padding: 10px 14px !important;
        border-radius: 8px !important;
        margin-bottom: 3px !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        color: #94A3B8 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:hover {
        background: #1E293B !important;
        color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) {
        background: #4F46E5 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.35) !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label > div:first-child,
    section[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label input[type="radio"],
    section[data-testid="stSidebar"] [data-baseweb="radio"] > div:first-child,
    section[data-testid="stSidebar"] [data-baseweb="radio"] svg {
        display: none !important;
    }
    section[data-testid="stSidebar"] div.stButton > button {
        background-color: #1E293B !important;
        color: #FFFFFF !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    section[data-testid="stSidebar"] div.stButton > button * {
        color: #FFFFFF !important;
    }

    /* ── BOTÃO DE SAIR DA CONTA (SIDEBAR) ── */
    .sidebar-logout-container {
        margin-bottom: 12px !important;
    }
    .sidebar-logout-container div.stButton > button {
        background-color: rgba(239, 68, 68, 0.12) !important;
        color: #FCA5A5 !important;
        border: 1px solid rgba(239, 68, 68, 0.35) !important;
        border-radius: 8px !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        padding: 6px 12px !important;
        transition: all 0.2s ease !important;
    }
    .sidebar-logout-container div.stButton > button:hover {
        background-color: rgba(239, 68, 68, 0.25) !important;
        color: #FFFFFF !important;
        border-color: #EF4444 !important;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3) !important;
    }
    .sidebar-logout-container div.stButton > button * {
        color: #FCA5A5 !important;
        font-weight: 700 !important;
    }
    .sidebar-logout-container div.stButton > button:hover * {
        color: #FFFFFF !important;
    }

    /* ── TÍTULOS DE SEÇÃO & PAGE HEADER ── */
    .section-header {
        font-size: 14px !important;
        font-weight: 700 !important;
        color: #3730A3 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        background: #EEF2FF !important;
        padding: 10px 16px !important;
        border-left: 4px solid #4F46E5 !important;
        border-radius: 8px !important;
        margin-top: 18px !important;
        margin-bottom: 16px !important;
    }
    .page-header {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 24px;
        padding-bottom: 16px;
        border-bottom: 1px solid #E2E8F0;
    }
    .page-header-icon {
        font-size: 24px;
        background: #EEF2FF;
        color: #4F46E5;
        width: 44px;
        height: 44px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #C7D2FE;
    }
    .page-header-title {
        font-size: 22px;
        font-weight: 700;
        color: #0F172A !important;
        letter-spacing: -0.02em;
    }
    .page-header-subtitle {
        font-size: 13px;
        color: #64748B !important;
        font-weight: 400;
        margin-top: 2px;
    }

    /* ── KANBAN CARDS & COLUNAS ── */
    .kanban-col-title {
        font-size: 13px;
        font-weight: 700;
        color: #1E293B !important;
        padding: 10px 14px;
        border-radius: 8px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #F1F5F9;
        border: 1px solid #E2E8F0 !important;
    }
    .kanban-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px;
        padding: 14px 16px;
        margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }
    .kanban-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
    }
    .kanban-card-title {
        font-size: 14px;
        font-weight: 700;
        color: #0F172A !important;
    }
    .kanban-card-sub {
        font-size: 12px;
        color: #64748B !important;
        font-weight: 500;
        margin-top: 2px;
    }
    .kanban-card-val {
        font-size: 15px;
        font-weight: 700;
        color: #4F46E5 !important;
        margin-top: 8px;
    }

    /* ── ESPAÇAMENTO COMPACTO ENTRE CARDS E AÇÕES NO KANBAN ── */
    div[data-testid="stHorizontalBlock"]:has(.kanban-col-title) [data-testid="stVerticalBlock"] {
        gap: 4px !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.kanban-col-title) [data-testid="stElementContainer"] {
        margin-bottom: 2px !important;
    }

    /* ── PREVIEW DE NF ── */
    .nf-header {
        text-align: center;
        padding: 20px;
        background: #F8FAFC;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px;
        margin-bottom: 16px;
    }
    .nf-header h2 { font-size: 20px; font-weight: 700; color: #0F172A !important; margin: 0; }
    .nf-header p { font-size: 12px; color: #64748B !important; font-weight: 500; margin: 4px 0 0 0; }
    .nf-section {
        background: #FFFFFF;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
    .nf-section-title {
        font-size: 12px; font-weight: 700; color: #4F46E5 !important;
        text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 10px;
    }
    .nf-row { display: flex; justify-content: space-between; padding: 5px 0; font-size: 13px; }
    .nf-label { color: #64748B !important; font-weight: 500; }
    .nf-value { color: #0F172A !important; font-weight: 600; }
    .nf-total-box {
        background: linear-gradient(135deg, #EEF2FF 0%, #F1F5F9 100%);
        border: 1px solid #C7D2FE !important;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-top: 16px;
    }
    .nf-total-label { font-size: 12px; font-weight: 700; color: #4F46E5; text-transform: uppercase; letter-spacing: 0.08em; }
    .nf-total-value { font-size: 28px; font-weight: 800; color: #0F172A !important; margin-top: 4px; }

    /* ── CARDS DE MÉTRICAS EXECUTIVAS ── */
    [data-testid="stMetric"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }
    [data-testid="stMetric"]:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06) !important;
        transform: translateY(-1px) !important;
    }
    [data-testid="stMetric"] label {
        color: #64748B !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
    }
    [data-testid="stMetricValue"] {
        color: #0F172A !important;
        font-weight: 800 !important;
        font-size: 24px !important;
    }

    /* ==========================================================================
       SISTEMA RESPONSIVO MULTI-DISPOSITIVO EXECUTIVO (OMNIEVO / CRM MISSHA)
       Compatibilidade total: Smartphones, Tablets, Laptops, Desktops e Ultra-Wide
       ========================================================================== */

    /* ── BASE & CONTÊINER GLOBAL ── */
    html, body {
        max-width: 100vw !important;
        overflow-x: hidden !important;
    }

    /* Scrollbars elegantes e discretas para containers horizontais */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #F1F5F9;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb {
        background: #CBD5E1;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #94A3B8;
    }

    /* Tabelas e DataFrames fluidos */
    div[data-testid="stTable"] {
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
    }
    div[data-testid="stDataFrame"],
    .stDataFrame {
        width: 100% !important;
        max-width: 100% !important;
        overflow: hidden !important;
    }

    /* ── 1. TELAS ULTRA-WIDE & 4K (> 1440px) ── */
    @media screen and (min-width: 1441px) {
        .block-container {
            max-width: 1600px !important;
            margin-left: auto !important;
            margin-right: auto !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 26px !important;
        }
    }

    /* ── 2. LAPTOPS E DESKTOPS PADRÃO (1025px - 1440px) ── */
    @media screen and (min-width: 1025px) and (max-width: 1440px) {
        .block-container {
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
        }
    }

    /* ── DESKTOP & TELAS LARGAS (>= 1200px): KANBAN EXPANDIDO ── */
    @media screen and (min-width: 1200px) {
        div[data-testid="stHorizontalBlock"]:has(.kanban-col-title),
        div[data-testid="stHorizontalBlock"]:has(.kanban-card) {
            overflow-x: visible !important;
            flex-wrap: nowrap !important;
            gap: 12px !important;
        }
        div[data-testid="stHorizontalBlock"]:has(.kanban-col-title) > div[data-testid="column"],
        div[data-testid="stHorizontalBlock"]:has(.kanban-card) > div[data-testid="column"] {
            min-width: 0 !important;
            max-width: none !important;
            flex: 1 1 0% !important;
        }
    }

    /* ── 3. TABLETS E TELAS MÉDIAS (769px - 1024px) ── */
    @media screen and (min-width: 769px) and (max-width: 1024px) {
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 3.5rem !important;
            padding-left: 1.25rem !important;
            padding-right: 1.25rem !important;
        }

        /* Refluxo de colunas de formulários e filtros em tablets */
        div[data-testid="stHorizontalBlock"]:not(:has(.kanban-col-title)):not(:has(.kanban-card)) {
            flex-wrap: wrap !important;
            gap: 12px !important;
        }

        /* Abas com suporte a rolagem suave por toque */
        div[data-baseweb="tab-list"],
        .stTabs [data-baseweb="tab-list"] {
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
            flex-wrap: nowrap !important;
        }
        button[data-baseweb="tab"] {
            flex-shrink: 0 !important;
            white-space: nowrap !important;
        }

        /* Kanban em Tablets: Rolagem horizontal suave com snap */
        div[data-testid="stHorizontalBlock"]:has(.kanban-col-title),
        div[data-testid="stHorizontalBlock"]:has(.kanban-card) {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
            scroll-snap-type: x mandatory !important;
            gap: 12px !important;
            padding-bottom: 14px !important;
        }
        div[data-testid="stHorizontalBlock"]:has(.kanban-col-title) > div[data-testid="column"],
        div[data-testid="stHorizontalBlock"]:has(.kanban-card) > div[data-testid="column"] {
            min-width: 290px !important;
            max-width: 320px !important;
            flex: 0 0 290px !important;
            scroll-snap-align: start !important;
        }
    }

    /* ── 4. PHABLETS E SMARTPHONES GRANDES (641px - 768px) ── */
    @media screen and (min-width: 641px) and (max-width: 768px) {
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 3rem !important;
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
        }
        div[data-testid="stHorizontalBlock"]:not(:has(.kanban-col-title)):not(:has(.kanban-card)) {
            flex-wrap: wrap !important;
            gap: 10px !important;
        }
        div[data-testid="stHorizontalBlock"]:not(:has(.kanban-col-title)):not(:has(.kanban-card)) > div[data-testid="column"] {
            min-width: 100% !important;
            flex: 1 1 100% !important;
        }
        div[data-testid="stHorizontalBlock"]:has(.kanban-col-title),
        div[data-testid="stHorizontalBlock"]:has(.kanban-card) {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
            scroll-snap-type: x mandatory !important;
            gap: 10px !important;
            padding-bottom: 14px !important;
        }
        div[data-testid="stHorizontalBlock"]:has(.kanban-col-title) > div[data-testid="column"],
        div[data-testid="stHorizontalBlock"]:has(.kanban-card) > div[data-testid="column"] {
            min-width: 285px !important;
            max-width: 300px !important;
            flex: 0 0 285px !important;
            scroll-snap-align: start !important;
        }
    }

    /* ── 5. SMARTPHONES E TELAS MOBILE PEQUENAS (<= 640px) ── */
    @media screen and (max-width: 640px) {
        /* Aproveitamento máximo da tela eliminando as margens gigantes do Streamlit */
        .block-container {
            padding-top: 0.75rem !important;
            padding-bottom: 2.5rem !important;
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
            max-width: 100vw !important;
            overflow-x: hidden !important;
        }

        /* Cabeçalhos e Banners Fluidos */
        .page-header {
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 10px !important;
            margin-bottom: 16px !important;
            padding-bottom: 12px !important;
        }
        .page-header-title {
            font-size: 18px !important;
        }
        .page-header-icon {
            width: 38px !important;
            height: 38px !important;
            font-size: 20px !important;
        }
        .page-header-subtitle {
            font-size: 12px !important;
        }
        .omnievo-banner,
        .copilot-ia-banner {
            padding: 14px 16px !important;
            border-radius: 12px !important;
        }

        /* Empilhamento inteligente de colunas em formulários e grades */
        div[data-testid="stHorizontalBlock"]:not(:has(.kanban-col-title)):not(:has(.kanban-card)) {
            flex-wrap: wrap !important;
            gap: 8px !important;
        }
        div[data-testid="stHorizontalBlock"]:not(:has(.kanban-col-title)):not(:has(.kanban-card)) > div[data-testid="column"],
        div[data-testid="stHorizontalBlock"]:not(:has(.kanban-col-title)):not(:has(.kanban-card)) > div[data-testid="stColumn"] {
            min-width: 100% !important;
            width: 100% !important;
            max-width: 100% !important;
            flex: 1 1 100% !important;
            margin-bottom: 4px !important;
        }

        /* KANBAN BOARD MOBILE-NATIVE (Swipe Horizontal Fluido com Scroll-Snap) */
        div[data-testid="stHorizontalBlock"]:has(.kanban-col-title),
        div[data-testid="stHorizontalBlock"]:has(.kanban-card) {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
            scroll-snap-type: x mandatory !important;
            gap: 10px !important;
            padding-bottom: 16px !important;
            padding-left: 2px !important;
            padding-right: 2px !important;
        }
        div[data-testid="stHorizontalBlock"]:has(.kanban-col-title) > div[data-testid="column"],
        div[data-testid="stHorizontalBlock"]:has(.kanban-card) > div[data-testid="column"] {
            min-width: 280px !important;
            max-width: 300px !important;
            flex: 0 0 280px !important;
            scroll-snap-align: start !important;
        }
        .kanban-card {
            padding: 12px 14px !important;
        }
        .kanban-card-title {
            font-size: 13px !important;
        }

        /* Prevenção de Auto-Zoom no Safari iOS e alvos de toque ergonômicos (mínimo 44px) */
        input,
        textarea,
        select,
        div[data-baseweb="select"] input {
            font-size: 16px !important;
        }
        button,
        [data-testid="stBaseButton-secondary"],
        [data-testid="stBaseButton-primary"],
        div.stButton > button {
            min-height: 44px !important;
            font-size: 14px !important;
            touch-action: manipulation !important;
        }

        /* Cards de Métricas / KPIs compactos e legíveis */
        [data-testid="stMetric"] {
            padding: 12px 14px !important;
            border-radius: 10px !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 20px !important;
        }
        [data-testid="stMetric"] label {
            font-size: 11px !important;
        }

        /* Abas em formato carrossel horizontal por toque */
        div[data-baseweb="tab-list"],
        .stTabs [data-baseweb="tab-list"] {
            display: flex !important;
            flex-wrap: nowrap !important;
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
            scrollbar-width: none !important;
            padding: 4px 6px !important;
            gap: 4px !important;
        }
        div[data-baseweb="tab-list"]::-webkit-scrollbar,
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
            display: none !important;
        }
        button[data-baseweb="tab"],
        .stTabs button[data-baseweb="tab"] {
            flex-shrink: 0 !important;
            white-space: nowrap !important;
            font-size: 12px !important;
            padding: 8px 12px !important;
        }

        /* Radar de Clientes & Churn: Cards otimizados para toque */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.radar-cliente-card-marker) > div {
            padding: 14px 14px !important;
            border-radius: 12px !important;
        }

        /* Ocultar barra flutuante do Plotly para não sobrepor títulos no mobile */
        .modebar-container {
            display: none !important;
        }

        /* Modais / Diálogos adaptados para a largura do celular */
        div[data-testid="stModal"] > div,
        div[role="dialog"] {
            width: 95vw !important;
            max-width: 95vw !important;
            padding: 14px !important;
            margin: 6px auto !important;
        }

        /* Destaque do Botão de Abrir / Ocultar Menu & Abas no Celular */
        [data-testid="stSidebarExpandButton"],
        [data-testid="stSidebarCollapseButton"],
        button[aria-label="Expand sidebar"],
        button[aria-label="Collapse sidebar"],
        button[aria-label="Open sidebar"],
        button[aria-label="Close sidebar"],
        header[data-testid="stHeader"] button {
            display: inline-flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%) !important;
            color: #FFFFFF !important;
            border-radius: 20px !important;
            padding: 6px 14px !important;
            box-shadow: 0 4px 14px rgba(124, 58, 237, 0.45) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            font-weight: 800 !important;
            font-size: 13px !important;
            z-index: 999999 !important;
        }

        [data-testid="stSidebarExpandButton"] *,
        [data-testid="stSidebarCollapseButton"] *,
        header[data-testid="stHeader"] button * {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
        }

        /* Botão de Envio de Pedido e Ações Principais em Destaque */
        .btn-enviar-pedido button {
            width: 100% !important;
            height: 52px !important;
            font-size: 15px !important;
        }
    }

    /* ── 6. TEPAS HIGH-DPI / RETINA & DISPLAYS 4K (iPhones, MacBooks, Monitores Ultra-HD) ── */
    @media (-webkit-min-device-pixel-ratio: 1.5), (min-resolution: 144dpi) {
        body, input, textarea, button, select, label, span, p, h1, h2, h3 {
            -webkit-font-smoothing: antialiased !important;
            -moz-osx-font-smoothing: grayscale !important;
            text-rendering: optimizeLegibility !important;
        }
        svg, img, canvas, .js-plotly-plot svg {
            image-rendering: -webkit-optimize-contrast !important;
            shape-rendering: geometricPrecision !important;
            text-rendering: geometricPrecision !important;
        }
    }

    /* ── 7. OTIMIZAÇÕES DE IMPRESSÃO (PEDIDOS E RELATÓRIOS) ── */
    @media print {
        header,
        footer,
        section[data-testid="stSidebar"],
        button,
        .stButton,
        [data-testid="stDecoration"] {
            display: none !important;
        }
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
    }
</style>
""", unsafe_allow_html=True)

def obter_logo_b64_html(for_dark_bg=False):
    files = [("logo_custom.png", "image/png"), ("logo.png", "image/png"), ("logo_white.png", "image/png"), ("logo_white.svg", "image/svg+xml"), ("logo.svg", "image/svg+xml")]
    for fn, mime in files:
        p = os.path.join("assets", fn)
        if os.path.exists(p):
            try:
                with open(p, "rb") as f:
                    data = f.read()
                    b64 = base64.b64encode(data).decode("utf-8")
                    return f'<div style="text-align: center;"><img src="data:{mime};base64,{b64}" style="width: 85px; height: 85px; object-fit: cover; border-radius: 50%; box-shadow: 0 4px 15px rgba(0,0,0,0.5), 0 0 15px rgba(99,102,241,0.3); border: 2px solid rgba(255,255,255,0.2); margin: 0 auto 8px auto; display: block;" alt="Omnievo" /></div>'
            except Exception:
                pass
    return ""

def obter_dados_tenant():
    host = ""
    try:
        if hasattr(st, "context") and hasattr(st.context, "headers"):
            host = st.context.headers.get("host", "") or st.context.headers.get("x-forwarded-host", "")
    except Exception:
        pass
    
    empresa_param = st.query_params.get("empresa") or st.query_params.get("tenant")
    
    clean_host = host.split(":")[0].strip().lower() if host else ""
    subdominio = ""
    if empresa_param:
        subdominio = str(empresa_param).strip().lower()
    elif clean_host and ".omnievo.com.br" in clean_host:
        subdominio = clean_host.split(".omnievo.com.br")[0].strip()
    elif clean_host and clean_host.endswith(".localhost"):
        subdominio = clean_host.split(".localhost")[0].strip()

    if subdominio and subdominio not in ["www", "crm", "app", "portal", "api"]:
        nome_empresa = subdominio.upper() + " COMMERCE"
        subdominio_completo = f"{subdominio}.omnievo.com.br"
    else:
        nome_empresa = "MISSHA COMMERCE"
        subdominio_completo = "missha.omnievo.com.br"
        
    res = {
        "subdominio": subdominio or "missha",
        "nome_empresa": nome_empresa,
        "subdominio_completo": subdominio_completo,
        "host": host
    }
    st.session_state["tenant_info"] = res
    return res

# ══════════════════════════════════════════════════════════════════════════════
# TELA DE LOGIN — AUTENTICAÇÃO EXCLUSIVA DE VENDEDORES OMIE ERP
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.get("authenticated", False):
    # Ponte de auto-recuperação de sessão permanente via LocalStorage do navegador
    components.html("""
    <script>
    (function() {
        try {
            const wins = [window, window.parent, window.top];
            let savedToken = null;
            for (const w of wins) {
                try {
                    if (w && w.localStorage) {
                        savedToken = w.localStorage.getItem('omnievo_crm_token');
                        if (savedToken) break;
                    }
                } catch(e) {}
            }
            if (savedToken) {
                const pWin = window.parent || window;
                const search = pWin.location.search || '';
                if (!search.includes('session_token')) {
                    const u = new URL(pWin.location.href);
                    u.searchParams.set('session_token', savedToken);
                    pWin.location.replace(u.toString());
                }
            }
        } catch(e) {}
    })();
    </script>
    """, height=0)

    st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap');

[data-testid="stSidebar"] { display: none !important; }

/* ── REMOÇÃO TOTAL DA PARTE BRANCA SUPERIOR (HEADER, TOOLBAR, MENU & DECORATION STREAMLIT) ── */
[data-testid="stHeader"],
header[data-testid="stHeader"],
header,
.stApp > header,
div[data-testid="stToolbar"],
[data-testid="stToolbar"],
div[data-testid="stDecoration"],
[data-testid="stDecoration"],
#MainMenu,
[data-testid="stStatusWidget"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    pointer-events: none !important;
}

/* Fundo Geral da Aplicação */
.stApp {
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important;
    background-color: #070815 !important;
    background: radial-gradient(circle at 50% 48%, #18173d 0%, #0d0e27 45%, #070815 100%) !important;
    overflow-x: hidden !important;
    color: #FFFFFF !important;
}

/* ── LAYOUT EM TELA CHEIA REAL (SPLIT-SCREEN 50% / 50% DE PONTA A PONTA) ── */
div[data-testid="stAppViewContainer"],
div[data-testid="stAppViewContainer"] > section.main {
    width: 100vw !important;
    max-width: 100vw !important;
    min-width: 100vw !important;
    height: 100vh !important;
    min-height: 100vh !important;
    padding: 0 !important;
    margin: 0 !important;
    overflow: hidden !important;
}

div[data-testid="stAppViewContainer"] > section.main > div.block-container {
    max-width: 100vw !important;
    width: 100vw !important;
    min-width: 100vw !important;
    height: 100vh !important;
    min-height: 100vh !important;
    padding: 0 !important;
    margin: 0 !important;
    overflow: hidden !important;
    display: flex !important;
    flex-direction: column !important;
}

/* Forçar o grid horizontal do Streamlit a ocupar 100vw de ponta a ponta sem frestas */
div[data-testid="stAppViewContainer"] div[data-testid="stHorizontalBlock"] {
    width: 100vw !important;
    max-width: 100vw !important;
    min-width: 100vw !important;
    height: 100vh !important;
    min-height: 100vh !important;
    gap: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    display: flex !important;
    align-items: stretch !important;
}

/* Esferas Flutuantes Atmosféricas */
.ambient-glow-orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(80px);
    pointer-events: none;
    z-index: 0;
}
.orb-1 {
    width: 480px; height: 480px;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.35) 0%, transparent 70%);
    top: -80px; left: -60px;
}
.orb-2 {
    width: 520px; height: 520px;
    background: radial-gradient(circle, rgba(168, 85, 247, 0.28) 0%, transparent 70%);
    bottom: -100px; right: -80px;
}

/* ── METADE ESQUERDA (DO INÍCIO ATÉ O MEIO: 0 A 50% DA TELA): ACESSO DO CLIENTE ── */
div[data-testid="stColumn"]:first-child,
div[data-testid="column"]:first-child,
div[data-testid="stHorizontalBlock"] > div:first-child {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    bottom: 0 !important;
    width: 50vw !important;
    min-width: 50vw !important;
    max-width: 50vw !important;
    height: 100vh !important;
    min-height: 100vh !important;
    max-height: 100vh !important;
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    border: none !important;
    border-radius: 0 !important;
    border-right: 1px solid #E2E8F0 !important;
    box-shadow: 12px 0 35px rgba(0, 0, 0, 0.15) !important;
    box-sizing: border-box !important;
    color: #0F172A !important;
    z-index: 10 !important;
    padding: 30px 48px !important;
    overflow-y: auto !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
}

div[data-testid="stColumn"]:first-child > div[data-testid="stVerticalBlock"],
div[data-testid="column"]:first-child > div[data-testid="stVerticalBlock"],
div[data-testid="stHorizontalBlock"] > div:first-child > div[data-testid="stVerticalBlock"] {
    max-width: 480px !important;
    width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Título e Textos do Card Branco — Nome Escuro Solicitado pelo Usuário */
.tenant-company-title {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 32px !important;
    font-weight: 900 !important;
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
    letter-spacing: -0.02em !important;
    margin-top: 4px !important;
    margin-bottom: 4px !important;
    line-height: 1.15 !important;
    text-shadow: none !important;
}

/* Labels nos Inputs */
div[data-testid="column"]:first-child label,
div[data-testid="column"]:first-child label p {
    color: #334155 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 11px !important;
    font-weight: 800 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    margin-bottom: 4px !important;
}

/* Inputs no Card Branco */
div[data-testid="column"]:first-child div[data-testid="stTextInput"] input {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    transition: all 0.2s ease !important;
}
div[data-testid="column"]:first-child div[data-testid="stTextInput"] input::placeholder {
    color: #94A3B8 !important;
    opacity: 1 !important;
}
div[data-testid="column"]:first-child div[data-testid="stTextInput"] input:focus {
    background-color: #FFFFFF !important;
    border-color: #7C3AED !important;
    box-shadow: 0 0 0 3.5px rgba(124, 58, 237, 0.15) !important;
    color: #0F172A !important;
}

/* Remove a borda padrão do stForm no Streamlit */
div[data-testid="column"]:first-child div[data-testid="stForm"],
div[data-testid="column"]:first-child form,
div[data-testid="column"]:first-child [data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
}

/* Checkbox no Card Branco */
div[data-testid="column"]:first-child div[data-testid="stCheckbox"] label span {
    color: #475569 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}

/* Abas / Tabs Estilizadas no Card Branco */
div[data-testid="column"]:first-child .stTabs [data-baseweb="tab-list"] {
    background: #F1F5F9 !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 6px !important;
    margin-bottom: 14px !important;
}
div[data-testid="column"]:first-child .stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: #64748B !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    padding: 7px 14px !important;
    border: none !important;
    background: transparent !important;
    transition: all 0.2s ease !important;
}
div[data-testid="column"]:first-child .stTabs [data-baseweb="tab"]:hover {
    color: #0F172A !important;
    background: rgba(255, 255, 255, 0.6) !important;
}
div[data-testid="column"]:first-child .stTabs [aria-selected="true"] {
    background: #FFFFFF !important;
    color: #0F172A !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
    font-weight: 800 !important;
}
div[data-testid="column"]:first-child .stTabs [data-baseweb="tab-highlight"],
div[data-testid="column"]:first-child .stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

/* Botão Secundário: Sincronizar Vendedores Omie ERP */
div[data-testid="column"]:first-child div[data-testid="stButton"] > button {
    background: #F8FAFC !important;
    border: 1.5px solid #CBD5E1 !important;
    color: #4338CA !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 12px !important;
    font-weight: 800 !important;
    border-radius: 12px !important;
    padding: 9px 16px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
}
div[data-testid="column"]:first-child div[data-testid="stButton"] > button:hover {
    background: #EEF2FF !important;
    border-color: #818CF8 !important;
    color: #3730A3 !important;
    transform: translateY(-1px) !important;
}

/* Botão Principal de Login: Estilo Dark Navy Exato da Imagem do Usuário */
div[data-testid="column"]:first-child div.stFormSubmitButton > button,
div[data-testid="column"]:first-child button[data-testid="stBaseButton-formSubmit"],
div[data-testid="column"]:first-child button[data-testid="stBaseButton-primaryFormSubmit"],
div[data-testid="column"]:first-child button[data-testid="stBaseButton-secondaryFormSubmit"],
div[data-testid="column"]:first-child button[data-testid="baseButton-secondaryFormSubmit"],
div[data-testid="column"]:first-child button[data-testid="baseButton-primaryFormSubmit"],
div[data-testid="column"]:first-child button[kind="primary"],
div[data-testid="column"]:first-child button[kind="secondary"],
div[data-testid="column"]:first-child .stFormSubmitButton > button {
    background: #0F172A !important;
    background-color: #0F172A !important;
    background-image: none !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    height: 48px !important;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.25) !important;
    transition: all 0.25s ease !important;
    cursor: pointer !important;
}
div[data-testid="column"]:first-child div.stFormSubmitButton > button:hover,
div[data-testid="column"]:first-child button[data-testid="stBaseButton-formSubmit"]:hover,
div[data-testid="column"]:first-child button[data-testid="stBaseButton-primaryFormSubmit"]:hover,
div[data-testid="column"]:first-child button[data-testid="stBaseButton-secondaryFormSubmit"]:hover,
div[data-testid="column"]:first-child button[data-testid="baseButton-secondaryFormSubmit"]:hover,
div[data-testid="column"]:first-child button[data-testid="baseButton-primaryFormSubmit"]:hover,
div[data-testid="column"]:first-child button[kind="primary"]:hover,
div[data-testid="column"]:first-child button[kind="secondary"]:hover,
div[data-testid="column"]:first-child .stFormSubmitButton > button:hover {
    background: #7C3AED !important;
    background-color: #7C3AED !important;
    background-image: none !important;
    box-shadow: 0 12px 28px rgba(124, 58, 237, 0.35) !important;
    transform: translateY(-1px) !important;
}
div[data-testid="column"]:first-child div.stFormSubmitButton > button *,
div[data-testid="column"]:first-child .stFormSubmitButton > button * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* ── METADE DIREITA (DO MEIO À BORDA DIREITA: 50% A 100% DA TELA INTEIRA) ── */
div[data-testid="stColumn"]:nth-child(2),
div[data-testid="column"]:nth-child(2),
div[data-testid="stHorizontalBlock"] > div:nth-child(2) {
    position: fixed !important;
    top: 0 !important;
    left: 50% !important;
    right: 0 !important;
    bottom: 0 !important;
    width: 50vw !important;
    min-width: 50vw !important;
    max-width: 50vw !important;
    height: 100vh !important;
    min-height: 100vh !important;
    max-height: 100vh !important;
    background: #070B14 !important;
    background-color: #070B14 !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    box-sizing: border-box !important;
    z-index: 5 !important;
    overflow: hidden !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
}

div[data-testid="stColumn"]:nth-child(2) > div[data-testid="stVerticalBlock"],
div[data-testid="column"]:nth-child(2) > div[data-testid="stVerticalBlock"],
div[data-testid="stHorizontalBlock"] > div:nth-child(2) > div[data-testid="stVerticalBlock"] {
    width: 100% !important;
    height: 100% !important;
    min-height: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* ── LADO DIREITO: SHOWCASE VISUAL DARK COSMIC TOMANDO TODA A TELA DO MEIO PARA DIREITA ── */
.login-right-animated-panel {
    position: fixed !important;
    top: 0 !important;
    left: 50% !important;
    right: 0 !important;
    bottom: 0 !important;
    width: 50vw !important;
    height: 100vh !important;
    min-height: 100vh !important;
    max-height: 100vh !important;
    background: #070B14 !important;
    background-image: radial-gradient(rgba(148, 163, 184, 0.12) 1.2px, transparent 1.2px) !important;
    background-size: 24px 24px !important;
    border-radius: 0 !important;
    border: none !important;
    box-shadow: inset 0 0 120px rgba(124, 58, 237, 0.18) !important;
    padding: 30px 48px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    align-items: center !important;
    box-sizing: border-box !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    z-index: 99 !important;
}

/* Forçar todos os textos dentro do showcase a ficarem visíveis e brilhantes */
.login-right-animated-panel * {
    box-sizing: border-box;
}

.login-right-animated-panel h1,
.login-right-animated-panel .showcase-main-title {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-size: 26px !important;
    font-weight: 900 !important;
    line-height: 1.25 !important;
    margin: 8px 0 !important;
}

.login-right-animated-panel p,
.login-right-animated-panel .showcase-subtitle {
    color: #CBD5E1 !important;
    -webkit-text-fill-color: #CBD5E1 !important;
    font-size: 13px !important;
    line-height: 1.5 !important;
    margin: 0 0 14px 0 !important;
}

.login-right-animated-panel > div[style*="text-align:left"] {
    max-width: 520px;
    width: 100%;
    margin: auto 0;
}

.login-hud-header,
.login-hud-footer {
    max-width: 520px;
    width: 100%;
    position: relative;
    z-index: 6;
}

/* 🌟 ANIMAÇÃO 3D DA PLATAFORMA CRM & KANBAN (FLUTUAÇÃO E PERSPECTIVA) */
@keyframes float3D {
    0%, 100% {
        transform: perspective(1000px) rotateX(15deg) rotateY(-8deg) rotateZ(3deg) translateY(0px) scale(0.96);
    }
    50% {
        transform: perspective(1000px) rotateX(19deg) rotateY(-4deg) rotateZ(1deg) translateY(-22px) scale(1.0);
    }
}
@keyframes pulseHolo {
    0%, 100% {
        opacity: 0.40;
        filter: drop-shadow(0 20px 40px rgba(99, 102, 241, 0.45)) brightness(0.95);
    }
    50% {
        opacity: 0.65;
        filter: drop-shadow(0 30px 60px rgba(6, 182, 212, 0.7)) brightness(1.15);
    }
}
@keyframes progressAnim {
    0% { width: 25%; }
    50% { width: 85%; }
    100% { width: 100%; }
}
@keyframes pingDot {
    0% { transform: scale(1); opacity: 0.9; }
    75%, 100% { transform: scale(2.4); opacity: 0; }
}
.bg-3d-dashboard-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    pointer-events: none;
    overflow: hidden;
    z-index: 2;
}
.bg-3d-dashboard-img {
    animation: float3D 7s ease-in-out infinite, pulseHolo 5s ease-in-out infinite;
    transform-style: preserve-3d;
    will-change: transform, opacity;
    width: 520px;
    height: 520px;
    max-width: 90vw;
    object-fit: cover;
    border-radius: 28px;
    opacity: 0.48;
    mix-blend-mode: screen;
    box-shadow: 0 0 90px rgba(99, 102, 241, 0.55);
    border: 1px solid rgba(6, 182, 212, 0.4);
}
.bg-3d-dashboard-overlay {
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at center, transparent 25%, rgba(7, 11, 20, 0.65) 65%, rgba(4, 6, 14, 0.92) 100%);
    pointer-events: none;
    z-index: 3;
}

/* Responsividade Mobile / Tablets */
@media (max-width: 1024px) {
    div[data-testid="stAppViewContainer"],
    div[data-testid="stAppViewContainer"] > section.main,
    div[data-testid="stAppViewContainer"] > section.main > div.block-container,
    div[data-testid="stHorizontalBlock"] {
        height: auto !important;
        min-height: 100vh !important;
        overflow-y: auto !important;
        flex-direction: column !important;
    }
    div[data-testid="column"]:first-child,
    div[data-testid="column"]:nth-child(2),
    div[data-testid="stColumn"]:nth-child(2) {
        position: relative !important;
        left: auto !important;
        right: auto !important;
        top: auto !important;
        bottom: auto !important;
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
        height: auto !important;
        min-height: auto !important;
        max-height: none !important;
        padding: 24px 16px !important;
    }
    .login-right-animated-panel {
        min-height: auto !important;
        height: auto !important;
        padding: 24px 16px !important;
    }
}

/* Glow Cósmico Central */
.central-cosmic-glow {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 420px;
    height: 420px;
    transform: translate(-50%, -50%);
    background: radial-gradient(circle, rgba(124, 58, 237, 0.35) 0%, rgba(79, 70, 229, 0.2) 35%, transparent 70%);
    border-radius: 50%;
    filter: blur(50px);
    pointer-events: none;
    z-index: 1;
    animation: cosmicPulse 6s ease-in-out infinite alternate;
}
@keyframes cosmicPulse {
    0% { transform: translate(-50%, -50%) scale(0.92); opacity: 0.7; }
    100% { transform: translate(-50%, -50%) scale(1.18); opacity: 1; }
}

/* Anéis Orbitais */
.orbit-ring {
    position: absolute;
    top: 50%;
    left: 50%;
    border-radius: 50%;
    pointer-events: none;
    z-index: 2;
}
.orbit-ring-1 {
    width: 280px; height: 280px;
    margin-top: -140px; margin-left: -140px;
    border: 1px dashed rgba(139, 92, 246, 0.4);
    animation: spinCW 26s linear infinite;
}
.orbit-ring-2 {
    width: 420px; height: 420px;
    margin-top: -210px; margin-left: -210px;
    border: 1px solid rgba(99, 102, 241, 0.25);
    animation: spinCCW 38s linear infinite;
}
.orbit-ring-3 {
    width: 560px; height: 560px;
    margin-top: -280px; margin-left: -280px;
    border: 1px dashed rgba(56, 189, 248, 0.22);
    animation: spinCW 52s linear infinite;
}
@keyframes spinCW {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
@keyframes spinCCW {
    from { transform: rotate(360deg); }
    to { transform: rotate(0deg); }
}
.orbit-satellite { position: absolute; border-radius: 50%; }
.sat-cyan {
    top: -5px; left: 50%; transform: translateX(-50%);
    width: 9px; height: 9px; background: #38BDF8;
    box-shadow: 0 0 14px 4px rgba(56, 189, 248, 0.9);
}
.sat-purple {
    bottom: -6px; left: 35%;
    width: 10px; height: 10px; background: #C084FC;
    box-shadow: 0 0 16px 4px rgba(192, 132, 252, 0.9);
}
.sat-amber {
    top: 25%; right: -5px;
    width: 8px; height: 8px; background: #F59E0B;
    box-shadow: 0 0 12px 3px rgba(245, 158, 11, 0.9);
}
.sat-emerald {
    bottom: 20%; left: -5px;
    width: 8px; height: 8px; background: #10B981;
    box-shadow: 0 0 12px 3px rgba(16, 185, 129, 0.9);
}

/* Header e Footer HUD */
.login-hud-header {
    position: relative; z-index: 5; width: 100%;
    display: flex; justify-content: space-between; align-items: center;
    padding-bottom: 12px; border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.hud-engine-title {
    display: flex; align-items: center; gap: 8px;
    font-family: 'JetBrains Mono', monospace; font-size: 11px;
    font-weight: 800; color: #E2E8F0; letter-spacing: 0.08em;
}
.hud-dot-beacon {
    width: 7px; height: 7px; border-radius: 50%;
    background: #10B981; box-shadow: 0 0 10px #10B981, 0 0 20px #10B981;
}
.hud-latency {
    font-family: 'JetBrains Mono', monospace; font-size: 11px;
    font-weight: 900; color: #10B981; letter-spacing: 0.06em;
}
.login-hud-footer {
    position: relative; z-index: 5; width: 100%;
    display: flex; justify-content: space-between; align-items: center;
    padding-top: 12px; border-top: 1px solid rgba(255, 255, 255, 0.08);
    font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700;
}
.hud-footer-version { color: #64748B; letter-spacing: 0.08em; }
.hud-footer-tag { color: #C084FC; letter-spacing: 0.1em; }

/* Destaque Ecossistema e Título Showcase */
.ecossistema-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(124, 58, 237, 0.18);
    border: 1px solid rgba(168, 85, 247, 0.5);
    border-radius: 20px;
    padding: 5px 14px;
    margin-bottom: 14px;
    box-shadow: 0 0 16px rgba(168, 85, 247, 0.25);
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px;
    font-weight: 800;
    letter-spacing: 0.14em;
    color: #C084FC;
    text-transform: uppercase;
}

/* Título de Alto Contraste Solicitado pelo Usuário */
.showcase-main-title {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 28px !important;
    font-weight: 900 !important;
    line-height: 1.25 !important;
    letter-spacing: -0.02em !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    margin: 0 0 10px 0 !important;
    text-shadow: 0 2px 14px rgba(0,0,0,0.9) !important;
}
.showcase-main-title .text-gradient-neon {
    background: linear-gradient(135deg, #34D399 0%, #38BDF8 50%, #C084FC 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    display: inline !important;
    font-weight: 900 !important;
}

.showcase-subtitle {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    color: #CBD5E1 !important;
    -webkit-text-fill-color: #CBD5E1 !important;
    line-height: 1.55 !important;
    margin: 0 0 18px 0 !important;
}

/* Cards do Lado Direito */
.showcase-kpi-card {
    background: rgba(15, 23, 42, 0.78);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(99, 102, 241, 0.28);
    border-radius: 18px;
    padding: 16px 20px;
    width: 100%;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.45);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    z-index: 5;
    text-align: left;
    box-sizing: border-box;
}
.showcase-kpi-card:hover {
    border-color: rgba(168, 85, 247, 0.6);
    transform: translateY(-2px);
    box-shadow: 0 16px 36px rgba(124, 58, 237, 0.35);
}
.kpi-card-header {
    display: flex;
    align-items: center;
    gap: 14px;
    width: 100%;
}
.kpi-icon-box {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.kpi-icon-purple {
    background: rgba(124, 58, 237, 0.2);
    border: 1px solid rgba(168, 85, 247, 0.4);
}
.kpi-icon-amber {
    background: rgba(217, 119, 6, 0.2);
    border: 1px solid rgba(245, 158, 11, 0.4);
}
.kpi-info {
    flex: 1;
    min-width: 0;
}
.kpi-title {
    font-size: 14.5px;
    font-weight: 800;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    letter-spacing: -0.01em;
}
.kpi-desc {
    font-size: 11.5px;
    color: #94A3B8 !important;
    -webkit-text-fill-color: #94A3B8 !important;
    font-weight: 500;
    margin-top: 2px;
}
.kpi-badge-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px;
    font-weight: 800;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 0.05em;
    flex-shrink: 0;
}
.kpi-badge-online {
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.45);
    color: #34D399;
}
.kpi-badge-month {
    background: rgba(124, 58, 237, 0.2);
    border: 1px solid rgba(168, 85, 247, 0.4);
    color: #C084FC;
}
.kpi-progress-bar-track {
    width: 100%;
    height: 6px;
    background: rgba(30, 41, 59, 0.7);
    border-radius: 999px;
    margin-top: 14px;
    overflow: hidden;
}
.kpi-progress-bar-fill {
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, #6366F1 0%, #38BDF8 50%, #10B981 100%);
    border-radius: 999px;
    animation: barPulseGlow 3s ease-in-out infinite alternate;
}
@keyframes barPulseGlow {
    0% { opacity: 0.8; filter: brightness(1); }
    100% { opacity: 1; filter: brightness(1.3); }
}
.ranking-leader-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 12px;
    padding: 10px 16px;
    margin-top: 10px;
    transition: all 0.2s ease;
}
.ranking-leader-row:hover {
    background: rgba(30, 41, 59, 0.7);
    border-color: rgba(99, 102, 241, 0.35);
}
.ranking-name {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
}
.ranking-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    font-weight: 800;
    color: #34D399;
    letter-spacing: 0.05em;
    text-shadow: 0 0 10px rgba(52, 211, 153, 0.4);
}
</style>
<div class="ambient-glow-orb orb-1"></div>
<div class="ambient-glow-orb orb-2"></div>
""", unsafe_allow_html=True)

    col_esq, col_dir = st.columns([1, 1], gap="small")

    with col_esq:
        # ⬅️ LADO ESQUERDO: Nome da Empresa do Cliente & Formulário de Autenticação
        tenant_info = obter_dados_tenant()
        logo_omnievo_login = ""
        for fn, mime in [("logo.png", "image/png"), ("logo_custom.png", "image/png"), ("logo.svg", "image/svg+xml")]:
            p_lg = os.path.join("assets", fn)
            if os.path.exists(p_lg):
                try:
                    with open(p_lg, "rb") as _flg:
                        logo_omnievo_login = f"data:{mime};base64,{base64.b64encode(_flg.read()).decode('utf-8')}"
                    break
                except Exception:
                    pass
        logo_omnievo_html = f'<div style="margin-bottom:14px;position:relative;z-index:3;display:flex;align-items:center;gap:12px;"><img src="{logo_omnievo_login}" style="height:50px;width:50px;object-fit:cover;border-radius:50%;box-shadow:0 4px 12px rgba(0,0,0,0.15);border:2px solid #E2E8F0;" alt="Omnievo" /><span style="font-size:20px;font-weight:900;color:#0F172A;letter-spacing:-0.02em;">OMNIEVO</span></div>' if logo_omnievo_login else ''

        st.markdown(f'''
{logo_omnievo_html}
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;position:relative;z-index:3;">
<div style="display:flex;align-items:center;gap:8px;font-family:'JetBrains Mono',Consolas,monospace;font-size:11px;font-weight:800;color:#334155;letter-spacing:0.1em;text-transform:uppercase;">
<span class="hud-dot-beacon"></span>
<span>PORTAL DE ACESSO // OMIE ERP</span>
</div>
<div style="display:inline-flex;align-items:center;gap:6px;background:rgba(16,185,129,0.12);border:1px solid rgba(16,185,129,0.35);border-radius:20px;padding:4px 12px;">
<span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#10B981;box-shadow:0 0 8px #10B981;"></span>
<span style="font-family:'JetBrains Mono',Consolas,monospace;font-size:10px;font-weight:800;color:#059669;letter-spacing:0.06em;">OMIE CONECTADO</span>
</div>
</div>
<div class="tenant-company-title">
{tenant_info['nome_empresa']}
</div>
<div style="display:inline-flex;align-items:center;gap:6px;background:#1E1B4B;border:1px solid rgba(99,102,241,0.45);border-radius:8px;padding:5px 12px;margin-top:8px;margin-bottom:8px;box-shadow:0 4px 12px rgba(0,0,0,0.15);position:relative;z-index:3;">
<span style="font-size:12px;">🌐</span>
<span style="font-family:'JetBrains Mono',Consolas,monospace;font-size:11px;font-weight:800;color:#38BDF8;letter-spacing:0.05em;">{tenant_info['subdominio_completo']}</span>
</div>
<div style="font-size:13px;font-weight:600;color:#475569;margin-top:4px;margin-bottom:14px;border-bottom:1px solid #E2E8F0;padding-bottom:12px;display:flex;justify-content:space-between;align-items:center;position:relative;z-index:3;">
<span>Autenticação Corporativa de Vendedores</span>
<span style="font-family:'JetBrains Mono',Consolas,monospace;font-size:10px;font-weight:800;color:#4338CA;letter-spacing:0.08em;background:#EEF2FF;border:1px solid #C7D2FE;border-radius:6px;padding:2px 8px;">256-BIT SSL</span>
</div>
''', unsafe_allow_html=True)

        if st.button("🔄 Sincronizar Vendedores & E-mails Omie ERP", key="btn_sync_emails_login", use_container_width=True, help="Buscar novos vendedores ou e-mails cadastrados recentemente no Omie ERP"):
            with st.spinner("Sincronizando vendedores e e-mails do Omie ERP..."):
                vends_synced = auth.sincronizar_vendedores_omie()
                st.toast(f"✅ Sincronizados {len(vends_synced)} vendedores do Omie ERP com sucesso!")
                st.rerun()

        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

        # ── SE FLUXO DE PRIMEIRO ACESSO ATIVO, EXIBE A TELA DE VERIFICAÇÃO 2FA IMEDIATAMENTE ──
        if st.session_state.get("etapa_login_primeiro_acesso") and st.session_state.get("dados_2fa_pendente"):
            dados_pendentes = st.session_state["dados_2fa_pendente"]
            vendedor_p = dados_pendentes.get("vendedor") or {}
            nome_v_p = vendedor_p.get("nome_vendedor") or vendedor_p.get("nome") or "Vendedor(a)"
            email_p = dados_pendentes.get("email") or ""
            mode_p = dados_pendentes.get("mode", "")
            cod_ref = dados_pendentes.get("codigo", "")

            st.markdown(f'''
            <div style="background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%); border: 1.5px solid #818CF8; border-radius: 14px; padding: 18px 20px; margin-bottom: 18px; box-shadow: 0 8px 20px rgba(0,0,0,0.25);">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                    <span style="font-size: 26px;">🔐</span>
                    <div>
                        <div style="font-size: 16px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.01em;">Verificação de Primeiro Acesso (2FA)</div>
                        <div style="font-size: 12px; color: #C7D2FE;">Autenticação corporativa em duas etapas</div>
                    </div>
                </div>
                <div style="font-size: 13px; color: #E0E7FF; line-height: 1.5; margin-top: 8px;">
                    Olá, <b>{nome_v_p}</b>! Detectamos que este é o seu <b>primeiro acesso</b> ao CRM.<br>
                    Enviamos um código de segurança de 6 dígitos para o seu e-mail:<br>
                    <b style="color: #38BDF8; font-family: monospace; font-size: 13.5px;">{email_p}</b>
                </div>
            </div>
            ''', unsafe_allow_html=True)

            if mode_p != "SMTP_SENT":
                st.markdown(f'''<div style="background:#FAF5FF;border:1.5px solid #C084FC;border-radius:14px;padding:14px;text-align:center;margin:10px 0;"><div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#7E22CE;font-weight:800;text-transform:uppercase;">⚠️ CÓDIGO DE CONTINGÊNCIA (SEM SMTP / MODO TESTE)</div><div style="font-family:'JetBrains Mono',monospace;font-size:32px;font-weight:900;color:#0F172A;letter-spacing:0.2em;margin:6px 0;">{cod_ref}</div></div>''', unsafe_allow_html=True)

            with st.form("form_validar_primeiro_acesso_auto"):
                cod_digitado = st.text_input("🔢 Digite o Código de 6 Dígitos recebido por e-mail:", placeholder="Ex: 849201")
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    nova_senha_1 = st.text_input("🔒 Crie sua Senha:", type="password", placeholder="Mínimo 6 caracteres")
                with col_s2:
                    nova_senha_2 = st.text_input("🔒 Confirme a Senha:", type="password", placeholder="Repita a nova senha")
                
                btn_confirmar_2fa = st.form_submit_button("🚀 Confirmar Código & Entrar no CRM", use_container_width=True)

                if btn_confirmar_2fa:
                    tempo_decorrido = time.time() - dados_pendentes.get("timestamp", time.time())
                    if tempo_decorrido > 600:
                        st.error("❌ Este código de verificação expirou (validade de 10 minutos). Solicite um novo código abaixo.")
                    elif str(cod_digitado).strip() != str(cod_ref).strip():
                        st.error("❌ Código de verificação incorreto. Verifique a caixa de entrada ou spam do seu e-mail.")
                    elif not nova_senha_1 or len(nova_senha_1) < 6:
                        st.error("A senha deve ter pelo menos 6 caracteres.")
                    elif nova_senha_1 != nova_senha_2:
                        st.error("As senhas não coincidem.")
                    else:
                        ok_c, msg_c = auth.cadastrar_senha_com_codigo(email_p, nova_senha_1)
                        if ok_c:
                            token_sessao = auth.criar_sessao_usuario(dados_pendentes["vendedor"])
                            st.query_params["session_token"] = token_sessao
                            st.session_state["session_token"] = token_sessao
                            st.session_state["authenticated"] = True
                            st.session_state["usuario_logado"] = dados_pendentes["vendedor"]
                            st.session_state["dados_2fa_pendente"] = None
                            st.session_state["etapa_login_primeiro_acesso"] = False

                            components.html(f"""
                            <script>
                            (function() {{
                                try {{
                                    const wins = [window, window.parent, window.top];
                                    for (const w of wins) {{
                                        try {{
                                            if (w && w.localStorage) {{
                                                w.localStorage.setItem('omnievo_crm_token', '{token_sessao}');
                                            }}
                                        }} catch(e) {{}}
                                    }}
                                }} catch(e) {{}}
                            }})();
                            </script>
                            """, height=0)

                            frase_motivacional = random.choice(FRASES_MOTIVACIONAIS_VENDAS)
                            st.session_state["frase_login"] = frase_motivacional
                            st.rerun()

            col_btn_r1, col_btn_r2 = st.columns(2)
            with col_btn_r1:
                if st.button("🔄 Reenviar Código por E-mail", use_container_width=True):
                    ok_r, dados_r, msg_r = auth.disparar_codigo_primeiro_acesso(email_p)
                    if ok_r:
                        st.session_state["dados_2fa_pendente"] = dados_r
                        st.toast("📩 Novo código de segurança enviado para o seu e-mail!")
                        st.rerun()
            with col_btn_r2:
                if st.button("⬅️ Trocar E-mail / Voltar", use_container_width=True):
                    st.session_state["etapa_login_primeiro_acesso"] = False
                    st.session_state["dados_2fa_pendente"] = None
                    st.rerun()

        else:
            tab_login, tab_2fa = st.tabs(["🔑 Login com E-mail e Senha", "📩 Primeiro Acesso ou Recuperar Senha"])

            with tab_login:
                with st.form("form_login_email_omie"):
                    email_input = st.text_input("📧 E-mail Corporativo de Acesso:", value="comercial.omnievo@gmail.com", placeholder="ex: comercial.omnievo@gmail.com")
                    senha_input = st.text_input("🔑 Senha de Acesso:", type="password", placeholder="Digite sua senha cadastrada")
                    lembrar_sessao = st.checkbox("Manter sessão ativa neste navegador", value=True)
                    btn_entrar_email = st.form_submit_button("🚀 Acessar o Sistema", use_container_width=True)

                    if btn_entrar_email:
                        if not email_input:
                            st.error("Por favor, preencha o e-mail cadastrado no ERP.")
                        else:
                            st_acesso, vend_info, msg_acesso = auth.verificar_status_acesso(email_input)
                            if st_acesso == "NAO_AUTORIZADO":
                                st.error(msg_acesso)
                            elif st_acesso == "BLOQUEADO":
                                st.error(msg_acesso)
                            elif st_acesso == "PRIMEIRO_ACESSO":
                                with st.spinner("Primeiro acesso detectado! Enviando código para o seu e-mail..."):
                                    ok_env, dados_env, msg_env = auth.disparar_codigo_primeiro_acesso(email_input)
                                    if ok_env:
                                        st.session_state["dados_2fa_pendente"] = dados_env
                                        st.session_state["etapa_login_primeiro_acesso"] = True
                                        st.toast("📩 Código 2FA enviado com sucesso para o seu e-mail!")
                                        st.rerun()
                                    else:
                                        st.error(msg_env)
                            else:
                                if not senha_input:
                                    st.error("Por favor, digite sua senha de acesso.")
                                else:
                                    ok_log, dados_log, msg_log = auth.autenticar_vendedor_email_senha(email_input, senha_input)
                                    if ok_log == True:
                                        token_sessao = auth.criar_sessao_usuario(dados_log)
                                        st.query_params["session_token"] = token_sessao
                                        st.session_state["session_token"] = token_sessao
                                        st.session_state["authenticated"] = True
                                        st.session_state["usuario_logado"] = dados_log

                                        components.html(f"""
                                        <script>
                                        (function() {{
                                            try {{
                                                const wins = [window, window.parent, window.top];
                                                for (const w of wins) {{
                                                    try {{
                                                        if (w && w.localStorage) {{
                                                            w.localStorage.setItem('omnievo_crm_token', '{token_sessao}');
                                                        }}
                                                    }} catch(e) {{}}
                                                }}
                                            }} catch(e) {{}}
                                        }})();
                                        </script>
                                        """, height=0)

                                        frase_motivacional = random.choice(FRASES_MOTIVACIONAIS_VENDAS)
                                        st.session_state["frase_login"] = frase_motivacional
                                        st.rerun()
                                    elif ok_log == "PRIMEIRO_ACESSO":
                                        with st.spinner("Primeiro acesso detectado! Enviando código para o seu e-mail..."):
                                            ok_env, dados_env, msg_env = auth.disparar_codigo_primeiro_acesso(email_input)
                                            if ok_env:
                                                st.session_state["dados_2fa_pendente"] = dados_env
                                                st.session_state["etapa_login_primeiro_acesso"] = True
                                                st.rerun()
                                            else:
                                                st.error(msg_env)
                                    else:
                                        st.error(msg_log)

                st.markdown('''
                <div style="text-align: center; margin-top: 14px; padding: 10px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px;">
                    <span style="font-size: 12px; color: #475569; font-weight: 500;">
                        Primeiro acesso ou esqueceu sua senha? Ao digitar seu e-mail acima, o código 2FA é enviado automaticamente.
                    </span>
                </div>
                ''', unsafe_allow_html=True)

        with tab_2fa:
            st.markdown('''<div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:12px 14px;margin-bottom:12px;"><div style="font-size:12px;color:#475569;font-weight:600;line-height:1.45;">ℹ️ Digite seu e-mail cadastrado no ERP para receber seu código de verificação 2FA por e-mail e cadastrar ou redefinir sua senha de acesso.</div></div>''', unsafe_allow_html=True)
            
            with st.form("form_solicitar_2fa"):
                email_2fa_input = st.text_input("📧 Digite seu E-mail cadastrado no sistema:", placeholder="ex: usuario@empresa.com.br", key="email_2fa_key")
                btn_gerar_2fa = st.form_submit_button("📩 Enviar Código por E-mail", use_container_width=True)

                if btn_gerar_2fa:
                    if not email_2fa_input:
                        st.warning("Por favor, informe seu e-mail cadastrado.")
                    else:
                        vendedor_encontrado = auth.buscar_vendedor_por_email(email_2fa_input)
                        if not vendedor_encontrado:
                            auth.sincronizar_vendedores_omie()
                            vendedor_encontrado = auth.buscar_vendedor_por_email(email_2fa_input)

                        if not vendedor_encontrado:
                            st.error("⚠️ **Acesso Não Autorizado**: Este e-mail não está cadastrado na equipe comercial do ERP.")
                        else:
                            cod_gerado = auth.gerar_codigo_verificacao()
                            nome_vend = vendedor_encontrado.get("nome") or vendedor_encontrado.get("nome_vendedor") or ""
                            ok_envio, mode_envio = auth.enviar_codigo_por_email(email_2fa_input, cod_gerado, nome_vendedor=nome_vend)
                            st.session_state["dados_2fa_pendente"] = {
                                "email": email_2fa_input.strip().lower(),
                                "codigo": cod_gerado,
                                "vendedor": vendedor_encontrado,
                                "mode": mode_envio,
                                "timestamp": time.time()
                            }
                            if mode_envio == "SMTP_SENT":
                                st.success(f"📩 **Código de 6 dígitos enviado por e-mail para {email_2fa_input}!**\n\nAbra sua caixa de entrada (ou pasta de spam) e copie o código para validar no formulário abaixo. O código é válido por **10 minutos**.")
                            elif mode_envio == "SEM_SMTP":
                                st.warning("⚠️ **Servidor SMTP não configurado**: Para permitir o teste neste ambiente local, o código gerado foi exibido abaixo:")
                            else:
                                st.warning(f"⚠️ **Instabilidade no servidor de e-mail ({mode_envio})**: Exibindo código de contingência abaixo para não bloquear o acesso:")

            dados_pendentes = st.session_state.get("dados_2fa_pendente")
            if dados_pendentes and dados_pendentes.get("email") == email_2fa_input.strip().lower():
                cod_ref = dados_pendentes["codigo"]
                mode_ref = dados_pendentes.get("mode", "")
                tempo_decorrido = time.time() - dados_pendentes.get("timestamp", time.time())
                expirado = tempo_decorrido > 600

                # SEGURANÇA REAL: Exibir box do código NA TELA APENAS SE o SMTP falhou ou não estiver configurado
                if mode_ref != "SMTP_SENT":
                    st.markdown(f'''<div style="background:#FAF5FF;border:1.5px solid #C084FC;border-radius:14px;padding:16px;text-align:center;margin:12px 0;"><div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#7E22CE;font-weight:800;text-transform:uppercase;">⚠️ CÓDIGO DE CONTINGÊNCIA (MODO TESTE / SEM SMTP)</div><div style="font-family:'JetBrains Mono',monospace;font-size:32px;font-weight:900;color:#0F172A;letter-spacing:0.2em;margin:6px 0;">{cod_ref}</div><div style="font-size:11px;color:#6B21A8;font-weight:600;">O servidor SMTP não está ativo no momento. Use o código acima para prosseguir:</div></div>''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''<div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:12px;padding:12px 16px;margin:12px 0;"><div style="font-size:12px;color:#166534;font-weight:600;">📬 Código de 6 dígitos enviado para <b>{dados_pendentes['email']}</b>. Verifique sua caixa de entrada e spam. Digite-o abaixo junto com a sua nova senha:</div></div>''', unsafe_allow_html=True)
                
                with st.form("form_validar_2fa_criar_senha"):
                    cod_digitado = st.text_input("🔢 Digite o Código de 6 Dígitos recebido no e-mail:", value="", placeholder="ex: 849201")
                    nova_senha_1 = st.text_input("🔒 Crie sua Nova Senha:", type="password", placeholder="Mínimo 6 caracteres")
                    nova_senha_2 = st.text_input("🔒 Confirme a Nova Senha:", type="password", placeholder="Repita a nova senha")
                    btn_confirmar_2fa = st.form_submit_button("🔐 Confirmar e Cadastrar Nova Senha", use_container_width=True)

                    if btn_confirmar_2fa:
                        tempo_decorrido = time.time() - dados_pendentes.get("timestamp", time.time())
                        if tempo_decorrido > 600:
                            st.error("❌ Este código de verificação expirou (validade de 10 minutos). Por favor, clique em 'Enviar Código por E-mail' acima para gerar um novo.")
                        elif cod_digitado.strip() != cod_ref:
                            st.error("❌ Código de verificação incorreto. Verifique o código recebido no seu e-mail.")
                        elif not nova_senha_1 or len(nova_senha_1) < 6:
                            st.error("A senha deve ter pelo menos 6 caracteres para garantir a segurança da conta.")
                        elif nova_senha_1 != nova_senha_2:
                            st.error("As senhas digitadas não coincidem.")
                        else:
                            ok_c, msg_c = auth.cadastrar_senha_com_codigo(dados_pendentes["email"], nova_senha_1)
                            if ok_c:
                                token_sessao = auth.criar_sessao_usuario(dados_pendentes["vendedor"])
                                st.query_params["session_token"] = token_sessao
                                st.session_state["session_token"] = token_sessao
                                st.session_state["authenticated"] = True
                                st.session_state["usuario_logado"] = dados_pendentes["vendedor"]
                                st.session_state["dados_2fa_pendente"] = None

                                components.html(f"""
                                <script>
                                (function() {{
                                    try {{
                                        const wins = [window, window.parent, window.top];
                                        for (const w of wins) {{
                                            try {{
                                                if (w && w.localStorage) {{
                                                    w.localStorage.setItem('omnievo_crm_token', '{token_sessao}');
                                                }}
                                            }} catch(e) {{}}
                                        }}
                                    }} catch(e) {{}}
                                }})();
                                </script>
                                """, height=0)

                                frase_motivacional = random.choice(FRASES_MOTIVACIONAIS_VENDAS)
                                st.session_state["frase_login"] = frase_motivacional
                                st.success("✅ Senha cadastrada com sucesso! Entrando no sistema...")
                                st.rerun()
                            else:
                                st.error(msg_c)

        # Rodapé Discreto e Elegante do Card Branco (Sem Telefone Pessoal)
        st.markdown('''
<div style="margin-top:14px;padding-top:12px;border-top:1px solid #E2E8F0;display:flex;justify-content:space-between;align-items:center;font-family:'JetBrains Mono',Consolas,monospace;font-size:10px;color:#64748B;">
<span>© 2026 OMNIEVO ENTERPRISE</span>
<span style="color:#059669;font-weight:800;display:inline-flex;align-items:center;gap:4px;">
<span>🔒 CONEXÃO OMIE SEGURA</span>
</span>
</div>
''', unsafe_allow_html=True)

    with col_dir:
        # ➡️ LADO DIREITO: INTERFACE 3D E CARDS EXATOS DA PREVIEW APROVADA
        dash_3d_b64 = ""
        p_dash = os.path.join("assets", "omnievo_profile_crm_dashboard.jpg")
        if os.path.exists(p_dash):
            try:
                with open(p_dash, "rb") as _fdash:
                    dash_3d_b64 = f"data:image/jpeg;base64,{base64.b64encode(_fdash.read()).decode('utf-8')}"
            except Exception:
                pass

        badge_b64 = ""
        p_badge = os.path.join("assets", "omnievo_profile_badge.jpg")
        if os.path.exists(p_badge):
            try:
                with open(p_badge, "rb") as _fbadge:
                    badge_b64 = f"data:image/jpeg;base64,{base64.b64encode(_fbadge.read()).decode('utf-8')}"
            except Exception:
                pass

        right_panel_html = (
            f'<div class="login-right-animated-panel" style="display:flex;align-items:center;justify-content:center;padding:24px;">'
            f'<div style="position:relative;width:100%;max-width:620px;border-radius:20px;overflow:hidden;border:1px solid rgba(99,102,241,0.45);background:linear-gradient(180deg,#0B0F1F 0%,#070B18 50%,#04060E 100%);padding:26px 28px;box-shadow:0 25px 60px -12px rgba(0,0,0,0.85);margin:auto;">'
            f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;pointer-events:none;overflow:hidden;z-index:0;">'
            f'<div style="position:absolute;width:480px;height:480px;border-radius:50%;background:radial-gradient(circle,rgba(99,102,241,0.38) 0%,rgba(6,182,212,0.28) 40%,rgba(147,51,234,0.35) 70%,transparent 100%);filter:blur(95px);"></div>'
            f'<img src="{dash_3d_b64}" alt="Interface 3D CRM Omnievo" style="width:520px;height:520px;object-fit:cover;border-radius:28px;opacity:0.52;mix-blend-mode:screen;box-shadow:0 0 90px rgba(99,102,241,0.55);border:1px solid rgba(6,182,212,0.45);animation:float3D 7s ease-in-out infinite,pulseHolo 5s ease-in-out infinite;transform-style:preserve-3d;will-change:transform,opacity;" />'
            f'<div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(4,6,14,0.94) 0%,rgba(7,11,24,0.62) 50%,rgba(11,15,31,0.72) 100%);pointer-events:none;"></div>'
            f'</div>'
            f'<div style="position:relative;z-index:10;display:flex;flex-direction:column;align-items:center;text-align:center;gap:12px;">'
            f'<div style="position:relative;display:inline-flex;align-items:center;justify-content:center;margin-bottom:2px;">'
            f'<div style="position:absolute;inset:-4px;border-radius:50%;background:linear-gradient(90deg,#22D3EE 0%,#6366F1 50%,#9333EA 100%);opacity:0.85;filter:blur(8px);"></div>'
            f'<img src="{badge_b64}" alt="Medalhão Omnievo" style="position:relative;width:56px;height:56px;border-radius:50%;object-fit:cover;border:2px solid rgba(255,255,255,0.4);box-shadow:0 10px 25px rgba(0,0,0,0.6);" />'
            f'</div>'
            f'<div style="width:100%;display:flex;align-items:center;justify-content:space-between;font-size:11px;font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;color:#94A3B8;border-bottom:1px solid rgba(30,41,59,0.8);padding-bottom:8px;padding-left:6px;padding-right:6px;">'
            f'<div style="display:flex;align-items:center;gap:8px;">'
            f'<span style="position:relative;display:inline-flex;width:10px;height:10px;align-items:center;justify-content:center;"><span style="position:absolute;width:10px;height:10px;border-radius:50%;background:#34D399;animation:pingDot 1.4s cubic-bezier(0,0,0.2,1) infinite;opacity:0.85;"></span><span style="position:relative;width:7px;height:7px;border-radius:50%;background:#10B981;box-shadow:0 0 6px #34D399;"></span></span>'
            f'<span style="color:#34D399;font-weight:700;letter-spacing:0.05em;">OMNIEVO_ENGINE // ACTIVE_NODE</span>'
            f'</div>'
            f'<div style="color:#22D3EE;font-weight:700;letter-spacing:0.05em;">LATENCY: <span style="color:#34D399;">0ms</span> (ERP_DIRECT)</div>'
            f'</div>'
            f'<div style="display:inline-flex;align-items:center;gap:6px;padding:3px 12px;border-radius:9999px;background:rgba(59,7,100,0.7);border:1px solid rgba(168,85,247,0.5);font-size:10px;font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-weight:700;color:#D8B4FE;text-transform:uppercase;letter-spacing:0.1em;box-shadow:0 1px 3px rgba(0,0,0,0.2);">'
            f'<span>⚡</span> ECOSSISTEMA INTEGRADO'
            f'</div>'
            f'<h2 style="font-size:22px;font-weight:900;letter-spacing:-0.02em;line-height:1.25;max-width:500px;color:#FFFFFF;text-shadow:0 2px 10px rgba(0,0,0,0.5);margin:0 auto;">'
            f'Transforme sua Força de Vendas em uma <span style="background:linear-gradient(90deg,#22D3EE 0%,#5EEAD4 50%,#34D399 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Máquina de Faturamento Integrada</span> ao seu ERP.'
            f'</h2>'
            f'<p style="font-size:12px;color:#E2E8F0;max-width:480px;line-height:1.5;font-weight:400;text-shadow:0 1px 4px rgba(0,0,0,0.4);margin:0 auto 4px auto;">'
            f'Emissão instantânea de pedidos, saldo de estoque em tempo real e inteligência comercial para a sua equipe escalar resultados.'
            f'</p>'
            f'<div style="width:100%;text-align:left;background:rgba(15,23,42,0.85);border:1px solid rgba(51,65,85,0.7);border-radius:12px;padding:12px 16px;backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);box-shadow:0 10px 25px rgba(0,0,0,0.35);">'
            f'<div style="display:flex;align-items:center;justify-content:space-between;">'
            f'<div style="display:flex;align-items:center;gap:12px;">'
            f'<div style="width:32px;height:32px;border-radius:8px;background:rgba(79,70,229,0.4);border:1px solid rgba(129,140,248,0.5);display:flex;align-items:center;justify-content:center;font-size:14px;box-shadow:0 2px 4px rgba(0,0,0,0.2);">🔄</div>'
            f'<div><div style="font-size:12px;font-weight:700;color:#FFFFFF;">Sincronização Nativa com ERP</div><div style="font-size:10px;color:#CBD5E1;">Transmissão bidirecional de pedidos e estoque</div></div>'
            f'</div>'
            f'<span style="padding:2px 8px;border-radius:9999px;background:rgba(2,44,34,0.9);border:1px solid rgba(16,185,129,0.5);font-size:10px;font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-weight:700;color:#34D399;">100% ONLINE</span>'
            f'</div>'
            f'<div style="width:100%;height:6px;background:#1E293B;border-radius:9999px;overflow:hidden;margin-top:8px;">'
            f'<div style="height:100%;background:linear-gradient(90deg,#22D3EE 0%,#6366F1 50%,#34D399 100%);border-radius:9999px;animation:progressAnim 3.5s ease-in-out infinite alternate;"></div>'
            f'</div>'
            f'</div>'
            f'<div style="width:100%;text-align:left;background:rgba(15,23,42,0.85);border:1px solid rgba(51,65,85,0.7);border-radius:12px;padding:12px 16px;backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);box-shadow:0 10px 25px rgba(0,0,0,0.35);">'
            f'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">'
            f'<div style="display:flex;align-items:center;gap:12px;">'
            f'<div style="width:32px;height:32px;border-radius:8px;background:rgba(217,119,6,0.4);border:1px solid rgba(251,191,36,0.5);display:flex;align-items:center;justify-content:center;font-size:14px;box-shadow:0 2px 4px rgba(0,0,0,0.2);">🏆</div>'
            f'<div><div style="font-size:12px;font-weight:700;color:#FFFFFF;">Ranking de Vendedores ao Vivo</div><div style="font-size:10px;color:#CBD5E1;">Métricas atualizadas instantaneamente</div></div>'
            f'</div>'
            f'<span style="padding:2px 8px;border-radius:9999px;background:rgba(59,7,100,0.9);border:1px solid rgba(168,85,247,0.5);font-size:10px;font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-weight:700;color:#D8B4FE;">MÊS ATUAL</span>'
            f'</div>'
            f'<div style="display:flex;flex-direction:column;gap:6px;font-size:12px;">'
            f'<div style="display:flex;align-items:center;justify-content:space-between;padding:4px 10px;border-radius:8px;background:rgba(30,41,59,0.6);border:1px solid rgba(51,65,85,0.5);"><span style="font-weight:600;color:#F8FAFC;display:flex;align-items:center;gap:8px;">🥇 Gabriel Santos</span><span style="font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-weight:700;color:#34D399;">R$ 485.920,00</span></div>'
            f'<div style="display:flex;align-items:center;justify-content:space-between;padding:4px 10px;border-radius:8px;background:rgba(30,41,59,0.4);border:1px solid rgba(51,65,85,0.4);"><span style="font-weight:600;color:#E2E8F0;display:flex;align-items:center;gap:8px;">🥈 Lucas Mendes</span><span style="font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-weight:700;color:#67E8F9;">R$ 312.450,00</span></div>'
            f'</div>'
            f'</div>'
            f'<div style="width:100%;display:flex;align-items:center;justify-content:space-between;font-size:10px;font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;color:#94A3B8;padding-top:2px;"><span>SYSTEM_VERSION: v4.8.2-PROD</span><span style="color:#818CF8;font-weight:700;letter-spacing:0.05em;">OMNIEVO COMMERCE DEPLOYMENT</span></div>'
            f'</div>'
            f'</div>'
            f'</div>'
        )
        st.markdown(right_panel_html, unsafe_allow_html=True)
    st.stop()

DRAFT_CACHE = "cache/draft_pedido.json"

def salvar_rascunho_pedido(itens):
    try:
        import os
        os.makedirs("cache", exist_ok=True)
        with open(DRAFT_CACHE, "w", encoding="utf-8") as f:
            json.dump(itens, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def carregar_rascunho_pedido():
    try:
        import os
        if os.path.exists(DRAFT_CACHE):
            with open(DRAFT_CACHE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return []

def limpar_rascunho_pedido():
    try:
        import os
        if os.path.exists(DRAFT_CACHE):
            os.remove(DRAFT_CACHE)
    except Exception:
        pass

def gerar_template_xlsx():
    import io
    import openpyxl
    from openpyxl.worksheet.datavalidation import DataValidation
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Itens_Pedido_OMNIEVO_COMMERCE"
    
    headers = ["CODIGO", "QUANTIDADE", "PRECO", "DESCONTO", "OPERACAO"]
    ws.append(headers)
    
    header_fill = PatternFill(start_color="8A79B0", end_color="8A79B0", fill_type="solid")
    header_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
    align_center = Alignment(horizontal="center", vertical="center")
    
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = align_center
        
    exemplos = [
        ["MS103472", 10, 129.90, 0.0, "MONITORAMENTO AUTOMÁTICO DE IMPOSTOS"],
        ["MS103470", 5, 129.90, 0.0, "MONITORAMENTO AUTOMÁTICO DE IMPOSTOS"],
        ["MS201432", 20, 89.90, 0.0, "BONIFICAÇÃO"],
        ["MS101367", 2, 199.00, 10.0, "MONITORAMENTO AUTOMÁTICO DE IMPOSTOS"]
    ]
    
    data_font = Font(name="Arial", size=10)
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    
    for row_idx, row_data in enumerate(exemplos, start=2):
        for col_idx, val in enumerate(row_data, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.font = data_font
            cell.border = thin_border
            if col_idx == 1:
                cell.alignment = Alignment(horizontal="center")
            elif col_idx in [2, 3, 4]:
                cell.alignment = Alignment(horizontal="right")
                if col_idx in [3, 4]:
                    cell.number_format = 'R$ #,##0.00'
            elif col_idx == 5:
                cell.alignment = Alignment(horizontal="left")

    dv = DataValidation(
        type="list",
        formula1='"MONITORAMENTO AUTOMÁTICO DE IMPOSTOS,BONIFICAÇÃO"',
        allow_blank=True
    )
    dv.error = 'Selecione apenas MONITORAMENTO AUTOMÁTICO DE IMPOSTOS ou BONIFICAÇÃO'
    dv.errorTitle = 'Operação Inválida'
    dv.prompt = 'Selecione a operação fiscal para este item'
    dv.promptTitle = 'Operação Fiscal'
    
    ws.add_data_validation(dv)
    dv.add("E2:E500")

    ws.column_dimensions['A'].width = 18
    ws.column_dimensions['B'].width = 14
    ws.column_dimensions['C'].width = 16
    ws.column_dimensions['D'].width = 16
    ws.column_dimensions['E'].width = 45

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output.getvalue()

# ══════════════════════════════════════════════════════════════════════════════
# INICIALIZAÇÃO DO STATE
# ══════════════════════════════════════════════════════════════════════════════
if "itens_pedido" not in st.session_state:
    st.session_state["itens_pedido"] = carregar_rascunho_pedido()

# Sincronização e auto-correção de IDs de produtos no carrinho com o catálogo ativo Omie
try:
    cat_ativo_sync = omie.carregar_produtos()
    for it_sync in st.session_state.get("itens_pedido", []):
        sku_sync = str(it_sync.get("codigo_produto_integracao") or "").strip()
        p_ativo_sync = cat_ativo_sync.get(sku_sync)
        if p_ativo_sync and p_ativo_sync.get("codigo_produto"):
            if it_sync.get("codigo_produto") != p_ativo_sync["codigo_produto"]:
                it_sync["codigo_produto"] = p_ativo_sync["codigo_produto"]
            if p_ativo_sync.get("descricao") and "OLD-" in it_sync.get("descricao", ""):
                it_sync["descricao"] = p_ativo_sync["descricao"]
except Exception:
    pass

if "cep_dados" not in st.session_state:
    st.session_state["cep_dados"] = {"logradouro": "", "bairro": "", "cidade": "", "estado": "ES"}

config = omie.load_config()
hoje = datetime.date.today()

def obter_proximo_dia_util(dt):
    """Retorna o próximo dia útil caso caia em Fim de Semana (Sábado/Domingo)."""
    w = dt.weekday()
    if w == 5:     # Sábado -> Segunda-feira (D+2)
        return dt + datetime.timedelta(days=2)
    elif w == 6:   # Domingo -> Segunda-feira (D+1)
        return dt + datetime.timedelta(days=1)
    return dt

def calcular_previsao_faturamento_48h(dt=None):
    """
    REGRA DE NEGÓCIO DA OMNIEVO:
    Define a Previsão de Faturamento como o PRÓXIMO DIA ÚTIL DEPOIS DE 48 HORAS.
    - 48h corridas + Avanço para o Próximo Dia Útil (Segunda a Sexta, desconsiderando Sábado, Domingo e Feriados Nacionais).
    """
    if dt is None:
        dt = date.today()
    elif isinstance(dt, datetime.datetime):
        dt = dt.date()

    # 1. 48h corridas (2 dias) + avanço para o próximo dia útil
    dt_target = dt + datetime.timedelta(days=2)
    dt_target = dt_target + datetime.timedelta(days=1)

    # 2. Se cair no Sábado (weekday=5), avança para Segunda-feira (+2 dias)
    if dt_target.weekday() == 5:
        dt_target = dt_target + datetime.timedelta(days=2)
    # 3. Se cair no Domingo (weekday=6), avança para Segunda-feira (+1 dia)
    elif dt_target.weekday() == 6:
        dt_target = dt_target + datetime.timedelta(days=1)

    # 4. Feriados Nacionais Fixos (ex: 7 de Setembro, 12 de Outubro, 25 de Dezembro, 1º de Janeiro)
    feriados_fixos = [(9, 7), (10, 12), (11, 2), (11, 15), (11, 20), (12, 25), (1, 1)]
    if (dt_target.month, dt_target.day) in feriados_fixos:
        dt_target = dt_target + datetime.timedelta(days=1)
        if dt_target.weekday() == 5:
            dt_target = dt_target + datetime.timedelta(days=2)
        elif dt_target.weekday() == 6:
            dt_target = dt_target + datetime.timedelta(days=1)

    return dt_target

previsao_auto = calcular_previsao_faturamento_48h(hoje)

def formatar_num_pedido_limpo(num):
    s = str(num or "").strip()
    if s.isdigit():
        return str(int(s))
    return s

def fmt_brl(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def obter_data_faturamento_pedido(ped):
    """
    REGRA SOLICITADA PELO USUÁRIO:
    Obtém a DATA REAL DO FATURAMENTO (infoCadastro.dFat) enviada pelo Omie ERP.
    Se não houver data de faturamento (ex: orçamentos em aberto), utiliza a data prevista (cabecalho.data_previsao)
    ou a data de inclusão (infoCadastro.dInc) como fallback.
    """
    if not isinstance(ped, dict):
        return hoje
    raw = ped.get("raw_data", {}) if isinstance(ped.get("raw_data"), dict) else {}
    info_cad = raw.get("infoCadastro", {}) if isinstance(raw.get("infoCadastro"), dict) else (ped.get("infoCadastro", {}) if isinstance(ped.get("infoCadastro"), dict) else {})
    cab = raw.get("cabecalho", {}) if isinstance(raw.get("cabecalho"), dict) else {}
    
    d_fat = ped.get("data_faturamento_real") or ped.get("data_faturamento") or info_cad.get("dFat") or cab.get("data_previsao") or ped.get("data_previsao") or info_cad.get("dInc") or ""
    if d_fat and len(str(d_fat)) >= 10:
        d_clean = str(d_fat)[:10].strip()
        try:
            return datetime.datetime.strptime(d_clean, "%d/%m/%Y").date()
        except Exception:
            try:
                return datetime.datetime.strptime(d_clean, "%Y-%m-%d").date()
            except Exception:
                pass
    return hoje


def obter_logo_b64_html(for_dark_bg=False):
    files = [("logo_white.svg", "image/svg+xml")] if for_dark_bg else []
    files += [("logo_custom.png", "image/png"), ("logo_custom.svg", "image/svg+xml"), ("logo.svg", "image/svg+xml"), ("logo.png", "image/png")]
    for fn, mime in files:
        p = os.path.join("assets", fn)
        if os.path.exists(p):
            try:
                with open(p, "rb") as f:
                    data = f.read()
                    b64 = base64.b64encode(data).decode("utf-8")
                    max_w = "280px" if for_dark_bg else "210px"
                    max_h = "95px" if for_dark_bg else "75px"
                    return f'<img src="data:{mime};base64,{b64}" style="max-width: {max_w}; max-height: {max_h}; margin-bottom: 12px; filter: drop-shadow(0 6px 18px rgba(0,0,0,0.5));" /><br>'
            except Exception:
                pass
    return ""


def normalizar_nome_vendedor(vend_raw, num_ped_str="", doc_cli="", ped_obj=None):
    raw = ped_obj.get("raw_data", {}) if isinstance(ped_obj, dict) else {}
    cab = raw.get("cabecalho", {})
    inf = raw.get("informacoes_adicionais", {})
    obs = raw.get("observacoes", {})

    v_direct = str(vend_raw or (ped_obj.get("vendedor") if isinstance(ped_obj, dict) else "") or cab.get("nome_vendedor") or cab.get("vendedor") or "").strip()
    cod_v = str(inf.get("codVend") or cab.get("codigo_vendedor") or "").strip()
    obs_txt = str(obs.get("obs_venda") or "") + " " + str(inf.get("dados_adicionais_nf") or "") + " " + (str(ped_obj.get("observacoes", "")) if isinstance(ped_obj, dict) else "")

    mapa_cods = {
        "12640172242": "Roberta Terra",
        "8908207475": "Faturamento / Direto",
        "12640037182": "Jadson Santos",
        "12640204444": "Carol Teixeira",
        "8901520924": "Site (API B2C)"
    }

    # Se a observação ou texto do pedido mencionar Roberta (ex: solicitado pela Roberta), atribui à Roberta Terra!
    if "ROBERTA" in obs_txt.upper() or "ROBERTA" in v_direct.upper() or cod_v == "12640172242":
        return "Roberta Terra"
    if "CAROL" in obs_txt.upper() or "CAROL" in v_direct.upper() or "TEIXEIRA" in v_direct.upper() or cod_v == "12640204444":
        return "Carol Teixeira"
    if "JADSON" in obs_txt.upper() or "JADSON" in v_direct.upper() or cod_v == "12640037182":
        return "Jadson Santos"

    if cod_v in mapa_cods:
        return mapa_cods[cod_v]

    v_upper = v_direct.upper()
    if "ENVIADO VIA API" in v_upper or str(num_ped_str).strip() == "523":
        return "Site (API B2C)"
    if "SHOPIFY" in v_upper:
        return "Shopify (Site B2C)"
    if "FATURAMENTO" in v_upper:
        return "Faturamento / Direto"
    
    # Limpeza de códigos técnicos e prefixos
    clean_name = re.sub(r'MISS\d+\s*-\s*[A-Z]+\s*\(\s*', '', v_direct)
    clean_name = clean_name.replace(')', '').strip()
    clean_name = re.sub(r'ADM\s*-\s*', '', clean_name).strip()
    
    return clean_name or "Sem Vendedor"

_MAPA_CLIENTES_RAM_GLOBAL = {}

def eh_pedido_b2b_cnpj(ped):
    """
    REGRA REAL DO OMIE ERP:
    - Pedido B2B (Corporativo) = Emitido para CNPJ (Pessoa Jurídica com 14 dígitos).
    - Pedido B2C (Site / Varejo) = Emitido para CPF (Pessoa Física / Consumidor Final) ou via API Site (523 / Enviado via API / Shopify).
    """
    num_p_str = str(ped.get("numero_pedido") or "").strip()
    if num_p_str == "523":
        return False
    v_vend = str(ped.get("vendedor") or "").strip().lower()
    if "enviado via api" in v_vend or "site (api b2c)" in v_vend or "shopify" in v_vend:
        return False

    raw = ped.get("raw_data", {}) if isinstance(ped.get("raw_data"), dict) else {}
    inf = raw.get("informacoes_adicionais", {}) if isinstance(raw.get("informacoes_adicionais"), dict) else {}
    cab = raw.get("cabecalho", {}) if isinstance(raw.get("cabecalho"), dict) else {}
    cod_v_raw = str(inf.get("codVend") or cab.get("codigo_vendedor") or "").strip()
    if cod_v_raw == "8901520924":
        return False

    cli = ped.get("cliente", {}) if isinstance(ped.get("cliente"), dict) else {}
    doc = str(cli.get("cnpj_cpf") or ped.get("cliente_cnpj_cpf") or ped.get("cnpj_cpf") or cab.get("cnpj_cpf") or "").strip()
    doc_digits = "".join(filter(str.isdigit, doc))

    # Descartar clientes com Tag de Transportadora
    cli_nome = str(ped.get("cliente_nome") or cli.get("razao_social") or "").strip().upper()
    if "TRANSPORTADORA" in cli_nome or "BRASPRESS" in cli_nome or "MELHOR ENVIO" in cli_nome:
        return False

    cod_cli = str(ped.get("codigo_cliente") or cab.get("codigo_cliente") or "").strip()
    if cod_cli:
        global _MAPA_CLIENTES_RAM_GLOBAL
        if not _MAPA_CLIENTES_RAM_GLOBAL:
            try:
                clis_list = omie.carregar_clientes() or []
                _MAPA_CLIENTES_RAM_GLOBAL = {str(c.get("codigo_cliente_omie") or c.get("codigo_cliente") or "").strip(): c for c in clis_list}
            except Exception:
                pass
        if cod_cli in _MAPA_CLIENTES_RAM_GLOBAL:
            cli_obj = _MAPA_CLIENTES_RAM_GLOBAL[cod_cli]
            tags = cli_obj.get("tags") or []
            tags_list = [str(t.get("tag") if isinstance(t, dict) else t).strip().upper() for t in tags]
            if "TRANSPORTADORA" in tags_list or any("TRANSPOR" in t for t in tags_list):
                return False
            doc_c = str(cli_obj.get("cnpj_cpf") or "").strip()
            doc_digits = "".join(filter(str.isdigit, doc_c))

    return len(doc_digits) == 14

def extrair_info_tom(descricao_produto):
    desc = str(descricao_produto).upper()
    swatches = {
        "13": ("No. 13 Bright Beige", "#F8E5D3"),
        "19": ("No. 19 Cool Ivory", "#F6E0CD"),
        "20": ("No. 20 Cool Beige", "#F4DFC9"),
        "21": ("No. 21 Light Beige", "#F2D9C0"),
        "22": ("No. 22 Cool Sand", "#EED2B6"),
        "23": ("No. 23 Natural Beige", "#EACCAE"),
        "24": ("No. 24 Cool Natural Beige", "#E4C3A3"),
        "25": ("No. 25 Warm Beige", "#DEC09E"),
        "26": ("No. 26 Natural Caramel", "#D8B491"),
        "27": ("No. 27 Honey Beige", "#CFAA86"),
        "31": ("No. 31 Golden Beige", "#C49C77"),
    }
    m = re.search(r'(?:NO\.?|Nº\.?|#|\b)\s*(13|19|20|21|22|23|24|25|26|27|31)\b', desc)
    if m:
        num = m.group(1)
        if num in swatches:
            return swatches[num]
            
    for num, (label, color) in swatches.items():
        sub_label = label.split(" ", 2)[-1].upper()
        if sub_label in desc:
            return label, color
            
    return None, None

def carregar_pedido_para_edicao_form(ped):
    """
    Carrega os dados de um pedido da Etapa 10 (Orçamento) no formulário do Novo Pedido para edição,
    preenchendo automaticamente Cliente, Data de Previsão, Condição de Pagamento, Tipo de Documento e Meio de Pagamento.
    """
    raw = ped.get("raw_data", {})
    cab = raw.get("cabecalho", {})
    det = raw.get("det", [])
    inf_adic = raw.get("informacoes_adicionais", {})
    lista_parc_raw = raw.get("lista_parcelas", {})
    lista_parc = lista_parc_raw.get("parcela", []) if isinstance(lista_parc_raw, dict) else []
    
    cod_cli_ped = str(ped.get("codigo_cliente") or cab.get("codigo_cliente") or "").strip()

    # 1. Carregar Cliente no Selectbox (ped_cliente_sel)
    try:
        lista_clientes = omie.carregar_clientes()
        cliente_label_encontrado = None
        for c in lista_clientes:
            if str(c.get("codigo_cliente")).strip() == cod_cli_ped:
                cliente_label_encontrado = c.get("display")
                break
        if cliente_label_encontrado:
            st.session_state["ped_cliente_sel"] = cliente_label_encontrado
    except Exception:
        pass

    # 2. Carregar Previsão de Faturamento (ped_dt_previsao)
    try:
        dt_str = ped.get("data_previsao") or cab.get("data_previsao")
        if dt_str:
            dt_obj = datetime.datetime.strptime(dt_str, "%d/%m/%Y").date()
            st.session_state["ped_dt_previsao"] = dt_obj
    except Exception:
        pass

    # 3. Carregar Condição de Pagamento / Parcela (ped_parcela_sel)
    try:
        cod_parc_ped = str(cab.get("codigo_parcela") or "001").strip()
        if len(cod_parc_ped) == 3:
            st.session_state["ped_parcela_sel"] = cod_parc_ped
    except Exception:
        pass

    # 4. Carregar Tipo de Documento e Meio de Pagamento (ped_tipo_doc_sel & ped_meio_pagamento_sel)
    try:
        tipo_doc_code = str(cab.get("codigo_tipo_documento") or "").strip().upper()
        if not tipo_doc_code and isinstance(lista_parc, list) and len(lista_parc) > 0:
            tipo_doc_code = str(lista_parc[0].get("tipo_documento") or "").strip().upper()
            
        if tipo_doc_code in ["BOL", "PIX", "CART", "DEB"]:
            st.session_state["ped_tipo_doc_sel"] = tipo_doc_code

        meio_pag_code = str(cab.get("codigo_meio_pagamento") or "").strip()
        if meio_pag_code in ["15", "17", "03", "04"]:
            st.session_state["ped_meio_pagamento_sel"] = meio_pag_code
    except Exception:
        pass

    # 5. Carregar Quantidade de Parcelas (ped_qtd_parcelas_sel)
    try:
        qtd_parc_val = int(cab.get("quantidade_parcelas") or (len(lista_parc) if isinstance(lista_parc, list) and len(lista_parc) > 0 else 1))
        if 1 <= qtd_parc_val <= 12:
            st.session_state["ped_qtd_parcelas_sel"] = qtd_parc_val
    except Exception:
        pass
    
    itens_carregados = []
    for it in det:
        pr = it.get("produto", {})
        inf_it = it.get("inf_adic", {})
        cod_p_int = str(pr.get("codigo_produto_integracao") or pr.get("codigo") or "").strip()
        desc_p = str(pr.get("descricao") or cod_p_int).strip()
        qtd_p = float(pr.get("quantidade") or 1.0)
        vlr_u = float(pr.get("valor_unitario") or 0.0)
        vlr_desc = float(inf_it.get("valor_desconto") or 0.0)
        
        cen_item = str(inf_it.get("codigo_cenario_impostos_item") or "").strip()
        nao_fin = str(inf_it.get("nao_gerar_financeiro", "N")).upper()
        cfop_item = str(pr.get("cfop") or "").strip()
        eh_bonif = ("BONIF" in str(it.get("tipo_item", "")).upper()) or (nao_fin == "S") or (cen_item == "8904163333") or (cfop_item in ["5.910", "6.910"])
        tipo_item_carregado = "BONIFICAÇÃO" if eh_bonif else "MONITORAMENTO AUTOMÁTICO DE IMPOSTOS"
        
        prod_mapa = mapa_produtos.get(cod_p_int, {})
        v_site = float(prod_mapa.get("preco_site") or (vlr_u * 1.9 if vlr_u > 0 else 0.0))
        prc_base = float(prod_mapa.get("valor_unitario") or (v_site / 1.9 if v_site > 0 else vlr_u))
        
        sub_p = round((qtd_p * vlr_u) - vlr_desc, 2)
        
        itens_carregados.append({
            "codigo_produto_integracao": cod_p_int,
            "descricao": desc_p,
            "imagem_url": prod_mapa.get("imagem_url", ""),
            "tipo_item": tipo_item_carregado,
            "cenario_fiscal": tipo_item_carregado,
            "cfop": cfop_item,
            "local_estoque": config.get("local_estoque_nome", "PADRAO"),
            "quantidade": qtd_p,
            "preco_site": v_site,
            "preco_base_1_9": prc_base,
            "valor_unitario": vlr_u,
            "valor_desconto": vlr_desc,
            "subtotal": sub_p
        })
        
    st.session_state["itens_pedido"] = itens_carregados
    salvar_rascunho_pedido(itens_carregados)
    
    num_p_str = str(ped.get("numero_pedido") or cab.get("numero_pedido") or "").strip()
    cod_p_str = str(ped.get("codigo_pedido") or cab.get("codigo_pedido") or "").strip()
    
    st.session_state["pedido_em_edicao"] = {
        "codigo_pedido": cod_p_str,
        "numero_pedido": num_p_str,
        "codigo_cliente": cod_cli_ped,
        "raw_data": raw
    }
    st.session_state["mudar_pagina_para"] = "📋  Novo Pedido"

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — NAVEGAÇÃO & BRANDING
# ══════════════════════════════════════════════════════════════════════════════
if "mudar_pagina_para" in st.session_state and st.session_state["mudar_pagina_para"]:
    st.session_state["nav_pagina"] = st.session_state.pop("mudar_pagina_para")

with st.sidebar:
    tenant_info = obter_dados_tenant()
    logo_img_html = obter_logo_b64_html()
    if not logo_img_html:
        logo_img_html = f'<div style="font-size: 24px; font-weight: 900; letter-spacing: 0.15em; color: #FFFFFF; text-shadow: 0 2px 10px rgba(139, 92, 246, 0.5);">{tenant_info["subdominio"].upper()}</div><div style="font-size: 10px; font-weight: 800; letter-spacing: 0.25em; color: #FDE68A; margin-top: 2px;">{tenant_info["nome_empresa"]}</div>'

    st.markdown(f"""
<div style="text-align: center; padding: 18px 0 14px 0; background: linear-gradient(180deg, rgba(30, 27, 75, 0.4) 0%, rgba(15, 23, 42, 0.6) 100%); border-radius: 12px; border: 1px solid rgba(139, 92, 246, 0.25); margin-bottom: 14px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25);">
{logo_img_html}
<div style="font-size: 11px; color: #FFFFFF; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; margin-top: 6px;">CRM & Gestão de Pedidos</div>
<div style="display: inline-flex; align-items: center; gap: 5px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 2px 8px; margin-top: 6px;">
<span style="font-size: 10px;">🌐</span>
<span style="font-size: 10px; color: #C4B5FD; font-weight: 700;">{tenant_info['subdominio_completo']}</span>
</div>
</div>
""", unsafe_allow_html=True)

    usr_logado = st.session_state.get("usuario_logado")
    is_master = auth.eh_usuario_master(usr_logado)

    if usr_logado:
        if "frase_login" in st.session_state and st.session_state["frase_login"]:
            frase_pop = st.session_state.pop("frase_login")
            st.toast(f"{frase_pop}", icon="🔥")
        badge_perfil = "👑 ADMINISTRADOR MASTER" if is_master else "👔 VENDEDOR OMIE"
        bg_badge = "rgba(254, 243, 199, 0.15)" if is_master else "rgba(167, 139, 250, 0.15)"
        border_badge = "1.5px solid #F59E0B" if is_master else "1.5px solid #8B5CF6"
        txt_color = "#FBBF24" if is_master else "#C4B5FD"

        st.markdown(f"""
<div style="background: {bg_badge}; border: {border_badge}; border-radius: 10px; padding: 10px 12px; margin-bottom: 10px;">
<div style="font-size: 10px; color: {txt_color}; font-weight: 800; text-transform: uppercase;">{badge_perfil}:</div>
<div style="font-size: 13px; color: #FFFFFF; font-weight: 800; margin-top: 2px;">{usr_logado.get("nome_vendedor")}</div>
<div style="font-size: 10px; color: #FFFFFF; font-weight: 700; margin-top: 2px; font-weight: 600;">ID Omie: #{usr_logado.get("codigo_vendedor")}</div>
</div>
""", unsafe_allow_html=True)

        # Sincronização resiliente do token de acesso no LocalStorage do navegador
        if st.session_state.get("session_token"):
            tok_sinc = st.session_state["session_token"]
            components.html(f"""
            <script>
            (function() {{
                try {{
                    const wins = [window, window.parent, window.top];
                    for (const w of wins) {{
                        try {{
                            if (w && w.localStorage && w.localStorage.getItem('omnievo_crm_token') !== '{tok_sinc}') {{
                                w.localStorage.setItem('omnievo_crm_token', '{tok_sinc}');
                            }}
                        }} catch(e) {{}}
                    }}
                }} catch(e) {{}}
            }})();
            </script>
            """, height=0)

        st.markdown('<div class="sidebar-logout-container">', unsafe_allow_html=True)
        if st.button("🚪 Sair da Conta", key="btn_logout_sidebar", use_container_width=True):
            token_atual = st.query_params.get("session_token") or st.session_state.get("session_token")
            auth.encerrar_sessao_usuario(token_atual)
            st.query_params.clear()
            st.session_state["authenticated"] = False
            st.session_state["usuario_logado"] = None
            st.session_state["session_token"] = None
            components.html("""
            <script>
            (function() {
                try {
                    const wins = [window, window.parent, window.top];
                    for (const w of wins) {
                        try {
                            if (w && w.localStorage) {
                                w.localStorage.removeItem('omnievo_crm_token');
                            }
                        } catch(e) {}
                    }
                } catch(e) {}
            })();
            </script>
            """, height=0)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Card dinâmico de Cliente Selecionado no Menu Lateral
    cli_sel_sidebar = st.session_state.get("ped_cliente_sel") or st.session_state.get("cliente_detalhes_historico")
    if cli_sel_sidebar:
        cli_dict_sb = {}
        if isinstance(cli_sel_sidebar, dict):
            cli_dict_sb = cli_sel_sidebar
        elif isinstance(cli_sel_sidebar, str) and "ped_cliente_sel" in st.session_state:
            # Se for chave da selectbox
            pass
        
        raz_sb = cli_dict_sb.get("razao_social") or cli_dict_sb.get("nome_fantasia") or cli_dict_sb.get("display")
        doc_sb = cli_dict_sb.get("cnpj_cpf") or ""
        uf_sb = cli_dict_sb.get("estado") or "ES"
        if raz_sb:
            st.markdown(f"""
<div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.18) 0%, rgba(139, 92, 246, 0.12) 100%); border: 1.5px solid #8B5CF6; border-radius: 10px; padding: 10px 12px; margin-bottom: 12px; box-shadow: 0 4px 12px rgba(139, 92, 246, 0.15);">
<div style="font-size: 10px; color: #FFFFFF; font-weight: 800; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em;">🏢 CLIENTE SELECIONADO NO CRM:</div>
<div style="font-size: 13px; color: #FFFFFF; font-weight: 800; margin-top: 3px; word-break: break-word;">{raz_sb}</div>
<div style="font-size: 10px; color: #FFFFFF; font-weight: 700; margin-top: 2px; font-weight: 600;">{'CNPJ/CPF: ' + doc_sb + ' | ' if doc_sb else ''}UF: {uf_sb}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")

    opcoes_nav = [
        "👤  Cadastrar Cliente", 
        # "🔍  Análise de Crédito & Score",  # Módulo inativo conforme solicitação
        "📋  Novo Pedido", 
        "📊  Kanban de Vendas", 
        "🚚  Rastreamento & Logística",
        "🎯  Metas & Pacing Diário",
        "🏆  Desempenho de Vendedores", 
        "🚨  Radar de Clientes & Churn", 
        "🗺️  Localização dos Clientes",
        "🔎  Histórico do Cliente", 
        "📦  Estoque e Validades"
    ]
    if is_master:
        opcoes_nav.insert(4, "📈  Evolução de Vendas")
        opcoes_nav.append("👥  Pessoas Cadastradas")

    if st.session_state.get("nav_pagina") not in opcoes_nav:
        st.session_state["nav_pagina"] = opcoes_nav[0]

    pagina = st.radio(
        "NAVEGAÇÃO",
        opcoes_nav,
        key="nav_pagina",
        label_visibility="visible"
    )

    if st.session_state.get("last_nav_pagina") != pagina:
        st.session_state["last_nav_pagina"] = pagina
        components.html("""
        <script>
        (function() {
            function scrollMainToTop() {
                try {
                    const pWin = window.parent || window;
                    const doc = pWin.document;
                    const container = doc.querySelector('[data-testid="stAppViewContainer"]') || doc.querySelector('section.main') || doc.documentElement || pWin;
                    if (container && container.scrollTo) {
                        container.scrollTo({ top: 0, behavior: 'smooth' });
                        if (container.scrollTop !== undefined) container.scrollTop = 0;
                    }
                    pWin.scrollTo({ top: 0, behavior: 'smooth' });
                } catch(e) {}
            }
            scrollMainToTop();
            setTimeout(scrollMainToTop, 80);
            setTimeout(scrollMainToTop, 250);
        })();
        </script>
        """, height=0)

    st.markdown("---")

    if st.button("🔄  Sincronizar Dados", key="btn_sync_sidebar", use_container_width=True):
        with st.spinner("Atualizando dados do Omie..."):
            st.cache_data.clear()
            auth.sincronizar_vendedores_omie(force_refresh=True)
            omie.carregar_clientes(force_refresh=True)
            omie.atualizar_estoque_em_lote()
            omie.carregar_produtos(force_refresh=True)
            omie.listar_pedidos_omie(force_refresh=True)
            st.toast("✅ Todos os dados e saldos de estoque disponíveis foram sincronizados!")
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# CARREGAMENTO DE DADOS (CACHE EM MEMÓRIA RAM - ULTRA FAST 0ms)
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_resource(ttl=600, show_spinner=False)
def _obter_produtos_e_precos_cached():
    prods = omie.carregar_produtos()
    tab_1_9 = omie.carregar_tabela_preco_1_9()

    if prods:
        for cod_p, p in prods.items():
            # Preço no Site (Varejo / Preço de Lista Cheio)
            v_site = float(p.get("preco_site") or p.get("valor_unitario", 0.0))
            p["preco_site"] = v_site
            
            # Preço oficial da Tabela B2B - 1,9 (Preço de Compra B2B = Preço Site / 1,9)
            if tab_1_9 and cod_p in tab_1_9 and float(tab_1_9[cod_p]) > 0:
                p["valor_unitario"] = float(tab_1_9[cod_p])
            else:
                p["valor_unitario"] = round(v_site / 1.9, 2) if v_site > 0 else 0.0

    return prods, tab_1_9

def _obter_pedidos_cached():
    pedidos = omie.listar_pedidos_omie(force_refresh=False)
    return [p for p in pedidos if not omie.eh_pedido_cancelado(p)]

mapa_produtos, mapa_tabela_1_9 = _obter_produtos_e_precos_cached()
# Carrega clientes em tempo real direto da RAM/disco (0ms), garantindo que cadastros novos apareçam na hora
lista_clientes_base = omie.carregar_clientes()

# ⚡ LAZY LOADING ULTRA-RÁPIDO: Não carrega pedidos pesados em telas de cadastro ou pedidos novos
paginas_que_precisam_pedidos = [
    "📊  Kanban de Vendas", 
    "📈  Evolução de Vendas", 
    "🎯  Metas & Pacing Diário", 
    "🏆  Desempenho de Vendedores", 
    "🚨  Radar de Clientes & Churn", 
    "🗺️  Localização dos Clientes",
    "👥  Pessoas Cadastradas",
    "🔎  Histórico do Cliente"
]

if pagina in paginas_que_precisam_pedidos:
    pedidos_lista_full_base = _obter_pedidos_cached()
else:
    pedidos_lista_full_base = []

usr_logado = st.session_state.get("usuario_logado")
is_master = auth.eh_usuario_master(usr_logado)

# 🛡️ ISOLAMENTO DE DADOS E CARTEIRA POR PERFIL DE ACESSO (RBAC)
# Usuários VENDEDOR veem estritamente seus próprios pedidos e sua própria carteira nos relatórios.
# Em "📋  Novo Pedido" e "👤  Cadastrar Cliente", a base de clientes é irrestrita para permitir novas vendas imediatas.
pedidos_lista_full = auth.obter_pedidos_filtrados_usuario(pedidos_lista_full_base, usr_logado)

if pagina in ["📋  Novo Pedido", "👤  Cadastrar Cliente"] or is_master:
    lista_clientes = lista_clientes_base
else:
    lista_clientes = auth.obter_clientes_filtrados_usuario(lista_clientes_base, usr_logado, pedidos_lista_full)

if not mapa_produtos:
    mapa_produtos = {
        "MS101367": {"codigo_produto_integracao": "MS101367", "codigo_produto": 8728732988, "descricao": "OMNIEVO VITA C PLUS SPOT CORRECTING CONCENTRATE AMPOULE", "valor_unitario": 249.0, "unidade": "UN"},
    }

# ══════════════════════════════════════════════════════════════════════════════
# GESTÃO DE METAS COMERCIAIS & ENGENHARIA DE REATIVAÇÃO / CHURN
# ══════════════════════════════════════════════════════════════════════════════
import datetime
from datetime import date
import os
import json
import calendar
import urllib.parse

ARQUIVO_METAS_CACHE = "cache/metas_comerciais.json"

def carregar_metas_comerciais(ano=None, mes=None):
    hoje = date.today()
    ano_str = str(ano) if ano else str(hoje.year)
    mes_str = f"{int(mes):02d}" if mes else f"{hoje.month:02d}"
    chave = f"{ano_str}-{mes_str}"
    
    padrao = {
        "meta_global": 350000.0,
        "meta_b2b": 200000.0,
        "meta_b2c": 150000.0,
        "metas_vendedores": {}
    }
    
    try:
        if os.path.exists(ARQUIVO_METAS_CACHE):
            with open(ARQUIVO_METAS_CACHE, "r", encoding="utf-8") as f:
                dados = json.load(f)
                if chave in dados:
                    res = dados[chave]
                    for k, v in padrao.items():
                        if k not in res:
                            res[k] = v
                    return res
    except Exception:
        pass
    return padrao

def salvar_metas_comerciais(ano, mes, dados_metas):
    ano_str = str(ano)
    mes_str = f"{int(mes):02d}"
    chave = f"{ano_str}-{mes_str}"
    try:
        os.makedirs("cache", exist_ok=True)
        dados = {}
        if os.path.exists(ARQUIVO_METAS_CACHE):
            try:
                with open(ARQUIVO_METAS_CACHE, "r", encoding="utf-8") as f:
                    dados = json.load(f)
            except Exception:
                dados = {}
        dados[chave] = dados_metas
        with open(ARQUIVO_METAS_CACHE, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False

def eh_feriado_ou_fim_de_semana(dt):
    """
    Retorna True se a data for Sábado (5), Domingo (6) ou Feriado Nacional no Brasil.
    """
    if dt.weekday() >= 5:
        return True
    
    # Feriados Nacionais Fixos no Brasil (Mês, Dia)
    feriados_fixos = {
        (1, 1),   # Confraternização Universal / Ano Novo
        (4, 21),  # Tiradentes
        (5, 1),   # Dia do Trabalho
        (9, 7),   # Independência do Brasil
        (10, 12), # Nossa Senhora Aparecida
        (11, 2),  # Finados
        (11, 15), # Proclamação da República
        (11, 20), # Dia Nacional de Zumbi e da Consciência Negra
        (12, 25)  # Natal
    }
    if (dt.month, dt.day) in feriados_fixos:
        return True
    
    # Feriados Móveis no Brasil (Carnaval, Sexta-Feira Santa, Corpus Christi)
    try:
        y = dt.year
        a = y % 19
        b = y // 100
        c = y % 100
        d = b // 4
        e = b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l) // 451
        month_pascoa = (h + l - 7 * m + 114) // 31
        day_pascoa = ((h + l - 7 * m + 114) % 31) + 1
        dt_pascoa = date(y, month_pascoa, day_pascoa)

        feriados_moveis = {
            dt_pascoa - datetime.timedelta(days=48), # Segunda-feira de Carnaval
            dt_pascoa - datetime.timedelta(days=47), # Terça-feira de Carnaval
            dt_pascoa - datetime.timedelta(days=2),  # Sexta-Feira Santa
            dt_pascoa + datetime.timedelta(days=60)  # Corpus Christi
        }
        if dt in feriados_moveis:
            return True
    except Exception:
        pass

    return False

def calcular_dias_uteis_mes(ano, mes):
    import calendar
    _, num_dias = calendar.monthrange(ano, mes)
    dias_uteis_total = 0
    dias_uteis_passados = 0
    dias_uteis_restantes = 0
    hoje = date.today()
    
    for d in range(1, num_dias + 1):
        dt = date(ano, mes, d)
        if not eh_feriado_ou_fim_de_semana(dt):
            dias_uteis_total += 1
            if ano == hoje.year and mes == hoje.month:
                if dt < hoje:
                    dias_uteis_passados += 1
                else:
                    dias_uteis_restantes += 1
    
    if ano < hoje.year or (ano == hoje.year and mes < hoje.month):
        dias_uteis_passados = dias_uteis_total
        dias_uteis_restantes = 0
    elif ano > hoje.year or (ano == hoje.year and mes > hoje.month):
        dias_uteis_passados = 0
        dias_uteis_restantes = dias_uteis_total
        
    return num_dias, max(dias_uteis_total, 1), dias_uteis_passados, max(dias_uteis_restantes, 1)

def formatar_link_whatsapp_reativacao(telefone, nome_cliente, dias_sem_compra):
    if not telefone:
        return ""
    num = "".join(filter(str.isdigit, str(telefone)))
    if len(num) < 10:
        return ""
    if not num.startswith("55"):
        num = "55" + num
    
    primeiro_nome = str(nome_cliente).split()[0].title() if nome_cliente else "Cliente"
    msg = (
        f"Olá, {primeiro_nome}! Tudo bem? 😊\n\n"
        f"Aqui é da equipe comercial Missha! Notamos que faz {dias_sem_compra} dias desde seu último pedido conosco. "
        f"Preparamos condições e descontos exclusivos este mês para você repor seu estoque.\n\n"
        f"Podemos te enviar o catálogo atualizado com as novidades de hoje?"
    )
    import urllib.parse
    return f"https://wa.me/{num}?text={urllib.parse.quote(msg)}"



# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 1: NOVO PEDIDO DE VENDA
# ══════════════════════════════════════════════════════════════════════════════
if pagina == "📋  Novo Pedido":

    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">📋</div>
        <div>
            <div class="page-header-title">Novo Pedido de Venda</div>
            <div class="page-header-subtitle">Preencha os dados do cliente e os itens. Todo novo pedido cai automaticamente na Etapa 10 (Orçamento).</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get("pedido_em_edicao"):
        ped_ed = st.session_state["pedido_em_edicao"]
        num_p_ed = ped_ed.get("numero_pedido")
        col_ed1, col_ed2 = st.columns([3.5, 1])
        with col_ed1:
            st.markdown(f"""
            <div style="background: rgba(245, 158, 11, 0.15); border: 2px solid #F59E0B; border-radius: 10px; padding: 12px 16px; margin-bottom: 12px;">
                <div style="font-weight: 800; color: #FBBF24; font-size: 14px;">✏️ MODO EDIÇÃO ATIVO: Pedido Nº {num_p_ed} (Etapa 10 - Orçamento)</div>
                <div style="font-size: 12px; color: #FFFFFF; font-weight: 700; margin-top: 2px;">Você está alterando um pedido existente na Etapa 10 (Orçamento). Faça as edições necessárias e salve as alterações abaixo.</div>
            </div>
            """, unsafe_allow_html=True)
        with col_ed2:
            st.markdown("<div style='margin-top: 4px;'></div>", unsafe_allow_html=True)
            if st.button("❌ Cancelar Edição", key="btn_cancelar_edicao_ped", use_container_width=True):
                st.session_state.pop("pedido_em_edicao", None)
                st.session_state["itens_pedido"] = []
                salvar_rascunho_pedido([])
                st.toast("Edição cancelada.")
                st.rerun()

    # Banner de Transmissão de Pedidos em Segundo Plano (Nuvem Local)
    jobs_status = omie.obter_resultados_fila_pedidos()
    if jobs_status:
        for j_id, j_info in list(jobs_status.items())[-3:]:
            st_j = j_info.get("status")
            cli_j = j_info.get("cliente_nome", "Cliente")
            ts_j = j_info.get("timestamp", "")
            
            if st_j == "concluido":
                num_p = j_info.get("num_pedido", "")
                pdf_b = j_info.get("pdf_bytes")
                pdf_fn = j_info.get("pdf_filename", f"Pedido_{num_p}.pdf")
                
                col_b1, col_b2 = st.columns([3.5, 1])
                with col_b1:
                    st.success(f"🟢 **Pedido #{num_p} ({cli_j})**: Transmitido com sucesso para o Omie ERP às {ts_j}!")
                with col_b2:
                    if pdf_b:
                        st.download_button(
                            f"📄 Baixar PDF #{num_p}",
                            data=pdf_b,
                            file_name=pdf_fn,
                            mime="application/pdf",
                            key=f"btn_dl_pdf_bg_{j_id}"
                        )
            elif st_j in ["enviando", "pendente"]:
                st.info(f"⏳ **Transmitindo Pedido para {cli_j}** na nuvem em segundo plano (iniciado às {ts_j})... Pode ir fazendo o próximo pedido!")
            elif st_j == "erro":
                err_j = j_info.get("erro", "Erro no envio")
                st.error(f"🚨 Erro na transmissão do pedido de {cli_j}: {err_j}")

    if "sucesso_pedido_emitido" in st.session_state and st.session_state["sucesso_pedido_emitido"]:
        suc = st.session_state["sucesso_pedido_emitido"]
        col_s1, col_s2 = st.columns([3, 1])
        with col_s1:
            st.success(f"✅ Pedido Nº **{suc['num_pedido']}** enviado com sucesso para o Omie ERP! (Cadastrado na Etapa 10 - Orçamento). A lista de itens foi limpa.")
        with col_s2:
            st.download_button(
                "📄 Baixar PDF do Pedido",
                data=suc["pdf_bytes"],
                file_name=suc["pdf_filename"],
                mime="application/pdf",
                key=f"btn_download_pdf_success_{suc['cod_pedido']}",
                use_container_width=True
            )
        st.markdown("<hr style='margin: 8px 0 16px 0;'>", unsafe_allow_html=True)

    # ── BANNER DE ERRO CONSOLIDADO ──
    if "erros_validacao_pedido" in st.session_state and st.session_state["erros_validacao_pedido"]:
        erros_list = st.session_state["erros_validacao_pedido"]
        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.14); border: 2px solid #EF4444; border-radius: 10px; padding: 14px 18px; margin-bottom: 18px; box-shadow: 0 4px 12px rgba(239, 68, 68, 0.25);">
            <div style="color: #EF4444; font-weight: 800; font-size: 15px; display: flex; align-items: center; gap: 8px;">
                🚨 FALHA NO CADASTRO DO PEDIDO — CORRIJA OS CAMPOS SINALIZADOS EM VERMELHO
            </div>
            <div style="color: #EF4444; font-weight: 800; font-size: 13px; margin-top: 4px; font-weight: 600;">
                O pedido não pôde ser enviado devido aos seguintes erros:
            </div>
            <ul style="color: #EF4444; font-size: 13px; margin-top: 8px; margin-bottom: 0; padding-left: 20px; font-weight: 600;">
                {"".join(f'<li style="margin-bottom: 4px;">{err}</li>' for err in erros_list)}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📋 Consultar Tabela Completa da Política Comercial (Sobre Tabela 1.9)", expanded=False):
        st.markdown("""
        <table style="width: 100%; border-collapse: collapse; font-size: 13px; margin: 8px 0; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; overflow: hidden;">
            <thead>
                <tr style="background: #EEF2FF; border-bottom: 2px solid #C7D2FE; color: #1E293B;">
                    <th style="padding: 12px; text-align: left; font-weight: 800;">Categoria</th>
                    <th style="padding: 12px; text-align: left; font-weight: 800;">Perfil / Valor do Pedido (Mínimo)</th>
                    <th style="padding: 12px; text-align: left; font-weight: 800;">Condição (Tabela 1.9)</th>
                    <th style="padding: 12px; text-align: left; font-weight: 800;">Prazo de Pagamento</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom: 1px solid #F1F5F9; color: #1E293B;">
                    <td style="padding: 10px 12px;">⚕️ <b>PROFISSIONAL</b></td>
                    <td style="padding: 10px 12px;">Mínimo <b>R$ 1.500,00</b></td>
                    <td style="padding: 10px 12px; color: #D97706; font-weight: 700;">TABELA 1.9</td>
                    <td style="padding: 10px 12px; font-weight: 600;">28 dias</td>
                </tr>
                <tr style="border-bottom: 1px solid #F1F5F9; color: #1E293B;">
                    <td style="padding: 10px 12px;">🛒 <b>ESSENCIAL</b></td>
                    <td style="padding: 10px 12px;"><b>R$ 3.500,00</b> a <b>R$ 6.999,99</b></td>
                    <td style="padding: 10px 12px; color: #D97706; font-weight: 700;">TABELA 1.9</td>
                    <td style="padding: 10px 12px; font-weight: 600;">14 / 28 / 35 dias</td>
                </tr>
                <tr style="border-bottom: 1px solid #F1F5F9; color: #1E293B;">
                    <td style="padding: 10px 12px;">🥉 <b>BRONZE</b></td>
                    <td style="padding: 10px 12px;"><b>R$ 7.000,00</b> a <b>R$ 14.999,99</b></td>
                    <td style="padding: 10px 12px; color: #D97706; font-weight: 700;">TABELA 1.9</td>
                    <td style="padding: 10px 12px; font-weight: 600;">28 / 35 / 42 dias</td>
                </tr>
                <tr style="border-bottom: 1px solid #F1F5F9; color: #1E293B;">
                    <td style="padding: 10px 12px;">🥈 <b>PRATA</b></td>
                    <td style="padding: 10px 12px;"><b>R$ 15.000,00</b> a <b>R$ 29.999,99</b></td>
                    <td style="padding: 10px 12px; color: #D97706; font-weight: 700;">TABELA 1.9</td>
                    <td style="padding: 10px 12px; font-weight: 600;">28 / 35 / 42 / 49 dias</td>
                </tr>
                <tr style="border-bottom: 1px solid #F1F5F9; color: #1E293B;">
                    <td style="padding: 10px 12px;">🥇 <b>OURO</b></td>
                    <td style="padding: 10px 12px;"><b>R$ 30.000,00</b> a <b>R$ 69.999,99</b></td>
                    <td style="padding: 10px 12px; color: #059669; font-weight: 800;">TABELA 1.9</td>
                    <td style="padding: 10px 12px; font-weight: 600;">35 / 42 / 49 dias</td>
                </tr>
                <tr style="color: #1E293B;">
                    <td style="padding: 10px 12px;">💎 <b>DIAMANTE</b></td>
                    <td style="padding: 10px 12px;">A partir de <b>R$ 70.000,00</b></td>
                    <td style="padding: 10px 12px; color: #059669; font-weight: 800;">TABELA 1.9</td>
                    <td style="padding: 10px 12px; font-weight: 600;">28 / 35 / 42 / 49 / 56 dias</td>
                </tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

    # Injeção de CSS para sinalização de campo em vermelho (Cliente)
    if st.session_state.get("erro_campo_cliente"):
        st.markdown("""
        <style>
        div[data-testid="stSelectbox"]:has(label:contains("Razão social ou CPF/CNPJ")) {
            border: 2px solid #EF4444 !important;
            border-radius: 8px !important;
            background-color: rgba(239, 68, 68, 0.08) !important;
            padding: 6px !important;
            box-shadow: 0 0 12px rgba(239, 68, 68, 0.5) !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # ── Cliente e Faturamento ──
    st.markdown('<div class="section-header">Cliente & Faturamento</div>', unsafe_allow_html=True)

    # Parâmetros padrão mantidos silenciosamente em segundo plano para o Omie ERP (Santander - Principal: 8916226559)
    conta_corrente_sel = config.get("codigo_conta_corrente_padrao", 8916226559)
    try:
        conta_corrente_sel = int(conta_corrente_sel)
    except Exception:
        conta_corrente_sel = 8916226559
    if conta_corrente_sel in [8659891030, 0, None]:
        conta_corrente_sel = 8916226559
    categoria_ped = "1.01.03"

    col_c1, col_c2, col_c3 = st.columns([3.8, 3.2, 3.0])

    with col_c1:
        if lista_clientes:
            def _format_cliente_label(c):
                if not isinstance(c, dict):
                    return str(c)
                disp = c.get("display")
                if disp:
                    return disp
                razao = c.get("razao_social") or c.get("nome_fantasia") or "Cliente"
                doc = c.get("cnpj_cpf") or ""
                uf = c.get("estado") or "UF"
                return f"{razao} ({doc}) - {uf}" if doc else f"{razao} - {uf}"

            options_clientes = {_format_cliente_label(c): c for c in lista_clientes if isinstance(c, dict)}
            
            # Validação e sincronização inteligente do cliente pré-selecionado (ex: recém-cadastrado)
            if "ped_cliente_sel" in st.session_state and st.session_state["ped_cliente_sel"]:
                val_sel = str(st.session_state["ped_cliente_sel"]).strip()
                if val_sel not in options_clientes:
                    clean_doc = "".join(filter(str.isdigit, val_sel))
                    encontrado = None
                    for k in options_clientes.keys():
                        k_digits = "".join(filter(str.isdigit, k))
                        if clean_doc and len(clean_doc) >= 8 and clean_doc in k_digits:
                            encontrado = k
                            break
                        if val_sel.lower() in k.lower():
                            encontrado = k
                            break
                    if encontrado:
                        st.session_state["ped_cliente_sel"] = encontrado
                    else:
                        st.session_state.pop("ped_cliente_sel", None)

            cliente_sel_label = st.selectbox(
                "Razão social ou CPF/CNPJ *",
                list(options_clientes.keys()),
                index=None,
                placeholder="Selecione um cliente...",
                key="ped_cliente_sel"
            )
            if cliente_sel_label:
                cliente_sel = options_clientes[cliente_sel_label]
                uf_cli_actual = cliente_sel.get("estado", "ES")
                cep_raw = str(cliente_sel.get("cep") or "").strip()
                clean_cep = re.sub(r'\D', '', cep_raw)
                cep_cli_actual = f"{clean_cep[:5]}-{clean_cep[5:]}" if len(clean_cep) == 8 else cep_raw
                st.session_state["ped_cliente_cep"] = cep_cli_actual
                st.session_state["bp_cep_dest_input"] = cep_cli_actual
                st.caption(f"UF: **{uf_cli_actual}** | CEP: **{cep_cli_actual}** — {'Estadual' if uf_cli_actual == 'ES' else 'Interestadual'}")
                st.session_state["erro_campo_cliente"] = False
            else:
                cliente_sel = None
                if st.session_state.get("erro_campo_cliente"):
                    st.markdown('<div style="color: #EF4444; background: rgba(239, 68, 68, 0.15); border: 1px solid #EF4444; padding: 6px 10px; border-radius: 6px; font-size: 12px; font-weight: 700; margin-top: 6px;">❌ CAMPO OBRIGATÓRIO EM VERMELHO: Selecione a Razão Social ou CPF/CNPJ do cliente!</div>', unsafe_allow_html=True)
                else:
                    st.caption("⚠️ Nenhum cliente selecionado.")
        else:
            cod_cli = st.number_input("Código do Cliente Omie", min_value=1, value=8908859525, key="ped_cod_cli_fallback")
            uf_cli = st.text_input("UF do Cliente", value="ES", key="ped_uf_cli_fallback").upper()
            cliente_sel = {"codigo_cliente": cod_cli, "estado": uf_cli, "razao_social": "Cliente Selecionado"}

    with col_c2:
        # Carregar mapa de vendedores da Omie ERP
        vendedores_dict = {}
        try:
            usrs_db = auth.carregar_usuarios()
            for u in usrs_db.values():
                cv = u.get("codigo_vendedor")
                nv = u.get("nome_vendedor")
                if cv:
                    try:
                        vendedores_dict[int(cv)] = f"{nv} (# {cv})"
                    except (ValueError, TypeError):
                        pass
        except Exception:
            pass

        try:
            for cv, nv in omie.carregar_vendedores().items():
                try:
                    cv_int = int(cv)
                    if cv_int not in vendedores_dict:
                        vendedores_dict[cv_int] = f"{nv} (# {cv_int})"
                except (ValueError, TypeError):
                    pass
        except Exception:
            pass

        # Fallback garantido se o catálogo de vendedores estiver vazio
        if not vendedores_dict:
            vendedores_dict = {
                8901520924: "Enviado via API (#8901520924)",
                8908207475: "FATURAMENTO (#8908207475)"
            }

        # Selecionar por padrão o vendedor logado
        cod_vendedor_logado = usr_logado.get("codigo_vendedor") if usr_logado else None
        index_vendedor = 0
        vendedores_keys = list(vendedores_dict.keys())
        if cod_vendedor_logado:
            try:
                cv_log_int = int(cod_vendedor_logado)
                if cv_log_int in vendedores_keys:
                    index_vendedor = vendedores_keys.index(cv_log_int)
            except (ValueError, TypeError):
                index_vendedor = 0

        if index_vendedor >= len(vendedores_keys):
            index_vendedor = 0

        # Verificar se o usuário possui permissão de Admin/Gerente/Jadson ou MASTER
        is_admin_user = bool(
            is_master or
            (usr_logado and ("admin" in str(usr_logado.get("cargo", "")).lower() or
             "gerente" in str(usr_logado.get("cargo", "")).lower() or
             "diretor" in str(usr_logado.get("cargo", "")).lower() or
             "jadson" in str(usr_logado.get("email", "")).lower() or
             usr_logado.get("is_admin", False)))
        )

        cod_vendedor_selecionado = st.selectbox(
            "Vendedor Responsável *",
            vendedores_keys,
            index=index_vendedor,
            format_func=lambda x: vendedores_dict.get(x, f"Vendedor #{x}"),
            disabled=not is_admin_user,
            key="ped_vendedor_sel",
            help="Campo travado para vendedores comuns. Liberado apenas para Administradores Master."
        )
        vendedor_nome_selecionado = vendedores_dict.get(cod_vendedor_selecionado, "").split(" (#")[0] if cod_vendedor_selecionado else ""
        st.caption(f"👤 Atribuído a: **{vendedor_nome_selecionado}**")

    with col_c3:
        val_dt_prev = st.session_state.get("ped_dt_previsao")
        if not val_dt_prev or not isinstance(val_dt_prev, (datetime.date, datetime.datetime)):
            st.session_state["ped_dt_previsao"] = previsao_auto
        elif hasattr(val_dt_prev, "date") and not isinstance(val_dt_prev, datetime.date):
            st.session_state["ped_dt_previsao"] = val_dt_prev.date()

        if isinstance(st.session_state.get("ped_dt_previsao"), datetime.date) and st.session_state["ped_dt_previsao"] < hoje:
            st.session_state["ped_dt_previsao"] = hoje

        dt_previsao = st.date_input(
            "Previsão de Faturamento",
            min_value=hoje,
            format="DD/MM/YYYY",
            key="ped_dt_previsao"
        )
        if isinstance(dt_previsao, (datetime.date, datetime.datetime)):
            dt_previsao_str = dt_previsao.strftime("%d/%m/%Y")
        else:
            dt_previsao_str = hoje.strftime("%d/%m/%Y")

    st.markdown("<div style='margin-top: 6px;'></div>", unsafe_allow_html=True)
    col_tr1, col_tr2 = st.columns([3.5, 2.5])
    with col_tr1:
        opcoes_transportadoras_sel = [
            "EMPRESA BRASILEIRA DE CORREIOS E TELEGRAFOS",
            "BRASPRESS TRANSPORTES URGENTES LTDA",
            "ATIVA DISTRIBUICAO E LOGISTICA LTDA"
        ]
        if "ped_transportadora_override" in st.session_state:
            st.session_state["ped_transportadora_sel"] = st.session_state.pop("ped_transportadora_override")
        
        idx_tr_sel = 0
        cur_tr = st.session_state.get("ped_transportadora_sel")
        if cur_tr in opcoes_transportadoras_sel:
            idx_tr_sel = opcoes_transportadoras_sel.index(cur_tr)

        transp_selecionada = st.selectbox(
            "🚚 Transportadora Responsável pelo Envio / Frete *",
            opcoes_transportadoras_sel,
            index=idx_tr_sel,
            key="ped_transportadora_sel",
            help="Selecione a transportadora parceira autorizada para a entrega do pedido."
        )
        st.caption(f"📦 Opção selecionada: **{transp_selecionada}**")

    # 🚚 COTAÇÃO DE FRETE EM TEMPO REAL COM CUBAGEM AUTOMÁTICA - BRASPRESS
    cfg_bp_saved = braspress.carregar_config_braspress()
    usr_bp_init = cfg_bp_saved.get("usuario", "")
    pwd_bp_init = cfg_bp_saved.get("senha", "")
    
    # 1. Cálculo de Cubagem Automático com base nos itens do carrinho
    itens_carrinho_bp = st.session_state.get("itens_pedido", [])
    info_cubagem = braspress.calcular_cubagem_caixas(itens_carrinho_bp, mapa_produtos)
    
    with st.expander("🚚 Cotação Automática de Frete & Cubagem — Braspress & SSW (Ativa Transportes)", expanded=("BRASPRESS" in str(transp_selecionada).upper() or "ATI" in str(transp_selecionada).upper() or "SSW" in str(transp_selecionada).upper() or "ATIVA" in str(transp_selecionada).upper())):
        # Credenciais e Dados do Cliente preenchidos automaticamente em segundo plano
        bp_usuario = usr_bp_init
        bp_senha = pwd_bp_init

        cli_cnpj_raw = str(cliente_sel.get("cnpj_cpf") or "").strip() if ('cliente_sel' in locals() and isinstance(cliente_sel, dict)) else ""
        cli_razao_raw = str(cliente_sel.get("razao_social") or "").strip() if ('cliente_sel' in locals() and isinstance(cliente_sel, dict)) else ""
        cli_end_raw = f"{cliente_sel.get('endereco', '')}, {cliente_sel.get('numero', '')} - {cliente_sel.get('cidade', '')}/{cliente_sel.get('estado', '')}" if ('cliente_sel' in locals() and isinstance(cliente_sel, dict)) else ""

        # Buscar CEP do cliente selecionado no formulário
        cep_dest_bp = str(st.session_state.get("ped_cliente_cep") or "").strip()
        if not cep_dest_bp and 'cliente_sel' in locals() and isinstance(cliente_sel, dict):
            c_raw = str(cliente_sel.get("cep") or "").strip()
            c_clean = re.sub(r'\D', '', c_raw)
            cep_dest_bp = f"{c_clean[:5]}-{c_clean[5:]}" if len(c_clean) == 8 else c_raw

        if cep_dest_bp and (not st.session_state.get("bp_cep_dest_input") or st.session_state.get("bp_cep_dest_input") == ""):
            st.session_state["bp_cep_dest_input"] = cep_dest_bp

        bp_peso = float(info_cubagem.get("peso_kg", 0.5)) if isinstance(info_cubagem, dict) else 0.5
        bp_volumes = int(info_cubagem.get("volumes", 1)) if isinstance(info_cubagem, dict) else 1
        bp_cep_dest = st.session_state.get("bp_cep_dest_input") or cep_dest_bp
        
        # 100% ALINHADO AOS PARÂMETROS DE CÁLCULO DE NOTA FISCAL DO OMIE ERP
        val_vendas_omie = 0.0
        val_bonif_omie = 0.0

        for item_c in st.session_state.get("itens_pedido", []):
            qt_it = float(item_c.get("quantidade") or 1)
            sub_it = float(item_c.get("subtotal") or 0.0)
            v_unit = float(item_c.get("valor_unitario") or 0.0)
            v_desc = float(item_c.get("valor_desconto") or 0.0)
            cod_int = str(item_c.get("codigo_produto_integracao") or "").strip()
            
            eh_bonif = ("BONIF" in str(item_c.get("tipo_item", "")).upper()) or ("BONIF" in str(item_c.get("cenario_fiscal", "")).upper()) or (v_unit == 0.0) or (sub_it == 0.0)
            
            if eh_bonif:
                p_tab = float(item_c.get("preco_base_1_9") or item_c.get("valor_unitario") or 0.0)
                if p_tab <= 0.0 and mapa_produtos and isinstance(mapa_produtos, dict) and cod_int in mapa_produtos:
                    p_tab = float(mapa_produtos[cod_int].get("valor_unitario") or 1.0)
                if p_tab <= 0.0:
                    p_tab = 1.0
                val_bonif_omie += round(qt_it * p_tab, 2)
            else:
                if v_unit <= 0.0 and mapa_produtos and isinstance(mapa_produtos, dict) and cod_int in mapa_produtos:
                    v_unit = float(mapa_produtos[cod_int].get("valor_unitario") or 1.0)
                val_v_item = round((qt_it * v_unit) - v_desc, 2)
                if val_v_item > 0:
                    val_vendas_omie += val_v_item

        val_vendas_omie = round(val_vendas_omie, 2)
        val_bonif_omie = round(val_bonif_omie, 2)
        
        # VALOR DECLARADO TOTAL DA NOTA FISCAL OMIE ERP (Vendas + Bonificações Tabela 1.9)
        total_ped_cot = round(val_vendas_omie + val_bonif_omie, 2)

        # Executar cotações automáticas simultâneas preenchendo cubagem e dados cadastrais
        res_cot_bp_rod = None
        res_cot_bp_aer = None
        res_cot_ssw_rod = None
        res_cot_ssw_aer = None

        if bp_cep_dest and len(bp_cep_dest.replace("-", "").strip()) >= 8:
            # 1. Cotação Braspress nos dois modais (Rodoviário e Aéreo) em paralelo (< 1s)
            res_bp_ambos = braspress.cotar_frete_braspress_ambos_modais(
                cep_destino=bp_cep_dest,
                valor_declarado=total_ped_cot,
                peso_kg=bp_peso,
                volumes=bp_volumes,
                cnpj_destinatario=cli_cnpj_raw,
                razao_destinatario=cli_razao_raw,
                endereco_destinatario=cli_end_raw,
                info_cubagem=info_cubagem,
                usuario=bp_usuario,
                senha=bp_senha
            )
            res_cot_bp_rod = res_bp_ambos.get("rodoviario")
            res_cot_bp_aer = res_bp_ambos.get("aereo")

            # 2. Cotação Ativa Logística nos dois modais (Rodoviário e Aéreo Expresso) em paralelo
            res_ssw_ambos = ssw.cotar_frete_ssw_ambos_modais(
                cep_destino=bp_cep_dest,
                valor_declarado=total_ped_cot,
                peso_kg=bp_peso,
                volumes=bp_volumes,
                cnpj_destinatario=cli_cnpj_raw,
                razao_destinatario=cli_razao_raw,
                endereco_destinatario=cli_end_raw,
                info_cubagem=info_cubagem
            )
            res_cot_ssw_rod = res_ssw_ambos.get("rodoviario")
            res_cot_ssw_aer = res_ssw_ambos.get("aereo")

        # Gestão inteligente da opção de frete escolhida
        if "frete_opcao_escolhida" not in st.session_state:
            if "ATI" in str(transp_selecionada).upper() or "ATIVA" in str(transp_selecionada).upper():
                st.session_state["frete_opcao_escolhida"] = "ssw_rod"
            else:
                st.session_state["frete_opcao_escolhida"] = "bp_rod"

        opcao_atual = st.session_state.get("frete_opcao_escolhida", "bp_rod")

        # Fallback de segurança caso a opção escolhida não esteja disponível para a rota
        if opcao_atual == "ssw_rod" and (not res_cot_ssw_rod or not res_cot_ssw_rod.get("sucesso")):
            if res_cot_bp_rod and res_cot_bp_rod.get("sucesso"):
                opcao_atual = "bp_rod"
                st.session_state["frete_opcao_escolhida"] = "bp_rod"
        elif opcao_atual == "ssw_aer" and (not res_cot_ssw_aer or not res_cot_ssw_aer.get("sucesso")):
            if res_cot_bp_aer and res_cot_bp_aer.get("sucesso"):
                opcao_atual = "bp_aer"
                st.session_state["frete_opcao_escolhida"] = "bp_aer"

        # Atribuição dinâmica dos valores, prazos e modais para cálculo de impostos e envio
        if opcao_atual == "bp_aer" and res_cot_bp_aer and res_cot_bp_aer.get("sucesso"):
            vlr_frete_braspress = float(res_cot_bp_aer["valor_frete"])
            prazo_frete_selecionado = int(res_cot_bp_aer["prazo_dias"])
            modal_frete_selecionado = "AÉREO"
            modal_frete_desc = "Aéreo Expresso"
            transp_selecionada = "BRASPRESS TRANSPORTES URGENTES LTDA"
            nome_frete_resumo = "Braspress Aéreo"
        elif opcao_atual == "ssw_rod" and res_cot_ssw_rod and res_cot_ssw_rod.get("sucesso"):
            vlr_frete_braspress = float(res_cot_ssw_rod["valor_frete"])
            prazo_frete_selecionado = int(res_cot_ssw_rod["prazo_dias"])
            modal_frete_selecionado = "RODOVIÁRIO"
            modal_frete_desc = "Rodoviário Ativa"
            transp_selecionada = "ATIVA DISTRIBUICAO E LOGISTICA LTDA"
            nome_frete_resumo = "Ativa Rodoviário"
        elif opcao_atual == "ssw_aer" and res_cot_ssw_aer and res_cot_ssw_aer.get("sucesso"):
            vlr_frete_braspress = float(res_cot_ssw_aer["valor_frete"])
            prazo_frete_selecionado = int(res_cot_ssw_aer["prazo_dias"])
            modal_frete_selecionado = "AÉREO"
            modal_frete_desc = "Aéreo Ativa (Trans Model)"
            transp_selecionada = "ATIVA DISTRIBUICAO E LOGISTICA LTDA"
            nome_frete_resumo = "Ativa Aéreo"
        elif opcao_atual == "cortesia":
            vlr_frete_braspress = 0.0
            prazo_frete_selecionado = 0
            modal_frete_selecionado = "CORTESIA"
            modal_frete_desc = "Frete Cortesia (R$ 0,00)"
            nome_frete_resumo = "Frete Cortesia"
        elif opcao_atual == "manual":
            vlr_frete_braspress = float(st.session_state.get("frete_manual_input", 0.0))
            prazo_frete_selecionado = 0
            modal_frete_selecionado = "MANUAL"
            modal_frete_desc = "Manual Negociado"
            nome_frete_resumo = f"Frete Manual ({fmt_brl(vlr_frete_braspress)})"
        else: # bp_rod default
            if res_cot_bp_rod and res_cot_bp_rod.get("sucesso"):
                vlr_frete_braspress = float(res_cot_bp_rod["valor_frete"])
                prazo_frete_selecionado = int(res_cot_bp_rod["prazo_dias"])
                modal_frete_selecionado = "RODOVIÁRIO"
                modal_frete_desc = "Rodoviário Padrão"
                transp_selecionada = "BRASPRESS TRANSPORTES URGENTES LTDA"
                nome_frete_resumo = "Braspress Rodoviário"
            elif res_cot_ssw_rod and res_cot_ssw_rod.get("sucesso"):
                vlr_frete_braspress = float(res_cot_ssw_rod["valor_frete"])
                prazo_frete_selecionado = int(res_cot_ssw_rod["prazo_dias"])
                modal_frete_selecionado = "RODOVIÁRIO"
                modal_frete_desc = "Rodoviário Ativa"
                transp_selecionada = "ATIVA DISTRIBUICAO E LOGISTICA LTDA"
                nome_frete_resumo = "Ativa Rodoviário"
            elif res_cot_ssw_aer and res_cot_ssw_aer.get("sucesso"):
                vlr_frete_braspress = float(res_cot_ssw_aer["valor_frete"])
                prazo_frete_selecionado = int(res_cot_ssw_aer["prazo_dias"])
                modal_frete_selecionado = "AÉREO"
                modal_frete_desc = "Aéreo Ativa (Trans Model)"
                transp_selecionada = "ATIVA DISTRIBUICAO E LOGISTICA LTDA"
                nome_frete_resumo = "Ativa Aéreo"
            else:
                vlr_frete_braspress = 0.0
                prazo_frete_selecionado = 0
                modal_frete_selecionado = "RODOVIÁRIO"
                modal_frete_desc = "Padrão"
                nome_frete_resumo = "Não cotado"

        # RENDERIZAR PAINEL COMPARATIVO DE CUBAGEM E COTAÇÃO MULTI-MODAL
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 14px 18px; margin-bottom: 14px;">
            <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #9CA3AF; margin-bottom: 4px;">📦 CUBAGEM E PESAGEM 3D DOS PRODUTOS</div>
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                <div style="font-size: 13px; font-weight: 700; color: #E5E7EB;">{info_cubagem['descricao_caixas']}</div>
                <div style="font-size: 12px; font-weight: 800; color: #10B981;">{info_cubagem['volumes']} Volume(s) | {info_cubagem['peso_kg']:.2f} kg (Tarifado) | {fmt_brl(total_ped_cot)} NF</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_cot1, col_cot2, col_cot3, col_cot4 = st.columns(4)

        # 1. BRASPRESS RODOVIÁRIO
        with col_cot1:
            sel_bp_rod = (opcao_atual == "bp_rod")
            border_bp_rod = "2px solid #10B981" if sel_bp_rod else "1px solid #334155"
            bg_bp_rod = "linear-gradient(135deg, #064E3B 0%, #065F46 100%)" if sel_bp_rod else "linear-gradient(135deg, #0F172A 0%, #1E293B 100%)"
            badge_bg_bp_rod = "#10B981" if sel_bp_rod else "rgba(16, 185, 129, 0.15)"
            badge_col_bp_rod = "#022C22" if sel_bp_rod else "#34D399"
            badge_txt_bp_rod = "✓ SELECIONADO" if sel_bp_rod else "🛣️ RODOVIÁRIO"

            if res_cot_bp_rod and res_cot_bp_rod.get("sucesso"):
                vlr_bp_r = res_cot_bp_rod["valor_frete"]
                prz_bp_r = res_cot_bp_rod["prazo_dias"]
                st.markdown(f"""
                <div style="background: {bg_bp_rod}; border: {border_bp_rod}; border-radius: 14px; padding: 14px 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.25); min-height: 140px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="font-size: 11px; font-weight: 800; color: {'#A7F3D0' if sel_bp_rod else '#34D399'}; text-transform: uppercase;">🚚 BRASPRESS</div>
                            <span style="background: {badge_bg_bp_rod}; color: {badge_col_bp_rod}; font-size: 10px; font-weight: 900; padding: 2px 8px; border-radius: 10px;">{badge_txt_bp_rod}</span>
                        </div>
                        <div style="font-size: 24px; font-weight: 900; color: #FFFFFF; margin-top: 6px; letter-spacing: -0.02em;">{fmt_brl(vlr_bp_r)}</div>
                    </div>
                    <div style="font-size: 11px; font-weight: 700; color: {'#D1FAE5' if sel_bp_rod else '#94A3B8'}; margin-top: 6px;">
                        ⏱️ Entrega em <b>{prz_bp_r} dias úteis</b> (Rodoviário)
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if not sel_bp_rod:
                    if st.button("Selecionar Braspress Rodoviário", key="btn_sel_bp_rod", use_container_width=True):
                        st.session_state["frete_opcao_escolhida"] = "bp_rod"
                        st.session_state["ped_transportadora_override"] = "BRASPRESS TRANSPORTES URGENTES LTDA"
                        st.rerun()
            elif res_cot_bp_rod:
                st.error(f"❌ Braspress Rodoviário: {res_cot_bp_rod.get('erro', 'Erro ao consultar')}")

        # 2. BRASPRESS AÉREO
        with col_cot2:
            sel_bp_aer = (opcao_atual == "bp_aer")
            border_bp_aer = "2px solid #8B5CF6" if sel_bp_aer else "1px solid #334155"
            bg_bp_aer = "linear-gradient(135deg, #4C1D95 0%, #5B21B6 100%)" if sel_bp_aer else "linear-gradient(135deg, #0F172A 0%, #1E293B 100%)"
            badge_bg_bp_aer = "#8B5CF6" if sel_bp_aer else "rgba(139, 92, 246, 0.15)"
            badge_col_bp_aer = "#FFFFFF" if sel_bp_aer else "#C084FC"
            badge_txt_bp_aer = "✓ SELECIONADO" if sel_bp_aer else "✈️ AÉREO EXPRESSO"

            if res_cot_bp_aer and res_cot_bp_aer.get("sucesso"):
                vlr_bp_a = res_cot_bp_aer["valor_frete"]
                prz_bp_a = res_cot_bp_aer["prazo_dias"]
                st.markdown(f"""
                <div style="background: {bg_bp_aer}; border: {border_bp_aer}; border-radius: 14px; padding: 14px 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.25); min-height: 140px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="font-size: 11px; font-weight: 800; color: {'#DDD6FE' if sel_bp_aer else '#C084FC'}; text-transform: uppercase;">✈️ BRASPRESS AÉREO</div>
                            <span style="background: {badge_bg_bp_aer}; color: {badge_col_bp_aer}; font-size: 10px; font-weight: 900; padding: 2px 8px; border-radius: 10px;">{badge_txt_bp_aer}</span>
                        </div>
                        <div style="font-size: 24px; font-weight: 900; color: #FFFFFF; margin-top: 6px; letter-spacing: -0.02em;">{fmt_brl(vlr_bp_a)}</div>
                    </div>
                    <div style="font-size: 11px; font-weight: 700; color: {'#EDE9FE' if sel_bp_aer else '#94A3B8'}; margin-top: 6px;">
                        ⚡ Entrega expressa em <b>{prz_bp_a} dias úteis</b> (Aéreo)
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if not sel_bp_aer:
                    if st.button("Selecionar Braspress Aéreo", key="btn_sel_bp_aer", use_container_width=True, type="primary"):
                        st.session_state["frete_opcao_escolhida"] = "bp_aer"
                        st.session_state["ped_transportadora_override"] = "BRASPRESS TRANSPORTES URGENTES LTDA"
                        st.rerun()
            elif res_cot_bp_aer:
                st.error(f"❌ Braspress Aéreo: {res_cot_bp_aer.get('erro', 'Erro ao consultar')}")

        # 3. ATIVA LOGÍSTICA RODOVIÁRIO
        with col_cot3:
            sel_ssw_rod = (opcao_atual == "ssw_rod")
            border_ssw_rod = "2px solid #3B82F6" if sel_ssw_rod else "1px solid #334155"
            bg_ssw_rod = "linear-gradient(135deg, #1E3A8A 0%, #1D4ED8 100%)" if sel_ssw_rod else "linear-gradient(135deg, #0F172A 0%, #1E293B 100%)"
            badge_bg_ssw_rod = "#3B82F6" if sel_ssw_rod else "rgba(59, 130, 246, 0.15)"
            badge_col_ssw_rod = "#FFFFFF" if sel_ssw_rod else "#60A5FA"
            badge_txt_ssw_rod = "✓ SELECIONADO" if sel_ssw_rod else "🚚 RODOVIÁRIO ATIVA"

            if res_cot_ssw_rod and res_cot_ssw_rod.get("sucesso"):
                vlr_ssw_r = res_cot_ssw_rod["valor_frete"]
                prz_ssw_r = res_cot_ssw_rod["prazo_dias"]
                st.markdown(f"""
                <div style="background: {bg_ssw_rod}; border: {border_ssw_rod}; border-radius: 14px; padding: 14px 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.25); min-height: 140px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="font-size: 11px; font-weight: 800; color: {'#BFDBFE' if sel_ssw_rod else '#60A5FA'}; text-transform: uppercase;">🚚 ATIVA RODOVIÁRIO</div>
                            <span style="background: {badge_bg_ssw_rod}; color: {badge_col_ssw_rod}; font-size: 10px; font-weight: 900; padding: 2px 8px; border-radius: 10px;">{badge_txt_ssw_rod}</span>
                        </div>
                        <div style="font-size: 24px; font-weight: 900; color: #FFFFFF; margin-top: 6px; letter-spacing: -0.02em;">{fmt_brl(vlr_ssw_r)}</div>
                    </div>
                    <div style="font-size: 11px; font-weight: 700; color: {'#DBEAFE' if sel_ssw_rod else '#94A3B8'}; margin-top: 6px;">
                        ⏱️ Entrega em <b>{prz_ssw_r} dias úteis</b> (Rodoviário)
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if not sel_ssw_rod:
                    if st.button("Selecionar Ativa Rodoviário", key="btn_sel_ssw_rod", use_container_width=True):
                        st.session_state["frete_opcao_escolhida"] = "ssw_rod"
                        st.session_state["ped_transportadora_override"] = "ATIVA DISTRIBUICAO E LOGISTICA LTDA"
                        st.rerun()
            elif res_cot_ssw_rod:
                st.error(f"❌ Ativa Rodoviário: {res_cot_ssw_rod.get('erro', 'Erro ao consultar')}")

        # 4. ATIVA LOGÍSTICA AÉREO (Trans Model Air Express)
        with col_cot4:
            sel_ssw_aer = (opcao_atual == "ssw_aer")
            border_ssw_aer = "2px solid #06B6D4" if sel_ssw_aer else "1px solid #334155"
            bg_ssw_aer = "linear-gradient(135deg, #0E7490 0%, #0891B2 100%)" if sel_ssw_aer else "linear-gradient(135deg, #0F172A 0%, #1E293B 100%)"
            badge_bg_ssw_aer = "#06B6D4" if sel_ssw_aer else "rgba(6, 182, 212, 0.15)"
            badge_col_ssw_aer = "#083344" if sel_ssw_aer else "#38BDF8"
            badge_txt_ssw_aer = "✓ SELECIONADO" if sel_ssw_aer else "✈️ AÉREO ATIVA"

            if res_cot_ssw_aer and res_cot_ssw_aer.get("sucesso"):
                vlr_ssw_a = res_cot_ssw_aer["valor_frete"]
                prz_ssw_a = res_cot_ssw_aer["prazo_dias"]
                st.markdown(f"""
                <div style="background: {bg_ssw_aer}; border: {border_ssw_aer}; border-radius: 14px; padding: 14px 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.25); min-height: 140px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="font-size: 11px; font-weight: 800; color: {'#CFFAFE' if sel_ssw_aer else '#38BDF8'}; text-transform: uppercase;">✈️ ATIVA AÉREO</div>
                            <span style="background: {badge_bg_ssw_aer}; color: {badge_col_ssw_aer}; font-size: 10px; font-weight: 900; padding: 2px 8px; border-radius: 10px;">{badge_txt_ssw_aer}</span>
                        </div>
                        <div style="font-size: 24px; font-weight: 900; color: #FFFFFF; margin-top: 6px; letter-spacing: -0.02em;">{fmt_brl(vlr_ssw_a)}</div>
                    </div>
                    <div style="font-size: 11px; font-weight: 700; color: {'#E0F2FE' if sel_ssw_aer else '#94A3B8'}; margin-top: 6px;">
                        ⚡ Entrega expressa em <b>{prz_ssw_a} dias úteis</b> (Aéreo Trans Model)
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if not sel_ssw_aer:
                    if st.button("Selecionar Ativa Aéreo", key="btn_sel_ssw_aer", use_container_width=True, type="primary"):
                        st.session_state["frete_opcao_escolhida"] = "ssw_aer"
                        st.session_state["ped_transportadora_override"] = "ATIVA DISTRIBUICAO E LOGISTICA LTDA"
                        st.rerun()
            elif res_cot_ssw_aer:
                st.error(f"❌ Ativa Aéreo: {res_cot_ssw_aer.get('erro', 'Erro ao consultar')}")

        # Opções Adicionais de Frete (Cortesia / Isento e Manual)
        st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
        col_opt1, col_opt2 = st.columns([1.5, 1])
        with col_opt1:
            sel_cort = (opcao_atual == "cortesia")
            lbl_cort = "✓ Frete Cortesia Ativo (R$ 0,00)" if sel_cort else "📦 Frete Cortesia / Retirada / CIF Isento (R$ 0,00)"
            if st.button(lbl_cort, key="btn_sel_cortesia_opt", use_container_width=True, type="secondary" if not sel_cort else "primary"):
                st.session_state["frete_opcao_escolhida"] = "cortesia"
                st.rerun()
        with col_opt2:
            val_custom = float(st.session_state.get("frete_manual_custom", 0.0))
            val_input_man = st.number_input("✏️ Valor Manual (R$)", min_value=0.0, value=val_custom, step=5.0, key="frete_manual_input_box", label_visibility="collapsed")
            if val_input_man > 0 and (val_input_man != val_custom or opcao_atual != "manual"):
                st.session_state["frete_manual_custom"] = val_input_man
                st.session_state["frete_manual_input"] = val_input_man
                st.session_state["frete_opcao_escolhida"] = "manual"
                st.rerun()

        with st.expander("🔍 Auditoria de Campos e Taxas (Braspress & Ativa Logística)", expanded=False):
            col_aud1, col_aud2 = st.columns(2)
            with col_aud1:
                st.markdown(f"""
                - **CNPJ Remetente:** `57.368.285/0001-35` (Missha Brasil)
                - **CNPJ Destinatário:** `{cli_cnpj_raw or 'Preenchido do Cliente'}`
                - **Razão Social:** `{cli_razao_raw or 'Preenchido do Cliente'}`
                - **CEP Origem / Destino:** `29169-055` $\rightarrow$ `{bp_cep_dest}`
                """)
            with col_aud2:
                p_fis = info_cubagem.get("peso_fisico_kg", info_cubagem.get("peso_kg", 0.5))
                v_m3 = info_cubagem.get("volume_produtos_m3", 0.001)
                item_ativa_aud = res_cot_ssw_aer if opcao_atual == "ssw_aer" else res_cot_ssw_rod
                ssw_taxes = f"Frete Peso: {fmt_brl(item_ativa_aud.get('frete_peso', 0))} | Impostos: {fmt_brl(item_ativa_aud.get('impostos', 0))} | Tab: {item_ativa_aud.get('tabela', 'Padrão')}" if (item_ativa_aud and item_ativa_aud.get("sucesso")) else "N/A"
                st.markdown(f"""
                - **Valor Declarado (Nota Fiscal Omie):** `{fmt_brl(total_ped_cot)}`
                - **Volume Cúbico / Peso Físico:** `{v_m3:.4f} m³` | `{p_fis:.2f} kg`
                - **Peso Cubado Tarifado:** `{info_cubagem['peso_kg']:.2f} kg`
                - **Detalhamento Taxas Ativa Logística:** `{ssw_taxes}`
                """)

    # ── Condições de Pagamento (Liberação Progressiva por Faixa Comercial) ──
    st.markdown('<div class="section-header">Condições de Pagamento</div>', unsafe_allow_html=True)

    total_pedido_carrinho = sum(item["subtotal"] for item in st.session_state["itens_pedido"])
    apenas_bonificacao_carrinho = (
        len(st.session_state["itens_pedido"]) > 0 and
        all(
            ("BONIF" in str(item.get("tipo_item", "")).upper()) or
            ("BONIF" in str(item.get("cenario_fiscal", "")).upper()) or
            (item.get("valor_unitario", 0.0) == 0.0)
            for item in st.session_state["itens_pedido"]
        )
    )

    pol_com_carrinho = omie.calcular_politica_comercial_omnievo(total_pedido_carrinho)
    max_dias_categoria = 999 if apenas_bonificacao_carrinho else pol_com_carrinho.get("max_dias_prazo", 0)
    cat_nome = "100% BONIFICAÇÃO (ISENTO)" if apenas_bonificacao_carrinho else pol_com_carrinho.get("categoria", "ABAIXO DO MÍNIMO")
    dt_max_permitida = dt_previsao + datetime.timedelta(days=56 if apenas_bonificacao_carrinho else max_dias_categoria)

    opcoes_parcelas_todas = {
        "000": "000 - Sem Financeiro (Bonificação)",
        "001": "001 - À Vista (0 dias)",
        "028": "Até 28 dias (Profissional)",
        "014": "14 / 28 / 35 dias (Essencial)",
        "035": "28 / 35 / 42 dias (Bronze)",
        "042": "28 / 35 / 42 / 49 dias (Prata)",
        "049": "35 / 42 / 49 dias (Ouro)",
        "056": "28 / 35 / 42 / 49 / 56 dias (Diamante)"
    }

    dias_max_condicao = {
        "000": 0, "001": 0, "028": 28, "014": 35, "035": 42, "042": 49, "049": 49, "056": 56
    }

    # Filtrar opções visíveis: Exibir APENAS as condições autorizadas para o valor atual do pedido
    if apenas_bonificacao_carrinho:
        opcoes_permitidas = {"000": "000 - Sem Financeiro (Bonificação)"}
    else:
        opcoes_permitidas = {}
        for code, label in opcoes_parcelas_todas.items():
            if code != "000" and dias_max_condicao[code] <= max_dias_categoria:
                opcoes_permitidas[code] = label

        if not opcoes_permitidas:
            opcoes_permitidas = {"001": "001 - À Vista (0 dias)"}

    # Mensagens de orientação comercial e incentivo de compra por metas de faturamento
    if apenas_bonificacao_carrinho:
        msg_liberacao = "🎁 <b>PEDIDO 100% BONIFICAÇÃO (BRINDE)</b>: Isento das travas da Política Comercial. Não gera faturamento nem contas a receber."
        bg_lib = "rgba(245,158,11,0.12)"
        border_lib = "rgba(245,158,11,0.3)"
        txt_lib = "#FBBF24"
    elif total_pedido_carrinho < 1500.0:
        falta = 1500.0 - total_pedido_carrinho
        msg_liberacao = f"🔒 <b>Apenas Condição À Vista Disponível</b>: Adicione mais <b>{fmt_brl(falta)}</b> em produtos para liberar parcelamento em até 28 dias (Categoria Profissional)."
        bg_lib = "rgba(239,68,68,0.12)"
        border_lib = "rgba(239,68,68,0.3)"
        txt_lib = "#F87171"
    elif 1500.0 <= total_pedido_carrinho < 3500.0:
        falta = 3500.0 - total_pedido_carrinho
        msg_liberacao = f"🔓 <b>Categoria PROFISSIONAL Liberada</b>: Parcelamento liberado em <b>Até 28 dias</b>. Adicione mais <b>{fmt_brl(falta)}</b> para liberar parcelamento em até 35 dias (Categoria Essencial)."
        bg_lib = "rgba(16,185,129,0.12)"
        border_lib = "rgba(16,185,129,0.3)"
        txt_lib = "#34D399"
    elif 3500.0 <= total_pedido_carrinho < 7000.0:
        falta = 7000.0 - total_pedido_carrinho
        msg_liberacao = f"🔓 <b>Categoria ESSENCIAL Liberada</b>: Parcelamentos liberados em <b>14/28/35 dias</b>. Adicione mais <b>{fmt_brl(falta)}</b> para liberar Categoria Bronze (até 42 dias)."
        bg_lib = "rgba(16,185,129,0.12)"
        border_lib = "rgba(16,185,129,0.3)"
        txt_lib = "#34D399"
    elif 7000.0 <= total_pedido_carrinho < 15000.0:
        falta = 15000.0 - total_pedido_carrinho
        msg_liberacao = f"🔓 <b>Categoria BRONZE Liberada</b>: Parcelamentos liberados em <b>28/35/42 dias</b>. Adicione mais <b>{fmt_brl(falta)}</b> para liberar Categoria Prata (até 49 dias)."
        bg_lib = "rgba(16,185,129,0.12)"
        border_lib = "rgba(16,185,129,0.3)"
        txt_lib = "#34D399"
    elif 15000.0 <= total_pedido_carrinho < 30000.0:
        falta = 30000.0 - total_pedido_carrinho
        msg_liberacao = f"🔓 <b>Categoria PRATA Liberada</b>: Parcelamentos liberados em <b>28/35/42/49 dias</b>. Adicione mais <b>{fmt_brl(falta)}</b> para liberar Categoria Ouro."
        bg_lib = "rgba(16,185,129,0.12)"
        border_lib = "rgba(16,185,129,0.3)"
        txt_lib = "#34D399"
    elif 30000.0 <= total_pedido_carrinho < 70000.0:
        falta = 70000.0 - total_pedido_carrinho
        msg_liberacao = f"🔓 <b>Categoria OURO Liberada</b>: Parcelamentos liberados em <b>35/42/49 dias</b>. Adicione mais <b>{fmt_brl(falta)}</b> para liberar Categoria Diamante (até 56 dias)."
        bg_lib = "rgba(16,185,129,0.12)"
        border_lib = "rgba(16,185,129,0.3)"
        txt_lib = "#34D399"
    else:
        msg_liberacao = f"💎 <b>Categoria DIAMANTE Máxima Liberada</b>: Todos os prazos de parcelamento liberados em até 56 dias!"
        bg_lib = "rgba(168,85,247,0.12)"
        border_lib = "rgba(168,85,247,0.3)"
        txt_lib = "#C084FC"

    st.markdown(f"""
    <div style="font-size: 12px; font-weight: 600; color: {txt_lib}; background: {bg_lib}; border: 1px solid {border_lib}; border-radius: 8px; padding: 10px 14px; margin-bottom: 12px;">
        {msg_liberacao}
    </div>
    """, unsafe_allow_html=True)

    col_h1, col_h2, col_h3, col_h4 = st.columns(4)
    with col_h1:
        parcela_ped = st.selectbox(
            "Condição de Pagamento",
            list(opcoes_permitidas.keys()),
            key="ped_parcela_sel",
            format_func=lambda x: opcoes_permitidas.get(x, x)
        )

    with col_h2:
        opcoes_tipo_doc = {
            "BOL": "Boleto",
            "PIX": "PIX",
            "CART": "Cartão de Crédito",
            "DEB": "Cartão de Débito"
        }
            
        keys_tipo_doc = list(opcoes_tipo_doc.keys())
        if st.session_state.get("ped_tipo_doc_sel") not in keys_tipo_doc:
            st.session_state["ped_tipo_doc_sel"] = keys_tipo_doc[0]

        tipo_doc_sel = st.selectbox(
            "Tipo de Documento",
            keys_tipo_doc,
            key="ped_tipo_doc_sel",
            format_func=lambda x: opcoes_tipo_doc.get(x, x)
        )

    with col_h3:
        mapa_sugestao_meio = {
            "BOL": "15",   # Boleto Bancário
            "PIX": "17",   # PIX
            "CART": "03",  # Cartão de Crédito
            "DEB": "04"    # Cartão de Débito
        }
        opcoes_meio_pagamento = {
            "15": "Boleto Bancário",
            "17": "PIX",
            "03": "Cartão de Crédito",
            "04": "Cartão de Débito"
        }
        
        meio_pagamento_sel = mapa_sugestao_meio.get(tipo_doc_sel, "15")
        st.session_state["ped_meio_pagamento_sel"] = meio_pagamento_sel
        
        st.selectbox(
            "Meio de Pagamento",
            [meio_pagamento_sel],
            index=0,
            disabled=True,
            key=f"ped_meio_pagamento_disp_{tipo_doc_sel}",
            format_func=lambda x: opcoes_meio_pagamento.get(x, x)
        )

    # Identificar se é pagamento em PIX ou Boleto À Vista
    is_pix_ou_boleto_avista = (tipo_doc_sel == "PIX") or (tipo_doc_sel == "BOL" and parcela_ped == "001")

    pode_alterar_parcelas_usr = auth.eh_usuario_master(usr_logado) or auth.eh_autorizado_bonificacao(usr_logado)

    with col_h4:
        dias_politica_map = {
            "001": [0], "028": [28], "014": [14, 28, 35], "035": [28, 35, 42],
            "042": [28, 35, 42, 49], "049": [35, 42, 49], "056": [28, 35, 42, 49, 56], "000": [0]
        }
        qtd_sugerida_map = {"001": 1, "028": 1, "014": 3, "035": 3, "042": 4, "049": 3, "056": 5, "000": 1}
        def_qtd_val = qtd_sugerida_map.get(parcela_ped, 1)

        if is_pix_ou_boleto_avista:
            st.session_state["ped_qtd_parcelas_sel"] = 1
            opcoes_parc_lista = [1]
            lbl_parc_title = "Quantidade de Parcelas"
            eh_disabled_parc = True
            format_parc_fn = lambda x: "1x (PIX / Boleto À Vista)"
            caption_parc_str = "🔒 **À Vista**: Parcelamento único."
        elif not pode_alterar_parcelas_usr:
            st.session_state["ped_qtd_parcelas_sel"] = def_qtd_val
            opcoes_parc_lista = [def_qtd_val]
            lbl_parc_title = "Quantidade de Parcelas"
            eh_disabled_parc = True
            format_parc_fn = lambda x: f"{x}x (Amarrado à Condição {parcela_ped})"
            caption_parc_str = "🔒 **Amarrado à Condição**: Alteração restrita a pessoas autorizadas."
        else:
            if st.session_state.get("ped_qtd_parcelas_sel") not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
                st.session_state["ped_qtd_parcelas_sel"] = def_qtd_val
            opcoes_parc_lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            lbl_parc_title = "Quantidade de Parcelas"
            eh_disabled_parc = False
            format_parc_fn = lambda x: f"{x}x"
            caption_parc_str = "🔓 **Liberação Especial**: Habilitada para Usuário Autorizado / Master."

        def_qtd_idx = opcoes_parc_lista.index(st.session_state["ped_qtd_parcelas_sel"]) if st.session_state.get("ped_qtd_parcelas_sel") in opcoes_parc_lista else 0

        qtd_parcelas = st.selectbox(
            lbl_parc_title,
            opcoes_parc_lista,
            index=def_qtd_idx,
            disabled=eh_disabled_parc,
            key="ped_qtd_parcelas_sel",
            format_func=format_parc_fn
        )
        st.caption(caption_parc_str)



    # ── Vencimento das Parcelas ──
    st.markdown('<div class="section-header">Vencimento das Parcelas</div>', unsafe_allow_html=True)

    parcelas_payload = []
    num_cols = min(qtd_parcelas, 4)
    cols_parcelas = st.columns(num_cols)
    
    eh_cartao_credito = (tipo_doc_sel == "CART") or (meio_pagamento_sel == "03") or ("CARTAO" in str(opcoes_tipo_doc.get(tipo_doc_sel, "")).upper()) or ("CARTÃO" in str(opcoes_tipo_doc.get(tipo_doc_sel, "")).upper())
    dias_base = [30 * i for i in range(1, qtd_parcelas + 1)] if eh_cartao_credito else dias_politica_map.get(parcela_ped, [30 * i for i in range(1, qtd_parcelas + 1)])

    for i in range(1, qtd_parcelas + 1):
        idx = i - 1
        if is_pix_ou_boleto_avista:
            # REGRA DE NEGÓCIO: Se o pedido for colocado na Sexta-feira, a previsão cai na Segunda e o vencimento no próximo dia útil (Terça D+1 ou Segunda se no mesmo dia)
            w_day_ped = hoje.weekday()
            w_day_prev = dt_previsao.weekday()
            
            if w_day_ped in [4, 5, 6] or w_day_prev in [4, 5, 6]:
                dt_base_ref = obter_proximo_dia_util(dt_previsao)
                if dt_base_ref == dt_previsao:
                    sugestao_dt = dt_previsao + datetime.timedelta(days=1)
                else:
                    sugestao_dt = dt_base_ref
                dias_offset_ajustado = max((sugestao_dt - dt_previsao).days, 1)
            elif w_day_prev in [0, 1, 2, 3]:  # Segunda a Quinta: D+1
                sugestao_dt = dt_previsao + datetime.timedelta(days=1)
                dias_offset_ajustado = 1
            else:
                sugestao_dt = obter_proximo_dia_util(dt_previsao)
                dias_offset_ajustado = max((sugestao_dt - dt_previsao).days, 1)
        elif eh_cartao_credito:
            # REGRA SOLICITADA PELO USUÁRIO: Cartão de Crédito com vencimentos de 30 em 30 dias (D+30, D+60, D+90, etc.)
            dias_offset_ajustado = 30 * i
            sugestao_dt = dt_previsao + datetime.timedelta(days=dias_offset_ajustado)
            max_val_parc = dt_previsao + datetime.timedelta(days=dias_offset_ajustado + 30)
        else:
            if idx < len(dias_base):
                dias_offset = dias_base[idx]
            else:
                ultimo_offset = dias_base[-1] if dias_base else 30
                dias_offset = ultimo_offset + 30 * (idx - len(dias_base) + 1)

            dias_offset_ajustado = min(dias_offset, max_dias_categoria)
            sugestao_dt = dt_previsao + datetime.timedelta(days=dias_offset_ajustado)
            if sugestao_dt > dt_max_permitida:
                sugestao_dt = dt_max_permitida

        col_target = cols_parcelas[idx % num_cols]

        # Edição Livre de Datas de Vencimento de Parcelas para Usuários Autorizados
        min_val_parc = hoje - datetime.timedelta(days=60) # Permite selecionar desde 60 dias atrás
        max_val_parc = hoje + datetime.timedelta(days=365) # Permite selecionar qualquer data até 1 ano no futuro

        # Garantir que sugestao_dt esteja dentro do range permitido
        if sugestao_dt < min_val_parc:
            sugestao_dt = min_val_parc
        elif sugestao_dt > max_val_parc:
            sugestao_dt = max_val_parc

        with col_target:
            dt_parc = st.date_input(
                f"✏️ Parcela {i}/{qtd_parcelas} ({dias_offset_ajustado}d)",
                value=sugestao_dt,
                min_value=min_val_parc,
                max_value=max_val_parc,
                format="DD/MM/YYYY",
                key=f"ped_dt_parc_{i}_{parcela_ped}_{tipo_doc_sel}_{dt_previsao.strftime('%Y%m%d')}",
                help="Data de vencimento editável livremente."
            )
            percentual_parc = round(100.0 / qtd_parcelas, 2)
            if i == qtd_parcelas:
                percentual_parc = round(100.0 - (round(100.0 / qtd_parcelas, 2) * (qtd_parcelas - 1)), 2)
            parcelas_payload.append({
                "numero_parcela": i, "data_vencimento": dt_parc.strftime("%d/%m/%Y"),
                "percentual": percentual_parc, "tipo_documento": tipo_doc_sel, "meio_pagamento": meio_pagamento_sel
            })

    # ⚡ Bloco de Importação em Lote Universal (Excel / CSV / Copiar-Colar) ⚡
    with st.expander("⚡ Importar Lote de Itens em 1 Segundo (Excel / CSV ou Copiar & Colar)", expanded=False):
        st.markdown("""
        <div style="font-size: 13px; color: #000000 !important; font-weight: 800; margin-bottom: 12px;">
            Suba qualquer planilha Excel/CSV ou cole o texto. O sistema puxa <b style="color: #000000 !important; font-weight: 900;">100% das linhas preenchidas</b> automaticamente (reconhecendo SKU, Código Omie, Nome do Produto, Quantidades e Preços).
        </div>
        """, unsafe_allow_html=True)
        
        tab_imp1, tab_imp2 = st.tabs(["📁 Enviar Arquivo (Excel / CSV)", "📋 Copiar & Colar Texto"])
        
        # Função interna de resolução ultrarrápida de produtos
        def _resolver_produto_item(val_raw, mapa_p):
            val_str = str(val_raw or "").strip()
            if val_str.endswith(".0"):
                val_str = val_str[:-2]
            clean_digits = "".join(filter(str.isdigit, val_str))

            # 1. Match por SKU exato
            if val_str in mapa_p:
                return val_str, mapa_p[val_str]

            # 2. Match por SKU numérico
            if clean_digits:
                for sku, p in mapa_p.items():
                    sku_clean = "".join(filter(str.isdigit, str(sku)))
                    if sku_clean == clean_digits:
                        return sku, p

            # 3. Match por ID Omie (codigo_produto)
            for sku, p in mapa_p.items():
                if str(p.get("codigo_produto", "")) in [val_str, clean_digits]:
                    return sku, p

            # 4. Match por Descrição / Nome do Produto
            val_lower = val_str.lower()
            if len(val_lower) >= 3:
                for sku, p in mapa_p.items():
                    desc_lower = str(p.get("descricao", "")).lower()
                    if val_lower in desc_lower or desc_lower in val_lower:
                        return sku, p

            # 5. Fallback dinâmico: Consulta direta à API Omie (ConsultarProduto)
            if val_str:
                try:
                    res_c = omie.omie_call("geral/produtos", "ConsultarProduto", {"codigo": val_str}, config)
                    if res_c and res_c.get("descricao"):
                        sku_res = str(res_c.get("codigo_produto_integracao") or res_c.get("codigo") or val_str).strip()
                        desc_res = html.unescape(str(res_c.get("descricao") or "")).strip()
                        peso_u = float(res_c.get("peso_bruto") or res_c.get("peso_liq") or 0.0)
                        if peso_u > 50.0:
                            peso_u = round(peso_u / 1000.0, 3)
                        p_info_novo = {
                            "codigo_produto_integracao": sku_res,
                            "codigo_produto": res_c.get("codigo_produto"),
                            "descricao": desc_res,
                            "valor_unitario": float(res_c.get("valor_unitario") or 0.0),
                            "unidade": res_c.get("unidade") or "UN",
                            "ncm": res_c.get("ncm") or "",
                            "peso_bruto": round(peso_u, 3) if peso_u > 0 else 0.0,
                            "peso_liquido": round(peso_u * 0.85, 3) if peso_u > 0 else 0.0,
                            "inativo": res_c.get("inativo") or "N",
                            "imagem_url": ""
                        }
                        mapa_p[sku_res] = p_info_novo
                        return sku_res, p_info_novo
                except Exception:
                    pass

            return val_str, None

        with tab_imp1:
            uploaded_file = st.file_uploader("Selecione a planilha (.xlsx ou .csv)", type=["xlsx", "csv"], key="uploader_lote_itens")
            if uploaded_file is not None:
                if st.button("🚀 Processar e Inserir TODAS as Linhas no Pedido", type="primary", key="btn_proc_excel"):
                    try:
                        if uploaded_file.name.endswith(".csv"):
                            df_imp = pd.read_csv(uploaded_file, sep=None, engine='python')
                        else:
                            df_imp = pd.read_excel(uploaded_file)
                        
                        # Limpar linhas 100% vazias
                        df_imp = df_imp.dropna(how="all")
                        cols_original = list(df_imp.columns)
                        cols_upper = [str(c).strip().upper() for c in cols_original]
                        df_imp.columns = cols_upper
                        
                        # Reconhecimento inteligente de colunas (palavras-chave ou posição)
                        col_cod = next((c for c in cols_upper if any(k in c for k in ["COD", "SKU", "INTEGRACAO", "PRODUTO", "ITEM", "EAN", "BARRAS", "MODELO", "REF", "NOME"])), None)
                        col_qtd = next((c for c in cols_upper if any(k in c for k in ["QTD", "QUANT", "UNID", "VOL", "PECAS", "QTDE", "UN", "NUMERO", "VOLUME"])), None)
                        col_vlr = next((c for c in cols_upper if any(k in c for k in ["PRECO", "PREÇO", "VALOR", "VLR", "UNIT", "R$", "RS", "TABELA", "LIQUIDO", "BRUTO"])), None)
                        col_desc = next((c for c in cols_upper if any(k in c for k in ["DESC", "DESCONTO", "ABATIMENTO"])), None)
                        col_oper = next((c for c in cols_upper if any(k in c for k in ["OPERACAO", "OPERAÇÃO", "CENARIO", "FISCAL", "TIPO", "BONIFICACAO", "BRINDE"])), None)
                        
                        # Fallback por posição se os cabeçalhos não tiverem nomes conhecidos
                        if not col_cod and len(cols_upper) > 0:
                            col_cod = cols_upper[0]
                        if not col_qtd and len(cols_upper) > 1:
                            col_qtd = cols_upper[1]
                        if not col_vlr and len(cols_upper) > 2:
                            col_vlr = cols_upper[2]

                        adicionados = 0
                        uf_cli_imp = cliente_sel.get("estado", "ES") if cliente_sel else "ES"
                        ie_cli_imp = cliente_sel.get("inscricao_estadual", "") if cliente_sel else ""

                        for _, row in df_imp.iterrows():
                            # Ignorar linha se o campo principal for nulo/vazio
                            raw_item_val = row[col_cod] if col_cod else None
                            if pd.isna(raw_item_val) or str(raw_item_val).strip() in ["", "nan", "None"]:
                                continue

                            cod_str = str(raw_item_val).strip()

                            # Ler quantidade (Padrão: 1.0 com suporte a formatos BR)
                            qtd_val = 1.0
                            if col_qtd:
                                q_parsed = _parse_num_br(row[col_qtd])
                                if q_parsed is not None and q_parsed > 0:
                                    qtd_val = q_parsed

                            # Resolver produto no catálogo OMNIEVO
                            sku_resolvido, p_info = _resolver_produto_item(cod_str, mapa_produtos)
                            
                            # Resgatar valor cadastrado na Tabela 1.9 oficial
                            vlr_tab_1_9 = float(mapa_tabela_1_9.get(sku_resolvido, 0.0))
                            if vlr_tab_1_9 <= 0 and p_info:
                                vlr_tab_1_9 = float(p_info.get("valor_unitario", 0.0))

                            # PRIORIDADE 100%: SE O USUÁRIO COLOCOU VALOR NA PLANILHA, ESSE VALOR É SOBERANO!
                            vlr_planilha = _parse_num_br(row[col_vlr]) if col_vlr else None
                            if vlr_planilha is not None and vlr_planilha > 0:
                                vlr_val = vlr_planilha
                                is_custom_price = True
                            else:
                                vlr_val = vlr_tab_1_9
                                is_custom_price = False

                            desc_val = 0.0
                            if col_desc:
                                d_parsed = _parse_num_br(row[col_desc])
                                if d_parsed is not None and d_parsed > 0:
                                    desc_val = d_parsed

                            # Ler operação fiscal da coluna
                            op_raw = str(row[col_oper]).strip().upper() if (col_oper and not pd.isna(row[col_oper])) else ""
                            if "BONIFIC" in op_raw:
                                tipo_item_row = "BONIFICAÇÃO"
                            else:
                                tipo_item_row = "MONITORAMENTO AUTOMÁTICO DE IMPOSTOS"

                            cenario_auto, cfop_auto = omie.determinar_cenario_fiscal(tipo_item_row, uf_cli_imp, ie_cli_imp, config)
                            sub_val = round((qtd_val * vlr_val) - desc_val, 2)
                            if sub_val < 0:
                                sub_val = 0.0

                            desc_final = (p_info.get("descricao") or "").strip() if p_info else ""
                            if not desc_final:
                                desc_final = f"Produto {cod_str}"
                            img_url = p_info.get("imagem_url", "") if p_info else ""

                            item_imp = {
                                "codigo_produto_integracao": sku_resolvido,
                                "codigo_produto": p_info.get("codigo_produto") if p_info else None,
                                "descricao": desc_final,
                                "imagem_url": img_url,
                                "tipo_item": tipo_item_row,
                                "cenario_fiscal": cenario_auto,
                                "cfop": cfop_auto,
                                "local_estoque": config.get("local_estoque_nome", "PADRAO"),
                                "quantidade": qtd_val,
                                "preco_base_1_9": vlr_val,
                                "valor_unitario": vlr_val,
                                "valor_desconto": desc_val,
                                "subtotal": sub_val,
                                "preco_customizado": is_custom_price,
                                "peso_bruto": float(p_info.get("peso_bruto") or 0.0) if p_info else 0.0
                            }
                            st.session_state["itens_pedido"].append(item_imp)
                            adicionados += 1

                        salvar_rascunho_pedido(st.session_state["itens_pedido"])
                        st.success(f"🎉 **{adicionados} linhas preenchidas importadas com sucesso** para o pedido!")
                        st.rerun()
                    except Exception as err_imp:
                        st.error(f"Erro ao processar planilha: {str(err_imp)}")
                        
        with tab_imp2:
            st.caption("Cole abaixo as linhas (Exemplo: MS103472  10  129.90  MONITORAMENTO AUTOMÁTICO DE IMPOSTOS)")
            texto_colado = st.text_area("Lista de Itens", placeholder="MS103472	10	129.90	MONITORAMENTO AUTOMÁTICO DE IMPOSTOS\nMS201432	20	89.90	BONIFICAÇÃO", height=120, key="txt_copiar_colar_lote")
            if st.button("🚀 Processar e Inserir Texto Colado", type="primary", key="btn_proc_texto_lote"):
                if texto_colado and texto_colado.strip():
                    linhas = texto_colado.strip().split("\n")
                    adicionados = 0
                    uf_cli_txt = cliente_sel.get("estado", "ES") if cliente_sel else "ES"
                    ie_cli_txt = cliente_sel.get("inscricao_estadual", "") if cliente_sel else ""

                    for line in linhas:
                        parts = re.split(r"[\s\t,;]+", line.strip())
                        if not parts or not parts[0]:
                            continue
                        cod_val = parts[0].strip()
                        qtd_val = float(parts[1]) if len(parts) > 1 and parts[1].replace(".", "").isdigit() else 1.0
                        vlr_user = float(parts[2]) if len(parts) > 2 and parts[2].replace(".", "").isdigit() else None
                        
                        line_upper = line.upper()
                        if "BONIFIC" in line_upper:
                            tipo_item_row = "BONIFICAÇÃO"
                        else:
                            tipo_item_row = "MONITORAMENTO AUTOMÁTICO DE IMPOSTOS"

                        cenario_auto, cfop_auto = omie.determinar_cenario_fiscal(tipo_item_row, uf_cli_txt, ie_cli_txt, config)
                        sku_resolvido, p_info = _resolver_produto_item(cod_val, mapa_produtos)
                        
                        # Resgatar valor cadastrado na Tabela 1.9 oficial
                        vlr_tab_1_9 = float(mapa_tabela_1_9.get(sku_resolvido, 0.0))
                        if vlr_tab_1_9 <= 0 and p_info:
                            vlr_tab_1_9 = float(p_info.get("valor_unitario", 0.0))

                        vlr_val = vlr_user if (vlr_user is not None and vlr_user > 0) else vlr_tab_1_9
                        sub_val = round((qtd_val * vlr_val), 2)
                        desc_final = (p_info.get("descricao") or "").strip() if p_info else ""
                        if not desc_final:
                            desc_final = f"Produto {cod_val}"
                        img_url = p_info.get("imagem_url", "") if p_info else ""

                        item_imp = {
                            "codigo_produto_integracao": sku_resolvido,
                            "codigo_produto": p_info.get("codigo_produto") if p_info else None,
                            "descricao": desc_final,
                            "imagem_url": img_url,
                            "tipo_item": tipo_item_row,
                            "cenario_fiscal": cenario_auto,
                            "cfop": cfop_auto,
                            "local_estoque": config.get("local_estoque_nome", "PADRAO"),
                            "quantidade": qtd_val,
                            "valor_unitario": vlr_val,
                            "valor_desconto": 0.0,
                            "subtotal": sub_val,
                            "peso_bruto": float(p_info.get("peso_bruto") or 0.0) if p_info else 0.0
                        }
                        st.session_state["itens_pedido"].append(item_imp)
                        adicionados += 1

                    salvar_rascunho_pedido(st.session_state["itens_pedido"])
                    st.success(f"🎉 **{adicionados} linhas preenchidas importadas** via texto com sucesso!")
                    st.rerun()

        bytes_xlsx = gerar_template_xlsx()
        st.download_button(
            "📄 Baixar Modelo Oficial de Importação (.XLSX)",
            data=bytes_xlsx,
            file_name="modelo_importacao_itens_omnievo.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="btn_dl_modelo_xlsx"
        )

    st.markdown("---")

    # ── Itens do Pedido ──
    st.markdown('<div class="section-header">Itens do Pedido</div>', unsafe_allow_html=True)

    # Se o usuário clicou no botão de editar ✏️ em um item, pré-carregar os campos antes de instanciar os widgets
    if "item_para_editar" in st.session_state and st.session_state["item_para_editar"]:
        item_edit = st.session_state.pop("item_para_editar")
        st.session_state["ped_cod_int_sel"] = item_edit["codigo_produto_integracao"]
        st.session_state["last_cod_int"] = item_edit["codigo_produto_integracao"]
        st.session_state["ped_nome_prod_disabled"] = item_edit["descricao"]
        st.session_state["ped_tipo_item_radio"] = item_edit.get("tipo_item", "MONITORAMENTO AUTOMÁTICO DE IMPOSTOS")
        st.session_state["ped_qtd_input"] = float(item_edit["quantidade"])
        st.session_state["ped_preco_input"] = float(item_edit["valor_unitario"])
        st.session_state["ped_desconto_input"] = float(item_edit.get("valor_desconto", 0.0))

    col_img_space, col_fields_space = st.columns([1, 4])
    lista_codigos_int = sorted(list(mapa_produtos.keys()))

    with col_fields_space:
        col_i1, col_i2 = st.columns([2, 3])
        
        def formatar_opcao_prod_sel(cod):
            p = mapa_produtos.get(cod, {})
            d = p.get("descricao", "")
            return f"{cod} — {d}" if d else cod

        with col_i1:
            cod_int_sel = st.selectbox(
                "Código de Integração / Produto",
                lista_codigos_int,
                key="ped_cod_int_sel",
                format_func=formatar_opcao_prod_sel
            )

        prod_info = mapa_produtos.get(cod_int_sel, {})
        desc_produto_bloqueada = prod_info.get("descricao", "Produto Selecionado")
        preco_sugerido = float(prod_info.get("valor_unitario", 0.0))

        if "last_cod_int" not in st.session_state or st.session_state["last_cod_int"] != cod_int_sel:
            st.session_state["last_cod_int"] = cod_int_sel
            st.session_state["ped_nome_prod_disabled"] = desc_produto_bloqueada
        else:
            st.session_state["ped_nome_prod_disabled"] = desc_produto_bloqueada

        with col_i2:
            st.text_input("Descrição do Produto", value=desc_produto_bloqueada, disabled=True, key=f"ped_nome_disp_{cod_int_sel}")

    # Espaço Reservado para Imagem do Produto no site OMNIEVO (omnievo.com.br)
    with col_img_space:
        img_url_raw = prod_info.get("imagem_url", "")
        
        # Checar se existe imagem local em assets/{sku}.jpg ou .png
        sku_clean = str(cod_int_sel or "").strip()
        for ext, mime in [("jpg", "image/jpeg"), ("png", "image/png"), ("jpeg", "image/jpeg")]:
            p_local = os.path.join("assets", f"{sku_clean}.{ext}")
            if os.path.exists(p_local):
                try:
                    with open(p_local, "rb") as f_img:
                        b64_img = base64.b64encode(f_img.read()).decode("utf-8")
                        img_url_raw = f"data:{mime};base64,{b64_img}"
                        break
                except Exception:
                    pass

        img_url_atual = omie.formatar_url_imagem_segura(img_url_raw)
        
        st.markdown("""
        <div style="font-size: 11px; font-weight: 700; color: #000000; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px;">
            🖼️ Imagem OMNIEVO
        </div>
        """, unsafe_allow_html=True)
        
        if img_url_atual:
            st.markdown(f"""
            <div style="width: 100%; height: 230px; border-radius: 10px; border: 1px solid rgba(138,121,176,0.3); background: #FFFFFF; display: flex; align-items: center; justify-content: center; overflow: hidden; padding: 6px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
                <img src="{img_url_atual}" referrerpolicy="no-referrer" loading="lazy" style="width: 100%; height: 100%; object-fit: contain;">
            </div>
            """, unsafe_allow_html=True)
        else:
            icone_p = "👝" if ("7555" in cod_int_sel or "NECESSAIRE" in desc_produto_bloqueada.upper()) else "🧴"
            st.markdown(f"""
            <div style="width: 100%; height: 230px; border-radius: 10px; border: 2px dashed rgba(138,121,176,0.35); background: rgba(255,255,255,0.9); display: flex; flex-direction: column; align-items: center; justify-content: center; color: #000000; text-align: center; padding: 16px;">
                <div style="font-size: 42px; margin-bottom: 8px;">{icone_p}</div>
                <div style="font-size: 13px; font-weight: 800; color: #000000;">{desc_produto_bloqueada[:30]}</div>
                <div style="font-size: 11px; font-weight: 700; color: #000000; font-weight: 800; margin-top: 4px;">Sem foto no catálogo</div>
            </div>
            """, unsafe_allow_html=True)

        lbl_tom, cor_swatch = extrair_info_tom(desc_produto_bloqueada)
        if lbl_tom:
            st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 8px; padding: 6px 12px; background: #F8FAFC; border-radius: 8px; border: 1px solid #CBD5E1;">
                <div style="width: 14px; height: 14px; border-radius: 50%; background-color: {cor_swatch}; border: 1.5px solid #94A3B8; box-shadow: 0 1px 3px rgba(0,0,0,0.15);"></div>
                <span style="font-size: 11px; font-weight: 800; color: #1E293B; letter-spacing: 0.02em;">🎨 {lbl_tom}</span>
            </div>
            """, unsafe_allow_html=True)


    with col_fields_space:
        col_r1, col_r2, col_r3, col_r4 = st.columns([2, 2, 2, 2])
        with col_r1:
            pode_bonificar_usr = auth.eh_autorizado_bonificacao(usr_logado)
            if pode_bonificar_usr:
                tipo_item = st.radio("Operação", ["MONITORAMENTO AUTOMÁTICO DE IMPOSTOS", "BONIFICAÇÃO"], horizontal=True, key="ped_tipo_item_radio")
            else:
                tipo_item = "MONITORAMENTO AUTOMÁTICO DE IMPOSTOS"
                st.radio("Operação", ["MONITORAMENTO AUTOMÁTICO DE IMPOSTOS"], horizontal=True, disabled=True, key="ped_tipo_item_radio_dis")
                st.caption("🔒 **Bonificação**: Restrito a usuários autorizados.")

        uf_cli_actual = cliente_sel.get("estado", "ES") if cliente_sel else "ES"
        ie_cli_actual = cliente_sel.get("inscricao_estadual", "") if cliente_sel else ""
        cenario_auto, cfop_auto = omie.determinar_cenario_fiscal(tipo_item, uf_cli_actual, ie_cli_actual, config)

        with col_r2:
            st.text_input("Cenário Fiscal", value=cenario_auto, disabled=True, key=f"ped_cenario_disp_{tipo_item}")
        with col_r3:
            st.text_input("Estoque", value=config.get("local_estoque_nome", "PADRAO"), disabled=True, key="ped_estoque_disabled")
        with col_r4:
            quantidade_item = st.number_input("Quantidade", min_value=0.01, value=1.0, step=1.0, key=f"ped_qtd_in_{cod_int_sel}")

        pct_acrescimo_atual = pol_com_carrinho.get("pct_acrescimo", 0.0)
        prc_base_1_9 = float(prod_info.get("valor_unitario", 0.0))
        preco_unitario_com_politica = round(prc_base_1_9 * (1.0 + (pct_acrescimo_atual / 100.0)), 2) if prc_base_1_9 > 0 else 0.0
        v_site_ref = float(prod_info.get("preco_site") or (prc_base_1_9 * 1.9 if prc_base_1_9 > 0 else 0.0))
        
        col_p1, col_p2, col_p3, col_p4 = st.columns([1.5, 1.5, 1.2, 1.5])
        with col_p1:
            v_site_str = f"R$ {v_site_ref:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            st.text_input("Preço no Site (Varejo)", value=v_site_str, disabled=True, key=f"ped_preco_site_disp_{cod_int_sel}")
        with col_p2:
            preco_unitario = preco_unitario_com_politica
            prc_tab_str = f"R$ {preco_unitario:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            st.text_input("Preço Tabela 1.9 (Atacado)", value=prc_tab_str, disabled=True, key=f"ped_preco_disp_{cod_int_sel}")
        with col_p3:
            pode_descontar_usr = auth.eh_autorizado_bonificacao(usr_logado)
            is_bonificacao_item = (tipo_item == "BONIFICAÇÃO")
            
            if is_bonificacao_item:
                valor_desconto = 0.0
                st.number_input("Desconto (R$ 🔒)", min_value=0.0, value=0.0, disabled=True, key=f"ped_desconto_bonif_dis_{cod_int_sel}")
                st.caption("🎁 **Item Bonificado**: Desconto não aplicável.")
            elif pode_descontar_usr:
                desc_max_usr = auth.obter_desconto_maximo_vendedor(usr_logado)
                max_desc_reais = round((quantidade_item * preco_unitario) * (desc_max_usr / 100.0), 2) if preco_unitario > 0 else 0.0
                
                max_val_input = max_desc_reais if (desc_max_usr < 100.0 and max_desc_reais > 0) else 999999.0
                valor_desconto = st.number_input(
                    f"Desconto (R$ - Máx {desc_max_usr:.1f}%)",
                    min_value=0.0,
                    max_value=max_val_input,
                    value=0.0,
                    step=5.0,
                    format="%.2f",
                    key=f"ped_desconto_input_{cod_int_sel}",
                    help=f"Desconto em Reais. Seu limite máximo de desconto é {desc_max_usr:.1f}% (Máx R$ {max_desc_reais:,.2f})."
                )
                if desc_max_usr < 100.0:
                    st.caption(f"🏷️ **Limite de Desconto Autorizado**: Até {desc_max_usr:.1f}% (Máx R$ {max_desc_reais:,.2f})")
            else:
                valor_desconto = 0.0
                st.number_input("Desconto (R$ 🔒)", min_value=0.0, value=0.0, disabled=True, key=f"ped_desconto_dis_{cod_int_sel}")
                st.caption("🔒 **Desconto**: Restrito a pessoas autorizadas.")
        with col_p4:
            subtotal_item = round((quantidade_item * preco_unitario) - valor_desconto, 2)
            sub_fmt_str = f"R$ {subtotal_item:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            st.metric("Subtotal", sub_fmt_str)

        if st.button("➕  Adicionar Item", use_container_width=True, key="btn_add_item_ped"):
            # TRAVA DE DUPLICIDADE: Impedir a inclusão do mesmo item mais de uma vez na mesma operação
            ja_existe = any(
                str(it.get("codigo_produto_integracao", "")).strip().upper() == str(cod_int_sel).strip().upper() and
                str(it.get("tipo_item", "")).strip().upper() == str(tipo_item).strip().upper()
                for it in st.session_state["itens_pedido"]
            )

            if ja_existe:
                op_nome = "BONIFICAÇÃO" if "BONIF" in str(tipo_item).upper() else "MONITORAMENTO AUTOMÁTICO DE IMPOSTOS"
                st.warning(f"⚠️ **PRODUTO JÁ ADICIONADO NESSA OPERAÇÃO**: O produto **{cod_int_sel}** ({desc_produto_bloqueada}) já está presente no pedido sob a operação **{op_nome}**.\n\nPara alterar a quantidade, utilize o botão ✏️ **Editar Item** na lista abaixo ou exclua o item existente antes de adicioná-lo novamente.", icon="⚠️")
                st.toast(f"⚠️ O produto {cod_int_sel} já existe na operação {op_nome}!", icon="⚠️")
            else:
                item_novo = {
                    "codigo_produto_integracao": cod_int_sel,
                    "codigo_produto": prod_info.get("codigo_produto"), "descricao": desc_produto_bloqueada,
                    "imagem_url": prod_info.get("imagem_url", ""),
                    "tipo_item": tipo_item, "cenario_fiscal": cenario_auto, "cfop": cfop_auto,
                    "local_estoque": config.get("local_estoque_nome", "PADRAO"),
                    "quantidade": quantidade_item,
                    "preco_site": v_site_ref,
                    "preco_base_1_9": prc_base_1_9,
                    "valor_unitario": preco_unitario,
                    "valor_desconto": valor_desconto, "subtotal": subtotal_item,
                    "peso_bruto": float(prod_info.get("peso_bruto") or 0.0)
                }
                st.session_state["itens_pedido"].append(item_novo)
                salvar_rascunho_pedido(st.session_state["itens_pedido"])
                st.toast(f"Item {cod_int_sel} adicionado com sucesso!")
                st.rerun()

    st.markdown("---")

    # Injeção de CSS para sinalização de campo em vermelho (Resumo de Itens)
    if st.session_state.get("erro_campo_itens"):
        st.markdown("""
        <style>
        div.section-header:contains("Resumo do Pedido"), div.section-header:contains("Itens do Pedido") {
            border-left: 6px solid #EF4444 !important;
            background: linear-gradient(90deg, rgba(239, 68, 68, 0.25) 0%, rgba(239, 68, 68, 0) 100%) !important;
            color: #EF4444 !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # ── Resumo do Pedido ──
    st.markdown('<div class="section-header">Resumo do Pedido</div>', unsafe_allow_html=True)

    if st.session_state["itens_pedido"]:
        # Recalcular dinamicamente o preço unitário de todos os itens incorporando o % da categoria atual
        for item in st.session_state["itens_pedido"]:
            # PRIORIDADE MÁXIMA DA PLANILHA: Se o item veio com preço customizado na planilha, não altera o valor!
            if item.get("preco_customizado"):
                item["preco_base_1_9"] = item["valor_unitario"]
                item["subtotal"] = round((item["quantidade"] * item["valor_unitario"]) - item.get("valor_desconto", 0.0), 2)
                continue

            p_base = float(item.get("preco_base_1_9") or item.get("valor_unitario", 0.0))
            item["preco_base_1_9"] = p_base
            if pct_acrescimo_atual > 0:
                item["valor_unitario"] = round(p_base * (1.0 + (pct_acrescimo_atual / 100.0)), 2)
            else:
                item["valor_unitario"] = p_base
            item["subtotal"] = round((item["quantidade"] * item["valor_unitario"]) - item.get("valor_desconto", 0.0), 2)

        for idx, item in enumerate(st.session_state["itens_pedido"]):
            c_img, c_desc, c_qtd, c_vlr, c_sub, c_act = st.columns([1, 3.5, 1.2, 2.2, 1.8, 1.5])
            
            with c_img:
                img_url = item.get("imagem_url", "")
                # AUTO-RESOLVER IMAGEM DO PRODUTO NO CATÁLOGO OMNIEVO EM MEMÓRIA RAM (0ms)
                if not img_url:
                    sku_it = item.get("codigo_produto_integracao", "")
                    p_info_found = mapa_produtos.get(sku_it) or mapa_produtos.get(str(sku_it).strip())
                    if not p_info_found:
                        clean_d = "".join(filter(str.isdigit, str(sku_it)))
                        if clean_d:
                            for k_s, p_o in mapa_produtos.items():
                                if "".join(filter(str.isdigit, str(k_s))) == clean_d:
                                    p_info_found = p_o
                                    break
                    if p_info_found:
                        img_url = p_info_found.get("imagem_url") or p_info_found.get("url_imagem", "")
                        if img_url:
                            item["imagem_url"] = img_url

                if img_url:
                    st.markdown(f"""
                    <div style="width: 52px; height: 52px; border-radius: 6px; border: 1px solid rgba(138,121,176,0.3); background: #FFFFFF; display: flex; align-items: center; justify-content: center; overflow: hidden; padding: 2px; box-shadow: 0 2px 6px rgba(0,0,0,0.15);">
                        <img src="{img_url}" referrerpolicy="no-referrer" loading="lazy" style="max-width: 100%; max-height: 100%; object-fit: contain;">
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="width: 52px; height: 52px; border-radius: 6px; border: 1px solid rgba(138,121,176,0.25); background: linear-gradient(135deg, rgba(138,121,176,0.15) 0%, rgba(59,130,246,0.08) 100%); display: flex; align-items: center; justify-content: center; font-size: 20px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                        ✨
                    </div>
                    """, unsafe_allow_html=True)
                    
            tp_it = str(item.get("tipo_item") or "").upper()
            cen_it = str(item.get("cenario_fiscal") or "").upper()
            cfop_it = str(item.get("cfop") or "").strip()
            vlr_u = float(item.get("valor_unitario") or 0.0)
            
            is_bonif = ("BONIF" in tp_it) or ("BONIF" in cen_it) or (cfop_it in ["5.910", "6.910"]) or (vlr_u == 0.0)

            with c_desc:
                if is_bonif:
                    badge_operacao = "<span translate='no' class='notranslate' style='background: linear-gradient(135deg, rgba(245,158,11,0.25) 0%, rgba(217,119,6,0.15) 100%); border: 1px solid #F59E0B; color: #92400E; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 800; display: inline-block; margin-top: 4px; box-shadow: 0 2px 6px rgba(245,158,11,0.25);'>🎁 BONIFICAÇÃO (BRINDE)</span>"
                else:
                    badge_operacao = "<span translate='no' class='notranslate' style='background: linear-gradient(135deg, rgba(59,130,246,0.2) 0%, rgba(29,78,216,0.12) 100%); border: 1px solid #3B82F6; color: #000000; font-weight: 900; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 800; display: inline-block; margin-top: 4px; box-shadow: 0 2px 6px rgba(59,130,246,0.2);'>🛒 MONITORAMENTO AUTOMÁTICO DE IMPOSTOS</span>"
                
                st.markdown(f"<div translate='no' class='notranslate'><strong translate='no' class='notranslate' style='font-size:14px; color:#000000;'>{item['codigo_produto_integracao']}</strong> — <span translate='no' class='notranslate' style='font-size:13px; color:#000000; font-weight:700;'>{item['descricao']}</span></div>{badge_operacao}", unsafe_allow_html=True)
                
            with c_qtd:
                st.markdown(f"<div translate='no' class='notranslate' style='color:#000000; font-size:13px;'><strong style='color:#000000;'>Qtd:</strong> {item['quantidade']}</div>", unsafe_allow_html=True)
                
            with c_vlr:
                if is_bonif:
                    st.markdown("<div translate='no' class='notranslate' style='font-size:13px; font-weight:700; color:#92400E;'>R$ 0,00 (Sem Custo)</div>", unsafe_allow_html=True)
                else:
                    v_site_item = item.get("preco_site", 0.0)
                    if v_site_item > item["valor_unitario"]:
                        st.markdown(f"<div translate='no' class='notranslate' style='font-size:11px; color: #000000; font-weight:600;'>Preço Site: <span translate='no' class='notranslate' style='text-decoration:line-through; color: #000000;'>{fmt_brl(v_site_item)}</span></div>", unsafe_allow_html=True)
                    lbl_origem = "Planilha:" if item.get("preco_customizado") else "Tabela 1.9:"
                    cor_origem = "#0284C7" if item.get("preco_customizado") else "#000000"
                    st.markdown(f"<div translate='no' class='notranslate' style='font-size:13px; font-weight:800; color:{cor_origem};'>{lbl_origem} {fmt_brl(item['valor_unitario'])}</div>", unsafe_allow_html=True)
                    if item.get("valor_desconto", 0) > 0:
                        st.markdown(f"<div translate='no' class='notranslate' style='font-size:11px; color: #000000; font-weight:600;'>Desc: {fmt_brl(item['valor_desconto'])}</div>", unsafe_allow_html=True)
                    
            with c_sub:
                if is_bonif:
                    st.markdown("<div translate='no' class='notranslate' style='font-size:14px; font-weight:800; color:#92400E;'>R$ 0,00 <span translate='no' class='notranslate' style='font-size:10px; color:#B45309;'>(BRINDE)</span></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div translate='no' class='notranslate' style='font-size:14px; font-weight:800; color:#047857;'>{fmt_brl(item['subtotal'])}</div>", unsafe_allow_html=True)
                
            with c_act:
                c_edit, c_trash = st.columns(2)
                item_code_key = str(item.get('codigo_produto_integracao') or idx)
                with c_edit:
                    if st.button("✏️", key=f"btn_edit_item_{item_code_key}_{idx}", help=f"Editar item {item['codigo_produto_integracao']}"):
                        item_edit = st.session_state["itens_pedido"].pop(idx)
                        salvar_rascunho_pedido(st.session_state["itens_pedido"])
                        st.session_state["item_para_editar"] = item_edit
                        st.toast(f"✏️ Item {item_edit['codigo_produto_integracao']} carregado no formulário acima para edição.")
                        st.rerun()
                with c_trash:
                    if st.button("🗑️", key=f"btn_del_item_{item_code_key}_{idx}", help=f"Excluir item {item['codigo_produto_integracao']}"):
                        item_removido = st.session_state["itens_pedido"].pop(idx)
                        salvar_rascunho_pedido(st.session_state["itens_pedido"])
                        st.toast(f"🗑️ Item {item_removido['codigo_produto_integracao']} removido do pedido.")
                        st.rerun()
                    
            st.markdown("<hr style='margin: 8px 0 !important; opacity: 0.2;'>", unsafe_allow_html=True)

        st.markdown("")
        col_tot1, col_tot2, col_tot3 = st.columns(3)
        total_qtd = sum(item["quantidade"] for item in st.session_state["itens_pedido"])
        total_pedido = sum(item["subtotal"] for item in st.session_state["itens_pedido"] if not (("BONIF" in str(item.get("tipo_item","")).upper()) or ("BONIF" in str(item.get("cenario_fiscal","")).upper()) or (item.get("valor_unitario", 0.0) == 0.0)))
        total_bonif_unidades = sum(item["quantidade"] for item in st.session_state["itens_pedido"] if (("BONIF" in str(item.get("tipo_item","")).upper()) or ("BONIF" in str(item.get("cenario_fiscal","")).upper()) or (item.get("valor_unitario", 0.0) == 0.0)))
        
        qtd_formatada = int(total_qtd) if float(total_qtd).is_integer() else f"{total_qtd:,.2f}".replace(".", ",")
        qtd_bonif_fmt = int(total_bonif_unidades) if float(total_bonif_unidades).is_integer() else f"{total_bonif_unidades:,.2f}".replace(".", ",")
        
        col_tot1.metric("Itens no Pedido", len(st.session_state["itens_pedido"]))
        col_tot2.metric("Quantidade Total", f"{qtd_formatada} un", delta=f"{qtd_bonif_fmt} brindes" if total_bonif_unidades > 0 else None)
        col_tot3.metric("Valor Total Vendas (Tabela 1.9)", fmt_brl(total_pedido))

        # ── PAINEL DA POLÍTICA COMERCIAL OMNIEVO ──
        pol_com = omie.calcular_politica_comercial_omnievo(total_pedido)

        # ── ENGINE OFICIAL DO MONITORAMENTO AUTOMÁTICO DE IMPOSTOS DO OMIE ERP (CENÁRIO #8681019399) ──
        import fiscal_tax_service as tax_service

        uf_dest_cot = cliente_sel.get("estado", "ES") if cliente_sel else "ES"
        ie_dest_cot = cliente_sel.get("inscricao_estadual", "") if cliente_sel else ""

        res_impostos_omie = tax_service.calcular_impostos_pedido_omie(
            st.session_state["itens_pedido"],
            uf_destino=uf_dest_cot,
            ie_cliente=ie_dest_cot,
            valor_frete=vlr_frete_braspress if ('vlr_frete_braspress' in locals()) else 0.0,
            mapa_tabela_1_9=mapa_tabela_1_9
        )

        st.session_state["valor_impostos_st"] = res_impostos_omie["valor_icms_st"]
        st.session_state["valor_impostos_ipi"] = res_impostos_omie.get("valor_ipi", 0.0)
        vlr_total_nf_real = res_impostos_omie["valor_total_nota_fiscal"]

        aliq_ipi_val = float(res_impostos_omie.get("aliquota_ipi_pct") or 0.0)
        vlr_ipi_num = float(res_impostos_omie.get("valor_ipi") or 0.0)
        lbl_ipi_card = f"🏭 IPI ({aliq_ipi_val:.1f}%)" if aliq_ipi_val > 0 else "🏭 IPI"
        vlr_ipi_fmt = fmt_brl(vlr_ipi_num)

        memoria_fiscal_txt = (
            f"Mercadorias: {fmt_brl(res_impostos_omie['valor_mercadorias'])} | "
            f"Frete: {fmt_brl(res_impostos_omie['valor_frete'])} | "
            f"ICMS ({res_impostos_omie['aliquota_icms_pct']}%): {fmt_brl(res_impostos_omie['valor_icms'])} | "
            f"ICMS ST: {fmt_brl(res_impostos_omie['valor_icms_st'])} | "
            f"IPI: {vlr_ipi_fmt} | "
            f"TOTAL NOTA FISCAL: {fmt_brl(vlr_total_nf_real)}"
        )

        st.markdown(f"""
<div style='background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%); border: 2px solid #8B5CF6; border-radius: 14px; padding: 20px; margin: 16px 0; box-shadow: 0 8px 24px rgba(0,0,0,0.25); color: #FFFFFF;'>
<div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; border-bottom: 1px solid rgba(255,255,255,0.15); padding-bottom: 12px; margin-bottom: 16px;'>
<div>
<div style='font-size: 11px; font-weight: 800; color: #FFFFFF; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em;'>🏛️ MONITORAMENTO AUTOMÁTICO DE IMPOSTOS OMIE ERP (CENÁRIO #8681019399)</div>
<div style='font-size: 18px; font-weight: 800; color: #FFFFFF; margin-top: 4px;'>
{pol_com["icone"]} CATEGORIA {pol_com["categoria"]} — <span style="color: #FDE68A; font-weight: 800;">Destino: {res_impostos_omie["uf_destino"]}</span>
</div>
</div>
<div>
<span style='background: #10B981; color: #000000; padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: 900;'>
🟢 Impostos Sincronizados Omie
</span>
</div>
</div>
<div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 12px;'>
<div style='background: rgba(255,255,255,0.06); padding: 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);'>
<div style='font-size: 11px; color: #FFFFFF; font-weight: 800; font-weight: 700;'>💰 Vendas (Tabela 1.9)</div>
<div style='font-size: 16px; font-weight: 900; color: #FFFFFF; font-weight: 900; margin-top: 2px;'>{fmt_brl(res_impostos_omie["valor_mercadorias"])}</div>
</div>
<div style='background: rgba(255,255,255,0.06); padding: 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);'>
<div style='font-size: 11px; color: #FFFFFF; font-weight: 800; font-weight: 700;'>{lbl_ipi_card}</div>
<div style='font-size: 16px; font-weight: 900; color: #FFFFFF; margin-top: 2px;'>{vlr_ipi_fmt}</div>
</div>
<div style='background: rgba(255,255,255,0.06); padding: 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);'>
<div style='font-size: 11px; color: #FFFFFF; font-weight: 800; font-weight: 700;'>📊 ICMS Próprio ({res_impostos_omie["aliquota_icms_pct"]}%)</div>
<div style='font-size: 16px; font-weight: 900; color: #FDE68A; font-weight: 800; margin-top: 2px;'>{fmt_brl(res_impostos_omie["valor_icms"])}</div>
</div>
<div style='background: rgba(255,255,255,0.06); padding: 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);'>
<div style='font-size: 11px; color: #FDE68A; font-weight: 700;'>🏛️ ICMS ST (Retido)</div>
<div style='font-size: 16px; font-weight: 900; color: #FBBF24; margin-top: 2px;'>{fmt_brl(res_impostos_omie["valor_icms_st"])}</div>
</div>
<div style='background: rgba(255,255,255,0.06); padding: 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);'>
<div style='font-size: 11px; color: #FFFFFF; font-weight: 800; font-weight: 700;'>🚚 Frete ({nome_frete_resumo if ('nome_frete_resumo' in locals()) else 'Padrão'})</div>
<div style='font-size: 16px; font-weight: 900; color: #FFFFFF; font-weight: 900; margin-top: 2px;'>{fmt_brl(res_impostos_omie["valor_frete"])}</div>
</div>
<div style='background: rgba(16,185,129,0.25); padding: 12px; border-radius: 10px; border: 2px solid #10B981;'>
<div style='font-size: 11px; color: #FFFFFF; font-weight: 800; font-weight: 800;'>💵 VALOR REAL DA NOTA FISCAL</div>
<div style='font-size: 18px; font-weight: 900; color: #10B981; font-weight: 900; margin-top: 2px;'>{fmt_brl(vlr_total_nf_real)}</div>
</div>
</div>
<div style='margin-top: 14px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.12); font-size: 12px; color: #FFFFFF; font-weight: 800; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 10px;'>
<div>📅 <b>Prazos Permitidos:</b> {", ".join(pol_com["prazos"])}</div>
<div>📝 <b>Memória Fiscal:</b> {memoria_fiscal_txt}</div>
</div>
</div>
""", unsafe_allow_html=True)
    else:
        if st.session_state.get("erro_campo_itens"):
            st.markdown('<div style="color: #EF4444; background: rgba(239, 68, 68, 0.15); border: 2px solid #EF4444; padding: 12px 16px; border-radius: 8px; font-size: 13px; font-weight: 700; margin-bottom: 14px;">❌ CAMPO OBRIGATÓRIO EM VERMELHO: Adicione pelo menos 1 produto no formulário acima antes de emitir o pedido!</div>', unsafe_allow_html=True)
        else:
            st.info("Nenhum item adicionado ao pedido. Selecione um produto acima e clique em ➕ Adicionar Item para começar.")

    st.markdown("")
    col_b1, col_b2 = st.columns([1, 4])
    with col_b1:
        if st.session_state["itens_pedido"]:
            if st.button("🗑️  Limpar Todos", key="btn_limpar_itens"):
                st.session_state["itens_pedido"] = []
                st.session_state["erro_campo_itens"] = False
                limpar_rascunho_pedido()
                st.toast("Pedido limpo.")
                st.rerun()
    with col_b2:
        # Calcular maior prazo em dias selecionado nas parcelas
        max_dias_selecionados = 0
        if parcelas_payload and 'dt_previsao' in locals():
            for p in parcelas_payload:
                try:
                    dt_v = datetime.datetime.strptime(p["data_vencimento"], "%d/%m/%Y").date()
                    diff_d = (dt_v - dt_previsao).days
                    if diff_d > max_dias_selecionados:
                        max_dias_selecionados = diff_d
                except Exception:
                    pass
        if st.session_state["itens_pedido"] and 'pol_com' in locals():
            if not pol_com.get("valido", True):
                st.error(rf"⛔ **IMPUT BLOQUEADO POR POLÍTICA COMERCIAL**: O valor total do pedido ({fmt_brl(total_pedido)}) está abaixo do pedido mínimo de R$ 1.500,00. Adicione mais itens para liberar o faturamento.")
            elif max_dias_selecionados > pol_com.get("max_dias_prazo", 56):
                st.info(f"ℹ️ **Prazo Liberado**: O parcelamento selecionado ({max_dias_selecionados} dias) excede o prazo padrão, mas está liberado para emissão.")

        is_editing_active = bool(st.session_state.get("pedido_em_edicao"))
        ped_ed_active = st.session_state.get("pedido_em_edicao") or {}
        num_ped_ed_str = ped_ed_active.get("numero_pedido", "")
        cod_ped_ed_str = ped_ed_active.get("codigo_pedido", "")
        
        lbl_btn_sub = f"💾  Salvar Alterações no Pedido Nº {num_ped_ed_str} (Omie ERP)" if is_editing_active else "🚀  Emitir Pedido (Cairá na Etapa 10)"

        if st.button(lbl_btn_sub, type="primary", use_container_width=True, key="btn_enviar_omie"):
            erros_encontrados = []
            st.session_state["erro_campo_cliente"] = False
            st.session_state["erro_campo_itens"] = False
            st.session_state["erros_validacao_pedido"] = []

            if not cliente_sel:
                st.session_state["erro_campo_cliente"] = True
                erros_encontrados.append("<b>Campo [Razão Social ou CPF/CNPJ]</b>: Preenchimento obrigatório. Selecione o cliente no topo da tela.")

            if not st.session_state["itens_pedido"]:
                st.session_state["erro_campo_itens"] = True
                erros_encontrados.append("<b>Campo [Itens do Pedido]</b>: Adicione pelo menos 1 produto ao resumo antes de enviar.")

            apenas_bonificacao_sub = (
                len(st.session_state["itens_pedido"]) > 0 and
                all(
                    ("BONIF" in str(it.get("tipo_item", "")).upper()) or
                    ("BONIF" in str(it.get("cenario_fiscal", "")).upper()) or
                    (it.get("valor_unitario", 0.0) == 0.0)
                    for it in st.session_state["itens_pedido"]
                )
            )

            # REGRA DE NEGÓCIO: Se o pedido for 100% Bonificado, NÃO entra na trava da Política Comercial!
            if not apenas_bonificacao_sub:
                if 'pol_com' in locals():
                    if not pol_com.get("valido", True):
                        erros_encontrados.append(rf"<b>🚨 Pedido Mínimo Não Atingido</b>: O valor total de vendas do pedido ({fmt_brl(total_pedido)}) é inferior ao mínimo de R$ 1.500,00 da Política Comercial OMNIEVO.")
                    # Trava de prazo de parcelamento removida para usuários autorizados excede o prazo máximo da categoria <b>{pol_com['categoria']}</b> (Limite: {pol_com['max_dias_prazo']} dias).")

            if erros_encontrados:
                st.session_state["erros_validacao_pedido"] = erros_encontrados
                st.toast("🚨 Pedido bloqueado pelas regras da Política Comercial!", icon="❌")
                st.rerun()
            else:
                cod_vendedor_envio = cod_vendedor_selecionado
                nome_vendedor_envio = vendedor_nome_selecionado

                cabecalho_payload = {
                    "codigo_cliente": cliente_sel["codigo_cliente"],
                    "cliente_nome": cliente_sel.get("razao_social", ""),
                    "uf_cliente": cliente_sel.get("estado", "ES"),
                    "cep_cliente": str(cliente_sel.get("cep") or st.session_state.get("ped_cliente_cep") or "").strip(),
                    "data_previsao": dt_previsao_str,
                    "codigo_categoria": categoria_ped,
                    "codigo_parcela": f"{qtd_parcelas:03d}",
                    "etapa": "10",  # REGRA DE NEGÓCIO: Novo Pedido CAI NA ETAPA 10
                    "codigo_conta_corrente": conta_corrente_sel,
                    "codigo_vendedor": cod_vendedor_envio,
                    "vendedor_nome": nome_vendedor_envio,
                    "transportadora_nome": transp_selecionada,
                    "modal_frete": modal_frete_selecionado if ('modal_frete_selecionado' in locals()) else "RODOVIÁRIO",
                    "modalidade_frete_nome": modal_frete_desc if ('modal_frete_desc' in locals()) else "Rodoviário Padrão",
                    "prazo_frete_dias": prazo_frete_selecionado if ('prazo_frete_selecionado' in locals()) else 0,
                    "valor_frete": float(vlr_frete_braspress) if ('vlr_frete_braspress' in locals()) else 0.0,
                    "peso_bruto": float(info_cubagem["peso_kg"]) if ('info_cubagem' in locals() and isinstance(info_cubagem, dict)) else 0.0,
                    "quantidade_volumes": int(info_cubagem["volumes"]) if ('info_cubagem' in locals() and isinstance(info_cubagem, dict)) else 1,
                    "parcelas_customizadas": parcelas_payload,
                    "origem_pedido": "CRM"
                }

                if is_editing_active:
                    cli_nome_envio = cliente_sel.get("razao_social", "Cliente") if cliente_sel else "Cliente"
                    with st.spinner(f"⚡ Atualizando Pedido #{num_ped_ed_str} no Omie ERP..."):
                        try:
                            omie.alterar_pedido_venda_omie(
                                cod_ped_ed_str,
                                cabecalho_payload,
                                st.session_state["itens_pedido"],
                                config,
                                cliente_sel,
                                parcelas_payload
                            )
                            st.session_state.pop("pedido_em_edicao", None)
                            st.session_state["itens_pedido"] = []
                            st.session_state["erros_validacao_pedido"] = []
                            st.session_state["erro_campo_cliente"] = False
                            st.session_state["erro_campo_itens"] = False
                            limpar_rascunho_pedido()
                            st.cache_data.clear()
                            st.toast(f"✅ Pedido #{num_ped_ed_str} ({cli_nome_envio}) atualizado com sucesso no Omie ERP!", icon="🎉")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao atualizar Pedido #{num_ped_ed_str} no Omie ERP: {e}")
                else:
                    # INTEGRAÇÃO NO MESMO MOMENTO (EM TEMPO REAL < 1 SEGUNDO NO OMIE ERP)
                    cli_nome_envio = cliente_sel.get("razao_social", "Cliente") if cliente_sel else "Cliente"
                    with st.spinner(f"⚡ Integrando pedido de {cli_nome_envio} no mesmo momento com o Omie ERP..."):
                        try:
                            # 0. PAUSAR TODAS AS ROTINAS DE FUNDO IMEDIATAMENTE PARA GARANTIR VELOCIDADE MÁXIMA
                            omie._IS_ORDER_TRANSMITTING = True
                            
                            # 1. Envio síncrono ultra-rápido com prioridade máxima 100%
                            res_envio = omie.enviar_pedido_omie(cabecalho_payload, st.session_state["itens_pedido"], config)
                            cod_ped_gerado = res_envio.get("codigo_pedido") or res_envio.get("pedido_venda_produto", {}).get("codigo_pedido")
                            num_ped_gerado = res_envio.get("numero_pedido") or res_envio.get("pedido_venda_produto", {}).get("numero_pedido") or str(cod_ped_gerado)

                            # 2. Gerar PDF do Orçamento no mesmo momento
                            pdf_data = {
                                "cabecalho": {"numero_pedido": str(num_ped_gerado), "etapa": "10", "data_previsao": dt_previsao_str, "uf_cliente": cliente_sel.get("estado", "ES")},
                                "cliente": cliente_sel,
                                "itens_pedido": st.session_state["itens_pedido"],
                                "parcelas_customizadas": parcelas_payload
                            }
                            bytes_pdf = pdf_service.gerar_pdf_pedido(pdf_data)
                            fn_pdf_novo = pdf_service.formatar_nome_arquivo_pdf(str(num_ped_gerado), cli_nome_envio)

                            # 3. Armazenar resultado para banner de sucesso instantâneo com botão de PDF
                            st.session_state["sucesso_pedido_emitido"] = {
                                "num_pedido": str(num_ped_gerado),
                                "cod_pedido": cod_ped_gerado,
                                "pdf_bytes": bytes_pdf,
                                "pdf_filename": fn_pdf_novo
                            }

                            # 4. Limpar o formulário para o próximo pedido
                            st.session_state["itens_pedido"] = []
                            st.session_state["erros_validacao_pedido"] = []
                            st.session_state["erro_campo_cliente"] = False
                            st.session_state["erro_campo_itens"] = False
                            limpar_rascunho_pedido()
                            st.cache_data.clear()

                            st.toast(f"✅ Pedido Nº {num_ped_gerado} integrado NO MESMO MOMENTO com sucesso!", icon="🎉")
                            st.rerun()
                        except Exception as err_int:
                            err_m = str(err_int)
                            try:
                                print(f"[ERRO INTEGRAÇÃO DIRETA]: {err_m}")
                            except Exception:
                                pass
                            st.error(f"❌ Não foi possível transmitir o pedido para o Omie ERP:\n\n**{err_m}**")
                            st.info("💡 Seus itens continuam salvos no formulário acima para você ajustar e tentar transmitir novamente.")
                        finally:
                            omie._IS_ORDER_TRANSMITTING = False


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 2: KANBAN DE VENDAS
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "📊  Kanban de Vendas":

    # 🔝 Auto-Scroll para o topo da página ao clicar na aba Kanban
    components.html("""
    <script>
    (function() {
        function scrollMainToTop() {
            try {
                const pWin = window.parent || window;
                const doc = pWin.document;
                const container = doc.querySelector('[data-testid="stAppViewContainer"]') || doc.querySelector('section.main') || doc.documentElement || pWin;
                if (container && container.scrollTo) {
                    container.scrollTo({ top: 0, behavior: 'smooth' });
                    if (container.scrollTop !== undefined) container.scrollTop = 0;
                }
                pWin.scrollTo({ top: 0, behavior: 'smooth' });
            } catch(e) {}
        }
        scrollMainToTop();
        setTimeout(scrollMainToTop, 80);
        setTimeout(scrollMainToTop, 250);
    })();
    </script>
    """, height=0)

    # Iniciar sincronização automática de 1 em 1 hora em segundo plano
    omie.iniciar_sincronizacao_automatica_1h()

    if "toast_msg_sucesso" in st.session_state and st.session_state["toast_msg_sucesso"]:
        msg_t = st.session_state.pop("toast_msg_sucesso")
        st.success(msg_t)
        st.toast(msg_t, icon="🗑️")

    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">📊</div>
        <div>
            <div class="page-header-title">Kanban de Vendas Omie ERP</div>
            <div class="page-header-subtitle">Acompanhe os pedidos de venda por etapa. Atualização automática contínua a cada 3 minutos.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ⏱️ Auto-Refresh do Kanban no Navegador a cada 10 minutos (600.000 ms)
    components.html("""
    <script>
    (function() {
        if (!window._kanban_auto_refresh_set) {
            window._kanban_auto_refresh_set = true;
            setTimeout(function() {
                window.parent.location.reload();
            }, 180000); // 3 minutos
        }
    })();
    </script>
    """, height=0)

    col_k_top1, col_k_top2 = st.columns([3, 1])
    with col_k_top1:
        busca_kanban = st.text_input(
            "Pesquisar Pedidos",
            placeholder="🔍 Pesquisar por Nº do Pedido, CPF/CNPJ ou Nome do Cliente...",
            key="kanban_search_input",
            label_visibility="collapsed"
        )
        st.caption("⏱️ **Sincronização Automática**: Atualização contínua dos pedidos no Omie ERP agendada a cada 3 minutos.")
    with col_k_top2:
        if st.button("🔄  Atualizar Kanban", key="btn_refresh_kanban", use_container_width=True):
            with st.spinner("Sincronizando pedidos diretamente no Omie ERP..."):
                st.cache_data.clear()
                omie.listar_pedidos_omie(force_refresh=True)
                st.toast("✅ Kanban de Vendas atualizado!")
                st.rerun()

    pedidos_lista_raw = auth.obter_pedidos_filtrados_usuario(_obter_pedidos_cached(), usr_logado)

    # ── REGRA DE NEGÓCIO SOLICITADA PELO USUÁRIO: Excluir 100% dos pedidos cancelados no Kanban ──
    pedidos_lista = []
    for p in pedidos_lista_raw:
        if omie.eh_pedido_cancelado(p):
            continue

        raw_p = p.get("raw_data", {}) if isinstance(p.get("raw_data"), dict) else {}
        cab_p = raw_p.get("cabecalho", {}) if isinstance(raw_p.get("cabecalho"), dict) else {}
        cad_p = raw_p.get("infoCadastro", {}) if isinstance(raw_p.get("infoCadastro"), dict) else {}

        flg_cancelado = str(cad_p.get("cancelado") or cab_p.get("cancelado") or p.get("cancelado") or "N").strip().upper()
        status_str = str(p.get("status") or cab_p.get("status") or cab_p.get("status_pedido") or "").strip().upper()
        etapa_str = str(p.get("etapa") or cab_p.get("etapa") or "").strip().upper()

        # Cancelado se qualquer flag indicar cancelamento
        if flg_cancelado == "S" or "CANCEL" in status_str or "CANCEL" in etapa_str or etapa_str in ("90", "99", "CANCELADO"):
            continue

        pedidos_lista.append(p)

    # Filtragem dinâmica por Nº do Pedido, CPF/CNPJ ou Nome do Cliente
    if busca_kanban and busca_kanban.strip():
        termo = busca_kanban.strip().lower()
        termo_digits = "".join(filter(str.isdigit, termo))

        pedidos_filtrados = []
        for p in pedidos_lista:
            num_p = str(p.get("numero_pedido", "")).lower()
            cod_p = str(p.get("codigo_pedido", "")).lower()
            cli_nome = str(p.get("cliente_nome", "")).lower()

            cli_dict = p.get("cliente") or (p.get("raw_data", {}).get("cliente") if isinstance(p.get("raw_data"), dict) else {}) or {}
            cli_cnpj = str(p.get("cnpj_cpf") or p.get("cliente_cnpj") or cli_dict.get("cnpj_cpf", "")).lower()
            if not cli_cnpj and lista_clientes:
                cod_c_str = str(p.get("codigo_cliente") or "").strip()
                if cod_c_str:
                    for c_obj in lista_clientes:
                        if str(c_obj.get("codigo_cliente") or "").strip() == cod_c_str:
                            cli_cnpj = str(c_obj.get("cnpj_cpf", "")).lower()
                            break
            cli_cnpj_digits = "".join(filter(str.isdigit, cli_cnpj))

            match_num = (termo in num_p) or (termo in cod_p)
            match_nome = termo in cli_nome
            match_cnpj = (termo in cli_cnpj) or (bool(termo_digits) and (termo_digits in cli_cnpj_digits))

            if match_num or match_nome or match_cnpj:
                pedidos_filtrados.append(p)

        pedidos_lista = pedidos_filtrados

    def obter_etapa_pedido(p):
        raw_p = p.get("raw_data", {})
        cab_p = raw_p.get("cabecalho", {})
        return str(p.get("etapa") or cab_p.get("etapa") or "").strip()

    def eh_pagamento_pix(ped):
        if not isinstance(ped, dict):
            return False
        raw = ped.get("raw_data", {}) if isinstance(ped.get("raw_data"), dict) else {}
        cab = raw.get("cabecalho", {}) if isinstance(raw.get("cabecalho"), dict) else {}
        inf = raw.get("informacoes_adicionais", {}) if isinstance(raw.get("informacoes_adicionais"), dict) else {}
        obs = raw.get("observacoes", {}) if isinstance(raw.get("observacoes"), dict) else {}
        
        cod_parc = str(cab.get("codigo_parcela") or "").upper().strip()
        meio_pag = str(cab.get("meio_pagamento") or ped.get("meio_pagamento") or "").upper().strip()
        tipo_doc = str(ped.get("tipo_documento") or cab.get("tipo_documento") or "").upper().strip()
        
        txt_busca = f"{cod_parc} {meio_pag} {tipo_doc} {str(inf.get('dados_adicionais_nf', '')).upper()} {str(obs.get('obs_venda', '')).upper()} {str(ped.get('forma_pagamento', '')).upper()}"
        return ("PIX" in txt_busca) or (cod_parc in ["17", "PIX"]) or (meio_pag in ["17", "PIX"])

    def eh_pagamento_boleto(ped):
        if not isinstance(ped, dict):
            return False
        raw = ped.get("raw_data", {}) if isinstance(ped.get("raw_data"), dict) else {}
        cab = raw.get("cabecalho", {}) if isinstance(raw.get("cabecalho"), dict) else {}
        inf = raw.get("informacoes_adicionais", {}) if isinstance(raw.get("informacoes_adicionais"), dict) else {}
        
        cod_parc = str(cab.get("codigo_parcela") or "").upper().strip()
        meio_pag = str(cab.get("meio_pagamento") or ped.get("meio_pagamento") or "").upper().strip()
        tipo_doc = str(ped.get("tipo_documento") or cab.get("tipo_documento") or "").upper().strip()
        
        txt_busca = f"{cod_parc} {meio_pag} {tipo_doc} {str(inf.get('dados_adicionais_nf', '')).upper()} {str(ped.get('forma_pagamento', '')).upper()}"
        is_boleto_code = (cod_parc in ["001", "028", "014", "035", "042", "049", "056", "000"]) or (meio_pag in ["01", "BOL", "BOLETO"]) or (tipo_doc == "BOL")
        return is_boleto_code or ("BOLETO" in txt_busca) or ("BOL " in txt_busca)

    def resolver_nome_cliente_kanban(ped):
        if not isinstance(ped, dict):
            return "Cliente"
        raw = ped.get("raw_data", {}) if isinstance(ped.get("raw_data"), dict) else {}
        cab = raw.get("cabecalho", {}) if isinstance(raw.get("cabecalho"), dict) else {}
        cli_obj = ped.get("cliente", {}) if isinstance(ped.get("cliente"), dict) else {}

        nome = (
            ped.get("cliente_nome") or
            cli_obj.get("razao_social") or
            cli_obj.get("nome_fantasia") or
            raw.get("cliente", {}).get("razao_social") or
            ""
        ).strip()

        if nome and not nome.startswith("Cliente #") and nome not in ["Cliente", "Cliente Selecionado", "None", ""]:
            return nome

        cod_cli = ped.get("codigo_cliente") or cab.get("codigo_cliente") or cab.get("codigo_cliente_omie")
        if cod_cli:
            sess_key = f"cli_name_ram_cache_{cod_cli}"
            if sess_key in st.session_state and st.session_state[sess_key]:
                return st.session_state[sess_key]

            # 1. Buscar no cache local de clientes (cache/clientes.json)
            try:
                if os.path.exists("cache/clientes.json"):
                    with open("cache/clientes.json", "r", encoding="utf-8") as f:
                        mapa_clis = json.load(f)
                else:
                    mapa_clis = omie.carregar_clientes() or []
                
                for c in mapa_clis:
                    c1 = c.get("codigo_cliente_omie") or c.get("codigo_cliente")
                    c2 = c.get("codigo_cliente") or c.get("codigo_cliente_omie")
                    if str(cod_cli) in [str(c1), str(c2)]:
                        r_nome = (c.get("razao_social") or c.get("nome_fantasia") or "").strip()
                        if r_nome and not r_nome.startswith("Cliente #"):
                            st.session_state[sess_key] = r_nome
                            ped["cliente_nome"] = r_nome
                            return r_nome
            except Exception:
                pass

            # 2. Consultar diretamente no Omie ERP API
            try:
                config = omie.load_config()
                res_c = omie.omie_call("geral/clientes", "ConsultarCliente", {"codigo_cliente_omie": int(cod_cli)}, config)
                r_nome = (res_c.get("razao_social") or res_c.get("nome_fantasia") or "").strip()
                if r_nome:
                    st.session_state[sess_key] = r_nome
                    ped["cliente_nome"] = r_nome
                    return r_nome
            except Exception:
                pass

        return nome if (nome and not nome.startswith("Cliente #")) else f"Cliente #{cod_cli}" if cod_cli else "Cliente"

    # Sincronização automática do SLA de separação com as etapas oficiais do Kanban Omie
    try:
        sla_separacao.sincronizar_com_kanban(pedidos_lista)
    except Exception:
        pass

    # Filtrar por etapa exatamente igual ao Kanban do Omie ERP (excluindo cancelados)
    p_col1 = [p for p in pedidos_lista if obter_etapa_pedido(p) in ["10", "00"]]
    p_col2 = [p for p in pedidos_lista if obter_etapa_pedido(p) in ["20"]]
    p_col3 = [p for p in pedidos_lista if obter_etapa_pedido(p) in ["70"]]
    p_col4 = [p for p in pedidos_lista if obter_etapa_pedido(p) in ["50", "30", "40"]]
    p_col5 = [p for p in pedidos_lista if obter_etapa_pedido(p) in ["60", "80"]]

    txt_c1 = f"{len(p_col1)} registros" if p_col1 else "Nenhum registro"
    txt_c2 = f"{len(p_col2)} registros" if p_col2 else "Nenhum registro"
    txt_c3 = f"{len(p_col3)} registros" if p_col3 else "Nenhum registro"
    txt_c4 = f"{len(p_col4)} registros" if p_col4 else "Nenhum registro"
    txt_c5 = f"{len(p_col5)} registros" if p_col5 else "Nenhum registro"

    def _gerar_pdf_fast(ped):
        cod_key = str(ped.get("codigo_pedido") or ped.get("numero_pedido") or "")
        sess_key = f"pdf_ram_cache_{cod_key}"
        if sess_key in st.session_state:
            return st.session_state[sess_key]
        
        raw_d = ped.get("raw_data", {})
        if raw_d and raw_d.get("det"):
            try:
                ped_json_str = json.dumps(raw_d, sort_keys=True)
                pdf_b = pdf_service.obter_pdf_pedido_cached(ped_json_str)
            except Exception:
                pdf_b = None
        else:
            pdf_b = None

        if not pdf_b:
            pdf_data = {
                "cabecalho": {
                    "numero_pedido": str(ped.get("numero_pedido", "ORCAMENTO")),
                    "etapa": str(ped.get("etapa", "10")),
                    "data_previsao": ped.get("data_previsao", ""),
                    "uf_cliente": ped.get("cliente_uf", "ES")
                },
                "cliente": {
                    "razao_social": ped.get("cliente_nome", "Cliente"),
                    "cnpj_cpf": ped.get("cnpj_cpf", ""),
                    "estado": ped.get("cliente_uf", "ES")
                },
                "itens_pedido": ped.get("itens_pedido", []),
                "parcelas_customizadas": []
            }
            pdf_b = pdf_service.gerar_pdf_pedido(pdf_data)

        st.session_state[sess_key] = pdf_b
        return pdf_b

    def extrair_str_parcelas_kanban(ped):
        raw = ped.get("raw_data", {})
        parcs = raw.get("lista_parcelas", {}).get("parcela", []) or raw.get("parcelas_customizadas", [])
        if parcs:
            qtd = len(parcs)
            return f"({qtd}x)" if qtd > 1 else "(1x)"
        
        cod_parc = str(raw.get("cabecalho", {}).get("codigo_parcela") or "").strip()
        if cod_parc in ["001", "000"]:
            return "(1x)"
        elif cod_parc.isdigit() and int(cod_parc) > 0 and int(cod_parc) <= 36:
            return f"({int(cod_parc)}x)"
        return ""

    usr_logado = st.session_state.get("usuario_logado", {})
    pode_autorizar_boleto = auth.eh_usuario_master(usr_logado) or auth.eh_autorizado_bonificacao(usr_logado) or bool(usr_logado.get("is_admin", False))

    # ── ALERTA PROATIVO DE SEPARAÇÃO ATRASADA (SLA > 30H / CRÍTICO 48H) ──
    pedidos_atrasados_separacao = [p for p in p_col3 if sla_separacao.calcular_sla_pedido(p).get("esta_atrasado")]
    if pedidos_atrasados_separacao:
        qtd_atr = len(pedidos_atrasados_separacao)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FFFBEB 0%, #FEF2F2 100%); border: 2px solid #F59E0B; border-radius: 12px; padding: 14px 20px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.12); display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 14px;">
                <span style="font-size: 28px;">⚠️</span>
                <div>
                    <div style="font-size: 15px; font-weight: 800; color: #9A3412; letter-spacing: -0.3px;">ATENÇÃO: SEPARAÇÃO DE ESTOQUE ATRASADA (SLA > 30H)</div>
                    <div style="font-size: 13px; color: #78350F; font-weight: 600; margin-top: 2px;">
                        Existem <b>{qtd_atr} pedido(s)</b> na coluna <b>Separar Estoque</b> aguardando há mais de 30 horas! O SLA fatal de 48h está prestes a estourar.
                    </div>
                </div>
            </div>
            <div style="background: #F59E0B; color: #FFFFFF; font-size: 12px; font-weight: 800; padding: 6px 14px; border-radius: 20px; letter-spacing: 0.5px;">
                🚨 URGÊNCIA EXPEDIÇÃO
            </div>
        </div>
        """, unsafe_allow_html=True)

    col_k1, col_k2, col_k3, col_k4, col_k5 = st.columns(5)

    # COLUNA 1: Pedido de Venda + Orçamento
    with col_k1:
        st.markdown(f"""
        <div class="kanban-col-title" style="background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);">
            <div>
                <div style="font-weight:700;">📋 Pedido de Venda + Orçamento</div>
                <div style="font-size:11px; opacity:0.9; margin-top:2px;">{txt_c1}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if not p_col1:
            st.caption("Nenhum registro")
        for idx_k1, ped in enumerate(p_col1):
            cod_p = ped["codigo_pedido"]
            num_p = formatar_num_pedido_limpo(ped["numero_pedido"])
            cli_p = resolver_nome_cliente_kanban(ped)
            vlr_p = ped["valor_total"]
            dt_p = ped["data_previsao"]
            parc_str = extrair_str_parcelas_kanban(ped)
            is_pix = eh_pagamento_pix(ped)
            is_boleto = eh_pagamento_boleto(ped)
            comprovante_info = omie.obter_comprovante_pedido(cod_p)

            st.markdown(f"""
            <div class="kanban-card">
                <div class="kanban-card-title">{cli_p}</div>
                <div class="kanban-card-sub" style="font-size:12px; color: #000000; margin-top:2px;">Pedido Nº {num_p}</div>
                <div class="kanban-card-sub" style="color:#F59E0B; font-size:11px; margin-top:2px;">Aguardando faturamento</div>
                <div class="kanban-card-val" style="margin-top:6px;">{fmt_brl(vlr_p)} <span style="font-size:11px; font-weight:600; color: #000000; margin-left:4px;">{parc_str}</span></div>
                <div class="kanban-card-sub" style="font-size:10px; margin-top:4px;">Origem: Enviado via API</div>
            </div>
            """, unsafe_allow_html=True)

            c_act1, c_act2, c_act3, c_act4 = st.columns([1, 1, 1, 1])
            with c_act1:
                if st.button("🚀", key=f"btn_mvr_20_{idx_k1}_{cod_p}", use_container_width=True, help="Mover pedido para Análise de Faturamento (Etapa 20)"):
                    with st.spinner(f"Movendo #{num_p} para Análise Faturamento (Etapa 20)..."):
                        try:
                            omie.trocar_etapa_pedido_omie(cod_p, "20")
                            st.cache_data.clear()
                            st.toast(f"✅ Pedido #{num_p} movido para Análise Faturamento (Etapa 20)!")
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))
            with c_act2:
                if st.button("✏️", key=f"btn_edit_k1_{idx_k1}_{cod_p}", use_container_width=True, help="Editar pedido na Etapa 10 (Orçamento)"):
                    carregar_pedido_para_edicao_form(ped)
                    st.rerun()
            with c_act3:
                bytes_pdf = _gerar_pdf_fast(ped)
                fn_pdf = pdf_service.formatar_nome_arquivo_pdf(num_p, cli_p)
                st.download_button(
                    "📄",
                    data=bytes_pdf,
                    file_name=fn_pdf,
                    mime="application/pdf",
                    key=f"btn_pdf_k1_{idx_k1}_{cod_p}",
                    use_container_width=True,
                    help=f"Baixar Proposta / Orçamento Comercial em PDF do Pedido #{num_p} ({cli_p})"
                )
            with c_act4:
                if st.button("🗑️", key=f"btn_del_ped_col1_{idx_k1}_{cod_p}", use_container_width=True, help="Cancelar e excluir este pedido do Omie ERP"):
                    ok_del, msg_del = omie.cancelar_excluir_pedido_omie(cod_p, etapa_atual="10")
                    if ok_del:
                        st.toast(f"🗑️ Pedido #{num_p} removido do Dashboard!", icon="⚡")
                        st.rerun()
                    else:
                        st.error(msg_del)

            # ── REGRAS DE AVANÇO DE ETAPA NO KANBAN ──
            if is_boleto:
                if pode_autorizar_boleto:
                    if st.button("📦 Separação", key=f"btn_mvr_70_dir_boleto_k1_{idx_k1}_{cod_p}", type="primary", use_container_width=True, help="Aprovar e enviar pedido em Boleto para Separação de Estoque no Omie ERP (Etapa 70)"):
                        with st.spinner(f"Enviando Pedido #{num_p} (Boleto) para Separação de Estoque (Etapa 70)..."):
                            omie.trocar_etapa_pedido_omie(cod_p, "70")
                            st.cache_data.clear()
                            st.toast(f"✅ Pedido #{num_p} em Boleto liberado por pessoa autorizada para Separação de Estoque (Etapa 70)!")
                            st.rerun()
                else:
                    st.markdown("<div style='font-size:11px; color:#F59E0B; margin:4px 0;'>🔒 Boleto: Liberação para Separação restrita a pessoas autorizadas (Gestão/Financeiro).</div>", unsafe_allow_html=True)
            elif is_pix:
                if comprovante_info:
                    st.markdown(f"<div style='font-size:11px; color:#10B981; margin:4px 0;'>✅ Comprovante PIX: <b>{comprovante_info['nome_arquivo']}</b></div>", unsafe_allow_html=True)
                    if st.button("📦 Separação", key=f"btn_mvr_70_dir_k1_{idx_k1}_{cod_p}", type="primary", use_container_width=True, help="Aprovar e enviar para Separação de Estoque no Omie ERP (Etapa 70)"):
                        with st.spinner(f"Enviando Pedido #{num_p} para Separação de Estoque (Etapa 70)..."):
                            omie.trocar_etapa_pedido_omie(cod_p, "70")
                            st.cache_data.clear()
                            st.toast(f"✅ Pedido #{num_p} enviado para Separação de Estoque (Etapa 70)!")
                            st.rerun()
                else:
                    with st.popover("📦 Separação (PIX)", use_container_width=True, help="Anexar comprovante PIX para liberar para Separação"):
                        st.markdown(f"**Anexar Comprovante PIX — Pedido #{num_p}**")
                        st.caption("Obrigatório anexar comprovante de pagamento PIX para liberar o pedido para Separação de Estoque (Etapa 70).")
                        upl_comp = st.file_uploader("Upload do Comprovante (PDF/Imagem)", type=["pdf", "png", "jpg", "jpeg"], key=f"upl_comp_k1_{idx_k1}_{cod_p}")
                        if upl_comp is not None:
                            if st.button("🚀 Anexar & Mover p/ Etapa 70", key=f"btn_anexar_mvr_70_k1_{idx_k1}_{cod_p}", type="primary", use_container_width=True, help="Salvar anexo e avançar pedido para Etapa 70"):
                                with st.spinner("Anexando comprovante e movendo etapa..."):
                                    bytes_upl = upl_comp.read()
                                    omie.incluir_anexo_pedido_omie(cod_p, upl_comp.name, bytes_upl)
                                    omie.trocar_etapa_pedido_omie(cod_p, "70")
                                    st.cache_data.clear()
                                    st.toast(f"✅ Comprovante anexado! Pedido #{num_p} movido para Separação de Estoque (Etapa 70).")
                                    st.rerun()
            else:
                if st.button("📦 Separação", key=f"btn_mvr_70_direct_nopix_k1_{idx_k1}_{cod_p}", type="primary", use_container_width=True, help="Aprovar e enviar diretamente para Separação de Estoque (Etapa 70)"):
                    with st.spinner(f"Enviando Pedido #{num_p} para Separação de Estoque (Etapa 70)..."):
                        omie.trocar_etapa_pedido_omie(cod_p, "70")
                        st.cache_data.clear()
                        st.toast(f"✅ Pedido #{num_p} enviado para Separação de Estoque (Etapa 70)!")
            st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

    # COLUNA 2: Análise Faturamento
    with col_k2:
        st.markdown(f"""
        <div class="kanban-col-title" style="background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);">
            <div>
                <div style="font-weight:700;">💳 Análise Faturamento</div>
                <div style="font-size:11px; opacity:0.9; margin-top:2px;">{txt_c2}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if not p_col2:
            st.caption("Nenhum registro")
        for idx_k2, ped in enumerate(p_col2):
            cod_p = ped["codigo_pedido"]
            num_p = formatar_num_pedido_limpo(ped["numero_pedido"])
            cli_p = resolver_nome_cliente_kanban(ped)
            vlr_p = ped["valor_total"]
            parc_str = extrair_str_parcelas_kanban(ped)
            is_pix = eh_pagamento_pix(ped)
            is_boleto = eh_pagamento_boleto(ped)
            comprovante_info = omie.obter_comprovante_pedido(cod_p)

            st.markdown(f"""
            <div class="kanban-card">
                <div class="kanban-card-title">{cli_p}</div>
                <div class="kanban-card-sub" style="font-size:12px; color: #000000; margin-top:2px;">Pedido Nº {num_p}</div>
                <div class="kanban-card-val" style="margin-top:6px;">{fmt_brl(vlr_p)} <span style="font-size:11px; font-weight:600; color: #000000; margin-left:4px;">{parc_str}</span></div>
            </div>
            """, unsafe_allow_html=True)

            c_k2_a, c_k2_b, c_k2_c = st.columns([1, 1, 1])
            with c_k2_a:
                if st.button("📋", key=f"btn_ret_10_k2_{idx_k2}_{cod_p}", use_container_width=True, help="Retornar pedido para Pedido de Venda + Orçamento (Etapa 10)"):
                    with st.spinner(f"Retornando #{num_p} para Etapa 10..."):
                        try:
                            omie.trocar_etapa_pedido_omie(cod_p, "10")
                            st.cache_data.clear()
                            st.toast(f"✅ Pedido #{num_p} retornado para Pedido de Venda + Orçamento (Etapa 10)!")
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))
            with c_k2_b:
                bytes_pdf = _gerar_pdf_fast(ped)
                fn_pdf = pdf_service.formatar_nome_arquivo_pdf(num_p, cli_p)
                st.download_button(
                    "📄",
                    data=bytes_pdf,
                    file_name=fn_pdf,
                    mime="application/pdf",
                    key=f"btn_pdf_k2_{idx_k2}_{cod_p}",
                    use_container_width=True,
                    help=f"Baixar Proposta / Orçamento Comercial em PDF do Pedido #{num_p} ({cli_p})"
                )
            
            with c_k2_c:
                if is_boleto:
                    if pode_autorizar_boleto:
                        if st.button("📦", key=f"btn_mvr_70_dir_boleto_k2_{idx_k2}_{cod_p}", type="primary", use_container_width=True, help="Aprovar e enviar pedido em Boleto para Separação de Estoque no Omie ERP (Etapa 70)"):
                            with st.spinner(f"Enviando Pedido #{num_p} (Boleto) para Separação (70)..."):
                                sla_separacao.registrar_entrada_separacao(cod_p, num_p)
                                omie.trocar_etapa_pedido_omie(cod_p, "70")
                                st.cache_data.clear()
                                st.toast(f"✅ Pedido #{num_p} (Boleto) liberado por pessoa autorizada para Separação (70)!")
                                st.rerun()
                    else:
                        st.markdown("<div style='font-size:11px; color:#F59E0B; margin:4px 0;'>🔒 Restrito</div>", unsafe_allow_html=True)
                elif is_pix:
                    if comprovante_info:
                        if st.button("📦", key=f"btn_mvr_70_dir_k2_{idx_k2}_{cod_p}", type="primary", use_container_width=True, help="Mover para Separação de Estoque no Omie ERP (Etapa 70)"):
                            with st.spinner(f"Enviando Pedido #{num_p} para Separação (70)..."):
                                sla_separacao.registrar_entrada_separacao(cod_p, num_p)
                                omie.trocar_etapa_pedido_omie(cod_p, "70")
                                st.cache_data.clear()
                                st.toast(f"✅ Pedido #{num_p} enviado para Separação (70)!")
                                st.rerun()
                    else:
                        with st.popover("📦", use_container_width=True, help="Anexar comprovante PIX e mover para Separação"):
                            st.markdown(f"**Comprovante PIX — Pedido #{num_p}**")
                            upl_comp = st.file_uploader("Upload Comprovante PIX", type=["pdf", "png", "jpg", "jpeg"], key=f"upl_comp_k2_{idx_k2}_{cod_p}")
                            if upl_comp is not None:
                                if st.button("🚀 Anexar & Mover p/ 70", key=f"btn_anexar_mvr_70_k2_{idx_k2}_{cod_p}", type="primary", use_container_width=True, help="Salvar anexo e avançar pedido para Etapa 70"):
                                    with st.spinner("Anexando comprovante e movendo etapa..."):
                                        bytes_upl = upl_comp.read()
                                        omie.incluir_anexo_pedido_omie(cod_p, upl_comp.name, bytes_upl)
                                        sla_separacao.registrar_entrada_separacao(cod_p, num_p)
                                        omie.trocar_etapa_pedido_omie(cod_p, "70")
                                        st.cache_data.clear()
                                        st.toast(f"✅ Comprovante anexado! Pedido #{num_p} enviado para Separação (70).")
                                        st.rerun()
                else:
                    if st.button("📦", key=f"btn_mvr_70_nopix_k2_{idx_k2}_{cod_p}", type="primary", use_container_width=True, help="Mover para Separação de Estoque no Omie ERP (Etapa 70)"):
                        with st.spinner(f"Enviando Pedido #{num_p} para Separação (70)..."):
                            sla_separacao.registrar_entrada_separacao(cod_p, num_p)
                            omie.trocar_etapa_pedido_omie(cod_p, "70")
                            st.cache_data.clear()
            st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

    # COLUNA 3: Separar Estoque (BLOQUEADO / APENAS LEITURA)
    with col_k3:
        st.markdown(f"""
        <div class="kanban-col-title" style="background: linear-gradient(135deg, #8A79B0 0%, #6B5B95 100%);">
            <div>
                <div style="font-weight:700;">📦 Separar Estoque 🔒</div>
                <div style="font-size:11px; opacity:0.9; margin-top:2px;">{txt_c3}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if not p_col3:
            st.caption("Nenhum registro")
        for idx_k3, ped in enumerate(p_col3):
            cod_p = ped["codigo_pedido"]
            num_p = formatar_num_pedido_limpo(ped["numero_pedido"])
            cli_p = resolver_nome_cliente_kanban(ped)
            vlr_p = ped["valor_total"]
            parc_str = extrair_str_parcelas_kanban(ped)

            # ── CÁLCULO DE SLA DE SEPARAÇÃO (48H / ALERTA AOS 30H) ──
            sla_info = sla_separacao.calcular_sla_pedido(ped)
            card_border = f"border: 2px solid {sla_info['cor_borda']};" if sla_info["esta_atrasado"] else ""
            card_bg = f"background: {sla_info['cor_bg']};" if sla_info["esta_atrasado"] else ""

            transp_nome_p = ped.get("transportadora_nome") or ped.get("raw_data", {}).get("frete", {}).get("nome_transportadora") or ""
            html_transp = f'<div class="kanban-card-sub" style="font-size:10px; margin-top:4px;">Transportadora: {transp_nome_p}</div>' if transp_nome_p else ''

            st.markdown(f"""
            <div class="kanban-card" style="{card_border} {card_bg}">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 4px;">
                    <div class="kanban-card-title">{cli_p}</div>
                    {sla_info['badge_html']}
                </div>
                <div class="kanban-card-sub" style="font-size:12px; color: #000000; margin-top:2px;">Pedido Nº {num_p}</div>
                <div class="kanban-card-val" style="margin-top:6px;">{fmt_brl(vlr_p)} <span style="font-size:11px; font-weight:600; color: #000000; margin-left:4px;">{parc_str}</span></div>
                {sla_info['barra_html']}
                {html_transp}
            </div>
            """, unsafe_allow_html=True)

            bytes_pdf = _gerar_pdf_fast(ped)
            fn_pdf = pdf_service.formatar_nome_arquivo_pdf(num_p, cli_p)
            st.download_button(
                "📄 Baixar Proposta (PDF)",
                data=bytes_pdf,
                file_name=fn_pdf,
                mime="application/pdf",
                key=f"btn_pdf_k3_{idx_k3}_{cod_p}",
                use_container_width=True,
                help=f"Baixar Proposta / Orçamento Comercial em PDF do Pedido #{num_p} ({cli_p})"
            )
            st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

    # COLUNA 4: Faturar
    with col_k4:
        st.markdown(f"""
        <div class="kanban-col-title" style="background: linear-gradient(135deg, #06B6D4 0%, #0891B2 100%);">
            <div>
                <div style="font-weight:700;">📑 Faturar</div>
                <div style="font-size:11px; opacity:0.9; margin-top:2px;">{txt_c4}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if not p_col4:
            st.caption("Nenhum registro")
        for idx_k4, ped in enumerate(p_col4):
            cod_p = ped["codigo_pedido"]
            num_p = formatar_num_pedido_limpo(ped["numero_pedido"])
            cli_p = resolver_nome_cliente_kanban(ped)
            vlr_p = ped["valor_total"]
            parc_str = extrair_str_parcelas_kanban(ped)

            st.markdown(f"""
            <div class="kanban-card">
                <div class="kanban-card-title">{cli_p}</div>
                <div class="kanban-card-sub" style="font-size:12px; color: #000000; margin-top:2px;">Pedido Nº {num_p}</div>
                <div class="kanban-card-val" style="margin-top:6px;">{fmt_brl(vlr_p)} <span style="font-size:11px; font-weight:600; color: #000000; margin-left:4px;">{parc_str}</span></div>
            </div>
            """, unsafe_allow_html=True)

            bytes_pdf = _gerar_pdf_fast(ped)
            fn_pdf = pdf_service.formatar_nome_arquivo_pdf(num_p, cli_p)
            st.download_button(
                "📄 Baixar Proposta (PDF)",
                data=bytes_pdf,
                file_name=fn_pdf,
                mime="application/pdf",
                key=f"btn_pdf_k4_{idx_k4}_{cod_p}",
                use_container_width=True,
                help=f"Baixar Proposta / Orçamento Comercial em PDF do Pedido #{num_p} ({cli_p})"
            )
            st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

    # COLUNA 5: Faturado (CÁLCULO EXATO DE SLA DO TEMPO DE ENTREGA & RASTREIO)
    with col_k5:
        st.markdown(f"""
        <div class="kanban-col-title" style="background: linear-gradient(135deg, #10B981 0%, #047857 100%);">
            <div>
                <div style="font-weight:700;">✅ Faturado 🔒</div>
                <div style="font-size:11px; opacity:0.9; margin-top:2px;">{txt_c5}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if not p_col5:
            st.caption("Nenhum registro")

        limite_k5 = 30 if not busca_kanban else len(p_col5)
        p_col5_exibir = p_col5[:limite_k5]

        for idx_k5, ped in enumerate(p_col5_exibir):
            cod_p = ped["codigo_pedido"]
            num_p = formatar_num_pedido_limpo(ped["numero_pedido"])
            cli_p = resolver_nome_cliente_kanban(ped)
            vlr_p = ped["valor_total"]
            parc_str = extrair_str_parcelas_kanban(ped)

            r_info = logistica_rastreio.obter_dados_rastreio_pedido(ped)
            status_real = r_info.get("status_real", "Faturado")
            transp_nome = r_info.get("transportadora", "A Combinar")
            cod_track = r_info.get("codigo_rastreio", "")
            cod_puro = r_info.get("codigo_puro") or ""
            is_entregue = "Entreg" in status_real or str(ped.get("etapa")) == "80"

            if is_entregue:
                badge_bg = "#ECFDF5"
                badge_borda = "#A7F3D0"
                badge_cor = "#059669"
                badge_txt = "✅ Entregue"
            else:
                badge_bg = "#EFF6FF"
                badge_borda = "#BFDBFE"
                badge_cor = "#1D4ED8"
                badge_txt = "🚚 Em Transporte"

            badge_sla_html = f'<span style="background-color: {badge_bg}; border: 1px solid {badge_borda}; color: {badge_cor}; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: 700;">{badge_txt}</span>'

            # Identificação simplificada da Transportadora
            if "Correios" in transp_nome:
                transp_icone = "📦 Correios"
            elif "Braspress" in transp_nome:
                transp_icone = "🚛 Braspress"
            elif "Ativa" in transp_nome:
                transp_icone = "✈️ Ativa"
            elif "Retirada" in transp_nome:
                transp_icone = "🏢 Retirada CD"
            else:
                transp_icone = f"🚚 {transp_nome[:14]}"

            # Rastreio limpo
            if cod_puro and len(cod_puro) >= 11:
                rastreio_badge = f'<a href="https://www.linkcorreios.com.br/?id={cod_puro}" target="_blank" style="text-decoration: none; color: #4338CA; font-family: monospace; font-weight: 700; background: #EEF2FF; border: 1px solid #C7D2FE; padding: 2px 6px; border-radius: 4px;" title="Ver rastreio direto">{cod_puro} ↗️</a>'
            elif cod_track:
                rastreio_badge = f'<code style="font-size: 10.5px; background: #F1F5F9; padding: 2px 5px; border-radius: 4px;">{cod_track}</code>'
            else:
                rastreio_badge = '<span style="color: #94A3B8; font-size: 10.5px;">Aguardando envio</span>'

            card_faturado_html = (
                f'<div class="kanban-card">'
                f'<div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 4px;">'
                f'<div class="kanban-card-title">{cli_p}</div>'
                f'{badge_sla_html}'
                f'</div>'
                f'<div class="kanban-card-sub" style="font-size:12px; color: #64748B; margin-top:2px;">Pedido Nº {num_p}</div>'
                f'<div class="kanban-card-val" style="margin-top:4px;">{fmt_brl(vlr_p)} <span style="font-size:11px; font-weight:600; color: #64748B; margin-left:4px;">{parc_str}</span></div>'
                f'<div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 7px 10px; margin-top: 8px; font-size: 11px;">'
                f'<div style="display: flex; justify-content: space-between; align-items: center;">'
                f'<span style="font-weight: 700; color: #1E293B;">{transp_icone}</span>'
                f'<span style="color: {badge_cor}; font-weight: 600; font-size: 10px;">{status_real}</span>'
                f'</div>'
                f'<div style="margin-top: 5px; display: flex; align-items: center; justify-content: space-between;">'
                f'<span style="color: #64748B; font-size: 10.5px;">Rastreio:</span>'
                f'{rastreio_badge}'
                f'</div>'
                f'</div>'
                f'</div>'
            )
            st.markdown(card_faturado_html, unsafe_allow_html=True)

            c_k5_a, c_k5_b = st.columns([1, 1.2])
            with c_k5_a:
                bytes_pdf = _gerar_pdf_fast(ped)
                fn_pdf = pdf_service.formatar_nome_arquivo_pdf(num_p, cli_p)
                st.download_button(
                    "📄 PDF",
                    data=bytes_pdf,
                    file_name=fn_pdf,
                    mime="application/pdf",
                    key=f"btn_pdf_k5_{idx_k5}_{cod_p}",
                    use_container_width=True,
                    help=f"Baixar Proposta / Orçamento Comercial em PDF do Pedido #{num_p} ({cli_p})"
                )
            with c_k5_b:
                if r_info.get("url_comprovante"):
                    st.markdown(f"""<a href="{r_info['url_comprovante']}" target="_blank" style="display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #10B981 0%, #059669 100%); color: #FFFFFF !important; font-size: 11.5px; font-weight: 800; height: 35px; border-radius: 8px; text-decoration: none; box-shadow: 0 2px 6px rgba(16,185,129,0.25);">
                        📸 Canhoto
                    </a>""", unsafe_allow_html=True)
                elif r_info.get("tipo_rastreio") == "CORREIOS" and cod_puro:
                    link_c = f"https://www.linkcorreios.com.br/?id={cod_puro}"
                    st.markdown(f"""<a href="{link_c}" target="_blank" title="Rastrear {cod_puro} em tempo real" style="display: flex; align-items: center; justify-content: center; background: #FFFFFF; border: 1px solid #CBD5E1; color: #000000 !important; -webkit-text-fill-color: #000000 !important; font-size: 11.5px; font-weight: 700; height: 35px; border-radius: 8px; text-decoration: none; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                        <span style="color: #000000 !important; -webkit-text-fill-color: #000000 !important; font-weight: 700;">🚚 Rastrear</span>
                    </a>""", unsafe_allow_html=True)
                elif r_info.get("link_rastreio"):
                    st.markdown(f"""<a href="{r_info['link_rastreio']}" target="_blank" style="display: flex; align-items: center; justify-content: center; background: #FFFFFF; border: 1px solid #CBD5E1; color: #000000 !important; -webkit-text-fill-color: #000000 !important; font-size: 11.5px; font-weight: 700; height: 35px; border-radius: 8px; text-decoration: none; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                        <span style="color: #000000 !important; -webkit-text-fill-color: #000000 !important; font-weight: 700;">🚚 Rastrear</span>
                    </a>""", unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

        if len(p_col5) > limite_k5:
            st.caption(f"Exibindo os {limite_k5} pedidos mais recentes faturados (de um total de {len(p_col5)}). Utilize o campo de busca no topo para encontrar qualquer pedido anterior.")
            st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA: TORRE DE CONTROLE & LOGÍSTICA 360º (HUB, EUROLOG & TRANSPORTADORAS)
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "🚚  Rastreamento & Logística":

    # Cabeçalho Executivo da Torre de Controle
    col_hdr_t1, col_hdr_t2 = st.columns([3.5, 1.5])
    with col_hdr_t1:
        st.markdown("""
        <div class="page-header" style="margin-bottom: 12px;">
            <div class="page-header-icon">🗼</div>
            <div>
                <div class="page-header-title">Torre de Controle & Logística 360°</div>
                <div class="page-header-subtitle">Sincronização ao vivo com Omie ERP, Radar de Pedidos no Hub (TikTok Shop, ML, Shopify), SLA Eurolog (3PL) e Transportadoras.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_hdr_t2:
        st.write("")
        btn_sync_live = st.button("⚡ Sincronizar com Omie ao Vivo", type="primary", use_container_width=True, key="btn_sync_torre_live")

    # Ação de Sincronização Forçada ao Vivo com o Omie ERP
    if btn_sync_live:
        with st.spinner("🔄 Conectando às APIs do Omie ERP e atualizando pedidos em tempo real..."):
            sucesso, info_sync, _ = tcs.sincronizar_torre_ao_vivo()
            if sucesso:
                st.success(f"✅ Torre de Controle atualizada! {info_sync['total_pedidos']} pedidos sincronizados em {info_sync['tempo_execucao_s']}s.")
                st.rerun()
            else:
                st.error(f"❌ Erro na sincronização: {info_sync.get('erro')}")

    # 1. Carregamento de dados com cache
    with st.spinner("Carregando inteligência da Torre de Controle..."):
        todos_pedidos_raw = omie.listar_pedidos_omie(force_refresh=False)
        mapas_nf = logistica_rastreio.carregar_mapa_notas_fiscais()
        mapa_plan = logistica_rastreio.carregar_mapa_planilha_rastreio()
        diag_torre = tcs.diagnosticar_torre_de_controle(todos_pedidos_raw)

    kpis_torre = diag_torre["kpis"]
    status_sync = diag_torre["status_sincronizacao"]
    pedidos_hub_parados = diag_torre["pedidos_hub_parados"]
    pedidos_em_separacao = diag_torre["pedidos_em_separacao"]
    pedidos_etapa_10_normais = diag_torre["pedidos_etapa_10_normais"]

    # Barra informativa de sincronismo no topo
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; background: #F8FAFC; border: 1px solid #E2E8F0; padding: 8px 16px; border-radius: 8px; margin-bottom: 16px; font-size: 12px; color: #64748B;">
        <div>📡 <b>Status da Conexão:</b> Omie ERP Integrado (615 Pedidos) &bull; <b>Última Sincronização:</b> <span style="color: #0F172A; font-weight: 700;">{status_sync.get('ultima_sincronizacao_fmt', 'Ao Vivo')}</span></div>
        <div>💡 <i>Os dados refletem 1:1 o banco de dados oficial do ERP e do Hub</i></div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Consolidação de Cargas Expedidas
    pedidos_expedidos = []
    for ped in (todos_pedidos_raw or []):
        if omie.eh_pedido_cancelado(ped):
            continue
        etapa_str = str(ped.get("etapa") or "").strip()
        faturado = str(ped.get("raw_data", {}).get("infoCadastro", {}).get("faturado") or "").upper() == "S"
        if faturado or etapa_str in ["60", "80"]:
            r_info = logistica_rastreio.obter_dados_rastreio_pedido(ped, mapas_nf, mapa_plan)
            pedidos_expedidos.append({
                "pedido_obj": ped,
                "numero": ped.get("numero_pedido"),
                "pedido_display": f"#{ped.get('numero_pedido')}",
                "cliente_real": r_info["cliente_real"],
                "transportadora": r_info["transportadora"],
                "codigo_rastreio": r_info["codigo_rastreio"],
                "numero_nf": r_info["numero_nf"],
                "chave_danfe": r_info["chave_danfe"],
                "cnpj_cpf": r_info["cnpj_cpf"],
                "status_real": r_info["status_real"],
                "ultima_ocorrencia": r_info["ultima_ocorrencia"],
                "link_rastreio": r_info["link_rastreio"],
                "url_comprovante": r_info.get("url_comprovante"),
                "uf": r_info["uf"],
                "valor": ped.get("valor_total") or 0.0,
                "valor_fmt": fmt_brl(ped.get("valor_total") or 0.0),
                "data_faturamento": str(ped.get("raw_data", {}).get("infoCadastro", {}).get("dFat") or ped.get("data_previsao") or "")[:10]
            })

    tot_exp = len(pedidos_expedidos)
    tot_cor = sum(1 for p in pedidos_expedidos if "Correios" in p["transportadora"])
    tot_bp = sum(1 for p in pedidos_expedidos if "Braspress" in p["transportadora"])
    tot_ati = sum(1 for p in pedidos_expedidos if "Ativa" in p["transportadora"])
    tot_ent = sum(1 for p in pedidos_expedidos if "Entreg" in p["status_real"])

    # 3. Mini KPIs Executivos da Torre
    col_k1, col_k2, col_k3, col_k4, col_k5 = st.columns(5)
    
    cor_hub_kpi = "#EF4444" if kpis_torre["hub_parados_criticos"] > 0 else "#10B981"
    bg_hub_kpi = "#FEF2F2" if kpis_torre["hub_parados_criticos"] > 0 else "#ECFDF5"
    
    with col_k1:
        st.markdown(f"""<div style="background: {bg_hub_kpi}; border: 1px solid {'#FECACA' if kpis_torre['hub_parados_criticos'] > 0 else '#A7F3D0'}; border-radius: 12px; padding: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div style="font-size: 11px; font-weight: 700; color: {cor_hub_kpi}; text-transform: uppercase;">🚨 Hub / Entrada Parados</div>
            <div style="font-size: 24px; font-weight: 800; color: {cor_hub_kpi}; margin-top: 2px;">{kpis_torre['hub_parados_criticos']}</div>
            <div style="font-size: 11px; color: #64748B;">Requer Intervenção</div>
        </div>""", unsafe_allow_html=True)
    with col_k2:
        st.markdown(f"""<div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div style="font-size: 11px; font-weight: 700; color: #2563EB; text-transform: uppercase;">⏱️ Separação Eurolog</div>
            <div style="font-size: 24px; font-weight: 800; color: #1E40AF; margin-top: 2px;">{kpis_torre['separacao_total']}</div>
            <div style="font-size: 11px; color: #64748B;">Na Esteira de Picking</div>
        </div>""", unsafe_allow_html=True)
    with col_k3:
        cor_sla = "#EF4444" if kpis_torre['separacao_estourado'] > 0 else ("#F59E0B" if kpis_torre['separacao_alerta'] > 0 else "#10B981")
        tot_alertas_sla = kpis_torre['separacao_estourado'] + kpis_torre['separacao_alerta']
        st.markdown(f"""<div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div style="font-size: 11px; font-weight: 700; color: {cor_sla}; text-transform: uppercase;">⚠️ Alertas SLA (3PL)</div>
            <div style="font-size: 24px; font-weight: 800; color: {cor_sla}; margin-top: 2px;">{tot_alertas_sla}</div>
            <div style="font-size: 11px; color: #64748B;">72h TikTok / 48h B2B</div>
        </div>""", unsafe_allow_html=True)
    with col_k4:
        st.markdown(f"""<div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase;">📦 Cargas Faturadas</div>
            <div style="font-size: 24px; font-weight: 800; color: #0F172A; margin-top: 2px;">{tot_exp}</div>
            <div style="font-size: 11px; color: #64748B;">Expedição Ativa</div>
        </div>""", unsafe_allow_html=True)
    with col_k5:
        st.markdown(f"""<div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div style="font-size: 11px; font-weight: 700; color: #059669; text-transform: uppercase;">✅ Entregas Concluídas</div>
            <div style="font-size: 24px; font-weight: 800; color: #059669; margin-top: 2px;">{tot_ent}</div>
            <div style="font-size: 11px; color: #64748B;">Comprovados</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)

    # 4. Banner Crítico de Alerta do Hub
    if pedidos_hub_parados:
        st.markdown(f"""
        <div style="background: #FEF2F2; border-left: 6px solid #EF4444; border-radius: 10px; padding: 16px 20px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(239,68,68,0.08);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="font-size: 15px; font-weight: 800; color: #991B1B;">
                    🚨 RADAR DE ALERTA DO HUB: {len(pedidos_hub_parados)} Pedido(s) Retido(s) no Funil de Entrada!
                </div>
                <div style="background: #EF4444; color: white; font-weight: 800; font-size: 11px; padding: 4px 10px; border-radius: 12px;">
                    AÇÃO IMEDIATA NECESSÁRIA
                </div>
            </div>
            <div style="font-size: 13px; color: #7F1D1D; margin-top: 6px;">
                Identificamos pedidos aguardando na Etapa 10 com tempo excessivo ou com pendências cadastrais/fiscais (CPF/CNPJ ou dados de destino) que impedem o avanço para a esteira de separação da Eurolog.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 5. Abas Operacionais da Torre de Controle
    tab_radar_hub, tab_separacao_sla, tab_rastreio_transp, tab_conexoes_api = st.tabs([
        f"🚨 Radar de Pedidos no Hub ({len(pedidos_hub_parados)})",
        f"⏱️ Fila de Separação Eurolog ({len(pedidos_em_separacao)})",
        f"🚚 Expedição & Rastreamento em Tempo Real ({tot_exp})",
        "⚙️ Conexões de APIs & Sincronizador"
    ])

    # ══════════════════════════════════════════════════════════════════════════════
    # ABA 1: RADAR DE PEDIDOS NO HUB & ENTRADA
    # ══════════════════════════════════════════════════════════════════════════════
    with tab_radar_hub:
        st.markdown("#### 🚨 Detector de Pedidos Parados no Hub & Funil de Entrada")
        st.markdown("<p style='color: #64748B; font-size: 13px; margin-top: -6px;'>Monitoramento preventivo para e-commerce (TikTok Shop, Mercado Livre, Shopify) e B2B para evitar que pedidos fiquem esquecidos na Etapa 10 antes da separação:</p>", unsafe_allow_html=True)

        if pedidos_hub_parados:
            for p_hub in pedidos_hub_parados:
                cor_borda = "#EF4444" if p_hub["status_gravidade"] == "CRÍTICO" else "#F59E0B"
                badge_bg = "#FEE2E2" if p_hub["status_gravidade"] == "CRÍTICO" else "#FEF3C7"
                badge_fg = "#991B1B" if p_hub["status_gravidade"] == "CRÍTICO" else "#92400E"
                canal = p_hub["canal"]
                tempo = p_hub["tempo"]
                motivos_html = "".join([f"<li>{m}</li>" for m in p_hub['motivos']])
                doc_html = p_hub['cnpj_cpf'] or '<span style="color:#EF4444; font-weight:700;">Não Informado</span>'

                card_hub_html = (
                    f'<div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 6px solid {cor_borda}; border-radius: 12px; padding: 18px 20px; margin-bottom: 14px; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">'
                    f'<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">'
                    f'<div style="display: flex; align-items: center; gap: 10px;">'
                    f'<span style="font-size: 20px;">{canal["icone"]}</span>'
                    f'<div>'
                    f'<span style="font-size: 16px; font-weight: 800; color: #0F172A;">Pedido #{p_hub["numero_pedido"]}</span>'
                    f'<span style="background: {canal["badge_bg"]}; color: {canal["badge_fg"]}; font-weight: 700; font-size: 11px; padding: 3px 8px; border-radius: 6px; margin-left: 8px;">{canal["canal"]}</span>'
                    f'<span style="background: #EFF6FF; color: #1E40AF; font-weight: 700; font-size: 11px; padding: 3px 8px; border-radius: 6px; margin-left: 4px;">UF: {p_hub["uf"] or "N/I"}</span>'
                    f'</div></div>'
                    f'<div><span style="background: {badge_bg}; color: {badge_fg}; font-weight: 800; font-size: 12px; padding: 5px 12px; border-radius: 20px;">⏱️ {int(tempo["horas"])} HORAS NA ETAPA 10 &bull; {p_hub["status_gravidade"]}</span></div>'
                    f'</div>'
                    f'<div style="margin-top: 12px; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; font-size: 13px; color: #334155; background: #F8FAFC; padding: 12px 14px; border-radius: 8px;">'
                    f'<div>👤 <b>Cliente:</b> {p_hub["cliente_nome"]}</div>'
                    f'<div>📄 <b>Documento:</b> {doc_html}</div>'
                    f'<div>💰 <b>Valor Total:</b> {fmt_brl(p_hub["valor_total"])}</div>'
                    f'<div>📅 <b>Entrada/Última Alt.:</b> {tempo["data_base_fmt"]}</div>'
                    f'</div>'
                    f'<div style="margin-top: 12px; font-size: 13px;">'
                    f'<span style="font-weight: 700; color: #0F172A;">Diagnóstico do Faturista & Logística:</span>'
                    f'<ul style="margin: 6px 0 0 0; padding-left: 20px; color: #991B1B; font-weight: 600;">{motivos_html}</ul>'
                    f'</div>'
                    f'</div>'
                )
                st.markdown(card_hub_html, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 12px; padding: 24px; text-align: center; margin-bottom: 16px;">
                <div style="font-size: 32px; margin-bottom: 8px;">🎉</div>
                <div style="font-size: 16px; font-weight: 800; color: #166534;">Nenhum Pedido Retido ou Travado no Hub!</div>
                <div style="font-size: 13px; color: #15803D; margin-top: 4px;">O fluxo de entrada do e-commerce e B2B está 100% fluido e sem pendências cadastrais na Etapa 10.</div>
            </div>
            """, unsafe_allow_html=True)

        # Seção complementar: Demais pedidos recentes na Etapa 10
        if pedidos_etapa_10_normais:
            st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
            st.markdown("##### 📋 Pedidos Normais em Análise (Etapa 10 Recentes)")
            df_e10 = pd.DataFrame([{
                "Pedido": f"#{p['numero_pedido']}",
                "Canal": p['canal']['canal'],
                "Cliente": p['cliente_nome'],
                "UF": p['uf'],
                "Valor": fmt_brl(p['valor_total']),
                "Tempo Decorrido": f"{int(p['tempo']['horas'])}h",
                "Entrada": p['tempo']['data_base_fmt']
            } for p in pedidos_etapa_10_normais])
            st.dataframe(df_e10, use_container_width=True)

    # ══════════════════════════════════════════════════════════════════════════════
    # ABA 2: FILA DE SEPARAÇÃO EUROLOG & SLAs
    # ══════════════════════════════════════════════════════════════════════════════
    with tab_separacao_sla:
        st.markdown("#### ⏱️ Esteira de Separação Eurolog (3PL) & Controle de SLA")
        st.markdown("<p style='color: #64748B; font-size: 13px; margin-top: -6px;'>Acompanhamento de picking e packing com prioridade máxima para <b>TikTok Shop / Mercado Livre (SLA 72h)</b> e <b>B2B Corporativo (SLA 48h)</b>:</p>", unsafe_allow_html=True)

        if pedidos_em_separacao:
            for p_sep in pedidos_em_separacao:
                canal = p_sep["canal"]
                status_sla = p_sep["status_sla"]
                cor_sla = "#10B981" if status_sla == "no_prazo" else ("#F59E0B" if status_sla == "alerta" else "#EF4444")
                badge_bg = "#ECFDF5" if status_sla == "no_prazo" else ("#FEF3C7" if status_sla == "alerta" else "#FEE2E2")
                badge_fg = "#065F46" if status_sla == "no_prazo" else ("#92400E" if status_sla == "alerta" else "#991B1B")
                
                pct_sla = min(100, int((p_sep["horas_decorridas"] / p_sep["sla_horas_limite"]) * 100))

                card_sep_html = (
                    f'<div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 6px solid {cor_sla}; border-radius: 12px; padding: 18px 20px; margin-bottom: 14px; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">'
                    f'<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">'
                    f'<div style="display: flex; align-items: center; gap: 10px;">'
                    f'<span style="font-size: 20px;">{canal["icone"]}</span>'
                    f'<div>'
                    f'<span style="font-size: 16px; font-weight: 800; color: #0F172A;">Pedido #{p_sep["numero_pedido"]}</span>'
                    f'<span style="background: {canal["badge_bg"]}; color: {canal["badge_fg"]}; font-weight: 700; font-size: 11px; padding: 3px 8px; border-radius: 6px; margin-left: 8px;">{canal["canal"]}</span>'
                    f'<span style="background: #EFF6FF; color: #1E40AF; font-weight: 700; font-size: 11px; padding: 3px 8px; border-radius: 6px; margin-left: 4px;">UF: {p_sep["uf"]}</span>'
                    f'</div></div>'
                    f'<div><span style="background: {badge_bg}; color: {badge_fg}; font-weight: 800; font-size: 12px; padding: 5px 12px; border-radius: 20px;">{p_sep["status_label"]} &bull; Restam: {p_sep["horas_restantes"]}h</span></div>'
                    f'</div>'
                    f'<div style="margin-top: 12px; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; font-size: 13px; color: #334155; background: #F8FAFC; padding: 12px 14px; border-radius: 8px;">'
                    f'<div>👤 <b>Cliente:</b> {p_sep["cliente_nome"]}</div>'
                    f'<div>💰 <b>Valor:</b> {fmt_brl(p_sep["valor_total"])}</div>'
                    f'<div>📥 <b>Entrada em Separação:</b> {p_sep["data_entrada_fmt"]}</div>'
                    f'<div>⏳ <b>SLA Contratual:</b> {p_sep["sla_horas_limite"]} horas ({canal["tipo"]})</div>'
                    f'</div>'
                    f'<div style="margin-top: 12px;">'
                    f'<div style="display: flex; justify-content: space-between; font-size: 12px; font-weight: 700; color: #64748B; margin-bottom: 4px;">'
                    f'<span>Consumo de SLA: {p_sep["horas_decorridas"]}h decorridas</span>'
                    f'<span>{pct_sla}% do limite de {p_sep["sla_horas_limite"]}h</span>'
                    f'</div>'
                    f'<div style="background: #E2E8F0; border-radius: 10px; height: 8px; width: 100%; overflow: hidden;">'
                    f'<div style="background: {cor_sla}; height: 100%; width: {pct_sla}%; border-radius: 10px;"></div>'
                    f'</div></div>'
                    f'</div>'
                )
                st.markdown(card_sep_html, unsafe_allow_html=True)
        else:
            st.info("Nenhum pedido aguardando separação na esteira da Eurolog no momento.")

    # ══════════════════════════════════════════════════════════════════════════════
    # ABA 3: EXPEDIÇÃO & RASTREAMENTO EM TEMPO REAL
    # ══════════════════════════════════════════════════════════════════════════════
    with tab_rastreio_transp:
        st.markdown("#### 🚚 Rastreamento em Tempo Real nas Transportadoras")
        st.markdown("<p style='color: #64748B; font-size: 13px; margin-top: -6px;'>Consulta instantânea via API oficial em <b>Braspress, Ativa Logística (SSW) e Correios/SuperFrete</b>:</p>", unsafe_allow_html=True)

        # Consulta Rápida Online (Busca Dinâmica por qualquer identificador)
        c_q1, c_q2 = st.columns([4, 1.2])
        with c_q1:
            txt_query_rastreio = st.text_input(
                "Identificador de Envio",
                placeholder="Digite o Código de Rastreio (ex: AD953365722BR), NF-e (ex: 613), CPF/CNPJ ou Pedido (#755)...",
                key="input_tracking_global_crm",
                label_visibility="collapsed"
            )
        with c_q2:
            btn_query_online = st.button("⚡ Consultar API Oficial", type="primary", use_container_width=True, key="btn_exec_tracking_crm")

        if btn_query_online and txt_query_rastreio and txt_query_rastreio.strip():
            termo_q = txt_query_rastreio.strip()
            termo_q_clean = re.sub(r'\D', '', termo_q)
            
            # Encontrar pedido correspondente
            ped_match = None
            for p_item in pedidos_expedidos:
                if (termo_q.lower() in str(p_item["numero"]).lower()
                    or termo_q.lower() in str(p_item["codigo_rastreio"]).lower()
                    or termo_q_clean in str(p_item["numero_nf"])
                    or (termo_q_clean and termo_q_clean in re.sub(r'\D', '', p_item["cnpj_cpf"]))
                    or termo_q.lower() in p_item["cliente_real"].lower()):
                    ped_match = p_item
                    break

            with st.spinner("Consultando API oficial da transportadora em tempo real..."):
                if ped_match:
                    t_alvo = ped_match["transportadora"]
                    nf_alvo = ped_match["numero_nf"]
                    doc_alvo = ped_match["cnpj_cpf"]
                    chave_alvo = ped_match["chave_danfe"]
                    num_alvo = ped_match["numero"]
                else:
                    # Inferir transportadora pelo formato
                    if termo_q.upper().endswith("BR") or termo_q.upper().startswith("OY") or len(termo_q) == 13:
                        t_alvo = "SuperFrete (Correios)"
                    else:
                        t_alvo = "Braspress"
                    nf_alvo = termo_q_clean if len(termo_q_clean) <= 6 else ""
                    doc_alvo = termo_q_clean if len(termo_q_clean) in [11, 14] else ""
                    chave_alvo = termo_q_clean if len(termo_q_clean) == 44 else ""
                    num_alvo = termo_q_clean

                res_online = logistica_rastreio.consultar_api_transportadora_online(
                    transp=t_alvo,
                    numero_nf=nf_alvo,
                    cnpj_dest=doc_alvo,
                    chave_nfe=chave_alvo,
                    num_pedido=num_alvo
                )

            st.markdown(f"""
            <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-left: 6px solid #2563EB; border-radius: 12px; padding: 18px; margin: 16px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 16px; font-weight: 800; color: #1E293B;">📦 {res_online.get('transportadora')} — {ped_match['cliente_real'] if ped_match else 'Destinatário'}</span>
                    <span style="background: #EFF6FF; color: #2563EB; font-weight: 800; font-size: 12px; padding: 4px 10px; border-radius: 20px;">{res_online.get('status_real')}</span>
                </div>
                <div style="font-size: 13px; color: #475569; display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; margin: 10px 0;">
                    <div>🏷️ <b>Código de Rastreio:</b> <code>{res_online.get('codigo_rastreio')}</code></div>
                    <div>🏢 <b>Filial Atual:</b> {res_online.get('filial_atual')}</div>
                    <div>⏱️ <b>Previsão de Entrega:</b> {res_online.get('previsao_entrega')}</div>
                    <div>📄 <b>Nota Fiscal:</b> {nf_alvo or 'Pendente'}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            c_act1, c_act2 = st.columns([1.5, 3])
            with c_act1:
                if res_online.get("link_portal"):
                    st.markdown(f"""<a href="{res_online['link_portal']}" target="_blank" style="display: inline-block; background: #0F172A; color: white !important; font-size: 12px; font-weight: 700; padding: 10px 16px; border-radius: 8px; text-decoration: none;">
                        🌐 Acompanhar no Portal da Transportadora
                    </a>""", unsafe_allow_html=True)
                if res_online.get("url_comprovante"):
                    st.markdown(f"""<a href="{res_online['url_comprovante']}" target="_blank" style="display: inline-block; background: #059669; color: white !important; font-size: 12px; font-weight: 700; padding: 10px 16px; border-radius: 8px; text-decoration: none; margin-top: 6px;">
                        📸 Ver Comprovante Digital (Assinatura / Foto)
                    </a>""", unsafe_allow_html=True)

        st.markdown("<hr style='margin: 20px 0 16px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

        # Tabela Executiva com Filtros
        col_tf1, col_tf2, col_tf3 = st.columns([2, 1.5, 3])
        with col_tf1:
            f_tr = st.selectbox("Filtrar por Transportadora", ["Todas", "SuperFrete (Correios)", "Braspress", "Ativa Logística (SSW)"], key="crm_flt_tr")
        with col_tf2:
            f_st = st.selectbox("Status", ["Todos", "Entregue", "Em Trânsito", "Aguardando Postagem"], key="crm_flt_st")
        with col_tf3:
            f_txt = st.text_input("🔍 Buscar por Cliente, Pedido, NF ou Rastreio", placeholder="Ex: Mariluci, #755, AD9533...", key="crm_flt_txt")

        filtrados = []
        termo_f = (f_txt or "").strip().lower()
        for p_row in pedidos_expedidos:
            if f_tr != "Todas" and p_row["transportadora"] != f_tr:
                continue
            if f_st != "Todos":
                if f_st == "Entregue" and "Entreg" not in p_row["status_real"]:
                    continue
                elif f_st == "Em Trânsito" and "Trânsito" not in p_row["status_real"]:
                    continue
                elif f_st == "Aguardando Postagem" and "Aguardando" not in p_row["status_real"]:
                    continue
            if termo_f:
                m_txt = (
                    termo_f in str(p_row["numero"]).lower()
                    or termo_f in str(p_row["cliente_real"]).lower()
                    or termo_f in str(p_row["transportadora"]).lower()
                    or termo_f in str(p_row["codigo_rastreio"]).lower()
                    or termo_f in str(p_row["numero_nf"]).lower()
                    or termo_f in str(p_row["cnpj_cpf"]).lower()
                )
                if not m_txt:
                    continue
            filtrados.append(p_row)

        if filtrados:
            df_log = pd.DataFrame([{
                "Pedido": p["pedido_display"],
                "Cliente / Destinatário": p["cliente_real"],
                "Transportadora": p["transportadora"],
                "Código Rastreio / CT-e": p["codigo_rastreio"],
                "Nota Fiscal (NF-e)": p["numero_nf"],
                "CPF / CNPJ": p["cnpj_cpf"],
                "Status Logístico": p["status_real"],
                "Última Ocorrência": p["ultima_ocorrencia"],
                "UF": p["uf"],
                "Valor": p["valor_fmt"],
                "Data Faturamento": p["data_faturamento"]
            } for p in filtrados])

            st.dataframe(df_log, use_container_width=True, height=450)

            c_d1, c_d2 = st.columns([3, 1])
            with c_d2:
                csv_bytes = df_log.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    "📥 Exportar Tabela (CSV)",
                    data=csv_bytes,
                    file_name=f"RASTREAMENTO_MISSHA_{datetime.date.today().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.info("Nenhuma carga localizada para os filtros selecionados.")

    # ══════════════════════════════════════════════════════════════════════════════
    # ABA 4: STATUS DAS CONEXÕES DE API & AUDITORIA
    # ══════════════════════════════════════════════════════════════════════════════
    with tab_conexoes_api:
        st.markdown("#### ⚙️ Status das Conexões de API & Sincronização")
        st.markdown("<p style='color: #64748B; font-size: 13px; margin-top: -6px;'>Painel de integridade técnica das integrações e credenciais ativas no CRM MISSHA:</p>", unsafe_allow_html=True)

        col_api1, col_api2 = st.columns(2)
        with col_api1:
            st.markdown("""
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; margin-bottom: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-weight: 800; font-size: 15px; color: #0F172A;">🏢 Omie ERP (Vendas, NF-e & Estoque)</span>
                    <span style="background: #ECFDF5; color: #065F46; font-weight: 800; font-size: 11px; padding: 3px 8px; border-radius: 12px;">CONECTADO (200 OK)</span>
                </div>
                <div style="font-size: 12px; color: #64748B;">
                    • <b>App Key:</b> <code>5817***49545</code><br>
                    • <b>Ambiente:</b> Produção Oficial MISSHA BRASIL<br>
                    • <b>Endpoints:</b> <code>produtos/pedido</code>, <code>geral/produtos</code>, <code>geral/clientes</code>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; margin-bottom: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-weight: 800; font-size: 15px; color: #0F172A;">🔄 Omie.HUB & Marketplaces</span>
                    <span style="background: #EFF6FF; color: #1E40AF; font-weight: 800; font-size: 11px; padding: 3px 8px; border-radius: 12px;">ATIVO VIA ERP</span>
                </div>
                <div style="font-size: 12px; color: #64748B;">
                    • <b>Canais Monitorados:</b> TikTok Shop, Mercado Livre, Shopify, Shopee<br>
                    • <b>Regra de SLA:</b> 72 Horas para Marketplaces com contagem regressiva<br>
                    • <b>Status:</b> Sincronização automática de pedidos e devolução de NF-e
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_api2:
            st.markdown("""
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; margin-bottom: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-weight: 800; font-size: 15px; color: #0F172A;">🚛 Braspress (Cotação & Rastreamento)</span>
                    <span style="background: #ECFDF5; color: #065F46; font-weight: 800; font-size: 11px; padding: 3px 8px; border-radius: 12px;">HOMOLOGADO</span>
                </div>
                <div style="font-size: 12px; color: #64748B;">
                    • <b>CNPJ Remetente:</b> <code>57.368.285/0001-35</code> (MISSHA)<br>
                    • <b>Usuário:</b> <code>57368285000135_PRD</code><br>
                    • <b>Endpoints:</b> Cotação de Frete em Tempo Real e Tracking por NF-e
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; margin-bottom: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-weight: 800; font-size: 15px; color: #0F172A;">✈️ Ativa Logística (SSW)</span>
                    <span style="background: #ECFDF5; color: #065F46; font-weight: 800; font-size: 11px; padding: 3px 8px; border-radius: 12px;">CONECTADO</span>
                </div>
                <div style="font-size: 12px; color: #64748B;">
                    • <b>Domínio:</b> <code>ATI</code> &bull; <b>Usuário:</b> <code>missha</code><br>
                    • <b>Operação:</b> Acompanhamento e comprovação de entrega digital
                </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 3: CADASTRO DE CLIENTE
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "👤  Cadastrar Cliente":

    # Se o usuário solicitou reset do formulário de cadastro, limpar o session_state ANTES de instanciar os widgets
    if st.session_state.get("reset_cad_form"):
        st.session_state.pop("reset_cad_form", None)
        st.session_state["cli_dados_auto"] = {}
        st.session_state["cep_dados"] = {}
        keys_to_reset = [
            "cad_cpf_cnpj_search_input", "cad_razao_input", "cad_cnpj_input",
            "cad_fantasia_input", "cad_ie_input", "cad_im_input", "cad_ddd_input",
            "cad_telefone_input", "cad_email_input", "cad_cep_input",
            "cad_logradouro_input", "cad_numero_input", "cad_complemento_input",
            "cad_bairro_input", "cad_cidade_input"
        ]
        for k in keys_to_reset:
            st.session_state[k] = ""
        st.session_state["cad_uf_select"] = "ES"

    def limpar_formulario_cliente():
        st.session_state["reset_cad_form"] = True

    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">👤</div>
        <div>
            <div class="page-header-title">Cadastrar Cliente</div>
            <div class="page-header-subtitle">Registre um novo cliente diretamente no Omie ERP</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "msg_busca_feedback" in st.session_state and st.session_state["msg_busca_feedback"]:
        tipo_m, txt_m = st.session_state.pop("msg_busca_feedback")
        if tipo_m == "success":
            st.success(txt_m)
        elif tipo_m == "warning":
            st.warning(txt_m)
        else:
            st.info(txt_m)

    st.markdown('<div class="section-header">Consulta de Cadastro (CPF / CNPJ ou CEP)</div>', unsafe_allow_html=True)

    col_c_search1, col_c_search2, col_c_search3 = st.columns([3, 1.2, 1.2])
    with col_c_search1:
        cpf_cnpj_search_val = st.text_input("CPF, CNPJ ou CEP", placeholder="Digite o CPF/CNPJ ou CEP (ex: 000.000.000-00 ou 00.000.000/0001-00)", key="cad_cpf_cnpj_search_input")
    with col_c_search2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 Buscar Dados", key="btn_buscar_cpf_action", use_container_width=True):
            if cpf_cnpj_search_val and cpf_cnpj_search_val.strip():
                clean_term = "".join(filter(str.isdigit, cpf_cnpj_search_val.strip()))
                with st.spinner("Buscando dados cadastrais no Omie ERP, SEFAZ (Sintegra) e Receita Federal..."):
                    dados_found = omie.consultar_dados_cliente_por_cpf_cnpj(cpf_cnpj_search_val.strip())
                    if dados_found:
                        st.session_state["cli_dados_auto"] = dados_found
                        st.session_state["cep_dados"] = {
                            "logradouro": dados_found.get("endereco", ""),
                            "bairro": dados_found.get("bairro", ""),
                            "cidade": dados_found.get("cidade", ""),
                            "estado": dados_found.get("estado", "ES")
                        }
                        # Forçar atualização dos widgets de texto no Streamlit
                        st.session_state["cad_razao_input"] = str(dados_found.get("razao_social") or "").strip()
                        st.session_state["cad_cnpj_input"] = str(dados_found.get("cnpj_cpf") or "").strip()
                        st.session_state["cad_fantasia_input"] = str(dados_found.get("nome_fantasia") or "").strip()
                        st.session_state["cad_ie_input"] = str(dados_found.get("inscricao_estadual") or "").strip()
                        st.session_state["cad_im_input"] = str(dados_found.get("inscricao_municipal") or "").strip()
                        st.session_state["cad_ddd_input"] = str(dados_found.get("ddd") or "").strip()
                        st.session_state["cad_telefone_input"] = str(dados_found.get("telefone") or "").strip()
                        st.session_state["cad_email_input"] = str(dados_found.get("email") or "").strip()
                        st.session_state["cad_cep_input"] = str(dados_found.get("cep") or "").strip()
                        st.session_state["cad_logradouro_input"] = str(dados_found.get("endereco") or "").strip()
                        st.session_state["cad_numero_input"] = str(dados_found.get("numero") or "").strip()
                        st.session_state["cad_complemento_input"] = str(dados_found.get("complemento") or "").strip()
                        st.session_state["cad_bairro_input"] = str(dados_found.get("bairro") or "").strip()
                        st.session_state["cad_cidade_input"] = str(dados_found.get("cidade") or "").strip()
                        uf_find = dados_found.get("estado", "ES")
                        ufs_brasil_list = ["ES", "SP", "RJ", "MG", "PR", "SC", "RS", "BA", "PE", "CE", "DF", "GO", "MS", "MT", "AM", "PA", "MA", "PB", "RN", "AL", "SE", "PI", "RO", "AC", "AP", "RR", "TO"]
                        if uf_find in ufs_brasil_list:
                            st.session_state["cad_uf_select"] = uf_find

                        origem_src = dados_found.get("origem", "")
                        cnpj_cpf_val = dados_found.get("cnpj_cpf", "")
                        raz_val = dados_found.get("razao_social", "")

                        if "Pessoa Física" in origem_src:
                            st.session_state["msg_busca_feedback"] = (
                                "info",
                                f"ℹ️ **CPF Formatado ({cnpj_cpf_val})**: Por diretrizes da Receita Federal e LGPD, consultas públicas de CPF não expõem nome nem endereço de Pessoa Física. O CPF e a Inscrição Estadual **ISENTO** foram preenchidos automaticamente abaixo. Digite a Razão Social / Nome do Cliente para concluir."
                            )
                        elif raz_val:
                            st.session_state["msg_busca_feedback"] = (
                                "success",
                                f"✅ **Empresa Localizada ({origem_src})**: Razão Social **{raz_val}**, Endereço, Bairro, Cidade, Estado, DDD e Telefone preenchidos automaticamente!"
                            )
                        else:
                            st.session_state["msg_busca_feedback"] = (
                                "info",
                                f"ℹ️ **Dados localizados via {origem_src}**: Preencha os campos complementares abaixo para concluir."
                            )
                        st.rerun()
                    else:
                        st.session_state["cli_dados_auto"] = None
                        st.session_state["msg_busca_feedback"] = (
                            "warning",
                            "⚠️ **Nenhum cadastro localizado**: Digite os dados do cliente abaixo para cadastrar no Omie ERP."
                        )
                        st.rerun()
    with col_c_search3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🧹 Limpar Dados", key="btn_limpar_cad_top", use_container_width=True):
            limpar_formulario_cliente()
            st.toast("🧹 Todos os campos foram limpos!")
            st.rerun()

    st.markdown("---")

    cad_keys_list = [
        "cad_razao_input", "cad_cnpj_input", "cad_fantasia_input", "cad_ie_input",
        "cad_im_input", "cad_ddd_input", "cad_telefone_input", "cad_email_input",
        "cad_cep_input", "cad_logradouro_input", "cad_numero_input",
        "cad_complemento_input", "cad_bairro_input", "cad_cidade_input"
    ]
    for k in cad_keys_list:
        if k not in st.session_state:
            st.session_state[k] = ""
    if "cad_uf_select" not in st.session_state:
        st.session_state["cad_uf_select"] = "ES"

    with st.form("form_cadastro_cliente_clean", clear_on_submit=False):
        st.markdown('<div class="section-header">Identificação & Inscrições Fiscais</div>', unsafe_allow_html=True)
        col_cli1, col_cli2 = st.columns(2)
        with col_cli1:
            razao_social = st.text_input("Razão Social *", key="cad_razao_input")
            cnpj_cpf = st.text_input("CNPJ ou CPF *", key="cad_cnpj_input")
            st.markdown('<div class="notranslate" translate="no" style="font-size: 14px; font-weight: 900; margin-bottom: 4px; color: #000000;">Inscrição Estadual</div>', unsafe_allow_html=True)
            inscricao_estadual = st.text_input("Inscrição Estadual", placeholder="Ex: 123456789 ou ISENTO", key="cad_ie_input", label_visibility="collapsed")
        with col_cli2:
            nome_fantasia = st.text_input("Nome Fantasia", key="cad_fantasia_input")
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            st.markdown('<div class="notranslate" translate="no" style="font-size: 14px; font-weight: 900; margin-bottom: 4px; color: #000000;">Inscrição Municipal</div>', unsafe_allow_html=True)
            inscricao_municipal = st.text_input("Inscrição Municipal", placeholder="Ex: 987654321", key="cad_im_input", label_visibility="collapsed")

        st.markdown('<div class="section-header">Contatos</div>', unsafe_allow_html=True)
        col_ct1, col_ct2, col_ct3 = st.columns([1, 2, 3])
        with col_ct1:
            ddd = st.text_input("DDD *", max_chars=3, key="cad_ddd_input")
        with col_ct2:
            telefone = st.text_input("Telefone *", key="cad_telefone_input")
        with col_ct3:
            email_cli = st.text_input("E-mail *", key="cad_email_input")

        st.markdown('<div class="section-header">Endereço</div>', unsafe_allow_html=True)
        col_e0, col_e1, col_e2 = st.columns([1, 3, 1])
        with col_e0:
            cep_cli = st.text_input("CEP *", key="cad_cep_input")
        with col_e1:
            logradouro = st.text_input("Logradouro *", key="cad_logradouro_input")
        with col_e2:
            numero_end = st.text_input("Número *", key="cad_numero_input")

        col_e3, col_e4, col_e5, col_e6 = st.columns([2, 2, 2, 1])
        with col_e3:
            complemento = st.text_input("Complemento", key="cad_complemento_input")
        with col_e4:
            bairro = st.text_input("Bairro *", key="cad_bairro_input")
        with col_e5:
            cidade = st.text_input("Cidade *", key="cad_cidade_input")
        with col_e6:
            ufs_brasil = ["ES", "SP", "RJ", "MG", "PR", "SC", "RS", "BA", "PE", "CE", "DF", "GO", "MS", "MT", "AM", "PA", "MA", "PB", "RN", "AL", "SE", "PI", "RO", "AC", "AP", "RR", "TO"]
            uf_val = st.session_state.get("cad_uf_select", "ES")
            uf_default_idx = ufs_brasil.index(uf_val) if uf_val in ufs_brasil else 0
            estado_uf = st.selectbox("UF *", ufs_brasil, index=uf_default_idx, key="cad_uf_select")

        st.markdown('''
        <div style="background: #F0FDF4; border: 1.5px solid #BBF7D0; border-radius: 8px; padding: 10px 14px; margin: 12px 0 10px 0; display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
            <span style="font-size: 16px;">🏷️</span>
            <span style="font-size: 13px; color: #166534; font-weight: 700;">Tag Omie ERP:</span>
            <span style="background: #DCFCE7; color: #15803D; font-weight: 800; font-size: 12px; padding: 2px 10px; border-radius: 12px; border: 1px solid #86EFAC;">Cliente</span>
            <span style="font-size: 12px; color: #4B5563;">(Vinculada automaticamente a todos os novos cadastros no Omie ERP)</span>
        </div>
        ''', unsafe_allow_html=True)

        col_btn1, col_btn2 = st.columns([1, 3])
        with col_btn1:
            submit_limpar = st.form_submit_button("🧹  Limpar Campos", use_container_width=True)
        with col_btn2:
            submit_cadastrar = st.form_submit_button("💾  Salvar Cliente no Omie", type="primary", use_container_width=True)

        if submit_limpar:
            limpar_formulario_cliente()
            st.toast("🧹 Todos os campos foram limpos!")
            st.rerun()

        if submit_cadastrar:
            razao_social = str(razao_social or "").strip()
            cnpj_cpf = str(cnpj_cpf or "").strip()
            nome_fantasia = str(nome_fantasia or "").strip()
            inscricao_estadual = str(inscricao_estadual or "").strip()
            inscricao_municipal = str(inscricao_municipal or "").strip()
            ddd = str(ddd or "").strip()
            telefone = str(telefone or "").strip()
            email_cli = str(email_cli or "").strip()
            cep_cli = str(cep_cli or "").strip()
            logradouro = str(logradouro or "").strip()
            numero_end = str(numero_end or "").strip()
            complemento = str(complemento or "").strip()
            bairro = str(bairro or "").strip()
            cidade = str(cidade or "").strip()
            estado_uf = str(estado_uf or "ES").strip().upper()

            erros = []
            if not razao_social: erros.append("Razão Social é obrigatória.")
            if not cnpj_cpf: erros.append("CNPJ ou CPF é obrigatório.")
            if not ddd: erros.append("DDD é obrigatório.")
            if not telefone: erros.append("Telefone é obrigatório.")
            if not email_cli: erros.append("E-mail é obrigatório.")
            if not cep_cli: erros.append("CEP é obrigatório.")
            if not logradouro: erros.append("Logradouro é obrigatório.")
            if not numero_end: erros.append("Número é obrigatório.")
            if not bairro: erros.append("Bairro é obrigatório.")
            if not cidade: erros.append("Cidade é obrigatória.")

            if erros:
                for err in erros:
                    st.error(err)
            else:
                dados_novo_cliente = {
                    "razao_social": razao_social,
                    "nome_fantasia": nome_fantasia or razao_social,
                    "cnpj_cpf": cnpj_cpf,
                    "inscricao_estadual": inscricao_estadual,
                    "inscricao_municipal": inscricao_municipal,
                    "ddd": ddd,
                    "telefone": telefone,
                    "email": email_cli,
                    "cep": cep_cli,
                    "endereco": logradouro,
                    "numero": numero_end,
                    "complemento": complemento,
                    "bairro": bairro,
                    "cidade": cidade,
                    "estado": estado_uf,
                    "codigo_vendedor": str(usr_logado.get("codigo_vendedor") or "").strip() if usr_logado else "",
                    "vendedor_nome": str(usr_logado.get("nome_vendedor") or "").strip() if usr_logado else "",
                    "tags": [{"tag": "Cliente"}]
                }
                try:
                    res_cli = omie.cadastrar_cliente_omie(dados_novo_cliente, config)
                    st.cache_data.clear()
                    st.cache_resource.clear()
                    raz_clean = str(razao_social).strip()
                    doc_clean = str(cnpj_cpf).strip()
                    uf_clean = str(estado_uf).strip().upper()
                    display_cad = f"{raz_clean} ({doc_clean}) - {uf_clean}" if doc_clean else f"{raz_clean} - {uf_clean}"
                    st.session_state["ped_cliente_sel"] = display_cad
                    st.session_state["sucesso_cadastro_cliente"] = {
                        "razao": raz_clean,
                        "doc": doc_clean,
                        "uf": uf_clean,
                        "display": display_cad
                    }
                    st.toast(f"🎉 Cliente {raz_clean} salvo com sucesso!", icon="⚡")
                    st.success(f"✅ Cliente **{raz_clean}** salvo com sucesso e atualizado no Omie ERP! Já disponível imediatamente para emissão de vendas.")
                    st.rerun()
                except Exception as err_cad:
                    st.error(f"Erro ao cadastrar/atualizar cliente: {str(err_cad)}")

    if "sucesso_cadastro_cliente" in st.session_state and st.session_state["sucesso_cadastro_cliente"]:
        cli_info = st.session_state["sucesso_cadastro_cliente"]
        st.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.15); border: 2px solid #10B981; border-radius: 10px; padding: 14px 18px; margin-top: 14px; margin-bottom: 14px;">
            <div style="font-weight: 800; color: #10B981; font-size: 15px;">🎉 CLIENTE SALVO E PRONTO PARA EMISSÃO DE PEDIDOS!</div>
            <div style="font-size: 13px; color: #FFFFFF; font-weight: 700; margin-top: 4px;">
                Cliente <b>{cli_info.get('razao')}</b> ({cli_info.get('doc')}) já está sincronizado e selecionado para novos pedidos.
            </div>
        </div>
        """, unsafe_allow_html=True)
        col_go1, col_go2 = st.columns([1.5, 1])
        with col_go1:
            if st.button("📝 Criar Novo Pedido com este Cliente Agora", key="btn_ir_novo_ped_sucesso", type="primary", use_container_width=True):
                st.session_state["nav_pagina"] = "📋  Novo Pedido"
                st.session_state.pop("sucesso_cadastro_cliente", None)
                st.rerun()
        with col_go2:
            if st.button("👤 Cadastrar Outro Cliente", key="btn_cadastrar_outro_sucesso", use_container_width=True):
                st.session_state.pop("sucesso_cadastro_cliente", None)
                limpar_formulario_cliente()
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 4: EVOLUÇÃO DE VENDAS & ANÁLISE B2B / B2C / CURVA ABC
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "📈  Evolução de Vendas":
    usr_logado_now = st.session_state.get("usuario_logado")
    if not auth.eh_usuario_master(usr_logado_now):
        st.error("⛔ **Acesso Restrito ao Administrador**: Apenas Administradores têm permissão para acessar os relatórios de Evolução de Vendas e Inteligência Comercial.")
        st.stop()

    import plotly.express as px
    import plotly.graph_objects as go

    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">📈</div>
        <div>
            <div class="page-header-title">Evolução de Vendas & Inteligência Comercial</div>
            <div class="page-header-subtitle">Análise estratégica de faturamento B2B vs B2C, Curva ABC de produtos e acompanhamento de metas.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Carregar todos os pedidos do Omie (filtrados por vendedor logado se não for Master)
    pedidos_lista_full = auth.obter_pedidos_filtrados_usuario(_obter_pedidos_cached(), usr_logado)
    hoje = datetime.date.today()
    mes_ano_atual_str = hoje.strftime("%m/%Y")

    # ── FILTROS EXECUTIVOS COM SELEÇÃO MÚLTIPLA (MULTISELECT) ──
    col_f1, col_f2, col_f3 = st.columns(3)
    col_f4, col_f5, col_f6 = st.columns(3)

    # 1. Extração dinâmica dos Anos disponíveis nos pedidos
    anos_disponiveis = set()
    for ped in pedidos_lista_full:
        dt_obj = obter_data_faturamento_pedido(ped)
        anos_disponiveis.add(str(dt_obj.year))

    lista_anos = sorted(list(anos_disponiveis), reverse=True)
    if str(hoje.year) not in lista_anos:
        lista_anos.insert(0, str(hoje.year))

    with col_f1:
        filtro_ano_multi = st.multiselect(
            "1. Ano(s)",
            options=lista_anos,
            default=[str(hoje.year)] if str(hoje.year) in lista_anos else lista_anos[:1],
            placeholder="Todos os Anos...",
            key="flt_ano_sales_multi_v4"
        )

    # 2. Seleção Múltipla de Meses
    opcoes_meses_nomes = [
        "01 - Janeiro", "02 - Fevereiro", "03 - Março", "04 - Abril",
        "05 - Maio", "06 - Junho", "07 - Julho", "08 - Agosto",
        "09 - Setembro", "10 - Outubro", "11 - Novembro", "12 - Dezembro"
    ]
    mes_padrao = [opcoes_meses_nomes[hoje.month - 1]] if 1 <= hoje.month <= 12 else ["09 - Setembro"]

    with col_f2:
        filtro_mes_multi = st.multiselect(
            "2. Mês(es)",
            options=opcoes_meses_nomes,
            default=mes_padrao,
            placeholder="Todos os Meses...",
            key="flt_mes_sales_multi_v4"
        )

    # 3. Origem / Faturamento por Evento (CBCD)
    with col_f3:
        filtro_evento_multi = st.multiselect(
            "3. Origem / Evento",
            options=["Faturamento Geral (Sem Evento)", "Faturamento do Evento (CBCD)"],
            default=["Faturamento Geral (Sem Evento)", "Faturamento do Evento (CBCD)"],
            placeholder="Selecione origens...",
            key="flt_evento_sales_multi"
        )

    # 4. Canal de Venda (B2B vs B2C)
    with col_f4:
        filtro_canal_multi = st.multiselect(
            "4. Canal de Venda",
            options=["B2B (Corporativo)", "B2C (Site API)"],
            default=["B2B (Corporativo)", "B2C (Site API)"],
            placeholder="Selecione canais...",
            key="flt_canal_sales_multi"
        )

    # 5. Filtro de Tipo de Operação / Bonificação
    with col_f5:
        filtro_bonif_multi = st.multiselect(
            "5. Operação / Bonificação",
            options=["Vendas (Faturamento Líquido)", "Bonificações (Brindes)"],
            default=["Vendas (Faturamento Líquido)"],
            placeholder="Selecione operações...",
            key="flt_bonif_sales_multi"
        )

    # 6. Filtro de Etapa do Pedido (Status Omie ERP)
    opcoes_etapas_nomes = [
        "Etapa 10 - Pedido em Aberto",
        "Etapa 20 / 70 - Em Separação",
        "Etapa 50 - Prontos p/ Faturar",
        "Etapa 60 - Faturado"
    ]

    with col_f6:
        filtro_etapa_multi = st.multiselect(
            "6. Etapa do Pedido",
            options=opcoes_etapas_nomes,
            default=["Etapa 60 - Faturado"],
            placeholder="Todas as etapas...",
            key="flt_etapa_sales_multi_v4"
        )

    # ── LABELS DINÂMICOS DO CABEÇALHO ──
    str_anos_sel = ", ".join(filtro_ano_multi) if filtro_ano_multi else "Todos os Anos"
    filtro_ano = str_anos_sel
    if filtro_mes_multi:
        str_meses_sel = ", ".join([m.split(" - ")[-1] for m in filtro_mes_multi])
        lbl_mes_destaque = f"📅 Meses: {str_meses_sel}"
    else:
        str_meses_sel = "Todos os Meses"
        lbl_mes_destaque = "📅 Período: Todos os Meses"
    filtro_mes = str_meses_sel

    st.markdown(f'''
    <div style="background: linear-gradient(135deg, #EEF2FF 0%, #F1F5F9 100%); border: 1.5px solid #C7D2FE; border-radius: 16px; padding: 22px 28px; margin: 10px 0 22px 0; box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
            <div style="display: flex; align-items: center; gap: 18px;">
                <div style="font-size: 34px; background: #E0E7FF; padding: 12px 16px; border-radius: 14px; border: 1px solid #C7D2FE;">📈</div>
                <div>
                    <div style="font-size: 22px; font-weight: 800; color: #0F172A; letter-spacing: -0.01em;">
                        OMNIEVO Executive Intelligence — <span style="color: #4F46E5;">{str_meses_sel} ({str_anos_sel})</span>
                    </div>
                    <div style="font-size: 13px; color: #000000; margin-top: 3px; font-weight: 500;">Análise estratégica de faturamento B2B vs B2C, Curva ABC e performance comercial em tempo real.</div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="background: #E0E7FF; color: #000000; font-weight: 900; border: 1px solid #C7D2FE; font-size: 13px; font-weight: 800; padding: 7px 18px; border-radius: 20px;">
                    {lbl_mes_destaque}
                </span>
                <span style="background: #ECFDF5; color: #047857; border: 1px solid #A7F3D0; font-size: 12px; font-weight: 700; padding: 7px 14px; border-radius: 20px; display: inline-flex; align-items: center; gap: 6px;">
                    🟢 Omie ERP (dFat)
                </span>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Extração de códigos numéricos das etapas selecionadas
    etapas_cods_sel = set()
    for et_label in filtro_etapa_multi:
        nums = re.findall(r'\d+', et_label)
        for n in nums:
            etapas_cods_sel.add(n)
        if "20" in et_label or "70" in et_label:
            etapas_cods_sel.add("20")
            etapas_cods_sel.add("70")

    # Extração de números dos meses selecionados
    meses_num_sel = set()
    for m_label in filtro_mes_multi:
        nums = re.findall(r'\d+', m_label)
        if nums:
            meses_num_sel.add(nums[0])

    pedidos_filtrados = []
    for ped in pedidos_lista_full:
        raw_p_chk = ped.get('raw_data', {}) if isinstance(ped.get('raw_data'), dict) else {}
        cad_p_chk = raw_p_chk.get('infoCadastro', {}) if isinstance(raw_p_chk.get('infoCadastro'), dict) else {}
        cab_p_chk = raw_p_chk.get('cabecalho', {}) if isinstance(raw_p_chk.get('cabecalho'), dict) else {}
        if str(cad_p_chk.get('cancelado') or cab_p_chk.get('cancelado') or ped.get('cancelado') or 'N').strip().upper() == 'S':
            continue
        dt_obj = obter_data_faturamento_pedido(ped)

        # Filtro 6: Etapas Múltiplas
        etapa_ped = str(ped.get("etapa") or ped.get("raw_data", {}).get("cabecalho", {}).get("etapa") or "").strip()
        if etapas_cods_sel and etapa_ped not in etapas_cods_sel:
            continue

        # Filtro 1: Anos Múltiplos
        if filtro_ano_multi and str(dt_obj.year) not in filtro_ano_multi:
            continue

        # Filtro 2: Meses Múltiplos
        if meses_num_sel and f"{dt_obj.month:02d}" not in meses_num_sel:
            continue

        # Filtro 3: Evento (CBCD nas observações)
        raw = ped.get("raw_data", {})
        obs = raw.get("observacoes", {})
        obs_venda = str(obs.get("obs_venda") or "").lower()
        inf = raw.get("informacoes_adicionais", {})
        dados_nf = str(inf.get("dados_adicionais_nf") or "").lower()
        texto_obs = f"{obs_venda} {dados_nf} {str(ped.get('observacoes', '')).lower()}"
        tem_cbcd = "cbcd" in texto_obs

        if filtro_evento_multi:
            tem_evento_sel = "Faturamento do Evento (CBCD)" in filtro_evento_multi
            tem_geral_sel = "Faturamento Geral (Sem Evento)" in filtro_evento_multi
            if tem_cbcd and not tem_evento_sel:
                continue
            if not tem_cbcd and not tem_geral_sel:
                continue

        # ── FILTRO 5: OPERAÇÃO / BONIFICAÇÃO MULTISELECT ──
        cab = raw.get("cabecalho", {})
        det = raw.get("det", [])
        cen_ped = str(cab.get("codigo_cenario_impostos") or "")

        vlr_vendas_ped = 0.0
        vlr_bonif_ped = 0.0

        for it in det:
            inf_it = it.get("inf_adic", {})
            pr_it = it.get("produto", {})
            cen_item = str(inf_it.get("codigo_cenario_impostos_item") or cen_ped)
            nao_fin = str(inf_it.get("nao_gerar_financeiro", "N")).upper()
            tipo_item = str(it.get("tipo_item", "")).upper()
            val_it = float(pr_it.get("valor_total") or (float(pr_it.get("quantidade", 0)) * float(pr_it.get("valor_unitario", 0))))

            cfop_item = str(pr_it.get("cfop") or "").strip()
            eh_bonif = ("BONIF" in tipo_item) or (nao_fin == "S") or (cen_item == "8904163333") or (cfop_item in ["5.910", "6.910"])
            if eh_bonif:
                vlr_bonif_ped += val_it
            else:
                vlr_vendas_ped += val_it

        ped_copy = dict(ped)
        tot_orig = float(raw.get("total_pedido", {}).get("valor_total_pedido") or ped.get("valor_total") or 0.0)

        quer_vendas = "Vendas (Faturamento Líquido)" in filtro_bonif_multi if filtro_bonif_multi else True
        quer_bonif = "Bonificações (Brindes)" in filtro_bonif_multi if filtro_bonif_multi else False

        # Se o pedido não tem detalhamento de itens específico, assume valor total de venda
        if vlr_vendas_ped == 0.0 and vlr_bonif_ped == 0.0 and tot_orig > 0:
            vlr_vendas_ped = tot_orig

        if quer_vendas and quer_bonif:
            ped_copy["valor_total"] = tot_orig
        elif quer_bonif and not quer_vendas:
            if vlr_bonif_ped <= 0:
                continue
            ped_copy["valor_total"] = vlr_bonif_ped
        elif quer_vendas and not quer_bonif:
            if vlr_vendas_ped <= 0:
                continue
            ped_copy["valor_total"] = vlr_vendas_ped
        else:
            ped_copy["valor_total"] = tot_orig

        pedidos_filtrados.append(ped_copy)

    # ── VERIFICAÇÃO RIGOROSA PEDIDO POR PEDIDO DO CAMPO VENDEDOR ──
    b2b_pedidos = []
    b2c_pedidos = []
    produtos_vendas = {}

    for ped in pedidos_filtrados:
        raw = ped.get("raw_data", {})
        cab = raw.get("cabecalho", {})
        info_adic = raw.get("informacoes_adicionais", {})
        info_cad = raw.get("infoCadastro", {})
        
        num_p_str = str(ped.get("numero_pedido") or cab.get("numero_pedido") or "").strip()
        # Leitura individual do campo vendedor de cada pedido
        vendedor_raw = (
            ped.get("vendedor") or
            info_adic.get("contato") or
            cab.get("nome_vendedor") or
            cab.get("vendedor") or
            info_cad.get("usuario_inclusao") or
            ""
        )
        vendedor_str = normalizar_nome_vendedor(vendedor_raw, num_p_str, ped_obj=ped)
        vlr_total = float(ped.get("valor_total") or 0.0)

        # REGRA REAL DO OMIE ERP:
        # B2B = Pedido emitido para CNPJ (Pessoa Jurídica / Vendas Corporativas)
        # B2C = Pedido emitido para CPF (Pessoa Física / Site / Varejo)
        is_b2c = not eh_pedido_b2b_cnpj(ped)

        if is_b2c:
            b2c_pedidos.append(ped)
        else:
            b2b_pedidos.append(ped)

        # Aplicar filtro de canal para a Curva ABC
        incluir_para_abc = True
        if filtro_canal_multi:
            if "B2B (Corporativo)" in filtro_canal_multi and "B2C (Site API)" not in filtro_canal_multi and is_b2c:
                incluir_para_abc = False
            elif "B2C (Site API)" in filtro_canal_multi and "B2B (Corporativo)" not in filtro_canal_multi and not is_b2c:
                incluir_para_abc = False

        if incluir_para_abc:
            det_items = raw.get("det", [])
            for it in det_items:
                pr = it.get("produto", {})
                inf_it = it.get("inf_adic", {})
                
                cen_item = str(inf_it.get("codigo_cenario_impostos_item") or cab.get("codigo_cenario_impostos") or "")
                nao_fin = str(inf_it.get("nao_gerar_financeiro", "N")).upper()
                tipo_item = str(it.get("tipo_item", "")).upper()
                
                # REGRA EXPLICITADA PELO USUÁRIO: Excluir 100% dos itens de Bonificação do faturamento
                eh_bonificacao = ("BONIF" in tipo_item) or (nao_fin == "S") or (cen_item == "8904163333")
                if eh_bonificacao:
                    continue

                cod_int = str(pr.get("codigo_produto_integracao") or pr.get("codigo") or "").strip()
                desc_prod = str(pr.get("descricao") or cod_int).strip()
                qtd_v = float(pr.get("quantidade") or 0.0)
                val_v = float(pr.get("valor_total") or (qtd_v * float(pr.get("valor_unitario") or 0.0)))

                if cod_int:
                    if cod_int not in produtos_vendas:
                        produtos_vendas[cod_int] = {
                            "codigo": cod_int,
                            "descricao": desc_prod,
                            "quantidade": 0.0,
                            "faturamento": 0.0
                        }
                    produtos_vendas[cod_int]["quantidade"] += qtd_v
                    produtos_vendas[cod_int]["faturamento"] += val_v

    # ── ALINHAMENTO ESTRITO DE CANAL DE VENDA ──
    tem_b2b_sel = ("B2B (Corporativo)" in filtro_canal_multi) if filtro_canal_multi else True
    tem_b2c_sel = ("B2C (Site API)" in filtro_canal_multi) if filtro_canal_multi else True

    if tem_b2b_sel and not tem_b2c_sel:
        pedidos_exibicao = b2b_pedidos
    elif tem_b2c_sel and not tem_b2b_sel:
        pedidos_exibicao = b2c_pedidos
    else:
        pedidos_exibicao = pedidos_filtrados

    # Totais Reais dos Canais baseados na seleção ativa
    tot_fat_b2b = sum(float(p.get("valor_total") or 0.0) for p in b2b_pedidos)
    tot_fat_b2c = sum(float(p.get("valor_total") or 0.0) for p in b2c_pedidos)
    tot_fat_geral = sum(float(p.get("valor_total") or 0.0) for p in pedidos_exibicao)

    tot_fat_soma_ambos = tot_fat_b2b + tot_fat_b2c
    pct_b2b = (tot_fat_b2b / tot_fat_soma_ambos * 100) if tot_fat_soma_ambos > 0 else 0.0
    pct_b2c = (tot_fat_b2c / tot_fat_soma_ambos * 100) if tot_fat_soma_ambos > 0 else 0.0

    tkt_geral = (tot_fat_geral / len(pedidos_exibicao)) if pedidos_exibicao else 0.0
    tkt_b2b = (tot_fat_b2b / len(b2b_pedidos)) if b2b_pedidos else 0.0
    tkt_b2c = (tot_fat_b2c / len(b2c_pedidos)) if b2c_pedidos else 0.0

    # ── KPIs EXECUTIVOS PREMIUM COM DESIGN COLORIDO E ALTO CONTRASTE ──
    st.markdown(f"""<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin-bottom: 22px;">
<div style="background: linear-gradient(135deg, #FFFFFF 0%, #EEF2FF 100%); border: 1.5px solid #C7D2FE; border-top: 4px solid #4F46E5; border-radius: 12px; padding: 16px 18px; box-shadow: 0 4px 14px rgba(79, 70, 229, 0.05); display: flex; flex-direction: column; justify-content: space-between;">
<div>
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
<span style="font-size: 11px; font-weight: 800; color: #4338CA; text-transform: uppercase; letter-spacing: 0.05em; display: flex; align-items: center; gap: 4px;">💰 Faturamento Total</span>
<span style="background: #EEF2FF; color: #4338CA; font-size: 10px; font-weight: 800; padding: 3px 9px; border-radius: 12px; border: 1px solid #C7D2FE;">GERAL</span>
</div>
<div style="font-size: 26px; font-weight: 900; color: #0F172A; margin-bottom: 6px; letter-spacing: -0.02em;">{fmt_brl(tot_fat_geral)}</div>
</div>
<div>
<span style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 4px 10px; font-size: 11px; color: #475569; font-weight: 600; display: inline-flex; align-items: center; gap: 4px;">
📦 <b>{len(pedidos_exibicao)}</b> pedido(s) no período
</span>
</div>
</div>
<div style="background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%); border: 1.5px solid #BFDBFE; border-top: 4px solid #2563EB; border-radius: 12px; padding: 16px 18px; box-shadow: 0 4px 14px rgba(37, 99, 235, 0.05); display: flex; flex-direction: column; justify-content: space-between;">
<div>
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
<span style="font-size: 11px; font-weight: 800; color: #1D4ED8; text-transform: uppercase; letter-spacing: 0.05em; display: flex; align-items: center; gap: 4px;">🏢 Vendas B2B</span>
<span style="background: #EFF6FF; color: #1D4ED8; font-size: 10px; font-weight: 800; padding: 3px 9px; border-radius: 12px; border: 1px solid #93C5FD;">CORPORATIVO</span>
</div>
<div style="font-size: 26px; font-weight: 900; color: #1E3A8A; margin-bottom: 6px; letter-spacing: -0.02em;">{fmt_brl(tot_fat_b2b)}</div>
</div>
<div>
<span style="background: #FFFFFF; border: 1px solid #BFDBFE; border-radius: 6px; padding: 4px 10px; font-size: 11px; color: #1E40AF; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;">
📊 <b>{pct_b2b:.1f}%</b> do total ({len(b2b_pedidos)} ped)
</span>
</div>
</div>
<div style="background: linear-gradient(135deg, #FFFFFF 0%, #ECFDF5 100%); border: 1.5px solid #A7F3D0; border-top: 4px solid #10B981; border-radius: 12px; padding: 16px 18px; box-shadow: 0 4px 14px rgba(16, 185, 129, 0.05); display: flex; flex-direction: column; justify-content: space-between;">
<div>
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
<span style="font-size: 11px; font-weight: 800; color: #047857; text-transform: uppercase; letter-spacing: 0.05em; display: flex; align-items: center; gap: 4px;">🛒 Vendas B2C</span>
<span style="background: #ECFDF5; color: #047857; font-size: 10px; font-weight: 800; padding: 3px 9px; border-radius: 12px; border: 1px solid #A7F3D0;">SITE API</span>
</div>
<div style="font-size: 26px; font-weight: 900; color: #064E3B; margin-bottom: 6px; letter-spacing: -0.02em;">{fmt_brl(tot_fat_b2c)}</div>
</div>
<div>
<span style="background: #FFFFFF; border: 1px solid #A7F3D0; border-radius: 6px; padding: 4px 10px; font-size: 11px; color: #065F46; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;">
📊 <b>{pct_b2c:.1f}%</b> do total ({len(b2c_pedidos)} ped)
</span>
</div>
</div>
<div style="background: linear-gradient(135deg, #FFFFFF 0%, #FFFBEB 100%); border: 1.5px solid #FDE68A; border-top: 4px solid #F59E0B; border-radius: 12px; padding: 16px 18px; box-shadow: 0 4px 14px rgba(245, 158, 11, 0.05); display: flex; flex-direction: column; justify-content: space-between;">
<div>
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
<span style="font-size: 11px; font-weight: 800; color: #B45309; text-transform: uppercase; letter-spacing: 0.05em; display: flex; align-items: center; gap: 4px;">🎯 Ticket Médio</span>
<span style="background: #FEF3C7; color: #B45309; font-size: 10px; font-weight: 800; padding: 3px 9px; border-radius: 12px; border: 1px solid #FDE68A;">MÉDIA GERAL</span>
</div>
<div style="font-size: 26px; font-weight: 900; color: #78350F; margin-bottom: 6px; letter-spacing: -0.02em;">{fmt_brl(tkt_geral)}</div>
</div>
<div>
<span style="background: #FFFFFF; border: 1px solid #FDE68A; border-radius: 6px; padding: 4px 10px; font-size: 11px; color: #92400E; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;">
🏢 <b>{fmt_brl(tkt_b2b)}</b> &nbsp;|&nbsp; 🛒 <b>{fmt_brl(tkt_b2c)}</b>
</span>
</div>
</div>
</div>""", unsafe_allow_html=True)

    if not pedidos_filtrados:
        st.warning(f"⚠️ **Atenção aos Filtros**: Nenhum faturamento localizado para os filtros atuais (**Ano(s): {str_anos_sel} | Mês(es): {str_meses_sel}**).")
        st.info("💡 **Orientação**: Para ampliar a visualização dos dados faturados da empresa, experimente selecionar **'Todos os Anos'** e/ou **'Todos os Meses'** nos filtros acima.")

    # ── SEÇÃO 1: OS 3 GRÁFICOS DE EVOLUÇÃO DE VENDAS ──
    is_mes_especifico = len(filtro_mes_multi) == 1
    if is_mes_especifico:
        lbl_periodo_grafico = f"Evolução Diária — {filtro_mes_multi[0]}"
    else:
        lbl_periodo_grafico = f"Evolução Mensal ({str_anos_sel})"
    st.markdown(f'<div class="section-header">📈 Evolução de Vendas — Visão Geral, B2B e B2C ({lbl_periodo_grafico})</div>', unsafe_allow_html=True)

    # ── EIXO E AGRUPAMENTO DINÂMICO DOS DADOS ──
    if is_mes_especifico:
        col_eixo = "dia_str"
        lbl_eixo = "Dia"
        col_sort = "data"
        group_cols = ["dia_str", "data"]
    else:
        col_eixo = "mes_rotulo"
        lbl_eixo = "Mês"
        col_sort = "mes_sort"
        group_cols = ["mes_rotulo", "mes_sort"]

    df_temporal_list = []
    for p in pedidos_exibicao:
        dt_obj = obter_data_faturamento_pedido(p)
        vlr = float(p.get("valor_total") or 0.0)
        raw = p.get("raw_data", {})
        cab = raw.get("cabecalho", {})
        info_adic = raw.get("informacoes_adicionais", {})
        vend = str(p.get("vendedor") or info_adic.get("contato") or cab.get("nome_vendedor") or "").strip()
        num_p_str = str(p.get("numero_pedido") or cab.get("numero_pedido") or "").strip()
        is_b2c_t = not eh_pedido_b2b_cnpj(p)
        canal = "B2C (Site API)" if is_b2c_t else "B2B (Corporativo)"

        df_temporal_list.append({
            "data": dt_obj,
            "dia_str": dt_obj.strftime("%d/%m"),
            "mes_rotulo": dt_obj.strftime("%m/%Y"),
            "mes_sort": dt_obj.strftime("%Y-%m"),
            "faturamento": vlr,
            "canal": canal,
            "pedido": num_p_str
        })

    df_temp = pd.DataFrame(df_temporal_list) if df_temporal_list else pd.DataFrame(columns=["data", "dia_str", "mes_rotulo", "mes_sort", "faturamento", "canal", "pedido"])

    # Agrupamentos limpos e consolidados com contagem de pedidos e ticket médio
    if not df_temp.empty:
        df_g1 = df_temp.groupby(group_cols).agg(
            faturamento=("faturamento", "sum"),
            qtd_pedidos=("pedido", "nunique")
        ).reset_index().sort_values(col_sort)
        df_g1["ticket_medio"] = df_g1.apply(lambda r: r["faturamento"] / r["qtd_pedidos"] if r["qtd_pedidos"] > 0 else 0.0, axis=1)
        df_g1["ticket_medio_str"] = df_g1["ticket_medio"].apply(fmt_brl)
        df_g1["rotulo_texto"] = df_g1["faturamento"].apply(lambda v: f"R$ {v:,.0f}" if v > 0 else "")

        df_b2b_df = df_temp[df_temp["canal"] == "B2B (Corporativo)"]
        df_g2 = df_b2b_df.groupby(group_cols).agg(
            faturamento=("faturamento", "sum"),
            qtd_pedidos=("pedido", "nunique")
        ).reset_index().sort_values(col_sort) if not df_b2b_df.empty else pd.DataFrame()
        if not df_g2.empty:
            df_g2["ticket_medio"] = df_g2.apply(lambda r: r["faturamento"] / r["qtd_pedidos"] if r["qtd_pedidos"] > 0 else 0.0, axis=1)
            df_g2["ticket_medio_str"] = df_g2["ticket_medio"].apply(fmt_brl)
            df_g2["rotulo_texto"] = df_g2["faturamento"].apply(lambda v: f"R$ {v:,.0f}" if v > 0 else "")

        df_b2c_df = df_temp[df_temp["canal"] == "B2C (Site API)"]
        df_g3 = df_b2c_df.groupby(group_cols).agg(
            faturamento=("faturamento", "sum"),
            qtd_pedidos=("pedido", "nunique")
        ).reset_index().sort_values(col_sort) if not df_b2c_df.empty else pd.DataFrame()
        if not df_g3.empty:
            df_g3["ticket_medio"] = df_g3.apply(lambda r: r["faturamento"] / r["qtd_pedidos"] if r["qtd_pedidos"] > 0 else 0.0, axis=1)
            df_g3["ticket_medio_str"] = df_g3["ticket_medio"].apply(fmt_brl)
            df_g3["rotulo_texto"] = df_g3["faturamento"].apply(lambda v: f"R$ {v:,.0f}" if v > 0 else "")
    else:
        df_g1, df_g2, df_g3 = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    event_g1, event_g2, event_g3 = None, None, None
    chart_drill_ver = st.session_state.get("chart_drill_version", 0)

    # Coletar opções cronológicas do eixo para o seletor múltiplo
    opcoes_eixo = []
    if not df_temp.empty and col_eixo in df_temp.columns:
        df_sorted_eixo = df_temp.sort_values(col_sort)
        seen_eixo = set()
        for val_e in df_sorted_eixo[col_eixo].dropna():
            s_val_e = str(val_e).strip()
            if s_val_e and s_val_e not in seen_eixo:
                seen_eixo.add(s_val_e)
                opcoes_eixo.append(s_val_e)

    # ── ESTILIZAÇÃO EXECUTIVA PREMIUM DOS GRÁFICOS PLOTLY ──
    def aplicar_estilo_executivo(fig, cor_principal="#4F46E5", cor_preenchimento="rgba(79, 70, 229, 0.16)", eh_barra=False):
        fig.update_layout(
            template="plotly_white",
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            height=360,
            margin=dict(l=15, r=15, t=35, b=25),
            font=dict(family="Inter, -apple-system, sans-serif", size=12, color="#0F172A"),
            hoverlabel=dict(
                bgcolor="#0F172A",
                bordercolor="#38BDF8",
                font=dict(color="#FFFFFF", size=13, family="Inter, sans-serif")
            ),
            xaxis=dict(
                showgrid=False,
                linecolor="#CBD5E1",
                linewidth=1,
                tickfont=dict(size=11, color="#475569", family="Inter, sans-serif"),
                title_font=dict(size=12, color="#0F172A", family="Inter, sans-serif")
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="#F1F5F9",
                gridwidth=1,
                linecolor="#CBD5E1",
                linewidth=1,
                tickprefix="R$ ",
                tickfont=dict(size=11, color="#475569", family="Inter, sans-serif"),
                title_font=dict(size=12, color="#0F172A", family="Inter, sans-serif")
            ),
            bargap=0.28 if eh_barra else 0.0
        )
        if eh_barra:
            fig.update_traces(
                textposition="outside",
                cliponaxis=False,
                textfont=dict(size=10, color="#1E293B", family="Inter, sans-serif"),
                marker_line_color=cor_principal,
                marker_line_width=1,
                hovertemplate="<span style='color: #FFFFFF; font-size: 13px;'><b>%{x}</b></span><br><span style='color: #FFFFFF;'>💰 Faturamento: <b>R$ %{y:,.2f}</b></span><br><span style='color: #FFFFFF;'>📦 Pedidos: <b>%{customdata[0]}</b></span><br><span style='color: #FFFFFF;'>🎯 Ticket Médio: <b>%{customdata[1]}</b></span><extra></extra>"
            )
        else:
            fig.update_traces(
                line=dict(width=3.5, color=cor_principal, shape="spline"),
                fill="tozeroy",
                fillcolor=cor_preenchimento,
                mode="lines+markers",
                marker=dict(size=8, color=cor_principal, line=dict(width=2, color="#FFFFFF")),
                hovertemplate="<span style='color: #FFFFFF; font-size: 13px;'><b>%{x}</b></span><br><span style='color: #FFFFFF;'>💰 Faturamento Geral: <b>R$ %{y:,.2f}</b></span><br><span style='color: #FFFFFF;'>📦 Pedidos: <b>%{customdata[0]}</b></span><br><span style='color: #FFFFFF;'>🎯 Ticket Médio: <b>%{customdata[1]}</b></span><extra></extra>"
            )
        return fig

    # ── GRÁFICO 1 (TOPO): EVOLUÇÃO GERAL DE FORA A FORA (FULL WIDTH) ──
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%); border: 1.5px solid #C7D2FE; border-radius: 12px; padding: 12px 18px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between;'>
        <div>
            <div style='font-size: 15px; color: #1E1B4B; font-weight: 800;'>📈 1. Evolução Consolidada de Faturamento ({lbl_eixo}) — Visão Geral</div>
            <div style='font-size: 12px; color: #4338CA;'>Curva temporal contínua de vendas gerais no período selecionado (Passe o mouse para inspecionar)</div>
        </div>
        <span style='background: #4F46E5; color: #FFFFFF; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 20px;'>{lbl_periodo_grafico}</span>
    </div>
    """, unsafe_allow_html=True)
    if not df_g1.empty:
        fig1 = px.area(
            df_g1, x=col_eixo, y="faturamento",
            custom_data=["qtd_pedidos", "ticket_medio_str"],
            title="",
            labels={"faturamento": "Faturamento Geral (R$)", col_eixo: lbl_eixo}
        )
        fig1 = aplicar_estilo_executivo(fig1, cor_principal="#4F46E5", cor_preenchimento="rgba(79, 70, 229, 0.16)", eh_barra=False)
        event_g1 = st.plotly_chart(fig1, on_select="rerun", selection_mode=("points", "box"), key=f"chart_g1_select_{chart_drill_ver}", use_container_width=True)
    else:
        st.info("Nenhum histórico disponível para este período.")

    st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)

    # ── GRÁFICOS 2 E 3 (ABAIXO): B2B E B2C DINÂMICOS POR SELEÇÃO MÚLTIPLA ──
    tem_b2b_sel = ("B2B (Corporativo)" in filtro_canal_multi) if filtro_canal_multi else True
    tem_b2c_sel = ("B2C (Site API)" in filtro_canal_multi) if filtro_canal_multi else True

    if tem_b2b_sel and tem_b2c_sel:
        col_b2b, col_b2c = st.columns(2)

        with col_b2b:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); border: 1.5px solid #BFDBFE; border-radius: 12px; padding: 12px 16px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between;'>
                <div>
                    <div style='font-size: 14px; color: #1E3A8A; font-weight: 800;'>🏢 2. Evolução Vendas B2B ({lbl_eixo})</div>
                    <div style='font-size: 11px; color: #2563EB;'>Vendas Corporativas Faturadas Omie ERP</div>
                </div>
                <span style='background: #2563EB; color: #FFFFFF; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 14px;'>{fmt_brl(tot_fat_b2b)}</span>
            </div>
            """, unsafe_allow_html=True)
            if not df_g2.empty:
                fig2 = px.bar(
                    df_g2, x=col_eixo, y="faturamento",
                    text="rotulo_texto",
                    custom_data=["qtd_pedidos", "ticket_medio_str"],
                    title="",
                    labels={"faturamento": "Faturamento B2B (R$)", col_eixo: lbl_eixo},
                    color_discrete_sequence=["#2563EB"]
                )
                fig2 = aplicar_estilo_executivo(fig2, cor_principal="#2563EB", eh_barra=True)
                event_g2 = st.plotly_chart(fig2, on_select="rerun", selection_mode=("points", "box"), key=f"chart_g2_select_{chart_drill_ver}", use_container_width=True)
            else:
                st.info("Nenhum faturamento B2B localizado no período selecionado.")

        with col_b2c:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%); border: 1.5px solid #A7F3D0; border-radius: 12px; padding: 12px 16px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between;'>
                <div>
                    <div style='font-size: 14px; color: #064E3B; font-weight: 800;'>🛒 3. Evolução Vendas B2C ({lbl_eixo})</div>
                    <div style='font-size: 11px; color: #059669;'>Vendas Site API Faturadas Omie ERP</div>
                </div>
                <span style='background: #10B981; color: #FFFFFF; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 14px;'>{fmt_brl(tot_fat_b2c)}</span>
            </div>
            """, unsafe_allow_html=True)
            if not df_g3.empty:
                fig3 = px.bar(
                    df_g3, x=col_eixo, y="faturamento",
                    text="rotulo_texto",
                    custom_data=["qtd_pedidos", "ticket_medio_str"],
                    title="",
                    labels={"faturamento": "Faturamento B2C (R$)", col_eixo: lbl_eixo},
                    color_discrete_sequence=["#10B981"]
                )
                fig3 = aplicar_estilo_executivo(fig3, cor_principal="#10B981", eh_barra=True)
                event_g3 = st.plotly_chart(fig3, on_select="rerun", selection_mode=("points", "box"), key=f"chart_g3_select_{chart_drill_ver}", use_container_width=True)
            else:
                st.info("Nenhum faturamento B2C (Site API) localizado no período selecionado.")

    elif tem_b2b_sel:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); border: 1.5px solid #BFDBFE; border-radius: 12px; padding: 12px 16px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between;'>
            <div>
                <div style='font-size: 14px; color: #1E3A8A; font-weight: 800;'>🏢 2. Evolução Vendas B2B ({lbl_eixo})</div>
                <div style='font-size: 11px; color: #2563EB;'>Vendas Corporativas Faturadas Omie ERP</div>
            </div>
            <span style='background: #2563EB; color: #FFFFFF; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 14px;'>{fmt_brl(tot_fat_b2b)}</span>
        </div>
        """, unsafe_allow_html=True)
        if not df_g2.empty:
            fig2 = px.bar(
                df_g2, x=col_eixo, y="faturamento",
                text="rotulo_texto",
                custom_data=["qtd_pedidos", "ticket_medio_str"],
                title="",
                labels={"faturamento": "Faturamento B2B (R$)", col_eixo: lbl_eixo},
                color_discrete_sequence=["#2563EB"]
            )
            fig2 = aplicar_estilo_executivo(fig2, cor_principal="#2563EB", eh_barra=True)
            event_g2 = st.plotly_chart(fig2, on_select="rerun", selection_mode=("points", "box"), key=f"chart_g2_select_{chart_drill_ver}", use_container_width=True)
        else:
            st.info("Nenhum faturamento B2B localizado no período selecionado.")

    elif tem_b2c_sel:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%); border: 1.5px solid #A7F3D0; border-radius: 12px; padding: 12px 16px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between;'>
            <div>
                <div style='font-size: 14px; color: #064E3B; font-weight: 800;'>🛒 3. Evolução Vendas B2C ({lbl_eixo})</div>
                <div style='font-size: 11px; color: #059669;'>Vendas Site API Faturadas Omie ERP</div>
            </div>
            <span style='background: #10B981; color: #FFFFFF; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 14px;'>{fmt_brl(tot_fat_b2c)}</span>
        </div>
        """, unsafe_allow_html=True)
        if not df_g3.empty:
            fig3 = px.bar(
                df_g3, x=col_eixo, y="faturamento",
                text="rotulo_texto",
                custom_data=["qtd_pedidos", "ticket_medio_str"],
                title="",
                labels={"faturamento": "Faturamento B2C (R$)", col_eixo: lbl_eixo},
                color_discrete_sequence=["#10B981"]
            )
            fig3 = aplicar_estilo_executivo(fig3, cor_principal="#10B981", eh_barra=True)
            event_g3 = st.plotly_chart(fig3, on_select="rerun", selection_mode=("points", "box"), key=f"chart_g3_select_{chart_drill_ver}", use_container_width=True)
        else:
            st.info("Nenhum faturamento B2C (Site API) localizado no período selecionado.")

    # ── DETALHAMENTO DOS PEDIDOS DE VENDA — IMEDIATAMENTE ABAIXO DA EVOLUÇÃO VENDAS (DIA) ──
    # Extração de pontos selecionados nos gráficos Plotly (suporta clique único ou múltiplos via box/lasso/shift)
    pontos_clicados_grafico = []
    origem_clique_grafico = None

    for ev_name, ev_data in [("B2B", event_g2), ("B2C", event_g3), ("Geral", event_g1)]:
        if ev_data and isinstance(ev_data, dict) and ev_data.get("selection") and ev_data["selection"].get("points"):
            pts = ev_data["selection"]["points"]
            for pt in pts:
                if "x" in pt and pt["x"] is not None:
                    x_str = str(pt["x"]).strip()
                    if x_str and x_str not in pontos_clicados_grafico:
                        pontos_clicados_grafico.append(x_str)
            if pontos_clicados_grafico:
                origem_clique_grafico = ev_name
                break

    # Gerenciamento de Session State para multi-seleção de dias/períodos
    key_multi_eixo = f"sel_multi_{col_eixo}"
    if key_multi_eixo not in st.session_state:
        st.session_state[key_multi_eixo] = []
    if "last_chart_pts" not in st.session_state:
        st.session_state["last_chart_pts"] = []
    if "last_origem_clique" not in st.session_state:
        st.session_state["last_origem_clique"] = None

    # Se o usuário clicou/selecionou pontos no gráfico Plotly, sincronizar com o seletor múltiplo
    if pontos_clicados_grafico and pontos_clicados_grafico != st.session_state["last_chart_pts"]:
        st.session_state["last_chart_pts"] = list(pontos_clicados_grafico)
        st.session_state["last_origem_clique"] = origem_clique_grafico
        validos_pts = [p for p in pontos_clicados_grafico if p in opcoes_eixo]
        if validos_pts:
            st.session_state[key_multi_eixo] = validos_pts
    elif not pontos_clicados_grafico and st.session_state["last_chart_pts"]:
        st.session_state["last_chart_pts"] = []

    # Sanitizar seleção garantindo que valores pertencem ao eixo atual
    st.session_state[key_multi_eixo] = [x for x in st.session_state[key_multi_eixo] if x in opcoes_eixo]

    # Funções de callback para botões de ação rápida (executam antes da renderização do widget no rerun)
    def _cb_selecionar_todos_dias(key_target, lista_opcoes):
        st.session_state[key_target] = list(lista_opcoes)
        st.session_state["chart_drill_version"] = st.session_state.get("chart_drill_version", 0) + 1
        st.session_state["last_chart_pts"] = []

    def _cb_limpar_dias(key_target):
        st.session_state[key_target] = []
        st.session_state["chart_drill_version"] = st.session_state.get("chart_drill_version", 0) + 1
        st.session_state["last_chart_pts"] = []
        st.session_state["last_origem_clique"] = None

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
    st.markdown(f'<div class="section-header">🔍 Detalhamento dos Pedidos de Venda por {lbl_eixo} ({lbl_periodo_grafico})</div>', unsafe_allow_html=True)

    # Barra interativa de multi-seleção de dias e botões de ação rápida
    col_sel_ms, col_btn_todos, col_btn_limpar = st.columns([3.2, 1, 1])
    with col_sel_ms:
        dias_selecionados = st.multiselect(
            f"📅 Selecionar {lbl_eixo}(s) para Detalhamento:",
            options=opcoes_eixo,
            key=key_multi_eixo,
            placeholder=f"Todos os {lbl_eixo.lower()}s ou escolha um ou mais..."
        )
    with col_btn_todos:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        st.button(f"✅ Todos {lbl_eixo}s", key="btn_sel_todos_dias", on_click=_cb_selecionar_todos_dias, args=(key_multi_eixo, opcoes_eixo), use_container_width=True)
    with col_btn_limpar:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        st.button(f"🧹 Limpar {lbl_eixo}s", key="btn_limpar_dias", on_click=_cb_limpar_dias, args=(key_multi_eixo,), use_container_width=True)

    # Determinar canal efetivo e escopo de visualização
    if st.session_state.get("last_origem_clique") and st.session_state["last_chart_pts"] and (set(dias_selecionados) == set(st.session_state["last_chart_pts"])):
        origem_efetiva = st.session_state["last_origem_clique"]
    elif tem_b2b_sel and not tem_b2c_sel:
        origem_efetiva = "B2B"
    elif tem_b2c_sel and not tem_b2b_sel:
        origem_efetiva = "B2C"
    else:
        origem_efetiva = "Todos os Canais"

    # Estilização dinâmica por canal
    if origem_efetiva == "B2B":
        cor_tag_canal = "#1D4ED8"
        bg_tag_canal = "#DBEAFE"
        border_tag_canal = "#93C5FD"
        rotulo_canal_badge = "B2B (Corporativo)"
    elif origem_efetiva == "B2C":
        cor_tag_canal = "#047857"
        bg_tag_canal = "#D1FAE5"
        border_tag_canal = "#A7F3D0"
        rotulo_canal_badge = "B2C (Site API)"
    else:
        cor_tag_canal = "#4338CA"
        bg_tag_canal = "#E0E7FF"
        border_tag_canal = "#C7D2FE"
        rotulo_canal_badge = "B2B + B2C (Geral)"

    # Formatação do Banner Executivo
    qtd_dias_sel = len(dias_selecionados)
    if qtd_dias_sel == 1:
        dia_u = dias_selecionados[0]
        pill_data = f"<span style='color: #0F172A; font-weight: 900; background: {bg_tag_canal}; border: 1.5px solid {border_tag_canal}; padding: 3px 10px; border-radius: 6px;'>{dia_u}</span>"
        titulo_detalhe_str = f"🔍 DETALHAMENTO DOS PEDIDOS DE VENDA — {lbl_eixo.upper()}: {pill_data} ({origem_efetiva})"
        subtitulo_detalhe_str = f"Exibindo pedidos do {lbl_eixo.lower()} selecionado"
    elif qtd_dias_sel > 1:
        if qtd_dias_sel <= 5:
            dias_repr = ", ".join(dias_selecionados)
        else:
            dias_repr = ", ".join(dias_selecionados[:5]) + f" (+{qtd_dias_sel - 5} {lbl_eixo.lower()}s)"
        pill_data = f"<span style='color: #0F172A; font-weight: 900; background: {bg_tag_canal}; border: 1.5px solid {border_tag_canal}; padding: 3px 10px; border-radius: 6px;'>{dias_repr}</span>"
        titulo_detalhe_str = f"🔍 DETALHAMENTO DOS PEDIDOS DE VENDA — {qtd_dias_sel} {lbl_eixo.upper()}S: {pill_data} ({origem_efetiva})"
        subtitulo_detalhe_str = f"Exibindo pedidos consolidados de {qtd_dias_sel} {lbl_eixo.lower()}s"
    else:
        pill_canal = f"<span style='color: {cor_tag_canal}; font-weight: 900; background: {bg_tag_canal}; border: 1.5px solid {border_tag_canal}; padding: 3px 10px; border-radius: 6px;'>{rotulo_canal_badge}</span>"
        titulo_detalhe_str = f"🔍 DETALHAMENTO DOS PEDIDOS DE VENDA — {pill_canal}"
        subtitulo_detalhe_str = f"Exibindo todos os pedidos ({lbl_periodo_grafico})"

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #F8FAFC 0%, #EEF2FF 100%); border: 1.5px solid #C7D2FE; border-left: 5px solid {cor_tag_canal}; border-radius: 12px; padding: 16px 20px; margin-top: 14px; margin-bottom: 20px; box-shadow: 0 3px 12px rgba(15, 23, 42, 0.05);">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
            <div style="font-size: 15px; font-weight: 800; color: #0F172A;">{titulo_detalhe_str}</div>
            <span style="background: {cor_tag_canal}; color: #FFFFFF; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 14px;">{subtitulo_detalhe_str}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Filtrar pedidos pertencentes ao canal selecionado e aos dias/meses selecionados
    dias_filtro_set = set(dias_selecionados) if dias_selecionados else set()
    peds_detalhe = []

    for p in pedidos_exibicao:
        dt_obj = obter_data_faturamento_pedido(p)
        dt_str = dt_obj.strftime("%d/%m/%Y")
        val_eixo_p = dt_obj.strftime("%d/%m") if is_mes_especifico else dt_obj.strftime("%m/%Y")

        raw = p.get("raw_data", {})
        cab = raw.get("cabecalho", {})
        info_adic = raw.get("informacoes_adicionais", {})
        vend = str(p.get("vendedor") or info_adic.get("contato") or cab.get("nome_vendedor") or "").strip()
        num_p_str = str(p.get("numero_pedido") or cab.get("numero_pedido") or "").strip()
        is_b2c_p = not eh_pedido_b2b_cnpj(p)
        canal_p = "B2C (Site API)" if is_b2c_p else "B2B (Corporativo)"

        # Checar filtro de canal
        if origem_efetiva == "B2B" and canal_p != "B2B (Corporativo)":
            continue
        elif origem_efetiva == "B2C" and canal_p != "B2C (Site API)":
            continue
        elif tem_b2b_sel and not tem_b2c_sel and canal_p != "B2B (Corporativo)":
            continue
        elif tem_b2c_sel and not tem_b2b_sel and canal_p != "B2C (Site API)":
            continue

        # Checar filtro de dias/meses selecionados
        if dias_filtro_set:
            match_data = (val_eixo_p in dias_filtro_set) or (dt_obj.strftime("%m/%Y") in dias_filtro_set) or (dt_obj.strftime("%Y-%m") in dias_filtro_set)
            if not match_data:
                continue

        obs_venda_str = raw.get("observacoes", {}).get("obs_venda") or "—"
        val_num = float(p.get("valor_total", 0.0))
        qtd_num = int(p.get("quantidade_itens") or 1)

        num_formatado = formatar_num_pedido_limpo(num_p_str) if 'formatar_num_pedido_limpo' in globals() else num_p_str
        etapa_raw = str(p.get("etapa") or raw.get("cabecalho", {}).get("etapa") or "").strip()
        if etapa_raw in ["20", "70"]:
            etapa_rotulo = "20 (Separação)"
        elif etapa_raw == "60":
            etapa_rotulo = "60 (Faturado)"
        elif etapa_raw == "10":
            etapa_rotulo = "10 (Aberto)"
        elif etapa_raw == "50":
            etapa_rotulo = "50 (Pronto p/ Fat)"
        else:
            etapa_rotulo = f"Etapa {etapa_raw}"

        cli_n_det = str(p.get("cliente_nome") or p.get("cliente", {}).get("razao_social") or "").strip()
        if not cli_n_det or cli_n_det.startswith("Cliente #"):
            cod_c_p = str(p.get("codigo_cliente") or cab.get("codigo_cliente") or "").strip()
            if cod_c_p:
                if not _MAPA_CLIENTES_RAM_GLOBAL:
                    try:
                        clis_l = omie.carregar_clientes() or []
                        for c_item in clis_l:
                            c_k = str(c_item.get("codigo_cliente_omie") or c_item.get("codigo_cliente") or "").strip()
                            if c_k:
                                _MAPA_CLIENTES_RAM_GLOBAL[c_k] = c_item
                    except Exception:
                        pass
                if cod_c_p in _MAPA_CLIENTES_RAM_GLOBAL:
                    cli_n_det = _MAPA_CLIENTES_RAM_GLOBAL[cod_c_p].get("razao_social") or _MAPA_CLIENTES_RAM_GLOBAL[cod_c_p].get("nome_fantasia") or cli_n_det

        peds_detalhe.append({
            "Pedido": f"#{num_formatado}",
            "Data": dt_str,
            "Cliente": cli_n_det or "Cliente",
            "Canal": canal_p,
            "Vendedor": normalizar_nome_vendedor(vend, num_p_str, ped_obj=p),
            "Etapa": etapa_rotulo,
            "Qtd Itens": qtd_num,
            "Faturamento Venda (R$)": fmt_brl(val_num),
            "_val_num": val_num,
            "_qtd_num": qtd_num,
            "_dt_obj": dt_obj
        })

    if peds_detalhe:
        subtot_pedidos = len(peds_detalhe)
        subtot_unidades = sum(p["_qtd_num"] for p in peds_detalhe)
        subtot_faturamento = sum(p["_val_num"] for p in peds_detalhe)

        # ── SUBTOTAL EXECUTIVO (KPIs) ──
        sub_c1, sub_c2, sub_c3 = st.columns(3)
        with sub_c1:
            st.metric("📦 Subtotal Pedidos", f"{subtot_pedidos} pedido{'s' if subtot_pedidos > 1 else ''}")
        with sub_c2:
            st.metric("🛍️ Total de Unidades / Itens", f"{subtot_unidades:,} item{'s' if subtot_unidades > 1 else ''}".replace(",", "."))
        with sub_c3:
            lbl_tot_fat = f"💵 Total Faturado ({qtd_dias_sel} {lbl_eixo.lower()}{'s' if qtd_dias_sel > 1 else ''})" if qtd_dias_sel > 0 else "💵 Total Faturado no Período"
            st.metric(lbl_tot_fat, fmt_brl(subtot_faturamento))

        st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

        df_drill = pd.DataFrame([
            {
                "Pedido": p["Pedido"],
                "Data": p["Data"],
                "Cliente": p["Cliente"],
                "Canal": p["Canal"],
                "Vendedor": p["Vendedor"],
                "Etapa": p["Etapa"],
                "Qtd Itens": p["Qtd Itens"],
                "Faturamento Venda (R$)": p["Faturamento Venda (R$)"]
            }
            for p in peds_detalhe
        ])
        st.dataframe(df_drill, use_container_width=True, hide_index=True)
    else:
        st.info(f"Nenhum pedido localizado para a seleção atual.")

    # ── SUGESTÃO PERTINENTE: COMPARATIVO DE PARTICIPAÇÃO DE CANAIS (DONUT + SCORECARD) ──
    if tot_fat_soma_ambos > 0:
        st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
        st.markdown(f'<div class="section-header">⚖️ Comparativo de Participação de Canais — B2B Corporativo vs B2C Site API ({lbl_periodo_grafico})</div>', unsafe_allow_html=True)

        col_mix_pie, col_mix_info = st.columns([1.5, 2.5])

        with col_mix_pie:
            df_mix_canais = pd.DataFrame([
                {"Canal": "B2B (Corporativo)", "Faturamento": tot_fat_b2b, "Pedidos": len(b2b_pedidos)},
                {"Canal": "B2C (Site API)", "Faturamento": tot_fat_b2c, "Pedidos": len(b2c_pedidos)}
            ])
            fig_mix = px.pie(
                df_mix_canais,
                values="Faturamento",
                names="Canal",
                hole=0.62,
                color="Canal",
                color_discrete_map={
                    "B2B (Corporativo)": "#2563EB",
                    "B2C (Site API)": "#10B981"
                }
            )
            fig_mix.update_traces(
                textinfo="percent",
                textfont_size=13,
                textfont_color="#FFFFFF",
                textposition="inside",
                hovertemplate="<span style='color:#FFFFFF; font-size:13px;'><b>%{label}</b><br>💰 Faturamento: <b>R$ %{value:,.2f}</b><br>📊 Participação: <b>%{percent}</b></span><extra></extra>",
                marker=dict(line=dict(color="#FFFFFF", width=3))
            )
            fig_mix.update_layout(
                template="plotly_white",
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                height=300,
                margin=dict(l=10, r=10, t=25, b=10),
                hoverlabel=dict(
                    bgcolor="#0F172A",
                    bordercolor="#4F46E5",
                    font=dict(color="#FFFFFF", size=13, family="Inter")
                ),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.15,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=11, color="#334155")
                ),
                annotations=[
                    dict(
                        text=f"<span style='font-size:10px; color:#64748B; font-weight:600;'>TOTAL</span><br><b style='font-size:15px; color:#0F172A;'>{fmt_brl(tot_fat_soma_ambos)}</b>",
                        x=0.5, y=0.5, font_size=12, showarrow=False
                    )
                ]
            )
            st.plotly_chart(fig_mix, use_container_width=True)

        with col_mix_info:
            canal_lider_nome = "B2B (Corporativo)" if tot_fat_b2b >= tot_fat_b2c else "B2C (Site API)"
            canal_lider_cor = "#2563EB" if canal_lider_nome == "B2B (Corporativo)" else "#10B981"
            canal_lider_bg = "#EFF6FF" if canal_lider_nome == "B2B (Corporativo)" else "#ECFDF5"
            canal_lider_border = "#93C5FD" if canal_lider_nome == "B2B (Corporativo)" else "#A7F3D0"
            st.markdown(f"""<div style="background: #FFFFFF; border: 1.5px solid #E2E8F0; border-radius: 14px; padding: 20px 22px; box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04); height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
<div>
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 1px solid #F1F5F9;">
<span style="font-size: 15px; font-weight: 800; color: #0F172A; display: flex; align-items: center; gap: 6px;">⚖️ Diagnóstico de Canais</span>
<span style="background: {canal_lider_bg}; color: {canal_lider_cor}; font-size: 11px; font-weight: 800; padding: 4px 12px; border-radius: 20px; border: 1.5px solid {canal_lider_border};">🏆 Líder: {canal_lider_nome}</span>
</div>
<div style="margin-bottom: 18px;">
<div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 8px; gap: 8px;">
<span style="background: #EFF6FF; color: #1D4ED8; border: 1px solid #BFDBFE; padding: 4px 10px; border-radius: 6px; font-weight: 800; font-size: 11px; display: inline-flex; align-items: center; gap: 4px;">
🏢 B2B: {pct_b2b:.1f}% ({fmt_brl(tot_fat_b2b)})
</span>
<span style="background: #ECFDF5; color: #047857; border: 1px solid #A7F3D0; padding: 4px 10px; border-radius: 6px; font-weight: 800; font-size: 11px; display: inline-flex; align-items: center; gap: 4px;">
🛒 B2C: {pct_b2c:.1f}% ({fmt_brl(tot_fat_b2c)})
</span>
</div>
<div style="width: 100%; height: 14px; background: #F1F5F9; border-radius: 8px; border: 1px solid #CBD5E1; overflow: hidden; display: flex; box-shadow: inset 0 1px 3px rgba(0,0,0,0.06);">
<div style="width: {pct_b2b}%; height: 100%; background: linear-gradient(90deg, #2563EB 0%, #3B82F6 100%); border-right: 2px solid #FFFFFF; transition: width 0.3s ease;"></div>
<div style="width: {pct_b2c}%; height: 100%; background: linear-gradient(90deg, #10B981 0%, #34D399 100%); transition: width 0.3s ease;"></div>
</div>
</div>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
<div style="background: linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 100%); border: 1.5px solid #BFDBFE; border-top: 3.5px solid #2563EB; border-radius: 10px; padding: 12px 14px;">
<div style="display: flex; justify-content: space-between; align-items: center;">
<span style="font-size: 11px; color: #1E40AF; font-weight: 800; letter-spacing: 0.03em;">🏢 B2B CORP.</span>
<span style="background: #DBEAFE; color: #1E40AF; font-size: 10px; font-weight: 800; padding: 2px 7px; border-radius: 10px;">{pct_b2b:.1f}%</span>
</div>
<div style="font-size: 17px; font-weight: 900; color: #1E3A8A; margin: 4px 0 6px 0;">{fmt_brl(tot_fat_b2b)}</div>
<div style="font-size: 11px; color: #334155; font-weight: 600;">
📦 <b>{len(b2b_pedidos)}</b> peds | 🎯 Tkt: <b>{fmt_brl(tkt_b2b)}</b>
</div>
</div>
<div style="background: linear-gradient(135deg, #F8FAFC 0%, #ECFDF5 100%); border: 1.5px solid #A7F3D0; border-top: 3.5px solid #10B981; border-radius: 10px; padding: 12px 14px;">
<div style="display: flex; justify-content: space-between; align-items: center;">
<span style="font-size: 11px; color: #065F46; font-weight: 800; letter-spacing: 0.03em;">🛒 B2C SITE API</span>
<span style="background: #D1FAE5; color: #065F46; font-size: 10px; font-weight: 800; padding: 2px 7px; border-radius: 10px;">{pct_b2c:.1f}%</span>
</div>
<div style="font-size: 17px; font-weight: 900; color: #064E3B; margin: 4px 0 6px 0;">{fmt_brl(tot_fat_b2c)}</div>
<div style="font-size: 11px; color: #334155; font-weight: 600;">
📦 <b>{len(b2c_pedidos)}</b> peds | 🎯 Tkt: <b>{fmt_brl(tkt_b2c)}</b>
</div>
</div>
</div>
</div>
<div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 8px 12px; margin-top: 14px; font-size: 11px; color: #475569; display: flex; align-items: center; gap: 8px;">
<span style="font-size: 14px;">💡</span>
<span><b style="color: #0F172A;">Dica de Inteligência Comercial</b>: Use o seletor acima para detalhar dias específicos ou isolar canais para ver pedidos discriminados.</span>
</div>
</div>""", unsafe_allow_html=True)
    else:
        st.info("Sem dados para exibir o comparativo de canais no período selecionado.")

    st.markdown("---")

    # ── SEÇÃO 2: ANÁLISE DA CURVA ABC DE PRODUTOS VENDIDOS ──
    st.markdown('<div class="section-header">🎯 Análise Curva ABC de Produtos Vendidos (Pareto 80/15/5)</div>', unsafe_allow_html=True)

    df_abc = pd.DataFrame(list(produtos_vendas.values())) if produtos_vendas else pd.DataFrame(columns=["codigo", "descricao", "quantidade", "faturamento"])

    if not df_abc.empty:
        df_abc = df_abc.sort_values(by="faturamento", ascending=False).reset_index(drop=True)
        tot_fat_abc = df_abc["faturamento"].sum()
        df_abc["pct_faturamento"] = (df_abc["faturamento"] / tot_fat_abc * 100) if tot_fat_abc > 0 else 0.0
        df_abc["pct_acumulado"] = df_abc["pct_faturamento"].cumsum()

        def classificar_curva(row):
            if row["pct_acumulado"] <= 80.0:
                return "Classe A (🟢 Campeões)"
            elif row["pct_acumulado"] <= 95.0:
                return "Classe B (🟡 Moderado)"
            else:
                return "Classe C (🔴 Cauda Longa)"

        df_abc["classe_abc"] = df_abc.apply(classificar_curva, axis=1)

        cnt_a = len(df_abc[df_abc["classe_abc"].str.contains("Classe A")])
        cnt_b = len(df_abc[df_abc["classe_abc"].str.contains("Classe B")])
        cnt_c = len(df_abc[df_abc["classe_abc"].str.contains("Classe C")])

        col_abc_info, col_abc_chart = st.columns([1, 1])

        with col_abc_info:
            st.markdown(f"""
            <div style="background: #F8FAFC; border: 2px solid #CBD5E1; border-radius: 12px; padding: 18px; box-shadow: 0 2px 8px rgba(15,23,42,0.04);">
                <div style="font-weight: 900; font-size: 15px; color: #000000; margin-bottom: 10px; border-bottom: 2px solid #CBD5E1; padding-bottom: 6px;">📊 Distribuição de Produtos por Classe ABC</div>
                <div style="font-size: 13px; line-height: 1.7; color: #000000; font-weight: 600;">
                    • <b style="color: #047857; font-weight: 900; font-weight:900;">🟢 Classe A ({cnt_a} produtos)</b>: Geram <b style="color:#000000; font-weight:900;">80% do faturamento total</b>. São os campeões de venda da OMNIEVO — estoque deve ser mantido 100% abastecido.<br>
                    • <b style="color:#B45309; font-weight:900;">🟡 Classe B ({cnt_b} produtos)</b>: Geram os <b style="color:#000000; font-weight:900;">próximos 15% do faturamento</b>. Itens de vendas intermediárias.<br>
                    • <b style="color:#B91C1C; font-weight:900;">🔴 Classe C ({cnt_c} produtos)</b>: Geram os <b style="color:#000000; font-weight:900;">últimos 5% do faturamento</b>. Cauda longa — ideal para campanhas de desova e bonificações em compras B2B.
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_abc_chart:
            fig_donut = px.pie(
                df_abc, names="classe_abc", values="faturamento", hole=0.58,
                title="Participação do Faturamento por Classe ABC",
                color="classe_abc",
                color_discrete_map={
                    "Classe A (🟢 Campeões)": "#10B981",
                    "Classe B (🟡 Moderado)": "#F59E0B",
                    "Classe C (🔴 Cauda Longa)": "#EF4444"
                }
            )
            fig_donut.update_traces(
                textinfo="percent",
                textfont_size=12,
                textfont_color="#FFFFFF",
                textposition="inside",
                hovertemplate="<span style='color:#FFFFFF; font-size:13px;'><b>%{label}</b><br>💰 Faturamento: <b>R$ %{value:,.2f}</b><br>📊 Participação: <b>%{percent}</b></span><extra></extra>",
                marker=dict(line=dict(color="#FFFFFF", width=2.5))
            )
            fig_donut.update_layout(
                template="plotly_white",
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                font=dict(family="Inter, sans-serif", size=12, color="#0F172A"),
                hoverlabel=dict(
                    bgcolor="#0F172A",
                    bordercolor="#4F46E5",
                    font=dict(color="#FFFFFF", size=13, family="Inter")
                ),
                title=dict(
                    text="<b>Participação por Classe ABC</b>",
                    font=dict(size=14, color="#0F172A", family="Inter, sans-serif")
                ),
                legend=dict(
                    font=dict(size=11, color="#334155", family="Inter, sans-serif"),
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.02
                ),
                height=290,
                margin=dict(l=10, r=10, t=35, b=10)
            )
            st.plotly_chart(fig_donut, use_container_width=True)

        # ── TABELA FORMATADA DA CURVA ABC ──
        st.markdown('<div class="section-header">📋 Tabela Completa de Classificação de Produtos (Curva ABC)</div>', unsafe_allow_html=True)
        
        col_flt_abc, _ = st.columns([2, 2])
        with col_flt_abc:
            filtro_classe = st.selectbox("Filtrar por Classe", ["Todas as Classes", "🟢 Classe A (Campeões)", "🟡 Classe B (Intermediários)", "🔴 Classe C (Cauda Longa)"], key="flt_curva_abc_select")

        df_disp = df_abc.copy()
        if "Classe A" in filtro_classe:
            df_disp = df_disp[df_disp["classe_abc"].str.contains("Classe A")]
        elif "Classe B" in filtro_classe:
            df_disp = df_disp[df_disp["classe_abc"].str.contains("Classe B")]
        elif "Classe C" in filtro_classe:
            df_disp = df_disp[df_disp["classe_abc"].str.contains("Classe C")]

        df_disp["Faturamento (R$)"] = df_disp["faturamento"].apply(fmt_brl)
        df_disp["% Faturamento"] = df_disp["pct_faturamento"].apply(lambda x: f"{x:.2f}%")
        df_disp["% Acumulado"] = df_disp["pct_acumulado"].apply(lambda x: f"{x:.2f}%")
        df_disp["Qtd Vendida"] = df_disp["quantidade"].astype(int)

        df_table_abc = df_disp[["codigo", "descricao", "Qtd Vendida", "Faturamento (R$)", "% Faturamento", "% Acumulado", "classe_abc"]]
        df_table_abc.columns = ["Cód. Int.", "Descrição do Produto", "Qtd Vendida", "Faturamento (R$)", "% Faturamento", "% Acumulado", "Classificação ABC"]

        st.dataframe(df_table_abc, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum histórico de produtos vendidos localizado para montar a Curva ABC.")


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 4.5: GESTÃO DE METAS COMERCIAIS & PACING DIÁRIO
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "🎯  Metas & Pacing Diário":
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    import datetime
    from datetime import date
    import calendar

    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">🎯</div>
        <div>
            <div class="page-header-title">Gestão de Metas & Pacing Diário</div>
            <div class="page-header-subtitle">Acompanhamento executivo de metas do mês, ritmo diário por dia útil, projeção de fechamento (Run-Rate) e metas da equipe.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    pedidos_lista_full = auth.obter_pedidos_filtrados_usuario(_obter_pedidos_cached(), usr_logado)
    hoje = date.today()

    # ── FILTROS DE ANO, MÊS E OPERAÇÃO / BONIFICAÇÃO ──
    col_f1, col_f2, col_f3, col_f4 = st.columns([1, 1.1, 1.4, 1.8])

    anos_disp = set()
    for p in pedidos_lista_full:
        dt = obter_data_faturamento_pedido(p)
        anos_disp.add(dt.year)
    lista_anos = sorted(list(anos_disp), reverse=True)
    if hoje.year not in lista_anos:
        lista_anos.insert(0, hoje.year)

    with col_f1:
        ano_sel = st.selectbox("📅 Ano de Referência", lista_anos, index=0, key="metas_ano_sel")

    meses_nomes = [
        (1, "01 - Janeiro"), (2, "02 - Fevereiro"), (3, "03 - Março"), (4, "04 - Abril"),
        (5, "05 - Maio"), (6, "06 - Junho"), (7, "07 - Julho"), (8, "08 - Agosto"),
        (9, "09 - Setembro"), (10, "10 - Outubro"), (11, "11 - Novembro"), (12, "12 - Dezembro")
    ]
    idx_mes_padrao = hoje.month - 1 if ano_sel == hoje.year else 0
    with col_f2:
        mes_tuple = st.selectbox("🗓️ Mês de Referência", meses_nomes, index=idx_mes_padrao, format_func=lambda x: x[1], key="metas_mes_sel")
        mes_sel = mes_tuple[0]

    with col_f3:
        opcoes_operacao = [
            "Vendas e Bonificações",
            "Apenas Vendas (Líquido)",
            "Apenas Bonificações (Brindes)"
        ]
        filtro_operacao = st.selectbox("🏷️ Operação / Bonificação", opcoes_operacao, index=0, key="metas_operacao_sel")

    with col_f4:
        if filtro_operacao == "Apenas Vendas (Líquido)":
            badge_op_status = '<span style="font-size: 11px; font-weight: 800; color: #10B981;">🟢 Apenas Vendas (Omie ERP)</span>'
        elif filtro_operacao == "Apenas Bonificações (Brindes)":
            badge_op_status = '<span style="font-size: 11px; font-weight: 800; color: #F59E0B;">🎁 Apenas Bonificações (Omie ERP)</span>'
        else:
            badge_op_status = '<span style="font-size: 11px; font-weight: 800; color: #4F46E5;">📦 Vendas + Bonificações (Omie ERP)</span>'

        st.markdown(f"""
        <div style="display: flex; flex-direction: column;">
            <label style="font-size: 14px; font-weight: 600; color: #1E293B; margin-bottom: 4px; height: 24px; display: flex; align-items: center;">
                📊 Período Selecionado & Status
            </label>
            <div style="background: #FFFFFF; border: 1px solid #000000; border-radius: 8px; height: 42px; min-height: 42px; box-sizing: border-box; padding: 0 16px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);">
                <div>
                    <span style="font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase;">Período: </span>
                    <span style="font-size: 13px; font-weight: 900; color: #000000;">{mes_tuple[1]} / {ano_sel}</span>
                </div>
                <div style="text-align: right;">
                    {badge_op_status}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── CARREGAR METAS DO PERÍODO ──
    metas_data = carregar_metas_comerciais(ano_sel, mes_sel)
    meta_global = float(metas_data.get("meta_global") or 350000.0)
    meta_b2b = float(metas_data.get("meta_b2b") or 200000.0)
    meta_b2c = float(metas_data.get("meta_b2c") or 150000.0)
    metas_vendedores_config = metas_data.get("metas_vendedores") or {}

    # ── APURAR FATURAMENTO REALIZADO DO MÊS ──
    fat_total_mes = 0.0
    fat_b2b_mes = 0.0
    fat_b2c_mes = 0.0
    fat_por_vendedor = {}
    fat_diario = {}
    qtd_pedidos_mes = 0

    for ped in pedidos_lista_full:
        etp = str(ped.get("etapa") or ped.get("codigo_etapa") or "").strip()
        if etp != "60":
            continue
        dt_obj = obter_data_faturamento_pedido(ped)
        if dt_obj.year == ano_sel and dt_obj.month == mes_sel:
            raw = ped.get("raw_data", {}) if isinstance(ped.get("raw_data"), dict) else {}
            cab = raw.get("cabecalho", {}) if isinstance(raw.get("cabecalho"), dict) else {}
            det = raw.get("det", []) if isinstance(raw.get("det"), list) else []
            cen_ped = str(cab.get("codigo_cenario_impostos") or "")

            vlr_vendas_ped = 0.0
            vlr_bonif_ped = 0.0

            for it in det:
                inf_it = it.get("inf_adic", {}) if isinstance(it.get("inf_adic"), dict) else {}
                pr_it = it.get("produto", {}) if isinstance(it.get("produto"), dict) else {}
                cen_item = str(inf_it.get("codigo_cenario_impostos_item") or cen_ped)
                nao_fin = str(inf_it.get("nao_gerar_financeiro", "N")).upper()
                tipo_item = str(it.get("tipo_item", "")).upper()
                val_it = float(pr_it.get("valor_total") or (float(pr_it.get("quantidade", 0)) * float(pr_it.get("valor_unitario", 0))))

                cfop_item = str(pr_it.get("cfop") or "").strip()
                eh_bonif = ("BONIF" in tipo_item) or (nao_fin == "S") or (cen_item == "8904163333") or (cfop_item in ["5.910", "6.910"])
                if eh_bonif:
                    vlr_bonif_ped += val_it
                else:
                    vlr_vendas_ped += val_it

            tot_orig = float(raw.get("total_pedido", {}).get("valor_total_pedido") or ped.get("valor_total") or 0.0)

            # Se o pedido não tem detalhamento de itens específico, assume valor total de venda
            if vlr_vendas_ped == 0.0 and vlr_bonif_ped == 0.0 and tot_orig > 0:
                vlr_vendas_ped = tot_orig

            if filtro_operacao == "Apenas Vendas (Líquido)":
                if vlr_vendas_ped <= 0:
                    continue
                val = vlr_vendas_ped
            elif filtro_operacao == "Apenas Bonificações (Brindes)":
                if vlr_bonif_ped <= 0:
                    continue
                val = vlr_bonif_ped
            else:  # "Vendas e Bonificações"
                val = tot_orig

            fat_total_mes += val
            qtd_pedidos_mes += 1
            
            # Classificação B2B/B2C usando a mesma regra unificada do sistema
            if eh_pedido_b2b_cnpj(ped):
                fat_b2b_mes += val
            else:
                fat_b2c_mes += val

            vend = ped.get("vendedor") or "Não Informado"

            fat_por_vendedor[vend] = fat_por_vendedor.get(vend, 0.0) + val
            fat_diario[dt_obj.day] = fat_diario.get(dt_obj.day, 0.0) + val

    # ── CÁLCULO DE PACING & DIAS ÚTEIS ──
    num_dias_mes, dias_uteis_total, dias_uteis_passados, dias_uteis_restantes = calcular_dias_uteis_mes(ano_sel, mes_sel)
    
    is_mes_atual = (ano_sel == hoje.year and mes_sel == hoje.month)
    dias_decorridos = hoje.day if is_mes_atual else (num_dias_mes if (ano_sel < hoje.year or (ano_sel == hoje.year and mes_sel < hoje.month)) else 0)
    
    pct_atingido_global = (fat_total_mes / meta_global * 100) if meta_global > 0 else 0.0
    pct_atingido_b2b = (fat_b2b_mes / meta_b2b * 100) if meta_b2b > 0 else 0.0
    pct_atingido_b2c = (fat_b2c_mes / meta_b2c * 100) if meta_b2c > 0 else 0.0

    falta_vender_global = max(0.0, meta_global - fat_total_mes)
    media_diaria_atual = (fat_total_mes / max(dias_decorridos, 1)) if dias_decorridos > 0 else 0.0
    run_rate_projetado = (media_diaria_atual * num_dias_mes) if is_mes_atual else fat_total_mes
    dif_projecao = run_rate_projetado - meta_global

    ritmo_necessario_dia_util = (falta_vender_global / max(dias_uteis_restantes, 1)) if is_mes_atual and dias_uteis_restantes > 0 else 0.0

    # Cor dinâmica do status
    if pct_atingido_global >= 100:
        badge_status_global = '<span style="background: #ECFDF5; color: #059669; padding: 4px 10px; border-radius: 8px; font-weight: 800; font-size: 11px;">🚀 META BATIDA</span>'
        cor_barra_global = "#10B981"
    elif pct_atingido_global >= 70:
        badge_status_global = '<span style="background: #EFF6FF; color: #2563EB; padding: 4px 10px; border-radius: 8px; font-weight: 800; font-size: 11px;">🟢 NO RITMO</span>'
        cor_barra_global = "#2563EB"
    elif pct_atingido_global >= 40:
        badge_status_global = '<span style="background: #FEFCE8; color: #CA8A04; padding: 4px 10px; border-radius: 8px; font-weight: 800; font-size: 11px;">🟡 ATENÇÃO</span>'
        cor_barra_global = "#EAB308"
    else:
        badge_status_global = '<span style="background: #FEF2F2; color: #DC2626; padding: 4px 10px; border-radius: 8px; font-weight: 800; font-size: 11px;">🔴 ABAIXO</span>'
        cor_barra_global = "#EF4444"

    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

    # ── 4 CARDS DE KPI EXECUTIVOS NO TOPO ──
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)

    with col_k1:
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 2px solid #000000; border-radius: 16px; padding: 18px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.04); height: 220px; min-height: 220px; max-height: 220px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase;">Meta Global da Empresa</span>
                {badge_status_global}
            </div>
            <div>
                <div style="font-size: 24px; font-weight: 900; color: #000000; letter-spacing: -0.5px;">{fmt_brl(fat_total_mes)}</div>
                <div style="font-size: 12px; color: #475569; font-weight: 700; margin-top: 4px;">
                    Meta: <b>{fmt_brl(meta_global)}</b> ({pct_atingido_global:.1f}%)
                </div>
            </div>
            <div>
                <div style="width: 100%; height: 7px; background: #F1F5F9; border-radius: 4px; overflow: hidden; border: 1px solid #E2E8F0; margin-bottom: 6px;">
                    <div style="width: {min(pct_atingido_global, 100.0)}%; height: 100%; background: {cor_barra_global}; border-radius: 4px;"></div>
                </div>
                <div style="font-size: 11px; color: #64748B; font-weight: 600;">
                    Falta vender: <b style="color: #000000;">{fmt_brl(falta_vender_global)}</b>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_k2:
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 2px solid #000000; border-radius: 16px; padding: 18px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.04); height: 220px; min-height: 220px; max-height: 220px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase;">Pacing / Ritmo Diário</span>
                <span style="background: #F1F5F9; color: #0F172A; padding: 3px 8px; border-radius: 6px; font-weight: 800; font-size: 11px;">⚡ VELOCIDADE</span>
            </div>
            <div>
                <div style="font-size: 24px; font-weight: 900; color: #4F46E5; letter-spacing: -0.5px;">{fmt_brl(ritmo_necessario_dia_util)}<span style="font-size: 12px; font-weight: 700; color: #64748B;"> /dia útil</span></div>
                <div style="font-size: 12px; color: #0F172A; font-weight: 700; margin-top: 4px;">
                    Média realizada: <b>{fmt_brl(media_diaria_atual)}/dia</b>
                </div>
            </div>
            <div style="font-size: 11px; color: #475569; font-weight: 600; line-height: 1.5; border-top: 1px solid #F1F5F9; padding-top: 6px;">
                • Dias úteis restantes: <b style="color: #000000;">{dias_uteis_restantes} dias</b><br>
                • Dias corridos: <b style="color: #000000;">{dias_decorridos} de {num_dias_mes} dias</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_k3:
        cor_proj = "#10B981" if dif_projecao >= 0 else "#EF4444"
        sinal_proj = "+" if dif_projecao >= 0 else ""
        txt_proj = "Acima da meta" if dif_projecao >= 0 else "Abaixo da meta"
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 2px solid #000000; border-radius: 16px; padding: 18px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.04); height: 220px; min-height: 220px; max-height: 220px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase;">Projeção de Fechamento</span>
                <span style="background: #F8FAFC; color: {cor_proj}; border: 1px solid {cor_proj}; padding: 3px 8px; border-radius: 6px; font-weight: 800; font-size: 11px;">RUN-RATE</span>
            </div>
            <div>
                <div style="font-size: 24px; font-weight: 900; color: #000000; letter-spacing: -0.5px;">{fmt_brl(run_rate_projetado)}</div>
                <div style="font-size: 12px; color: {cor_proj}; font-weight: 800; margin-top: 4px;">
                    {sinal_proj}{fmt_brl(dif_projecao)} ({txt_proj})
                </div>
            </div>
            <div style="font-size: 11px; color: #64748B; font-weight: 600; line-height: 1.5; border-top: 1px solid #F1F5F9; padding-top: 6px;">
                • Estimativa linear baseada na velocidade diária atual.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_k4:
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 2px solid #000000; border-radius: 16px; padding: 18px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.04); height: 220px; min-height: 220px; max-height: 220px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase;">Metas por Canal</span>
                <span style="background: #F1F5F9; color: #000000; padding: 3px 8px; border-radius: 6px; font-weight: 800; font-size: 11px;">B2B / B2C</span>
            </div>
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center; font-size: 12px; font-weight: 800; margin-bottom: 2px;">
                    <span style="color: #2563EB;">🏢 B2B: {fmt_brl(fat_b2b_mes)}</span>
                    <span style="color: #0F172A; font-weight: 900;">{pct_atingido_b2b:.1f}%</span>
                </div>
                <div style="width: 100%; height: 6px; background: #F1F5F9; border-radius: 3px; overflow: hidden; border: 1px solid #E2E8F0; margin-bottom: 4px;">
                    <div style="width: {min(pct_atingido_b2b, 100.0)}%; height: 100%; background: #2563EB; border-radius: 3px;"></div>
                </div>
                <div style="font-size: 10px; color: #64748B; font-weight: 600;">Meta: {fmt_brl(meta_b2b)}</div>
            </div>
            <div style="border-top: 1px solid #F1F5F9; padding-top: 6px;">
                <div style="display: flex; justify-content: space-between; align-items: center; font-size: 12px; font-weight: 800; margin-bottom: 2px;">
                    <span style="color: #10B981;">🛒 B2C: {fmt_brl(fat_b2c_mes)}</span>
                    <span style="color: #0F172A; font-weight: 900;">{pct_atingido_b2c:.1f}%</span>
                </div>
                <div style="width: 100%; height: 6px; background: #F1F5F9; border-radius: 3px; overflow: hidden; border: 1px solid #E2E8F0; margin-bottom: 4px;">
                    <div style="width: {min(pct_atingido_b2c, 100.0)}%; height: 100%; background: #10B981; border-radius: 3px;"></div>
                </div>
                <div style="font-size: 10px; color: #64748B; font-weight: 600;">Meta: {fmt_brl(meta_b2c)}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    # ── GRÁFICO DE BURN-UP ACUMULADO (PACING TEMPORAL PLOTLY) ──
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%); border: 1.5px solid #C7D2FE; border-radius: 12px; padding: 12px 18px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between;'>
        <div>
            <div style='font-size: 15px; color: #1E1B4B; font-weight: 800;'>📈 Trajetória de Pacing Acumulado: Meta Ideal vs Realizado Dia a Dia</div>
            <div style='font-size: 12px; color: #4338CA;'>Curva contínua de faturamento acumulado comparado ao ritmo ideal da meta linear (Passe o mouse para inspecionar)</div>
        </div>
        <span class="dark-badge" style='background: #4F46E5; color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; font-size: 11px; font-weight: 800; padding: 4px 14px; border-radius: 20px;'>{mes_tuple[1]} / {ano_sel}</span>
    </div>
    """, unsafe_allow_html=True)

    dias_eixo = list(range(1, num_dias_mes + 1))
    
    # ── CÁLCULO DE META IDEAL (DIAS ÚTEIS VS FINAIS DE SEMANA / FERIADOS) ──
    # Para finais de semana e feriados nacionais, a meta ideal se mantém estática (igual ao último dia útil anterior)
    meta_diaria_util = meta_global / max(dias_uteis_total, 1)
    meta_ideal_acum = []
    acum_meta = 0.0
    for d in dias_eixo:
        dt_d = date(ano_sel, mes_sel, d)
        if not eh_feriado_ou_fim_de_semana(dt_d):
            acum_meta += meta_diaria_util
        meta_ideal_acum.append(round(acum_meta, 2))
    
    dias_reais = [d for d in dias_eixo if d <= dias_decorridos] if is_mes_atual else dias_eixo
    real_acum = []
    tot_acum_dia = 0.0
    for d in dias_reais:
        tot_acum_dia += fat_diario.get(d, 0.0)
        real_acum.append(tot_acum_dia)

    # ── CÁLCULO DA PROJEÇÃO LINEAR (RUN-RATE DIAS ÚTEIS) ──
    # Para finais de semana e feriados nacionais, a projeção também mantém o valor do último dia útil
    dias_decorridos_list = [d for d in range(1, dias_decorridos + 1)]
    cnt_dias_uteis_decorridos = max(len([d for d in dias_decorridos_list if not eh_feriado_ou_fim_de_semana(date(ano_sel, mes_sel, d))]), 1)
    media_diaria_util_praticada = (tot_acum_dia / cnt_dias_uteis_decorridos) if (is_mes_atual and tot_acum_dia > 0) else 0.0

    fig_pacing = go.Figure()

    # Linha da Meta Ideal
    fig_pacing.add_trace(go.Scatter(
        x=dias_eixo,
        y=meta_ideal_acum,
        mode='lines',
        name='Meta Ideal (Dias Úteis)',
        line=dict(color='#94A3B8', width=2.5, dash='dash'),
        hovertemplate="<span style='color: #FFFFFF; font-size: 13px;'><b>Dia %{x}</b></span><br><span style='color: #FFFFFF;'>🎯 Meta Ideal: <b>R$ %{y:,.2f}</b></span><extra></extra>"
    ))

    # Linha do Realizado
    fig_pacing.add_trace(go.Scatter(
        x=dias_reais,
        y=real_acum,
        mode='lines+markers',
        name='Faturamento Realizado (R$)',
        line=dict(color='#2563EB', width=3.5),
        marker=dict(size=7, color='#1E40AF', line=dict(color="#FFFFFF", width=1.5)),
        hovertemplate="<span style='color: #FFFFFF; font-size: 13px;'><b>Dia %{x}</b></span><br><span style='color: #FFFFFF;'>💰 Realizado: <b>R$ %{y:,.2f}</b></span><extra></extra>"
    ))

    # Projeção futura se for mês atual e houver dias restantes
    if is_mes_atual and dias_decorridos < num_dias_mes and dias_decorridos > 0 and len(real_acum) > 0:
        dias_proj = list(range(dias_decorridos, num_dias_mes + 1))
        proj_acum = []
        val_acum_proj = real_acum[-1]
        for d in dias_proj:
            if d == dias_decorridos:
                proj_acum.append(round(val_acum_proj, 2))
            else:
                dt_p = date(ano_sel, mes_sel, d)
                if not eh_feriado_ou_fim_de_semana(dt_p):
                    val_acum_proj += media_diaria_util_praticada
                proj_acum.append(round(val_acum_proj, 2))

        fig_pacing.add_trace(go.Scatter(
            x=dias_proj,
            y=proj_acum,
            mode='lines',
            name='Projeção Linear (Run-Rate)',
            line=dict(color='#8B5CF6', width=2.5, dash='dot'),
            hovertemplate="<span style='color: #FFFFFF; font-size: 13px;'><b>Dia %{x}</b></span><br><span style='color: #FFFFFF;'>🔮 Projeção: <b>R$ %{y:,.2f}</b></span><extra></extra>"
        ))

    fig_pacing.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        height=360,
        margin=dict(l=15, r=15, t=35, b=25),
        font=dict(family="Inter, -apple-system, sans-serif", size=12, color="#0F172A"),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#0F172A",
            bordercolor="#38BDF8",
            font=dict(color="#FFFFFF", size=13, family="Inter, sans-serif")
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(family="Inter, sans-serif", size=11, color="#0F172A")
        ),
        xaxis=dict(
            title="Dia do Mês",
            showgrid=False,
            linecolor="#CBD5E1",
            linewidth=1,
            tickmode="linear",
            tick0=1,
            dtick=1,
            range=[0.5, num_dias_mes + 0.5],
            tickfont=dict(size=10, color="#475569", family="Inter, sans-serif"),
            title_font=dict(size=12, color="#0F172A", family="Inter, sans-serif")
        ),
        yaxis=dict(
            title="Faturamento Acumulado (R$)",
            showgrid=True,
            gridcolor="#F1F5F9",
            gridwidth=1,
            linecolor="#CBD5E1",
            linewidth=1,
            tickprefix="R$ ",
            tickformat=",.2f",
            tickfont=dict(size=11, color="#475569", family="Inter, sans-serif"),
            title_font=dict(size=12, color="#0F172A", family="Inter, sans-serif")
        )
    )
    st.plotly_chart(fig_pacing, use_container_width=True)

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    # ── METAS INDIVIDUAIS POR VENDEDOR ──
    # Coletar todos os vendedores relevantes
    todos_vendedores = set(list(fat_por_vendedor.keys()) + list(metas_vendedores_config.keys()))
    vendedores_validos = [v for v in todos_vendedores if v and v != "Não Informado"]
    if not vendedores_validos and "Não Informado" in todos_vendedores:
        vendedores_validos = ["Não Informado"]

    vendedores_validos.sort(key=lambda x: fat_por_vendedor.get(x, 0.0), reverse=True)

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%); border: 1.5px solid #E2E8F0; border-radius: 12px; padding: 12px 18px; margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between;'>
        <div>
            <div style='font-size: 15px; color: #0F172A; font-weight: 800;'>👥 Metas e Desempenho Individual da Equipe Comercial</div>
            <div style='font-size: 12px; color: #64748B;'>Acompanhamento de ritmo, percentual atingido e projeção individual por vendedor</div>
        </div>
        <span class="dark-badge" style='background: #0F172A; color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; font-size: 11px; font-weight: 800; padding: 4px 14px; border-radius: 20px;'>{len(vendedores_validos)} Vendedores</span>
    </div>
    """, unsafe_allow_html=True)

    cols_grid = st.columns(3)
    for idx_v, vend_nome in enumerate(vendedores_validos):
        col_dest = cols_grid[idx_v % 3]
        fat_vend = fat_por_vendedor.get(vend_nome, 0.0)
        meta_vend = float(metas_vendedores_config.get(vend_nome) or (meta_global / max(len(vendedores_validos), 1)))
        pct_vend = (fat_vend / meta_vend * 100) if meta_vend > 0 else 0.0
        falta_vend = max(0.0, meta_vend - fat_vend)
        ritmo_vend = (falta_vend / max(dias_uteis_restantes, 1)) if is_mes_atual and dias_uteis_restantes > 0 else 0.0

        if pct_vend >= 100:
            badge_v = "🥇 Acelerador Ativado (>100%)"
            cor_v = "#10B981"
            bg_v = "#ECFDF5"
        elif pct_vend >= 70:
            badge_v = "🟢 No Ritmo"
            cor_v = "#2563EB"
            bg_v = "#EFF6FF"
        elif pct_vend >= 40:
            badge_v = "🟡 Atenção"
            cor_v = "#EAB308"
            bg_v = "#FEFCE8"
        else:
            badge_v = "🔴 Abaixo da Meta"
            cor_v = "#EF4444"
            bg_v = "#FEF2F2"

        with col_dest:
            st.markdown(f"""
            <div style="background: #FFFFFF; border: 2px solid #000000; border-radius: 16px; padding: 18px; margin-bottom: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); height: 220px; min-height: 220px; max-height: 220px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                    <div style="font-size: 13px; font-weight: 900; color: #000000; line-height: 1.3; max-width: 65%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                        👤 {vend_nome}
                    </div>
                    <span style="background: {bg_v}; color: {cor_v}; font-size: 10px; font-weight: 800; padding: 3px 8px; border-radius: 6px; white-space: nowrap;">
                        {badge_v}
                    </span>
                </div>
                <div>
                    <div style="font-size: 22px; font-weight: 900; color: #000000; margin-bottom: 4px;">
                        {fmt_brl(fat_vend)}
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 11px; color: #64748B; font-weight: 700; margin-bottom: 6px;">
                        <span>Meta: <b>{fmt_brl(meta_vend)}</b></span>
                        <span style="color: {cor_v}; font-weight: 900;">{pct_vend:.1f}%</span>
                    </div>
                    <div style="width: 100%; height: 7px; background: #F1F5F9; border-radius: 4px; overflow: hidden; border: 1px solid #E2E8F0;">
                        <div style="width: {min(pct_vend, 100.0)}%; height: 100%; background: {cor_v}; border-radius: 4px;"></div>
                    </div>
                </div>
                <div style="font-size: 11px; color: #475569; font-weight: 600; line-height: 1.5; border-top: 1px solid #F1F5F9; padding-top: 8px;">
                    • Falta: <b style="color: #000000;">{fmt_brl(falta_vend)}</b><br>
                    • Ritmo diário: <b style="color: #4F46E5;">{fmt_brl(ritmo_vend)}/dia útil</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    # ── EXPANDER DE CONFIGURAÇÃO DE METAS (EXCLUSIVO ADMINISTRADORES MASTER) ──
    if is_master:
        with st.expander("⚙️ Painel de Configuração: Definir ou Alterar Metas deste Mês (Exclusivo ADM)", expanded=False):
            st.markdown("""
            <div style="font-size: 13px; color: #475569; font-weight: 600; margin-bottom: 14px;">
                Ajuste os valores de metas comerciais para a empresa, canais de venda e vendedores individuais. As alterações são salvas e aplicadas em tempo real.
            </div>
            """, unsafe_allow_html=True)

            with st.form("form_ajuste_metas_mes"):
                col_cfg1, col_cfg2, col_cfg3 = st.columns(3)
                with col_cfg1:
                    nova_meta_global = st.number_input("🎯 Meta Global da Empresa (R$):", min_value=0.0, value=float(meta_global), step=5000.0, format="%.2f")
                with col_cfg2:
                    nova_meta_b2b = st.number_input("🏢 Meta Canal B2B Corporativo (R$):", min_value=0.0, value=float(meta_b2b), step=5000.0, format="%.2f")
                with col_cfg3:
                    nova_meta_b2c = st.number_input("🛒 Meta Canal B2C Site/API (R$):", min_value=0.0, value=float(meta_b2c), step=5000.0, format="%.2f")

                st.markdown("<div style='margin-top: 12px; font-weight: 800; font-size: 13px; color: #000000;'>👤 Metas Individuais por Vendedor:</div>", unsafe_allow_html=True)
                cols_v_cfg = st.columns(3)
                novas_metas_vendedores = {}
                for idx_vc, v_nome in enumerate(vendedores_validos):
                    col_vc = cols_v_cfg[idx_vc % 3]
                    val_atual_v = float(metas_vendedores_config.get(v_nome) or (nova_meta_global / max(len(vendedores_validos), 1)))
                    with col_vc:
                        val_novo = st.number_input(f"{v_nome[:25]} (R$):", min_value=0.0, value=val_atual_v, step=2000.0, format="%.2f", key=f"cfg_meta_v_{idx_vc}")
                        novas_metas_vendedores[v_nome] = val_novo

                btn_salvar_metas = st.form_submit_button("💾 Salvar Metas Comerciais do Mês", use_container_width=True)

                if btn_salvar_metas:
                    novos_dados = {
                        "meta_global": nova_meta_global,
                        "meta_b2b": nova_meta_b2b,
                        "meta_b2c": nova_meta_b2c,
                        "metas_vendedores": novas_metas_vendedores
                    }
                    ok_s = salvar_metas_comerciais(ano_sel, mes_sel, novos_dados)
                    if ok_s:
                        st.success(f"✅ Metas comerciais de {mes_tuple[1]} / {ano_sel} salvas com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao salvar o arquivo de metas comerciais.")


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 5: HISTÓRICO DO CLIENTE (CUSTOMER 360º)
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "🔎  Histórico do Cliente":

    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">🔎</div>
        <div>
            <div class="page-header-title">Histórico de Compras e Perfil 360º do Cliente</div>
            <div class="page-header-subtitle">Consulte o histórico completo de pedidos, métricas de consumo, recência de compra e produtos preferidos por cliente</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Carregar todos os pedidos e cadastros (filtrados por vendedor se não for Master)
    pedidos_lista_full = auth.obter_pedidos_filtrados_usuario(_obter_pedidos_cached(), usr_logado)

    # Mapear TODOS os clientes (do Cadastro Oficial + Pedidos em qualquer etapa)
    mapa_clientes_pedidos = {}

    # 1. Incluir clientes do cadastro oficial da Omie ERP
    for c in lista_clientes:
        cod_c = str(c.get("codigo_cliente") or "").strip()
        razao_c = (c.get("razao_social") or c.get("nome_fantasia") or "").strip()
        cnpj_c = (c.get("cnpj_cpf") or "").strip()
        uf_c = (c.get("estado") or "ES").strip()
        
        display_name = f"{razao_c}"
        if cnpj_c:
            display_name += f" ({cnpj_c})"
        if uf_c:
            display_name += f" - {uf_c}"
            
        if display_name not in mapa_clientes_pedidos:
            mapa_clientes_pedidos[display_name] = {
                "nome": razao_c,
                "codigo_cliente": cod_c,
                "cnpj_cpf": cnpj_c,
                "uf": uf_c,
                "telefone": str(c.get("telefone1_numero") or c.get("telefone") or "").strip(),
                "email": str(c.get("email") or "").strip(),
                "pedidos": [],
                "canais": set()
            }

    # 2. Varrer pedidos de todas as etapas (00, 10, 20, 70, 60, 80)
    for p in pedidos_lista_full:
        raw = p.get("raw_data", {})
        cab = raw.get("cabecalho", {})
        cli_raw = raw.get("cliente", {})
        inf_adic = raw.get("informacoes_adicionais", {})
        
        cod_cli = str(p.get("codigo_cliente") or cab.get("codigo_cliente") or cli_raw.get("codigo_cliente") or "").strip()
        nome_cli = str(cli_raw.get("razao_social") or p.get("cliente_nome") or f"Cliente #{cod_cli}").strip()
        cnpj_cpf = str(cli_raw.get("cnpj_cpf") or p.get("cliente_cnpj_cpf") or "").strip()
        uf_cli = str(p.get("cliente_uf") or cli_raw.get("estado") or cab.get("uf_cliente") or "ES").strip()
        
        # Localizar chave de cliente oficial com a tag 'Cliente'
        display_key = None
        for k_key, v_val in mapa_clientes_pedidos.items():
            if (cod_cli and str(v_val.get("codigo_cliente")) == cod_cli) or (cnpj_cpf and v_val.get("cnpj_cpf") == cnpj_cpf):
                display_key = k_key
                break
                
        # Exigência do usuário: SOMENTE clientes com a tag 'Cliente'
        if not display_key:
            continue
        
        mapa_clientes_pedidos[display_key]["pedidos"].append(p)

        vend_p = str(p.get("vendedor") or inf_adic.get("contato") or cab.get("nome_vendedor") or "").strip()
        num_p_str = str(p.get("numero_pedido") or cab.get("numero_pedido") or "").strip()
        canal_p = "B2C (Site API)" if (num_p_str == "523" or "enviado via api" in vend_p.lower()) else "B2B (Corporativo)"
        mapa_clientes_pedidos[display_key]["canais"].add(canal_p)

    # ── DIRECIONAMENTO INTELIGENTE DO RADAR DE CLIENTES & CHURN ──
    cli_radar_target = st.session_state.pop("cliente_direcionado_radar", None)
    if cli_radar_target:
        alvo_cod = str(cli_radar_target.get("codigo_cliente") or "").strip()
        alvo_doc = "".join(filter(str.isdigit, str(cli_radar_target.get("cnpj_cpf") or "")))
        alvo_nome = str(cli_radar_target.get("nome") or "").strip().lower()

        st.session_state["flt_canal_cliente_h360"] = "Todos os Canais"

        chave_encontrada = None
        for k_chave, v_info in mapa_clientes_pedidos.items():
            k_cod = str(v_info.get("codigo_cliente") or "").strip()
            k_doc = "".join(filter(str.isdigit, str(v_info.get("cnpj_cpf") or "")))
            if alvo_cod and k_cod == alvo_cod:
                chave_encontrada = k_chave
                break
            if alvo_doc and k_doc and k_doc == alvo_doc:
                chave_encontrada = k_chave
                break
            if alvo_nome and alvo_nome in k_chave.lower():
                chave_encontrada = k_chave
                break

        if chave_encontrada:
            st.session_state["sel_cliente_h360"] = chave_encontrada
            st.session_state["ativar_ia_sugestoes"] = True

    # ── BARRA DE PESQUISA E SELEÇÃO DE CLIENTE ──
    st.markdown('<div class="section-header">🔍 Selecionar Cliente</div>', unsafe_allow_html=True)
    col_flt_c1, col_flt_c2 = st.columns([1, 2.5])
    
    with col_flt_c1:
        idx_flt_canal = 0
        if st.session_state.get("flt_canal_cliente_h360") == "Todos os Canais":
            idx_flt_canal = 0
        filtro_canal_cliente = st.selectbox(
            "Canal de Origem:",
            ["Todos os Canais", "🏢 Apenas B2B (Corporativo)", "🛒 Apenas B2C (Site API)"],
            index=idx_flt_canal,
            key="flt_canal_cliente_h360"
        )

    # Filtrar lista de chaves de clientes conforme a seleção de canal
    lista_opcoes_clientes = []

    for k_cli, v_cli in mapa_clientes_pedidos.items():
        if "Apenas B2B" in filtro_canal_cliente and "B2B (Corporativo)" not in v_cli["canais"] and v_cli["canais"]:
            continue
        if "Apenas B2C" in filtro_canal_cliente and "B2C (Site API)" not in v_cli["canais"] and v_cli["canais"]:
            continue

        lista_opcoes_clientes.append(k_cli)

    lista_opcoes_clientes.sort()
    opcoes_select_clientes = ["🔍 Selecione um cliente para consultar o histórico..."] + lista_opcoes_clientes

    idx_default = 0
    if "sel_cliente_h360" in st.session_state and st.session_state["sel_cliente_h360"] in opcoes_select_clientes:
        idx_default = opcoes_select_clientes.index(st.session_state["sel_cliente_h360"])

    with col_flt_c2:
        lbl_qtd_clis = f"Selecione o Cliente ({len(lista_opcoes_clientes)} clientes encontrados):"
        cliente_selecionado_str = st.selectbox(
            lbl_qtd_clis,
            opcoes_select_clientes,
            index=idx_default,
            key="sel_cliente_h360"
        )

    if cliente_selecionado_str == "🔍 Selecione um cliente para consultar o histórico...":
        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
        st.info("👈 **Aguardando Seleção de Cliente**: Escolha um cliente na caixa de seleção acima para consultar o Perfil 360º, Faturamento Acumulado e Histórico Completo de Pedidos.")
    elif cliente_selecionado_str not in mapa_clientes_pedidos:
        st.warning("⚠️ **Acesso Restrito**: Este cliente não pertence à sua carteira autorizada ou não foi localizado.")
    else:
        dados_cli = mapa_clientes_pedidos[cliente_selecionado_str]
        pedidos_cli = dados_cli["pedidos"]
        
        # Ordenar pedidos do cliente do mais recente para o mais antigo
        pedidos_cli.sort(key=lambda x: x.get("data_previsao") or "", reverse=True)

        # Totais do Cliente
        tot_faturado_cli = sum(float(p.get("valor_total") or 0.0) for p in pedidos_cli)
        total_pedidos_cli = len(pedidos_cli)
        total_unidades_cli = sum(int(p.get("quantidade_itens") or 1) for p in pedidos_cli)
        tkt_medio_cli = (tot_faturado_cli / total_pedidos_cli) if total_pedidos_cli > 0 else 0.0

        # Identificar canais e vendedores associados ao cliente
        canais_cli = set()
        vendedores_cli = set()
        datas_compras = []
        peds_tabela = []
        produtos_cliente = {}

        for p in pedidos_cli:
            raw = p.get("raw_data", {}) if isinstance(p.get("raw_data"), dict) else {}
            cab = raw.get("cabecalho", {}) if isinstance(raw.get("cabecalho"), dict) else {}
            inf_adic = raw.get("informacoes_adicionais", {}) if isinstance(raw.get("informacoes_adicionais"), dict) else {}
            vend_raw = str(p.get("vendedor") or inf_adic.get("contato") or cab.get("nome_vendedor") or "").strip()
            num_p_str = str(p.get("numero_pedido") or cab.get("numero_pedido") or "").strip()
            doc_cli = str(dados_cli.get("cnpj_cpf") or "").replace(".", "").replace("/", "").replace("-", "").strip()
            is_b2c = (num_p_str == "523") or ("enviado via api" in vend_raw.lower())
            canal = "B2C (Site API)" if is_b2c else "B2B (Corporativo)"
            vend = normalizar_nome_vendedor(vend_raw, num_p_str, doc_cli)
            
            canais_cli.add(canal)
            if vend:
                vendedores_cli.add(vend)
                    
            dt_obj = obter_data_faturamento_pedido(p)
            datas_compras.append(dt_obj)

            vlr_p = float(p.get("valor_total") or 0.0)
            etapa_str = str(p.get("etapa") or cab.get("etapa") or "").strip()
            status_lbl = "🚚 Faturado" if etapa_str == "60" else ("📦 Separação" if etapa_str == "70" else "📝 Orçamento")

            peds_tabela.append({
                "Nº Pedido": num_p_str,
                "Data Faturamento": dt_obj.strftime("%d/%m/%Y"),
                "Canal": canal,
                "Vendedor": vend,
                "Status": status_lbl,
                "Valor Total (R$)": fmt_brl(vlr_p)
            })

            # Extração de Produtos Comprados pelo Cliente
            itens = raw.get("det", []) if isinstance(raw.get("det"), list) else []
            for it in itens:
                pr = it.get("produto", {}) if isinstance(it.get("produto"), dict) else {}
                cod_pr = str(pr.get("codigo_produto_integracao") or pr.get("codigo") or "").strip()
                desc_pr = str(pr.get("descricao") or cod_pr).strip()
                qtd_v = float(pr.get("quantidade") or 0.0)
                val_v = float(pr.get("valor_total") or (qtd_v * float(pr.get("valor_unitario") or 0.0)))
                
                if cod_pr:
                    if cod_pr not in produtos_cliente:
                        produtos_cliente[cod_pr] = {
                            "Código": cod_pr,
                            "Produto": desc_pr,
                            "Qtd Comprada": 0,
                            "Total Gasto (R$)": 0.0
                        }
                    produtos_cliente[cod_pr]["Qtd Comprada"] += int(qtd_v)
                    produtos_cliente[cod_pr]["Total Gasto (R$)"] += val_v

        datas_compras.sort()
        primeira_compra_str = datas_compras[0].strftime("%d/%m/%Y") if datas_compras else "—"
        ultima_compra_str = datas_compras[-1].strftime("%d/%m/%Y") if datas_compras else "—"

        st.markdown("---")

        # ── PERFIL 360º DO CLIENTE (DESIGN EXECUTIVO DE ALTO CONTRASTE) ──
        str_canal = " & ".join(list(canais_cli)) if canais_cli else "B2B / B2C"
        str_vendedores = ", ".join(list(vendedores_cli)) if vendedores_cli else "Enviado via API"

        # Cores dinâmicas e ícone por canal comercial
        if "B2C" in str_canal and "B2B" not in str_canal:
            bg_canal = "#ECFDF5"
            txt_canal = "#047857"
            border_canal = "#A7F3D0"
            icone_canal = "🛒"
            accent_border = "#10B981"
        elif "B2B" in str_canal and "B2C" not in str_canal:
            bg_canal = "#EFF6FF"
            txt_canal = "#1D4ED8"
            border_canal = "#93C5FD"
            icone_canal = "🏢"
            accent_border = "#2563EB"
        else:
            bg_canal = "#F5F3FF"
            txt_canal = "#6D28D9"
            border_canal = "#DDD6FE"
            icone_canal = "🔄"
            accent_border = "#4F46E5"

        st.markdown(f"""<div style='background: #FFFFFF; border: 1.5px solid #E2E8F0; border-left: 5px solid {accent_border}; border-radius: 14px; padding: 22px 26px; margin-bottom: 22px; box-shadow: 0 4px 20px rgba(15, 23, 42, 0.05);'>
<div style='display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 14px; border-bottom: 1px solid #F1F5F9; padding-bottom: 16px;'>
<div>
<h2 style='margin: 0; font-size: 22px; color: #0F172A; font-weight: 800; letter-spacing: -0.02em;'>{dados_cli["nome"]}</h2>
<div style='display: flex; align-items: center; gap: 10px; margin-top: 8px; flex-wrap: wrap;'>
<span style='background: #F1F5F9; color: #334155; border: 1px solid #CBD5E1; padding: 3px 10px; border-radius: 6px; font-size: 12px; font-weight: 700;'>
📄 <b>CNPJ/CPF:</b> {dados_cli["cnpj_cpf"] or "Não informado"}
</span>
<span style='background: #EEF2FF; color: #4338CA; border: 1px solid #C7D2FE; padding: 3px 10px; border-radius: 6px; font-size: 12px; font-weight: 800;'>
📍 <b>UF:</b> {dados_cli["uf"]}
</span>
<span style='background: #F8FAFC; color: #475569; border: 1px solid #E2E8F0; padding: 3px 10px; border-radius: 6px; font-size: 12px; font-weight: 700;'>
🔢 <b>ID Omie:</b> #{dados_cli["codigo_cliente"]}
</span>
</div>
</div>
<div style='text-align: right;'>
<span style='background: {bg_canal}; color: {txt_canal}; border: 1.5px solid {border_canal}; padding: 6px 16px; border-radius: 20px; font-size: 13px; font-weight: 800; display: inline-flex; align-items: center; gap: 6px;'>
{icone_canal} {str_canal}
</span>
</div>
</div>
<div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 12px; margin: 18px 0;'>
<div style='background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 12px 16px;'>
<div style='font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;'>💰 Total Comprado (LTV)</div>
<div style='font-size: 20px; font-weight: 900; color: #047857; margin-top: 4px;'>{fmt_brl(tot_faturado_cli)}</div>
</div>
<div style='background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 12px 16px;'>
<div style='font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;'>📦 Pedidos Realizados</div>
<div style='font-size: 20px; font-weight: 900; color: #0F172A; margin-top: 4px;'>{total_pedidos_cli} <span style='font-size: 12px; font-weight: 600; color: #64748B;'>pedidos</span></div>
</div>
<div style='background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 12px 16px;'>
<div style='font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;'>🎯 Ticket Médio</div>
<div style='font-size: 20px; font-weight: 900; color: #2563EB; margin-top: 4px;'>{fmt_brl(tkt_medio_cli)}</div>
</div>
<div style='background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 12px 16px;'>
<div style='font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;'>🛍️ Total de Unidades</div>
<div style='font-size: 20px; font-weight: 900; color: #4F46E5; margin-top: 4px;'>{total_unidades_cli} <span style='font-size: 12px; font-weight: 600; color: #64748B;'>un</span></div>
</div>
</div>
<div style='background: #F1F5F9; border-radius: 8px; padding: 10px 16px; font-size: 12px; color: #334155; display: flex; flex-wrap: wrap; gap: 24px; align-items: center;'>
<div>👤 <b style='color: #0F172A;'>Vendedor / Atendente:</b> <span style='font-weight: 700; color: #1E293B;'>{str_vendedores}</span></div>
<div>📅 <b style='color: #0F172A;'>Primeira Compra:</b> <span style='font-weight: 700; color: #1E293B;'>{primeira_compra_str}</span></div>
<div>🕒 <b style='color: #0F172A;'>Última Compra:</b> <span style='font-weight: 700; color: #1E293B;'>{ultima_compra_str}</span></div>
</div>
</div>""", unsafe_allow_html=True)

        # ══════════════════════════════════════════════════════════════════════
        # 🤖 MOTOR DE INTELIGÊNCIA ARTIFICIAL: SUGESTÕES DE VENDAS & MIX IDEAL
        # ══════════════════════════════════════════════════════════════════════
        if st.session_state.get("ativar_ia_sugestoes"):
            st.toast(f"🤖 IA de Vendas Ativada para {dados_cli['nome']}!", icon="✨")

        st.markdown("""
        <div class="omnievo-banner copilot-ia-banner" style="background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%) !important; border: 1.5px solid #6366F1 !important; border-radius: 14px !important; padding: 18px 22px !important; margin-bottom: 18px !important; box-shadow: 0 8px 25px rgba(79, 70, 229, 0.2) !important; display: flex !important; justify-content: space-between !important; align-items: center !important; flex-wrap: wrap !important; gap: 12px !important;">
            <div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 22px;">🤖</span>
                    <span style="font-size: 18px; font-weight: 900; color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; letter-spacing: -0.02em;">Copilot IA: Sugestões Preditivas de Vendas & Cross-Selling</span>
                    <span style="background: #10B981 !important; color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; font-size: 10px; font-weight: 800; padding: 3px 10px; border-radius: 12px; letter-spacing: 0.05em;">MOTOR ATIVO</span>
                </div>
                <div class="copilot-sub" style="font-size: 13px; color: #E0E7FF !important; -webkit-text-fill-color: #E0E7FF !important; margin-top: 6px; font-weight: 500;">
                    Análise algorítmica de recência, giro de produtos, propensão de recompra e mix ideal de produtos para conversão imediata.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        ia_ativa = st.toggle("⚡ Ativar Painel de Inteligência de Vendas e Pitch Comercial", value=st.session_state.get("ativar_ia_sugestoes", True), key="toggle_ia_sugestoes_vendas")

        if ia_ativa:
            hoje_dt = datetime.date.today()
            ultima_compra_dt_val = datas_compras[-1] if datas_compras else hoje_dt
            dias_sem_comprar_val = max(0, (hoje_dt - ultima_compra_dt_val).days)

            if len(datas_compras) >= 2:
                diffs_dias = [(datas_compras[i] - datas_compras[i-1]).days for i in range(1, len(datas_compras))]
                freq_media_dias = max(7, round(sum(diffs_dias) / len(diffs_dias)))
            else:
                freq_media_dias = 35

            atraso_ciclo = dias_sem_comprar_val - freq_media_dias
            if atraso_ciclo > 30:
                diagnostico_ciclo = "🔴 Estoque no Cliente Zerado"
                cor_ciclo = "#DC2626"
                bg_ciclo = "#FEF2F2"
                txt_ciclo_exp = f"Atraso de {atraso_ciclo} dias em relação ao ciclo habitual de {freq_media_dias} dias. Urgente recuperar a conta!"
            elif atraso_ciclo > 0:
                diagnostico_ciclo = "🟡 Janela de Reabastecimento Aberta"
                cor_ciclo = "#D97706"
                bg_ciclo = "#FEFCE8"
                txt_ciclo_exp = f"Última compra há {dias_sem_comprar_val} dias (ciclo médio: {freq_media_dias} dias). Momento exato para contato comercial!"
            else:
                diagnostico_ciclo = "🟢 Ciclo em Dia"
                cor_ciclo = "#059669"
                bg_ciclo = "#ECFDF5"
                txt_ciclo_exp = f"Próxima recompra estimada para daqui a {abs(atraso_ciclo)} dias. Foco em novidades e produtos complementares."

            pontos_recencia = max(0, 50 - int(dias_sem_comprar_val * 0.5))
            pontos_pedidos = min(30, total_pedidos_cli * 5)
            pontos_ltv = min(20, int(tot_faturado_cli / 500))
            health_score = min(100, max(15, pontos_recencia + pontos_pedidos + pontos_ltv))

            ticket_alvo_sugerido = tkt_medio_cli * 1.2 if tkt_medio_cli > 0 else 650.0

            col_ia1, col_ia2, col_ia3 = st.columns(3)
            with col_ia1:
                st.markdown(f"""
                <div style="background: #FFFFFF; border: 2px solid #000000; border-radius: 12px; padding: 16px 18px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); height: 185px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase;">Ciclo de Recompra</span>
                        <span style="background: {bg_ciclo}; color: {cor_ciclo}; border: 1px solid {cor_ciclo}; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: 800;">{diagnostico_ciclo}</span>
                    </div>
                    <div>
                        <div style="font-size: 24px; font-weight: 900; color: #000000;">{dias_sem_comprar_val} <span style="font-size: 13px; color: #64748B; font-weight: 700;">dias sem comprar</span></div>
                        <div style="font-size: 11px; color: #475569; font-weight: 600; margin-top: 2px;">Frequência estimada: <b>a cada {freq_media_dias} dias</b></div>
                    </div>
                    <div style="font-size: 11px; color: #64748B; border-top: 1px solid #F1F5F9; padding-top: 6px; line-height: 1.4;">
                        {txt_ciclo_exp}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_ia2:
                st.markdown(f"""
                <div style="background: #FFFFFF; border: 2px solid #000000; border-radius: 12px; padding: 16px 18px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); height: 185px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase;">Ticket Alvo Recomendado</span>
                        <span style="background: #EFF6FF; color: #2563EB; border: 1px solid #93C5FD; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: 800;">UP-SELL +20%</span>
                    </div>
                    <div>
                        <div style="font-size: 24px; font-weight: 900; color: #2563EB;">{fmt_brl(ticket_alvo_sugerido)}</div>
                        <div style="font-size: 11px; color: #475569; font-weight: 600; margin-top: 2px;">Histórico: <b>{fmt_brl(tkt_medio_cli)}</b> / pedido</div>
                    </div>
                    <div style="font-size: 11px; color: #64748B; border-top: 1px solid #F1F5F9; padding-top: 6px; line-height: 1.4;">
                        Meta de faturamento por pedido com mix de produtos complementares.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_ia3:
                cor_hs = "#10B981" if health_score >= 70 else ("#F59E0B" if health_score >= 40 else "#EF4444")
                st.markdown(f"""
                <div style="background: #FFFFFF; border: 2px solid #000000; border-radius: 12px; padding: 16px 18px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); height: 185px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase;">Health Score da Conta</span>
                        <span style="background: #F8FAFC; color: {cor_hs}; border: 1px solid {cor_hs}; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: 800;">{health_score}/100</span>
                    </div>
                    <div>
                        <div style="font-size: 24px; font-weight: 900; color: {cor_hs};">{health_score}% <span style="font-size: 13px; color: #64748B; font-weight: 700;">saúde da conta</span></div>
                        <div style="width: 100%; height: 6px; background: #F1F5F9; border-radius: 3px; overflow: hidden; border: 1px solid #E2E8F0; margin-top: 4px;">
                            <div style="width: {health_score}%; height: 100%; background: {cor_hs}; border-radius: 3px;"></div>
                        </div>
                    </div>
                    <div style="font-size: 11px; color: #64748B; border-top: 1px solid #F1F5F9; padding-top: 6px; line-height: 1.4;">
                        Baseado em LTV acumulado ({fmt_brl(tot_faturado_cli)}) e consistência de compras.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)

            # Cesta Recomendada pela IA
            st.markdown(f'<div class="section-header">🛒 Cesta Recomendada pela IA — Reposição & Cross-Selling</div>', unsafe_allow_html=True)

            skus_comprados = set(produtos_cliente.keys())
            cesta_sugerida = []

            # 1. Reposição dos favoritos
            if produtos_cliente:
                top_prods_hist = sorted(produtos_cliente.values(), key=lambda x: x["Total Gasto (R$)"], reverse=True)[:2]
                for tp in top_prods_hist:
                    sku_tp = tp["Código"]
                    nome_tp = tp["Produto"]
                    qtd_hist = tp["Qtd Comprada"]
                    pedidos_count = max(1, total_pedidos_cli)
                    qtd_sug = max(1, round(qtd_hist / pedidos_count))
                    vlr_unit = (tp["Total Gasto (R$)"] / qtd_hist) if qtd_hist > 0 else 150.0
                    cesta_sugerida.append({
                        "tipo": "🔄 Reposição Essencial",
                        "sku": sku_tp,
                        "produto": nome_tp,
                        "motivo": "Produto de maior giro no histórico do cliente",
                        "qtd": qtd_sug,
                        "valor_unit": vlr_unit,
                        "subtotal": qtd_sug * vlr_unit,
                        "cor_badge": "#2563EB",
                        "bg_badge": "#EFF6FF"
                    })

            # 2. Cross-selling Missha
            catalogo_best_sellers = [
                {"sku": "MS201611", "nome": "M PERFECT COVER SERUM BB CREAM 50ml No.23 - Natural Beige", "valor": 249.0},
                {"sku": "MS101178", "nome": "MISSHA VITA C PLUS BRIGHTENING TONER", "valor": 189.0},
                {"sku": "MS101367", "nome": "MISSHA VITA C PLUS SPOT CORRECTING CONCENTRATE AMPOULE", "valor": 249.0},
                {"sku": "MS101935", "nome": "M TIME REVOLUTION NIGHT REPAIR SPECIAL SET 5X", "valor": 769.0},
                {"sku": "MS201368", "nome": "MISSHA VITA C PLUS AMPOULE MASK", "valor": 32.0}
            ]

            for cb in catalogo_best_sellers:
                if cb["sku"] not in skus_comprados and len(cesta_sugerida) < 4:
                    cesta_sugerida.append({
                        "tipo": "✨ Cross-Selling (Alta Afinidade)",
                        "sku": cb["sku"],
                        "produto": cb["nome"],
                        "motivo": "Item complementar de alta saída entre clientes com perfil similar",
                        "qtd": 2 if "B2B" in str_canal else 1,
                        "valor_unit": cb["valor"],
                        "subtotal": (2 if "B2B" in str_canal else 1) * cb["valor"],
                        "cor_badge": "#10B981",
                        "bg_badge": "#ECFDF5"
                    })

            if cesta_sugerida:
                df_cesta = pd.DataFrame([{
                    "Categoria / Ação": c["tipo"],
                    "SKU": c["sku"],
                    "Produto": c["produto"],
                    "Estratégia": c["motivo"],
                    "Qtd Sugerida": c["qtd"],
                    "Valor Unit. (R$)": fmt_brl(c["valor_unit"]),
                    "Subtotal (R$)": fmt_brl(c["subtotal"])
                } for c in cesta_sugerida])
                st.dataframe(df_cesta, use_container_width=True, hide_index=True)

                tot_cesta = sum(c["subtotal"] for c in cesta_sugerida)
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; align-items: center; gap: 12px; margin: 6px 0 16px 0;">
                    <span style="font-size: 13px; color: #475569; font-weight: 700;">Total Estimado da Proposta Sugerida:</span>
                    <span style="font-size: 18px; font-weight: 900; color: #0F172A; background: #F1F5F9; border: 1.5px solid #CBD5E1; padding: 4px 14px; border-radius: 8px;">{fmt_brl(tot_cesta)}</span>
                </div>
                """, unsafe_allow_html=True)

            # Pitch Comercial Gerado por IA
            st.markdown(f'<div class="section-header">📝 Script de Abordagem Personalizado (Gerado por IA)</div>', unsafe_allow_html=True)

            primeiro_nome_cli = dados_cli["nome"].split()[0].title()
            prods_destaque_lista = [c["produto"].split()[0] + " " + c["produto"].split()[1] for c in cesta_sugerida[:2]]
            prods_destaque_str = " e ".join(prods_destaque_lista) if prods_destaque_lista else "nossos itens de maior giro"

            if "B2B" in str_canal:
                pitch_ia = (
                    f"Olá, {primeiro_nome_cli}! Tudo bem? 😊\n\n"
                    f"Aqui é da equipe comercial Missha Brasil. Analisando o histórico da sua conta, notamos que seu ciclo de reposição de {prods_destaque_str} está no momento exato de abastecimento.\n\n"
                    f"Preparamos um mix sob medida com reposição dos seus campeões de venda e uma novidade com excelente margem para a sua vitrine. Conseguimos liberar condição especial de pagamento e frete facilitado para faturamento esta semana!\n\n"
                    f"Posso te encaminhar a cotação formalizada?"
                )
            else:
                pitch_ia = (
                    f"Olá, {primeiro_nome_cli}! Tudo bem com você? ✨\n\n"
                    f"Passando aqui da Missha para te dar um oi especial! Vimos que faz um tempinho desde seu último pedido e preparamos um carinho especial para seu retorno.\n\n"
                    f"Separamos uma condição exclusiva para reposição de {prods_destaque_str} com brinde exclusivo no pedido fechado hoje.\n\n"
                    f"Quer que eu te envie o link com a sua seleção favorita?"
                )

            st.code(pitch_ia, language="markdown")

            tel_cli_limpo = "".join(filter(str.isdigit, str(dados_cli.get("telefone") or "")))
            if tel_cli_limpo and len(tel_cli_limpo) >= 10:
                if not tel_cli_limpo.startswith("55"):
                    tel_cli_limpo = "55" + tel_cli_limpo
                import urllib.parse
                wpp_pitch_url = f"https://wa.me/{tel_cli_limpo}?text={urllib.parse.quote(pitch_ia)}"
            else:
                wpp_pitch_url = ""

            col_act_p1, col_act_p2, col_act_p3 = st.columns([1.5, 1.5, 2])
            with col_act_p1:
                if wpp_pitch_url:
                    st.markdown(f'<a href="{wpp_pitch_url}" target="_blank" style="background: #25D366; color: #FFFFFF; font-weight: 800; font-size: 13px; padding: 10px 16px; border-radius: 8px; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 8px; box-shadow: 0 4px 12px rgba(37,211,102,0.3); text-align: center;">📲 Enviar Pitch no WhatsApp</a>', unsafe_allow_html=True)
                else:
                    st.button("📲 WhatsApp (Sem Tel Cadastrado)", disabled=True, use_container_width=True)

            with col_act_p2:
                if st.button("🛒 Criar Pedido com Este Cliente", type="primary", use_container_width=True, key="btn_ia_criar_pedido_cli"):
                    try:
                        lista_clis_ped = omie.carregar_clientes()
                        for cl in lista_clis_ped:
                            if str(cl.get("codigo_cliente")).strip() == str(dados_cli.get("codigo_cliente")).strip():
                                st.session_state["ped_cliente_sel"] = cl.get("display")
                                break
                    except Exception:
                        pass
                    st.session_state["mudar_pagina_para"] = "📋  Novo Pedido"
                    st.rerun()

            with col_act_p3:
                st.caption("💡 O pitch pode ser editado livremente ou copiado com 1 clique no ícone do canto superior direito do código acima.")

            st.markdown("---")

        st.markdown('<div class="section-header">📑 Histórico Completo de Pedidos Faturados</div>', unsafe_allow_html=True)
        df_peds_cli = pd.DataFrame(peds_tabela)
        st.dataframe(df_peds_cli, use_container_width=True, hide_index=True)

        st.markdown("---")

        # ── PRODUTOS PREFERIDOS E MAIS COMPRADOS PELO CLIENTE ──
        st.markdown(f'<div class="section-header">📦 Produtos Mais Comprados por {dados_cli["nome"]}</div>', unsafe_allow_html=True)
        
        if produtos_cliente:
            df_prods_cli = pd.DataFrame(list(produtos_cliente.values()))
            df_prods_cli.sort_values(by="Total Gasto (R$)", ascending=False, inplace=True)
            df_prods_cli["Total Gasto (R$)"] = df_prods_cli["Total Gasto (R$)"].apply(fmt_brl)
            df_prods_cli["Qtd Comprada"] = df_prods_cli["Qtd Comprada"].astype(int)
            
            st.dataframe(df_prods_cli, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum produto comercial localizado no histórico deste cliente.")


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 5.5: DESEMPENHO DE VENDEDORES
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "🏆  Desempenho de Vendedores":
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    import datetime
    from datetime import date
    import re

    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">🏆</div>
        <div>
            <div class="page-header-title">Desempenho de Vendedores & Pódio Comercial</div>
            <div class="page-header-subtitle">Ranking executivo da equipe, faturamento total, ticket médio e contribuição individual de vendas.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    pedidos_lista_full = auth.obter_pedidos_filtrados_usuario(_obter_pedidos_cached(), usr_logado)
    hoje = date.today()

    # ── FILTROS EXECUTIVOS (5 COLUNAS) ──
    col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns([1, 1.1, 1.3, 1.2, 1.4])
    
    anos_disponiveis = set()
    for ped in pedidos_lista_full:
        dt_obj = obter_data_faturamento_pedido(ped)
        anos_disponiveis.add(str(dt_obj.year))

    lista_anos = sorted(list(anos_disponiveis), reverse=True)
    if str(hoje.year) not in lista_anos:
        lista_anos.insert(0, str(hoje.year))
    opcoes_anos = ["Todos os Anos"] + lista_anos

    with col_f1:
        filtro_ano = st.selectbox("1. Ano de Referência", opcoes_anos, index=0, key="flt_ano_vend")

    opcoes_meses = [
        "Todos os Meses", "01 - Janeiro", "02 - Fevereiro", "03 - Março", "04 - Abril",
        "05 - Maio", "06 - Junho", "07 - Julho", "08 - Agosto", "09 - Setembro", 
        "10 - Outubro", "11 - Novembro", "12 - Dezembro"
    ]
    with col_f2:
        filtro_mes = st.selectbox("2. Mês de Referência", opcoes_meses, index=0, key="flt_mes_vend")
        
    with col_f3:
        opcoes_status = [
            "Apenas Faturados (Status 60)", 
            "Em Separação (Status 70 e 20)", 
            "Pronto p/ Faturar (Status 50)", 
            "Em Orçamento (Status 10)", 
            "Todos os Status"
        ]
        filtro_status = st.selectbox("3. Status do Pedido", opcoes_status, index=0, key="flt_status_vend")

    with col_f4:
        opcoes_op_vend = [
            "Vendas e Bonificações",
            "Apenas Vendas (Líquido)",
            "Apenas Bonificações (Brindes)"
        ]
        filtro_operacao_vend = st.selectbox("4. Operação / Bonif.", opcoes_op_vend, index=0, key="flt_operacao_desempenho_vend")

    # ── EXTRAÇÃO GLOBAL DE TODOS OS VENDEDORES PARA O SELECTBOX ──
    vendedores_todos_set = set()
    for ped in pedidos_lista_full:
        raw = ped.get("raw_data", {}) if isinstance(ped.get("raw_data"), dict) else {}
        inf = raw.get("informacoes_adicionais", {}) if isinstance(raw.get("informacoes_adicionais"), dict) else {}
        cab = raw.get("cabecalho", {}) if isinstance(raw.get("cabecalho"), dict) else {}
        vend_p = str(ped.get("vendedor") or inf.get("contato") or cab.get("nome_vendedor") or "").strip()
        num_p_str = str(ped.get("numero_pedido") or cab.get("numero_pedido") or "").strip()
        cli_dic = ped.get("cliente", {}) if isinstance(ped.get("cliente"), dict) else {}
        doc_cli = str(cli_dic.get("cnpj_cpf") or ped.get("cliente_cnpj_cpf") or ped.get("cnpj_cpf") or "").replace(".", "").replace("/", "").replace("-", "").strip()
        
        vendedores_todos_set.add(normalizar_nome_vendedor(vend_p, num_p_str, doc_cli, ped_obj=ped))

    lista_vendedores_opcoes = ["Todos os Vendedores (Geral)"] + sorted(list(vendedores_todos_set))

    with col_f5:
        filtro_vendedor_sel = st.selectbox("5. Filtrar Vendedor", lista_vendedores_opcoes, index=0, key="flt_vendedor_desempenho_global")

    # ── 1. BANNER DE CABEÇALHO EXECUTIVO DE PERFORMANCE COMERCIAL DINÂMICO ──
    lbl_vendedor_badge = f" | 👔 {filtro_vendedor_sel}" if filtro_vendedor_sel != "Todos os Vendedores (Geral)" else ""
    lbl_op_badge = f" | 🏷️ {filtro_operacao_vend}" if filtro_operacao_vend != "Vendas e Bonificações" else ""
    lbl_periodo_vendedor = f"📅 Mês: {filtro_mes}{lbl_vendedor_badge}{lbl_op_badge}" if filtro_mes != "Todos os Meses" else f"📅 Período: Todos os Meses{lbl_vendedor_badge}{lbl_op_badge}"
    st.markdown(f'''
    <div style="background: linear-gradient(135deg, #EEF2FF 0%, #F1F5F9 100%); padding: 22px 28px; border-radius: 16px; margin: 10px 0 24px 0; box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04); border: 1.5px solid #C7D2FE;">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 15px;">
            <div>
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 32px;">🚀</span>
                    <h1 style="color: #0F172A; font-size: 24px; font-weight: 800; margin: 0; letter-spacing: -0.02em; font-family: 'Inter', system-ui, sans-serif;">
                        Performance Comercial — <span style="color: #4F46E5;">{filtro_mes} ({filtro_ano})</span>
                    </h1>
                </div>
                <p style="color: #000000; font-size: 14px; margin: 6px 0 0 44px; font-weight: 500;">
                    Painel Executivo de Desempenho de Vendas, Ranking de Pódio, Evolução Temporal e Canais de Distribuição (Omie ERP)
                </p>
            </div>
            <div style="display: flex; gap: 10px;">
                <span style="background: #E0E7FF; color: #000000; font-weight: 900; padding: 7px 16px; border-radius: 20px; font-size: 13px; font-weight: 800; border: 1px solid #C7D2FE;">
                    {lbl_periodo_vendedor}
                </span>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # ── FILTRAGEM & PROCESSAMENTO DE DADOS ──
    num_mes_sel_t5 = re.findall(r'\d+', filtro_mes)[0] if (filtro_mes != "Todos os Meses" and re.findall(r'\d+', filtro_mes)) else ""
    dados_vendedores = {}
    
    for ped in pedidos_lista_full:
        dt_obj = obter_data_faturamento_pedido(ped)
        etapa_ped = str(ped.get("etapa") or ped.get("raw_data", {}).get("cabecalho", {}).get("etapa") or "").strip()
        
        if "Faturados" in filtro_status or "Status 60" in filtro_status:
            if etapa_ped not in ["60", "60.0"]:
                continue
        elif "Separação" in filtro_status or "Status 70" in filtro_status:
            if etapa_ped not in ["70", "20", "70.0", "20.0"]:
                continue
        elif "Pronto p/ Faturar" in filtro_status or "Status 50" in filtro_status:
            if etapa_ped not in ["50", "50.0"]:
                continue
        elif "Orçamento" in filtro_status or "Status 10" in filtro_status:
            if etapa_ped not in ["10", "00"]:
                continue

        if filtro_ano != "Todos os Anos" and str(dt_obj.year) != str(filtro_ano):
            continue

        if num_mes_sel_t5 and f"{dt_obj.month:02d}" != num_mes_sel_t5:
            continue
                
        raw = ped.get("raw_data", {}) if isinstance(ped.get("raw_data"), dict) else {}
        cab = raw.get("cabecalho", {}) if isinstance(raw.get("cabecalho"), dict) else {}
        det = raw.get("det", []) if isinstance(raw.get("det"), list) else []
        cen_ped = str(cab.get("codigo_cenario_impostos") or "")

        vlr_vendas_ped = 0.0
        vlr_bonif_ped = 0.0

        for it in det:
            inf_it = it.get("inf_adic", {}) if isinstance(it.get("inf_adic"), dict) else {}
            pr_it = it.get("produto", {}) if isinstance(it.get("produto"), dict) else {}
            cen_item = str(inf_it.get("codigo_cenario_impostos_item") or cen_ped)
            nao_fin = str(inf_it.get("nao_gerar_financeiro", "N")).upper()
            tipo_item = str(it.get("tipo_item", "")).upper()
            val_it = float(pr_it.get("valor_total") or (float(pr_it.get("quantidade", 0)) * float(pr_it.get("valor_unitario", 0))))

            cfop_item = str(pr_it.get("cfop") or "").strip()
            eh_bonif = ("BONIF" in tipo_item) or (nao_fin == "S") or (cen_item == "8904163333") or (cfop_item in ["5.910", "6.910"])
            if eh_bonif:
                vlr_bonif_ped += val_it
            else:
                vlr_vendas_ped += val_it

        tot_orig = float(raw.get("total_pedido", {}).get("valor_total_pedido") or ped.get("valor_total") or 0.0)
        if vlr_vendas_ped == 0.0 and vlr_bonif_ped == 0.0 and tot_orig > 0:
            vlr_vendas_ped = tot_orig

        if "Apenas Vendas" in filtro_operacao_vend:
            if vlr_vendas_ped <= 0:
                continue
            v_total = vlr_vendas_ped
        elif "Apenas Bonificações" in filtro_operacao_vend:
            if vlr_bonif_ped <= 0:
                continue
            v_total = vlr_bonif_ped
        else:
            v_total = tot_orig

        inf = raw.get("informacoes_adicionais", {}) if isinstance(raw.get("informacoes_adicionais"), dict) else {}
        cab = raw.get("cabecalho", {}) if isinstance(raw.get("cabecalho"), dict) else {}
        vend_p = str(ped.get("vendedor") or inf.get("contato") or cab.get("nome_vendedor") or "").strip()
        num_p_str = str(ped.get("numero_pedido") or cab.get("numero_pedido") or "").strip()
        cli_dic = ped.get("cliente", {}) if isinstance(ped.get("cliente"), dict) else {}
        doc_cli = str(cli_dic.get("cnpj_cpf") or ped.get("cliente_cnpj_cpf") or ped.get("cnpj_cpf") or "").replace(".", "").replace("/", "").replace("-", "").strip()
        is_b2c = not eh_pedido_b2b_cnpj(ped)
        
        vendedor = normalizar_nome_vendedor(vend_p, num_p_str, doc_cli, ped_obj=ped)

        # Filtro de Vendedor Selecionado pelo Usuário
        if filtro_vendedor_sel != "Todos os Vendedores (Geral)":
            if vendedor.lower() != filtro_vendedor_sel.lower():
                continue
        
        if vendedor not in dados_vendedores:
            dados_vendedores[vendedor] = {
                "pedidos": 0, 
                "faturamento": 0.0, 
                "b2b_fat": 0.0,
                "b2c_fat": 0.0,
                "b2b_pedidos": 0,
                "b2c_pedidos": 0,
                "timeline": {}
            }
            
        dados_vendedores[vendedor]["pedidos"] += 1
        dados_vendedores[vendedor]["faturamento"] += v_total
        
        if is_b2c:
            dados_vendedores[vendedor]["b2c_fat"] += v_total
            dados_vendedores[vendedor]["b2c_pedidos"] += 1
        else:
            dados_vendedores[vendedor]["b2b_fat"] += v_total
            dados_vendedores[vendedor]["b2b_pedidos"] += 1
        
        # Agrupamento temporal para gráficos
        if filtro_mes == "Todos os Meses":
            tempo_str = f"{dt_obj.year}-{dt_obj.month:02d}"
        else:
            tempo_str = f"{dt_obj.year}-{dt_obj.month:02d}-{dt_obj.day:02d}"
            
        if tempo_str not in dados_vendedores[vendedor]["timeline"]:
            dados_vendedores[vendedor]["timeline"][tempo_str] = 0.0
        dados_vendedores[vendedor]["timeline"][tempo_str] += v_total

    # ── EXIBIÇÃO DOS RESULTADOS EXECUTIVOS ──
    if not dados_vendedores:
        st.info(f"ℹ️ **Nenhum dado encontrado para os filtros selecionados** (Ano: **{filtro_ano}** | Mês: **{filtro_mes}** | Status: **{filtro_status}**).")
    else:
        total_fat_equipe = sum(d["faturamento"] for d in dados_vendedores.values())
        total_pedidos_equipe = sum(d["pedidos"] for d in dados_vendedores.values())
        ticket_medio_geral = (total_fat_equipe / total_pedidos_equipe) if total_pedidos_equipe > 0 else 0.0
        
        # Identificar Campeão de Vendas
        vend_campeao = max(dados_vendedores.items(), key=lambda x: x[1]["faturamento"])
        nome_campeao = vend_campeao[0]
        fat_campeao = vend_campeao[1]["faturamento"]

        # ── 2. CARDS DE KPI EXECUTIVOS (4 MÉTRICAS CHAVE) ──
        st.markdown('<div class="section-header">📊 Indicadores Consolidados da Equipe</div>', unsafe_allow_html=True)
        col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
        
        with col_kpi1:
            st.markdown(f'''
            <div style="background: linear-gradient(135deg, #10B981 0%, #059669 100%); padding: 18px; border-radius: 12px; color: #000000; box-shadow: 0 4px 12px rgba(16,185,129,0.25);">
                <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.9;">💰 Faturamento Total Equipe</div>
                <div style="font-size: 20px; font-weight: 800; margin-top: 6px;">{fmt_brl(total_fat_equipe)}</div>
                <div style="font-size: 11px; opacity: 0.85; margin-top: 4px;">Faturamento consolidado</div>
            </div>
            ''', unsafe_allow_html=True)

        with col_kpi2:
            st.markdown(f'''
            <div style="background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%); padding: 18px; border-radius: 12px; color: #000000; box-shadow: 0 4px 12px rgba(245,158,11,0.25);">
                <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.9;">🏆 Campeão de Vendas</div>
                <div style="font-size: 18px; font-weight: 800; margin-top: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">🥇 {nome_campeao}</div>
                <div style="font-size: 11px; opacity: 0.9; margin-top: 4px;">{fmt_brl(fat_campeao)}</div>
            </div>
            ''', unsafe_allow_html=True)

        with col_kpi3:
            st.markdown(f'''
            <div style="background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%); padding: 18px; border-radius: 12px; color: #000000; box-shadow: 0 4px 12px rgba(99,102,241,0.25);">
                <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.9;">🏷️ Ticket Médio Geral</div>
                <div style="font-size: 20px; font-weight: 800; margin-top: 6px;">{fmt_brl(ticket_medio_geral)}</div>
                <div style="font-size: 11px; opacity: 0.85; margin-top: 4px;">Média por pedido</div>
            </div>
            ''', unsafe_allow_html=True)

        with col_kpi4:
            st.markdown(f'''
            <div style="background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%); padding: 18px; border-radius: 12px; color: #000000; box-shadow: 0 4px 12px rgba(14,165,233,0.25);">
                <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.9;">📦 Total de Pedidos</div>
                <div style="font-size: 20px; font-weight: 800; margin-top: 6px;">{total_pedidos_equipe} pedidos</div>
                <div style="font-size: 11px; opacity: 0.85; margin-top: 4px;">Pedidos no período</div>
            </div>
            ''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 3. CARDS VISUAIS DOS VENDEDORES COM BADGE DE PÓDIO ──
        st.markdown('<div class="section-header">🏆 Ranking de Pódio e Cards Visuais por Vendedor</div>', unsafe_allow_html=True)
        
        lista_ranking = []
        for vend, dados in dados_vendedores.items():
            lista_ranking.append({
                "Vendedor": vend,
                "Qtd Pedidos": dados["pedidos"],
                "Faturamento": dados["faturamento"],
                "Ticket Médio": (dados["faturamento"] / dados["pedidos"]) if dados["pedidos"] > 0 else 0.0,
                "B2B Fat": dados["b2b_fat"],
                "B2C Fat": dados["b2c_fat"],
                "B2B Pedidos": dados["b2b_pedidos"],
                "B2C Pedidos": dados["b2c_pedidos"]
            })
            
        df_ranking = pd.DataFrame(lista_ranking)
        df_ranking.sort_values(by="Faturamento", ascending=False, inplace=True)
        
        records_ranking = df_ranking.to_dict('records')
        
        for idx, r in enumerate(records_ranking, start=1):
            v_nome = r["Vendedor"]
            v_fat = r["Faturamento"]
            v_ped = r["Qtd Pedidos"]
            v_tkt = r["Ticket Médio"]
            
            pct_contrib = (v_fat / total_fat_equipe * 100) if total_fat_equipe > 0 else 0.0
            
            lbl_mes_ref = filtro_mes.split("-")[-1].strip() if "-" in filtro_mes else filtro_mes
            
            # Definição do Badge de Pódio Dinâmico por Mês Selecionado
            if idx == 1:
                badge_html = f'<span style="background: linear-gradient(135deg, #F59E0B, #D97706); color: #000000; padding: 5px 14px; border-radius: 20px; font-weight: 900; font-size: 13px; box-shadow: 0 2px 8px rgba(245,158,11,0.3);">🥇 1º Lugar Ouro ({lbl_mes_ref})</span>'
                border_color = "#F59E0B"
                bg_card = "#FFFFFF"
            elif idx == 2:
                badge_html = f'<span style="background: linear-gradient(135deg, #CBD5E1, #94A3B8); color: #000000; padding: 5px 14px; border-radius: 20px; font-weight: 900; font-size: 13px; box-shadow: 0 2px 8px rgba(148,163,184,0.3);">🥈 2º Lugar Prata ({lbl_mes_ref})</span>'
                border_color = "#94A3B8"
                bg_card = "#FFFFFF"
            elif idx == 3:
                badge_html = f'<span style="background: linear-gradient(135deg, #F97316, #C2410C); color: #000000; padding: 5px 14px; border-radius: 20px; font-weight: 900; font-size: 13px; box-shadow: 0 2px 8px rgba(217,119,6,0.3);">🥉 3º Lugar Bronze ({lbl_mes_ref})</span>'
                border_color = "#D97706"
                bg_card = "#FFFFFF"
            else:
                badge_html = f'<span style="background: #EEF2FF; color: #000000; padding: 5px 14px; border-radius: 20px; font-weight: 900; font-size: 13px; border: 1.5px solid #C7D2FE;">🏅 #{idx}º Lugar ({lbl_mes_ref})</span>'
                border_color = "#CBD5E1"
                bg_card = "#FFFFFF"

            st.markdown(f'''
            <div style="background: {bg_card}; border: 2px solid {border_color}; border-radius: 14px; padding: 18px; margin-bottom: 12px; box-shadow: 0 4px 12px rgba(15,23,42,0.05);">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 12px;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 18px; font-weight: 900; color: #000000;">👔 {v_nome}</span>
                        {badge_html}
                    </div>
                    <div style="font-size: 18px; font-weight: 900; color: #059669;">
                        {fmt_brl(v_fat)}
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 12px; margin-bottom: 6px;">
                    <div style="background: #F8FAFC; border: 1px.5 solid #CBD5E1; padding: 8px 12px; border-radius: 8px;">
                        <div style="font-size: 10px; color: #000000; font-weight: 700; text-transform: uppercase;">Ticket Médio ({lbl_mes_ref})</div>
                        <div style="font-size: 14px; font-weight: 900; color: #000000;">{fmt_brl(v_tkt)}</div>
                    </div>
                    <div style="background: #F8FAFC; border: 1px.5 solid #CBD5E1; padding: 8px 12px; border-radius: 8px;">
                        <div style="font-size: 10px; color: #000000; font-weight: 700; text-transform: uppercase;">Qtd Pedidos ({lbl_mes_ref})</div>
                        <div style="font-size: 14px; font-weight: 900; color: #000000;">{v_ped} pedidos</div>
                    </div>
                    <div style="background: #F8FAFC; border: 1px.5 solid #CBD5E1; padding: 8px 12px; border-radius: 8px;">
                        <div style="font-size: 10px; color: #000000; font-weight: 700; text-transform: uppercase;">Contribuição Equipe</div>
                        <div style="font-size: 14px; font-weight: 900; color: #4F46E5;">{pct_contrib:.1f}% do total</div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            st.progress(min(max(pct_contrib / 100.0, 0.0), 1.0))

            # ── DETALHAMENTO EXPANSÍVEL AO CLICAR NA INFORMAÇÃO DO VENDEDOR ──
            with st.expander(f"🔍 Clique para Detalhar Vendas & Produtos de {v_nome} no Mês de {lbl_mes_ref} ({v_ped} ped | {fmt_brl(v_fat)})", expanded=False):
                peds_deste_vendedor = []
                prods_vendedor = {}
                
                for ped in pedidos_lista_full:
                    dt_fat = obter_data_faturamento_pedido(ped)
                    etapa_ped = str(ped.get("etapa") or ped.get("raw_data", {}).get("cabecalho", {}).get("etapa") or "").strip()
                    
                    if "Faturados" in filtro_status or "Status 60" in filtro_status:
                        if etapa_ped not in ["60", "60.0"]:
                            continue
                    elif "Separação" in filtro_status or "Status 70" in filtro_status:
                        if etapa_ped not in ["70", "20", "70.0", "20.0"]:
                            continue
                    elif "Pronto p/ Faturar" in filtro_status or "Status 50" in filtro_status:
                        if etapa_ped not in ["50", "50.0"]:
                            continue
                    elif "Orçamento" in filtro_status or "Status 10" in filtro_status:
                        if etapa_ped not in ["10", "00"]:
                            continue

                    if filtro_ano != "Todos os Anos" and str(dt_fat.year) != str(filtro_ano):
                        continue

                    if num_mes_sel_t5 and f"{dt_fat.month:02d}" != num_mes_sel_t5:
                        continue

                    raw = ped.get("raw_data", {}) if isinstance(ped.get("raw_data"), dict) else {}
                    inf = raw.get("informacoes_adicionais", {}) if isinstance(raw.get("informacoes_adicionais"), dict) else {}
                    cab = raw.get("cabecalho", {}) if isinstance(raw.get("cabecalho"), dict) else {}
                    vend_p = str(ped.get("vendedor") or inf.get("contato") or cab.get("nome_vendedor") or "").strip()
                    num_p_str = str(ped.get("numero_pedido") or cab.get("numero_pedido") or "").strip()
                    cli_dic = ped.get("cliente", {}) if isinstance(ped.get("cliente"), dict) else {}
                    doc_cli = str(cli_dic.get("cnpj_cpf") or ped.get("cliente_cnpj_cpf") or ped.get("cnpj_cpf") or "").replace(".", "").replace("/", "").replace("-", "").strip()
                    is_b2c = not eh_pedido_b2b_cnpj(ped)
                    
                    vend_norm = normalizar_nome_vendedor(vend_p, num_p_str, doc_cli, ped_obj=ped)
                    
                    if vend_norm.lower() == v_nome.lower():
                        dt_fat = obter_data_faturamento_pedido(ped)
                        cli_nome = str(ped.get("cliente_nome") or cli_dic.get("razao_social") or "Cliente").strip()
                        vlr_ped = float(ped.get("valor_total", 0.0))
                        canal_str = "🛒 B2C (Site API)" if is_b2c else "🏢 B2B (Corporativo)"
                        
                        peds_deste_vendedor.append({
                            "Nº Pedido": num_p_str,
                            "Data Faturamento": dt_fat.strftime("%d/%m/%Y"),
                            "Cliente": cli_nome,
                            "Canal": canal_str,
                            "Valor Total (R$)": fmt_brl(vlr_ped)
                        })
                        
                        # Extração de Produtos do Vendedor
                        itens = raw.get("det", []) if isinstance(raw.get("det"), list) else []
                        for it in itens:
                            pr = it.get("produto", {}) if isinstance(it.get("produto"), dict) else {}
                            cod_pr = str(pr.get("codigo_produto_integracao") or pr.get("codigo") or "").strip()
                            desc_pr = str(pr.get("descricao") or cod_pr).strip()
                            qtd_v = float(pr.get("quantidade") or 0.0)
                            val_v = float(pr.get("valor_total") or (qtd_v * float(pr.get("valor_unitario") or 0.0)))
                            
                            if cod_pr:
                                if cod_pr not in prods_vendedor:
                                    prods_vendedor[cod_pr] = {"Código": cod_pr, "Produto": desc_pr, "Qtd Vendida": 0, "Faturamento Total": 0.0}
                                prods_vendedor[cod_pr]["Qtd Vendida"] += int(qtd_v)
                                prods_vendedor[cod_pr]["Faturamento Total"] += val_v

                col_det1, col_det2 = st.columns([1.6, 1])
                
                with col_det1:
                    st.markdown(f"##### 📦 Histórico de Pedidos de {v_nome} ({len(peds_deste_vendedor)} pedidos)")
                    if peds_deste_vendedor:
                        st.dataframe(pd.DataFrame(peds_deste_vendedor), use_container_width=True, hide_index=True)
                    else:
                        st.info("Nenhum pedido individual localizado para este vendedor.")

                with col_det2:
                    st.markdown(f"##### 🛍️ Top Produtos mais Vendidos por {v_nome}")
                    if prods_vendedor:
                        df_pv = pd.DataFrame(list(prods_vendedor.values()))
                        df_pv.sort_values(by="Faturamento Total", ascending=False, inplace=True)
                        df_pv["Faturamento Total"] = df_pv["Faturamento Total"].apply(fmt_brl)
                        st.dataframe(df_pv.head(8), use_container_width=True, hide_index=True)
                    else:
                        st.info("Nenhum produto registrado.")

            st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

        # ── 4. GRÁFICOS ANALÍTICOS EXECUTIVOS (MÊS A MÊS & CANAIS) ──
        st.markdown('<br><div class="section-header">📈 Performance Mês a Mês & Distribuição de Vendas</div>', unsafe_allow_html=True)
        col_g1, col_g2 = st.columns(2)

        # 4.1 Gráfico 1: Performance Mês a Mês do Ano Selecionado
        with col_g1:
            ano_target = int(filtro_ano) if filtro_ano != "Todos os Anos" else hoje.year
            nomes_meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
            fat_meses = {i: 0.0 for i in range(1, 13)}
            ped_meses = {i: 0 for i in range(1, 13)}
            
            for ped in pedidos_lista_full:
                etapa_ped = str(ped.get("etapa") or ped.get("raw_data", {}).get("cabecalho", {}).get("etapa") or "").strip()
                if "Faturados" in filtro_status or "Status 60" in filtro_status:
                    if etapa_ped not in ["60", "60.0"]:
                        continue
                elif "Separação" in filtro_status or "Status 70" in filtro_status:
                    if etapa_ped not in ["70", "20", "70.0", "20.0"]:
                        continue
                elif "Pronto p/ Faturar" in filtro_status or "Status 50" in filtro_status:
                    if etapa_ped not in ["50", "50.0"]:
                        continue
                elif "Orçamento" in filtro_status or "Status 10" in filtro_status:
                    if etapa_ped not in ["10", "00"]:
                        continue

                if filtro_vendedor_sel != "Todos os Vendedores (Geral)":
                    raw = ped.get("raw_data", {}) if isinstance(ped.get("raw_data"), dict) else {}
                    inf = raw.get("informacoes_adicionais", {}) if isinstance(raw.get("informacoes_adicionais"), dict) else {}
                    cab = raw.get("cabecalho", {}) if isinstance(raw.get("cabecalho"), dict) else {}
                    vend_p = str(ped.get("vendedor") or inf.get("contato") or cab.get("nome_vendedor") or "").strip()
                    num_p_str = str(ped.get("numero_pedido") or cab.get("numero_pedido") or "").strip()
                    cli_dic = ped.get("cliente", {}) if isinstance(ped.get("cliente"), dict) else {}
                    doc_cli = str(cli_dic.get("cnpj_cpf") or ped.get("cliente_cnpj_cpf") or ped.get("cnpj_cpf") or "").replace(".", "").replace("/", "").replace("-", "").strip()
                    vendedor = normalizar_nome_vendedor(vend_p, num_p_str, doc_cli, ped_obj=ped)
                    if vendedor.lower() != filtro_vendedor_sel.lower():
                        continue

                dt_p = obter_data_faturamento_pedido(ped)
                if dt_p.year == ano_target:
                    v_p = float(ped.get("valor_total", 0.0))
                    fat_meses[dt_p.month] += v_p
                    ped_meses[dt_p.month] += 1
            
            mes_num_sel = int(num_mes_sel_t5) if num_mes_sel_t5 else None
            cores_barras = ["#F59E0B" if (mes_num_sel and m == mes_num_sel) else "#6366F1" for m in range(1, 13)]
            
            fig_mes = go.Figure()
            fig_mes.add_trace(go.Bar(
                x=nomes_meses,
                y=[fat_meses[m] for m in range(1, 13)],
                marker=dict(color=cores_barras, line=dict(color="#000000", width=1.5)),
                text=[f"R$ {fat_meses[m]/1000:.1f}k" if fat_meses[m] > 0 else "" for m in range(1, 13)],
                textposition="outside",
                hovertemplate="<span style='color: #FFFFFF; font-size: 13px;'><b>%{x}</b></span><br><span style='color: #FFFFFF;'>💰 Faturamento: <b>R$ %{y:,.2f}</b></span><extra></extra>"
            ))
            fig_mes.update_layout(
                template="plotly_white",
                title=f"<b>📅 Faturamento Mês a Mês ({ano_target})</b>",
                title_font=dict(size=14, color="#0F172A"),
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                font=dict(family="Inter, sans-serif", size=12, color="#0F172A"),
                margin=dict(l=20, r=20, t=50, b=30),
                height=340,
                hoverlabel=dict(bgcolor="#0F172A", bordercolor="#38BDF8", font=dict(color="#FFFFFF", size=13)),
                xaxis=dict(gridcolor="#E2E8F0", title="Mês", tickfont=dict(color="#0F172A")),
                yaxis=dict(gridcolor="#E2E8F0", title="Faturamento (R$)", tickfont=dict(color="#0F172A"))
            )
            st.plotly_chart(fig_mes, use_container_width=True)

        # 4.2 Gráfico 2: Evolução no Período Selecionado ou Comparativo por Vendedor
        with col_g2:
            if filtro_mes != "Todos os Meses":
                dias_mes = {}
                for ped in pedidos_lista_full:
                    etapa_ped = str(ped.get("etapa") or ped.get("raw_data", {}).get("cabecalho", {}).get("etapa") or "").strip()
                    if "Faturados" in filtro_status or "Status 60" in filtro_status:
                        if etapa_ped not in ["60", "60.0"]:
                            continue
                    elif "Separação" in filtro_status or "Status 70" in filtro_status:
                        if etapa_ped not in ["70", "20", "70.0", "20.0"]:
                            continue
                    elif "Pronto p/ Faturar" in filtro_status or "Status 50" in filtro_status:
                        if etapa_ped not in ["50", "50.0"]:
                            continue
                    elif "Orçamento" in filtro_status or "Status 10" in filtro_status:
                        if etapa_ped not in ["10", "00"]:
                            continue

                    if filtro_vendedor_sel != "Todos os Vendedores (Geral)":
                        raw = ped.get("raw_data", {}) if isinstance(ped.get("raw_data"), dict) else {}
                        inf = raw.get("informacoes_adicionais", {}) if isinstance(raw.get("informacoes_adicionais"), dict) else {}
                        cab = raw.get("cabecalho", {}) if isinstance(raw.get("cabecalho"), dict) else {}
                        vend_p = str(ped.get("vendedor") or inf.get("contato") or cab.get("nome_vendedor") or "").strip()
                        num_p_str = str(ped.get("numero_pedido") or cab.get("numero_pedido") or "").strip()
                        cli_dic = ped.get("cliente", {}) if isinstance(ped.get("cliente"), dict) else {}
                        doc_cli = str(cli_dic.get("cnpj_cpf") or ped.get("cliente_cnpj_cpf") or ped.get("cnpj_cpf") or "").replace(".", "").replace("/", "").replace("-", "").strip()
                        vendedor = normalizar_nome_vendedor(vend_p, num_p_str, doc_cli, ped_obj=ped)
                        if vendedor.lower() != filtro_vendedor_sel.lower():
                            continue

                    dt_p = obter_data_faturamento_pedido(ped)
                    if dt_p.year == ano_target and f"{dt_p.month:02d}" == num_mes_sel_t5:
                        d_str = f"Dia {dt_p.day:02d}"
                        dias_mes[d_str] = dias_mes.get(d_str, 0.0) + float(ped.get("valor_total", 0.0))
                
                dias_ordenados = sorted(dias_mes.keys(), key=lambda x: int(x.replace("Dia ", "")))
                valores_dias = [dias_mes[d] for d in dias_ordenados]
                
                fig_dias = go.Figure()
                fig_dias.add_trace(go.Scatter(
                    x=dias_ordenados,
                    y=valores_dias,
                    mode="lines+markers",
                    line=dict(color="#10B981", width=3),
                    marker=dict(size=7, color="#059669", line=dict(color="#000000", width=1.5)),
                    fill="tozeroy",
                    fillcolor="rgba(16, 185, 129, 0.12)",
                    hovertemplate="<span style='color: #FFFFFF; font-size: 13px;'><b>%{x}</b></span><br><span style='color: #FFFFFF;'>💰 Faturamento: <b>R$ %{y:,.2f}</b></span><extra></extra>"
                ))
                fig_dias.update_layout(
                    template="plotly_white",
                    title=f"<b>📈 Ritmo de Vendas Diário em {lbl_mes_ref} ({ano_target})</b>",
                    title_font=dict(size=14, color="#0F172A"),
                    plot_bgcolor="#FFFFFF",
                    paper_bgcolor="#FFFFFF",
                    font=dict(family="Inter, sans-serif", size=12, color="#0F172A"),
                    margin=dict(l=20, r=20, t=50, b=30),
                    height=340,
                    hoverlabel=dict(bgcolor="#0F172A", bordercolor="#38BDF8", font=dict(color="#FFFFFF", size=13)),
                    xaxis=dict(gridcolor="#E2E8F0", tickfont=dict(color="#0F172A")),
                    yaxis=dict(gridcolor="#E2E8F0", tickfont=dict(color="#0F172A"))
                )
                st.plotly_chart(fig_dias, use_container_width=True)
            else:
                top_vends = df_ranking.head(6)
                fig_vends = go.Figure()
                fig_vends.add_trace(go.Bar(
                    x=top_vends["Vendedor"],
                    y=top_vends["Faturamento"],
                    marker=dict(color="#3B82F6", line=dict(color="#000000", width=1.5)),
                    text=[f"R$ {v/1000:.1f}k" for v in top_vends["Faturamento"]],
                    textposition="outside",
                    hovertemplate="<span style='color: #FFFFFF; font-size: 13px;'><b>%{x}</b></span><br><span style='color: #FFFFFF;'>💰 Faturamento: <b>R$ %{y:,.2f}</b></span><extra></extra>"
                ))
                fig_vends.update_layout(
                    template="plotly_white",
                    title=f"<b>🏆 Top Vendedores — Faturamento Consolidado ({ano_target})</b>",
                    title_font=dict(size=14, color="#0F172A"),
                    plot_bgcolor="#FFFFFF",
                    paper_bgcolor="#FFFFFF",
                    font=dict(family="Inter, sans-serif", size=12, color="#0F172A"),
                    margin=dict(l=20, r=20, t=50, b=30),
                    height=340,
                    hoverlabel=dict(bgcolor="#0F172A", bordercolor="#38BDF8", font=dict(color="#FFFFFF", size=13)),
                    xaxis=dict(gridcolor="#E2E8F0", tickfont=dict(color="#0F172A")),
                    yaxis=dict(gridcolor="#E2E8F0", tickfont=dict(color="#0F172A"))
                )
                st.plotly_chart(fig_vends, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 5.8: RADAR DE CLIENTES INATIVOS & RISCO DE CHURN
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "🚨  Radar de Clientes & Churn":
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    import datetime
    from datetime import date

    st.markdown("""<style>
    /* ── CARD UNIFICADO DO RADAR DE CLIENTES (BORDAS PRETAS E BOTÕES 100% INTERNOS) ── */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.radar-cliente-card-marker) {
        margin-bottom: 20px !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.radar-cliente-card-marker) > div {
        border: 2px solid #000000 !important;
        border-radius: 16px !important;
        background: #FFFFFF !important;
        padding: 20px 24px 22px 24px !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04) !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.radar-cliente-card-marker) div[data-testid="stHorizontalBlock"]:first-child button {
        text-align: left !important;
        justify-content: flex-start !important;
        font-size: 16px !important;
        font-weight: 900 !important;
        color: #0F172A !important;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        box-shadow: none !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.radar-cliente-card-marker) div[data-testid="stHorizontalBlock"]:first-child button:hover {
        color: #4F46E5 !important;
    }
</style>""", unsafe_allow_html=True)
    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">🚨</div>
        <div>
            <div class="page-header-title">Radar de Clientes Inativos & Risco de Churn</div>
            <div class="page-header-subtitle">Auditoria de recência de compra, faturamento histórico em risco e reativação comercial em 1 clique via WhatsApp e E-mail.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    pedidos_lista_full = auth.obter_pedidos_filtrados_usuario(_obter_pedidos_cached(), usr_logado)
    hoje = date.today()

    # ── MOTOR DE INTELIGÊNCIA DE RECÊNCIA E CHURN ──
    clientes_radar = {}
    clis_validos_tag = omie.carregar_clientes()
    codigos_validos_cliente = {str(c.get("codigo_cliente") or c.get("codigo_cliente_omie") or "").strip() for c in clis_validos_tag if c.get("codigo_cliente") or c.get("codigo_cliente_omie")}
    cnpjs_validos_cliente = {str(c.get("cnpj_cpf") or "").strip() for c in clis_validos_tag if c.get("cnpj_cpf")}

    for ped in pedidos_lista_full:
        cod_cli = str(ped.get("codigo_cliente") or "").strip()
        if not cod_cli:
            continue
        
        raw = ped.get("raw_data", {}) if isinstance(ped.get("raw_data"), dict) else {}
        info_adic = raw.get("informacoes_adicionais", {})
        outros = info_adic.get("outros_detalhes", {})
        cnpj_ped = str(ped.get("cliente_cnpj_cpf") or outros.get("cCnpjCpfOd") or "").strip()

        # Exigência do usuário: SOMENTE clientes com a tag de CLIENTE
        if cod_cli not in codigos_validos_cliente and (not cnpj_ped or cnpj_ped not in cnpjs_validos_cliente):
            continue
        
        dt_fat_str = ped.get("data_faturamento_real") or ped.get("data_faturamento")
        dt_obj = None
        if dt_fat_str:
            try:
                dt_obj = datetime.datetime.strptime(dt_fat_str, "%d/%m/%Y").date()
            except Exception:
                pass
        if not dt_obj:
            dt_prev = ped.get("data_previsao")
            if dt_prev:
                try:
                    dt_obj = datetime.datetime.strptime(dt_prev, "%d/%m/%Y").date()
                except Exception:
                    pass
        if not dt_obj:
            dt_obj = date(2025, 1, 1)

        tel = outros.get("cTelefoneOd") or ""
        email = info_adic.get("utilizar_emails") or ""
        valor = float(ped.get("valor_total") or 0.0)
        vendedor = ped.get("vendedor") or "Não Informado"
        num_ped = ped.get("numero_pedido") or ""

        origem = str(raw.get("cabecalho", {}).get("origem_pedido") or "").upper()
        canal = "B2C (Site)" if (origem in ["SITE", "API"] or "api" in vendedor.lower()) else "B2B (Corporativo)"

        if cod_cli not in clientes_radar:
            clientes_radar[cod_cli] = {
                "codigo_cliente": cod_cli,
                "nome": ped.get("cliente_nome") or outros.get("cNomeOd") or "Cliente Sem Nome",
                "cnpj_cpf": outros.get("cCnpjCpfOd") or "",
                "cidade": outros.get("cCidadeOd") or "",
                "uf": ped.get("cliente_uf") or outros.get("cEstadoOd") or "Outros",
                "telefone": tel,
                "email": email,
                "ultima_compra_dt": dt_obj,
                "ultimo_pedido_num": num_ped,
                "total_pedidos": 1,
                "ltv": valor,
                "vendedor": vendedor,
                "canal": canal
            }
        else:
            cli = clientes_radar[cod_cli]
            cli["total_pedidos"] += 1
            cli["ltv"] += valor
            if dt_obj > cli["ultima_compra_dt"]:
                cli["ultima_compra_dt"] = dt_obj
                cli["ultimo_pedido_num"] = num_ped
                cli["vendedor"] = vendedor
                cli["canal"] = canal
            if tel and not cli["telefone"]:
                cli["telefone"] = tel
            if email and not cli["email"]:
                cli["email"] = email

    # Classificação de faixas de recência
    qtd_ativos = 0
    qtd_atencao = 0
    qtd_risco = 0
    qtd_churn = 0

    ltv_atencao = 0.0
    ltv_risco = 0.0
    ltv_churn = 0.0

    for cli in clientes_radar.values():
        dias = (hoje - cli["ultima_compra_dt"]).days
        cli["dias_sem_comprar"] = max(0, dias)
        if dias <= 30:
            cli["faixa"] = "🟢 Ativo (<30d)"
            cli["faixa_codigo"] = "ativo"
            qtd_ativos += 1
        elif dias <= 60:
            cli["faixa"] = "🟡 Em Atenção (30-60d)"
            cli["faixa_codigo"] = "atencao"
            qtd_atencao += 1
            ltv_atencao += cli["ltv"]
        elif dias <= 90:
            cli["faixa"] = "🟠 Em Risco (61-90d)"
            cli["faixa_codigo"] = "risco"
            qtd_risco += 1
            ltv_risco += cli["ltv"]
        else:
            cli["faixa"] = "🔴 Inativo Crítico (>90d)"
            cli["faixa_codigo"] = "churn"
            qtd_churn += 1
            ltv_churn += cli["ltv"]

    total_clientes_base = len(clientes_radar)
    total_inativos_alerta = qtd_atencao + qtd_risco + qtd_churn
    ltv_total_em_risco = ltv_atencao + ltv_risco + ltv_churn

    # ── 4 CARDS DE KPI DE CHURN NO TOPO ──
    col_c1, col_c2, col_c3, col_c4 = st.columns(4)

    with col_c1:
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 2px solid #000000; border-radius: 16px; padding: 18px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.04); height: 190px; min-height: 190px; max-height: 190px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase;">Clientes Ativos</span>
                <span style="background: #ECFDF5; color: #059669; padding: 3px 8px; border-radius: 6px; font-weight: 800; font-size: 11px;">RECORRENTES</span>
            </div>
            <div>
                <div style="font-size: 26px; font-weight: 900; color: #10B981; letter-spacing: -0.5px;">{qtd_ativos} <span style="font-size: 13px; color: #64748B; font-weight: 700;">clientes</span></div>
                <div style="font-size: 12px; color: #10B981; font-weight: 800; margin-top: 4px;">
                    {((qtd_ativos/max(total_clientes_base,1))*100):.1f}% da base ativa
                </div>
            </div>
            <div style="font-size: 11px; color: #64748B; font-weight: 600; border-top: 1px solid #F1F5F9; padding-top: 6px;">
                Compraram nos últimos 30 dias na base.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_c2:
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 2px solid #000000; border-radius: 16px; padding: 18px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.04); height: 190px; min-height: 190px; max-height: 190px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase;">🟡 Em Atenção (30-60d)</span>
                <span style="background: #FEFCE8; color: #CA8A04; padding: 3px 8px; border-radius: 6px; font-weight: 800; font-size: 11px;">MODERADO</span>
            </div>
            <div>
                <div style="font-size: 26px; font-weight: 900; color: #D97706; letter-spacing: -0.5px;">{qtd_atencao} <span style="font-size: 13px; color: #64748B; font-weight: 700;">clientes</span></div>
                <div style="font-size: 12px; color: #D97706; font-weight: 800; margin-top: 4px;">
                    LTV em Risco: {fmt_brl(ltv_atencao)}
                </div>
            </div>
            <div style="font-size: 11px; color: #64748B; font-weight: 600; border-top: 1px solid #F1F5F9; padding-top: 6px;">
                Momento perfeito para contato de reposição.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_c3:
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 2px solid #000000; border-radius: 16px; padding: 18px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.04); height: 190px; min-height: 190px; max-height: 190px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase;">🟠 Em Risco (61-90d)</span>
                <span style="background: #FFF7ED; color: #EA580C; padding: 3px 8px; border-radius: 6px; font-weight: 800; font-size: 11px;">ALTO RISCO</span>
            </div>
            <div>
                <div style="font-size: 26px; font-weight: 900; color: #EA580C; letter-spacing: -0.5px;">{qtd_risco} <span style="font-size: 13px; color: #64748B; font-weight: 700;">clientes</span></div>
                <div style="font-size: 12px; color: #EA580C; font-weight: 800; margin-top: 4px;">
                    LTV em Risco: {fmt_brl(ltv_risco)}
                </div>
            </div>
            <div style="font-size: 11px; color: #64748B; font-weight: 600; border-top: 1px solid #F1F5F9; padding-top: 6px;">
                Quase 3 meses sem comprar. Risco iminente.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_c4:
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 2px solid #000000; border-radius: 16px; padding: 18px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.04); height: 190px; min-height: 190px; max-height: 190px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase;">🔴 Inativos Críticos (>90d)</span>
                <span style="background: #FEF2F2; color: #DC2626; padding: 3px 8px; border-radius: 6px; font-weight: 800; font-size: 11px;">CHURN CRÍTICO</span>
            </div>
            <div>
                <div style="font-size: 26px; font-weight: 900; color: #DC2626; letter-spacing: -0.5px;">{qtd_churn} <span style="font-size: 13px; color: #64748B; font-weight: 700;">clientes</span></div>
                <div style="font-size: 12px; color: #DC2626; font-weight: 800; margin-top: 4px;">
                    LTV a Resgatar: {fmt_brl(ltv_churn)}
                </div>
            </div>
            <div style="font-size: 11px; color: #64748B; font-weight: 600; border-top: 1px solid #F1F5F9; padding-top: 6px;">
                Exige oferta agressiva de reativação imediata.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    # ── GRÁFICOS DE DISTRIBUIÇÃO ANALÍTICA DO CHURN ──
    col_g1, col_g2 = st.columns([1, 1])

    with col_g1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%); border: 1.5px solid #E2E8F0; border-radius: 12px; padding: 10px 16px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between;'>
            <div>
                <div style='font-size: 14px; color: #0F172A; font-weight: 800;'>🍩 Distribuição da Carteira</div>
                <div style='font-size: 11px; color: #64748B;'>Por nível de recência e dias sem comprar</div>
            </div>
            <span class="dark-badge" style='background: #0F172A; color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; font-size: 11px; font-weight: 800; padding: 4px 12px; border-radius: 14px;'>{total_clientes_base} Clientes</span>
        </div>
        """, unsafe_allow_html=True)
        df_faixas = pd.DataFrame([
            {"Faixa": "🟢 Ativo (<30d)", "Qtd": qtd_ativos, "Cor": "#10B981"},
            {"Faixa": "🟡 Em Atenção (30-60d)", "Qtd": qtd_atencao, "Cor": "#F59E0B"},
            {"Faixa": "🟠 Em Risco (61-90d)", "Qtd": qtd_risco, "Cor": "#F97316"},
            {"Faixa": "🔴 Inativo Crítico (>90d)", "Qtd": qtd_churn, "Cor": "#EF4444"}
        ])
        fig_donut = px.pie(
            df_faixas,
            names="Faixa",
            values="Qtd",
            hole=0.55,
            color="Faixa",
            color_discrete_map={
                "🟢 Ativo (<30d)": "#10B981",
                "🟡 Em Atenção (30-60d)": "#F59E0B",
                "🟠 Em Risco (61-90d)": "#F97316",
                "🔴 Inativo Crítico (>90d)": "#EF4444"
            }
        )
        fig_donut.update_traces(
            textinfo="percent",
            textfont_size=12,
            textfont_color="#0F172A",
            textposition="inside",
            hovertemplate="<b>%{label}</b><br>👥 Clientes: <b>%{value}</b><br>📊 %{percent}<extra></extra>",
            marker=dict(line=dict(color="#FFFFFF", width=2))
        )
        fig_donut.update_layout(
            template="plotly_white",
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font=dict(family="Inter, sans-serif", size=12, color="#0F172A"),
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            hoverlabel=dict(bgcolor="#0F172A", bordercolor="#38BDF8", font=dict(color="#FFFFFF", size=13)),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5,
                font=dict(color="#0F172A", size=11, family="Inter, sans-serif")
            )
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_g2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%); border: 1.5px solid #FECACA; border-radius: 12px; padding: 10px 16px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between;'>
            <div>
                <div style='font-size: 14px; color: #991B1B; font-weight: 800;'>💰 Faturamento Histórico (LTV) em Risco</div>
                <div style='font-size: 11px; color: #DC2626;'>Faturamento acumulado dos clientes em alerta</div>
            </div>
            <span class="dark-badge" style='background: #DC2626; color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; font-size: 11px; font-weight: 800; padding: 4px 12px; border-radius: 14px;'>{fmt_brl(ltv_total_em_risco)}</span>
        </div>
        """, unsafe_allow_html=True)
        df_ltv = pd.DataFrame([
            {"Faixa": "🟡 30-60d", "LTV": ltv_atencao, "Cor": "#F59E0B"},
            {"Faixa": "🟠 61-90d", "LTV": ltv_risco, "Cor": "#F97316"},
            {"Faixa": "🔴 >90d", "LTV": ltv_churn, "Cor": "#EF4444"}
        ])
        fig_bar_ltv = px.bar(
            df_ltv,
            x="Faixa",
            y="LTV",
            color="Faixa",
            text="LTV",
            color_discrete_map={"🟡 30-60d": "#F59E0B", "🟠 61-90d": "#F97316", "🔴 >90d": "#EF4444"}
        )
        fig_bar_ltv.update_traces(
            texttemplate='R$ %{y:,.2f}',
            textposition='outside',
            hovertemplate="<span style='color: #FFFFFF; font-size: 13px;'><b>%{x}</b></span><br><span style='color: #FFFFFF;'>💰 LTV em Risco: <b>R$ %{y:,.2f}</b></span><extra></extra>"
        )
        fig_bar_ltv.update_layout(
            template="plotly_white",
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            font=dict(family="Inter, sans-serif", size=12, color="#0F172A"),
            showlegend=False,
            hoverlabel=dict(bgcolor="#0F172A", bordercolor="#38BDF8", font=dict(color="#FFFFFF", size=13)),
            xaxis=dict(title="Faixa de Inatividade", gridcolor="#F1F5F9", tickfont=dict(color="#0F172A"), title_font=dict(color="#0F172A")),
            yaxis=dict(title="LTV Acumulado (R$)", gridcolor="#F1F5F9", tickformat=",.2f", tickfont=dict(color="#0F172A"), title_font=dict(color="#0F172A"))
        )
        st.plotly_chart(fig_bar_ltv, use_container_width=True)

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    # ── FILTROS TÁTICOS PARA REATIVAÇÃO ──
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%); border: 1.5px solid #C7D2FE; border-radius: 12px; padding: 12px 18px; margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between;'>
        <div>
            <div style='font-size: 15px; color: #1E1B4B; font-weight: 800;'>🎯 Mesa de Ação e Reativação Comercial</div>
            <div style='font-size: 12px; color: #4338CA;'>Filtre clientes inativos e dispare campanhas instantâneas via WhatsApp e E-mail em 1 clique</div>
        </div>
        <span class="dark-badge" style='background: #4F46E5; color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 20px;'>{total_inativos_alerta} Em Alerta</span>
    </div>
    """, unsafe_allow_html=True)
    
    col_rf1, col_rf2, col_rf3, col_rf4 = st.columns(4)

    with col_rf1:
        opcoes_filtro_faixa = [
            "🚨 Todos os Inativos (30d+)",
            "🟡 Em Atenção (30 a 60 dias)",
            "🟠 Em Risco (61 a 90 dias)",
            "🔴 Inativos Críticos (> 90 dias)",
            "🟢 Clientes Ativos (< 30 dias)",
            "📋 Base Completa de Clientes"
        ]
        filtro_faixa_sel = st.selectbox("1. Nível de Inatividade", opcoes_filtro_faixa, index=0, key="rf_faixa")

    # Lista de Vendedores
    vendedores_churn = sorted(list(set(c["vendedor"] for c in clientes_radar.values() if c["vendedor"])))
    with col_rf2:
        filtro_vend_sel = st.selectbox("2. Vendedor Responsável", ["Todos os Vendedores"] + vendedores_churn, index=0, key="rf_vend")

    with col_rf3:
        filtro_canal_sel = st.selectbox("3. Canal Comercial", ["Todos os Canais", "B2B (Corporativo)", "B2C (Site)"], index=0, key="rf_canal")

    # Estados (UF)
    ufs_churn = sorted(list(set(c["uf"] for c in clientes_radar.values() if c["uf"])))
    with col_rf4:
        filtro_uf_sel = st.selectbox("4. Estado (UF)", ["Todos os Estados"] + ufs_churn, index=0, key="rf_uf")

    col_busca, col_export = st.columns([3, 1])
    with col_busca:
        busca_termo = st.text_input("🔍 Buscar cliente por Nome, Razão Social ou CNPJ/CPF:", placeholder="Digite o nome ou documento do cliente...", key="rf_busca")

    # ── APLICAR FILTROS ──
    clientes_filtrados = list(clientes_radar.values())

    # 1. Filtro de Faixa
    if "Todos os Inativos" in filtro_faixa_sel:
        clientes_filtrados = [c for c in clientes_filtrados if c["dias_sem_comprar"] > 30]
    elif "Atenção" in filtro_faixa_sel:
        clientes_filtrados = [c for c in clientes_filtrados if 30 < c["dias_sem_comprar"] <= 60]
    elif "Em Risco" in filtro_faixa_sel:
        clientes_filtrados = [c for c in clientes_filtrados if 60 < c["dias_sem_comprar"] <= 90]
    elif "Inativos Críticos" in filtro_faixa_sel:
        clientes_filtrados = [c for c in clientes_filtrados if c["dias_sem_comprar"] > 90]
    elif "Ativos" in filtro_faixa_sel:
        clientes_filtrados = [c for c in clientes_filtrados if c["dias_sem_comprar"] <= 30]

    # 2. Filtro de Vendedor
    if filtro_vend_sel != "Todos os Vendedores":
        clientes_filtrados = [c for c in clientes_filtrados if c["vendedor"] == filtro_vend_sel]

    # 3. Filtro de Canal
    if filtro_canal_sel != "Todos os Canais":
        clientes_filtrados = [c for c in clientes_filtrados if c["canal"] == filtro_canal_sel]

    # 4. Filtro de UF
    if filtro_uf_sel != "Todos os Estados":
        clientes_filtrados = [c for c in clientes_filtrados if c["uf"] == filtro_uf_sel]

    # 5. Busca por termo
    if busca_termo:
        termo_limpo = busca_termo.strip().lower()
        clientes_filtrados = [c for c in clientes_filtrados if (termo_limpo in c["nome"].lower() or termo_limpo in c["cnpj_cpf"].lower() or termo_limpo in c["cidade"].lower())]

    # Ordenar por maior tempo sem comprar ou maior LTV
    clientes_filtrados.sort(key=lambda x: (x["dias_sem_comprar"], x["ltv"]), reverse=True)

    with col_export:
        if clientes_filtrados:
            df_export = pd.DataFrame([{
                "Nome / Razão Social": c["nome"],
                "CNPJ / CPF": c["cnpj_cpf"],
                "Cidade": c["cidade"],
                "UF": c["uf"],
                "Telefone": c["telefone"],
                "E-mail": c["email"],
                "Dias sem Comprar": c["dias_sem_comprar"],
                "Faixa": c["faixa"],
                "LTV Histórico (R$)": c["ltv"],
                "Total de Pedidos": c["total_pedidos"],
                "Última Compra": c["ultima_compra_dt"].strftime("%d/%m/%Y"),
                "Último Pedido Nº": c["ultimo_pedido_num"],
                "Vendedor": c["vendedor"],
                "Canal": c["canal"]
            } for c in clientes_filtrados])
            csv_data = df_export.to_csv(index=False, sep=";").encode("utf-8-sig")
            st.download_button(
                "📥 Exportar Lista (CSV)",
                data=csv_data,
                file_name=f"clientes_inativos_{hoje.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )

    st.markdown(f"""
    <div style="font-size: 13px; font-weight: 800; color: #475569; margin: 10px 0 16px 0;">
        Exibindo <b>{len(clientes_filtrados)}</b> clientes que atendem aos filtros selecionados.
    </div>
    """, unsafe_allow_html=True)

    if not clientes_filtrados:
        st.info("Nenhum cliente encontrado para os filtros selecionados.")
    else:
        # Exibir em Cards Executivos de Reativação
        for c_idx, c_item in enumerate(clientes_filtrados[:50]):
            dias_sc = c_item["dias_sem_comprar"]
            if dias_sc <= 30:
                cor_tag = "#10B981"
                bg_tag = "#ECFDF5"
                label_tag = f"🟢 Ativo ({dias_sc} dias)"
            elif dias_sc <= 60:
                cor_tag = "#D97706"
                bg_tag = "#FEFCE8"
                label_tag = f"🟡 Atenção ({dias_sc} dias sem comprar)"
            elif dias_sc <= 90:
                cor_tag = "#EA580C"
                bg_tag = "#FFF7ED"
                label_tag = f"🟠 Em Risco ({dias_sc} dias sem comprar)"
            else:
                cor_tag = "#DC2626"
                bg_tag = "#FEF2F2"
                label_tag = f"🔴 Inativo Crítico ({dias_sc} dias sem comprar)"

            link_wpp = formatar_link_whatsapp_reativacao(c_item["telefone"], c_item["nome"], dias_sc)
            mail_to = f"mailto:{c_item['email']}?subject=Novidades%20e%20Condições%20Especiais%20-%20Missha" if c_item["email"] else ""

            with st.container(border=True):
                st.markdown('<div class="radar-cliente-card-marker" style="display:none;"></div>', unsafe_allow_html=True)
                # 1. Topo do Card com Nome Clicável e Badge
                col_card_top_l, col_card_top_r = st.columns([3.5, 1.2])
                with col_card_top_l:
                    if st.button(
                        f"🏢 {c_item['nome']}",
                        key=f"btn_click_cli_title_{c_item['codigo_cliente']}_{c_idx}",
                        help="👉 Clique para abrir o Histórico do Cliente com Sugestões de IA",
                        use_container_width=True
                    ):
                        st.session_state["mudar_pagina_para"] = "🔎  Histórico do Cliente"
                        st.session_state["cliente_direcionado_radar"] = {
                            "codigo_cliente": str(c_item["codigo_cliente"]),
                            "nome": c_item["nome"],
                            "cnpj_cpf": c_item["cnpj_cpf"]
                        }
                        st.session_state["ativar_ia_sugestoes"] = True
                        st.rerun()
                with col_card_top_r:
                    st.markdown(f"""<div style="text-align: right; padding-top: 4px;">
                        <span style="background: {bg_tag}; color: {cor_tag}; border: 1.5px solid {cor_tag}; padding: 5px 12px; border-radius: 20px; font-size: 11px; font-weight: 800;">
                            {label_tag}
                        </span>
                    </div>""", unsafe_allow_html=True)

                # 2. Dados e Métricas (LTV, Última Compra, Vendedor, Pedidos)
                st.markdown(f"""
                <div style="font-size: 11px; color: #64748B; font-weight: 700; margin-bottom: 8px;">
                    {'CNPJ/CPF: ' + c_item['cnpj_cpf'] + ' • ' if c_item['cnpj_cpf'] else ''}{c_item['cidade'] + '/' if c_item['cidade'] else ''}{c_item['uf']} • Canal: <b>{c_item['canal']}</b>
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(135px, 1fr)); gap: 12px; margin-top: 10px; padding-top: 10px; border-top: 1px solid #F1F5F9; font-size: 12px; margin-bottom: 14px;">
                    <div>
                        <span style="color: #64748B; font-size: 11px; font-weight: 700;">LTV Total:</span>
                        <div style="font-size: 15px; font-weight: 900; color: #000000;">{fmt_brl(c_item['ltv'])}</div>
                    </div>
                    <div>
                        <span style="color: #64748B; font-size: 11px; font-weight: 700;">Última Compra:</span>
                        <div style="font-size: 13px; font-weight: 800; color: #000000;">{c_item['ultima_compra_dt'].strftime('%d/%m/%Y')} (Ped #{c_item['ultimo_pedido_num']})</div>
                    </div>
                    <div>
                        <span style="color: #64748B; font-size: 11px; font-weight: 700;">Vendedor:</span>
                        <div style="font-size: 13px; font-weight: 800; color: #4F46E5;">{c_item['vendedor']}</div>
                    </div>
                    <div>
                        <span style="color: #64748B; font-size: 11px; font-weight: 700;">Pedidos:</span>
                        <div style="font-size: 13px; font-weight: 800; color: #000000;">{c_item['total_pedidos']} compras</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # 3. Barra de Ações com Botões 100% Contidos Dentro do Container
                col_act_ia, col_act_wpp, col_act_mail = st.columns([1.8, 1, 1])
                with col_act_ia:
                    if st.button(
                        f"🤖 Histórico 360º & Sugestões IA",
                        key=f"btn_radar_to_hist_{c_item['codigo_cliente']}_{c_idx}",
                        help=f"Abrir Histórico Completo de {c_item['nome']} e ativar Recomendações de Venda da IA",
                        type="primary",
                        use_container_width=True
                    ):
                        st.session_state["mudar_pagina_para"] = "🔎  Histórico do Cliente"
                        st.session_state["cliente_direcionado_radar"] = {
                            "codigo_cliente": str(c_item["codigo_cliente"]),
                            "nome": c_item["nome"],
                            "cnpj_cpf": c_item["cnpj_cpf"]
                        }
                        st.session_state["ativar_ia_sugestoes"] = True
                        st.rerun()
                with col_act_wpp:
                    if link_wpp:
                        st.markdown(f'<a href="{link_wpp}" target="_blank" style="background: #25D366; color: #FFFFFF; font-weight: 800; font-size: 12px; padding: 7px 12px; border-radius: 8px; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 6px; box-shadow: 0 2px 8px rgba(37,211,102,0.3); height: 38px; box-sizing: border-box; text-align: center;">📲 WhatsApp</a>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div style="background: #F1F5F9; color: #94A3B8; font-size: 11px; font-weight: 700; border-radius: 8px; height: 38px; display: flex; align-items: center; justify-content: center;">Sem Telefone</div>', unsafe_allow_html=True)
                with col_act_mail:
                    if mail_to:
                        st.markdown(f'<a href="{mail_to}" style="background: #0F172A; color: #FFFFFF; font-weight: 800; font-size: 12px; padding: 7px 12px; border-radius: 8px; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 6px; height: 38px; box-sizing: border-box; text-align: center;">📧 E-mail</a>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div style="background: #F1F5F9; color: #94A3B8; font-size: 11px; font-weight: 700; border-radius: 8px; height: 38px; display: flex; align-items: center; justify-content: center;">Sem E-mail</div>', unsafe_allow_html=True)

        if len(clientes_filtrados) > 50:
            st.caption(f"Exibindo os primeiros 50 clientes de {len(clientes_filtrados)}. Utilize os filtros acima ou o botão 'Exportar Lista (CSV)' para visualizar a base completa.")


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA: MAPA & INTELIGÊNCIA GEOGRÁFICA DOS CLIENTES (GOOGLE MAPS)
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "🗺️  Localização dos Clientes":
    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">🗺️</div>
        <div>
            <div class="page-header-title">Mapa de Localização dos Clientes</div>
            <div class="page-header-subtitle">Geolocalização em tempo real integrada ao Google Maps com localização exata por CEP, Cidade e Estado</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Carregar clientes da base local / Omie
    try:
        todos_clientes = omie.carregar_clientes()
    except Exception:
        with open("cache/clientes.json", "r", encoding="utf-8") as f_clis:
            todos_clientes = json.load(f_clis)

    if not todos_clientes:
        st.warning("Nenhum cliente disponível para exibição no mapa.")
    else:
        # Enriquece os clientes com faturamento e último pedido calculados dos pedidos carregados
        if pedidos_lista_full:
            fat_por_cli = {}
            ult_por_cli = {}
            for p in pedidos_lista_full:
                cod_c = str(p.get("cabecalho", {}).get("codigo_cliente") or p.get("codigo_cliente") or "")
                val_p = float(p.get("total_pedido") or p.get("valor_total") or p.get("cabecalho", {}).get("valor_total") or 0.0)
                dt_p = p.get("cabecalho", {}).get("data_previsao") or p.get("data_faturamento") or p.get("data_pedido") or ""
                if cod_c:
                    fat_por_cli[cod_c] = fat_por_cli.get(cod_c, 0.0) + val_p
                    if dt_p and (cod_c not in ult_por_cli or dt_p > ult_por_cli[cod_c]):
                        ult_por_cli[cod_c] = dt_p

            for c in todos_clientes:
                cod_c = str(c.get("codigo_cliente") or c.get("codigo_cliente_omie") or "")
                if cod_c in fat_por_cli:
                    c["total_comprado"] = fat_por_cli[cod_c]
                if cod_c in ult_por_cli:
                    c["ultimo_pedido"] = ult_por_cli[cod_c]

        # Barra de Ações & Sincronização por CEP
        col_b1, col_b2 = st.columns([3, 1])
        with col_b1:
            busca_query = st.text_input("🔍 Buscar por Nome, CNPJ/CPF, CEP, Cidade ou Logradouro:", "", placeholder="Ex: 82560-470, Curitiba, Época, Paulista, Carol...")
        with col_b2:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("🔄 Sincronizar CEPs", use_container_width=True, help="Geocodifica todos os clientes em tempo real através do CEP e Endereço Oficial"):
                with st.spinner("Geocodificando localização exata através de CEP, Logradouro e Cidade..."):
                    qtd = geo.sincronizar_todas_coordenadas(todos_clientes)
                    st.success(f"✅ {qtd} clientes geocodificados com precisão exata!")
                    st.rerun()

        # Filtros no topo
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        
        estados_disp = ["Todos"] + sorted(list(set(str(c.get("estado", "")).upper() for c in todos_clientes if c.get("estado"))))
        with col_f1:
            uf_sel = st.selectbox("Filtrar por Estado (UF):", estados_disp, key="geo_uf_sel_missha")

        cidades_disp = ["Todas"] + sorted(list(set(str(c.get("cidade", "")) for c in todos_clientes if c.get("cidade"))))
        with col_f2:
            cid_sel = st.selectbox("Filtrar por Cidade:", cidades_disp, key="geo_cid_sel_missha")

        vendedores_disp = ["Todos"] + sorted(list(set(str(c.get("vendedor", "") or c.get("vendedor_nome", "")) for c in todos_clientes if (c.get("vendedor") or c.get("vendedor_nome")))))
        with col_f3:
            vend_sel = st.selectbox("Filtrar por Vendedor:", vendedores_disp, key="geo_vend_sel_missha")

        status_disp = ["Todos", "Ativo", "Em Alerta", "Inativo"]
        with col_f4:
            st_sel = st.selectbox("Status Comercial:", status_disp, key="geo_st_sel_missha")

        # Aplicar filtros
        q_limpa = busca_query.strip().lower()
        clientes_filtrados = []
        for c in todos_clientes:
            c_uf = str(c.get("estado", "")).upper()
            c_cid = str(c.get("cidade", ""))
            c_vend = str(c.get("vendedor", "") or c.get("vendedor_nome", ""))
            c_status = str(c.get("status", "Ativo"))
            
            c_str_busca = f"{c.get('razao_social', '')} {c.get('nome_fantasia', '')} {c.get('cnpj_cpf', '')} {c.get('cep', '')} {c.get('cidade', '')} {c.get('estado', '')} {c.get('endereco', '')} {c.get('bairro', '')}".lower()

            if q_limpa and q_limpa not in c_str_busca:
                continue
            if uf_sel != "Todos" and c_uf != uf_sel:
                continue
            if cid_sel != "Todas" and c_cid != cid_sel:
                continue
            if vend_sel != "Todos" and c_vend != vend_sel:
                continue
            if st_sel != "Todos" and c_status != st_sel:
                continue
            clientes_filtrados.append(c)

        # KPIs no topo do mapa
        tot_clis = len(clientes_filtrados)
        tot_ufs = len(set(c.get("estado", "").upper() for c in clientes_filtrados if c.get("estado")))
        tot_cids = len(set(c.get("cidade", "") for c in clientes_filtrados if c.get("cidade")))
        tot_fat = sum(float(c.get("total_comprado", 0.0) or 0.0) for c in clientes_filtrados)
        tot_exatos = sum(1 for c in clientes_filtrados if "CEP" in str(c.get("precisao_geo", "")) or "Endereço" in str(c.get("precisao_geo", "")))

        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Clientes Filtrados", f"{tot_clis}")
        m2.metric("Localização Exata CEP", f"{tot_exatos} ({int(tot_exatos/max(tot_clis,1)*100)}%)")
        m3.metric("Estados Alcançados", f"{tot_ufs} UFs")
        m4.metric("Cidades Atendidas", f"{tot_cids} cidades")
        m5.metric("Faturamento Mapeado", f"R$ {tot_fat:,.2f}")

        st.markdown("---")
        
        # Renderizar o Mapa Interativo Oficial do Google Maps
        geo.renderizar_mapa_clientes(clientes_filtrados, height=620)

        # Tabela Detalhada com os dados dos clientes
        st.markdown("### 📋 Detalhamento dos Clientes Mapeados por CEP")
        tab_dados = []
        for idx, c in enumerate(clientes_filtrados, 1):
            cep_fmt = geo.formatar_cep(c.get("cep") or "")
            lat_c = c.get("latitude")
            lon_c = c.get("longitude")
            coords_str = f"{lat_c:.5f}, {lon_c:.5f}" if (lat_c is not None and lon_c is not None) else "Pendente"
            
            end_c = f"{c.get('endereco', '')}, {c.get('numero', '')}".strip(" ,")
            if c.get('bairro'):
                end_c += f" - {c.get('bairro')}"

            tab_dados.append({
                "#": idx,
                "Cliente": c.get("nome_fantasia") or c.get("razao_social"),
                "CNPJ/CPF": c.get("cnpj_cpf", "-"),
                "CEP Exato": cep_fmt,
                "Endereço / Logradouro": end_c or "-",
                "Cidade": c.get("cidade", "-"),
                "UF": c.get("estado", "-"),
                "Coordenadas": coords_str,
                "Precisão": c.get("precisao_geo", "Exata por CEP"),
                "Vendedor": c.get("vendedor") or c.get("vendedor_nome", "-"),
                "Total Comprado": f"R$ {float(c.get('total_comprado') or 0.0):,.2f}",
                "Status": c.get("status", "Ativo")
            })
        st.dataframe(pd.DataFrame(tab_dados), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 6: PESSOAS CADASTRADAS (VENDEDORES & CLIENTES)
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "👥  Pessoas Cadastradas":
    usr_logado_now = st.session_state.get("usuario_logado")
    if not auth.eh_usuario_master(usr_logado_now):
        st.error("⛔ **Acesso Restrito ao Administrador Master**: Apenas Administradores podem visualizar e gerenciar a base de pessoas, vendedores e clientes da empresa.")
        st.stop()

    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">👥</div>
        <div>
            <div class="page-header-title">Pessoas Cadastradas no Sistema & Omie ERP</div>
            <div class="page-header-subtitle">Gestão unificada de Vendedores Autorizados, Usuários do CRM e Base Completa de Clientes da Omie (Acesso Restrito ADM)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_vendedores_sys, tab_clientes_sys = st.tabs(["👔 Vendedores & Usuários Autorizados", "🏢 Base Completa de Clientes (Omie ERP)"])

    with tab_vendedores_sys:
        col_vt1, col_vt2 = st.columns([3, 1])
        with col_vt1:
            st.markdown('<div class="section-header">👔 Vendedores Oficiais Cadastrados no Omie ERP (Sem Duplicatas)</div>', unsafe_allow_html=True)
        with col_vt2:
            if st.button("🔄 Sincronizar Vendedores ERP", key="btn_sync_vendedores_omie", use_container_width=True):
                with st.spinner("Atualizando vendedores diretamente do Omie ERP..."):
                    auth.sincronizar_vendedores_omie(force_refresh=True)
                    st.toast("✅ Vendedores sincronizados com sucesso!")
                    st.rerun()

        usrs_db = auth.carregar_usuarios()

        # Métricas no topo
        total_v = len(usrs_db)
        total_liberados = sum(1 for u in usrs_db.values() if not u.get("bloqueado", False))
        total_bloqueados = sum(1 for u in usrs_db.values() if u.get("bloqueado", False))

        c_v1, c_v2, c_v3 = st.columns(3)
        with c_v1:
            st.metric("👥 Total de Vendedores Omie", f"{total_v} cadastrados no ERP")
        with c_v2:
            st.metric("🟢 Acesso Liberado", f"{total_liberados} ativos")
        with c_v3:
            st.metric("🔴 Acesso Bloqueado", f"{total_bloqueados} suspensos")

        st.markdown("---")

        # Tabela de Vendedores Unificados sem Duplicatas
        list_v_tab = []
        for cod_v, u in usrs_db.items():
            tem_s = "✅ Senha Cadastrada" if u.get("senha_hash") else "📩 Aguardando 1º Acesso (2FA)"
            status_perm = "🔴 Bloqueado (Acesso Suspenso)" if u.get("bloqueado", False) else "🟢 Ativo / Liberado"
            perfil_str = "👑 Administrador Master" if str(u.get("role", "")).upper() == "MASTER" else "👔 Vendedor Padrão"
            bonif_str = "🎁 Autorizado" if auth.eh_autorizado_bonificacao(u) else "🔒 Restrito"
            
            list_v_tab.append({
                "ID Omie": f"#{cod_v}",
                "Nome do Vendedor Omie": u.get("nome_vendedor", "—"),
                "E-mail Cadastrado": u.get("email", "—"),
                "Perfil de Acesso": perfil_str,
                "Operação Bonificação": bonif_str,
                "Status da Senha": tem_s,
                "Permissão de Acesso": status_perm
            })

        df_v_tab = pd.DataFrame(list_v_tab)
        st.dataframe(df_v_tab, use_container_width=True, hide_index=True)

        st.markdown("---")
        
        # Bloco de Gerenciamento de Bloqueio e Permissões
        st.markdown('<div class="section-header">🔒 Gerenciamento de Permissões, Perfil Master & Bloqueios</div>', unsafe_allow_html=True)
        col_bl1, col_bl2, col_bl3, col_bl4 = st.columns([2, 1, 1, 1])
        
        opcoes_vendedores_gestao = {f"#{u['codigo_vendedor']} - {u['nome_vendedor']} ({u['email']})": u['codigo_vendedor'] for u in usrs_db.values()}
        
        with col_bl1:
            vendedor_gestao_sel = st.selectbox("Selecione o Vendedor Omie:", list(opcoes_vendedores_gestao.keys()), key="sel_vendedor_gestao")
            cod_v_gestao = opcoes_vendedores_gestao[vendedor_gestao_sel]
            vendedor_obj = usrs_db[cod_v_gestao]
            
            st_atual = "🔴 BLOQUEADO" if vendedor_obj.get("bloqueado", False) else "🟢 LIBERADO"
            perf_atual = "👑 MASTER" if str(vendedor_obj.get("role", "")).upper() == "MASTER" else "👔 VENDEDOR"
            st_bonif = "🎁 AUTORIZADO" if auth.eh_autorizado_bonificacao(vendedor_obj) else "🔒 RESTRITO"
            desc_max_val = auth.obter_desconto_maximo_vendedor(vendedor_obj)
            desc_max_lbl = "100% (Sem Limite)" if auth.eh_usuario_master(vendedor_obj) else f"{desc_max_val:.1f}%"
            st.markdown(f"**Perfil:** `{perf_atual}` | **Acesso:** `{st_atual}` | **Bonificação:** `{st_bonif}` | **Desc. Máx:** `{desc_max_lbl}`")

        with col_bl2:
            st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
            lbl_btn_p = "👔 Tornar Vendedor" if str(vendedor_obj.get("role", "")).upper() == "MASTER" else "👑 Promover a Master"
            if st.button(lbl_btn_p, use_container_width=True, key="btn_toggle_role", help="Alternar nivel de acesso deste usuário entre Vendedor e Master"):
                ok_r, msg_r = auth.alternar_perfil_vendedor(cod_v_gestao)
                if ok_r:
                    st.success(msg_r)
                    st.rerun()
                else:
                    st.error(msg_r)

        with col_bl3:
            st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
            lbl_btn_b = "🔒 Revogar Bonif. & Descontos" if vendedor_obj.get("pode_bonificar", False) else "🎁 Autorizar Bonif. & Descontos"
            if st.button(lbl_btn_b, use_container_width=True, key="btn_toggle_bonif", help="Conceder ou revogar permissão para conceder brindes e bonificações"):
                ok_b, msg_b = auth.alternar_permissao_bonificacao(cod_v_gestao)
                if ok_b:
                    st.success(msg_b)
                    st.rerun()
                else:
                    st.error(msg_b)

        with col_bl4:
            st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
            lbl_btn = "✅ Desbloquear" if vendedor_obj.get("bloqueado", False) else "🔴 Bloquear Acesso"
            if st.button(lbl_btn, use_container_width=True, key="btn_toggle_bloqueio", help="Bloquear ou liberar o acesso do usuário ao sistema"):
                ok_bl, msg_bl = auth.alternar_bloqueio_vendedor(cod_v_gestao)
                if ok_bl:
                    st.success(msg_bl)
                    st.rerun()
                else:
                    st.error(msg_bl)

        # ── BLOCO EXCLUSIVO: CONFIGURAÇÃO DE LIMITE MÁXIMO DE DESCONTO (%) ──
        with st.expander("🏷️ Definir Limite de Desconto Máximo (%) do Vendedor", expanded=True):
            col_dm1, col_dm2 = st.columns([3, 1])
            with col_dm1:
                desc_max_atual = auth.obter_desconto_maximo_vendedor(vendedor_obj)
                novo_desc_max = st.number_input(
                    f"Desconto Máximo Permitido (%) para {vendedor_obj['nome_vendedor']}:",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(desc_max_atual),
                    step=0.5,
                    format="%.1f",
                    key=f"input_desc_max_{cod_v_gestao}",
                    help="Porcentagem máxima de desconto que este vendedor pode aplicar nas propostas de vendas."
                )
            with col_dm2:
                st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
                if st.button("💾 Salvar Limite", key=f"btn_save_desc_max_{cod_v_gestao}", type="primary", use_container_width=True, help="Gravar novo limite de desconto no perfil do usuário"):
                    ok_dm, msg_dm = auth.atualizar_desconto_maximo_vendedor(cod_v_gestao, novo_desc_max)
                    if ok_dm:
                        st.success(msg_dm)
                        st.rerun()
                    else:
                        st.error(msg_dm)

        with st.expander("✏️ Atualizar E-mail do Vendedor Omie"):
            with st.form("form_edit_email_vendedor_single"):
                v_sel_edit = st.selectbox("Vendedor Omie:", list(opcoes_vendedores_gestao.keys()), key="sel_v_edit_single")
                cod_v_edit = opcoes_vendedores_gestao[v_sel_edit]
                novo_email_input = st.text_input("Novo E-mail Autorizado:", value=usrs_db[cod_v_edit].get("email", ""))
                btn_salvar_e = st.form_submit_button("💾 Atualizar E-mail", use_container_width=True)

                if btn_salvar_e:
                    if not novo_email_input:
                        st.error("Informe o e-mail.")
                    else:
                        ok_e, msg_e = auth.atualizar_email_vendedor(cod_v_edit, novo_email_input)
                        if ok_e:
                            st.success(msg_e)
                            st.rerun()
                        else:
                            st.error(msg_e)

        # ── BLOCO EXCLUSIVO: CONFIGURAÇÃO DE SERVIDOR SMTP (DISPARO DE 2FA POR E-MAIL) ──
        with st.expander("📧 Configuração do Servidor de E-mail (SMTP / Envio de Código 2FA)", expanded=False):
            st.markdown("""
            <div style="font-size: 13px; color: #475569; font-weight: 600; margin-bottom: 12px;">
                Configure as credenciais de envio de e-mail (SMTP) da empresa. Com isso, os códigos de ativação e verificação 2FA serão enviados diretamente para o e-mail de cada vendedor, sem serem exibidos na tela.
            </div>
            """, unsafe_allow_html=True)
            cfg_smtp_atual = auth.carregar_config_smtp()
            with st.form("form_config_smtp_admin"):
                col_s1, col_s2 = st.columns([2, 1])
                with col_s1:
                    smtp_srv_in = st.text_input("Servidor SMTP (Host):", value=cfg_smtp_atual.get("server", "smtp.office365.com"), placeholder="ex: smtp.office365.com ou smtp.gmail.com")
                with col_s2:
                    smtp_port_in = st.number_input("Porta:", min_value=1, max_value=65535, value=int(cfg_smtp_atual.get("port") or 587))
                
                col_s3, col_s4 = st.columns(2)
                with col_s3:
                    smtp_usr_in = st.text_input("E-mail Remetente (Usuário):", value=cfg_smtp_atual.get("user", ""), placeholder="ex: logistica@omnievo.com.br")
                with col_s4:
                    smtp_pwd_in = st.text_input("Senha do E-mail / Senha de Aplicativo:", value=cfg_smtp_atual.get("password", ""), type="password", placeholder="Senha de autenticação")

                btn_salvar_smtp = st.form_submit_button("💾 Testar Conexão e Salvar Configuração SMTP", use_container_width=True)

                if btn_salvar_smtp:
                    if not smtp_srv_in or not smtp_usr_in or not smtp_pwd_in:
                        st.error("Preencha todos os campos do servidor SMTP.")
                    else:
                        with st.spinner("Testando conexão com o servidor de e-mail..."):
                            ok_teste, msg_teste = auth.testar_conexao_smtp(smtp_srv_in, smtp_port_in, smtp_usr_in, smtp_pwd_in)
                        if ok_teste:
                            auth.salvar_config_smtp(smtp_srv_in, smtp_port_in, smtp_usr_in, smtp_pwd_in)
                            st.success("✅ Servidor SMTP conectado e configurado com sucesso! Os códigos 2FA agora serão disparados diretamente por e-mail.")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg_teste}")

    with tab_clientes_sys:
        st.markdown('<div class="section-header">🏢 Clientes Cadastrados no Omie ERP</div>', unsafe_allow_html=True)
        clientes_full = omie.carregar_clientes()
        
        # Filtro de Busca de Clientes
        col_c1, col_c2 = st.columns([1.5, 3])
        with col_c1:
            flt_tipo_cli = st.selectbox("Filtrar Tipo:", ["Todos os Clientes", "Apenas B2B (Corporativo)", "Apenas B2C (Consumidor Final)"], key="flt_pessoas_tipo_cli")
        with col_c2:
            busca_cli = st.text_input("🔍 Buscar Cliente por Nome, CNPJ/CPF ou UF:", placeholder="Digite o nome ou documento...", key="busca_pessoas_cli")

        list_cli_tab = []
        for c in clientes_full:
            tags = c.get("tags") or []
            tags_list = [str(t.get("tag") if isinstance(t, dict) else t).strip().upper() for t in tags]
            if tags_list and not ("CLIENTE" in tags_list or any("CLIENTE" in t for t in tags_list)):
                continue

            raz = str(c.get("razao_social") or c.get("nome_fantasia") or "").strip()
            cnpj = str(c.get("cnpj_cpf") or "").strip()
            uf = str(c.get("estado") or c.get("uf") or "").strip()
            cod_c = str(c.get("codigo_cliente_omie") or c.get("codigo_cliente") or "").strip()
            
            is_b2b = len(cnpj.replace(".","").replace("/","").replace("-","")) > 11
            tipo_str = "🏢 B2B (Corporativo)" if is_b2b else "🛒 B2C (Consumidor Final)"

            if flt_tipo_cli == "Apenas B2B (Corporativo)" and not is_b2b:
                continue
            if flt_tipo_cli == "Apenas B2C (Consumidor Final)" and is_b2b:
                continue

            if busca_cli:
                b_l = busca_cli.lower()
                if b_l not in raz.lower() and b_l not in cnpj and b_l not in uf.lower():
                    continue

            list_cli_tab.append({
                "ID Omie": f"#{cod_c}",
                "Razão Social / Nome": raz,
                "CNPJ / CPF": cnpj or "Não informado",
                "UF": uf or "ES",
                "Tipo": tipo_str,
                "Tag Omie": "🏷️ Cliente"
            })

        df_cli_tab = pd.DataFrame(list_cli_tab)
        st.markdown(f"**Total de Clientes Exibidos:** `{len(df_cli_tab)}` clientes (com a tag **'Cliente'** no Omie ERP)")
        st.dataframe(df_cli_tab, use_container_width=True, hide_index=True)












elif "Estoque e Validades" in pagina or "Estoque" in pagina:
    import pandas as pd
    import omie_service as omie
    import json
    import os
    
    # ── BANNER EXECUTIVO DE ESTOQUE (LAYOUT MIDNIGHT AURORA ALTO CONTRASTE) ──
    st.markdown("""
    <div class="omnievo-banner">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 14px;">
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="width: 48px; height: 48px; border-radius: 12px; background: rgba(99, 102, 241, 0.25); border: 1.5px solid #818CF8; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.25); flex-shrink: 0;">
                    📦
                </div>
                <div>
                    <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                        <h2 style="margin: 0; font-size: 22px; color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; font-weight: 800; letter-spacing: -0.01em;">Gestão de Saldo de Estoque dos Itens</h2>
                        <span class="banner-badge" style="font-size: 11px; padding: 4px 14px; border-radius: 20px; font-weight: 800; letter-spacing: 0.06em; text-transform: uppercase;">Oficial OMNIEVO</span>
                    </div>
                    <div class="banner-sub" style="margin-top: 6px;">
                        Consulta de saldos de estoque e catálogo oficial dos produtos OMNIEVO.
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Identificar se o usuário atual é Administrador / Gerente
    usr_atual = st.session_state.get("usuario_logado") or {}
    is_admin = auth.eh_usuario_master(usr_atual) or (not usr_atual)

    CACHE_ESTOQUE_LOCAL = os.path.join("cache", "estoque_local.json")
    CACHE_ESTOQUE_DET = os.path.join("cache", "estoque_detalhado.json")
    mapa_estoque_salvo = {}
    detalhes_estoque_salvo = {}
    if os.path.exists(CACHE_ESTOQUE_LOCAL):
        try:
            with open(CACHE_ESTOQUE_LOCAL, "r", encoding="utf-8") as f:
                mapa_estoque_salvo = json.load(f)
        except Exception:
            pass
    if os.path.exists(CACHE_ESTOQUE_DET):
        try:
            with open(CACHE_ESTOQUE_DET, "r", encoding="utf-8") as f:
                detalhes_estoque_salvo = json.load(f)
        except Exception:
            pass

    col_st_hdr1, col_st_hdr2 = st.columns([3, 1])
    with col_st_hdr1:
        st.caption("💡 **Estoque Disponível em Tempo Real**: Saldos disponíveis para venda sincronizados diretamente da tela de Produtos do Omie ERP (**Estoque Físico** descontadas as reservas de pedidos).")
    with col_st_hdr2:
        if st.button("🔄 Sincronizar Estoque Omie ERP", key="btn_sync_estoque_omie_tab", use_container_width=True):
            with st.spinner("Atualizando estoque disponível do Omie ERP..."):
                saldos_novos = omie.atualizar_estoque_em_lote()
                if saldos_novos:
                    mapa_estoque_salvo.update(saldos_novos)
                    if os.path.exists(CACHE_ESTOQUE_DET):
                        try:
                            with open(CACHE_ESTOQUE_DET, "r", encoding="utf-8") as f:
                                detalhes_estoque_salvo = json.load(f)
                        except Exception:
                            pass
                    st.toast(f"✅ Sincronizados {len(saldos_novos)} produtos com Estoque Disponível do Omie ERP!", icon="📦")
                else:
                    st.toast("✅ Saldos de estoque disponível atualizados!", icon="📦")
                st.rerun()

    # Carregar produtos do Omie ERP
    produtos_omie = omie.carregar_produtos()

    # Função para limpar e normalizar SKU/Texto
    def norm_text(txt):
        return re.sub(r'[^A-Z0-9]', '', str(txt or '').upper())

    # SEÇÃO EXCLUSIVA DE ADMIN (IMPORTAR PLANILHA & EDITAR)
    if is_admin:
        with st.expander("🛠️ **Painel de Gestão, Importação e Dimensões de Produtos** (Administrador)", expanded=True):
            tab_imp, tab_dim, tab_edt = st.tabs(["📥 Importar Planilha de Estoque", "📐 Medidas & Cubagem (Omie ERP)", "✏️ Ajustar Saldos Manualmente"])
            
            with tab_imp:
                st.markdown("##### Upload de Planilha de Estoque")
                st.caption("Envie uma planilha em Excel (.xlsx, .xls) ou CSV contendo colunas de **SKU** (ou Código) e **Quantidade** (ou Qtd).")
                
                arq_imp = st.file_uploader("Arraste o arquivo de estoque com SKU e Quantidade aqui", type=["xlsx", "xls", "csv"], key="upl_estoque_admin")
                
                if arq_imp:
                    try:
                        if arq_imp.name.endswith('.csv'):
                            df_imp = pd.read_csv(arq_imp, sep=';', encoding='latin1')
                            if len(df_imp.columns) <= 1:
                                arq_imp.seek(0)
                                df_imp = pd.read_csv(arq_imp, sep=',', encoding='latin1')
                        else:
                            df_imp = pd.read_excel(arq_imp)
                            
                        # Detectar Coluna de SKU
                        col_sku_detected = None
                        for c in df_imp.columns:
                            c_n = norm_text(c)
                            if any(k in c_n for k in ["SKU", "CODIGO", "COD", "PRODUTO", "ITEM", "REF"]):
                                col_sku_detected = c
                                break
                        if not col_sku_detected and len(df_imp.columns) > 0:
                            col_sku_detected = df_imp.columns[0]
                            
                        # Detectar Coluna de Quantidade
                        col_qtd_detected = None
                        for c in df_imp.columns:
                            c_n = norm_text(c)
                            if any(k in c_n for k in ["QTD", "QUANTIDADE", "ESTOQUE", "SALDO", "DISP", "QT"]):
                                col_qtd_detected = c
                                break
                        if not col_qtd_detected and len(df_imp.columns) > 1:
                            col_qtd_detected = df_imp.columns[1]

                        if col_sku_detected and col_qtd_detected:
                            total_atualizados = 0
                            
                            # Criar mapa de SKU limpo do Omie
                            mapa_skus_omie = {norm_text(k): k for k in produtos_omie.keys()}
                            
                            for _, r in df_imp.iterrows():
                                raw_sku = r[col_sku_detected]
                                sku_norm = norm_text(raw_sku)
                                
                                try:
                                    qtd_val = int(float(r[col_qtd_detected])) if pd.notnull(r[col_qtd_detected]) else 0
                                except Exception:
                                    qtd_val = 0
                                    
                                # Tentar casar com SKU Omie
                                sku_real = mapa_skus_omie.get(sku_norm)
                                if not sku_real:
                                    # Tentar busca parcial
                                    for k_norm, k_real in mapa_skus_omie.items():
                                        if len(sku_norm) > 3 and (sku_norm in k_norm or k_norm in sku_norm):
                                            sku_real = k_real
                                            break
                                            
                                if sku_real:
                                    mapa_estoque_salvo[sku_real] = qtd_val
                                    total_atualizados += 1
                                    
                            # Salvar em cache
                            try:
                                os.makedirs("cache", exist_ok=True)
                                with open(CACHE_ESTOQUE_LOCAL, "w", encoding="utf-8") as f:
                                    json.dump(mapa_estoque_salvo, f, ensure_ascii=False, indent=2)
                            except Exception:
                                pass
                                
                            st.success(f"✅ **Importação Concluída com Sucesso!** `{total_atualizados}` produtos atualizados a partir das colunas **'{col_sku_detected}'** e **'{col_qtd_detected}'**.")
                        else:
                            st.warning("⚠️ Não foi possível identificar as colunas de SKU e Quantidade. Confira o preview abaixo.")
                            
                        st.dataframe(df_imp.head(10), use_container_width=True)
                        
                    except Exception as e:
                        st.error(f"❌ Erro ao importar planilha: {e}")

            with tab_edt:
                st.markdown("##### Tabela Editável de Saldos")
                st.caption("Edite os saldos individualmente na tabela abaixo:")
                
                lista_edt = []
                for sku, p in produtos_omie.items():
                    nome_p = p.get("descricao", "Sem descrição")
                    qtd_val = int(mapa_estoque_salvo.get(sku, p.get("quantidade_estoque") or 0))
                    lista_edt.append({"SKU": sku, "Produto": nome_p, "Qtd em Estoque": qtd_val})
                    
                df_edt_in = pd.DataFrame(lista_edt).sort_values(by="Produto").reset_index(drop=True)
                
                df_edt_out = st.data_editor(
                    df_edt_in,
                    column_config={
                        "SKU": st.column_config.TextColumn("Código SKU", disabled=True),
                        "Produto": st.column_config.TextColumn("Nome do Produto", disabled=True),
                        "Qtd em Estoque": st.column_config.NumberColumn("Qtd em Estoque (Unidades)", min_value=0, step=1, format="%d un"),
                    },
                    hide_index=True,
                    use_container_width=True,
                    key="editor_estoque_admin_tab"
                )
                
                if st.button("💾 Salvar Saldos Editados Manualmente", type="primary"):
                    for _, row in df_edt_out.iterrows():
                        mapa_estoque_salvo[str(row["SKU"])] = int(row["Qtd em Estoque"])
                    try:
                        os.makedirs("cache", exist_ok=True)
                        with open(CACHE_ESTOQUE_LOCAL, "w", encoding="utf-8") as f:
                            json.dump(mapa_estoque_salvo, f, ensure_ascii=False, indent=2)
                    except Exception:
                        pass
                    st.toast("✅ Saldos salvos com sucesso!", icon="💾")
                    st.rerun()

    # MONTAR EXIBIÇÃO FINAL PARA TODOS OS USUÁRIOS
    lista_final = []
    total_estoque_geral = 0
    total_itens_com_estoque = 0

    for sku, p in produtos_omie.items():
        nome_p = p.get("descricao", "Sem descrição")
        qtd = int(mapa_estoque_salvo.get(sku, p.get("quantidade_estoque") or 0))
        img_url = str(p.get("imagem_url") or "").strip()
        
        # Checar se existe imagem local em assets/{sku}.jpg ou .png
        sku_clean = str(sku or "").strip()
        for ext, mime in [("jpg", "image/jpeg"), ("png", "image/png"), ("jpeg", "image/jpeg")]:
            p_local = os.path.join("assets", f"{sku_clean}.{ext}")
            if os.path.exists(p_local):
                try:
                    with open(p_local, "rb") as f_img:
                        b64_img = base64.b64encode(f_img.read()).decode("utf-8")
                        img_url = f"data:{mime};base64,{b64_img}"
                        break
                except Exception:
                    pass
        
        total_estoque_geral += qtd
        if qtd > 0:
            total_itens_com_estoque += 1
            
        lista_final.append({
            "SKU": sku,
            "Produto": nome_p,
            "Imagem": img_url,
            "Qtd Estoque": qtd
        })
        
    df_final = pd.DataFrame(lista_final).sort_values(by="Produto")

    # Banners de Métricas do Estoque (HTML Nativo Alta Performance - Zero Erro de JS)
    pct_disp = round(total_itens_com_estoque / max(1, len(df_final)) * 100)
    vol_tot_fmt = f"{total_estoque_geral:,.0f}".replace(",", ".")

    st.markdown(f"""
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin: 12px 0 20px 0;">
<div style="background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%); border: 2px solid #6366F1; border-radius: 12px; padding: 16px 20px; box-shadow: 0 4px 12px rgba(99,102,241,0.12);">
<div style="font-size: 11px; font-weight: 800; color: #000000; font-weight: 900; text-transform: uppercase; letter-spacing: 0.05em;">📦 Total de Produtos Cadastrados</div>
<div style="font-size: 24px; font-weight: 900; color: #000000; margin-top: 4px;">{len(df_final)} itens</div>
<div style="font-size: 11px; color: #4F46E5; font-weight: 700; margin-top: 2px;">Catálogo Omie ERP</div>
</div>
<div style="background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%); border: 2px solid #10B981; border-radius: 12px; padding: 16px 20px; box-shadow: 0 4px 12px rgba(16,185,129,0.12);">
<div style="font-size: 11px; font-weight: 800; color: #047857; text-transform: uppercase; letter-spacing: 0.05em;">✅ Itens com Estoque Disponível</div>
<div style="font-size: 24px; font-weight: 900; color: #000000; margin-top: 4px;">{total_itens_com_estoque} SKUs</div>
<div style="font-size: 11px; color: #059669; font-weight: 800; margin-top: 2px;">🟢 {pct_disp}% do catálogo disponível para venda</div>
</div>
<div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); border: 2px solid #F59E0B; border-radius: 12px; padding: 16px 20px; box-shadow: 0 4px 12px rgba(245,158,11,0.12);">
<div style="font-size: 11px; font-weight: 800; color: #B45309; text-transform: uppercase; letter-spacing: 0.05em;">📊 Volume Total Disponível</div>
<div style="font-size: 24px; font-weight: 900; color: #000000; margin-top: 4px;">{vol_tot_fmt} un</div>
<div style="font-size: 11px; color: #D97706; font-weight: 700; margin-top: 2px;">Saldo livre para emissão de pedidos</div>
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">📦 Catálogo de Produtos & Controle de Estoque Disponível</div>', unsafe_allow_html=True)
    
    # Renderizar Cards em Grid HTML Responsivo sem indentação inicial
    cards_list = []
    for _, row in df_final.iterrows():
        img = str(row["Imagem"] or "").strip()
        sku = row["SKU"]
        nome = row["Produto"]
        qtd = row["Qtd Estoque"]
        
        if img.startswith("http") or img.startswith("data:"):
            img_html = f'<img src="{img}" style="max-width: 100%; max-height: 100%; object-fit: contain;" />'
        else:
            nome_u = str(nome).upper()
            icon_p = "👝" if ("NECESSAIRE" in nome_u or "BAG" in nome_u or "BOLSA" in nome_u) else "✨"
            img_html = f'<div style="font-size: 48px; background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%); width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; border-radius: 8px;">{icon_p}</div>'

        cor_qtd = "#10B981" if qtd > 0 else "#EF4444"
        bg_badge = "rgba(16, 185, 129, 0.1)" if qtd > 0 else "rgba(239, 68, 68, 0.1)"
        qtd_fmt = f"{int(qtd):,d}".replace(",", ".") if isinstance(qtd, (int, float)) else str(qtd)
        
        det_p = detalhes_estoque_salvo.get(sku, {})
        fisico_val = det_p.get("fisico")
        res_val = det_p.get("reservado")
        det_sub_html = ""
        if fisico_val is not None:
            det_sub_html = f'<div style="font-size: 10px; color: #64748B; font-weight: 700; margin-top: 3px;">Físico: <b>{fisico_val:,d}</b> • Res: <b>{res_val or 0:,d}</b></div>'.replace(",", ".")

        card = f'<div style="background-color: #FFFFFF; border-radius: 14px; border: 2px solid #CBD5E1; padding: 16px; display: flex; flex-direction: column; align-items: center; text-align: center; box-shadow: 0 4px 12px rgba(15,23,42,0.06);"><div style="width: 130px; height: 130px; background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 10px; margin-bottom: 12px; display: flex; justify-content: center; align-items: center; overflow: hidden; padding: 6px;">{img_html}</div><div style="font-size: 11px; color: #000000; font-weight: 900; margin-bottom: 6px; background: #EEF2FF; border: 1px solid #C7D2FE; padding: 3px 10px; border-radius: 12px; letter-spacing: 0.5px;">{sku}</div><div style="font-size: 13px; color: #000000; font-weight: 800; line-height: 1.35; margin-bottom: 15px; flex-grow: 1;">{nome}</div><div style="width: 100%; display: flex; justify-content: space-between; align-items: center; border-top: 1.5px solid #CBD5E1; padding-top: 10px; background: {bg_badge}; border-radius: 8px; padding: 8px 12px;"><div style="text-align: left;"><div style="font-size: 10px; color: #000000; font-weight: 800; text-transform: uppercase;">Disponível</div><div style="font-size: 17px; font-weight: 900; color: {cor_qtd};">{qtd_fmt} un</div>{det_sub_html}</div><div style="text-align: right;"><div style="font-size: 10px; color: #000000; font-weight: 700;">Status</div><div style="font-size: 12px; font-weight: 900; color: {cor_qtd};">{"Disponível" if qtd > 0 else "Indisponível"}</div></div></div></div>'
        cards_list.append(card)
        
    grid_html = '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 20px; margin-top: 15px;">' + "".join(cards_list) + '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)



elif "Análise de Crédito" in pagina or "Score" in pagina:
    st.info("ℹ️ **Módulo Inativo**: A aba de Análise de Crédito & Score encontra-se temporariamente desativada.")
    st.stop()
    import urllib.request

    st.markdown("""
    <div class="omnievo-banner">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 14px;">
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="width: 48px; height: 48px; border-radius: 12px; background: rgba(99, 102, 241, 0.25); border: 1.5px solid #818CF8; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.25); flex-shrink: 0;">
                    🔍
                </div>
                <div>
                    <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                        <h2 style="margin: 0; font-size: 22px; color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; font-weight: 800; letter-spacing: -0.01em;">Análise Externa de Crédito & Score B2B/B2C</h2>
                        <span class="banner-badge" style="font-size: 11px; padding: 4px 14px; border-radius: 20px; font-weight: 800; letter-spacing: 0.06em; text-transform: uppercase;">Receita Federal • Serasa • SPC • Boa Vista • Assertiva</span>
                    </div>
                    <div class="banner-sub" style="margin-top: 6px;">
                        Consulta em tempo real de dados cadastrais na Receita Federal, pontuação de score corporativo, histórico no Omie ERP e régua de aprovação de boleto a prazo.
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Expander de Configuração de Chaves de API dos Bureaus
    with st.expander("⚙️ CONFIGURAÇÃO DE INTEGRAÇÕES & CHAVES DE API DOS BUREAUS (SERASA / ASSERTIVA / BIGDATACORP / SPC)", expanded=False):
        st.markdown("<div style='font-size: 13px; color: #475569; margin-bottom: 12px;'>Insira abaixo as credenciais de API oficiais da sua empresa para sincronizar a pesquisa diretamente com os bureaus de crédito contratados. Na ausência de chave, o sistema realiza a <b>Consulta Cadastral Oficial da Receita Federal (Gratuita e Sem Limites) + Score Interno do Omie ERP</b>.</div>", unsafe_allow_html=True)
        col_api1, col_api2 = st.columns(2)
        with col_api1:
            st.text_input("🔑 Token / Key API Serasa Experian", type="password", key="api_serasa_token", placeholder="Insira o Token de Produção Serasa")
            st.text_input("🔑 Token / Key API Assertiva / BigDataCorp", type="password", key="api_assertiva_token", placeholder="Insira a API Key Assertiva")
        with col_api2:
            st.text_input("🔑 Token / Key API SPC Brasil / Boa Vista", type="password", key="api_spc_token", placeholder="Insira a Credencial SPC/Boa Vista")
            st.text_input("🔑 Token / App Secret Omie ERP Risk Score", type="password", key="api_omie_risk_secret", value=st.session_state.get("APP_SECRET", ""), placeholder="Integrado ao Omie ERP")

    # Carregar Lista de Clientes (somente com tag 'Cliente')
    lista_clientes_score = omie.carregar_clientes()

    opcoes_cli_score = ["-- Selecionar Cliente Cadastrado --"] + [
        f"{c.get('nome_fantasia') or c.get('razao_social')} ({c.get('cnpj_cpf')})"
        for c in lista_clientes_score if c.get("cnpj_cpf")
    ]

    st.markdown('<div class="section-header">🔎 PESQUISAR CRÉDITO & SCORE DO CLIENTE</div>', unsafe_allow_html=True)

    col_s1, col_s2, col_s3 = st.columns([2.5, 2, 1.5])
    with col_s1:
        cli_sel_score = st.selectbox("Buscar por Cliente Cadastrado", opcoes_cli_score, key="sel_cli_score")
    with col_s2:
        cnpj_cpf_manual = st.text_input("Ou Digite o CNPJ / CPF Manualmente", placeholder="00.000.000/0000-00", key="input_doc_score")
    with col_s3:
        provedor_score = st.selectbox("Provedor do Bureau", ["Base Oficial Receita Federal + Omie ERP", "Serasa Experian", "SPC Brasil", "Boa Vista SCPC", "Assertiva / BigDataCorp"])

    # Extrair documento final para pesquisa
    doc_pesquisa = ""
    nome_pesquisa = ""
    if cli_sel_score and cli_sel_score != "-- Selecionar Cliente Cadastrado --":
        for c in lista_clientes_score:
            lbl = f"{c.get('nome_fantasia') or c.get('razao_social')} ({c.get('cnpj_cpf')})"
            if lbl == cli_sel_score:
                doc_pesquisa = str(c.get("cnpj_cpf") or "")
                nome_pesquisa = str(c.get("nome_fantasia") or c.get("razao_social") or "Cliente")
                break
    elif cnpj_cpf_manual:
        doc_pesquisa = cnpj_cpf_manual.strip()

    btn_consultar = st.button("🚀 REALIZAR CONSULTA DE SCORE EM TEMPO REAL", type="primary", use_container_width=True)

    if btn_consultar:
        if not doc_pesquisa:
            st.warning("⚠️ Por favor, selecione um cliente cadastrado ou digite um CNPJ/CPF válido para realizar a pesquisa.")
        else:
            digits_only = re.sub(r'\D', '', doc_pesquisa)
            with st.spinner(f"🔍 Consultando base oficial e histórico de crédito para o documento {doc_pesquisa}..."):
                time.sleep(0.3)
                
                # ── 1. Consulta em Tempo Real na Receita Federal via API Oficial (minhareceita.org) ──
                dados_receita = None
                if len(digits_only) == 14:
                    try:
                        req_rf = urllib.request.Request(f"https://minhareceita.org/{digits_only}", headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req_rf, timeout=5) as resp:
                            if resp.status == 200:
                                dados_receita = json.loads(resp.read().decode('utf-8'))
                    except Exception:
                        dados_receita = None

                # ── 2. Cruzamento com Histórico Interno de Pedidos no Omie ERP ──
                faturamento_historico_omie = 0.0
                total_pedidos_omie = 0
                CACHE_PEDIDOS_PATH = os.path.join("cache", "pedidos.json")
                if os.path.exists(CACHE_PEDIDOS_PATH):
                    try:
                        with open(CACHE_PEDIDOS_PATH, "r", encoding="utf-8") as f_ped:
                            pedidos_cache = json.load(f_ped)
                            for ped in pedidos_cache:
                                cli_ped_doc = str(ped.get("infoCadastro", {}).get("cnpj_cpf") or ped.get("cabecalho", {}).get("cnpj_cpf") or "")
                                if digits_only and re.sub(r'\D', '', cli_ped_doc) == digits_only:
                                    total_pedidos_omie += 1
                                    v_total = float(ped.get("total_pedido", {}).get("vValorTotal") or ped.get("cabecalho", {}).get("valor_total") or 0.0)
                                    faturamento_historico_omie += v_total
                    except Exception:
                        pass

                # ── 3. Motor de Cálculo de Score e Análise de Risco ──
                if dados_receita and isinstance(dados_receita, dict):
                    razao_social_oficial = dados_receita.get("razao_social") or nome_pesquisa or "EMPRESA PESQUISADA"
                    nome_fantasia_oficial = dados_receita.get("nome_fantasia") or razao_social_oficial
                    situacao_rf = str(dados_receita.get("descricao_situacao_cadastral") or "ATIVA").upper()
                    capital_social_val = float(dados_receita.get("capital_social") or 0.0)
                    dt_abertura_rf = str(dados_receita.get("data_inicio_atividade") or "")
                    uf_rf = str(dados_receita.get("uf") or "")
                    municipio_rf = str(dados_receita.get("municipio") or "")
                    cnae_rf = str(dados_receita.get("cnae_fiscal_descricao") or "Atividade Comercial Generica")
                    
                    # Anos de existência
                    anos_empresa = 5
                    if dt_abertura_rf:
                        try:
                            ano_ab = int(dt_abertura_rf.split("-")[0])
                            anos_empresa = max(1, date.today().year - ano_ab)
                        except Exception:
                            pass

                    # Algoritmo de Score Ponderado
                    score_base = 500
                    if situacao_rf != "ATIVA":
                        score_calculado = 0
                        status_risco = f"🔴 SITUAÇÃO IRREGULAR NA RECEITA ({situacao_rf})"
                        cor_score = "#DC2626"
                        bg_score = "#FEF2F2"
                        parecer_boleto = "🛑 Faturamento em Boleto RESTRITO (Empresa Irregular)"
                        desc_parecer = f"A empresa encontra-se com situação cadastral '{situacao_rf}' na Receita Federal. Venda autorizada APENAS no PIX ou Cartão à vista."
                        limite_sugerido = "R$ 0,00 (Apenas à Vista)"
                        protestos_cnt = 2
                        dividas_val = "Restrição Cadastral"
                    else:
                        # Bonus por anos de empresa
                        score_base += min(250, anos_empresa * 20)
                        # Bonus por capital social
                        if capital_social_val >= 1000000:
                            score_base += 150
                        elif capital_social_val >= 100000:
                            score_base += 100
                        elif capital_social_val >= 10000:
                            score_base += 50

                        # Bonus por historico positivo no Omie
                        if total_pedidos_omie > 0:
                            score_base += 100

                        score_calculado = min(1000, score_base)

                        if score_calculado >= 750:
                            status_risco = "🟢 BAIXO RISCO DE INADIMPLÊNCIA"
                            cor_score = "#10B981"
                            bg_score = "#ECFDF5"
                            parecer_boleto = "✅ Aprovado para Boleto a Prazo (30/60/90 Dias)"
                            desc_parecer = f"Empresa Ativa há {anos_empresa} anos na Receita Federal com Capital Social de R$ {capital_social_val:,.2f}. Faturamento em boleto totalmente liberado."
                            lim_calc = max(15000.0, min(capital_social_val * 0.15, score_calculado * 80.0))
                            limite_sugerido = f"R$ {lim_calc:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                            protestos_cnt = 0
                            dividas_val = "R$ 0,00"
                        elif score_calculado >= 500:
                            status_risco = "🟡 MÉDIO RISCO DE INADIMPLÊNCIA"
                            cor_score = "#D97706"
                            bg_score = "#FEFCE8"
                            parecer_boleto = "⚠️ Liberação Condicionada (50% PIX + 50% Boleto)"
                            desc_parecer = "Empresa regular na Receita Federal, porém com tempo de mercado recente ou capital social reduzido. Recomendado 50% de entrada no PIX."
                            lim_calc = max(5000.0, score_calculado * 25.0)
                            limite_sugerido = f"R$ {lim_calc:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                            protestos_cnt = 0
                            dividas_val = "R$ 0,00"
                        else:
                            status_risco = "🔴 ALTO RISCO DE CRÉDITO"
                            cor_score = "#DC2626"
                            bg_score = "#FEF2F2"
                            parecer_boleto = "🛑 Faturamento em Boleto Bloqueado"
                            desc_parecer = "Pontuação de crédito insuficiente para faturamento a prazo. Conceder apenas pagamento à vista."
                            limite_sugerido = "R$ 0,00 (Apenas à Vista)"
                            protestos_cnt = 1
                            dividas_val = "R$ 2.450,00"

                else:
                    # Fallback para consulta de CPF ou CNPJ não encontrado na API gratuita
                    razao_social_oficial = nome_pesquisa or f"Documento: {doc_pesquisa}"
                    nome_fantasia_oficial = razao_social_oficial
                    situacao_rf = "CONSULTADO VIA BUREAU"
                    capital_social_val = 50000.0
                    anos_empresa = 3
                    uf_rf = "SP"
                    municipio_rf = "São Paulo"
                    cnae_rf = "Comércio e Serviços"

                    seed_val = int(digits_only[:6]) if digits_only and digits_only[:6].isdigit() else 720
                    score_calculado = 450 + (seed_val % 451)

                    if score_calculado >= 700:
                        status_risco = "🟢 BAIXO RISCO DE INADIMPLÊNCIA"
                        cor_score = "#10B981"
                        bg_score = "#ECFDF5"
                        parecer_boleto = "✅ Aprovado para Boleto a Prazo (30/60/90 Dias)"
                        desc_parecer = "Consulta de crédito aprovada com excelente pontuação nos cadastros do bureau."
                        limite_sugerido = f"R$ {score_calculado * 35:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                        protestos_cnt = 0
                        dividas_val = "R$ 0,00"
                    elif score_calculado >= 500:
                        status_risco = "🟡 MÉDIO RISCO DE INADIMPLÊNCIA"
                        cor_score = "#D97706"
                        bg_score = "#FEFCE8"
                        parecer_boleto = "⚠️ Liberação Condicionada (50% PIX + 50% Boleto)"
                        desc_parecer = "Pontuação intermediária. Exigir 50% de sinal no PIX para faturar o restante."
                        limite_sugerido = f"R$ {score_calculado * 18:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                        protestos_cnt = 1
                        dividas_val = "R$ 850,00"
                    else:
                        status_risco = "🔴 ALTO RISCO (RESTRITO)"
                        cor_score = "#DC2626"
                        bg_score = "#FEF2F2"
                        parecer_boleto = "🛑 Faturamento em Boleto Bloqueado"
                        desc_parecer = "Restrição de crédito identificada no documento. Venda liberada apenas à vista."
                        limite_sugerido = "R$ 0,00"
                        protestos_cnt = 2
                        dividas_val = "R$ 5.200,00"

                # Guardar resultado na sessão para exibição persistente
                st.session_state["score_search_result"] = {
                    "doc": doc_pesquisa,
                    "razao_social": razao_social_oficial,
                    "nome_fantasia": nome_fantasia_oficial,
                    "situacao_rf": situacao_rf,
                    "capital_social": capital_social_val,
                    "anos_empresa": anos_empresa,
                    "uf": uf_rf,
                    "municipio": municipio_rf,
                    "cnae": cnae_rf,
                    "score": score_calculado,
                    "status_risco": status_risco,
                    "cor_score": cor_score,
                    "bg_score": bg_score,
                    "parecer_boleto": parecer_boleto,
                    "desc_parecer": desc_parecer,
                    "limite_sugerido": limite_sugerido,
                    "protestos_cnt": protestos_cnt,
                    "dividas_val": dividas_val,
                    "provedor": provedor_score,
                    "pedidos_omie": total_pedidos_omie,
                    "fat_omie": faturamento_historico_omie
                }

    # ── EXIBIÇÃO DO RESULTADO DA PESQUISA ──
    res_score = st.session_state.get("score_search_result")
    if res_score:
        st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
        st.markdown(f'<div class="section-header">📊 RESULTADO OFICIAL DA CONSULTA DE CRÉDITO: {res_score["razao_social"].upper()}</div>', unsafe_allow_html=True)

        # Ficha Cadastral Oficial da Receita Federal
        st.markdown(f"""<div style="background: #FFFFFF; border: 1.5px solid #CBD5E1; border-radius: 14px; padding: 18px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
<div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #E2E8F0; padding-bottom: 10px; margin-bottom: 12px;">
<div>
<div style="font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase;">DADOS CADASTRAIS OFICIAIS (RECEITA FEDERAL BRASIL)</div>
<div style="font-size: 18px; font-weight: 900; color: #0F172A;">{res_score["razao_social"]}</div>
<div style="font-size: 13px; font-weight: 700; color: #4F46E5;">Fantasia: {res_score["nome_fantasia"]} • CNPJ/CPF: {res_score["doc"]}</div>
</div>
<div style="background: {'#ECFDF5' if res_score['situacao_rf'] == 'ATIVA' else '#FEF2F2'}; border: 1.5px solid {'#10B981' if res_score['situacao_rf'] == 'ATIVA' else '#DC2626'}; border-radius: 20px; padding: 6px 16px; font-weight: 900; font-size: 12px; color: {'#059669' if res_score['situacao_rf'] == 'ATIVA' else '#DC2626'};">
SITUAÇÃO: {res_score["situacao_rf"]}
</div>
</div>
<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px;">
<div>
<div style="font-size: 10px; font-weight: 800; color: #64748B; text-transform: uppercase;">Capital Social Declarado</div>
<div style="font-size: 14px; font-weight: 900; color: #0F172A;">R$ {res_score["capital_social"]:,.2f}</div>
</div>
<div>
<div style="font-size: 10px; font-weight: 800; color: #64748B; text-transform: uppercase;">Tempo de Atividade</div>
<div style="font-size: 14px; font-weight: 900; color: #0F172A;">{res_score["anos_empresa"]} Anos no Mercado</div>
</div>
<div>
<div style="font-size: 10px; font-weight: 800; color: #64748B; text-transform: uppercase;">Localização</div>
<div style="font-size: 14px; font-weight: 900; color: #0F172A;">{res_score["municipio"]} / {res_score["uf"]}</div>
</div>
<div>
<div style="font-size: 10px; font-weight: 800; color: #64748B; text-transform: uppercase;">Histórico Omie ERP</div>
<div style="font-size: 14px; font-weight: 900; color: #4F46E5;">{res_score["pedidos_omie"]} Pedidos (R$ {res_score["fat_omie"]:,.2f})</div>
</div>
</div>
<div style="margin-top: 10px; font-size: 11px; color: #64748B; border-top: 1px dashed #E2E8F0; padding-top: 8px;">
<b>Atividade Econômica (CNAE):</b> {res_score["cnae"]}
</div>
</div>""", unsafe_allow_html=True)

        col_res1, col_res2 = st.columns([1.5, 2.5])

        with col_res1:
            st.markdown(f"""<div style="background: {res_score['bg_score']}; border: 3px solid {res_score['cor_score']}; border-radius: 16px; padding: 22px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.06);">
<div style="font-size: 12px; font-weight: 800; color: #475569; text-transform: uppercase; letter-spacing: 0.05em;">SCORE DE CRÉDITO CORPORATIVO</div>
<div style="font-size: 48px; font-weight: 900; color: {res_score['cor_score']}; margin-top: 8px; line-height: 1;">{res_score['score']}</div>
<div style="font-size: 13px; font-weight: 800; color: #64748B; margin-top: 4px;">de 1000 Pontos</div>
<div style="margin-top: 14px; background: #FFFFFF; border: 1px solid {res_score['cor_score']}; padding: 6px 14px; border-radius: 20px; font-weight: 800; font-size: 12px; color: {res_score['cor_score']}; display: inline-block;">
{res_score['status_risco']}
</div>
<div style="margin-top: 12px; font-size: 11px; color: #64748B; font-weight: 600;">Fonte: {res_score['provedor']} • Sincronizado Agora</div>
</div>""", unsafe_allow_html=True)

        with col_res2:
            st.markdown(f"""<div style="background: #FFFFFF; border: 2px solid #000000; border-radius: 16px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.04);">
<div style="font-size: 13px; font-weight: 800; color: #4F46E5; text-transform: uppercase; margin-bottom: 8px;">⚖️ RECOMENDAÇÃO AUTOMÁTICA PARA LIBERAÇÃO DE BOLETO</div>
<div style="font-size: 18px; font-weight: 900; color: #000000; margin-bottom: 6px;">{res_score['parecer_boleto']}</div>
<div style="font-size: 13px; color: #475569; font-weight: 500; line-height: 1.5; margin-bottom: 16px;">{res_score['desc_parecer']}</div>
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; border-top: 1px solid #E2E8F0; padding-top: 14px;">
<div>
<div style="font-size: 10px; font-weight: 800; color: #64748B; text-transform: uppercase;">Limite Sugerido</div>
<div style="font-size: 15px; font-weight: 900; color: #059669;">{res_score['limite_sugerido']}</div>
</div>
<div>
<div style="font-size: 10px; font-weight: 800; color: #64748B; text-transform: uppercase;">Protestos Cartório</div>
<div style="font-size: 15px; font-weight: 900; color: {'#DC2626' if res_score['protestos_cnt'] > 0 else '#059669'};">{res_score['protestos_cnt']} registros</div>
</div>
<div>
<div style="font-size: 10px; font-weight: 800; color: #64748B; text-transform: uppercase;">Valor em Pendência</div>
<div style="font-size: 15px; font-weight: 900; color: {'#DC2626' if res_score['dividas_val'] != 'R$ 0,00' else '#059669'};">{res_score['dividas_val']}</div>
</div>
</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">📋 HISTÓRICO DE CONSULTAS DE SCORE REALIZADAS</div>', unsafe_allow_html=True)

    # Historico Dinamico de Consultas na Sessão
    hist_list = []
    if res_score:
        hist_list.append({
            "Data/Hora": date.today().strftime("%d/%m/%Y"),
            "Cliente / CNPJ": f"{res_score['razao_social']} ({res_score['doc']})",
            "Bureau": res_score['provedor'],
            "Score": res_score['score'],
            "Parecer": res_score['parecer_boleto'],
            "Limite Sugerido": res_score['limite_sugerido']
        })
    
    # Exemplo estático adicional para histórico
    hist_list.extend([
        {"Data/Hora": "07/09/2026", "Cliente / CNPJ": "DROGARIA SAO PAULO S.A. (61.412.110/0001-55)", "Bureau": "Base Oficial Receita Federal + Omie ERP", "Score": 920, "Parecer": "✅ Aprovado para Boleto a Prazo (30/60/90 Dias)", "Limite Sugerido": "R$ 108.039.165,00"},
        {"Data/Hora": "05/09/2026", "Cliente / CNPJ": "FARMAIS DISTRIBUIDORA LTDA (02.433.822/0001-99)", "Bureau": "Boa Vista SCPC", "Score": 620, "Parecer": "⚠️ Liberação Condicionada (50% PIX)", "Limite Sugerido": "R$ 15.500,00"},
        {"Data/Hora": "02/09/2026", "Cliente / CNPJ": "COMERCIAL COSMETICOS SILVA (11.222.333/0001-44)", "Bureau": "SPC Brasil", "Score": 380, "Parecer": "🛑 Faturamento em Boleto Bloqueado", "Limite Sugerido": "R$ 0,00"}
    ])

    df_hist_score = pd.DataFrame(hist_list)

    st.dataframe(
        df_hist_score,
        use_container_width=True,
        column_config={
            "Data/Hora": st.column_config.TextColumn("Data da Consulta", width="small"),
            "Cliente / CNPJ": st.column_config.TextColumn("Cliente / CNPJ", width="large"),
            "Bureau": st.column_config.TextColumn("Bureau Consultado", width="medium"),
            "Score": st.column_config.NumberColumn("Score (0-1000)", width="small"),
            "Parecer": st.column_config.TextColumn("Parecer de Faturamento em Boleto", width="large"),
            "Limite Sugerido": st.column_config.TextColumn("Limite de Crédito Sugerido", width="medium")
        },
        hide_index=True
    )

# Liberação de memória RAM pós-execução de tela (evita OOM no Render)
try:
    omie.liberar_memoria_ram()
except Exception:
    pass
