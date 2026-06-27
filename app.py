import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(page_title="Simulador de Consórcio", layout="wide")

st.title("📊 Simulador Interativo de Consórcio")
st.markdown("Compare os cenários de **Lance Livre** e **Lance Fixo** dinamicamente.")

# --- BARRA LATERAL (INPUTS) ---
st.sidebar.header("🔧 Parâmetros de Entrada")

carta = st.sidebar.number_input("Valor da Carta (R$)", value=170000.0, step=5000.0)
saldo_devedor = st.sidebar.number_input("Saldo Devedor (R$)", value=183887.31, step=1000.0)
valor_carro = st.sidebar.number_input("Valor do Carro Desejado (R$)", value=138000.0, step=5000.0)
rec_proprio = st.sidebar.number_input("Recurso Próprio (Ex: Venda Civic) (R$)", value=74000.0, step=1000.0)

# Inputs específicos de cada modalidade baseados na sua planilha original
st.sidebar.subheader("Cenário Livre")
lance_total_livre = st.sidebar.number_input("Lance Total - Livre (R$)", value=76500.0, step=1000.0)
lance_embutido_livre = st.sidebar.number_input("Lance Embutido Utilizado - Livre (R$)", value=51000.0, step=1000.0)

st.sidebar.subheader("Cenário Fixo")
lance_total_fixo = st.sidebar.number_input("Lance Total - Fixo (R$)", value=36777.46, step=1000.0)
lance_embutido_fixo = st.sidebar.number_input("Lance Embutido Utilizado - Fixo (R$)", value=36777.46, step=1000.0)


# --- PROCESSAMENTO DOS DADOS (LÓGICA DA PLANILHA) ---

# Cenário Livre
rec_proprio_utilizado_livre = lance_total_livre - lance_embutido_livre
sobra_rec_proprio_livre = rec_proprio - rec_proprio_utilizado_livre
carta_liquida_livre = carta - lance_embutido_livre
necessidade_complemento_livre = max(0.0, valor_carro - carta_liquida_livre)
saldo_para_aquisicao_livre = carta_liquida_livre + sobra_rec_proprio_livre
resultado_final_livre = sobra_rec_proprio_livre - necessidade_complemento_livre

# Cenário Fixo
rec_proprio_utilizado_fixo = lance_total_fixo - lance_embutido_fixo
sobra_rec_proprio_fixo = rec_proprio - rec_proprio_utilizado_fixo
carta_liquida_fixo = carta - lance_embutido_fixo
necessidade_complemento_fixo = max(0.0, valor_carro - carta_liquida_fixo)
saldo_para_aquisicao_fixo = carta_liquida_fixo + sobra_rec_proprio_fixo
resultado_final_fixo = sobra_rec_proprio_fixo - necessidade_complemento_fixo


# --- EXIBIÇÃO NO DASHBOARD ---

# Cards de Resumo Metrificado
col1, col2 = st.columns(2)

with col1:
    st.subheader("🟢 Cenário: LANCE LIVRE")
    st.metric(label="Sobra do Recurso Próprio", value=f"R$ {sobra_rec_proprio_livre:,.2f}")
    st.metric(label="Carta Líquida (Pós-Embutido)", value=f"R$ {carta_liquida_livre:,.2f}")
    st.metric(label="Saldo Total para Aquisição", value=f"R$ {saldo_para_aquisicao_livre:,.2f}")

with col2:
    st.subheader("🔵 Cenário: LANCE FIXO")
    st.metric(label="Sobra do Recurso Próprio", value=f"R$ {sobra_rec_proprio_fixo:,.2f}")
    st.metric(label="Carta Líquida (Pós-Embutido)", value=f"R$ {carta_liquida_fixo:,.2f}")
    st.metric(label="Saldo Total para Aquisição", value=f"R$ {saldo_para_aquisicao_fixo:,.2f}")

st.markdown("---")

# Tabela Comparativa Completa
st.subheader("📋 Tabela Comparativa Detalhada")

dados_tabela = {
    "Métrica": [
        "Carta Original", "Saldo Devedor", "Lance Total Ofertado", 
        "Lance Embutido", "Sobra Recurso Próprio", "Carta Líquida disponível",
        "Valor do Carro", "Saldo Total para Aquisição (Carta Líquida + Sobra)"
    ],
    "LIVRE": [
        f"R$ {carta:,.2f}", f"R$ {saldo_devedor:,.2f}", f"R$ {lance_total_livre:,.2f}",
        f"R$ {lance_embutido_livre:,.2f}", f"R$ {sobra_rec_proprio_livre:,.2f}", f"R$ {carta_liquida_livre:,.2f}",
        f"R$ {valor_carro:,.2f}", f"R$ {saldo_para_aquisicao_livre:,.2f}"
    ],
    "FIXO": [
        f"R$ {carta:,.2f}", f"R$ {saldo_devedor:,.2f}", f"R$ {lance_total_fixo:,.2f}",
        f"R$ {lance_embutido_fixo:,.2f}", f"R$ {sobra_rec_proprio_fixo:,.2f}", f"R$ {carta_liquida_fixo:,.2f}",
        f"R$ {valor_carro:,.2f}", f"R$ {saldo_para_aquisicao_fixo:,.2f}"
    ]
}

df_comparativo = pd.DataFrame(dados_tabela)
st.table(df_comparativo.set_index("Métrica"))

# --- GRÁFICOS VISUAIS ---
st.markdown("---")
st.subheader("📊 Comparação Visual de Saldos")

# Gráfico de barras comparando a Sobra de caixa vs Saldo de Aquisição
fig = go.Figure()
fig.add_trace(go.Bar(
    name='Sobra Recurso Próprio (Bolso)',
    x=['LIVRE', 'FIXO'],
    y=[sobra_rec_proprio_livre, sobra_rec_proprio_fixo],
    marker_color='rgb(34, 139, 34)'
))
fig.add_trace(go.Bar(
    name='Carta Líquida para Carro',
    x=['LIVRE', 'FIXO'],
    y=[carta_liquida_livre, carta_liquida_fixo],
    marker_color='rgb(65, 105, 225)'
))

fig.update_layout(barmode='stack', title_text='Composição Financeira Pós-Contemplação (R$)')
st.plotly_chart(fig, use_container_width=True)
