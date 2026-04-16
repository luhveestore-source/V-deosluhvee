import streamlit as st

# Tenta carregar as bibliotecas de forma silenciosa
try:
    import moviepy.editor as mp
    from PIL import Image
    import numpy as np
    import tempfile
    import os
except Exception as e:
    st.error(f"Ainda estamos a preparar o ambiente. Erro: {e}")
    st.info("Dica: Verifique se o ficheiro requirements.txt está correto no GitHub.")
    st.stop()
