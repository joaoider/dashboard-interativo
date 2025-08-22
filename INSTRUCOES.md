# 📋 Instruções de Uso - Dashboard Interativo

## 🚀 **Como Usar o Dashboard**

### **1. Execução Local**
```bash
# Navegue para o diretório
cd dashboard-interativo

# Instale as dependências
pip install -r requirements.txt

# Execute o dashboard
streamlit run app.py
```

### **2. Acesse no Navegador**
```
http://localhost:8501
```

---

## 🎨 **Personalização do Dashboard**

### **📊 Alterando as Cores**
Edite o arquivo `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF6B6B"        # Cor principal
backgroundColor = "#FFFFFF"      # Cor de fundo
secondaryBackgroundColor = "#F8F9FA"  # Cor secundária
textColor = "#2C3E50"           # Cor do texto
```

### **🔧 Modificando o CSS**
Edite o arquivo `app.py` na seção de CSS:
```python
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF6B6B;  # Altere esta cor
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #F8F9FA;  # Altere esta cor
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF6B6B;  # Altere esta cor
    }
</style>
""", unsafe_allow_html=True)
```

---

## 📊 **Adicionando Novas Visualizações**

### **📈 Criando um Novo Gráfico**
```python
def create_custom_chart(df):
    """Cria um gráfico personalizado"""
    fig = px.scatter(
        df,
        x='coluna_x',
        y='coluna_y',
        color='categoria',
        size='valor',
        title='Meu Gráfico Personalizado'
    )
    
    # Personalizar layout
    fig.update_layout(
        title_font_size=20,
        showlegend=True,
        height=500
    )
    
    return fig

# Usar na página
st.plotly_chart(create_custom_chart(df), use_container_width=True)
```

### **🎛️ Adicionando Novos Filtros**
```python
# Na sidebar
st.sidebar.markdown("## 🎛️ Filtros Avançados")

# Filtro de texto
busca = st.sidebar.text_input("Buscar por nome", "")

# Filtro de slider
faixa_valor = st.sidebar.slider(
    "Faixa de Valor",
    min_value=float(df['valor'].min()),
    max_value=float(df['valor'].max()),
    value=(float(df['valor'].min()), float(df['valor'].max()))
)

# Aplicar filtros
df_filtrado = df[
    (df['nome'].str.contains(busca, case=False)) &
    (df['valor'].between(faixa_valor[0], faixa_valor[1]))
]
```

---

## 📱 **Responsividade e Mobile**

### **🎯 Otimizando para Mobile**
```python
# Detectar se é mobile
is_mobile = st.checkbox("📱 Modo Mobile")

if is_mobile:
    # Layout em coluna única
    st.markdown('<h3>📊 Métricas</h3>', unsafe_allow_html=True)
    st.metric("Vendas", "R$ 1.000")
    st.metric("Receita", "R$ 5.000")
else:
    # Layout em múltiplas colunas
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Vendas", "R$ 1.000")
    with col2:
        st.metric("Receita", "R$ 5.000")
```

---

## 🔄 **Atualização Automática de Dados**

### **⏰ Configurando Atualização**
```python
# Atualização automática a cada 5 minutos
if 'counter' not in st.session_state:
    st.session_state.counter = 0

# Incrementar contador
st.session_state.counter += 1

# Atualizar dados a cada 5 minutos (300 segundos)
if st.session_state.counter % 300 == 0:
    st.rerun()

# Mostrar tempo até próxima atualização
tempo_restante = 300 - (st.session_state.counter % 300)
st.sidebar.info(f"🔄 Próxima atualização em {tempo_restante//60}:{tempo_restante%60:02d}")
```

---

## 📊 **Conectando com Dados Reais**

### **🗄️ Conexão com Banco de Dados**
```python
import psycopg2
import sqlalchemy

def connect_database():
    """Conecta com banco de dados PostgreSQL"""
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="dashboard",
            user="usuario",
            password="senha"
        )
        return connection
    except Exception as e:
        st.error(f"Erro na conexão: {e}")
        return None

def load_real_data():
    """Carrega dados reais do banco"""
    conn = connect_database()
    if conn:
        query = "SELECT * FROM vendas WHERE data >= CURRENT_DATE - INTERVAL '30 days'"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    return None
```

