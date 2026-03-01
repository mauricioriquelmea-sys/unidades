# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

# =================================================================
# 1. CONFIGURACIÓN Y ESTILO CORPORATIVO
# =================================================================
st.set_page_config(page_title="Conversor de Unidades | Mauricio Riquelme", layout="wide")

st.markdown("""
    <style>
    .unit-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin-bottom: 20px;
    }
    .unit-title {
        color: #003366;
        font-weight: bold;
        border-bottom: 2px solid #003366;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    stNumberInput label { font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ Conversor de Unidades de Ingeniería")
st.caption("Structural Lab | Proyectos Estructurales EIRL")

# =================================================================
# 2. LÓGICA DE CONVERSIÓN (PORTADA DESDE VISUAL BASIC)
# =================================================================

def update_units(group_name, key_changed, value):
    """Sincroniza todas las unidades del grupo basándose en la que cambió."""
    if value is None: return

    # F1: PRESIÓN (Basado en psf como unidad base)
    if group_name == "F1":
        factors = {"psf": 1.0, "psi": 0.006944, "kgf/m2": 4.882428, "kPa": 0.04788, "MPa": 0.000048}
        base_val = value / factors[key_changed]
        for k in factors: st.session_state[f"F1_{k}"] = round(base_val * factors[k], 6)

    # F2: CARGAS UNIFORMEMENTE DISTRIBUIDAS (Basado en lbf/ft)
    elif group_name == "F2":
        factors = {"lbf/ft": 1.0, "lbf/in": 0.083333, "N/mm": 0.014594, "kN/m": 0.014594, "kgf/m": 1.488164}
        base_val = value / factors[key_changed]
        for k in factors: st.session_state[f"F2_{k}"] = round(base_val * factors[k], 6)

    # F3: VELOCIDAD (Basado en mi/hr)
    elif group_name == "F3":
        factors = {"mi/hr": 1.0, "km/hr": 1.609344, "m/sec": 0.44704}
        base_val = value / factors[key_changed]
        for k in factors: st.session_state[f"F3_{k}"] = round(base_val * factors[k], 4)

    # F4: MOMENTO FLECTOR (Basado en kip-ft)
    elif group_name == "F4":
        factors = {"kip-ft": 1.0, "kip-in": 12.0, "lbf-ft": 1000.0, "lbf-in": 12000.0, "N-m": 1355.8179, "kN-m": 1.3558, "kgf-m": 138.255}
        base_val = value / factors[key_changed]
        for k in factors: st.session_state[f"F4_{k}"] = round(base_val * factors[k], 4)

    # F5: ÁREA (Basado en in2)
    elif group_name == "F5":
        factors = {"in2": 1.0, "ft2": 0.006944, "m2": 0.000645, "cm2": 6.4516, "mm2": 645.16}
        base_val = value / factors[key_changed]
        for k in factors: st.session_state[f"F5_{k}"] = round(base_val * factors[k], 6)

    # F6: MÓDULO SECCIONAL / RESISTENTE (Basado en in3)
    elif group_name == "F6":
        factors = {"in3": 1.0, "ft3": 0.0005787, "m3": 0.00001639, "cm3": 16.387, "mm3": 16387.064}
        base_val = value / factors[key_changed]
        for k in factors: st.session_state[f"F6_{k}"] = round(base_val * factors[k], 6)

    # F7: INERCIA (Basado en in4)
    elif group_name == "F7":
        factors = {"in4": 1.0, "ft4": 0.0000482, "m4": 0.000000416, "cm4": 41.6231, "mm4": 416231.42}
        base_val = value / factors[key_changed]
        for k in factors: st.session_state[f"F7_{k}"] = round(base_val * factors[k], 6)

# Inicialización de estados
groups = {
    "F1": ["psf", "psi", "kgf/m2", "kPa", "MPa"],
    "F2": ["lbf/ft", "lbf/in", "N/mm", "kN/m", "kgf/m"],
    "F3": ["mi/hr", "km/hr", "m/sec"],
    "F4": ["kip-ft", "kip-in", "lbf-ft", "lbf-in", "N-m", "kN-m", "kgf-m"],
    "F5": ["in2", "ft2", "m2", "cm2", "mm2"],
    "F6": ["in3", "ft3", "m3", "cm3", "mm3"],
    "F7": ["in4", "ft4", "m4", "cm4", "mm4"]
}

for g, units in groups.items():
    for u in units:
        if f"{g}_{u}" not in st.session_state: st.session_state[f"{g}_{u}"] = 0.0

# =================================================================
# 3. INTERFAZ GRÁFICA (GRID 3 COLUMNAS)
# =================================================================
c1, c2, c3 = st.columns(3)

with c1:
    with st.container():
        st.markdown('<div class="unit-title">🟦 F1: Presión</div>', unsafe_allow_html=True)
        for u in groups["F1"]:
            st.number_input(u, key=f"F1_{u}", on_change=update_units, args=("F1", u, None), format="%.6f")
    
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="unit-title">📏 F2: Cargas Distribuidas</div>', unsafe_allow_html=True)
        for u in groups["F2"]:
            st.number_input(u, key=f"F2_{u}", on_change=update_units, args=("F2", u, None), format="%.6f")

with c2:
    with st.container():
        st.markdown('<div class="unit-title">🚀 F3: Velocidad</div>', unsafe_allow_html=True)
        for u in groups["F3"]:
            st.number_input(u, key=f"F3_{u}", on_change=update_units, args=("F3", u, None), format="%.4f")
    
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="unit-title">🔄 F4: Momento Flector</div>', unsafe_allow_html=True)
        for u in groups["F4"]:
            st.number_input(u, key=f"F4_{u}", on_change=update_units, args=("F4", u, None), format="%.4f")

    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="unit-title">🧱 F6: Módulo Sección</div>', unsafe_allow_html=True)
        for u in groups["F6"]:
            st.number_input(u, key=f"F6_{u}", on_change=update_units, args=("F6", u, None), format="%.6f")

with c3:
    with st.container():
        st.markdown('<div class="unit-title">📐 F5: Área</div>', unsafe_allow_html=True)
        for u in groups["F5"]:
            st.number_input(u, key=f"F5_{u}", on_change=update_units, args=("F5", u, None), format="%.6f")
    
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="unit-title">📉 F7: Inercia</div>', unsafe_allow_html=True)
        for u in groups["F7"]:
            st.number_input(u, key=f"F7_{u}", on_change=update_units, args=("F7", u, None), format="%.6f")

st.markdown("---")
st.info("💡 **Tip:** Cambia cualquier valor para ver la conversión instantánea en el resto de unidades del grupo.")