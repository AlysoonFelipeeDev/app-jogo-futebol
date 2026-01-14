import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="Jogo ao Vivo", layout="wide")

ARQUIVO_JOGO = "jogo_atual.json"

# =====================
# SALVAR / CARREGAR
# =====================
def salvar_jogo():
    dados = {
        "time_a": st.session_state.time_a,
        "time_b": st.session_state.time_b,
        "eventos": st.session_state.eventos
    }
    with open(ARQUIVO_JOGO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False)

def carregar_jogo():
    if os.path.exists(ARQUIVO_JOGO):
        with open(ARQUIVO_JOGO, "r", encoding="utf-8") as f:
            dados = json.load(f)
            st.session_state.time_a = dados["time_a"]
            st.session_state.time_b = dados["time_b"]
            st.session_state.eventos = dados.get("eventos", [])

# =====================
# RESET
# =====================
def resetar_jogo():
    if os.path.exists(ARQUIVO_JOGO):
        os.remove(ARQUIVO_JOGO)
    st.session_state.clear()
    st.rerun()

# =====================
# FUNÇÕES
# =====================
def criar_time(nome, jogadores):
    return {
        "nome": nome,
        "jogadores": {j: {"g": 0, "a": 0} for j in jogadores},
        "placar": 0
    }

def tabela(time):
    dados = []
    for jogador, v in time["jogadores"].items():
        dados.append({
            "Jogadores": jogador,
            "⚽": v["g"],
            "👟": v["a"]
        })
    st.dataframe(pd.DataFrame(dados), hide_index=True, use_container_width=True)

def aplicar_evento(evento, remover=False):
    time = st.session_state.time_a if evento["time"] == "A" else st.session_state.time_b
    fator = -1 if remover else 1

    time["placar"] += fator
    time["jogadores"][evento["autor"]]["g"] += fator

    if evento["assist"]:
        time["jogadores"][evento["assist"]]["a"] += fator

# =====================
# ESTADO INICIAL
# =====================
if "time_a" not in st.session_state:
    carregar_jogo()

if "time_a" not in st.session_state:
    st.session_state.time_a = criar_time(
        "Alyson",
        ["Alyson", "Artur", "Erick", "Rafa", "Vitão", "Gabriel", "Arthur"]
    )

if "time_b" not in st.session_state:
    st.session_state.time_b = criar_time(
        "Kadoya",
        ["Kadoya", "Wagner", "Miguel", "Kadu", "Gege", "Jessé", "Erick Cei"]
    )

if "eventos" not in st.session_state:
    st.session_state.eventos = []

# =====================
# PLACAR
# =====================
st.markdown(
    f"""
    <h2 style="text-align:center">
        {st.session_state.time_a['nome']}
        {st.session_state.time_a['placar']} x {st.session_state.time_b['placar']}
        {st.session_state.time_b['nome']}
    </h2>
    """,
    unsafe_allow_html=True
)

st.divider()

# =====================
# MODAIS DE GOL
# =====================
@st.dialog("Gol - Time A")
def gol_time_a():
    jogadores = list(st.session_state.time_a["jogadores"].keys())
    autor = st.selectbox("⚽ Gol", jogadores)
    assist = st.selectbox("👟 Assistência", ["Nenhuma"] + jogadores)

    if st.button("Confirmar"):
        evento = {
            "time": "A",
            "autor": autor,
            "assist": None if assist == "Nenhuma" else assist
        }
        st.session_state.eventos.append(evento)
        aplicar_evento(evento)
        salvar_jogo()
        st.rerun()

@st.dialog("Gol - Time B")
def gol_time_b():
    jogadores = list(st.session_state.time_b["jogadores"].keys())
    autor = st.selectbox("⚽ Gol", jogadores)
    assist = st.selectbox("👟 Assistência", ["Nenhuma"] + jogadores)

    if st.button("Confirmar"):
        evento = {
            "time": "B",
            "autor": autor,
            "assist": None if assist == "Nenhuma" else assist
        }
        st.session_state.eventos.append(evento)
        aplicar_evento(evento)
        salvar_jogo()
        st.rerun()

c1, c2 = st.columns(2)
with c1:
    if st.button("⚽ Gol Time A", use_container_width=True):
        gol_time_a()
with c2:
    if st.button("⚽ Gol Time B", use_container_width=True):
        gol_time_b()

st.divider()



# =====================
# TABELAS
# =====================
c1, c2 = st.columns(2)
with c1:
    st.subheader(st.session_state.time_a["nome"])
    tabela(st.session_state.time_a)
with c2:
    st.subheader(st.session_state.time_b["nome"])
    tabela(st.session_state.time_b)

# =====================
# HISTÓRICO DE GOLS
# =====================
st.subheader("📋 Histórico de gols")

for i, e in enumerate(st.session_state.eventos):
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

    time_nome = st.session_state.time_a["nome"] if e["time"] == "A" else st.session_state.time_b["nome"]

    col1.write(time_nome)
    col2.write(f"⚽ {e['autor']}")
    col3.write(f"👟 {e['assist'] or '-'}")

    if col4.button("❌", key=f"del_{i}"):
        aplicar_evento(e, remover=True)
        st.session_state.eventos.pop(i)
        salvar_jogo()
        st.rerun()

st.divider()

# =====================
# RESET COM CONFIRMAÇÃO
# =====================
st.divider()
st.subheader("⚠️ Finalizar / Novo jogo")

if "confirmar_reset" not in st.session_state:
    st.session_state.confirmar_reset = False

if not st.session_state.confirmar_reset:
    if st.button("🔄 Resetar jogo"):
        st.session_state.confirmar_reset = True
else:
    st.warning("Tem certeza que deseja resetar o jogo? Isso apagará o placar e os gols.")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ Sim, resetar"):
            resetar_jogo()
    with c2:
        if st.button("❌ Cancelar"):
            st.session_state.confirmar_reset = False

# =====================
# CONFIGURAÇÕES DO JOGO
# =====================
st.divider()
st.subheader("⚙️ Configurações do jogo")

def config_time(time_key, time_label):
    time = st.session_state[time_key]

    st.markdown(f"### {time_label}")

    # Alterar nome do time
    novo_nome = st.text_input(
        "Nome do time",
        value=time["nome"],
        key=f"nome_{time_key}"
    )

    if novo_nome != time["nome"]:
        time["nome"] = novo_nome
        salvar_jogo()

    # Adicionar jogador
    novo_jogador = st.text_input(
        "Adicionar jogador",
        key=f"add_{time_key}"
    )

    if st.button("➕ Adicionar", key=f"btn_add_{time_key}") and novo_jogador:
        if novo_jogador not in time["jogadores"]:
            time["jogadores"][novo_jogador] = {"g": 0, "a": 0}
            salvar_jogo()
            st.rerun()

    st.markdown("**Jogadores:**")

    for jogador, v in list(time["jogadores"].items()):
        c1, c2 = st.columns([4, 1])
        c1.write(jogador)

        # Só permite remover se não tiver stats
        if v["g"] == 0 and v["a"] == 0:
            if c2.button("❌", key=f"rem_{time_key}_{jogador}"):
                del time["jogadores"][jogador]
                salvar_jogo()
                st.rerun()
        else:
            c2.write("🔒")

# Configuração dos dois times
c1, c2 = st.columns(2)
with c1:
    config_time("time_a", "Time A")
with c2:
    config_time("time_b", "Time B")

