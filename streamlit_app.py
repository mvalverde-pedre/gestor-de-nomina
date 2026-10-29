import streamlit as st
import pandas as pd

# Configuración de página ancha
st.set_page_config(page_title="Control de Nómina", layout="wide", page_icon="📊")

# Estilos visuales personalizados
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .stRadio > label {
            font-size: 18px !important;
            font-weight: bold !important;
            color: #d51218;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ZONA SUPERIOR: TÍTULO Y CARGA DE EXCEL (ARRIBA DERECHA)
# ---------------------------------------------------------
col_titulo, col_carga = st.columns([2, 1])

with col_titulo:
    st.title("💼 Consultor de Nómina")
    st.caption("🍇 Campaña 2026 | Desde el 21 de Septiembre")

with col_carga:
    st.markdown("### 📥 Cargar Planilla")
    archivo_excel = st.file_uploader("Sube el archivo (.xlsx)", type=["xlsx"], label_visibility="collapsed")

st.divider()

# ---------------------------------------------------------
# ESTRUCTURA PRINCIPAL: MENÚ IZQUIERDO Y CONTENIDO
# ---------------------------------------------------------
col_menu, col_contenido = st.columns([1, 3])

with col_menu:
    st.markdown("### 🗓️ Periodo")
    opciones_semana = [
        "Toda la Campaña (Acumulado)",
        "Semana 39 (21 Sep - 27 Sep)",
        "Semana 40 (28 Sep - 04 Oct)",
        "Semana 41 (05 Oct - 11 Oct)",
        "Semana 42 (12 Oct - 18 Oct)",
        "Semana 43 (19 Oct - 25 Oct)",
        "Semana 44 (26 Oct - Actualidad)"
    ]
    semana_sel = st.selectbox("Seleccionar Semana:", opciones_semana, label_visibility="collapsed")

    st.write("")
    st.markdown("### 📋 Consultas")
    # Menú vertical (De arriba a abajo)
    opcion_menu = st.radio(
        "Navegación:",
        [
            "👤 1. Neto por Trabajador",
            "📊 2. Consolidado por Conceptos",
            "📈 3. Evolución Histórica",
            "🚨 4. Alertas y Control de Costos"
        ]
    )

# ---------------------------------------------------------
# LÓGICA DE VISUALIZACIÓN EN LA ZONA DE CONTENIDO
# ---------------------------------------------------------
with col_contenido:
    if archivo_excel is not None:
        try:
            df_raw = pd.read_excel(archivo_excel, header=None)
            encabezados = [str(col).strip() for col in df_raw.iloc[0].tolist()]
            df = df_raw.iloc[1:].copy()
            df.columns = encabezados

            if "1. Neto por Trabajador" in opcion_menu:
                st.subheader(f"📌 Resumen de Pagos Netos — {semana_sel}")
                
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    busqueda = st.text_input("🔍 Buscar por Nombre o DNI:")
                
                col_banco_nombre = next((c for c in df.columns if "BANCO" in str(c).upper()), None)
                with col_b2:
                    if col_banco_nombre:
                        banco_filtro = st.multiselect("🏦 Filtrar por Banco:", df[col_banco_nombre].dropna().unique())
                    else:
                        st.caption("ℹ️ Columna de Banco no detectada.")

                st.dataframe(df, use_container_width=True)

            elif "2. Consolidado por Conceptos" in opcion_menu:
                st.subheader(f"📊 Desglose por Conceptos (Ingresos vs. Descuentos) — {semana_sel}")
                st.info("Vista para consolidar los Bloques 2 (Ingresos) y Bloques 3 (Descuentos).")

            elif "3. Evolución Histórica" in opcion_menu:
                st.subheader("📈 Evolución Semanal de la Planilla")
                st.info("Gráfico acumulado del gasto salarial desde el 21 de Septiembre.")

            elif "4. Alertas y Control de Costos" in opcion_menu:
                st.subheader(f"🚨 Alertas de Costos y Top Horas Extras — {semana_sel}")
                st.info("Ranking de mayor volumen de ingresos adicionales o descuentos de la semana.")

        except Exception as e:
            st.error(f"❌ Error al procesar el archivo Excel: {e}")
    else:
        st.info("☝ Por favor, sube la planilla semanal en la esquina superior derecha para comenzar.")
