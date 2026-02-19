import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Spotify Genre Analysis",
    page_icon="🎵",
    layout="wide"
)

# Estilo CSS para mejorar la apariencia
st.markdown("""
    <style>
    .main {
        background-color: #121212;
        color: white;
    }
    .stMarkdown h1, h2, h3 {
        color: #1DB954 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Título e Introducción
st.title("Spotify Genre Analysis")
st.subheader("Descubriendo el ADN sonoro de la música")

st.markdown("""
Bienvenido a este análisis exploratorio y de clustering sobre más de **100.000 canciones** de Spotify. 
Este proyecto nace de la curiosidad por entender si los géneros musicales tienen fronteras sonoras reales 
o si son simples etiquetas culturales.

### ¿Cómo navegar por esta App?
En la **barra lateral de la izquierda** encontrarás diferentes secciones para explorar los datos:

* **Radar Chart**: Compara las características de audio (bailabilidad, energía, acústica) entre diferentes géneros.
* **Heatmap**: Visualiza la correlación entre las variables que definen el éxito de una canción.
* **Clustering**: Descubre cómo el aprendizaje no supervisado agrupa los géneros por sus similitudes acústicas reales.

---
""")

# Mostrar una pequeña muestra de los datos para dar contexto
st.info(" Estamos utilizando un dataset de Kaggle con 114,000 canciones procesadas mediante PCA y K-Means.")

try:
    df_sample = pd.read_csv('data/datos_con_clusters.csv').head(10)
    st.write("### Vista previa de los datos analizados:")
    st.dataframe(df_sample)
except Exception as e:
    st.warning("El dataset se está cargando o no está disponible en la raíz.")

st.sidebar.success("Selecciona una sección arriba para comenzar.")