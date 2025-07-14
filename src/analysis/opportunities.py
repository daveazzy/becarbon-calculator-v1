import pandas as pd
from typing import List

def filter_opportunities(
    df: pd.DataFrame,
    countries: List[str],
    categories: List[str],
    min_volume: int
) -> pd.DataFrame:
    """
    Filtra o DataFrame de oportunidades com base nos critérios selecionados pelo usuário.

    Args:
        df (pd.DataFrame): O DataFrame completo de oportunidades.
        countries (List[str]): Uma lista de países para filtrar. Se vazia, nenhum filtro de país é aplicado.
        categories (List[str]): Uma lista de categorias para filtrar. Se vazia, nenhum filtro de categoria é aplicado.
        min_volume (int): O volume mínimo de créditos disponíveis que um projeto deve ter.

    Returns:
        pd.DataFrame: Um novo DataFrame contendo apenas as oportunidades que correspondem aos filtros.
    """
    # Começa com uma cópia para garantir que o DataFrame original não seja modificado.
    # Este é um princípio de programação funcional que evita efeitos colaterais.
    filtered_df = df.copy()

    # Aplica o filtro de país, se algum país foi selecionado
    if countries:
        filtered_df = filtered_df[filtered_df['country'].isin(countries)]

    # Aplica o filtro de categoria, se alguma categoria foi selecionada
    if categories:
        filtered_df = filtered_df[filtered_df['category'].isin(categories)]

    # Aplica o filtro de volume mínimo
    # Este filtro é sempre aplicado, com base no valor do slider.
    filtered_df = filtered_df[filtered_df['volume_disponivel'] >= min_volume]

    return filtered_df