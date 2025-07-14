import streamlit as st
import pandas as pd
import os
from pathlib import Path

def render_data_preview():
    """
    Renderiza a visualização das primeiras 20 linhas de cada DataFrame da pasta data.
    """
    st.header("📋 Visualização dos Dados")
    st.write("Esta seção mostra as primeiras 20 linhas de cada arquivo CSV da pasta data.")
    
    # Caminho para a pasta data
    data_dir = Path(__file__).resolve().parent.parent.parent / "data"
    
    # Obter todos os arquivos CSV da pasta data
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    if not csv_files:
        st.warning("Nenhum arquivo CSV encontrado na pasta data.")
        return
    
    # Criar abas para cada arquivo
    tabs = st.tabs([f"📄 {file}" for file in csv_files])
    
    for i, csv_file in enumerate(csv_files):
        with tabs[i]:
            try:
                # Carregar o DataFrame
                file_path = data_dir / csv_file
                df = pd.read_csv(file_path)
                
                # Informações básicas do arquivo
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total de Linhas", len(df))
                with col2:
                    st.metric("Total de Colunas", len(df.columns))
                with col3:
                    file_size = os.path.getsize(file_path)
                    if file_size > 1024 * 1024:
                        size_str = f"{file_size / (1024 * 1024):.1f} MB"
                    elif file_size > 1024:
                        size_str = f"{file_size / 1024:.1f} KB"
                    else:
                        size_str = f"{file_size} bytes"
                    st.metric("Tamanho do Arquivo", size_str)
                
                st.subheader(f"Primeiras 20 linhas - {csv_file}")
                
                # Mostrar as primeiras 20 linhas
                preview_df = df.head(20)
                st.dataframe(preview_df, use_container_width=True)
                
                # Mostrar informações sobre as colunas
                st.subheader("Informações das Colunas")
                
                # Criar DataFrame com informações das colunas
                column_info = []
                for col in df.columns:
                    column_info.append({
                        'Coluna': col,
                        'Tipo': str(df[col].dtype),
                        'Valores Nulos': df[col].isnull().sum(),
                        'Valores Únicos': df[col].nunique()
                    })
                
                column_df = pd.DataFrame(column_info)
                st.dataframe(column_df, use_container_width=True)
                
                # Opção para mostrar estatísticas descritivas para colunas numéricas
                numeric_columns = df.select_dtypes(include=['number']).columns
                if len(numeric_columns) > 0:
                    st.subheader("Estatísticas Descritivas (Colunas Numéricas)")
                    st.dataframe(df[numeric_columns].describe(), use_container_width=True)
                
            except Exception as e:
                st.error(f"Erro ao carregar o arquivo {csv_file}: {str(e)}")
                st.exception(e) 