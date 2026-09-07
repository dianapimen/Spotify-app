import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Configuración de la página
st.set_page_config(page_title="Spotify Data IA", layout="centered")

st.title("📊 Dashboard de Spotify - Clase de IA")
st.write("Visualización de datos consumiendo el dataset de Spotify.")

# 2. Cargar el dataset
@st.cache_data
def load_data():
    # Asegúrate de que el nombre del archivo sea exactamente el mismo que bajaste
    df = pd.read_csv("dataset.csv") 
    return df

try:
    df = load_data()
    st.success("¡Dataset cargado correctamente!")

    # 3. Mostrar una vista previa de los datos
    if st.checkbox("Mostrar las primeras 10 filas"):
        st.dataframe(df.head(10))

    # --- GRÁFICA 1: Histograma con Matplotlib ---
    st.header("Distribución de la Popularidad")
    
    fig1, ax1 = plt.subplots() # Crear la figura de Matplotlib
    ax1.hist(df['popularity'], bins=20, color='skyblue', edgecolor='black')
    ax1.set_xlabel('Popularidad')
    ax1.set_ylabel('Frecuencia')
    ax1.set_title('Histograma de Popularidad de Canciones')
    
    st.pyplot(fig1) # Mostrar la figura en Streamlit

    # --- GRÁFICA 2: Gráfico de Dispersión (Scatter Plot) ---
    st.header("Relación Energía vs Danzabilidad")
    
    fig2, ax2 = plt.subplots()
    ax2.scatter(df['danceability'], df['energy'], alpha=0.5, color='green')
    ax2.set_xlabel('Danzabilidad')
    ax2.set_ylabel('Energía')
    ax2.set_title('Scatter Plot: Danceability vs Energy')
    
    st.pyplot(fig2)

except Exception as e:
    st.error(f"Error al cargar el dataset: {e}")
    st.info("Asegúrate de que el archivo 'dataset.csv' esté en la misma carpeta que app.py")