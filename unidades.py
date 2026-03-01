# -*- coding: utf-8 -*-
import streamlit as st

# =================================================================
# 1. CONFIGURACIÓN Y ESTILO CORPORATIVO
# =================================================================
st.set_page_config(page_title="Conversor de Unidades | Mauricio Riquelme", layout="wide")

st.markdown("""
    <style>
    .unit-title {
        color: #003366; font-weight: bold; border-bottom: 2px solid #003366;
        margin-bottom: 10px; padding-top: 10px; font-size: 1.2rem;
    }
    /* Estilo para que los inputs se vean más técnicos */
    .stNumberInput input { color: #003366 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ Conversor de Unidades de Ingeniería")
st.caption("Proyectos Estructurales | Sincronización Simultánea")

# =================================================================
# 2. MOTOR DE CONVERSIÓN SIMULTÁNEA
# =================================================================

def sync_units(group, unit_key):
    """Lógica de actualización instantánea basada en el cambio de un solo input"""
    val = st.session_state[f"{group}_{unit_key}"]
    
    # F1: PRESIÓN (Referencia base: psf)
    if group == "F1":
        factors = {"psf": 1.0, "psi": 0.006944, "kgf/m2": 4.882428, "kPa": 0.04788, "MPa": 0.000048}
        base = val / factors[unit_key]
        for u, f in factors.items():
            if u != unit_key: st.session_state[f"F1_{u}"] = base * f

    # F2: CARGAS DISTRIBUIDAS (Referencia base: lbf/ft)
    elif group == "F2":
        factors = {"lbf/ft": 1.0, "lbf/in": 0.083333, "N/mm": 0.014594, "kN/m": 0.014594, "kgf/m": 1.488164}
        base = val / factors[unit_key]
        for u, f in factors.items():
            if u != unit_key: st.session_state[f"F2_{u}"] = base * f

    # F7: INERCIA (Referencia base: in4)
    elif group == "F7":
        factors = {"in4": 1.0, "ft4": 0.0000482, "m4": 0.000000416, "cm4": 41.6231, "mm4": 416231.42}
        base = val / factors[unit_key]
        for u, f in factors.items():
            if u != unit_key: st.session_state[f"F7_{u}"] = base * f

# Inicializar estados si no existen
if "F1_psf" not in st.session_state:
    init_vals = {"F1_psf": 1.0, "F1_psi": 0.006944, "F1_kgf/m2": 4.882428, "F1_kPa": 0.04788, "F1_MPa": 0.000048,
                 "F2_lbf/ft": 1.0, "F2_lbf/in": 0.083, "F2_N/mm": 0.014, "F2_kN/m": 0.014, "F2_kgf/m": 1.488,
                 "F7_in4": 1.0, "F7_ft4": 0.000048, "F7_m4": 0.0, "F7_cm4": 41.623, "F7_mm4": 416231.4}
    for k, v in init_vals.items(): st.session_state[k] = v

# =================================================================
# 3. INTERFAZ EN COLUMNAS (MUESTRA DE FUNCIONALIDAD)
# =================================================================
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<div class="unit-title">🟦 F1: Presión</div>', unsafe_allow_html=True)
    st.number_input("psf (libras/pie²)", key="F1_psf", format="%.4f", on_change=sync_units, args=("F1", "psf"))
    st.number_input("psi (libras/pulg²)", key="F1_psi", format="%.6f", on_change=sync_units, args=("F1", "psi"))
    st.number_input("kgf/m²", key="F1_kgf/m2", format="%.4f", on_change=sync_units, args=("F1", "kgf/m2"))
    st.number_input("kPa", key="F1_kPa", format="%.4f", on_change=sync_units, args=("F1", "kPa"))
    st.number_input("MPa", key="F1_MPa", format="%.6f", on_change=sync_units, args=("F1", "MPa"))

with c2:
    st.markdown('<div class="unit-title">📏 F2: Cargas Distr.</div>', unsafe_allow_html=True)
    st.number_input("lbf/ft", key="F2_lbf/ft", format="%.4f", on_change=sync_units, args=("F2", "lbf/ft"))
    st.number_input("lbf/in", key="F2_lbf/in", format="%.4f", on_change=sync_units, args=("F2", "lbf/in"))
    st.number_input("kN/m", key="F2_kN/m", format="%.4f", on_change=sync_units, args=("F2", "kN/m"))
    st.number_input("kgf/m", key="F2_kgf/m", format="%.4f", on_change=sync_units, args=("F2", "kgf/m"))

with c3:
    st.markdown('<div class="unit-title">📉 F7: Inercia</div>', unsafe_allow_html=True)
    st.number_input("in⁴", key="F7_in4", format="%.4f", on_change=sync_units, args=("F7", "in4"))
    st.number_input("cm⁴", key="F7_cm4", format="%.4f", on_change=sync_units, args=("F7", "cm4"))
    st.number_input("mm⁴", key="F7_mm4", format="%.2f", on_change=sync_units, args=("F7", "mm4"))

st.divider()
st.info("✅ **Sincronización activa**: Cualquier cambio en una unidad actualiza el resto del grupo automáticamente.")