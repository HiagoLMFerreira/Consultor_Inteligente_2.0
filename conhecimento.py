import json
from pathlib import Path

"""Perguntas e respostas usadas pelo motor e pela futura interface Streamlit."""

PERGUNTAS = {
    'matematica': ('Qual é sua afinidade com matemática e estatística?', ['baixa', 'media', 'alta']),
    'atividade': ('Qual atividade você mais gostaria de realizar?', ['apis', 'interfaces', 'modelos', 'pipelines', 'seguranca', 'automacao', 'nuvem', 'mobile', 'testes', 'produto']),
    'ferramenta': ('Qual linguagem ou ferramenta você prefere?', ['python', 'java', 'javascript', 'sql', 'linux', 'docker', 'cloud', 'flutter', 'testes', 'gestao', 'nenhuma']),
    'entrega': ('Qual resultado mais te motivaria?', ['sistema', 'interface', 'previsoes', 'dados', 'protecao', 'automacao', 'escalabilidade', 'aplicativo', 'qualidade', 'produto']),
    'ambiente': ('Qual ambiente desperta mais interesse?', ['programacao', 'design', 'analise', 'dados', 'seguranca', 'servidores', 'nuvem', 'mobile', 'testes', 'negocios']),
    'resolver': ('Como prefere resolver problemas?', ['codigo', 'usuario', 'padroes', 'fluxos', 'riscos', 'automatizar', 'arquitetura', 'apps', 'erros', 'prioridades']),
    'estudo': ('O que gostaria de estudar?', ['apis', 'interfaces', 'machine_learning', 'etl', 'criptografia', 'cicd', 'cloud', 'mobile', 'testes', 'agil']),
    'programacao': ('Como se sente em relação à programação?', ['gosto', 'visual', 'dados', 'integracao', 'investigar', 'planejar', 'iniciante']),
    'aspecto': ('Em que aspecto de um projeto prefere atuar?', ['logica', 'usabilidade', 'inteligencia', 'dados', 'protecao', 'operacao', 'nuvem', 'mobile', 'qualidade', 'estrategia']),
    'objetivo': ('Qual é seu objetivo profissional?', ['sistemas', 'experiencias', 'ia', 'dados', 'seguranca', 'automacao', 'nuvem', 'aplicativos', 'qualidade', 'produtos']),
}

CARREIRAS = {
    'backend': 'Desenvolvimento Back-end',
    'frontend': 'Desenvolvimento Front-end & UI/UX',
    'ciencia': 'Ciência de Dados e Machine Learning',
    'engenharia': 'Engenharia de Dados',
    'seguranca': 'Cibersegurança',
    'devops': 'DevOps & SRE',
    'cloud': 'Computação em Nuvem',
    'mobile': 'Desenvolvimento Mobile',
    'qa': 'Engenharia de Qualidade e Testes (QA)',
    'produto': 'Gestão de Produtos',
}

def carregar_base_conhecimento():
    caminho = Path(__file__).parent / "conhecimento" / "regras_carreiras.json"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    return dados

def validar_base_conhecimento(base):
    perguntas = base.get("perguntas", [])
    carreiras = base.get("carreiras", {})

    if not perguntas:
        raise ValueError("A base não possui perguntas.")

    if len(carreiras) != 10:
        raise ValueError("A base deve conter 10 carreiras.")

    ids_perguntas = [pergunta["id"] for pergunta in perguntas]

    if len(ids_perguntas) != len(set(ids_perguntas)):
        raise ValueError("Existem perguntas com identificadores repetidos.")

    for codigo, carreira in carreiras.items():
        pesos = carreira.get("pesos", {})

        if set(pesos) != set(ids_perguntas):
            raise ValueError(
                f"A carreira {codigo} possui pesos incompletos."
            )

        for peso in pesos.values():
            if type(peso) is not int or not 1 <= peso <= 5:
                raise ValueError(
                    f"A carreira {codigo} possui um peso inválido."
                )

    nomes = base.get("nomes_caracteristicas", {})

    if set(nomes) != set(ids_perguntas):
        raise ValueError("Os nomes das características estão incompletos.")

    penalidades = base.get("penalidades", {})

    for regras in penalidades.values():
        for valor in regras.values():
            if type(valor) not in (int, float) or valor < 0:
                raise ValueError("Existe uma penalidade inválida.")

    print("Base de conhecimento validada com sucesso!")


if __name__ == "__main__":
    base = carregar_base_conhecimento()

    print("Base de conhecimento carregada com sucesso!")
    validar_base_conhecimento(base)
