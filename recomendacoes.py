"""Análise de competências e plano de estudos baseado no JSON."""
from conhecimento import carregar_base_conhecimento


def analisar_competencias(carreira, conhecimentos):
    base = carregar_base_conhecimento()
    if carreira not in base["carreiras"]:
        raise ValueError("Carreira não encontrada.")

    competencias = base["carreiras"][carreira].get("competencias_junior", {})
    if not competencias:
        raise ValueError("Carreira sem competências cadastradas.")
    if set(conhecimentos) != set(competencias):
        raise ValueError("Informe todas as competências, sem chaves extras.")

    resultado = []
    for codigo, dados in competencias.items():
        atual = conhecimentos[codigo]
        necessario = dados["nivel_necessario"]
        if type(atual) is not int or not 1 <= atual <= 5:
            raise ValueError(f"Nível inválido para {codigo}: use inteiros de 1 a 5.")
        lacuna = max(0, necessario - atual)
        resultado.append({
            "codigo": codigo,
            "competencia": dados["nome"],
            "nivel_atual": atual,
            "nivel_necessario": necessario,
            "lacuna": lacuna,
            "status": "Precisa estudar" if lacuna > 0 else "Requisito atingido",
        })
    return sorted(resultado, key=lambda item: item["lacuna"], reverse=True)


def gerar_roadmap(carreira, conhecimentos):
    """Seleciona somente estudos com lacuna, respeitando a ordem pedagógica."""
    base = carregar_base_conhecimento()
    if carreira not in base["carreiras"]:
        raise ValueError("Carreira não encontrada.")

    dados = base["carreiras"][carreira]
    analise = analisar_competencias(carreira, conhecimentos)
    configuracao = dados.get("roadmap", {})
    estudos_json = configuracao.get("estudos", {})
    if set(estudos_json) != set(dados["competencias_junior"]):
        raise ValueError("O roadmap deve ter um estudo para cada competência.")

    estudos = []
    for item in analise:
        if item["lacuna"] == 0:
            continue
        etapa = estudos_json[item["codigo"]]
        estudos.append({
            "competencia": item["competencia"],
            "ordem": etapa["ordem"],
            "conteudo": etapa["conteudo"],
            "lacuna": item["lacuna"],
        })

    estudos.sort(key=lambda item: item["ordem"])
    return {
        "carreira": dados["nome"],
        "estudos": estudos,
        "certificacoes": configuracao.get("certificacoes", []) if estudos else [],
        "projetos": configuracao.get("projetos", []) if estudos else [],
        "competencias_atendidas": sum(item["lacuna"] == 0 for item in analise),
        "total_competencias": len(analise),
    }
