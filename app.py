import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de la página (Ancho completo)
st.set_page_config(page_title="Spotify Data Insights", layout="wide")

# Estilo personalizado para que se vea más moderno
st.markdown("""
    <style>
    .main {
        background-color: #121212;
        color: white;
    }
    stMetric {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")
    # Limpieza básica por si acaso
    df = df.dropna()
    return df

df = load_data()

# --- BARRA LATERAL (FILTROS) ---
st.sidebar.header("🔍 Filtros de Búsqueda")
# Filtro por Artista
all_artists = sorted(df['artists'].unique())
selected_artists = st.sidebar.multiselect("Selecciona Artistas", all_artists, default=all_artists[:5])

# Filtro por Rango de Popularidad
pop_range = st.sidebar.slider("Rango de Popularidad", 0, 100, (0, 100))

# Aplicar filtros
df_filtered = df[(df['artists'].isin(selected_artists)) & 
                 (df['popularity'] >= pop_range[0]) & 
                 (df['popularity'] <= pop_range[1])]

# --- CUERPO PRINCIPAL ---
st.title("🎵 Spotify Data Analytics Dashboard")
st.markdown("---")

# 1. MÉTRICAS CLAVE (KPIs)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Canciones", len(df_filtered))
with col2:
    st.metric("Popularidad Media", f"{round(df_filtered['popularity'].mean(), 1)}%")
with col3:
    st.metric("Danzabilidad Promedio", f"{round(df_filtered['danceability'].mean(), 2)}")
with col4:
    st.metric("Energía Promedio", f"{round(df_filtered['energy'].mean(), 2)}")

st.markdown("---")

# 2. GRÁFICAS EN COLUMNAS
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 Distribución de Atributos Audio")
    # Creamos un boxplot de varios atributos para comparar
    fig, ax = plt.subplots(figsize=(8, 6))
    features = ['danceability', 'energy', 'valence', 'acousticness']
    ax.boxplot(df_filtered[features], labels=features)
    ax.set_title("Variabilidad de Atributos")
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

with col_right:
    st.subheader("🔝 Top 10 Canciones más Populares")
    top_10 = df_filtered.nlargest(10, 'popularity')[['track_name', 'popularity']]
    
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.barh(top_10['track_name'], top_10['popularity'], color='springgreen')
    ax2.invert_yaxis()  # Para que la más popular esté arriba
    ax2.set_xlabel('Popularidad')
    st.pyplot(fig2)

# 3. ANÁLISIS DETALLADO (Scatter Plot)
st.markdown("---")
st.subheader("🎯 Relación: Energía vs Valencia (Estado de Ánimo)")
st.write("La valencia mide qué tan positiva es una canción.")

fig3, ax3 = plt.subplots(figsize=(12, 5))
scatter = ax3.scatter(df_filtered['valence'], df_filtered['energy'], 
                    c=df_filtered['popularity'], cmap='viridis', alpha=0.6)
ax3.set_xlabel('Valencia (Triste -> Alegre)')
ax3.set_ylabel('Energía')
plt.colorbar(scatter, label='Popularidad')
st.pyplot(fig3)

# 4. TABLA DE DATOS AL FINAL
st.markdown("---")
with st.expander("Ver lista completa de canciones filtradas"):
    st.write(df_filtered)
