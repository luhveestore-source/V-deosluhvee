import streamlit as st
from moviepy.editor import ImageClip, CompositeVideoClip
from PIL import Image
import numpy as np
import tempfile

st.set_page_config(page_title="Gerador Pro com Transição", layout="centered")

st.title("✨ Gerador de Vídeo com Transições")
st.write("Crie vídeos suaves para o Instagram ou TikTok.")

# --- PASSO 1: Upload ---
uploaded_files = st.file_uploader(
    "Selecione até 20 imagens", 
    type=["png", "jpg", "jpeg"], 
    accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) > 20:
        st.warning("Apenas as primeiras 20 imagens serão processadas.")
        uploaded_files = uploaded_files[:20]

    # --- PASSO 2: Configurações ---
    duracao_imagem = st.slider("Duração de cada imagem (segundos):", 1.0, 5.0, 3.0)
    tempo_transicao = st.slider("Duração da transição (segundos):", 0.1, 1.0, 0.5)

    # --- PASSO 3: Processamento ---
    if st.button("Gerar Vídeo com Transição"):
        with st.spinner("Aplicando efeitos de transição..."):
            try:
                clips = []
                tempo_atual = 0

                for i, file in enumerate(uploaded_files):
                    # Abrir e redimensionar
                    img = Image.open(file).convert("RGB")
                    img = img.resize((1080, 1920))
                    img_array = np.array(img)

                    # Criar clipe da imagem
                    # Adicionamos o tempo de transição à duração para haver margem de sobreposição
                    clip = ImageClip(img_array).set_duration(duracao_imagem + tempo_transicao)
                    
                    # Definir quando o clipe começa na timeline
                    clip = clip.set_start(tempo_atual).crossfadein(tempo_transicao)
                    
                    clips.append(clip)
                    
                    # O próximo clipe começa um pouco antes deste terminar
                    tempo_atual += duracao_imagem

                # Juntar todos os clipes numa composição
                video_final = CompositeVideoClip(clips)
                
                # Guardar em ficheiro temporário
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
                    video_final.write_videofile(tmpfile.name, fps=24, codec="libx264")
                    
                    # Mostrar na App
                    st.video(tmpfile.name)

                    # Botão de Download
                    with open(tmpfile.name, "rb") as f:
                        st.download_button(
                            label="⬇️ Descarregar Vídeo com Transições",
                            data=f,
                            file_name="video_transicao.mp4",
                            mime="video/mp4"
                        )
                
                st.success("Pronto! Agora é só postar e escolher a música na rede social.")

            except Exception as e:
                st.error(f"Erro técnico: {e}")