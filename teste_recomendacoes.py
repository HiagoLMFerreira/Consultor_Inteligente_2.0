"""Teste demonstrativo da análise e do roadmap para as dez carreiras."""
from conhecimento import carregar_base_conhecimento
from recomendacoes import analisar_competencias, gerar_roadmap

base = carregar_base_conhecimento()

for codigo, carreira in base["carreiras"].items():
    # Perfil de teste: conhecimento básico em todas as competências.
    conhecimentos = {chave: 1 for chave in carreira["competencias_junior"]}
    analise = analisar_competencias(codigo, conhecimentos)
    plano = gerar_roadmap(codigo, conhecimentos)

    assert len(analise) == len(conhecimentos)
    assert len(plano["estudos"]) == sum(item["lacuna"] > 0 for item in analise)
    assert all(item["lacuna"] > 0 for item in plano["estudos"])

    print(f"\n{plano['carreira']}")
    for etapa in plano["estudos"]:
        print(f"  {etapa['ordem']}. {etapa['competencia']} (lacuna: {etapa['lacuna']})")
    print("  Certificações/opções:", "; ".join(plano["certificacoes"]))
    print("  Portfólio:", "; ".join(plano["projetos"]))

print("\nAs 10 carreiras passaram pelo teste demonstrativo.")
