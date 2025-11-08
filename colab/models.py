from django.db import models


class Teste(models.Model):
    categoria = models.CharField(max_length=255)
    quantidade = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.categoria}: {self.quantidade}'


class EGA_KPIS_PROD(models.Model):
    recid = models.IntegerField(null = True)
    maquina = models.IntegerField(null = True)
    registro = models.DateTimeField(null = True)
    os = models.IntegerField(null = True)
    produto = models.IntegerField(null = True)
    operacao = models.IntegerField(null = True)
    molde = models.IntegerField(null = True)
    ttotal = models.IntegerField(null = True)
    sec_total = models.IntegerField(null = True)
    tdisp = models.IntegerField(null = True)
    sec_disp = models.IntegerField(null = True)
    tprod = models.IntegerField(null = True)
    sec_prod = models.IntegerField(null = True)
    qtde_std = models.IntegerField(null = True)
    qtde_real = models.IntegerField(null = True)
    qtde_boas = models.IntegerField(null = True)
    teep = models.DecimalField(max_digits=6, decimal_places=2, null = True)
    oee = models.DecimalField(max_digits=6, decimal_places=2, null = True)
    disp = models.DecimalField(max_digits=6, decimal_places=2, null = True)
    perf = models.DecimalField(max_digits=6, decimal_places=2, null = True)
    qualidade = models.DecimalField(max_digits=6, decimal_places=2, null = True)


    def __str__(self):
        return f'{self.recid} {self.maquina} {self.registro} {self.os} {self.produto}'