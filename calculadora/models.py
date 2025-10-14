from django.db import models

class Analise(models.Model):
    funcao_texto = models.CharField(max_length=255)
    intervalo_a = models.FloatField()
    intervalo_b = models.FloatField()
    metodo_utilizado = models.CharField(max_length=50)
    resultado = models.FloatField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Análise de '{self.funcao_texto}' em {self.criado_em.strftime('%d/%m/%y')}"