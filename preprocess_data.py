import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path

def run_preprocessing():
    """
    Executa todo o pipeline de processamento de dados, desde os arquivos brutos
    até a criação de todos os arquivos CSV finais necessários para a aplicação Streamlit.
    """
    print("--- INICIANDO PRÉ-PROCESSAMENTO COMPLETO DOS DADOS ---")

    # --- Configuração de Caminhos ---
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data"
    
    # Garante que a pasta 'data' exista
    DATA_DIR.mkdir(exist_ok=True)
    
    RAW_CREDITS_FILE = DATA_DIR / "credits.csv"
    RAW_PROJECTS_FILE = DATA_DIR / "projects.csv"

    # --- 1. Carregar e Preparar Dados Brutos ---
    print("\n[1/5] Carregando e limpando dados brutos...")
    try:
        credits_df = pd.read_csv(RAW_CREDITS_FILE)
        projects_df = pd.read_csv(RAW_PROJECTS_FILE)
    except FileNotFoundError as e:
        print(f"ERRO: Arquivo de dados brutos não encontrado: {e.filename}")
        print("Por favor, garanta que 'credits.csv' e 'projects.csv' estão na pasta 'data/'.")
        return

    merged_df = pd.merge(credits_df, projects_df, on='project_id')
    merged_df['transaction_date'] = pd.to_datetime(merged_df['transaction_date'], errors='coerce')
    merged_df.dropna(subset=['transaction_date'], inplace=True)
    merged_df['transaction_year'] = merged_df['transaction_date'].dt.year
    df_filtrado = merged_df[merged_df['transaction_year'].between(2016, 2024)].copy()
    
    # Salva o arquivo de transações limpas (usado pelo heatmap do dashboard)
    df_aposentados = df_filtrado[df_filtrado['transaction_type'] == 'retirement'].copy()
    df_aposentados['idade_na_aposentadoria'] = df_aposentados['transaction_year'] - df_aposentados['vintage']
    colunas_transacoes = ['country', 'category', 'quantity', 'transaction_year', 'idade_na_aposentadoria']
    df_transacoes_limpas = df_aposentados[colunas_transacoes]
    df_transacoes_limpas.to_csv(DATA_DIR / "dados_limpos_para_regressao.csv", index=False)
    print("-> 'dados_limpos_para_regressao.csv' gerado.")

    # --- 2. Gerar Perfis de Mercado (para o Dashboard) ---
    print("\n[2/5] Gerando perfis de mercado...")
    # Perfil por País
    top_paises = df_transacoes_limpas.groupby('country')['quantity'].sum().nlargest(10).index.tolist()
    # (O resto da lógica de perfil está dentro dos componentes, então não precisamos salvar esses arquivos)

    # --- 3. Calcular o Índice de Alinhamento de Mercado ---
    print("\n[3/5] Calculando o 'Índice de Alinhamento de Mercado'...")
    total_volume_geral = df_transacoes_limpas['quantity'].sum()
    df_segments = df_transacoes_limpas.groupby(['country', 'category'])['quantity'].sum().reset_index()
    df_segments.rename(columns={'quantity': 'total_volume'}, inplace=True)
    df_segments['market_share'] = df_segments['total_volume'] / total_volume_geral

    median_age = df_transacoes_limpas.groupby(['country', 'category'])['idade_na_aposentadoria'].median().reset_index()
    df_segments = pd.merge(df_segments, median_age, on=['country', 'category'])

    def calculate_growth_slope(group):
        if len(group['transaction_year'].unique()) < 3: return 0
        yearly_data = group.groupby('transaction_year')['quantity'].sum().reset_index()
        model = LinearRegression()
        model.fit(yearly_data[['transaction_year']], yearly_data['quantity'])
        return model.coef_[0]

    growth_trends = df_transacoes_limpas.groupby(['country', 'category']).apply(calculate_growth_slope).reset_index(name='growth_trend')
    df_segments = pd.merge(df_segments, growth_trends, on=['country', 'category'])

    scaler = MinMaxScaler()
    df_segments[['share_norm', 'growth_norm', 'age_norm']] = scaler.fit_transform(
        df_segments[['market_share', 'growth_trend', 'idade_na_aposentadoria']]
    )
    df_segments['age_norm'] = 1 - df_segments['age_norm']

    w_share, w_growth, w_age = 0.40, 0.40, 0.20
    df_segments['alignment_score'] = (
        df_segments['share_norm'] * w_share +
        df_segments['growth_norm'] * w_growth +
        df_segments['age_norm'] * w_age
    ) * 100
    
    df_segments.to_csv(DATA_DIR / "indice_alinhamento_segmentos.csv", index=False)
    print("-> 'indice_alinhamento_segmentos.csv' gerado com todas as colunas.")

    # --- 4. Calcular o Relatório de Oportunidades com Score ---
    print("\n[4/5] Calculando o 'Score de Oportunidade' para cada projeto...")
    total_emitido = df_filtrado[df_filtrado['transaction_type'] == 'issuance'].groupby('project_id')['quantity'].sum()
    total_aposentado = df_filtrado[df_filtrado['transaction_type'] == 'retirement'].groupby('project_id')['quantity'].sum()
    df_balanco = pd.DataFrame({'total_emitido': total_emitido, 'total_aposentado': total_aposentado}).fillna(0)
    df_balanco['volume_disponivel'] = df_balanco['total_emitido'] - df_balanco['total_aposentado']
    
    metadados = df_filtrado[['project_id', 'name', 'country', 'category', 'registry', 'status', 'vintage']].drop_duplicates(subset='project_id')
    df_opps = pd.merge(df_balanco, metadados, on='project_id')
    df_opps = df_opps[df_opps['volume_disponivel'] > 0]

    df_opps['idade_estimada'] = 2025 - df_opps['vintage']
    df_opps['idade_estimada'].fillna(df_opps['idade_estimada'].median(), inplace=True)
    
    status_map = {'registered': 1.0, 'completed': 0.5, 'on-hold': 0.1}
    df_opps['fator_status'] = df_opps['status'].map(status_map).fillna(0.0)
    
    df_opps[['fator_volume_norm']] = scaler.fit_transform(df_opps[['volume_disponivel']])
    df_opps[['idade_norm']] = scaler.fit_transform(df_opps[['idade_estimada']])
    df_opps['fator_idade_norm'] = 1 - df_opps['idade_norm']
    
    peso_idade, peso_volume, peso_status = 0.4, 0.3, 0.3
    df_opps['opportunity_score'] = (
        df_opps['fator_idade_norm'] * peso_idade +
        df_opps['fator_volume_norm'] * peso_volume +
        df_opps['fator_status'] * peso_status
    )
    
    df_opps.to_csv(DATA_DIR / "relatorio_oportunidades_com_score.csv", index=False)
    print("-> 'relatorio_oportunidades_com_score.csv' gerado.")

    # --- 5. Gerar arquivos de perfil para o dashboard
    print("\n[5/5] Gerando arquivos de perfil para o dashboard...")
    # Os componentes do dashboard podem fazer isso em tempo real, mas vamos pré-calcular para consistência.
    top_10_paises = df_transacoes_limpas.groupby('country')['quantity'].sum().nlargest(10).index.tolist()
    #... (lógica de perfil pode ser adicionada aqui se necessário, mas os componentes atuais do dashboard já a fazem)
    # Por agora, vamos garantir que o dashboard funcione. O erro era nele.

    print("\n--- PRÉ-PROCESSAMENTO CONCLUÍDO COM SUCESSO ---")

if __name__ == "__main__":
    run_preprocessing()