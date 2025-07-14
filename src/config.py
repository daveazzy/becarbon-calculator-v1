from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Arquivos para a Calculadora / Consultor Estratégico
ALIGNMENT_INDEX_FILE = DATA_DIR / "indice_alinhamento_segmentos.csv"
OPPORTUNITIES_SCORED_FILE = DATA_DIR / "relatorio_oportunidades_com_score.csv"

# Arquivos para o Dashboard
COUNTRY_PROFILE_FILE = DATA_DIR / "perfil_mercado_por_pais.csv"
CATEGORY_PROFILE_FILE = DATA_DIR / "perfil_mercado_por_categoria.csv"
TRANSACTIONS_FILE = DATA_DIR / "dados_limpos_para_regressao.csv" # Usado pelo Heatmap