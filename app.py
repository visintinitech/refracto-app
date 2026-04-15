"""
Refracto - Aplicación de análisis de estilo de escritura
Versión con historial y comparación de textos
"""

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import json
import os
from datetime import datetime
from refractor import refractar

# Configuración de la página
st.set_page_config(
    page_title="Refracto - Analiza tu estilo de escritura",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== GESTIÓN DE HISTORIAL ====================

HISTORIAL_FILE = "historial_refracto.json"

def cargar_historial():
    """Carga el historial desde archivo JSON"""
    if os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def guardar_historial(historial):
    """Guarda el historial en archivo JSON"""
    with open(HISTORIAL_FILE, 'w', encoding='utf-8') as f:
        json.dump(historial, f, indent=2, ensure_ascii=False)

def guardar_analisis(texto, resultado):
    """Guarda un análisis en el historial"""
    historial = cargar_historial()
    
    nuevo_analisis = {
        "id": len(historial) + 1,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "texto": texto[:200] + "..." if len(texto) > 200 else texto,
        "texto_completo": texto,
        "perfil": resultado["perfil"],
        "stats": resultado["stats"],
        "recomendacion": resultado["recomendacion"]
    }
    
    historial.insert(0, nuevo_analisis)  # Los más nuevos primero
    if len(historial) > 20:  # Mantener solo últimos 20
        historial = historial[:20]
    
    guardar_historial(historial)
    return nuevo_analisis

def eliminar_analisis(id_analisis):
    """Elimina un análisis del historial"""
    historial = cargar_historial()
    historial = [a for a in historial if a["id"] != id_analisis]
    guardar_historial(historial)

# ==================== FUNCIONES DE VISUALIZACIÓN ====================

def mostrar_grafico_barras(metrics, titulo="Espectro de estilo"):
    """Muestra gráfico de barras para un conjunto de métricas"""
    categories = ['Formalidad', 'Complejidad', 'Repetición', 'Riqueza\nléxica', 'Legibilidad']
    values = [
        metrics["formalidad"] * 10,
        metrics["complejidad"],
        metrics["repeticion"] * 10,
        metrics["riqueza_lexica"] * 10,
        metrics["legibilidad"] / 10
    ]
    
    fig, ax = plt.subplots(figsize=(10, 4))
    colors = ['#6B46C1', '#3182CE', '#DD6B20', '#10B981', '#F59E0B']
    bars = ax.barh(categories, values, color=colors, alpha=0.8)
    ax.set_xlim(0, 10)
    ax.set_xlabel('Puntuación (0-10)', color='#94A3B8')
    ax.set_facecolor('#1E293B')
    fig.patch.set_facecolor('#1E293B')
    ax.tick_params(colors='#F1F5F9')
    for spine in ax.spines.values():
        spine.set_color('#334155')
    
    # Añadir valores al final de cada barra
    for i, (bar, val) in enumerate(zip(bars, values)):
        ax.text(val + 0.2, bar.get_y() + bar.get_height()/2, 
                f'{val:.1f}', va='center', color='#F1F5F9', fontsize=10)
    
    st.pyplot(fig)

def mostrar_tarjetas_metricas(metrics, cols=5):
    """Muestra tarjetas con métricas individuales"""
    col1, col2, col3, col4, col5 = st.columns(cols)
    
    with col1:
        formalidad = metrics["formalidad"]
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#6B46C1">{formalidad}</div>
            <div class="metric-label">Formalidad</div>
            <div style="font-size:0.8rem;">{'Formal' if formalidad > 0.6 else 'Informal' if formalidad < 0.4 else 'Neutral'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        complejidad = metrics["complejidad"]
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#3182CE">{complejidad}</div>
            <div class="metric-label">Complejidad</div>
            <div style="font-size:0.8rem;">/10</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        repeticion = metrics["repeticion"]
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#DD6B20">{repeticion}</div>
            <div class="metric-label">Repetición</div>
            <div style="font-size:0.8rem;">{'Alta' if repeticion > 0.6 else 'Media' if repeticion > 0.3 else 'Baja'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        riqueza = metrics["riqueza_lexica"]
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#10B981">{riqueza}</div>
            <div class="metric-label">Riqueza léxica</div>
            <div style="font-size:0.8rem;">{'Alta' if riqueza > 0.6 else 'Media' if riqueza > 0.4 else 'Baja'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        legibilidad = metrics["legibilidad"]
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#F59E0B">{legibilidad}</div>
            <div class="metric-label">Legibilidad</div>
            <div style="font-size:0.8rem;">{'Fácil' if legibilidad > 60 else 'Normal' if legibilidad > 40 else 'Difícil'}</div>
        </div>
        """, unsafe_allow_html=True)

def mostrar_comparacion(metrics1, metrics2, nombre1="Texto 1", nombre2="Texto 2"):
    """Muestra comparación lado a lado de dos análisis"""
    
    st.markdown("### ⚔️ Comparación visual")
    
    # DataFrame para comparación
    comparacion_df = pd.DataFrame({
        'Métrica': ['Formalidad', 'Complejidad', 'Repetición', 'Riqueza léxica', 'Legibilidad'],
        nombre1: [
            metrics1["formalidad"],
            metrics1["complejidad"],
            metrics1["repeticion"],
            metrics1["riqueza_lexica"],
            metrics1["legibilidad"]
        ],
        nombre2: [
            metrics2["formalidad"],
            metrics2["complejidad"],
            metrics2["repeticion"],
            metrics2["riqueza_lexica"],
            metrics2["legibilidad"]
        ]
    })
    
    # Añadir columna de diferencia
    comparacion_df['Diferencia'] = comparacion_df[nombre2] - comparacion_df[nombre1]
    
    st.dataframe(
        comparacion_df.style.format({
            nombre1: '{:.2f}',
            nombre2: '{:.2f}',
            'Diferencia': '{:+.2f}'
        }).background_gradient(subset=['Diferencia'], cmap='RdYlGn', vmin=-2, vmax=2),
        use_container_width=True
    )
    
    # Gráfico de barras comparativo
    fig, ax = plt.subplots(figsize=(12, 5))
    
    categories = ['Formalidad', 'Complejidad', 'Repetición', 'Riqueza\nléxica', 'Legibilidad']
    values1 = [
        metrics1["formalidad"] * 10,
        metrics1["complejidad"],
        metrics1["repeticion"] * 10,
        metrics1["riqueza_lexica"] * 10,
        metrics1["legibilidad"] / 10
    ]
    values2 = [
        metrics2["formalidad"] * 10,
        metrics2["complejidad"],
        metrics2["repeticion"] * 10,
        metrics2["riqueza_lexica"] * 10,
        metrics2["legibilidad"] / 10
    ]
    
    x = range(len(categories))
    width = 0.35
    
    bars1 = ax.barh([i - width/2 for i in x], values1, width, label=nombre1, color='#6B46C1', alpha=0.8)
    bars2 = ax.barh([i + width/2 for i in x], values2, width, label=nombre2, color='#DD6B20', alpha=0.8)
    
    ax.set_yticks(x)
    ax.set_yticklabels(categories)
    ax.set_xlabel('Puntuación (0-10)', color='#94A3B8')
    ax.set_facecolor('#1E293B')
    fig.patch.set_facecolor('#1E293B')
    ax.tick_params(colors='#F1F5F9')
    for spine in ax.spines.values():
        spine.set_color('#334155')
    ax.legend(facecolor='#1E293B', labelcolor='#F1F5F9')
    
    st.pyplot(fig)

# ==================== CSS PERSONALIZADO ====================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 100%);
    }
    
    h1 {
        background: linear-gradient(135deg, #6B46C1, #3182CE, #DD6B20);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        text-align: center;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #6B46C1, #3182CE, #DD6B20);
        color: white;
        border: none;
        border-radius: 40px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(107, 70, 193, 0.4);
    }
    
    .metric-card {
        background: #1E293B;
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #334155;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .metric-label {
        color: #94A3B8;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    .stTextArea textarea {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        color: #F1F5F9;
        font-size: 1rem;
    }
    
    .stTextArea textarea:focus {
        border-color: #6B46C1;
        box-shadow: 0 0 0 2px rgba(107, 70, 193, 0.2);
    }
    
    .recommendation-box {
        background: linear-gradient(135deg, rgba(107, 70, 193, 0.1), rgba(49, 130, 206, 0.1));
        border-left: 4px solid #DD6B20;
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
    }
    
    .sidebar .sidebar-content {
        background: #0F172A;
    }
    
    .footer {
        text-align: center;
        color: #64748B;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding: 1rem;
    }
    
    .history-card {
        background: #1E293B;
        border-radius: 12px;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        border: 1px solid #334155;
        cursor: pointer;
    }
    
    .history-card:hover {
        border-color: #6B46C1;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR - HISTORIAL ====================

with st.sidebar:
    st.markdown("## 📚 Historial")
    st.markdown("---")
    
    historial = cargar_historial()
    
    if historial:
        for analisis in historial[:10]:
            col_hist1, col_hist2 = st.columns([4, 1])
            with col_hist1:
                st.markdown(f"""
                <div class="history-card">
                    <small style="color:#94A3B8">{analisis['fecha']}</small><br>
                    <span style="font-size:0.85rem;">"{analisis['texto'][:50]}..."</span>
                </div>
                """, unsafe_allow_html=True)
            with col_hist2:
                if st.button("🗑️", key=f"del_{analisis['id']}"):
                    eliminar_analisis(analisis['id'])
                    st.rerun()
            
            if st.button(f"📖 Ver #{analisis['id']}", key=f"view_{analisis['id']}"):
                st.session_state['ver_historial'] = analisis
    else:
        st.info("💡 Aún no hay análisis guardados. Escribe algo y haz clic en REFRACTAR.")
    
    st.markdown("---")
    if st.button("🗑️ Limpiar todo el historial"):
        guardar_historial([])
        st.rerun()

# ==================== TABS PRINCIPALES ====================

tab1, tab2, tab3 = st.tabs(["🔮 Analizar texto", "⚔️ Comparar textos", "📚 Ver historial"])

# ==================== TAB 1: ANALIZAR TEXTO ====================

with tab1:
    st.markdown("""
    <div style="text-align: center;">
        <h1>🔮 REFRACTO</h1>
        <p style="color: #94A3B8; font-size: 1.2rem; margin-top: -0.5rem;">
            Tu escritura en descomposición
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Tu texto")
        texto_usuario = st.text_area(
            "Pega o escribe tu texto aquí:",
            height=250,
            placeholder="Ejemplo:\n\nHoy fue un día increíble. Aprendí muchas cosas nuevas y conocí personas interesantes. Definitivamente, repetiré la experiencia.",
            label_visibility="collapsed",
            key="texto_analisis"
        )
        
        boton_analizar = st.button("🌈 REFRACTAR", use_container_width=True)
    
    with col2:
        st.markdown("### 💡 ¿Cómo funciona?")
        st.markdown("""
        Refracto descompone tu texto en **5 dimensiones**:
        
        - **Formalidad** (¿informal o profesional?)
        - **Complejidad** (¿simple o elaborado?)
        - **Repetición** (¿variado o redundante?)
        - **Riqueza léxica** (¿vocabulario amplio?)
        - **Legibilidad** (¿fácil de leer?)
        
        > Cuanto más texto, más preciso el análisis.
        """)
    
    if boton_analizar:
        if not texto_usuario or len(texto_usuario.strip()) < 20:
            st.warning("⚠️ Escribe al menos 20 caracteres para un análisis significativo.")
        else:
            with st.spinner("🔮 Refractando tu estilo..."):
                resultado = refractar(texto_usuario)
            
            if "error" in resultado:
                st.error(resultado["error"])
            else:
                # Guardar en historial automáticamente
                guardar_analisis(texto_usuario, resultado)
                st.success("✅ Análisis guardado en el historial")
                
                # Mostrar estadísticas básicas
                stats = resultado["stats"]
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("📝 Palabras", stats["palabras_total"])
                with col_b:
                    st.metric("📄 Oraciones", stats["oraciones_total"])
                with col_c:
                    st.metric("🔤 Caracteres", stats["caracteres_total"])
                
                st.markdown("---")
                
                # Gráfico
                st.markdown("### 📊 Espectro de estilo")
                mostrar_grafico_barras(resultado["perfil"])
                
                # Tarjetas
                st.markdown("### 🔬 Desglose detallado")
                mostrar_tarjetas_metricas(resultado["perfil"])
                
                # Tono
                st.markdown("### 🎭 Tono emocional")
                tono = resultado["perfil"]["tono"]
                emoji = "😊" if tono["categoria"] == "positivo" else "😠" if tono["categoria"] == "negativo" else "😐"
                st.info(f"{emoji} **{tono['categoria'].capitalize()}** | Polaridad: {tono['polaridad']} | Subjetividad: {tono['subjetividad']}")
                
                # Recomendación
                st.markdown("### 💡 Recomendación personalizada")
                st.markdown(f"""
                <div class="recommendation-box">
                    {resultado['recomendacion']}
                </div>
                """, unsafe_allow_html=True)
                
                # Detalles
                with st.expander("🔍 Ver detalles técnicos"):
                    detalles = resultado["detalles"]
                    st.markdown(f"""
                    - **Longitud media de oración:** {detalles['oracion_promedio_palabras']} palabras
                    - **Longitud media de palabra:** {detalles['palabra_promedio_caracteres']} caracteres
                    - **Uso de exclamaciones:** {detalles['uso_exclamaciones']} veces
                    - **Uso de preguntas:** {detalles['uso_preguntas']} veces
                    """)
                    
                    if detalles['palabras_repetidas_top']:
                        st.markdown("**Palabras más repetidas:**")
                        for palabra, count in detalles['palabras_repetidas_top']:
                            st.markdown(f"- '{palabra}': {count} veces")

# ==================== TAB 2: COMPARAR TEXTOS ====================

with tab2:
    st.markdown("## ⚔️ Comparador de estilos")
    st.markdown("Compara dos textos y descubre cómo cambia tu estilo.")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Texto A")
        texto_a = st.text_area(
            "Primer texto:",
            height=200,
            placeholder="Escribe o pega el primer texto aquí...",
            key="texto_a"
        )
        boton_comparar_a = st.button("📊 Analizar Texto A", key="btn_a")
        
        if boton_comparar_a and texto_a and len(texto_a.strip()) >= 20:
            with st.spinner("Analizando Texto A..."):
                resultado_a = refractar(texto_a)
                if "error" not in resultado_a:
                    st.session_state['resultado_a'] = resultado_a
                    st.session_state['texto_a'] = texto_a
                    st.success("✅ Texto A analizado")
    
    with col2:
        st.markdown("### 📝 Texto B")
        texto_b = st.text_area(
            "Segundo texto:",
            height=200,
            placeholder="Escribe o pega el segundo texto aquí...",
            key="texto_b"
        )
        boton_comparar_b = st.button("📊 Analizar Texto B", key="btn_b")
        
        if boton_comparar_b and texto_b and len(texto_b.strip()) >= 20:
            with st.spinner("Analizando Texto B..."):
                resultado_b = refractar(texto_b)
                if "error" not in resultado_b:
                    st.session_state['resultado_b'] = resultado_b
                    st.session_state['texto_b'] = texto_b
                    st.success("✅ Texto B analizado")
    
    st.markdown("---")
    
    # Mostrar comparación si ambos textos están analizados
    if 'resultado_a' in st.session_state and 'resultado_b' in st.session_state:
        st.markdown("### 🔬 Resultados de la comparación")
        
        # Mostrar vista previa de textos
        with st.expander("📄 Ver textos completos"):
            st.markdown(f"**Texto A:** {st.session_state['texto_a'][:500]}...")
            st.markdown(f"**Texto B:** {st.session_state['texto_b'][:500]}...")
        
        # Tabla comparativa
        mostrar_comparacion(
            st.session_state['resultado_a']["perfil"],
            st.session_state['resultado_b']["perfil"],
            "Texto A",
            "Texto B"
        )
        
        # Tarjetas lado a lado
        st.markdown("### 📊 Comparación por métrica")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Texto A")
            mostrar_tarjetas_metricas(st.session_state['resultado_a']["perfil"], cols=5)
            st.caption(f"📊 {st.session_state['resultado_a']['stats']['palabras_total']} palabras")
        
        with col2:
            st.markdown("#### Texto B")
            mostrar_tarjetas_metricas(st.session_state['resultado_b']["perfil"], cols=5)
            st.caption(f"📊 {st.session_state['resultado_b']['stats']['palabras_total']} palabras")
        
        # Recomendaciones combinadas
        st.markdown("### 💡 Conclusiones")
        st.markdown(f"""
        <div class="recommendation-box">
            <strong>🎯 Texto A:</strong> {st.session_state['resultado_a']['recomendacion']}<br><br>
            <strong>🎯 Texto B:</strong> {st.session_state['resultado_b']['recomendacion']}
        </div>
        """, unsafe_allow_html=True)
        
        # Botón para limpiar
        if st.button("🔄 Limpiar comparación"):
            del st.session_state['resultado_a']
            del st.session_state['resultado_b']
            del st.session_state['texto_a']
            del st.session_state['texto_b']
            st.rerun()
    else:
        st.info("💡 Analiza ambos textos (mínimo 20 caracteres cada uno) para ver la comparación.")

# ==================== TAB 3: VER HISTORIAL ====================

with tab3:
    st.markdown("## 📚 Tu historial de análisis")
    st.markdown("Todos tus análisis guardados. Haz clic en uno para ver los detalles.")
    st.markdown("---")
    
    historial = cargar_historial()
    
    if historial:
        for i, analisis in enumerate(historial):
            with st.expander(f"📌 #{analisis['id']} - {analisis['fecha']}"):
                st.markdown(f"**Texto analizado:**")
                st.markdown(f"> {analisis['texto']}")
                
                st.markdown("**Métricas principales:**")
                mostrar_tarjetas_metricas(analisis["perfil"], cols=5)
                
                st.markdown(f"**💡 Recomendación:** {analisis['recomendacion']}")
                
                if st.button(f"📊 Ver análisis completo #{analisis['id']}", key=f"full_{analisis['id']}"):
                    # Cargar el análisis completo en la pestaña 1
                    st.session_state['ver_historial'] = analisis
                    st.info("Ve a la pestaña 'Analizar texto' para ver el análisis completo")
    else:
        st.info("📭 No hay análisis guardados todavía. Escribe algo en la pestaña 'Analizar texto'.")

# ==================== MOSTRAR ANÁLISIS DEL HISTORIAL ====================

if 'ver_historial' in st.session_state:
    analisis = st.session_state['ver_historial']
    
    st.markdown("---")
    st.markdown(f"## 🔮 Análisis guardado #{analisis['id']}")
    st.markdown(f"*{analisis['fecha']}*")
    
    with st.expander("📄 Ver texto completo"):
        st.markdown(analisis['texto_completo'])
    
    mostrar_grafico_barras(analisis["perfil"])
    mostrar_tarjetas_metricas(analisis["perfil"])
    
    st.markdown(f"""
    <div class="recommendation-box">
        {analisis['recomendacion']}
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🗑️ Eliminar este análisis"):
        eliminar_analisis(analisis['id'])
        del st.session_state['ver_historial']
        st.rerun()

# ==================== FOOTER ====================

st.markdown("---")
st.markdown("""
<div class="footer">
    Refracto — Porque cada palabra dobla la luz de quien la escribe<br>
    <span style="font-size: 0.7rem;">✨ Proyecto de práctica — Analiza, compara, mejora ✨</span>
</div>
""", unsafe_allow_html=True)