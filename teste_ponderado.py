from motor_ponderado import calcular_compatibilidade


respostas = {
    "logica": 1,
    "programacao": 1,
    "matematica": 3,
    "design": 2,
    "dados": 4,
    "seguranca": 2,
    "infraestrutura": 3,
    "automacao": 4,
    "testes": 3,
    "gestao": 1,
    "mobile": 2,
    "nuvem": 3
}

resultados = calcular_compatibilidade(respostas)

print("TOP 3 CARREIRAS RECOMENDADAS\n")

for posicao, resultado in enumerate(resultados[:3], start=1):
    print(
        f"{posicao}º - {resultado['carreira']}: "
        f"{resultado['compatibilidade']}%"
    )

    print("Pontos favoráveis:")
    if resultado["pontos_favoraveis"]:
        for ponto in resultado["pontos_favoraveis"]:
            print(f"  + {ponto}")
    else:
        print("  Nenhum ponto favorável identificado.")

    print("Pontos de atenção:")
    if resultado["pontos_atencao"]:
        for ponto in resultado["pontos_atencao"]:
            print(f"  - {ponto}")
    else:
        print("  Nenhum ponto de atenção identificado.")
    print(f"Penalidade aplicada: {resultado['penalidade']} pontos percentuais")

    print()