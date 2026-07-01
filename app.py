import streamlit as st
from PIL import Image
import torch
from torchvision import models, transforms
import requests

# Configuração da página
st.set_page_config(page_title="IA de Visão Computacional Real", page_icon="🧠", layout="centered")

st.title("🧠 Inteligência Artificial Real: Classificação de Imagens")
st.subheader("Atividade Acadêmica: Rede Neural MobileNetV2")
st.write("Agora o sistema utiliza uma rede neural profunda real, treinada com milhões de imagens (ImageNet), para identificar o objeto predominante na sua foto.")

st.markdown("---")

# Função para carregar as etiquetas (nomes das classes) do ImageNet
@st.cache_resource
def carregar_modelo_e_labels():
    # Carrega o modelo de IA leve pré-treinado
    modelo = models.mobilenet_v2(weights=models.MobileNetV2_Weights.DEFAULT)
    modelo.eval() # Coloca o modelo em modo de inferência (teste)
    
    # Baixa a lista de nomes dos objetos que a IA consegue reconhecer
    url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
    labels = requests.get(url).text.splitlines()
    
    return modelo, labels

try:
    modelo, labels = carregar_modelo_e_labels()
except Exception as e:
    st.error("Erro ao carregar o modelo de IA. Verifique a conexão.")

# Upload da imagem
uploaded_file = st.sidebar.file_uploader("Escolha uma imagem:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    imagem = Image.open(uploaded_file).convert("RGB")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(imagem, caption="Imagem Enviada", use_container_width=True)
        
    with col2:
        if st.button("🧠 Executar Inteligência Artificial"):
            with st.spinner("A Rede Neural está analisando os padrões de pixels..."):
                
                # Preparação da imagem para a IA (Redimensionar e Normalizar)
                transformacao = transforms.Compose([
                    transforms.Resize(256),
                    transforms.CenterCrop(224),
                    transforms.ToTensor(),
                    transforms.Normalize(
                        mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225]
                    )
                ])
                
                # Aplica a transformação e adiciona uma dimensão de lote (batch)
                tensor_imagem = transformacao(imagem).unsqueeze(0)
                
                # Executa a IA sem calcular gradientes (mais rápido e gasta menos memória)
                with torch.no_grad():
                    outputs = modelo(tensor_imagem)
                    # Aplica Softmax para transformar os resultados em porcentagens (probabilidades)
                    probabilidades = torch.nn.functional.softmax(outputs[0], dim=0)
                
                # Pega o resultado com maior certeza
                id_classe_mais_alta = torch.argmax(probabilidades).item()
                nome_objeto = labels[id_classe_mais_alta]
                confianca = probabilidades[id_classe_mais_alta].item() * 100
                
                # Exibe o resultado real
                st.success(f"🎉 **Identificado:** {nome_objeto.capitalize()}")
                st.info(f"🎯 **Grau de Certeza da IA:** {confianca:.2f}%")
                
                # Nota acadêmica explicativa
                st.markdown("### 📊 Como a IA pensou?")
                st.write(
                    "A imagem foi convertida em uma matriz numérica (tensor). A rede neural "
                    "passou esses números por várias camadas de convolução, extraindo características como formatos, "
                    "texturas e cores, até concluir qual objeto da base de dados se parecia mais com o enviado."
                )
else:
    st.info("💡 Carregue uma imagem para testar a IA real!")
