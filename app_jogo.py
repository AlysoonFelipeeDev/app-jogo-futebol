import streamlit as st
import json
import os
import urllib.parse

st.set_page_config(page_title="Jogo ao Vivo", layout="wide")

ARQUIVO_JOGO = "jogo_atual.json"
ARQUIVO_HISTORICO = "historico_jogos.json"

# -------------------------
# FUNÇÕES
# -------------------------
def carregar_jogo():
    if os.path.exists(ARQUIVO_JOGO):
        with open(ARQUIVO_JOGO, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def salvar_jogo():
    jogo = {
        "time_a": st.session_state.time_a,
        "time_b": st.session_state.time_b,
        "eventos": st.session_state.eventos,
    }
    with open(ARQUIVO_JOGO, "w", encoding="utf-8") as f:
        json.dump(jogo, f, ensure_ascii=False)


def gerar_resumo():
    linhas = []
    linhas.append(
        f"{st.session_state.time_a['nome']} "
        f"{st.session_state.time_a['placar']} x "
        f"{st.session_state.time_b['placar']} "
        f"{st.session_state.time_b['nome']}"
    )
    linhas.append("")
    linhas.append("⚽ Gols e Assistências:")

    for e in st.session_state.eventos:
        time_nome = (
            st.session_state.time_a["nome"]
            if e["time"] == "A"
            else st.session_state.time_b["nome"]
        )
        linha = f"- {time_nome}: {e['autor']}"
        if e["assist"]:
            linha += f" (assist: {e['assist']})"
        linhas.append(linha)

    return "\n".join(linhas)


def salvar_historico():
    jogo = {
        "resumo": gerar_resumo(),
        "time_a": st.session_state.time_a,
        "time_b": st.session_state.time_b,
        "eventos": st.session_state.eventos,
    }

    historico = []
    if os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
            historico = json.load(f)

    historico.append(jogo)

    with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False)


# -------------------------
# ESTADO INICIAL
# -------------------------
if "time_a" not in st.session_state:
    jogo = carregar_jogo()
    if jogo:
        st.session_state.time_a = jogo["time_a"]
        st.session_state.time_b = jogo["time_b"]
        st.session_state.eventos = jogo["eventos"]
    else:
        st.session_state.time_a = {
            "nome": "Branco",
            "placar": 0,
            "jogadores": ["Alyson", "Artur", "João", "Pedro", "Lucas", "Rafa", "Diego"],
        }
        st.session_state.time_b = {
            "nome": "Azul",
            "placar": 0,
            "jogadores": ["Kadoya", "Bruno", "Matheus", "Igor", "Felipe", "Leo", "Caio"],
        }
        st.session_state.eventos = []

# -------------------------
# TOPO
# -------------------------
st.title("⚽ Jogo ao Vivo")

col1, col2 = st.columns(2)
with col1:
    st.subheader(st.session_state.time_a["nome"])
    st.markdown(f"## {st.session_state.time_a['placar']}")

with col2:
    st.subheader(st.session_state.time_b["nome"])
    st.markdown(f"## {st.session_state.time_b['placar']}")

# -------------------------
# MARCAR GOL
# -------------------------
st.divider()
st.subheader("➕ Marcar Gol")

time = st.radio("Time", ["A", "B"], horizontal=True)

time_data = (
    st.session_state.time_a if time == "A" else st.session_state.time_b
)

autor = st.selectbox("⚽ Gol de", time_data["jogadores"])
assist = st.selectbox(
    "👟 Assistência",
    [""] + [j for j in time_data["jogadores"] if j != autor],
)

if st.button("Registrar Gol"):
    evento = {
        "time": time,
        "autor": autor,
        "assist": assist,
    }
    st.session_state.eventos.append(evento)

    if time == "A":
        st.session_state.time_a["placar"] += 1
    else:
        st.session_state.time_b["placar"] += 1

    salvar_jogo()
    st.rerun()

# -------------------------
# EVENTOS
# -------------------------
st.divider()
st.subheader("📋 Gols Registrados")

for i, e in enumerate(st.session_state.eventos):
    time_nome = (
        st.session_state.time_a["nome"]
        if e["time"] == "A"
        else st.session_state.time_b["nome"]
    )

    col1, col2 = st.columns([4, 1])
    with col1:
        txt = f"{time_nome} - {e['autor']}"
        if e["assist"]:
            txt += f" (assist: {e['assist']})"
        st.write(txt)

    with col2:
        if st.button("❌", key=f"del_{i}"):
            if e["time"] == "A":
                st.session_state.time_a["placar"] -= 1
            else:
                st.session_state.time_b["placar"] -= 1

            st.session_state.eventos.pop(i)
            salvar_jogo()
            st.rerun()

# -------------------------
# FINALIZAR JOGO
# -------------------------
st.divider()
st.subheader("🏁 Finalizar Jogo")

resumo = gerar_resumo()
st.text_area("Resumo", resumo, height=180)

msg = urllib.parse.quote(resumo)
link_whats = f"https://wa.me/?text={msg}"
st.markdown(f"📤 [Enviar para WhatsApp]({link_whats})")

if st.button("Salvar jogo e iniciar novo"):
    salvar_historico()
    if os.path.exists(ARQUIVO_JOGO):
        os.remove(ARQUIVO_JOGO)
    st.session_state.clear()
    st.rerun()
