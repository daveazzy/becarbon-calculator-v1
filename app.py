import streamlit as st
import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from src.data_loader import load_all_data
from src.components import dashboard, calculator, academic_context, data_preview
from src.utils.error_handlers import handle_data_loading_error
from src.utils.custom_exceptions import DataFileNotFoundError

st.set_page_config(page_title="Consultor de Carbono", page_icon="🌍", layout="wide")

def load_css(file_name: str):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Arquivo CSS '{file_name}' não encontrado.")

try:
    df_alignment, df_opps_scored, df_country, df_category, df_transactions = load_all_data()
    
    load_css("assets/styles.css")

    st.title("🌍 Consultor Estratégico para o Mercado de Carbono")

    tabs = ["💡 Consultor de Tese", "📊 Dashboard de Mercado", "🎓 Contexto do Projeto", "📋 Visualização dos Dados"]
    tab1, tab2, tab3, tab4 = st.tabs(tabs)

    with tab1:
        calculator.render_calculator(df_alignment=df_alignment, df_opps=df_opps_scored)
        
    with tab2:
        dashboard.render_dashboard(
            df_country=df_country,
            df_category=df_category,
            df_analise_completa=df_transactions
        )
        
    with tab3:
        academic_context.render_academic_context()
        
    with tab4:
        data_preview.render_data_preview()

except DataFileNotFoundError as e:
    handle_data_loading_error(e)
except Exception as e:
    st.error(f"Ocorreu um erro inesperado na aplicação: {e}")
    st.exception(e)