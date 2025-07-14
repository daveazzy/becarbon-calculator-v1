# src/components/calculator.py (VERSÃO FINAL COM GRÁFICO DE RADAR)

import streamlit as st
import pandas as pd
from ..analysis import strategy
from ..visuals import charts

def render_calculator(df_alignment: pd.DataFrame, df_opps: pd.DataFrame):
    """Renderiza a interface do Consultor Estratégico Interativo com layout aprimorado."""
    
    if 'selected_country' not in st.session_state:
        st.session_state.selected_country = None
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = None

    col_control, col_results = st.columns((1, 2))

    # ==============================================================================
    # PAINEL DE CONTROLE (COLUNA DA ESQUERDA)
    # ==============================================================================
    with col_control:
        st.header("💡 Tese de Investimento")
        st.markdown("Use as ferramentas abaixo para descobrir e refinar sua estratégia.")
        
        st.subheader("Radar de Oportunidades")
        st.caption("Comece explorando os segmentos mais promissores do mercado.")
        top_3_segments = df_alignment.head(3)
        
        for index, row in top_3_segments.iterrows():
            if st.button(f"**{row['country']}** - {row['category']}", use_container_width=True, key=f"button_{index}"):
                st.session_state.selected_country = row['country']
                st.session_state.selected_category = row['category']
                st.rerun() # Força o recarregamento para atualizar os selectbox

        st.divider()

        st.subheader("Construa sua Tese")
        st.caption("Ou construa sua própria tese selecionando um país e uma categoria.")

        paises_validos = sorted(df_alignment['country'].unique())
        country_index = paises_validos.index(st.session_state.selected_country) if st.session_state.selected_country in paises_validos else 0
        st.session_state.selected_country = st.selectbox("1. Selecione um País", options=paises_validos, index=country_index, key="sb_country")

        categorias_validas = sorted(df_alignment[df_alignment['country'] == st.session_state.selected_country]['category'].unique())
        # Reseta a categoria se a seleção de país mudou e a categoria antiga não é mais válida
        if st.session_state.selected_category not in categorias_validas:
            st.session_state.selected_category = categorias_validas[0] if categorias_validas else None
        
        category_index = categorias_validas.index(st.session_state.selected_category) if st.session_state.selected_category in categorias_validas else 0
        st.session_state.selected_category = st.selectbox("2. Selecione uma Categoria", options=categorias_validas, index=category_index, key="sb_category")

    # ==============================================================================
    # PAINEL DE RESULTADOS (COLUNA DA DIREITA)
    # ==============================================================================
    with col_results:
        if st.session_state.selected_country and st.session_state.selected_category:
            st.header(f"Dossiê: {st.session_state.selected_category} em {st.session_state.selected_country}")
            
            try:
                thesis = strategy.get_investment_thesis(df_alignment, st.session_state.selected_country, st.session_state.selected_category)
                segment_data_row = df_alignment[(df_alignment['country'] == st.session_state.selected_country) & (df_alignment['category'] == st.session_state.selected_category)].iloc[0]

                # --- MUDANÇA: ORGANIZANDO OS GRÁFICOS EM COLUNAS ---
                g_col1, g_col2 = st.columns(2)
                with g_col1:
                    gauge_fig = charts.create_gauge_chart(thesis['score'])
                    st.plotly_chart(gauge_fig, use_container_width=True)
                with g_col2:
                    radar_fig = charts.create_radar_chart(segment_data_row)
                    st.plotly_chart(radar_fig, use_container_width=True)

                st.subheader("Análise do Segmento")
                for just in thesis['justifications']:
                    st.markdown(f"▪️ {just}")
                
                st.divider()
                st.subheader("Projetos Disponíveis para esta Tese")
                project_results = df_opps[(df_opps['country'] == st.session_state.selected_country) & (df_opps['category'] == st.session_state.selected_category)]
                
                if project_results.empty:
                    st.warning("Não foram encontrados projetos com créditos disponíveis para este segmento.")
                else:
                    st.dataframe(project_results[['name', 'status', 'volume_disponivel', 'opportunity_score']], hide_index=True, use_container_width=True)
            except (IndexError, KeyError):
                 st.error("Não foi possível gerar a análise para o segmento selecionado. Pode haver dados insuficientes.")
        else:
            st.header("Seu Dossiê de Investimento Aparecerá Aqui")
            st.info("Use o painel à esquerda para selecionar um segmento de mercado e ver a análise detalhada.")