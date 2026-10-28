from conhecimento import PERGUNTAS
from motor_inferencia import analisar_respostas

respostas = {}
for campo, (pergunta, opcoes) in PERGUNTAS.items():
    print('\n' + pergunta)
    for i, opcao in enumerate(opcoes, 1):
        print(f'{i}. {opcao}')
    while True:
        escolha = input('Escolha o número da resposta: ').strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(opcoes):
            respostas[campo] = opcoes[int(escolha) - 1]
            break
        print('Opção inválida. Tente novamente.')

resultado = analisar_respostas(respostas)
print('\nRESULTADO:', resultado['carreira'] or resultado['mensagem'])
for motivo in resultado['motivos']:
    print(' -', motivo)
if resultado['empate']:
    print('Houve empate entre:', ', '.join(resultado['empatadas']))
