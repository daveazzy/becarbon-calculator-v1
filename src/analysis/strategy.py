import pandas as pd

def get_investment_thesis(df_alignment: pd.DataFrame, country: str, category: str):
    """
    Gera um dossiê de investimento para uma combinação de país e categoria.
    """
    try:
        # Encontra a linha específica para a combinação selecionada
        segment_data = df_alignment[
            (df_alignment['country'] == country) & 
            (df_alignment['category'] == category)
        ].iloc[0]

        score = segment_data['alignment_score']
        
        # --- CORREÇÃO: Usando as colunas originais e mais claras para as justificativas ---
        justifications = [
            f"**Participação de Mercado:** Este segmento representa **{segment_data['market_share']:.2%}** do volume total de aposentadorias no período.",
            f"**Tendência de Crescimento:** O volume deste segmento mostra uma tendência de crescimento com um coeficiente de **{int(segment_data['growth_trend']):,}**.",
            f"**Perfil de Idade:** A idade mediana dos créditos neste segmento é de **{segment_data['idade_na_aposentadoria']:.1f} anos**."
        ]
        
        return {"score": score, "justifications": justifications}

    except IndexError:
        # Retorna um valor padrão se a combinação não for encontrada, evitando que o app quebre.
        return {
            "score": 0,
            "justifications": ["Não há dados suficientes para analisar este segmento específico."]
        }