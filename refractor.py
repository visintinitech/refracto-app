"""
Refracto - Aplicación de análisis de estilo de escritura
Interfaz principal con Streamlit
"""

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from refractor import refractar

# Configuración de la página
st.set_page_config(
    page_title="Refracto - Analiza tu estilo de escritura",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Paleta de colores Refracto (CSS personalizado)
st.markdown("""
<style>
    /* Importar fuente */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Fondo principal */
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 100%);
    }
    
    /* Título principal */
    h1 {
        background: linear-gradient(135deg, #6B46C1, #3182CE, #DD6B20);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        text-align: center;
    }
    
    /* Tarjetas */
    .css-1r6slb0, .css-1v0mbdj, .stCard {
        background: #1E293B;
        border-radius: 16px;
        border: 1px solid #334155;
        padding: 1.5rem;
    }
    
    /* Botón principal */
    .stButton > button {
        background: linear-gradient(135deg, #6B46C1, #3182CE, #DD6B20);
        color: white;
        border: none;
        border-radius: 40px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(107, 70, 193, 0.4);
    }
    
    /* Métricas */
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
    
    /* Área de texto */
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
    
    /* Recomendación */
    .recommendation-box {
        background: linear-gradient(135deg, rgba(107, 70, 193, 0.1), rgba(49, 130, 206, 0.1));
        border-left: 4px solid #DD6B20;
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #64748B;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Título y descripción
st.markdown("""
<div style="text-align: center;">
    <h1>🔮 REFRACTO</h1>
    <p style="color: #94A3B8; font-size: 1.2rem; margin-top: -0.5rem;">
        Tu escritura en descomposición
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Layout de dos columnas
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Tu texto")
    texto_usuario = st.text_area(
        "Pega o escribe tu texto aquí:",
        height=250,
        placeholder="Ejemplo:\n\nHoy fue un día increíble. Aprendí muchas cosas nuevas y conocí personas interesantes. Definitivamente, repetiré la experiencia.",
        label_visibility="collapsed"
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

# Análisis
if boton_analizar:
    if not texto_usuario or len(texto_usuario.strip()) < 20:
        st.warning("⚠️ Escribe al menos 20 caracteres para un análisis significativo.")
    else:
        with st.spinner("🔮 Refractando tu estilo..."):
            resultado = refractar(texto_usuario)
        
        if "error" in resultado:
            st.error(resultado["error"])
        else:
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
            
            # Gráfico de métricas (radar chart)
            st.markdown("### 📊 Espectro de estilo")
            
            metrics = resultado["perfil"]
            
            # Datos para el gráfico
            categories = ['Formalidad', 'Complejidad', 'Repetición', 'Riqueza\nléxica', 'Legibilidad']
            values = [
                metrics["formalidad"] * 10,  # Escalar a 0-10
                metrics["complejidad"],
                metrics["repeticion"] * 10,
                metrics["riqueza_lexica"] * 10,
                metrics["legibilidad"] / 10
            ]
            
            # Gráfico de barras horizontal
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
            st.pyplot(fig)
            
            # Tarjetas de métricas
            st.markdown("### 🔬 Desglose detallado")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                formalidad = metrics["formalidad"]
                color = "#6B46C1"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value" style="color:{color}">{formalidad}</div>
                    <div class="metric-label">Formalidad</div>
                    <div style="font-size:0.8rem;">{'Formal' if formalidad > 0.6 else 'Informal' if formalidad < 0.4 else 'Neutral'}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                complejidad = metrics["complejidad"]
                color = "#3182CE"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value" style="color:{color}">{complejidad}</div>
                    <div class="metric-label">Complejidad</div>
                    <div style="font-size:0.8rem;">/10</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                repeticion = metrics["repeticion"]
                color = "#DD6B20"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value" style="color:{color}">{repeticion}</div>
                    <div class="metric-label">Repetición</div>
                    <div style="font-size:0.8rem;">{'Alta' if repeticion > 0.6 else 'Media' if repeticion > 0.3 else 'Baja'}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                riqueza = metrics["riqueza_lexica"]
                color = "#10B981"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value" style="color:{color}">{riqueza}</div>
                    <div class="metric-label">Riqueza léxica</div>
                    <div style="font-size:0.8rem;">{'Alta' if riqueza > 0.6 else 'Media' if riqueza > 0.4 else 'Baja'}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col5:
                legibilidad = metrics["legibilidad"]
                color = "#F59E0B"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value" style="color:{color}">{legibilidad}</div>
                    <div class="metric-label">Legibilidad</div>
                    <div style="font-size:0.8rem;">{'Fácil' if legibilidad > 60 else 'Normal' if legibilidad > 40 else 'Difícil'}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Tono emocional
            st.markdown("### 🎭 Tono emocional")
            tono = metrics["tono"]
            emoji = "😊" if tono["categoria"] == "positivo" else "😠" if tono["categoria"] == "negativo" else "😐"
            st.info(f"{emoji} **{tono['categoria'].capitalize()}** | Polaridad: {tono['polaridad']} | Subjetividad: {tono['subjetividad']}")
            
            # Recomendación
            st.markdown("### 💡 Recomendación personalizada")
            st.markdown(f"""
            <div class="recommendation-box">
                {resultado['recomendacion']}
            </div>
            """, unsafe_allow_html=True)
            
            # Detalles adicionales (expandible)
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

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    Refracto — Porque cada palabra dobla la luz de quien la escribe<br>
    <span style="font-size: 0.7rem;">✨ Proyecto de práctica — Analiza, aprende, mejora ✨</span>
</div>
""", unsafe_allow_html=True)