### **📡 Conexão com API**
```python
import requests

def fetch_api_data():
    """Busca dados de uma API externa"""
    try:
        response = requests.get('https://api.exemplo.com/dados')
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data)
        else:
            st.error(f"Erro na API: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Erro na requisição: {e}")
        return None
```

---

## 🚀 **Deploy em Produção**

### **☁️ Streamlit Cloud**
1. **Conecte seu repositório GitHub**
2. **Configure as variáveis de ambiente**
3. **Deploy automático a cada push**

### **🐳 Docker**
```bash
# Construir imagem
docker build -t dashboard-analytics .

# Executar container
docker run -p 8501:8501 dashboard-analytics

# Com Docker Compose
docker-compose up -d
```

---

## 🔧 **Troubleshooting**

### **❌ Erros Comuns**

#### **Erro: "Module not found"**
```bash
# Solução: Instalar dependências
pip install -r requirements.txt

# Ou criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

#### **Erro: "Port already in use"**
```bash
# Solução: Usar porta diferente
streamlit run app.py --server.port 8502

# Ou matar processo na porta 8501
lsof -ti:8501 | xargs kill -9  # Linux/Mac
netstat -ano | findstr :8501   # Windows
```

#### **Erro: "Memory issues"**
```python
# Solução: Otimizar carregamento de dados
@st.cache_data
def load_data():
    """Cache dos dados para melhor performance"""
    return pd.read_csv('dados.csv')

# Usar cache
df = load_data()
```

---

## 📈 **Métricas e Analytics**

### **📊 Adicionando Google Analytics**
```python
# No início do app.py
st.markdown("""
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
""", unsafe_allow_html=True)
```

### **📱 Tracking de Usuários**
```python
# Rastrear ações do usuário
def track_user_action(action, details=""):
    """Rastreia ações do usuário"""
    st.session_state.user_actions = st.session_state.get('user_actions', [])
    st.session_state.user_actions.append({
        'action': action,
        'details': details,
        'timestamp': datetime.now().isoformat()
    })

# Usar em botões
if st.button("📊 Gerar Relatório"):
    track_user_action("gerar_relatorio", "relatorio_vendas")
    # ... resto do código
```

---

## 🎨 **Temas e Estilos**

### **🌙 Modo Escuro**
```python
# Adicionar toggle para modo escuro
dark_mode = st.sidebar.checkbox("🌙 Modo Escuro")

if dark_mode:
    st.markdown("""
    <style>
        .stApp {
            background-color: #1a1a1a;
            color: #ffffff;
        }
        .metric-card {
            background-color: #2d2d2d;
            color: #ffffff;
        }
    </style>
    """, unsafe_allow_html=True)
```

### **🎨 Cores Personalizadas**
```python
# Definir paleta de cores
COLORS = {
    'primary': '#FF6B6B',
    'secondary': '#4ECDC4',
    'accent': '#45B7D1',
    'warning': '#FFA07A',
    'success': '#98D8C8'
}

# Usar nas visualizações
fig = px.bar(df, x='categoria', y='valor')
fig.update_traces(marker_color=COLORS['primary'])
```

---

## 📚 **Recursos Adicionais**

### **🔗 Links Úteis**
- [Documentação Streamlit](https://docs.streamlit.io/)
- [Plotly Express](https://plotly.com/python/plotly-express/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Streamlit Components](https://github.com/streamlit/streamlit/wiki/Third-party-components)

### **📖 Livros Recomendados**
- "Interactive Data Visualization" - Scott Murray
- "Storytelling with Data" - Cole Nussbaumer Knaflic
- "Python for Data Analysis" - Wes McKinney

---

## 🆘 **Suporte**

### **📧 Contato**
- **Email**: joao.silva@email.com
- **LinkedIn**: [João Silva](https://www.linkedin.com/in/joao-silva)
- **GitHub**: [joaoider](https://github.com/joaoider)

### **🐛 Reportar Bugs**
1. Abra uma **Issue** no GitHub
2. Descreva o problema detalhadamente
3. Inclua screenshots se possível
4. Especifique o ambiente (OS, versão Python, etc.)

---

<div align="center">

**🚀 Transforme seus dados em insights visuais impressionantes! 🚀**

**⭐ Se este projeto te ajudou, considere dar uma estrela! ⭐**

</div>
