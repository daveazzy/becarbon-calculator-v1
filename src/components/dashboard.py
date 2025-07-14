import streamlit as st
import pandas as pd
from ..visuals import charts 

def render_dashboard(df_country: pd.DataFrame, df_category: pd.DataFrame, df_analise_completa: pd.DataFrame):
    """
    Renderiza o painel de inteligência de mercado no Streamlit.

    Args:
        df_country (pd.DataFrame): DataFrame com o perfil por país.
        df_category (pd.DataFrame): DataFrame com o perfil por categoria.
        df_analise_completa (pd.DataFrame): O DataFrame com todas as transações de aposentadoria.
                                            Usado para o mapa de calor.
    """
    st.header("Visão Geral do Mercado de Aposentadorias (2016-2024)")
    st.markdown("Esta seção apresenta insights sobre os principais mercados e categorias de projetos de carbono.")

    # --- Seção 1: Análise por País ---
    st.subheader("🌍 Perfil dos Principais Mercados Nacionais")
    
    col1, col2 = st.columns(2) # Cria duas colunas para organizar o layout
    
    with col1:
        st.dataframe(df_country, use_container_width=True)
    
    with col2:
        # Cria e exibe o gráfico de barras para o volume por país
        fig_bar_country = charts.create_bar_chart(
            df=df_country,
            x_axis='País',
            y_axis='Volume Total Aposentado',
            title='Top 10 Países por Volume Aposentado'
        )
        st.plotly_chart(fig_bar_country, use_container_width=True)

    # --- Seção 2: Análise por Categoria ---
    st.subheader("🌱 Perfil das Principais Categorias de Projeto")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.dataframe(df_category, use_container_width=True)
        
    with col4:
        # Cria e exibe o gráfico de barras para o volume por categoria
        fig_bar_category = charts.create_bar_chart(
            df=df_category,
            x_axis='Categoria',
            y_axis='Volume Total Aposentado',
            title='Top 7 Categorias por Volume Aposentado'
        )
        st.plotly_chart(fig_bar_category, use_container_width=True)
        
    # --- Seção 3: Mapa de Calor ---
    st.subheader("🗺️ Mapa de Concentração de Mercado (País vs. Categoria)")

    # Usa as listas dos dataframes de perfil para manter a consistência
    top_paises = df_country['País'].tolist()
    top_categorias = df_category['Categoria'].tolist()

    fig_heatmap = charts.create_heatmap(
        df_analise=df_analise_completa,
        top_countries=top_paises,
        top_categories=top_categorias
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)