# Consultor Inteligente de Carreiras em TI — Entrega 3

Projeto acadêmico de Inteligência Artificial: sistema especialista baseado em 25 regras de inferência com Experta e interface em Streamlit.

## Execução no PyCharm (Windows)

1. Abra esta pasta como projeto.
2. Crie/selecione um ambiente virtual Python.
3. No terminal do projeto, execute:

```powershell
python -m pip install -r requirements.txt
python testes.py
python -m streamlit run app.py
```

A aplicação abrirá no navegador (em geral `http://localhost:8501`). Para parar, use `Ctrl+C` no terminal.

## Arquivos

- `conhecimento.py`: perguntas e carreiras.
- `motor_inferencia.py`: fatos, 25 regras e seleção do resultado.
- `app.py`: questionário e resultados no Streamlit.
- `exemplo_console.py`: alternativa de execução no terminal.
- `testes.py`: quatro personas da validação inicial.
- `requirements.txt`: bibliotecas.

## Funcionamento

O Streamlit envia dez respostas ao método `analisar_respostas`. O motor declara os fatos, executa as regras (`@Rule`) e retorna carreira, justificativas, pontuações e possíveis empates. Se nenhuma regra cruzada for ativada, o resultado é inconclusivo.

## Observações

A biblioteca Experta utiliza uma dependência antiga; `motor_inferencia.py` contém uma pequena correção de compatibilidade para `collections.Mapping`. As 25 regras da Entrega 2 foram preservadas. Os quatro testes iniciais não substituem os testes completos das dez carreiras, previstos na Entrega 4.


## Entrega 4: testes ampliados

Execute no terminal do PyCharm, com o ambiente virtual ativado:

```powershell
python testes.py
```

São 9 grupos de testes automatizados: dez personas representando todas as carreiras, cobertura das 25 regras, dois casos de empate, perfil inconclusivo, entradas inválidas e independência entre execuções. O relatório `relatorio_testes.md` é gerado **somente depois** que os testes passam.

O desempate, quando o objetivo profissional não favorece nenhum dos empatados, utiliza a ordem fixa das carreiras no dicionário de conhecimento. Isso é uma limitação conhecida da lógica atual, e não uma evidência de maior adequação da primeira carreira.
