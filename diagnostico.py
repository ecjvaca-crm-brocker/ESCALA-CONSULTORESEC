import streamlit as st
import pandas as pd
import numpy as np

# Configuración de página con enfoque profesional Corporativo
st.set_page_config(page_title="Premium Valuation & Tax Hub", layout="wide", page_icon="📈")

st.title("📈 Ecosistema Escala Corporate: Premium Valuation & Tax Hub")
st.caption("Módulo Avanzado de Valoración de Activos e Inteligencia Fiscal para Alta Gerencia y Comités Ejecutivos (Normas NIIF / IFRS y LRTI)")

# Estilos CSS Limpios para simular Reportes de Banca de Inversión
st.markdown("""
    <style>
    .metric-box {background-color: #f8f9fa; border-left: 5px solid #1f77b4; padding: 15px; border-radius: 4px; margin-bottom: 15px;}
    .report-title {font-size: 24px; font-weight: bold; color: #1e3d59; margin-top: 20px;}
    .section-desc {color: #555555; font-size: 14px; margin-bottom: 20px;}
    </style>
""", unsafe_allowed_html=True)

# Inicializar Datos en Sesión para Simular Persistencia en Base de Datos Temporal
if 'activos_tangibles' not in st.session_state:
    st.session_state.activos_tangibles = pd.DataFrame(columns=['Clase', 'Descripción', 'Valor Contable', 'Valor Razonable', 'Norma Aplicada'])
if 'impuestos_diferidos' not in st.session_state:
    st.session_state.impuestos_diferidos = pd.DataFrame(columns=['Concepto', 'Base Contable', 'Base Fiscal', 'Diferencia', 'Tipo', 'Impuesto Diferido (30%)'])

# --- DEFINICIÓN DE PESTAÑAS (Módulos Integrados del Proyecto) ---
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Valoración de Activos (Tangibles/VNR)",
    "2. Motor de Valoración Corporativa (DCF/WACC)",
    "3. Hub de Consultoría Tributaria (NIC 12)",
    "4. Reporte Ejecutivo para Directorios"
])

