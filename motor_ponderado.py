from conhecimento import carregar_base_conhecimento

def gerar_justificativas(respostas, pesos, nomes):
    pontos_favoraveis = []
    pontos_atencao = []

    for caracteristica, resposta in respostas.items():
        peso = pesos[caracteristica]
        nome = nomes.get(caracteristica, caracteristica)

        # Característica importante com alta afinidade
        if peso >= 4 and resposta >= 4:
            pontos_favoraveis.append(nome)

        # Característica importante com baixa afinidade
        elif peso >= 4 and resposta <= 2:
            pontos_atencao.append(nome)


    return pontos_favoraveis, pontos_atencao

def calcular_penalidade(respostas, pesos, regras_penalidade):
    penalidade = 0

    for caracteristica, resposta in respostas.items():
        peso = str(pesos[caracteristica])
        resposta = str(resposta)

        regras_peso = regras_penalidade.get(peso, {})
        penalidade += regras_peso.get(resposta, 0)

    return penalidade

def calcular_compatibilidade(respostas):
    base = carregar_base_conhecimento()
    carreiras = base["carreiras"]
    perguntas = base["perguntas"]

    # Identificadores das perguntas do JSON
    ids_perguntas = {pergunta["id"] for pergunta in perguntas}

    # Verifica se todas as perguntas foram respondidas
    if set(respostas) != ids_perguntas:
        raise ValueError("É necessário responder todas as perguntas.")

    # Verifica se as respostas estão entre 1 e 5
    for valor in respostas.values():
        if type(valor) is not int or not 1 <= valor <= 5:
            raise ValueError("As respostas devem ser números de 1 a 5.")

    resultados = []

    # Calcula a compatibilidade para cada carreira
    for codigo, carreira in carreiras.items():
        pesos = carreira["pesos"]

        pontuacao = 0
        soma_pesos = 0

        for pergunta, resposta in respostas.items():
            peso = pesos[pergunta]

            pontuacao += (resposta - 1) * peso
            soma_pesos += peso

        # Normaliza o resultado para uma escala de 0 a 100%
        percentual = (pontuacao / (4 * soma_pesos)) * 100

        penalidade = calcular_penalidade(
            respostas,
            pesos,
            base["penalidades"]
        )

        percentual = max(0, percentual - penalidade)

        favoraveis, atencao = gerar_justificativas(
            respostas,
            pesos,
            base["nomes_caracteristicas"]
        )

        resultados.append({
            "codigo": codigo,
            "carreira": carreira["nome"],
            "compatibilidade": round(percentual, 2),
            "pontos_favoraveis": favoraveis,
            "pontos_atencao": atencao,
            "penalidade": penalidade
        })

    # Organiza da maior para a menor compatibilidade
    resultados.sort(
        key=lambda resultado: resultado["compatibilidade"],
        reverse=True
    )

    return resultados