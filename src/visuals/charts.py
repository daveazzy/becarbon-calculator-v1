import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Definimos uma paleta de cores padrão para usar nos gráficos
DEFAULT_COLOR_PALETTE = px.colors.sequential.Teal

def create_bar_chart(df: pd.DataFrame, x_axis: str, y_axis: str, title: str) -> go.Figure:
    """
    Cria e retorna um gráfico de barras interativo usando o Plotly Express.

    Args:
        df (pd.DataFrame): O DataFrame contendo os dados.
        x_axis (str): O nome da coluna para o eixo X.
        y_axis (str): O nome da coluna para o eixo Y.
        title (str): O título do gráfico.

    Returns:
        go.Figure: O objeto do gráfico de barras.
    """
    fig = px.bar(
        df,
        x=x_axis,
        y=y_axis,
        title=title,
        color_discrete_sequence=DEFAULT_COLOR_PALETTE,
        text_auto='.2s'  # type: ignore # MUDANÇA: Ignora o falso positivo do Pylance
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(
        xaxis_title=None,
        yaxis_title=y_axis.replace("_", " ").title(),
        title_x=0.5
    )
    return fig

def create_heatmap(df_analise: pd.DataFrame, top_countries: list, top_categories: list) -> go.Figure:
    """
    Cria e retorna um mapa de calor (heatmap) do volume por país e categoria.

    Args:
        df_analise (pd.DataFrame): O DataFrame principal da análise.
        top_countries (list): Lista dos principais países a serem exibidos.
        top_categories (list): Lista das principais categorias a serem exibidas.

    Returns:
        go.Figure: O objeto do mapa de calor.
    """
    df_focado = df_analise[
        df_analise['country'].isin(top_countries) &
        df_analise['category'].isin(top_categories)
    ]

    pivot_table = df_focado.pivot_table(
        index='country',
        columns='category',
        values='quantity',
        aggfunc='sum',
        fill_value=0
    )
    
    if not pivot_table.empty:
        pivot_table = pivot_table.loc[top_countries].reindex(columns=top_categories)

    fig = px.imshow(
        pivot_table / 1_000_000,
        text_auto=".1f", # type: ignore # MUDANÇA: Ignora o falso positivo do Pylance
        aspect="auto",
        color_continuous_scale="YlGnBu",
        title='Volume Aposentado (em Milhões) por País e Categoria'
    )
    fig.update_layout(
        xaxis_title='Categoria do Projeto',
        yaxis_title='País',
        title_x=0.5
    )
    return fig

def create_opportunity_scatter_plot(df: pd.DataFrame) -> go.Figure:
    """
    Cria um gráfico de dispersão interativo para visualizar as oportunidades.

    Args:
        df (pd.DataFrame): DataFrame com as oportunidades já filtradas e com score.

    Returns:
        go.Figure: O objeto do gráfico de dispersão.
    """
    if df.empty:
        return go.Figure()

    fig = px.scatter(
        df,
        x="idade_estimada",
        y="volume_disponivel",
        size="volume_disponivel",
        color="opportunity_score",
        hover_name="name",
        color_continuous_scale=px.colors.sequential.Viridis,
        size_max=60, # Define o tamanho máximo das bolhas
        custom_data=['country', 'category', 'vintage', 'opportunity_score'] # Dados extras para o hover
    )
    
    fig.update_traces(
        hovertemplate="<br>".join([
            "<b>%{customdata[0]}</b> - %{hovertext}",
            "<b>Categoria:</b> %{customdata[1]}",
            "<b>Vintage:</b> %{customdata[2]}",
            "<b>Volume Disponível:</b> %{y:,.0f}",
            "<b>Idade Estimada:</b> %{x:.0f} anos",
            "<b>Score:</b> %{customdata[3]:.3f}"
        ])
    )

    fig.update_layout(
        title="Mapa Interativo de Oportunidades",
        xaxis_title="Idade Estimada do Projeto (anos)",
        yaxis_title="Volume de Créditos Disponíveis",
        coloraxis_colorbar=dict(title="Score"),
        title_x=0.5
    )
    return fig

def create_gauge_chart(score: float) -> go.Figure:
    """
    Cria um gráfico de medidor (gauge) para exibir um score de 0 a 100.
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Índice de Alinhamento de Mercado"},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#0d3b66"}, # Cor da barra principal
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#FFADAD'}, # Vermelho
                {'range': [40, 70], 'color': '#FDFFB6'}, # Amarelo
                {'range': [70, 100], 'color': '#CAFFBF'}  # Verde
            ],
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
    return fig

def create_radar_chart(segment_data: pd.Series) -> go.Figure:
    """
    Cria um gráfico de radar para visualizar os fatores de um segmento.
    
   Args:
    segment_data (pd.Series): Uma única linha do DataFrame de alinhamento.

    Returns:
        go.Figure: O objeto do gráfico de radar estilizado.
    """
    radar_values = [
        segment_data['share_norm'] * 100,
        segment_data['growth_norm'] * 100,
        (1 - segment_data['age_norm']) * 100
    ]
    radar_labels = ['Participação<br>Mercado', 'Tendência<br>Crescimento', 'Qualidade<br>Recente']

    fig = go.Figure(data=[go.Scatterpolar(
        r=radar_values,
        theta=radar_labels,
        fill='toself',
        name='Perfil do Segmento',
        line_color='#4a90a4',  # Azul mais suave e elegante
        fillcolor='rgba(74, 144, 164, 0.2)', # Preenchimento mais sutil
        line_width=2
    )])

    fig.update_layout(
        polar=dict(
            bgcolor='rgba(40, 44, 52, 0.8)',  # Fundo escuro suave para o círculo do radar
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='rgba(255, 255, 255, 0.3)', # Linhas de grade brancas mais visíveis
                linecolor='rgba(255, 255, 255, 0.5)', # Eixo radial branco mais visível
                tickfont=dict(color='white', size=16) # Números em branco maiores
            ),
            angularaxis=dict(
                linecolor='rgba(255, 255, 255, 0.5)', # Eixos angulares brancos mais visíveis
                tickfont=dict(color='white', size=12) # Labels menores para melhor responsividade
            )
        ),
        showlegend=False,
        height=350,
        margin=dict(l=80, r=80, t=60, b=60),
        autosize=True,  # Permite redimensionamento automático
        title={
            'text': "Perfil de Alinhamento do Segmento",
            'y':0.92,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(color='white', size=18) # Título menor para responsividade
        },
        paper_bgcolor='rgba(0,0,0,0)',  # Fundo completamente transparente
        plot_bgcolor='rgba(0,0,0,0)',   # Área do plot transparente
        font=dict(size=12)  # Fonte padrão menor para melhor adaptação
    )

    return fig