import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Radar de géneros", 
    layout="wide"
)

# cargamos datos
@st.cache_data
def load_data():
    df = pd.read_csv("data/datos_con_clusters.csv")
    return df

df = load_data()

# caract y normalización
caract_radar = ['danceability', 'energy', 'valence',
                  'acousticness', 'instrumentalness', 'speechiness']

media_genero = df.groupby('track_genre')[caract_radar].mean()
scaler = MinMaxScaler()
media_genero_scaler = pd.DataFrame(
    scaler.fit_transform(media_genero),
    index = media_genero.index,
    columns=media_genero.columns
)

# Interfaz
st.title("Comparador de Géneros")
st.markdown("Selecciona entre 2 y 6 géneros para comparar su ADN sonoro.")

genres_available = sorted(df['track_genre'].unique().tolist())
selected_genres = st.multiselect(
    "Elige los géneros a comparar:",
    options=genres_available,
    default=['classical', 'black-metal', 'reggaeton', 'hip-hop']
)

if len(selected_genres) < 2:
    st.warning("Selecciona al menos 2 géneros para comparar.")
else:
    # Generamos radar
    angles = np.linspace(0, 2*np.pi, len(caract_radar), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    colors = ['steelblue', 'crimson', 'gold', 'purple', 'green', 'orange']

    for i, genre in enumerate(selected_genres):
        values = media_genero_scaler.loc[genre, caract_radar ].tolist()
        values += values[:1]
        ax.plot(angles, values, 'o-', linewidth=2, 
                label=genre, color=colors[i % len(colors)])
        ax.fill(angles, values, alpha=0.15, color=colors[i % len(colors)])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(caract_radar , fontsize=11)
    ax.set_title('ADN Sonoro Comparativo', fontsize=14, pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.pyplot(fig)