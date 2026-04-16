import streamlit as st
import moviepy.editor as mp
from PIL import Image
import numpy as np
import tempfile
import os

st.set_page_config(page_title="Gerador de Vídeo PRO", layout="centered")

st.title("📽️ Criador de Vídeos")

# 1. Upload de Imagens
uploaded_files = st.file_uploader("Selecione até 20 imagens", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    # Opções de personalização
    duracao = st.slider("Segundos por imagem:", 1.0, 5.0, 2.0)
    
    # Botão para iniciar o processamento
    if st.button("Gerar Vídeo Agora"):
        with st.spinner("A processar o vídeo... Aguarde até aparecer o player."):
            try:
                clips = []
                t = 0
                
                # Processar cada imagem
                for file in uploaded_files:
                    img = Image.open(file).convert("RGB").resize((1080, 1920))
                    # Criar o clipe com transição
                    clip = mp.ImageClip(np.array(img)).set_duration(duracao + 0.5).set_start(t).crossfadein(0.5)
                    clips.append(clip)
                    t += duracao
                
                # Criar composição final
                video_final = mp.CompositeVideoClip(clips)
                
                # Guardar num ficheiro temporário que o Streamlit consiga ler
                tmp_dir = tempfile.gettempdir()
                path = os.path.join(tmp_dir, "output_video.mp4")
                
                # Escrever o ficheiro (fps 24 é ideal para redes sociais)
                video_final.write_videofile(path, fps=24, codec="libx264", audio=False)
                
                # --- EXIBIÇÃO ---
                st.success("Vídeo gerado com sucesso!")
                st.video(path)
                
                with open(path, "rb") as f:
                    st.download_button(
                        label="⬇️ Baixar Vídeo para o Telemóvel",
                        data=f,
                        file_name="meu_video_social.mp4",
                        mime="video/mp4"
                    )
            except Exception as e:
                st.error(f"Erro ao processar: {e}")

else:
    st.info("Aguardando imagens para começar...")
