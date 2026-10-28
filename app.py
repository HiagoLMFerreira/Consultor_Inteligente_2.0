"""Interface Streamlit do Consultor Inteligente de Carreiras em TI."""
import streamlit as st
from conhecimento import PERGUNTAS, CARREIRAS
from motor_inferencia import analisar_respostas

# Os codigos abaixo sao os mesmos de conhecimento.py; so os textos mudam.
ROTULOS = {
    "matematica": {"baixa": "Baixa", "media": "Média", "alta": "Alta"},
    "atividade": {"apis": "Desenvolver APIs e sistemas", "interfaces": "Criar interfaces e layouts", "modelos": "Analisar dados e criar modelos", "pipelines": "Construir pipelines de dados", "seguranca": "Investigar segurança digital", "automacao": "Automatizar processos", "nuvem": "Trabalhar com infraestrutura em nuvem", "mobile": "Criar aplicativos", "testes": "Testar e melhorar programas", "produto": "Planejar produtos digitais"},
    "ferramenta": {"python": "Python", "java": "Java ou C#", "javascript": "JavaScript / HTML / CSS", "sql": "SQL e bancos de dados", "linux": "Linux e redes", "docker": "Docker e CI/CD", "cloud": "AWS / Azure / GCP", "flutter": "Flutter / Kotlin / Swift", "testes": "Ferramentas de testes", "gestao": "Ferramentas de gestão", "nenhuma": "Nenhuma, estou começando"},
    "entrega": {"sistema": "Um sistema que funciona bem", "interface": "Uma interface fácil de usar", "previsoes": "Previsões baseadas em dados", "dados": "Dados organizados", "protecao": "Sistemas protegidos", "automacao": "Processos automatizados", "escalabilidade": "Infraestrutura escalável", "aplicativo": "Um aplicativo para celular", "qualidade": "Um software com qualidade", "produto": "Um produto útil ao cliente"},
    "ambiente": {"programacao": "Programação", "design": "Design e experiência do usuário", "analise": "Análise e pesquisa", "dados": "Bancos de dados", "seguranca": "Segurança e redes", "servidores": "Servidores e automação", "nuvem": "Serviços de nuvem", "mobile": "Aplicativos móveis", "testes": "Testes e qualidade", "negocios": "Planejamento e negócios"},
    "resolver": {"codigo": "Escrevendo código", "usuario": "Pensando no usuário", "padroes": "Encontrando padrões nos dados", "fluxos": "Organizando fluxos", "riscos": "Procurando riscos", "automatizar": "Automatizando tarefas", "arquitetura": "Planejando estruturas", "apps": "Criando funções em aplicativos", "erros": "Encontrando erros", "prioridades": "Definindo prioridades"},
    "estudo": {"apis": "APIs e arquitetura de software", "interfaces": "Interfaces e UI/UX", "machine_learning": "Machine Learning", "etl": "ETL e engenharia de dados", "criptografia": "Criptografia e pentesting", "cicd": "Integração e entrega contínua (CI/CD)", "cloud": "Arquitetura de nuvem", "mobile": "Desenvolvimento mobile", "testes": "Testes automatizados", "agil": "Metodologias ágeis"},
    "programacao": {"gosto": "Gosto de programar", "visual": "Gosto mais da parte visual", "dados": "Gosto de analisar dados com código", "integracao": "Gosto de integrar e automatizar", "investigar": "Gosto de investigar e testar", "planejar": "Prefiro planejar soluções", "iniciante": "Ainda estou aprendendo"},
    "aspecto": {"logica": "Lógica do sistema", "usabilidade": "Usabilidade", "inteligencia": "Inteligência dos dados", "dados": "Armazenamento de dados", "protecao": "Proteção", "operacao": "Operação e disponibilidade", "nuvem": "Infraestrutura na nuvem", "mobile": "Experiência mobile", "qualidade": "Qualidade", "estrategia": "Estratégia"},
    "objetivo": {"sistemas": "Construir sistemas robustos", "experiencias": "Criar boas experiências digitais", "ia": "Criar soluções inteligentes", "dados": "Estruturar dados", "seguranca": "Proteger sistemas", "automacao": "Melhorar automação", "nuvem": "Projetar sistemas na nuvem", "aplicativos": "Desenvolver apps", "qualidade": "Garantir qualidade de software", "produtos": "Liderar produtos digitais"},
}

