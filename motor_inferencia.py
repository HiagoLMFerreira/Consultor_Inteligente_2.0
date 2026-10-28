"""Sistema especialista com 25 regras SE-ENTÃO executadas pela Experta."""
# Ajuste de compatibilidade para a dependencia antiga frozendict do Experta.
import collections
import collections.abc
if not hasattr(collections, "Mapping"):
    collections.Mapping = collections.abc.Mapping

from experta import Fact, KnowledgeEngine, Rule
from conhecimento import PERGUNTAS, CARREIRAS


class Resposta(Fact):
    """Fato contendo campo do questionário e resposta escolhida."""
    pass


class ConsultorCarreiras(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.pontos = {nome: 0 for nome in CARREIRAS}
        self.motivos = {nome: [] for nome in CARREIRAS}

    def registrar(self, codigo, carreira, motivo, pontos=2):
        """Guarda a pontuação e a explicação da regra ativada."""
        self.pontos[carreira] += pontos
        self.motivos[carreira].append(f'{codigo}: {motivo}')

    # BACK-END
    @Rule(Resposta(campo='atividade', valor='apis'), Resposta(campo='aspecto', valor='logica'))
    def r01(self):
        self.registrar('R01', 'backend', 'Interesse em APIs e lógica de sistemas.', 3)

    @Rule(Resposta(campo='ambiente', valor='programacao'), Resposta(campo='estudo', valor='apis'))
    def r02(self):
        self.registrar('R02', 'backend', 'Preferência por programação e arquitetura de APIs.', 3)

    # FRONT-END
    @Rule(Resposta(campo='atividade', valor='interfaces'), Resposta(campo='ferramenta', valor='javascript'))
    def r03(self):
        self.registrar('R03', 'frontend', 'Interesse por interfaces e JavaScript.', 3)

    @Rule(Resposta(campo='ambiente', valor='design'), Resposta(campo='aspecto', valor='usabilidade'))
    def r04(self):
        self.registrar('R04', 'frontend', 'Prioriza design e experiência do usuário.', 3)

    # CIÊNCIA DE DADOS
    @Rule(Resposta(campo='matematica', valor='alta'), Resposta(campo='atividade', valor='modelos'))
    def r05(self):
        self.registrar('R05', 'ciencia', 'Alta afinidade matemática e interesse em modelos.', 3)

    @Rule(Resposta(campo='ferramenta', valor='python'), Resposta(campo='estudo', valor='machine_learning'))
    def r06(self):
        self.registrar('R06', 'ciencia', 'Interesse por Python e aprendizado de máquina.', 3)

    @Rule(Resposta(campo='entrega', valor='previsoes'), Resposta(campo='resolver', valor='padroes'))
    def r07(self):
        self.registrar('R07', 'ciencia', 'Gosta de analisar padrões para gerar previsões.', 3)

    # ENGENHARIA DE DADOS
    @Rule(Resposta(campo='ferramenta', valor='sql'), Resposta(campo='aspecto', valor='dados'))
    def r08(self):
        self.registrar('R08', 'engenharia', 'Interesse por SQL e organização dos dados.', 3)

    @Rule(Resposta(campo='atividade', valor='pipelines'), Resposta(campo='estudo', valor='etl'))
    def r09(self):
        self.registrar('R09', 'engenharia', 'Prefere pipelines e processamento ETL.', 3)

    # CIBERSEGURANÇA
    @Rule(Resposta(campo='ferramenta', valor='linux'), Resposta(campo='ambiente', valor='seguranca'))
    def r10(self):
        self.registrar('R10', 'seguranca', 'Afinidade com Linux/redes e segurança.', 3)

    @Rule(Resposta(campo='atividade', valor='seguranca'), Resposta(campo='resolver', valor='riscos'))
    def r11(self):
        self.registrar('R11', 'seguranca', 'Interesse em identificar vulnerabilidades.', 3)

    @Rule(Resposta(campo='estudo', valor='criptografia'), Resposta(campo='aspecto', valor='protecao'))
    def r12(self):
        self.registrar('R12', 'seguranca', 'Prefere criptografia e proteção de sistemas.', 3)

    # DEVOPS
    @Rule(Resposta(campo='atividade', valor='automacao'), Resposta(campo='ambiente', valor='servidores'))
    def r13(self):
        self.registrar('R13', 'devops', 'Interesse por automação e servidores.', 3)

    @Rule(Resposta(campo='ferramenta', valor='docker'), Resposta(campo='estudo', valor='cicd'))
    def r14(self):
        self.registrar('R14', 'devops', 'Afinidade com Docker e CI/CD.', 3)

    @Rule(Resposta(campo='resolver', valor='automatizar'), Resposta(campo='aspecto', valor='operacao'))
    def r15(self):
        self.registrar('R15', 'devops', 'Busca automação e confiabilidade operacional.', 3)

    # NUVEM
    @Rule(Resposta(campo='atividade', valor='nuvem'), Resposta(campo='aspecto', valor='nuvem'))
    def r16(self):
        self.registrar('R16', 'cloud', 'Interesse em infraestrutura de nuvem.', 3)

    @Rule(Resposta(campo='ferramenta', valor='cloud'), Resposta(campo='entrega', valor='escalabilidade'))
    def r17(self):
        self.registrar('R17', 'cloud', 'Afinidade com plataformas cloud e escalabilidade.', 3)

    # MOBILE
    @Rule(Resposta(campo='atividade', valor='mobile'), Resposta(campo='ferramenta', valor='flutter'))
    def r18(self):
        self.registrar('R18', 'mobile', 'Interesse por apps e desenvolvimento mobile.', 3)

    @Rule(Resposta(campo='resolver', valor='apps'), Resposta(campo='entrega', valor='aplicativo'))
    def r19(self):
        self.registrar('R19', 'mobile', 'Prefere criar funcionalidades de aplicativos.', 3)

    # QUALIDADE
    @Rule(Resposta(campo='atividade', valor='testes'), Resposta(campo='resolver', valor='erros'))
    def r20(self):
        self.registrar('R20', 'qa', 'Gosta de testar sistemas e encontrar defeitos.', 3)

    @Rule(Resposta(campo='ferramenta', valor='testes'), Resposta(campo='estudo', valor='testes'))
    def r21(self):
        self.registrar('R21', 'qa', 'Interesse em ferramentas e automação de testes.', 3)

    @Rule(Resposta(campo='aspecto', valor='qualidade'), Resposta(campo='entrega', valor='qualidade'))
    def r22(self):
        self.registrar('R22', 'qa', 'Valoriza validação e prevenção de defeitos.', 3)

    # GESTÃO DE PRODUTOS
    @Rule(Resposta(campo='ambiente', valor='negocios'), Resposta(campo='resolver', valor='prioridades'))
    def r23(self):
        self.registrar('R23', 'produto', 'Interesse em negócios e planejamento.', 3)

    @Rule(Resposta(campo='atividade', valor='produto'), Resposta(campo='aspecto', valor='estrategia'))
    def r24(self):
        self.registrar('R24', 'produto', 'Prefere estratégia e necessidades do cliente.', 3)

    @Rule(Resposta(campo='estudo', valor='agil'), Resposta(campo='objetivo', valor='produtos'))
    def r25(self):
        self.registrar('R25', 'produto', 'Interesse em metodologias ágeis e produtos.', 3)


def analisar_respostas(respostas):
    """Recebe 10 respostas e devolve diagnóstico com motivos rastreáveis."""
    if set(respostas) != set(PERGUNTAS):
        raise ValueError('É necessário responder às 10 perguntas.')
    for campo, valor in respostas.items():
        if valor not in PERGUNTAS[campo][1]:
            raise ValueError(f'Resposta inválida para {campo}: {valor}')

    motor = ConsultorCarreiras()
    motor.reset()
    for campo, valor in respostas.items():
        motor.declare(Resposta(campo=campo, valor=valor))
    motor.run()

    pontuacao_maxima = max(motor.pontos.values())
    if pontuacao_maxima == 0:
        return {
            'carreira': None,
            'mensagem': 'Perfil inconclusivo: nenhuma regra cruzada foi ativada.',
            'motivos': [],
            'pontuacoes': motor.pontos,
            'empate': False,
        }

    empatadas = [c for c, p in motor.pontos.items() if p == pontuacao_maxima]
    # Desempate: preferência explícita da pergunta sobre objetivo profissional.
    mapa_objetivo = {
        'sistemas':'backend', 'experiencias':'frontend', 'ia':'ciencia',
        'dados':'engenharia', 'seguranca':'seguranca', 'automacao':'devops',
        'nuvem':'cloud', 'aplicativos':'mobile', 'qualidade':'qa', 'produtos':'produto'
    }
    objetivo = mapa_objetivo[respostas['objetivo']]
    escolhido = objetivo if objetivo in empatadas else empatadas[0]
    return {
        'carreira': CARREIRAS[escolhido],
        'codigo': escolhido,
        'mensagem': 'Recomendação baseada nas regras acionadas.',
        'motivos': motor.motivos[escolhido],
        'pontuacoes': motor.pontos,
        'empate': len(empatadas) > 1,
        'empatadas': [CARREIRAS[c] for c in empatadas],
    }
