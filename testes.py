"""Entrega 4: validação automática de 10 carreiras e cenários de borda.

Execute: python testes.py
O arquivo relatorio_testes.md só é criado quando todos os testes passam.
"""
from collections import Counter
from pathlib import Path
import unittest

from conhecimento import CARREIRAS
from motor_inferencia import analisar_respostas

# Um conjunto completo de respostas válidas, usado como ponto de partida.
BASE = dict(
    matematica='media', atividade='apis', ferramenta='java', entrega='sistema',
    ambiente='programacao', resolver='codigo', estudo='apis',
    programacao='gosto', aspecto='logica', objetivo='sistemas'
)

# Cada persona foi montada para ativar TODAS as regras de sua carreira.
# Estes são cenários elaborados para validar a lógica, não perfis reais de pessoas.
PERSONAS = [
    ('Back-end', 'backend', dict(BASE), {'R01','R02'}),
    ('Front-end', 'frontend', dict(BASE, atividade='interfaces', ferramenta='javascript',
        entrega='interface', ambiente='design', resolver='usuario', estudo='interfaces',
        aspecto='usabilidade', objetivo='experiencias'), {'R03','R04'}),
    ('Ciência de Dados', 'ciencia', dict(BASE, matematica='alta', atividade='modelos',
        ferramenta='python', entrega='previsoes', ambiente='analise', resolver='padroes',
        estudo='machine_learning', aspecto='inteligencia', objetivo='ia'), {'R05','R06','R07'}),
    ('Engenharia de Dados', 'engenharia', dict(BASE, atividade='pipelines',
        ferramenta='sql', entrega='dados', ambiente='dados', resolver='fluxos',
        estudo='etl', aspecto='dados', objetivo='dados'), {'R08','R09'}),
    ('Cibersegurança', 'seguranca', dict(BASE, atividade='seguranca', ferramenta='linux',
        entrega='protecao', ambiente='seguranca', resolver='riscos',
        estudo='criptografia', aspecto='protecao', objetivo='seguranca'), {'R10','R11','R12'}),
    ('DevOps e SRE', 'devops', dict(BASE, atividade='automacao', ferramenta='docker',
        entrega='automacao', ambiente='servidores', resolver='automatizar',
        estudo='cicd', aspecto='operacao', objetivo='automacao'), {'R13','R14','R15'}),
    ('Computação em Nuvem', 'cloud', dict(BASE, atividade='nuvem', ferramenta='cloud',
        entrega='escalabilidade', ambiente='nuvem', resolver='arquitetura',
        estudo='cloud', aspecto='nuvem', objetivo='nuvem'), {'R16','R17'}),
    ('Desenvolvimento Mobile', 'mobile', dict(BASE, atividade='mobile', ferramenta='flutter',
        entrega='aplicativo', ambiente='mobile', resolver='apps',
        estudo='mobile', aspecto='mobile', objetivo='aplicativos'), {'R18','R19'}),
    ('Qualidade e Testes', 'qa', dict(BASE, atividade='testes', ferramenta='testes',
        entrega='qualidade', ambiente='testes', resolver='erros',
        estudo='testes', aspecto='qualidade', objetivo='qualidade'), {'R20','R21','R22'}),
    ('Gestão de Produtos', 'produto', dict(BASE, atividade='produto', ferramenta='gestao',
        entrega='produto', ambiente='negocios', resolver='prioridades',
        estudo='agil', aspecto='estrategia', objetivo='produtos'), {'R23','R24','R25'}),
]


def ids_dos_motivos(resultado):
    """Extrai identificadores R01...R25 das justificativas retornadas."""
    return {texto.split(':', 1)[0] for texto in resultado['motivos']}