st.set_page_config(page_title="Consultor de Carreiras em TI", page_icon="🧠", layout="centered")
st.markdown("""<style>
.block-container {max-width: 850px; padding-top: 2.2rem;}
.hero {background: linear-gradient(110deg,#162943,#283e67); color:white; padding: 25px 28px; border-radius: 16px; margin-bottom: 22px;}
.hero h1 {font-size: 2rem; margin:0 0 10px 0; color:white;}
.hero p {color:#e5edf8; margin:0;}
.mini {color:#65758b; font-size:.9rem;}
</style>""", unsafe_allow_html=True)
st.markdown("""<div class="hero"><h1>🧠 Consultor Inteligente de Carreiras em TI</h1>
<p>Descubra uma trilha profissional compatível com seus interesses usando um sistema especialista baseado em regras.</p></div>""", unsafe_allow_html=True)
st.caption("Projeto acadêmico · Inteligência Artificial · UNIPAC")

st.markdown("### Seu perfil profissional")
st.write("Responda às 10 perguntas. Não existem respostas certas ou erradas.")

# Utilizamos um formulário único para enviar todas as respostas ao mesmo tempo.
respostas = {}
with st.form("formulario_perfil"):
    for indice, (campo, (pergunta, opcoes)) in enumerate(PERGUNTAS.items(), start=1):
        st.markdown(f"**{indice:02d}. {pergunta}**")
        respostas[campo] = st.radio(
            pergunta,
            options=opcoes,
            format_func=lambda opcao, campo=campo: ROTULOS[campo].get(opcao, opcao),
            index=None,
            key=f"resposta_{campo}",
            label_visibility="collapsed",
        )
        if indice < len(PERGUNTAS):
            st.divider()
    enviar = st.form_submit_button("🔎 Analisar meu perfil", use_container_width=True, type="primary")

if enviar:
    faltando = [campo for campo, resposta in respostas.items() if resposta is None]
    if faltando:
        st.warning(f"Responda todas as perguntas antes de continuar. Faltam {len(faltando)} resposta(s).")
    else:
        try:
            st.session_state["resultado"] = analisar_respostas(respostas)
        except Exception as erro:
            st.error(f"Não foi possível analisar as respostas: {erro}")
            st.session_state.pop("resultado", None)

if "resultado" in st.session_state:
    resultado = st.session_state["resultado"]
    st.divider()
    st.markdown("## 📌 Resultado da análise")
    if resultado["carreira"] is None:
        st.info(resultado["mensagem"])
        st.write("Tente revisar as preferências e escolher opções que reflitam melhor seus interesses.")
    else:
        st.success(f"### {resultado['carreira']}")
        st.write("**Por que essa carreira foi recomendada?**")
        for motivo in resultado["motivos"]:
            st.write(f"• {motivo}")
        if resultado["empate"]:
            st.warning("Houve empate na pontuação entre: " + ", ".join(resultado["empatadas"]) + ". O motor aplicou o critério de desempate definido no código.")
    st.markdown("### Pontuação por carreira")
    pontuacoes = sorted(resultado["pontuacoes"].items(), key=lambda item: (-item[1], item[0]))
    maximo = max((p for _, p in pontuacoes), default=0)
    for codigo, pontos in pontuacoes:
        st.write(f"**{CARREIRAS[codigo]}:** {pontos} ponto(s)")
        st.progress(pontos / maximo if maximo else 0)
    st.caption("Pontuações representam regras ativadas, não percentuais de aptidão ou garantia de sucesso na carreira.")
    st.info("Esta recomendação é orientativa e baseada nas regras programadas. Não substitui orientação profissional.")
