# -*- coding: utf-8 -*-
import streamlit as st
import base64
import os

# =================================================================
# 1. CONFIGURACIÓN Y ESTILO CORPORATIVO
# =================================================================
st.set_page_config(page_title="Conversor | Proyectos Estructurales", layout="wide")

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

st.markdown("""
    <style>
    .unit-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid #003366;
        margin-bottom: 15px;
        padding-bottom: 5px;
    }
    .unit-title {
        color: #003366;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .unit-icon {
        width: 60px; /* Tamaño uniforme para todos los iconos */
        height: auto;
    }
    .stNumberInput input { color: #003366 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ Conversor de Unidades | Structural Lab")

# =================================================================
# 2. MOTOR DE SINCRONIZACIÓN (FACTORES ORIGINALES VB)
# =================================================================
CONV_DATA = {
    "F1": {"label": "Presión", "icon": "presion.jpg", "factors": {"psf": 1.0, "psi": 0.006944, "kgf/m2": 4.882428, "kPa": 0.04788, "MPa": 0.000048}},
    "F2": {"label": "Cargas Distribuidas", "icon": "Cargas.jpg", "factors": {"lbf/ft": 1.0, "lbf/in": 0.083333, "N/mm": 0.014594, "kN/m": 0.014594, "kgf/m": 1.488164}},
    "F3": {"label": "Velocidad", "icon": "velocidad.jpg", "factors": {"mi/hr": 1.0, "km/hr": 1.609344, "m/sec": 0.44704}},
    "F4": {"label": "Momento Flector", "icon": "Momento.jpg", "factors": {"kip-ft": 1.0, "kip-in": 12.0, "lbf-ft": 1000.0, "lbf-in": 12000.0, "N-m": 1355.818, "kN-m": 1.355, "kgf-m": 138.255}},
    "F5": {"label": "Área", "icon": "area.jpg", "factors": {"in2": 1.0, "ft2": 0.007, "m2": 0.001, "cm2": 6.452, "mm2": 645.16}},
    "F6": {"label": "Módulo Sección", "icon": "seccional.jpg", "factors": {"in3": 1.0, "ft3": 0.001, "m3": 0.00002, "cm3": 16.387, "mm3": 16387.064}},
    "F7": {"label": "Inercia", "icon": "Inercia.jpg", "factors": {"in4": 1.0, "ft4": 0.00005, "m4": 0.0000004, "cm4": 41.623, "mm4": 416231.426}}
}

def sync(group_id, unit_id):
    val = st.session_state[f"{group_id}_{unit_id}"]
    factors = CONV_DATA[group_id]["factors"]
    base_val = val / factors[unit_id]
    for u, f in factors.items():
        if u != unit_id:
            st.session_state[f"{group_id}_{u}"] = base_val * f

# Inicialización de estados
for g_id, g_info in CONV_DATA.items():
    for u_id in g_info["factors"]:
        if f"{g_id}_{u_id}" not in st.session_state:
            st.session_state[f"{g_id}_{u_id}"] = 1.0 if u_id in ["psf", "lbf/ft", "mi/hr", "kip-ft", "in2", "in3", "in4"] else g_info["factors"][u_id]

# =================================================================
# 3. INTERFAZ GRÁFICA CON ICONOS UNIFORMES
# =================================================================
def render_group(group_id):
    info = CONV_DATA[group_id]
    icon_b64 = get_base64_image(info["icon"])
    
    # Encabezado con Título e Icono alineados
    header_html = f"""
    <div class="unit-header">
        <span class="unit-title">{group_id}: {info['label']}</span>
        <img src="data:image/jpeg;base64,{icon_b64}" class="unit-icon">
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
    
    for u in info["factors"]:
        # El formato de decimales se ajusta según el factor
        fmt = "%.6f" if info["factors"][u] < 0.001 else "%.3f"
        st.number_input(u, key=f"{group_id}_{u}", format=fmt, on_change=sync, args=(group_id, u))

c1, c2, c3 = st.columns(3)

with c1:
    render_group("F1")
    st.markdown("<br>", unsafe_allow_html=True)
    render_group("F2")

with c2:
    render_group("F3")
    st.markdown("<br>", unsafe_allow_html=True)
    render_group("F4")
    st.markdown("<br>", unsafe_allow_html=True)
    render_group("F6")

with c3:
    render_group("F5")
    st.markdown("<br>", unsafe_allow_html=True)
    render_group("F7")

st.divider()
st.info("💡 Cambia cualquier valor para actualizar el grupo completo instantáneamente.")