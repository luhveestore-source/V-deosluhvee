import streamlit as st
import moviepy.editor as mp
from PIL import Image, ImageOps
import numpy as np
import tempfile
import os

st.set_page_config(page_title="Gerador PRO - Sem Distorção", layout="centered")
st.title("📽️ Criador de Vídeos (Formato Correto)")

uploaded_files = st.file_uploader("Selecione as imagens", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    duracao = st.slider("Segundos por imagem:", 1.0, 5.0, 3.0)
    
    if st.button("Gerar Vídeo"):
        with st.spinner("Ajustando proporções e gerando vídeo..."):
            try:
                clips = []
                t = 0
                largura_alvo, altura_alvo = 1080, 1920

                for file in uploaded_files:
                    # 1. Abrir imagem original
                    img_original = Image.open(file).convert("RGB")
                    
                    # 2. Criar um fundo preto sólido
                    fundo_preto = Image.new('RGB', (largura_alvo, altura_alvo), (0, 0, 0))
                    
                    # 3. Redimensionar a imagem mantendo a proporção (sem esticar)
                    img_proporcional = ImageOps.contain(img_original, (largura_alvo, altura_alvo))
                    
                    # 4. Centralizar a imagem no fundo preto
                    x = (largura_alvo - img_proporcional.width) // 2
                    y = (altura_alvo - img_proporcional.height) // 2
                    fundo_preto.paste(img_proporcional, (x, y))
                    
                    # 5. Transformar em clipe
                    clip = mp.ImageClip(np.array(fundo_preto)).set_duration(duracao + 0.5).set_start(t).crossfadein(0.5)
                    clips.append(clip)
                    t += duracao
                
                # Gerar vídeo final
                video_final = mp.CompositeVideoClip(clips)
                path = os.path.join(tempfile.gettempdir(), "video_perfeito.mp4")
                video_final.write_videofile(path, fps=24, codec="libx264", audio=False)
                
                st.success("Vídeo ajustado!")
                st.video(path)
                with open(path, "rb") as f:
                    st.download_button("⬇️ Baixar Vídeo Ajustado", f, "video_corrigido.mp4")

            except Exception as e:
                st.error(f"Erro: {e}")
