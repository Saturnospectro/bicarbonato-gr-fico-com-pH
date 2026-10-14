import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==========================================
# 1. CARREGAMENTO E TRATAMENTO DOS DADOS
# ==========================================

# Lê a planilha pulando as 6 primeiras linhas de metadados
df = pd.read_excel("dados_bicarbonato.xlsx", sheet_name='Dados em', skiprows=6, header=None)

# Renomeia as colunas para facilitar o trabalho
df.columns = ["TIME", "pH", "Pressão", "Temperatura", "CH4"]

# Filtra para manter apenas as linhas onde a coluna de tempo começa com o ano "20..."
df = df[df['TIME'].astype(str).str.startswith('20')]

# Converte os tipos de dados para o formato correto (data/hora e números)
df['TIME'] = pd.to_datetime(df['TIME'])
df['pH'] = pd.to_numeric(df['pH'], errors='coerce')
df['Pressão'] = pd.to_numeric(df['Pressão'], errors='coerce')

# Remove linhas vazias e ordena cronologicamente
df = df.sort_values('TIME').dropna(subset=['pH', 'Pressão'])

# ==========================================
# 2. CRIAÇÃO DO GRÁFICO INTERATIVO
# ==========================================

# Cria a figura permitindo um segundo eixo Y (já que pH e Pressão têm escalas diferentes)
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Adiciona a linha do pH (eixo Y esquerdo)
fig.add_trace(
    go.Scatter(x=df['TIME'], y=df['pH'], name="pH", line=dict(color='blue')),
    secondary_y=False,
)

# Adiciona a linha da Pressão (eixo Y direito)
fig.add_trace(
    go.Scatter(x=df['TIME'], y=df['Pressão'], name="Pressão (kPa)", line=dict(color='red')),
    secondary_y=True,
)

# ==========================================
# 3. CUSTOMIZAÇÃO VISUAL (LAYOUT)
# ==========================================

# Adiciona títulos e configura o cursor para mostrar os dois valores juntos ao passar o mouse
fig.update_layout(
    title_text="Monitoramento Interativo: Variação de pH e Pressão",
    hovermode="x unified" 
)

# Títulos dos eixos
fig.update_xaxes(title_text="Tempo")
fig.update_yaxes(title_text="<b>pH</b>", color="blue", secondary_y=False)
fig.update_yaxes(title_text="<b>Pressão (kPa)</b>", color="red", secondary_y=True)

# ==========================================
# 4. GERAÇÃO DO ARQUIVO PARA O GITHUB
# ==========================================

# Salva o gráfico como index.html (nome padrão exigido pelo GitHub Pages)
fig.write_html("index.html")

print("Sucesso! O arquivo 'index.html' foi criado. Agora é só fazer o upload no seu repositório do GitHub.")