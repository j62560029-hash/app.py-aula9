import streamlit as range_utils
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import time
import random

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Simulador de Visão Computacional",
    page_icon="👁️",
    layout="centered"
)

# Título e descrição do projeto
st.title("👁️ Simulador de Visão Computacional")
st.subheader("Atividade Acadêmica: Detecção de Objetos Baseada em Regras")
st.write(
    "Este aplicativo simula o funcionamento de um modelo de Inteligência Artificial "
    "para detecção de objetos de forma leve, utilizando lógica de programação simples "
    "e processamento digital de imagens com a biblioteca Pillow (PIL)."
)

st.markdown("---")

# Seção de Upload da Imagem pelo usuário
st.sidebar.header("⚙️ Configurações")
uploaded_file = st.sidebar.file_uploader(
    "Escolha uma imagem (JPG, PNG ou JPEG):", 
    type=["jpg", "jpeg", "png"]
)

# Seleção do objeto que o usuário deseja "detectar"
objeto_alvo = st.sidebar.selectbox(
    "O que você deseja detectar na imagem?",
    ["Pessoa", "Carro", "Animal (Cão/Gato)", "Celular"]
)

if uploaded_file is not None:
    # 1. Carregar a imagem usando a biblioteca PIL
    imagem_original = Image.open(uploaded_file).convert("RGB")
    largura, altura = imagem_original.size

    # Criar duas colunas para visualização (Antes e Depois)
    col1, col2 = st.columns(2)

    with col1:
        st.image(imagem_original, caption="Imagem Original", use_container_width=True)

    with col2:
        # Botão para iniciar a simulação do escaneamento
        if st.button("🔍 Iniciar Detecção Simulada"):
            
            # Simulação de um tempo de processamento (efeito visual para o usuário)
            with st.spinner("Analisando pixels e aplicando lógica baseada em regras..."):
                time.sleep(1.5)  # Pausa de 1.5 segundos
                
            # 2. Lógica Simples Baseada em Regras (Simulação)
            # Para fins didáticos, vamos extrair a cor média do centro da imagem
            # e usá-la como uma "falsa métrica de confiança" do algoritmo.
            pixel_centro = imagem_original.getpixel((largura // 2, altura // 2))
            confianca_simulada = round(max(50.0, min(99.0, (pixel_centro[0] + pixel_centro[1] + pixel_centro[2]) / 3)), 2)

            # 3. Desenhar o Bounding Box (Caixa de Delimitação) Falso
            # Criamos uma cópia da imagem para não alterar a original
            imagem_processada = imagem_original.copy()
            draw = ImageDraw.Draw(imagem_processada)
            
            # Define coordenadas fictícias/aleatórias para a caixa com base no tamanho da imagem
            # Garante que a caixa fique centralizada de forma dinâmica
            x1 = int(largura * 0.25)
            y1 = int(altura * 0.25)
            x2 = int(largura * 0.75)
            y2 = int(altura * 0.75)
            
            # Desenha o retângulo (Bounding Box) na imagem com cor verde
            draw.rectangle([x1, y1, x2, y2], outline="green", width=5)
            
            # Adiciona o texto com a classe detectada e a confiança simulada
            texto_exibido = f"{objeto_alvo}: {confianca_simulada}%"
            
            # Tenta desenhar o texto logo acima da caixa
            draw.text((x1 + 5, y1 + 5), texto_exibido, fill="green")

            # Exibe a imagem com a detecção simulada na tela
            st.image(imagem_processada, caption="Resultado da Detecção", use_container_width=True)
            
            # Exibe métricas de sucesso acadêmico
            st.success(f"🎉 Sucesso! Objeto '{objeto_alvo}' simulado com {confianca_simulada}% de confiança.")
            st.info(
                f"**Nota Didática:** O sistema simulou a detecção desenhando uma caixa fixa "
                f"nas coordenadas [{x1}, {y1}, {x2}, {y2}] baseado no tamanho da sua imagem ({largura}x{altura}px)."
            )
        else:
            st.warning("Clique no botão acima para processar a imagem.")

else:
    # Mensagem caso nenhuma imagem tenha sido carregada ainda
    st.info("💡 Por favor, carregue uma imagem no menu lateral para começar a simulação.")

st.markdown("---")
st.caption("Desenvolvido para fins acadêmicos e demonstração lógica de estruturas de dados aplicadas a imagens.")