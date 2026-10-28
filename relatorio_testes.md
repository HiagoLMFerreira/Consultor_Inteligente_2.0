# Relatório de validação — Entrega 4

Este documento registra cenários automatizados de teste elaborados para o projeto.
Não constitui uma pesquisa com profissionais reais ou uma validação científica de orientação de carreira.

## Personas testadas

| Persona | Carreira esperada | Carreira obtida | Regras ativadas | Situação |
|---|---|---|---|---|
| Back-end | Desenvolvimento Back-end | Desenvolvimento Back-end | R01, R02 | APROVADO |
| Front-end | Desenvolvimento Front-end & UI/UX | Desenvolvimento Front-end & UI/UX | R03, R04 | APROVADO |
| Ciência de Dados | Ciência de Dados e Machine Learning | Ciência de Dados e Machine Learning | R05, R06, R07 | APROVADO |
| Engenharia de Dados | Engenharia de Dados | Engenharia de Dados | R08, R09 | APROVADO |
| Cibersegurança | Cibersegurança | Cibersegurança | R10, R11, R12 | APROVADO |
| DevOps e SRE | DevOps & SRE | DevOps & SRE | R13, R14, R15 | APROVADO |
| Computação em Nuvem | Computação em Nuvem | Computação em Nuvem | R16, R17 | APROVADO |
| Desenvolvimento Mobile | Desenvolvimento Mobile | Desenvolvimento Mobile | R18, R19 | APROVADO |
| Qualidade e Testes | Engenharia de Qualidade e Testes (QA) | Engenharia de Qualidade e Testes (QA) | R20, R21, R22 | APROVADO |
| Gestão de Produtos | Gestão de Produtos | Gestão de Produtos | R23, R24, R25 | APROVADO |

## Cobertura de regras

25 de 25 regras acionadas pelas dez personas.

## Testes adicionais

- Desempate pelo objetivo profissional
- Desempate sem objetivo correspondente (prioridade fixa da implementação)
- Perfil inconclusivo sem regras acionadas
- Resposta ausente, resposta inválida e campo inesperado
- Independência entre execuções consecutivas

**Resultado:** todos os testes automatizados passaram na execução que gerou este relatório.

### Limites da validação

Estes testes confirmam o comportamento do código nos casos definidos, não a qualidade de recomendações para todos os usuários. Ainda é útil fazer testes manuais na interface Streamlit.
