import streamlit as st

st.set_page_config(page_title="Jogo ao Vivo", layout="wide")

# =====================
# FUNÇÕES
# =====================
def criar_time(nome, jogadores):
    return {
        "nome": nome,
        "jogadores": {j: {"g": 0, "a": 0} for j in jogadores},
        "placar": 0
    }

import pandas as pd

def tabela(time):
    dados = []

    for jogador, v in time["jogadores"].items():
        dados.append({
            "Jogadores": jogador,
            "⚽": v["g"],
            "👟": v["a"]
        })

    df = pd.DataFrame(dados)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

 

# =====================
# ESTADO INICIAL
# =====================
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

# =====================
# CONFIGURAÇÃO
# =====================
with st.expander("⚙️ Configuração do jogo"):
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Time A")
        st.session_state.time_a["nome"] = st.text_input(
            "Nome do time",
            st.session_state.time_a["nome"],
            key="nome_a"
        )

        novo = st.text_input("Adicionar jogador", key="novo_a")
        if st.button("Adicionar", key="add_a"):
            if novo:
                st.session_state.time_a["jogadores"][novo] = {"g": 0, "a": 0}
                st.rerun()

        if st.session_state.time_a["jogadores"]:
            rem = st.selectbox(
                "Remover jogador",
                list(st.session_state.time_a["jogadores"].keys()),
                key="rem_a"
            )
            if st.button("Remover", key="del_a"):
                del st.session_state.time_a["jogadores"][rem]
                st.rerun()

    with c2:
        st.subheader("Time B")
        st.session_state.time_b["nome"] = st.text_input(
            "Nome do time",
            st.session_state.time_b["nome"],
            key="nome_b"
        )

        novo = st.text_input("Adicionar jogador", key="novo_b")
        if st.button("Adicionar", key="add_b"):
            if novo:
                st.session_state.time_b["jogadores"][novo] = {"g": 0, "a": 0}
                st.rerun()

        if st.session_state.time_b["jogadores"]:
            rem = st.selectbox(
                "Remover jogador",
                list(st.session_state.time_b["jogadores"].keys()),
                key="rem_b"
            )
            if st.button("Remover", key="del_b"):
                del st.session_state.time_b["jogadores"][rem]
                st.rerun()

# =====================
# PLACAR
# =====================
st.markdown(
    f"""
    <h2 style="text-align:center">
        {st.session_state.time_a['nome']}
        &nbsp; {st.session_state.time_a['placar']} x {st.session_state.time_b['placar']} &nbsp;
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
    autor = st.selectbox("⚽ Quem fez o gol?", jogadores)
    assist = st.selectbox("👟 Assistência", ["Sem assistência"] + jogadores)

    if st.button("Confirmar Gol", use_container_width=True):
        st.session_state.time_a["placar"] += 1
        st.session_state.time_a["jogadores"][autor]["g"] += 1
        if assist != "Sem assistência" and assist != autor:
            st.session_state.time_a["jogadores"][assist]["a"] += 1
        st.rerun()

@st.dialog("Gol - Time B")
def gol_time_b():
    jogadores = list(st.session_state.time_b["jogadores"].keys())
    autor = st.selectbox("⚽ Quem fez o gol?", jogadores)
    assist = st.selectbox("👟 Assistência", ["Sem assistência"] + jogadores)

    if st.button("Confirmar Gol", use_container_width=True):
        st.session_state.time_b["placar"] += 1
        st.session_state.time_b["jogadores"][autor]["g"] += 1
        if assist != "Sem assistência" and assist != autor:
            st.session_state.time_b["jogadores"][assist]["a"] += 1
        st.rerun()

# =====================
# BOTÕES DE GOL
# =====================
b1, b2 = st.columns(2)

with b1:
    if st.button(f"⚽ Gol {st.session_state.time_a['nome']}", use_container_width=True):
        gol_time_a()

with b2:
    if st.button(f"⚽ Gol {st.session_state.time_b['nome']}", use_container_width=True):
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
