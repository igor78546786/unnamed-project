from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Analise

class TestesFuncionalidadesCalculadora(TestCase):
    def test_pagina_inicial_carrega_corretamente(self):
        url = reverse('pagina_inicial')
        resposta = self.client.get(url)

        self.assertEqual(resposta.status_code, 200) 
        self.assertTemplateUsed(resposta, 'calculadora/pagina_inicial.html') 
        self.assertContains(resposta, "Análises Recentes") 

    def test_formulario_encontrar_raiz_cria_analise_no_db(self):
        contagem_inicial = Analise.objects.count()

        url = reverse('encontrar_raiz')
        dados_formulario = {
            'funcao_texto': 'x**2 - 4',
            'intervalo_a': '0',
            'intervalo_b': '3',
            'metodo': 'bissecao'
        }
        resposta = self.client.post(url, dados_formulario)

        self.assertEqual(Analise.objects.count(), contagem_inicial + 1)

        self.assertEqual(resposta.status_code, 200)
        
        self.assertContains(resposta, "Resultado Encontrado")

    def test_pagina_inicial_le_dados_do_banco_de_dados(self):
        Analise.objects.create(
            funcao_texto='teste',
            intervalo_a=1,
            intervalo_b=2,
            metodo_utilizado='teste_metodo'
        )

        url = reverse('pagina_inicial')
        resposta = self.client.get(url)
        data_hoje = timezone.now().strftime('%d/%m/%y')
        texto_esperado = f"Análise de 'teste' em {data_hoje}"
        self.assertContains(resposta, "Análise de 'teste'")