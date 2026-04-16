import streamlit as st
import moviepy.editor as mp
from PIL import Image
import numpy as np
import tempfile

st.title("Gerador de Vídeo - Status: Ativo ✅")

uploaded_files = st.file_uploader("Suba as imagens", accept_multiple_files=True)

if uploaded_files:
    if st.button("Gerar"):
        st.write("Processando...")
        # Lógica simples para testar o MoviePy
        img = Image.open(uploaded_files[0]).convert("RGB").resize((720, 1280))
        clip = mp.ImageClip(np.array(img)).set_duration(2)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
            clip.write_videofile(tmp.name, fps=24, codec="libx264")
            st.video(tmp.name)
