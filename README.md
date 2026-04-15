
# 🔮 Refracto

Refracto es una herramienta de análisis de escritura que descompone cualquier texto en un perfil lingüístico completo. Como un prisma que separa la luz en colores, Refracto revela las dimensiones ocultas de tu forma de escribir.

Métricas que analiza:

Formalidad — Detecta si tu texto es profesional, neutral o coloquial, analizando pronombres personales, contracciones y muletillas.

Complejidad — Mide la estructura de tus oraciones y la longitud de tus palabras. Textos más complejos suelen tener oraciones más largas y vocabulario elaborado.

Repetición — Identifica palabras que usas en exceso. Una repetición alta puede hacer que tu texto sea monótono o redundante.

Riqueza léxica — Evalúa la variedad de tu vocabulario. Cuanto más único sea tu conjunto de palabras, más rico se considera tu estilo.

Legibilidad — Calcula qué tan fácil es leer y entender tu texto, usando el índice Flesch adaptado al español.

Tono emocional — Detecta si tu escritura es positiva, negativa o neutral, además de medir su subjetividad.

Además, Refracto incluye:

💡 Recomendaciones personalizadas para mejorar tu estilo

📚 Historial automático de todos tus análisis

⚔️ Comparador lado a lado de dos textos

Ideal para escritores, estudiantes, profesionales y cualquier persona que quiera entender y mejorar su forma de escribir.

---

## 🚀 Instalación rápida

```bash
# 1. Clonar o crear carpeta
git clone https://github.com/tuusuario/refracto.git
cd refracto

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar
streamlit run app.py
```

La app se abre en `http://localhost:8501`

---

## 📁 Archivos necesarios

| Archivo | Qué hace |
|---------|----------|
| `app.py` | Interfaz (Streamlit) |
| `refractor.py` | Motor de análisis |
| `requirements.txt` | Librerías necesarias |

---

## ☁️ Desplegar en la nube

### Opción 1: Streamlit Cloud (más fácil)

1. Sube los archivos a GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Selecciona tu repositorio y archivo `app.py`
4. Listo

### Opción 2: Railway

1. Sube tu código a GitHub
2. Ve a [railway.app](https://railway.app)
3. "New Project" → "Deploy from GitHub"
4. Railway lo detecta automáticamente

---

## 📊 Métricas

| Métrica | Rango | Qué significa |
|---------|-------|---------------|
| Formalidad | 0-1 | >0.6 formal / <0.4 informal |
| Complejidad | 0-10 | >7 complejo / <4 simple |
| Repetición | 0-1 | >0.6 mucha repetición |
| Riqueza léxica | 0-1 | >0.6 vocabulario rico |
| Legibilidad | 0-100 | >60 fácil / <40 difícil |
| Tono | -1 a 1 | Positivo / Neutral / Negativo |

---

## 🎮 Cómo usar

**Analizar texto:**
- Pega tu texto → haz clic en "REFRACTAR"

**Comparar dos textos:**
- Ve a la pestaña "Comparar textos" → analiza A y B

**Ver historial:**
- Los análisis se guardan solos → sidebar izquierdo

---

## 🧪 Ejemplo

**Texto:** *"La verdad es que esto es muy muy interesante"*

**Resultado:**
- Formalidad: 0.28 (informal)
- Repetición: 0.67 (alta)
- Recomendación: "Evita repetir 'muy'"

---

## 📦 Dependencias

```
streamlit>=1.28.0
textblob>=0.17.0
matplotlib>=3.7.0
```

---

## 📄 Licencia

MIT

---

**¿Preguntas?** Abre un issue en GitHub.
```

---

## ✅ Cambios que hice

| Antes | Ahora |
|-------|-------|
| 200+ líneas | ~70 líneas |
| Badges decorativos | Eliminados |
| Emojis y centrado | Minimalista |
| Explicaciones largas | Tablas directas |
| Múltiples opciones de despliegue | Solo las 2 más útiles |
| Capturas de pantalla (placeholder) | Eliminadas |

---
