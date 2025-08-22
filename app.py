"""
📊 Dashboard Interativo de Analytics - Data Science
🚀 Aplicação principal desenvolvida com Streamlit
👨‍💻 Desenvolvido por: João Silva
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import time

# Configuração da página
st.set_page_config(
    page_title="Dashboard Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Importar componentes personalizados
try:
    from components.charts import create_line_chart, create_bar_chart, create_pie_chart
    from components.filters import create_filters, apply_filters
    from components.utils import load_data, calculate_kpis
except ImportError:
    # Fallback se os componentes não estiverem disponíveis
    st.warning("⚠️ Componentes personalizados não encontrados. Usando versão básica.")

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 1rem;
        color: #666;
    }
    .chart-container {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def load_sample_data():
    """Carrega dados de exemplo para demonstração"""
    # Gerar dados sintéticos
    dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
    np.random.seed(42)
    
    data = {
        'data': dates,
        'vendas': np.random.normal(1000, 200, len(dates)) + np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 200,
        'clientes': np.random.poisson(50, len(dates)),
        'receita': np.random.normal(5000, 1000, len(dates)),
        'custo': np.random.normal(3000, 800, len(dates)),
        'regiao': np.random.choice(['Norte', 'Sul', 'Leste', 'Oeste', 'Centro'], len(dates)),
        'categoria': np.random.choice(['Eletrônicos', 'Vestuário', 'Casa', 'Esporte', 'Livros'], len(dates))
    }
    
    df = pd.DataFrame(data)
    df['lucro'] = df['receita'] - df['custo']
    df['margem'] = (df['lucro'] / df['receita']) * 100
    df['mes'] = df['data'].dt.month
    df['ano'] = df['data'].dt.year
    df['trimestre'] = df['data'].dt.quarter
    
    return df

def calculate_metrics(df):
    """Calcula métricas principais"""
    hoje = datetime.now()
    df_hoje = df[df['data'] <= hoje]
    
    metrics = {
        'total_vendas': df_hoje['vendas'].sum(),
        'total_receita': df_hoje['receita'].sum(),
        'total_lucro': df_hoje['lucro'].sum(),
        'media_margem': df_hoje['margem'].mean(),
        'total_clientes': df_hoje['clientes'].sum(),
        'vendas_hoje': df_hoje[df_hoje['data'].dt.date == hoje.date()]['vendas'].sum() if len(df_hoje[df_hoje['data'].dt.date == hoje.date()]) > 0 else 0
    }
    
    return metrics

def create_overview_page(df):
    """Cria a página de visão geral"""
    st.markdown('<h1 class="main-header">📊 Dashboard Analytics</h1>', unsafe_allow_html=True)
    
    # Métricas principais
    metrics = calculate_metrics(df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">R$ {metrics['total_receita']:,.0f}</div>
            <div class="metric-label">Receita Total</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">R$ {metrics['total_lucro']:,.0f}</div>
            <div class="metric-label">Lucro Total</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metrics['total_clientes']:,.0f}</div>
            <div class="metric-label">Total Clientes</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metrics['media_margem']:.1f}%</div>
            <div class="metric-label">Margem Média</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Gráficos principais
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3>📈 Evolução das Vendas</h3>', unsafe_allow_html=True)
        fig = px.line(
            df.groupby('data')['vendas'].sum().reset_index(),
            x='data',
            y='vendas',
            title='Vendas Diárias ao Longo do Tempo'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<h3>💰 Evolução da Receita</h3>', unsafe_allow_html=True)
        fig = px.line(
            df.groupby('data')['receita'].sum().reset_index(),
            x='data',
            y='receita',
            title='Receita Diária ao Longo do Tempo'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Análise por região
    st.markdown('<h3>🗺️ Distribuição por Região</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            df.groupby('regiao')['vendas'].sum().reset_index(),
            values='vendas',
            names='regiao',
            title='Vendas por Região'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            df.groupby('regiao')['receita'].sum().reset_index(),
            x='regiao',
            y='receita',
            title='Receita por Região'
        )
        st.plotly_chart(fig, use_container_width=True)

def create_analytics_page(df):
    """Cria a página de analytics"""
    st.markdown('<h1>📈 Analytics Avançado</h1>', unsafe_allow_html=True)
    
    # Filtros
    st.sidebar.markdown("## 🎛️ Filtros")
    regioes = st.sidebar.multiselect("Regiões", df['regiao'].unique(), default=df['regiao'].unique())
    categorias = st.sidebar.multiselect("Categorias", df['categoria'].unique(), default=df['categoria'].unique())
    data_inicio = st.sidebar.date_input("Data Início", df['data'].min())
    data_fim = st.sidebar.date_input("Data Fim", df['data'].max())
    
    # Aplicar filtros
    df_filtrado = df[
        (df['regiao'].isin(regioes)) &
        (df['categoria'].isin(categorias)) &
        (df['data'].dt.date >= data_inicio) &
        (df['data'].dt.date <= data_fim)
    ]
    
    # Estatísticas descritivas
    st.markdown('<h3>📊 Estatísticas Descritivas</h3>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Vendas**")
        st.write(f"**Média:** {df_filtrado['vendas'].mean():.2f}")
        st.write(f"**Mediana:** {df_filtrado['vendas'].median():.2f}")
        st.write(f"**Desvio Padrão:** {df_filtrado['vendas'].std():.2f}")
    
    with col2:
        st.markdown("**Receita**")
        st.write(f"**Média:** R$ {df_filtrado['receita'].mean():.2f}")
        st.write(f"**Mediana:** R$ {df_filtrado['receita'].median():.2f}")
        st.write(f"**Desvio Padrão:** R$ {df_filtrado['receita'].std():.2f}")
    
    with col3:
        st.markdown("**Margem**")
        st.write(f"**Média:** {df_filtrado['margem'].mean():.2f}%")
        st.write(f"**Mediana:** {df_filtrado['margem'].median():.2f}%")
        st.write(f"**Desvio Padrão:** {df_filtrado['margem'].std():.2f}%")
    
    st.markdown("---")
    
    # Análise temporal
    st.markdown('<h3>⏰ Análise Temporal</h3>', unsafe_allow_html=True)
    
    # Vendas por mês
    vendas_mensais = df_filtrado.groupby(['ano', 'mes'])['vendas'].sum().reset_index()
    vendas_mensais['data_mes'] = pd.to_datetime(vendas_mensais[['ano', 'mes']].assign(day=1))
    
    fig = px.line(
        vendas_mensais,
        x='data_mes',
        y='vendas',
        title='Vendas Mensais',
        markers=True
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise sazonal
    col1, col2 = st.columns(2)
    
    with col1:
        vendas_por_mes = df_filtrado.groupby('mes')['vendas'].mean().reset_index()
        fig = px.bar(
            vendas_por_mes,
            x='mes',
            y='vendas',
            title='Vendas Médias por Mês (Sazonalidade)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        vendas_por_trimestre = df_filtrado.groupby('trimestre')['vendas'].sum().reset_index()
        fig = px.pie(
            vendas_por_trimestre,
            values='vendas',
            names='trimestre',
            title='Vendas por Trimestre'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Análise de correlação
    st.markdown('<h3>🔗 Análise de Correlação</h3>', unsafe_allow_html=True)
    
    # Selecionar variáveis numéricas
    variaveis_numericas = ['vendas', 'receita', 'custo', 'lucro', 'margem']
    correlacao = df_filtrado[variaveis_numericas].corr()
    
    fig = px.imshow(
        correlacao,
        text_auto=True,
        aspect="auto",
        title="Matriz de Correlação"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise por categoria
    st.markdown('<h3>🏷️ Análise por Categoria</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        vendas_categoria = df_filtrado.groupby('categoria')['vendas'].sum().reset_index()
        fig = px.bar(
            vendas_categoria,
            x='categoria',
            y='vendas',
            title='Vendas por Categoria'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        margem_categoria = df_filtrado.groupby('categoria')['margem'].mean().reset_index()
        fig = px.bar(
            margem_categoria,
            x='categoria',
            y='margem',
            title='Margem Média por Categoria'
        )
        st.plotly_chart(fig, use_container_width=True)

def create_kpis_page(df):
    """Cria a página de KPIs"""
    st.markdown('<h1>🎯 Dashboard de KPIs</h1>', unsafe_allow_html=True)
    
    # KPIs em tempo real
    st.markdown('<h3>📊 KPIs em Tempo Real</h3>', unsafe_allow_html=True)
    
    metrics = calculate_metrics(df)
    
    # Métricas principais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Receita Total",
            value=f"R$ {metrics['total_receita']:,.0f}",
            delta=f"R$ {metrics['vendas_hoje']:,.0f} (hoje)"
        )
    
    with col2:
        st.metric(
            label="Lucro Total",
            value=f"R$ {metrics['total_lucro']:,.0f}",
            delta=f"{metrics['media_margem']:.1f}% (margem)"
        )
    
    with col3:
        st.metric(
            label="Total Clientes",
            value=f"{metrics['total_clientes']:,.0f}",
            delta=f"{metrics['total_clientes']/len(df):.0f} (média/dia)"
        )
    
    st.markdown("---")
    
    # Comparação de períodos
    st.markdown('<h3>📅 Comparação de Períodos</h3>', unsafe_allow_html=True)
    
    # Selecionar período de comparação
    col1, col2 = st.columns(2)
    
    with col1:
        periodo_atual = st.selectbox(
            "Período Atual",
            ["Último Mês", "Último Trimestre", "Último Ano"],
            index=0
        )
    
    with col2:
        periodo_anterior = st.selectbox(
            "Período Anterior",
            ["Mês Anterior", "Trimestre Anterior", "Ano Anterior"],
            index=0
        )
    
    # Calcular métricas para os períodos
    hoje = datetime.now()
    
    if periodo_atual == "Último Mês":
        inicio_atual = hoje - timedelta(days=30)
        fim_atual = hoje
    elif periodo_atual == "Último Trimestre":
        inicio_atual = hoje - timedelta(days=90)
        fim_atual = hoje
    else:  # Último Ano
        inicio_atual = hoje - timedelta(days=365)
        fim_atual = hoje
    
    # Aplicar filtros de período
    df_atual = df[(df['data'] >= inicio_atual) & (df['data'] <= fim_atual)]
    
    # Calcular métricas
    vendas_atual = df_atual['vendas'].sum()
    receita_atual = df_atual['receita'].sum()
    lucro_atual = df_atual['lucro'].sum()
    
    # Exibir comparação
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Vendas (Período Atual)",
            value=f"{vendas_atual:,.0f}",
            delta=f"R$ {receita_atual:,.0f} (receita)"
        )
    
    with col2:
        st.metric(
            label="Receita (Período Atual)",
            value=f"R$ {receita_atual:,.0f}",
            delta=f"R$ {lucro_atual:,.0f} (lucro)"
        )
    
    with col3:
        margem_atual = (lucro_atual / receita_atual * 100) if receita_atual > 0 else 0
        st.metric(
            label="Margem (Período Atual)",
            value=f"{margem_atual:.1f}%",
            delta=f"{len(df_atual)} dias"
        )
    
    st.markdown("---")
    
    # Gráfico de tendências dos KPIs
    st.markdown('<h3>📈 Tendências dos KPIs</h3>', unsafe_allow_html=True)
    
    # Agrupar dados por semana para suavizar
    df_semanal = df_atual.groupby(pd.Grouper(key='data', freq='W')).agg({
        'vendas': 'sum',
        'receita': 'sum',
        'lucro': 'sum'
    }).reset_index()
    
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=('Vendas Semanais', 'Receita Semanal', 'Lucro Semanal'),
        vertical_spacing=0.1
    )
    
    fig.add_trace(
        go.Scatter(x=df_semanal['data'], y=df_semanal['vendas'], name='Vendas'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=df_semanal['data'], y=df_semanal['receita'], name='Receita'),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=df_semanal['data'], y=df_semanal['lucro'], name='Lucro'),
        row=3, col=1
    )
    
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def create_settings_page():
    """Cria a página de configurações"""
    st.markdown('<h1>⚙️ Configurações</h1>', unsafe_allow_html=True)
    
    # Configurações do dashboard
    st.markdown('<h3>🎨 Configurações do Dashboard</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        tema = st.selectbox("Tema", ["Claro", "Escuro", "Automático"])
        layout = st.selectbox("Layout", ["Wide", "Centered"])
        sidebar_state = st.selectbox("Estado da Sidebar", ["Expanded", "Collapsed"])
    
    with col2:
        atualizacao_auto = st.checkbox("Atualização Automática", value=True)
        intervalo_atualizacao = st.slider("Intervalo de Atualização (min)", 1, 60, 5)
        notificacoes = st.checkbox("Notificações", value=True)
    
    # Configurações de dados
    st.markdown('<h3>📊 Configurações de Dados</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fonte_dados = st.selectbox("Fonte de Dados", ["CSV", "Database", "API", "Excel"])
        cache_dados = st.checkbox("Cache de Dados", value=True)
        tempo_cache = st.slider("Tempo de Cache (min)", 1, 1440, 60)
    
    with col2:
        formato_data = st.selectbox("Formato de Data", ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
        fuso_horario = st.selectbox("Fuso Horário", ["UTC", "America/Sao_Paulo", "Europe/London"])
        idioma = st.selectbox("Idioma", ["Português", "English", "Español"])
    
    # Configurações de usuário
    st.markdown('<h3>👤 Configurações de Usuário</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        nome_usuario = st.text_input("Nome do Usuário", value="João Silva")
        email = st.text_input("Email", value="joao.silva@email.com")
        empresa = st.text_input("Empresa", value="Data Science Corp")
    
    with col2:
        cargo = st.text_input("Cargo", value="Data Scientist")
        departamento = st.selectbox("Departamento", ["TI", "Marketing", "Vendas", "Financeiro", "RH"])
        nivel_acesso = st.selectbox("Nível de Acesso", ["Admin", "Manager", "Analyst", "Viewer"])
    
    # Botões de ação
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Salvar Configurações"):
            st.success("✅ Configurações salvas com sucesso!")
    
    with col2:
        if st.button("🔄 Restaurar Padrões"):
            st.info("🔄 Configurações restauradas para os valores padrão")
    
    with col3:
        if st.button("📤 Exportar Configurações"):
            st.info("📤 Configurações exportadas para config.json")

def main():
    """Função principal da aplicação"""
    
    # Sidebar
    st.sidebar.markdown("## 📊 Dashboard Analytics")
    st.sidebar.markdown("### 👨‍💻 Desenvolvido por João Silva")
    
    # Menu de navegação
    pagina = st.sidebar.selectbox(
        "Navegação",
        ["📊 Overview", "📈 Analytics", "🎯 KPIs", "⚙️ Settings"]
    )
    
    # Carregar dados
    df = load_sample_data()
    
    # Navegação entre páginas
    if pagina == "📊 Overview":
        create_overview_page(df)
    elif pagina == "📈 Analytics":
        create_analytics_page(df)
    elif pagina == "🎯 KPIs":
        create_kpis_page(df)
    elif pagina == "⚙️ Settings":
        create_settings_page()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            📊 Dashboard Analytics | 🚀 Desenvolvido com Streamlit | 👨‍💻 João Silva
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