class TesteConsultor(unittest.TestCase):
    def test_01_todas_as_dez_personas(self):
        for nome, codigo, respostas, regras_esperadas in PERSONAS:
            with self.subTest(persona=nome):
                resultado = analisar_respostas(respostas)
                self.assertEqual(resultado['codigo'], codigo)
                self.assertEqual(resultado['carreira'], CARREIRAS[codigo])
                self.assertEqual(ids_dos_motivos(resultado), regras_esperadas)
                self.assertEqual(resultado['pontuacoes'][codigo], 3 * len(regras_esperadas))
                self.assertFalse(resultado['empate'])
                self.assertEqual(len(resultado['pontuacoes']), 10)

    def test_02_cobertura_das_25_regras(self):
        ativadas = set()
        for _, _, respostas, _ in PERSONAS:
            ativadas.update(ids_dos_motivos(analisar_respostas(respostas)))
        esperadas = {f'R{i:02}' for i in range(1, 26)}
        self.assertEqual(ativadas, esperadas)

    def test_03_desempate_usando_objetivo_profissional(self):
        # R01 -> backend e R14 -> devops (ambos com 3 pontos).
        respostas = dict(BASE, ferramenta='docker', estudo='cicd', objetivo='automacao')
        resultado = analisar_respostas(respostas)
        self.assertTrue(resultado['empate'])
        self.assertEqual(resultado['codigo'], 'devops')
        self.assertEqual(resultado['pontuacoes']['backend'], 3)
        self.assertEqual(resultado['pontuacoes']['devops'], 3)
        self.assertEqual(set(resultado['empatadas']),
                         {CARREIRAS['backend'], CARREIRAS['devops']})
        self.assertEqual(ids_dos_motivos(resultado), {'R14'})

    def test_04_desempate_fallback_estavel(self):
        respostas = dict(BASE, ferramenta='docker', estudo='cicd', objetivo='produtos')
        resultado = analisar_respostas(respostas)
        self.assertTrue(resultado['empate'])
        self.assertEqual(resultado['codigo'], 'backend')

    def test_05_sem_regras_acionadas(self):
        respostas = dict(BASE, matematica='baixa', ferramenta='nenhuma',
            entrega='produto', ambiente='analise', resolver='fluxos',
            estudo='cloud', programacao='iniciante', aspecto='mobile', objetivo='produtos')
        resultado = analisar_respostas(respostas)
        self.assertIsNone(resultado['carreira'])
        self.assertFalse(resultado['motivos'])
        self.assertEqual(sum(resultado['pontuacoes'].values()), 0)
        self.assertFalse(resultado['empate'])

    def test_06_resposta_ausente(self):
        respostas = dict(BASE)
        del respostas['matematica']
        with self.assertRaises(ValueError):
            analisar_respostas(respostas)

    def test_07_resposta_invalida(self):
        with self.assertRaises(ValueError):
            analisar_respostas(dict(BASE, matematica='muito_alta'))

    def test_08_campo_extra(self):
        with self.assertRaises(ValueError):
            analisar_respostas(dict(BASE, idade='20'))

    def test_09_chamadas_independentes(self):
        primeiro = analisar_respostas(PERSONAS[0][2])
        segundo = analisar_respostas(PERSONAS[1][2])
        terceiro = analisar_respostas(PERSONAS[0][2])
        self.assertEqual(primeiro['pontuacoes'], terceiro['pontuacoes'])
        self.assertEqual(primeiro['motivos'], terceiro['motivos'])
        self.assertNotEqual(primeiro['codigo'], segundo['codigo'])


def salvar_relatorio():
    linhas = [
        '# Relatório de validação — Entrega 4', '',
        'Este documento registra cenários automatizados de teste elaborados para o projeto.',
        'Não constitui uma pesquisa com profissionais reais ou uma validação científica de orientação de carreira.', '',
        '## Personas testadas', '',
        '| Persona | Carreira esperada | Carreira obtida | Regras ativadas | Situação |',
        '|---|---|---|---|---|',
    ]
    contagem = Counter()
    for nome, esperado, respostas, _ in PERSONAS:
        resultado = analisar_respostas(respostas)
        regras = sorted(ids_dos_motivos(resultado))
        contagem.update(regras)
        status = 'APROVADO' if resultado['codigo'] == esperado else 'REPROVADO'
        linhas.append(f'| {nome} | {CARREIRAS[esperado]} | '
                      f'{resultado["carreira"]} | {", ".join(regras)} | {status} |')
    linhas += ['', '## Cobertura de regras', '',
        f'{len(contagem)} de 25 regras acionadas pelas dez personas.', '',
        '## Testes adicionais', '',
        '- Desempate pelo objetivo profissional',
        '- Desempate sem objetivo correspondente (prioridade fixa da implementação)',
        '- Perfil inconclusivo sem regras acionadas',
        '- Resposta ausente, resposta inválida e campo inesperado',
        '- Independência entre execuções consecutivas', '',
        '**Resultado:** todos os testes automatizados passaram na execução que gerou este relatório.', '',
        '### Limites da validação', '',
        'Estes testes confirmam o comportamento do código nos casos definidos, '
        'não a qualidade de recomendações para todos os usuários. '
        'Ainda é útil fazer testes manuais na interface Streamlit.', ''
    ]
    Path(__file__).with_name('relatorio_testes.md').write_text('\n'.join(linhas), encoding='utf-8')


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TesteConsultor)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        salvar_relatorio()
        print('\n[OK] Todas as 10 carreiras e as 25 regras foram cobertas.')
        print('[OK] Relatório gerado: relatorio_testes.md')
    else:
        print('\n[ERRO] Testes falharam; corrija antes da Entrega 5.')
        raise SystemExit(1)
