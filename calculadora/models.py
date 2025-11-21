from django.db import models

class Sessao(models.Model):
    nome = models.CharField(max_length=100, default="Sessão sem nome")
    tipo_ferramenta = models.CharField(max_length=50)
    metodo = models.CharField(max_length=50)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    dados_input = models.JSONField() 
    dados_output = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.tipo_ferramenta} - {self.data_criacao.strftime('%d/%m/%Y %H:%M')}"