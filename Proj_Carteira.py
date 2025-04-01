import streamlit as st
from PIL import Image
import locale
import time
# from google.cloud import bigquery
# from bancos_confiante import bq
import os

# KEY_PATH = os.environ.get("KEY_PATH")
# BIGQUERY = bq('confianca-fidc', KEY_PATH)

# Configurar a localização para o formato brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def calculate_projections(faturamento, prazo_medio):
    # Define a taxa de acordo com o faturamento
    if 800_000 <= faturamento <= 2_000_000:
        taxa_faturamento = 1.9 / 100
    elif 2_100_000 <= faturamento <= 3_500_000:
        taxa_faturamento = 1.7 / 100
    elif 3_600_000 <= faturamento <= 5_000_000:
        taxa_faturamento = 1.4 / 100
    elif faturamento > 5_100_000:
        taxa_faturamento = 1.0 / 100
    else:
        st.warning("O faturamento mensal deve ser no mínimo 800k.")
        return None, None

    # Define a taxa de acordo com o prazo médio de vendas
    if prazo_medio == 30:
        taxa_prazo = 1 / 100
    elif prazo_medio == 45:
        taxa_prazo = 1.5 / 100
    elif prazo_medio == 60:
        taxa_prazo = 2 / 100
    elif prazo_medio == 90:
        taxa_prazo = 2.5 / 100
    elif prazo_medio > 90:
        taxa_prazo = 3 / 100
    else:
        st.warning("Prazo médio de vendas inválido. Escolha entre 30, 45, 60, 90 ou acima de 90 dias.")
        return None, None

    # Calcula a projeção de carteira
    taxa_total = taxa_faturamento + taxa_prazo
    prazo = prazo_medio / 30 / 2
    projecao_carteira = faturamento * prazo #* taxa_total
    # projecao_total = projecao_carteira + faturamento
    
    # print(taxa_total)
    # print(prazo)
    # print(projecao_carteira)
    # print(faturamento)

    return projecao_carteira, taxa_total

# Configurar formatação em reais
def format_currency(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def main():
    
    # Carregar imagem
    image = Image.open("3.png")

    # Redimensionar imagem
    new_width = 300
    new_height = int(image.height * (new_width / image.width))
    resized_image = image.resize((new_width, new_height))
    left_co,cent_co,last_co = st.columns(3)
    with cent_co:
        st.image(resized_image, use_column_width=False)
    # Exibir imagem
    st.title("Simulador de Carteira")
    # Entrada de dados
    cnpj = st.text_input("CNPJ da empresa:")
    # cnae = st.text_input("CNAE da empresa:")
    # segmento = st.text_input("Segmento da empresa:")

    # Campo para faturamento
    st.subheader("Faturamento Mensal")
    # faturamento = st.number_input("Digite o faturamento mensal da empresa (em reais):", 
    #                           min_value=800_000, step=100_000, format="%d")
    
    # Entrada do usuário
    faturamento = st.number_input(
        "Digite o faturamento mensal da empresa (em reais):",
        min_value=800_000,
        step=100_000,
        format="%d"
    )

    # Formatar o número com pontos para milhares/milhões
    faturamento_formatado = f"{faturamento:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    # faturamento_formatado = f"{faturamento:,.0f}".replace(",", ".")  # Substitui ',' por '.' para formato brasileiro

    # Exibir o valor formatado
    st.write(f"Faturamento mensal: R$ {faturamento_formatado}")

    

    # Botões para prazo médio
    st.subheader("Prazo Médio de Vendas")
    prazo_medio_options = [30, 45, 60, 90, 120]
    prazo_medio = st.radio("Selecione o prazo médio de vendas (em dias):", prazo_medio_options)

    # Botão para calcular
    if st.button("Calcular Projeção de Carteira"):
        # Exibir fogos de artifício ao aprovar o crédito
        
        
        with st.spinner("Carregando..."):
            time.sleep(4)
        # st.success("Carregamento concluído!")
        # st.balloons()
        st.toast("Crédito aprovado! Parabéns!")
        if cnpj and faturamento and prazo_medio:
            projecao_carteira, taxa_total = calculate_projections(faturamento, prazo_medio)

            if projecao_carteira is not None:
                projecao_formatada = locale.currency(projecao_carteira, grouping=True)
                st.success(f"A projeção de carteira: {projecao_formatada}")
                # st.info(f"A taxa aplicada foi: {taxa_total * 100:,.2f}%")

                # Exibir tabela com os resultados
                st.table({
                    "Descrição": ["Projeção de Carteira"], #"Taxa Total",
                    "Valor": [projecao_formatada] # f"{taxa_total * 100:.2f}%"]
                })

        else:
            st.error("Por favor, preencha todos os campos corretamente.")
        st.warning(f"Lembrando que isso é apenas uma simulação. Para informações mais precisas, envie os documentos para os contatos abaixo:")
        st.write("**E-mail:** financeiro@empresa.com")
        st.write("**Telefone:** (11) 1234-5678")
        st.write("**WhatsApp:** (11) 91234-5678")
if __name__ == "__main__":
    main()