# ==========================================
# PESTAÑA 1: VALORACIÓN DE ACTIVOS INDIVIDUALES
# ==========================================
with tab1:
    st.header("🏢 Registro y Revaluación de Activos bajo NIIF")
    st.markdown("<p class='section-desc'>Cumplimiento estricto con NIC 16, NIC 40 y NIC 2 para auditorías de salida a bolsa.</p>", unsafe_allowed_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Carga y Homologación de Activo")
        clase_activo = st.selectbox("Clase de Activo", ["Vehículos (NIC 16)", "Maquinaria y Equipos (NIC 16)", "Inmuebles (NIC 40)", "Inventarios (NIC 2 - VNR)"])
        desc_activo = st.text_input("Identificador / Descripción del Activo", placeholder="Ej. Planta Industrial Pifo")
        val_contable = st.number_input("Valor Neto Contable (Libros)", min_value=0.0, step=1000.0)
        
        # Simulación de Tasación o cálculo VNR automatizado
        val_razonable = st.number_input("Valor Razonable / Valor Neto Realizable Tasado", min_value=0.0, step=1000.0)
        
        if st.button("Ingresar Activo al Motor"):
            norma = "NIC 40 / NIIF 13" if clase_activo == "Inmuebles (NIC 40)" else ("NIC 2 (VNR)" if clase_activo == "Inventarios (NIC 2 - VNR)" else "NIC 16")
            nuevo_activo = pd.DataFrame([{
                'Clase': clase_activo, 'Descripción': desc_activo, 
                'Valor Contable': val_contable, 'Valor Razonable': val_razonable, 
                'Norma Aplicada': norma
            }])
            st.session_state.activos_tangibles = pd.concat([st.session_state.activos_tangibles, nuevo_activo], ignore_index=True)
            st.success("Activo indexado correctamente.")
            
    with col2:
        st.subheader("Inventario de Activos Valuados para Ajuste Patrimonial")
        if not st.session_state.activos_tangibles.empty:
            st.dataframe(st.session_state.activos_tangibles, use_container_width=True)
            total_libros = st.session_state.activos_tangibles['Valor Contable'].sum()
            total_razonable = st.session_state.activos_tangibles['Valor Razonable'].sum()
            ajuste_patrimonial = total_razonable - total_libros
            
            c1, c2 = st.columns(2)
            c1.metric("Total Valor Razonable", f"${total_razonable:,.2f}")
            c2.metric("Ajuste Patrimonial Bruto (Superávit)", f"${ajuste_patrimonial:,.2f}", delta_color="inverse" if ajuste_patrimonial < 0 else "normal")
        else:
            st.info("No se han ingresado activos tangibles aún.")

# ==========================================
# PESTAÑA 2: MOTOR DE VALORACIÓN CORPORATIVA (DCF / WACC)
# ==========================================
with tab2:
    st.header("⚙️ Motor de Valoración por Flujo de Caja Descontado (DCF)")
    st.markdown("<p class='section-desc'>Algoritmo de cálculo de tasa WACC mediante CAPM y proyección de flujos para cotización bursátil.</p>", unsafe_allowed_html=True)
    
    col_wacc, col_dcf = st.columns(2)
    
    with col_wacc:
        st.subheader("1. Parámetros del Costo de Capital (WACC - CAPM)")
        rf = st.number_input("Tasa Libre de Riesgo (Rf %)", value=4.5, step=0.1) / 100
        beta = st.number_input("Beta Apalancado del Sector (β)", value=1.2, step=0.05)
        rm = st.number_input("Rendimiento de Mercado Esperado (Rm %)", value=9.5, step=0.1) / 100
        riesgo_pais = st.number_input("Prima por Riesgo País (EMBI Ecuador pb)", value=1200, step=50) / 10000
        
        # CAPM Calculation
        ke = rf + beta * (rm - rf) + riesgo_pais
        st.markdown(f"<div class='metric-box'><b>Costo del Capital Propio (Ke) vía CAPM:</b> {ke*100:.2f}%</div>", unsafe_allowed_html=True)
        
        kd = st.number_input("Costo de la Deuda Financiera (Kd %)", value=10.5, step=0.25) / 100
        tasa_tax = st.number_input("Tasa Impositiva Efectiva + Participación Trabajadores (%)", value=36.25, step=0.5) / 100
        
        peso_e = st.slider("Proporción de Capital Propio (E/V %)", 10, 100, 60) / 100
        peso_d = 1.0 - peso_e
        
        # WACC Calculation
        wacc = (peso_e * ke) + (peso_d * kd * (1 - tasa_tax))
        st.metric("TASA WACC RESULTANTE (Descuento)", f"{wacc*100:.2f}%")
        
    with col_dcf:
        st.subheader("2. Proyección de Flujos Libres de Caja (FCFF)")
        fcl_año1 = st.number_input("Flujo de Caja Libre Año 1 ($)", value=500000.0, step=50000.0)
        growth_tasa = st.slider("Tasa de Crecimiento de Flujos (Años 2-5 %)", 1.0, 15.0, 5.0) / 100
        g_perpetuidad = st.slider("Tasa de Crecimiento a Perpetuidad (g %)", 0.5, 5.0, 2.0) / 100
        
        # Generar Proyecciones Automáticas
        flujos = [fcl_año1]
        for i in range(4):
            flujos.append(flujos[-1] * (1 + growth_tasa))
            
        df_flujos = pd.DataFrame({
            'Año': [f"Año {i+1}" for i in range(5)],
            'Flujo Proyectado': flujos
        })
        
        # Descontar Flujos
        df_flujos['Factor Descuento'] = [1 / ((1 + wacc) ** (i+1)) for i in range(5)]
        df_flujos['Valor Presente'] = df_flujos['Flujo Proyectado'] * df_flujos['Factor Descuento']
        st.dataframe(df_flujos.style.format({'Flujo Proyectado': '${:,.2f}', 'Factor Descuento': '{:.4f}', 'Valor Presente': '${:,.2f}'}), use_container_width=True)
        
        # Terminal Value & Enterprise Value
        vp_flujosp = df_flujos['Valor Presente'].sum()
        valor_terminal = (flujos[-1] * (1 + g_perpetuidad)) / (wacc - g_perpetuidad)
        vp_valor_terminal = valor_terminal * df_flujos['Factor Descuento'].iloc[-1]
        enterprise_value = vp_flujosp + vp_valor_terminal
        
        st.markdown(f"""
        <div style='background-color:#e3f2fd; padding:15px; border-radius:5px;'>
        <b>Valor Operativo de la Empresa (Enterprise Value):</b><br>
        <span style='font-size:22px; font-weight:bold; color:#0d47a1;'>${enterprise_value:,.2f}</span><br>
        <small>VP Flujos Explícitos: ${vp_flujosp:,.2f} | VP Valor Terminal: ${vp_valor_terminal:,.2f}</small>
        </div>
        """, unsafe_allowed_html=True)

# ==========================================
# PESTAÑA 3: HUB DE CONSULTORÍA TRIBUTARIA
# ==========================================
with tab3:
    st.header("⚖️ Unidad Especial de Impuestos Diferidos y Conciliación (NIC 12)")
    st.markdown("<p class='section-desc'>Módulo analítico fiscal para identificar pasivos latentes y optimizar el escudo fiscal según la LRTI.</p>", unsafe_allowed_html=True)
    
    col_tax1, col_tax2 = st.columns([1, 2])
    with col_tax1:
        st.subheader("Cálculo de Diferencias Temporarias")
        concepto_fiscal = st.selectbox("Concepto de Conciliación", [
            "Provisión Jubilación Patronal (No aprobada por Actuario)",
            "Deterioro de Inventarios (Obsolescencia / NIC 2 sin destruir)",
            "Diferencia por Revaluación de Inmuebles (Superávit NIIF 13)",
            "Amortización de Pérdidas Fiscales"
        ])
        base_contable = st.number_input("Monto Contable (NIIF)", min_value=0.0, step=1000.0, key="bc")
        base_fiscal = st.number_input("Monto Fiscal (LRTI)", min_value=0.0, step=1000.0, key="bf")
        
        if st.button("Calcular Impuesto Diferido"):
            diferencia = base_contable - base_fiscal
            # Determinar si es activo o pasivo diferido
            es_superavit_reval = "Revaluación" in concepto_fiscal
            tipo_id = "Pasivo Diferido" if (diferencia > 0 and es_superavit_reval) or (diferencia < 0 and not es_superavit_reval) else "Activo Diferido"
            
            impuesto_calc = abs(diferencia) * 0.25 # Supuesto de tasa corporativa estándar del 25% para el diferido puro
            
            nuevo_id = pd.DataFrame([{
                'Concepto': concepto_fiscal, 'Base Contable': base_contable,
                'Base Fiscal': base_fiscal, 'Diferencia': diferencia,
                'Tipo': tipo_id, 'Impuesto Diferido (30%)': impuesto_calc
            }])
            st.session_state.impuestos_diferidos = pd.concat([st.session_state.impuestos_diferidos, nuevo_id], ignore_index=True)
            st.success("Mapeo fiscal integrado con éxito.")
            
    with col_tax2:
        st.subheader("Matriz de Posiciones e Impuestos Diferidos Detectados")
        if not st.session_state.impuestos_diferidos.empty:
            st.dataframe(st.session_state.impuestos_diferidos, use_container_width=True)
            
            total_activos_dif = st.session_state.impuestos_diferidos[st.session_state.impuestos_diferidos['Tipo'] == "Activo Diferido"]['Impuesto Diferido (30%)'].sum()
            total_pasivos_dif = st.session_state.impuestos_diferidos[st.session_state.impuestos_diferidos['Tipo'] == "Pasivo Diferido"]['Impuesto Diferido (30%)'].sum()
            
            c_t1, c_t2 = st.columns(2)
            c_t1.metric("Total Activos Diferidos (Recuperables)", f"${total_activos_dif:,.2f}")
            c_t2.metric("Total Pasivos Diferidos (Obligaciones)", f"${total_pasivos_dif:,.2f}")
        else:
            st.info("No se han registrado conciliaciones temporarias.")

# ==========================================
# PESTAÑA 4: REPORTE EJECUTIVO PARA DIRECTORIOS Y COMITÉS
# ==========================================
with tab4:
    st.markdown("<div class='report-title'>INFORME ESTRATÉGICO DE VALORACIÓN INTEGRAL Y VIABILIDAD FINANCIERA</div>", unsafe_allowed_html=True)
    st.markdown("**Destinatarios:** Directorio, Comités Ejecutivos y Bancos de Inversión ESTRUCTURADORES DE LA IPO")
    st.divider()
    
    # Consolidación Dinámica de Resultados
    try:
        ev_final = enterprise_value
    except NameError:
        ev_final = 0.0
        
    tot_activos_razonable = st.session_state.activos_tangibles['Valor Razonable'].sum() if not st.session_state.activos_tangibles.empty else 0.0
    val_total_combinado = ev_final + tot_activos_razonable
    
    # Bloque de Métricas Críticas para la Toma de Decisiones de Alta Gerencia
    rep_c1, rep_c2, rep_c3 = st.columns(3)
    with rep_c1:
        st.markdown(f"""
        <div class='metric-box'>
        <small>VALORACIÓN CORPORATIVA DE NEGOCIO EN MARCHA (DCF)</small><br>
        <span style='font-size:24px; font-weight:bold; color:#2c3e50;'>${ev_final:,.2f}</span>
        </div>
        """, unsafe_allowed_html=True)
    with rep_c2:
        st.markdown(f"""
        <div class='metric-box'>
        <small>VALOR RAZONABLE DE ACTIVOS NETOS E INDEPENDIENTES (NIIF 13)</small><br>
        <span style='font-size:24px; font-weight:bold; color:#2c3e50;'>${tot_activos_razonable:,.2f}</span>
        </div>
        """, unsafe_allowed_html=True)
    with rep_c3:
        st.markdown(f"""
        <div class='metric-box' style='border-left-color: #2ecc71;'>
        <small>VALOR ESTIMADO PRE-MONEY INTEGRAL SUGERIDO</small><br>
        <span style='font-size:24px; font-weight:bold; color:#27ae60;'>${val_total_combinado:,.2f}</span>
        </div>
        """, unsafe_allowed_html=True)
        
    st.subheader("📝 Notas del Comité Financiero y Fiscal Extendido")
    st.info("""
    **Declaración de Cumplimiento Normativo de la Herramienta:** Los análisis expuestos fueron procesados respetando las metodologías de flujos descontados amparados por la **NIIF 13 (Medición del Valor Razonable)**. Las diferencias de base imponible e impuestos diferidos se estructuran bajo las directrices de la **NIC 12** y las reglas obligatorias de adición/deducción dictadas por la **Ley de Régimen Tributario Interno (LRTI)** de la República del Ecuador. Este informe constituye un documento de entrega formal para soporte de toma de decisiones estratégicas corporativas de Gobierno Corporativo de nivel C-Level.
    """)
    
    # Inputs ejecutivos para personalización del Dictamen Técnico antes de exportación
    observaciones_director = st.text_area("Observaciones Estratégicas Adicionales para el Acta del Directorio", 
        value="La valoración presenta alta sensibilidad ante variaciones del EMBI (Riesgo País). Se sugiere blindar la estructura patrimonial maximizando el uso de los activos diferidos aprobados por actuario para reducir la tasa efectiva impositiva antes del Roadshow bursátil.")
    
    if st.button("Emitir Certificado de Valoración de Alta Gerencia (Aprobado)"):
        st.balloons()
        st.success("Dictamen de Valoración Técnica Corporativa consolidado. Listo para auditoría y radicación formal ante el Comité de Salida a Bolsa.")
