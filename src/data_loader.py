import streamlit as st
import pandas as pd
from . import config
from .utils.custom_exceptions import DataFileNotFoundError

@st.cache_data
def load_all_data():
    """Carrega todos os 5 DataFrames necessários para a aplicação."""
    try:
        # Carrega os arquivos
        df_alignment = pd.read_csv(config.ALIGNMENT_INDEX_FILE)
        df_opps_scored = pd.read_csv(config.OPPORTUNITIES_SCORED_FILE)
        df_country_profile = pd.read_csv(config.COUNTRY_PROFILE_FILE)
        df_category_profile = pd.read_csv(config.CATEGORY_PROFILE_FILE)
        df_transactions = pd.read_csv(config.TRANSACTIONS_FILE) # Carrega os dados para o heatmap

        print("Dados carregados do disco e armazenados em cache.")
        
        # Retorna todos os dataframes
        return df_alignment, df_opps_scored, df_country_profile, df_category_profile, df_transactions

    except FileNotFoundError as e:
        raise DataFileNotFoundError(f"Arquivo de dados não encontrado: {e.filename}. Verifique a pasta 'data/'.")