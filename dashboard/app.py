import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sprint4 - IA Dashboard", layout="wide")
st.title("Sprint 4 – IA (Detecção de Motos) :bar_chart:")

BACKEND_URL = st.secrets.get("BACKEND_URL", "http://localhost:8000")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Saúde do Backend")
    try:
        health = requests.get(f"{BACKEND_URL}/health", timeout=3).json()
        st.success(f"OK - {health['ts']}")
    except Exception as e:
        st.error(f"Falha no backend: {e}")

with col2:
    st.subheader("Estatísticas")
    try:
        stats = requests.get(f"{BACKEND_URL}/stats", timeout=5).json()
        st.metric("Total", stats.get("total", 0))
        c1, c2 = st.columns(2)
        c1.metric("Esquerda", stats.get("moto_esquerda", 0))
        c2.metric("Direita", stats.get("moto_direita", 0))
    except Exception as e:
        st.error(f"Erro ao obter stats: {e}")

st.divider()
st.subheader("Eventos recentes")

try:
    df = pd.DataFrame(requests.get(f"{BACKEND_URL}/events?limit=500", timeout=5).json())
    if not df.empty:
        st.dataframe(df)
        st.subheader("Dispersão (cx, cy)")
        plt.figure()
        plt.scatter(df["cx"], df["cy"], s=10)
        plt.gca().invert_yaxis()
        plt.xlabel("Largura (px)")
        plt.ylabel("Altura (px)")
        st.pyplot(plt.gcf())
    else:
        st.info("Sem eventos ainda.")
except Exception as e:
    st.error(f"Erro ao listar eventos: {e}")
