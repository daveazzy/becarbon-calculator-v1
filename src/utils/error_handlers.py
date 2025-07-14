import streamlit as st

def handle_data_loading_error(exception):
    """
    Exibe uma mensagem de erro formatada no Streamlit e para a execução do app
    quando um DataFileNotFoundError ocorre.
    """
    st.error(f"❌ Erro Crítico ao Carregar os Dados: {exception}")
    st.warning(
        "A aplicação não pode continuar sem os arquivos de dados essenciais. "
        "Por favor, verifique se a pasta 'data/' contém os seguintes arquivos:"
    )
    st.code(
        "- relatorio_de_oportunidades.csv\n"
        "- perfil_mercado_por_pais.csv\n"
        "- perfil_mercado_por_categoria.csv"
    )
    # st.stop() é um comando útil que interrompe a execução do script do Streamlit
    # de forma limpa, sem mostrar uma stacktrace feia para o usuário final.
    st.stop()