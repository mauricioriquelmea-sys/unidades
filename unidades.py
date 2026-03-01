# -*- coding: utf-8 -*-
import streamlit as st

# =================================================================
# 1. CONFIGURACIÓN Y ESTILO CORPORATIVO
# =================================================================
st.set_page_config(page_title="Conversor Proyectos Estructurales", layout="wide")

st.markdown("""
    <style>
    .unit-title {
        color: #003366; font-weight: bold; border-bottom: 2px solid #003366;
        margin-bottom: 10px; padding-top: 15px; font-size: 1.1rem;
    }
    .stNumberInput label { font-size: 0.9rem !important; color: #555; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ Conversor de Unidades | Structural Lab")
st.caption("Factores de Conversión de Alta Precisión - Mauricio Riquelme")

# =================================================================
# 2. MOTOR DE SINCRONIZACIÓN TOTAL (F1 A F7)
# =================================================================

# Diccionario Maestro de Factores (Relacionados a la unidad base de cada grupo)
CONV_DATA = {
    "F1": {"base": "psf", "factors": {"psf": 1.0, "psi": 0.006944, "kgf/m2": 4.882428, "kPa": 0.04788, "MPa": 0.000048}},
    "F2": {"base": "lbf/ft", "factors": {"lbf/ft": 1.0, "lbf/in": 0.083333, "N/mm": 0.014594, "kN/m": 0.014594, "kgf/m": 1.488164}},
    "F3": {"base": "mi/hr", "factors": {"mi/hr": 1.0, "km/hr": 1.609344, "m/sec": 0.44704}},
    "F4": {"base": "kip-ft", "factors": {"kip-ft": 1.0, "kip-in": 12.0, "lbf-ft": 1000.0, "lbf-in": 12000.0, "N-m": 1355.8179, "kN-m": 1.3558, "kgf-m": 138.255}},
    "F5": {"base": "in2", "factors": {"in2": 1.0, "ft2": 0.006944, "m2": 0.000645, "cm2": 6.4516, "mm2": 645.16}},
    "F6": {"base": "in3", "factors": {"in3": 1.0, "ft3": 0.0005787, "m3": 0.00001639, "cm3": 16.387, "mm3": 16387.064}},
    "F7": {"base": "in4", "factors": {"in4": 1.0, "ft4": 0.0000482, "m4": 0.000000416, "cm4": 41.6231, "mm4": 416231.42}}
}

def sync(group_id, unit_id):
    """Función de callback que sincroniza todas las unidades del bloque."""
    input_val = st.session_state[f"{group_id}_{unit_id}"]
    factors = CONV_DATA[group_id]["factors"]
    
    # Calcular valor base
    base_val = input_val / factors[unit_id]
    
    # Actualizar todos los demás del grupo
    for u, f in factors.items():
        if u != unit_id:
            st.session_state[f"{group_id}_{u}"] = base_val * f

# Inicialización silenciosa de Session State
for g_id, g_info in CONV_DATA.items():
    for u_id in g_info["factors"]:
        key = f"{g_id}_{u_id}"
        if key not in st.session_state:
            st.session_state[key] = 0.0

# =================================================================
# 3. INTERFAZ EN 3 COLUMNAS (FULL DASHBOARD)
# =================================================================
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<div class="unit-title">🟦 F1: Presión</div>', unsafe_allow_html=True)
    for u in CONV_DATA["F1"]["factors"]:
        st.number_input(u, key=f"F1_{u}", format="%.6f", on_change=sync, args=("F1", u))

    st.markdown('<div class="unit-title">📏 F2: Cargas Distribuidas</div>', unsafe_allow_html=True)
    for u in CONV_DATA["F2"]["factors"]:
        st.number_input(u, key=f"F2_{u}", format="%.6f", on_change=sync, args=("F2", u))

with c2:
    st.markdown('<div class="unit-title">🚀 F3: Velocidad</div>', unsafe_allow_html=True)
    for u in CONV_DATA["F3"]["factors"]:
        st.number_input(u, key=f"F3_{u}", format="%.4f", on_change=sync, args=("F3", u))

    st.markdown('<div class="unit-title">🔄 F4: Momento Flector</div>', unsafe_allow_html=True)
    for u in CONV_DATA["F4"]["factors"]:
        st.number_input(u, key=f"F4_{u}", format="%.4f", on_change=sync, args=("F4", u))

    st.markdown('<div class="unit-title">🧱 F6: Módulo Seccional</div>', unsafe_allow_html=True)
    for u in CONV_DATA["F6"]["factors"]:
        st.number_input(u, key=f"F6_{u}", format="%.6f", on_change=sync, args=("F6", u))

with c3:
    st.markdown('<div class="unit-title">📐 F5: Área</div>', unsafe_allow_html=True)
    for u in CONV_DATA["F5"]["factors"]:
        st.number_input(u, key=f"F5_{u}", format="%.6f", on_change=sync, args=("F5", u))

    st.markdown('<div class="unit-title">📉 F7: Inercia</div>', unsafe_allow_html=True)
    for u in CONV_DATA["F7"]["factors"]:
        st.number_input(u, key=f"F7_{u}", format="%.6f", on_change=sync, args=("F7", u))

st.divider()
st.info("✅ **Sincronización Inteligente Activada**: Los 7 módulos operan en tiempo real sin conflictos de bucle.")