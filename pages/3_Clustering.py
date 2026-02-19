import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

st.set_page_config(page_title="Clustering"
                   , layout="wide")

@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(BASE_DIR, '..', 'data', 'datos_con_clusters.csv'))
    return df

df = load_data()

st.title("Clustering de Géneros")
st.markdown("""
El algoritmo **KMeans** agrupó 106.999 canciones en 10 clusters 
basándose únicamente en sus características de audio, sin saber nada de géneros.
""")

# Perfil de clusters
caract_cluster = ['danceability', 'energy', 'valence',
                    'acousticness', 'instrumentalness',
                    'speechiness', 'tempo', 'loudness']

perfiles_cluster = df.groupby('cluster_name')[caract_cluster].mean()
scaler = MinMaxScaler()
perfiles_cluster_scaled = pd.DataFrame(
    scaler.fit_transform(perfiles_cluster),
    index=perfiles_cluster.index,
    columns=perfiles_cluster.columns
)

# Dos columnas
col1, col2 = st.columns(2)

with col1:
    st.subheader("Perfil sonoro de cada cluster")
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(
        perfiles_cluster_scaled,
        cmap='coolwarm',
        ax=ax,
        linewidths=0.5,
        annot=True,
        fmt='.2f'
    )
    ax.set_title('Heatmap de Clusters', fontsize=13)
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("¿Qué hay en cada cluster?")
    cluster_seleccionado = st.selectbox(
        "Selecciona un cluster:",
        options=sorted(df['cluster_name'].unique().tolist())
    )
    
    top_genres = (df[df['cluster_name'] == cluster_seleccionado]
                  ['track_genre']
                  .value_counts()
                  .head(8))
    
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    top_genres.plot(kind='barh', ax=ax2, color='steelblue')
    ax2.set_title(f'Géneros en: {cluster_seleccionado}')
    ax2.set_xlabel('Número de canciones')
    plt.tight_layout()
    st.pyplot(fig2)

# Hallazgo destacado
st.divider()
st.info(""" **Hallazgo clave:** La música turca y el hip-hop fueron agrupados en el mismo cluster 
pese a ser culturalmente muy distintos. El algoritmo solo escucha números, no cultura.
""")