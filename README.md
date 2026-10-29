# Consultor Inteligente de Carreiras em TI — v2.0

Projeto acadêmico desenvolvido para a disciplina de Inteligência Artificial do curso de Ciência da Computação.

O sistema funciona como um consultor de carreiras em TI, utilizando regras, pesos e respostas do usuário para identificar as áreas de tecnologia mais compatíveis com seu perfil.

Além de recomendar carreiras, o programa identifica competências que precisam ser desenvolvidas e gera um plano de estudos personalizado.

## Funcionalidades

- Questionário interativo com 12 perguntas de afinidade.
- Respostas em escala de 1 a 5.
- Análise de compatibilidade com 10 carreiras de TI.
- Ranking das três carreiras mais compatíveis.
- Cálculo de compatibilidade percentual com pesos e penalidades.
- Justificativas com pontos favoráveis e pontos de atenção.
- Identificação de lacunas de conhecimento para o nível Júnior.
- Roadmap personalizado com conteúdos de estudo, certificações opcionais e sugestões de projetos para o GitHub.
- Interface web desenvolvida com Streamlit.

## Tecnologias utilizadas

- **Python:** linguagem principal do projeto.
- **JSON:** armazenamento da base de conhecimento.
- **Streamlit:** desenvolvimento da interface web.
- **Pandas:** organização e apresentação dos dados.
- **Unittest:** execução dos testes automatizados.

## Estrutura do projeto

```text
Consultor_Inteligente_2.0/
│
├── conhecimento/
│   └── regras_carreiras.json
│
├── app.py
├── conhecimento.py
├── motor_ponderado.py
├── recomendacoes.py
├── testes_v2.py
├── teste_ponderado.py
├── teste_recomendacoes.py
├── requirements.txt
└── README.md
```

### Descrição dos arquivos

- `app.py`: interface web, questionário, resultados e plano de desenvolvimento.
- `conhecimento.py`: carregamento e validação da base JSON.
- `regras_carreiras.json`: perguntas, carreiras, pesos, penalidades, competências e roadmaps.
- `motor_ponderado.py`: cálculo das compatibilidades e geração das justificativas.
- `recomendacoes.py`: análise das competências e geração dos planos de estudo.
- `testes_v2.py`: testes automatizados de funcionamento e robustez.
- `teste_ponderado.py`: demonstração do cálculo de compatibilidade.
- `teste_recomendacoes.py`: demonstração dos roadmaps das dez carreiras.
- `requirements.txt`: dependências necessárias para executar o projeto.

## Instalação e execução

Recomenda-se utilizar Python 3.10 ou superior, em uma versão compatível com as dependências instaladas.

**1.** Abra a pasta do projeto no PyCharm ou em outro editor Python.

**2.** Crie um ambiente virtual, caso ainda não tenha:

```powershell
python -m venv .venv
```

**3.** Ative o ambiente virtual no Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

**4.** Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

**5.** Execute a aplicação:

```powershell
python -m streamlit run app.py
```

A interface será aberta no navegador, normalmente em `http://localhost:8501`.

Para encerrar a aplicação, pressione `Ctrl+C` no terminal.

## Funcionamento do sistema

O usuário começa preenchendo seu perfil e respondendo às 12 perguntas sobre interesses em tecnologia.

As respostas utilizam uma escala de 1 a 5 e são processadas pelo motor de inferência ponderado.

Cada carreira possui pesos específicos para características como programação, lógica, matemática, design, infraestrutura e segurança.

O motor calcula a compatibilidade considerando esses pesos e aplica penalidades quando existe baixa afinidade com características importantes.

Ao final, o sistema apresenta as três carreiras com maior compatibilidade, juntamente com justificativas e um gráfico comparativo das dez carreiras.

### Análise de competências

Depois de visualizar o ranking, o usuário pode escolher uma das três carreiras recomendadas.

O sistema apresenta as competências consideradas necessárias para o nível Júnior e solicita que o usuário informe seu conhecimento atual.

A diferença entre o nível atual e o nível necessário permite identificar as lacunas de conhecimento.

### Roadmap personalizado

Com base nas lacunas identificadas, o sistema gera um plano de desenvolvimento que contém:

- Conteúdos organizados em uma sequência de estudos.
- Sugestões de certificações e cursos.
- Ideias de projetos para desenvolver e publicar no GitHub.

As informações utilizadas são carregadas do JSON, mantendo a base de conhecimento separada das funções Python.

## Testes

O projeto possui testes automatizados e testes demonstrativos.

Para executar os testes automatizados:

```powershell
python testes_v2.py
```

São oito testes que verificam:

1. Ranking completo das dez carreiras.
2. Validade dos percentuais e ordenação.
3. Perfil com afinidade máxima.
4. Perfil com afinidade mínima.
5. Perfil ambíguo com empate.
6. Aplicação de penalidades.
7. Tratamento de respostas inválidas.
8. Geração de roadmaps para as dez carreiras.

Também é possível executar os testes demonstrativos:

```powershell
python teste_ponderado.py
python teste_recomendacoes.py
```

## Observações

O sistema utiliza regras e pesos definidos para fins educacionais. Os percentuais representam uma estimativa de compatibilidade segundo o modelo desenvolvido e não uma probabilidade real de sucesso profissional.

Os níveis de competência também são referências educacionais e não substituem avaliações técnicas ou profissionais.

Em situações de empate, o motor mantém a ordem original das carreiras cadastradas no JSON. Essa ordem não significa que uma carreira seja necessariamente mais adequada que outra.

O projeto foi desenvolvido como uma evolução de um sistema especialista anterior, substituindo as regras categóricas da Experta por um motor próprio de pontuação ponderada, com base de conhecimento externa e interface interativa.