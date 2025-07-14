# src/components/academic_context.py (VERSÃO FINAL E PERSUASIVA)

import streamlit as st
import pandas as pd

def render_academic_context():
    """
    Renderiza a aba de Contexto Acadêmico, explicando a jornada completa do projeto
    de forma didática e persuasiva, conectando-o a conceitos avançados.
    """
    st.header("🎓 Jornada Analítica: Da Hipótese à Estratégia")

    st.markdown(
        """
        Este projeto documenta o ciclo de vida completo de uma solução de dados, refletindo os desafios e as decisões
        estratégicas do mundo real. A seguir, cada fase da análise é apresentada, destacando a metodologia
        estatística aplicada e o valor gerado em cada etapa.
        """
    )
    st.divider()

    # --- FASE 1: TESTE DE HIPÓTESE INICIAL ---
    with st.expander("Fase 1: Testando a Hipótese Inicial (Idade vs. Volume)"):
        st.subheader("Pergunta de Partida")
        st.markdown("A hipótese inicial era que a idade de um crédito poderia influenciar o volume de sua aposentadoria. Testamos a correlação linear entre essas duas variáveis.")
        st.subheader("Resultados e Conclusão")
        st.warning(
            "**Hipótese Rejeitada (R² ≈ 0.11%).** A análise de regressão linear provou que a idade, sozinha, não é uma variável preditiva útil para o volume, forçando um pivô na estratégia do projeto."
        )
        st.subheader("Conexão com a Disciplina")
        st.info("**Tópicos Aplicados:** `Teste de Hipóteses`, `Análise de Regressão Linear`, `Interpretação de R-Quadrado`.")
    
    # --- FASE 2: ANÁLISE DESCRITIVA E PERFIL DE MERCADO ---
    with st.expander("Fase 2: Da Análise Descritiva à Inteligência de Mercado"):
        st.subheader("Nova Abordagem")
        st.markdown("Com a falha do modelo preditivo simples, o foco mudou para a análise descritiva. O objetivo passou a ser caracterizar e comparar os diferentes segmentos de mercado (países e categorias).")
        st.subheader("Resultados e Conclusão")
        st.success(
            "**Perfis de Mercado Gerados.** Ao calcular métricas como **idade mediana**, **vintage mais comum (moda)** e **tamanho médio da transação**, criamos perfis detalhados que revelaram as diferentes dinâmicas e preferências de cada nicho."
        )
        st.subheader("Conexão com a Disciplina")
        st.info("**Tópicos Aplicados:** `Estatística Descritiva`, `Medidas de Tendência Central e Dispersão`, `Análise de Frequências`.")

    # --- FASE 3: O CONSULTOR ESTRATÉGICO ---
    with st.expander("Fase 3: O Consultor Estratégico (Índice de Alinhamento)", expanded=True):
        st.subheader("O Desafio Final: Como Recomendar Ações?")
        st.markdown(
            "Um dashboard descritivo é útil, mas uma ferramenta verdadeiramente valiosa para uma startup deve **guiar a decisão** do cliente. O desafio era criar uma métrica que pudesse, de forma objetiva, ranquear e recomendar os segmentos de mercado mais promissores."
        )
        
        st.subheader("Metodologia: Análise de Decisão Multicritério")
        st.markdown(
            """
            Para resolver isso, foi desenvolvido o **"Índice de Alinhamento de Mercado"**, um indicador composto que transforma dados complexos em um único score (0-100). A criação deste índice é uma aplicação direta de modelagem estatística avançada:

            1.  **Engenharia de Features:** Para cada segmento (País + Categoria), calculamos três fatores-chave:
                * **Market Share:** A participação de mercado histórica.
                * **Tendência de Crescimento:** O coeficiente de uma **regressão linear** aplicada à série histórica de volume de cada segmento, medindo sua aceleração.
                * **Perfil de Qualidade:** A idade mediana dos créditos do segmento.

            2.  **Normalização:** Os fatores foram normalizados (Min-Max Scaling) para permitir uma comparação justa entre variáveis de escalas diferentes.

            3.  **Modelo Ponderado:** O índice final é uma média ponderada desses fatores, representando um modelo de **Análise de Decisão Multicritério (MCDA)**.
            """
        )