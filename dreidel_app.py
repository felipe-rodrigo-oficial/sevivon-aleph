import streamlit as st
from io import BytesIO

# Configuração inicial
st.title("Jogo de Dreidel - PDF de Lances")

# Inicializar lista de lances no estado da sessão
if "lances" not in st.session_state:
    st.session_state.lances = []

# Inicializar jogadores
if "jogadores" not in st.session_state:
    st.session_state.jogadores = {}

# Regras do Dreidel
regras = {
    "נ": "Nun - Nada acontece",
    "ג": "Gimel - Pegue tudo",
    "ה": "Hei - Pegue metade",
    "ש": "Shin - Adicione uma moeda"
}

# Gerenciamento de jogadores
st.sidebar.header("Gerenciamento de Jogadores")
nome = st.sidebar.text_input("Nome do jogador")
moedas = st.sidebar.number_input("Moedas iniciais", min_value=1, step=1)

if st.sidebar.button("Adicionar jogador"):
    if nome and nome not in st.session_state.jogadores:
        st.session_state.jogadores[nome] = moedas
        st.sidebar.success(f"Jogador {nome} adicionado com {moedas} moedas!")
    elif nome in st.session_state.jogadores:
        st.sidebar.warning("Jogador já existe!")
    else:
        st.sidebar.error("Insira um nome válido!")

# Mostrar jogadores e saldos
st.header("Jogadores")
if st.session_state.jogadores:
    for jogador, saldo in st.session_state.jogadores.items():
        st.write(f"{jogador}: {saldo} moedas")
else:
    st.write("Nenhum jogador cadastrado.")

# Rodada do Dreidel
st.header("Rodada do Dreidel")
jogador_selecionado = st.selectbox("Selecione um jogador", list(st.session_state.jogadores.keys()))
resultado = st.radio("Resultado do Dreidel", list(regras.keys()))
moedas_por_jogador = st.number_input("Quantidade de moedas por jogador nesta jogada", min_value=1, step=1)

# Calcular total de moedas em jogo
total_jogadores = len(st.session_state.jogadores)
moedas_em_jogo = moedas_por_jogador * total_jogadores
st.write(f"Total de moedas em jogo: {moedas_em_jogo} (Quantidade por jogador x Número de jogadores)")

if resultado:
    st.write(f"Resultado: {regras[resultado]}")

if st.button("Aplicar resultado"):
    if jogador_selecionado:
        # Subtrair moedas de todos os jogadores
        for jogador in st.session_state.jogadores:
            st.session_state.jogadores[jogador] -= moedas_por_jogador
            if st.session_state.jogadores[jogador] < 0:
                st.session_state.jogadores[jogador] = 0  # Evitar saldo negativo

        # Registrar o lance
        lance = f"{jogador_selecionado} - {resultado} ({regras[resultado]}) com {moedas_em_jogo} moedas em jogo"
        st.session_state.lances.append(lance)

        # Atualizar saldo do jogador selecionado com base no resultado
        if resultado == "נ":  # Nun
            st.success("Nada acontece!")
        elif resultado == "ג":  # Gimel
            st.session_state.jogadores[jogador_selecionado] += moedas_em_jogo
            st.success(f"{jogador_selecionado} ganhou {moedas_em_jogo} moedas!")
        elif resultado == "ה":  # Hei
            ganho = moedas_em_jogo // 2
            st.session_state.jogadores[jogador_selecionado] += ganho
            st.success(f"{jogador_selecionado} ganhou {ganho} moedas!")
        elif resultado == "ש":  # Shin
            st.session_state.jogadores[jogador_selecionado] -= moedas_em_jogo
            st.success(f"{jogador_selecionado} perdeu {moedas_em_jogo} moedas!")

        # Ajustar saldo mínimo novamente
        if st.session_state.jogadores[jogador_selecionado] < 0:
            st.session_state.jogadores[jogador_selecionado] = 0

        # Exibir saldo atualizado
        st.write(f"Saldo atualizado de {jogador_selecionado}: {st.session_state.jogadores[jogador_selecionado]} moedas")

