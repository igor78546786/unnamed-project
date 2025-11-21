from django.test import TestCase
from django.urls import reverse
from .models import Sessao

class TestesFuncionalidadesCalculadora(TestCase):
    
    def test_pagina_inicial_carrega(self):
        url = reverse('pagina_inicial')
        resposta = self.client.get(url)
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Encontrar Raíz")

    def test_calculo_raiz_bissecao(self):
        url = reverse('encontrar_raiz')
        dados = {
            'funcao_texto': '2x - 4',
            'intervalo_a': '0',
            'intervalo_b': '4',
            'metodo': 'bissecao'
        }
        resposta = self.client.post(url, dados)
        
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.context['resultado'], 2.0)
        self.assertIn('dados_sessao_atual', self.client.session)

    def test_calculo_sistema_gauss(self):
        url = reverse('sistemas_lineares')
        dados = {
            'matrix_rows': 2,
            'matrix_cols': 2,
            'metodo': 'gauss',
            'a_0_0': 1, 'a_0_1': 1, 'b_0': 2,
            'a_1_0': 1, 'a_1_1': -1, 'b_1': 0
        }
        resposta = self.client.post(url, dados)
        
        self.assertEqual(resposta.status_code, 200)
        solucao = resposta.context['solucao']
        self.assertAlmostEqual(solucao[0], 1.0)
        self.assertAlmostEqual(solucao[1], 1.0)

    def test_salvar_sessao_funciona(self):
        sessao = self.client.session
        sessao['dados_sessao_atual'] = {
            'tipo': 'raiz',
            'metodo': 'bissecao',
            'inputs': {'funcao': 'x'},
            'outputs': {'resultado': 0}
        }
        sessao.save()

        url = reverse('salvar_sessao')
        resposta = self.client.get(url)

        self.assertRedirects(resposta, reverse('historico'))
        self.assertTrue(Sessao.objects.exists())

    def test_carregar_sessao(self):
        sessao_salva = Sessao.objects.create(
            tipo_ferramenta='raiz',
            metodo='bissecao',
            dados_input={'funcao_texto': 'x**2'},
            dados_output={'resultado': 0}
        )

        url = reverse('carregar_sessao', args=[sessao_salva.id])
        resposta = self.client.get(url)

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.context['inputs']['funcao_texto'], 'x**2')

    def test_exportar_relatorio(self):
        sessao = self.client.session
        sessao['relatorio_download'] = "Conteúdo do Relatório Teste"
        sessao.save()

        url = reverse('exportar_relatorio')
        resposta = self.client.get(url)

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta['Content-Type'], 'text/plain')
        self.assertIn('attachment', resposta['Content-Disposition'])
        self.assertEqual(resposta.content.decode(), "Conteúdo do Relatório Teste")