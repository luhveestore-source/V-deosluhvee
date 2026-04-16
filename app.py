import streamlit as st
import os

# Tentativa de importação robusta
try:
    from moviepy.editor import ImageClip, CompositeVideoClip
except ImportError:
    st.error("O MoviePy ainda não foi instalado pelo Streamlit. Por favor, aguarde 1 minuto e recarregue a página.")
    st.stop()

from PIL import Image
import numpy as np
import tempfile

st.set_page_config(page_title="Gerador de Vídeo", layout="centered")

st.title("📽️ Criador de Vídeos Profissional")

# O resto do código continua igual...
uploaded_files = st.file_uploader("Selecione fotos", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    duracao = st.slider("Duração (seg)", 1.0, 5.0, 2.0)
    if st.button("Gerar Vídeo"):
        with st.spinner("Criando..."):
            clips = []
            t = 0
            for file in uploaded_files:
                img = Image.open(file).convert("RGB").resize((1080, 1920))
                c = ImageClip(np.array(img)).set_duration(duracao + 0.5).set_start(t).crossfadein(0.5)
                clips.append(c)
                t += duracao
            
            final = CompositeVideoClip(clips)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                final.write_videofile(tmp.name, fps=24, codec="libx264", audio=False)
                st.video(tmp.name)
                with open(tmp.name, "rb") as f:
                    st.download_button("Baixar Vídeo", f, "video.mp4")
