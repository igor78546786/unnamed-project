from django.test import TestCase
from django.urls import reverse

class TestesFuncionalidadesCalculadora(TestCase):
    
    def test_pagina_inicial_carrega_corretamente(self):
        url = reverse('pagina_inicial')
        resposta = self.client.get(url)
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'calculadora/pagina_inicial.html')
        self.assertContains(resposta, "Encontrar Raíz de uma Equação")

    def test_formulario_encontrar_raiz_exibe_resultado(self):
        url = reverse('encontrar_raiz')
        dados_formulario = {
            'funcao_texto': 'x**2 - 4',
            'intervalo_a': '0',
            'intervalo_b': '3',
            'metodo': 'bissecao'
        }
        resposta = self.client.post(url, dados_formulario)
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Resultado Encontrado")