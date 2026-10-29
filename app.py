
import streamlit as st
import pandas as pd

from conhecimento import carregar_base_conhecimento
from motor_ponderado import calcular_compatibilidade
from recomendacoes import analisar_competencias, gerar_roadmap


# ==================================================
# CONFIGURAÇÕES INICIAIS
# ==================================================

st.set_page_config(
    page_title="CareerPath | Consultor de Carreiras",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

base = carregar_base_conhecimento()

ETAPAS = [
    "Perfil pessoal",
    "Afinidades técnicas",
    "Objetivos profissionais",
    "Compatibilidade",
    "Plano de desenvolvimento"
]

EXPERIENCIAS = [
    "Iniciante",
    "Estudante",
    "Já trabalho na área"
]

OBJETIVOS = [
    "Conseguir o primeiro emprego",
    "Mudar de área",
    "Aprimorar meus conhecimentos",
    "Descobrir uma carreira"
]

ESCALA = {
    1: "Nenhuma afinidade",
    2: "Pouca afinidade",
    3: "Afinidade moderada",
    4: "Boa afinidade",
    5: "Muita afinidade"
}


# ==================================================
# IDENTIDADE VISUAL
# ==================================================

st.markdown("""
<style>
    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        letter-spacing: -0.025em;
    }

    div[data-testid="stMetric"] {
        padding: 16px;
        border: 1px solid #CBD5E1;
        border-radius: 12px;
    }

    div[data-testid="stForm"] {
        border-radius: 14px;
    }

    div.stButton > button {
        border-radius: 9px;
        min-height: 42px;
    }

    div[data-testid="stProgress"] {
        margin-bottom: 10px;
    }

    @media (max-width: 640px) {
        .block-container {
            padding-top: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)


# ==================================================
# CONTROLE DA SESSÃO
# ==================================================

def iniciar_sessao():
    valores_iniciais = {
        "etapa": 1,
        "perfil": {},
        "respostas": {},
        "carreira_escolhida": None,
        "conhecimentos_por_carreira": {},
        "mostrar_roadmap": False
    }

    for chave, valor in valores_iniciais.items():
        if chave not in st.session_state:
            st.session_state[chave] = valor


def mudar_etapa(numero):
    st.session_state.etapa = numero
    st.rerun()


def reiniciar_avaliacao():
    for chave in list(st.session_state.keys()):
        del st.session_state[chave]

    st.rerun()


iniciar_sessao()


# ==================================================
# CABEÇALHO E NAVEGAÇÃO
# ==================================================

st.title("🎯 CareerPath")
st.caption("CONSULTOR INTELIGENTE DE CARREIRAS EM TI")

st.write(
    "Descubra suas afinidades profissionais, explore carreiras "
    "em tecnologia e construa seu plano de desenvolvimento."
)

with st.sidebar:
    st.header("Sobre o sistema")

    st.write(
        "Sistema especialista educacional baseado em regras, "
        "pontuação ponderada e análise de competências."
    )

    st.divider()

    st.write("**Tecnologias:**")
    st.write("Python • JSON • Streamlit")

    st.divider()

    if st.button(
        "🔄 Nova avaliação",
        use_container_width=True
    ):
        reiniciar_avaliacao()


etapa = st.session_state.etapa

st.progress(etapa / 5)

st.caption(
    f"Etapa {etapa} de 5 — {ETAPAS[etapa - 1]}"
)

st.divider()


# ==================================================
# ETAPA 1 - PERFIL PESSOAL
# ==================================================

if etapa == 1:
    st.header("Vamos conhecer você")
    st.write(
        "Preencha algumas informações iniciais "
        "para personalizar sua experiência."
    )

    perfil = st.session_state.perfil

    with st.form("form_perfil"):
        nome = st.text_input(
            "Como podemos chamar você?",
            value=perfil.get("nome", ""),
            placeholder="Digite seu nome (opcional)"
        )

        experiencia_atual = perfil.get(
            "experiencia", EXPERIENCIAS[0]
        )

        experiencia = st.selectbox(
            "Qual sua experiência com tecnologia?",
            EXPERIENCIAS,
            index=EXPERIENCIAS.index(experiencia_atual)
        )

        st.info(
            "Não é necessário ter experiência profissional "
            "para realizar esta avaliação."
        )

        avancar = st.form_submit_button(
            "Continuar →",
            type="primary",
            use_container_width=True
        )

    if avancar:
        st.session_state.perfil = {
            **perfil,
            "nome": nome.strip(),
            "experiencia": experiencia
        }

        mudar_etapa(2)


# ==================================================
# ETAPA 2 - AFINIDADES TÉCNICAS
# ==================================================

elif etapa == 2:
    st.header("Suas afinidades técnicas")

    st.write(
        "Responda às perguntas de acordo com seus interesses. "
        "Não existem respostas certas ou erradas."
    )

    with st.expander("Entenda a escala de respostas"):
        for numero, descricao in ESCALA.items():
            st.write(f"**{numero}** — {descricao}")

    perguntas = base["perguntas"]
    respostas_anteriores = st.session_state.respostas

    with st.form("form_afinidades"):
        respostas = {}

        for indice, pergunta in enumerate(perguntas):
            if indice % 2 == 0:
                colunas = st.columns(2, gap="large")

            coluna = colunas[indice % 2]

            with coluna:
                with st.container(border=True):
                    st.markdown(
                        f"**{indice + 1}. {pergunta['texto']}**"
                    )

                    codigo = pergunta["id"]

                    valor_inicial = respostas_anteriores.get(
                        codigo, 3
                    )

                    respostas[codigo] = st.radio(
                        "Grau de afinidade",
                        options=[1, 2, 3, 4, 5],
                        index=valor_inicial - 1,
                        horizontal=True,
                        key=f"afinidade_{codigo}",
                        help=(
                            "1 = Nenhuma afinidade; "
                            "5 = Muita afinidade."
                        )
                    )

        st.caption(
            f"{len(perguntas)} perguntas de afinidade."
        )

        voltar, proximo = st.columns(2)

        with voltar:
            botao_voltar = st.form_submit_button(
                "← Voltar",
                use_container_width=True
            )

        with proximo:
            botao_proximo = st.form_submit_button(
                "Continuar →",
                type="primary",
                use_container_width=True
            )

    if botao_voltar or botao_proximo:
        alterou_respostas = (
            respostas != st.session_state.respostas
        )

        st.session_state.respostas = respostas

        if alterou_respostas:
            st.session_state.mostrar_roadmap = False

        mudar_etapa(1 if botao_voltar else 3)


# ==================================================
# ETAPA 3 - OBJETIVOS PROFISSIONAIS
# ==================================================

elif etapa == 3:
    st.header("Seus objetivos profissionais")

    st.write(
        "Agora queremos entender o que você "
        "pretende alcançar na área de tecnologia."
    )

    perfil = st.session_state.perfil

    objetivo_atual = perfil.get(
        "objetivo", OBJETIVOS[0]
    )

    with st.form("form_objetivos"):
        objetivo = st.selectbox(
            "Qual é seu principal objetivo?",
            OBJETIVOS,
            index=OBJETIVOS.index(objetivo_atual)
        )

        with st.container(border=True):
            st.subheader("Resumo do seu perfil")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Nome**")
                st.write(perfil.get("nome") or "Não informado")

                st.write("**Experiência**")
                st.write(perfil.get("experiencia"))

            with col2:
                st.write("**Afinidades respondidas**")
                st.write(
                    f"{len(st.session_state.respostas)} "
                    f"de {len(base['perguntas'])}"
                )

        voltar, finalizar = st.columns(2)

        with voltar:
            botao_voltar = st.form_submit_button(
                "← Voltar",
                use_container_width=True
            )

        with finalizar:
            botao_resultados = st.form_submit_button(
                "Ver meus resultados →",
                type="primary",
                use_container_width=True
            )

    if botao_voltar or botao_resultados:
        st.session_state.perfil["objetivo"] = objetivo

        mudar_etapa(2 if botao_voltar else 4)


# ==================================================
# ETAPA 4 - RESULTADOS DE COMPATIBILIDADE
# ==================================================

elif etapa == 4:
    respostas = st.session_state.respostas

    ids_perguntas = {
        pergunta["id"] for pergunta in base["perguntas"]
    }

    if set(respostas) != ids_perguntas:
        st.warning(
            "Complete todas as perguntas antes de continuar."
        )

        if st.button("Voltar ao questionário"):
            mudar_etapa(2)

        st.stop()

    resultados = calcular_compatibilidade(respostas)
    top3 = resultados[:3]

    nome = st.session_state.perfil.get("nome")

    st.header(
        f"Seus resultados{', ' + nome if nome else ''}"
    )

    st.write(
        "Com base nas suas afinidades, estas são "
        "as carreiras com maior compatibilidade."
    )

    st.subheader("🏆 Suas três principais carreiras")

    for posicao, resultado in enumerate(top3, start=1):
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(
                    f"### {posicao}º — {resultado['carreira']}"
                )

            with col2:
                st.metric(
                    "Compatibilidade",
                    f"{resultado['compatibilidade']:.1f}%"
                )

            st.progress(
                min(
                    1.0,
                    max(
                        0.0,
                        resultado["compatibilidade"] / 100
                    )
                )
            )

            favoraveis = resultado["pontos_favoraveis"]
            atencao = resultado["pontos_atencao"]

            coluna_positiva, coluna_atencao = st.columns(2)

            with coluna_positiva:
                st.markdown("**✅ Pontos favoráveis**")

                if favoraveis:
                    for ponto in favoraveis:
                        st.write(f"• {ponto}")
                else:
                    st.caption("Nenhum ponto identificado.")

            with coluna_atencao:
                st.markdown("**⚠️ Pontos de atenção**")

                if atencao:
                    for ponto in atencao:
                        st.write(f"• {ponto}")
                else:
                    st.caption(
                        "Nenhum ponto de atenção identificado."
                    )

            st.caption(
                f"Penalidade aplicada: "
                f"{resultado['penalidade']} "
                "pontos percentuais"
            )

    # Comparação geral
    st.divider()
    st.subheader("📊 Comparação das dez carreiras")

    dados_grafico = pd.DataFrame([
        {
            "Carreira": item["carreira"],
            "Compatibilidade (%)": item["compatibilidade"]
        }
        for item in resultados
    ])

    st.bar_chart(
        dados_grafico,
        x="Carreira",
        y="Compatibilidade (%)",
        horizontal=True,
        sort=False
    )

    with st.expander("Ver tabela completa"):
        st.dataframe(
            dados_grafico,
            hide_index=True,
            use_container_width=True
        )

    st.info(
        "As porcentagens representam uma estimativa "
        "calculada pelo modelo educacional de regras e pesos. "
        "Não são probabilidades de sucesso profissional."
    )

    # Escolha de carreira
    st.divider()
    st.subheader("📚 Próximo passo: seu desenvolvimento")

    st.write(
        "Escolha uma das três carreiras recomendadas "
        "para descobrir quais competências desenvolver."
    )

    opcoes = {
        item["codigo"]: item["carreira"]
        for item in top3
    }

    codigos = list(opcoes.keys())

    escolha_anterior = st.session_state.carreira_escolhida

    indice = (
        codigos.index(escolha_anterior)
        if escolha_anterior in codigos
        else 0
    )

    codigo_selecionado = st.selectbox(
        "Carreira para o plano de estudos",
        options=codigos,
        format_func=lambda codigo: opcoes[codigo],
        index=indice
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "← Revisar respostas",
            use_container_width=True
        ):
            mudar_etapa(3)

    with col2:
        if st.button(
            "Criar meu plano →",
            type="primary",
            use_container_width=True
        ):
            st.session_state.carreira_escolhida = (
                codigo_selecionado
            )

            st.session_state.mostrar_roadmap = False
            mudar_etapa(5)


# ==================================================
# ETAPA 5 - COMPETÊNCIAS E ROADMAP
# ==================================================

elif etapa == 5:
    codigo = st.session_state.carreira_escolhida

    if codigo not in base["carreiras"]:
        st.warning("Nenhuma carreira foi selecionada.")

        if st.button("Voltar aos resultados"):
            mudar_etapa(4)

        st.stop()

    carreira = base["carreiras"][codigo]
    competencias = carreira["competencias_junior"]

    st.header("Seu plano de desenvolvimento")
    st.subheader(carreira["nome"])

    st.write(
        "Informe seu conhecimento atual nas competências "
        "abaixo. As respostas serão comparadas aos níveis "
        "esperados para um perfil Júnior."
    )

    st.caption(
        "Escala: 1 = Conhecimento muito básico | "
        "3 = Intermediário | 5 = Domínio elevado"
    )

    historico = st.session_state.conhecimentos_por_carreira
    conhecimentos_anteriores = historico.get(codigo, {})

    with st.form("form_competencias"):
        conhecimentos = {}

        for chave, dados in competencias.items():
            with st.container(border=True):
                nivel_necessario = dados["nivel_necessario"]

                st.markdown(f"**{dados['nome']}**")

                st.caption(
                    f"Nível de referência: {nivel_necessario}/5"
                )

                conhecimentos[chave] = st.slider(
                    "Seu nível atual",
                    min_value=1,
                    max_value=5,
                    value=conhecimentos_anteriores.get(
                        chave, 1
                    ),
                    key=f"conhecimento_{codigo}_{chave}"
                )

        analisar = st.form_submit_button(
            "Analisar minhas competências",
            type="primary",
            use_container_width=True
        )

    if analisar:
        st.session_state.conhecimentos_por_carreira[
            codigo
        ] = conhecimentos

        st.session_state.mostrar_roadmap = True

    if st.session_state.mostrar_roadmap:
        conhecimentos_salvos = (
            st.session_state.conhecimentos_por_carreira[codigo]
        )

        analise = analisar_competencias(
            codigo,
            conhecimentos_salvos
        )

        plano = gerar_roadmap(
            codigo,
            conhecimentos_salvos
        )

        lacunas = [
            item for item in analise
            if item["lacuna"] > 0
        ]

        concluidas = len(analise) - len(lacunas)

        st.divider()
        st.subheader("📊 Diagnóstico de competências")

        metrica1, metrica2, metrica3 = st.columns(3)

        with metrica1:
            st.metric(
                "Competências avaliadas",
                len(analise)
            )

        with metrica2:
            st.metric(
                "Requisitos atingidos",
                concluidas
            )

        with metrica3:
            st.metric(
                "Competências a desenvolver",
                len(lacunas)
            )

        st.write("**Requisitos atendidos**")

        if analise:
            st.progress(concluidas / len(analise))

        tabela = pd.DataFrame(analise)

        tabela = tabela.rename(columns={
            "competencia": "Competência",
            "nivel_atual": "Nível atual",
            "nivel_necessario": "Nível necessário",
            "lacuna": "Lacuna",
            "status": "Situação"
        })

        st.dataframe(
            tabela,
            hide_index=True,
            use_container_width=True
        )

        # Plano de estudos
        st.divider()
        st.subheader("🗺️ Seu roteiro de estudos")

        estudos = plano["estudos"]

        if estudos:
            st.write(
                "Siga a sequência sugerida para desenvolver "
                "as competências que ainda precisam melhorar."
            )

            for posicao, estudo in enumerate(
                estudos, start=1
            ):
                with st.container(border=True):
                    st.markdown(
                        f"### {posicao}. {estudo['competencia']}"
                    )

                    st.write(estudo["conteudo"])

                    st.caption(
                        f"Lacuna atual: "
                        f"{estudo['lacuna']} nível(is)"
                    )
        else:
            st.success(
                "Parabéns! Você já atende aos níveis "
                "de referência definidos para esta carreira."
            )

        # Certificações
        st.divider()
        st.subheader("🎓 Cursos e certificações")

        for certificacao in plano["certificacoes"]:
            st.write(f"• {certificacao}")

        # Portfólio
        st.subheader("💻 Projetos para o GitHub")

        for projeto in plano["projetos"]:
            st.write(f"• {projeto}")

        st.info(
            "Este plano é uma orientação educacional "
            "baseada nos conhecimentos informados. "
            "Não substitui uma avaliação profissional."
        )

    st.divider()

    if st.button(
        "← Voltar às carreiras",
        use_container_width=True
    ):
        st.session_state.mostrar_roadmap = False
        mudar_etapa(4)


# ==================================================
# RODAPÉ
# ==================================================

st.divider()

st.caption(
    "CareerPath v2.0 | Sistema Especialista de Carreiras em TI "
    "• Projeto acadêmico de Inteligência Artificial"
)
