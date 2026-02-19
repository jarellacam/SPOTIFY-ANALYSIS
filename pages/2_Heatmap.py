import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

st.set_page_config(page_title="ADN Sonoro"
                   , layout="wide")

@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(BASE_DIR, '..', 'data', 'datos_con_clusters.csv'))
    return df

df = load_data()

caract_radar = ['danceability', 'energy', 'valence',
                  'acousticness', 'instrumentalness', 'speechiness']

media_generos = df.groupby('track_genre')[caract_radar].mean()
scaler = MinMaxScaler()
media_generos_scalar = pd.DataFrame(
    scaler.fit_transform(media_generos),
    index=media_generos.index,
    columns=media_generos.columns
)

st.title("ADN Sonoro por Género")
st.markdown("Visualiza las características de audio de cada género musical.")

# Filtro de géneros
generos = sorted(df['track_genre'].unique().tolist())
seleccionados = st.multiselect(
    "Filtra géneros (vacío = todos):",
    options=generos,
    default=[]
)

data_to_show = media_generos_scalar.loc[seleccionados] if seleccionados else media_generos_scalar

# Heatmap
fig, ax = plt.subplots(figsize=(12, max(6, len(data_to_show) * 0.3)))
sns.heatmap(
    data_to_show,
    cmap='coolwarm',
    ax=ax,
    linewidths=0.3,
    cbar_kws={'label': 'Valor normalizado'}
)
ax.set_title('ADN Sonoro por Género', fontsize=14, pad=20)
ax.set_xlabel('Característica')
ax.set_ylabel('Género')
plt.tight_layout()
st.pyplot(fig)