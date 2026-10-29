
import unittest

from conhecimento import carregar_base_conhecimento
from motor_ponderado import calcular_compatibilidade
from recomendacoes import analisar_competencias, gerar_roadmap


class TestesConsultorV2(unittest.TestCase):

    def setUp(self):
        # Carrega os dados antes de cada teste
        self.base = carregar_base_conhecimento()

        self.perguntas = [
            pergunta["id"]
            for pergunta in self.base["perguntas"]
        ]

    def criar_perfil(self, valor=3):
        # Cria um perfil com a mesma resposta para todas as perguntas
        return {
            pergunta: valor
            for pergunta in self.perguntas
        }

    def test_01_ranking_completo(self):
        respostas = self.criar_perfil()
        resultados = calcular_compatibilidade(respostas)

        self.assertEqual(len(resultados), 10)

        codigos = [item["codigo"] for item in resultados]

        self.assertEqual(len(set(codigos)), 10)

    def test_02_percentuais_validos(self):
        respostas = self.criar_perfil(4)
        resultados = calcular_compatibilidade(respostas)

        percentuais = [
            item["compatibilidade"]
            for item in resultados
        ]

        for percentual in percentuais:
            self.assertGreaterEqual(percentual, 0)
            self.assertLessEqual(percentual, 100)

        self.assertEqual(
            percentuais,
            sorted(percentuais, reverse=True)
        )

    def test_03_afinidade_maxima(self):
        respostas = self.criar_perfil(5)
        resultados = calcular_compatibilidade(respostas)

        for resultado in resultados:
            self.assertAlmostEqual(
                resultado["compatibilidade"], 100
            )
            self.assertEqual(resultado["penalidade"], 0)

    def test_04_afinidade_minima(self):
        respostas = self.criar_perfil(1)
        resultados = calcular_compatibilidade(respostas)

        for resultado in resultados:
            self.assertEqual(
                resultado["compatibilidade"], 0
            )

    def test_05_perfil_ambiguo(self):
        # Perfil com interesse moderado em todas as áreas
        respostas = self.criar_perfil(3)
        resultados = calcular_compatibilidade(respostas)

        for resultado in resultados:
            self.assertAlmostEqual(
                resultado["compatibilidade"], 50
            )

        # Verifica se os resultados empatados aparecem
        self.assertEqual(len(resultados), 10)

    def test_06_penalidades(self):
        respostas = self.criar_perfil(5)

        # Baixa afinidade com programação
        respostas["programacao"] = 1

        resultados = calcular_compatibilidade(respostas)

        backend = next(
            item for item in resultados
            if item["codigo"] == "backend"
        )

        self.assertEqual(backend["penalidade"], 5)

        self.assertIn(
            "Programação",
            backend["pontos_atencao"]
        )

        self.assertLess(
            backend["compatibilidade"], 100
        )

    def test_07_respostas_invalidas(self):
        respostas = self.criar_perfil()

        respostas["logica"] = 6

        with self.assertRaises(ValueError):
            calcular_compatibilidade(respostas)

        respostas = self.criar_perfil()
        del respostas["logica"]

        with self.assertRaises(ValueError):
            calcular_compatibilidade(respostas)

    def test_08_roadmaps(self):
        # Percorre todas as carreiras do JSON
        for codigo, carreira in self.base["carreiras"].items():

            with self.subTest(carreira=codigo):
                competencias = carreira["competencias_junior"]

                conhecimentos = {
                    chave: 1
                    for chave in competencias
                }

                analise = analisar_competencias(
                    codigo, conhecimentos
                )

                plano = gerar_roadmap(
                    codigo, conhecimentos
                )

                self.assertEqual(
                    len(analise),
                    len(competencias)
                )

                self.assertIn("estudos", plano)
                self.assertIn("certificacoes", plano)
                self.assertIn("projetos", plano)

                for item in analise:
                    self.assertGreaterEqual(
                        item["lacuna"], 0
                    )

                # Verifica também um usuário com nível máximo
                conhecimentos_maximos = {
                    chave: 5
                    for chave in competencias
                }

                analise_maxima = analisar_competencias(
                    codigo, conhecimentos_maximos
                )

                plano_maximo = gerar_roadmap(
                    codigo, conhecimentos_maximos
                )

                self.assertTrue(
                    all(
                        item["lacuna"] == 0
                        for item in analise_maxima
                    )
                )

                self.assertEqual(
                    len(plano_maximo["estudos"]), 0
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
