from urllib.parse import urlparse

from django.conf import settings
from django.db import models


class Candidatura(models.Model):
    class Status(models.TextChoices):
        CANDIDATADO = "CANDIDATADO", "Candidatado"
        EM_ANALISE = "EM_ANALISE", "Em análise"
        ENTREVISTA = "ENTREVISTA", "Entrevista"
        APROVADO = "APROVADO", "Aprovado"
        REPROVADO = "REPROVADO", "Reprovado"
        DESISTENCIA = "DESISTENCIA", "Desistência"

    class Modalidade(models.TextChoices):
        REMOTO = "REMOTO", "Remoto"
        HIBRIDO = "HIBRIDO", "Híbrido"
        PRESENCIAL = "PRESENCIAL", "Presencial"

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="candidaturas",
    )
    empresa = models.CharField("Empresa", max_length=120)
    cargo = models.CharField("Cargo", max_length=120)
    salario = models.DecimalField(
        "Salário", max_digits=10, decimal_places=2, null=True, blank=True
    )
    modalidade = models.CharField(
        "Modalidade", max_length=20, choices=Modalidade.choices, default=Modalidade.REMOTO
    )
    link = models.CharField("Link da vaga", max_length=500, blank=True)
    data_candidatura = models.DateField("Data da candidatura")
    status = models.CharField(
        "Status", max_length=20, choices=Status.choices, default=Status.CANDIDATADO
    )
    observacoes = models.TextField("Observações", blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-data_candidatura", "-criado_em"]
        verbose_name = "Candidatura"
        verbose_name_plural = "Candidaturas"

    def __str__(self):
        return f"{self.cargo} @ {self.empresa}"

    @property
    def safe_link(self):
        if not self.link:
            return None
        scheme = urlparse(self.link).scheme.lower()
        if scheme in ("http", "https"):
            return self.link
        return None

    @property
    def status_cor(self):
        mapa = {
            self.Status.CANDIDATADO: "bg-slate-100 text-slate-700 ring-slate-200",
            self.Status.EM_ANALISE: "bg-amber-50 text-amber-700 ring-amber-200",
            self.Status.ENTREVISTA: "bg-indigo-50 text-indigo-700 ring-indigo-200",
            self.Status.APROVADO: "bg-emerald-50 text-emerald-700 ring-emerald-200",
            self.Status.REPROVADO: "bg-rose-50 text-rose-700 ring-rose-200",
            self.Status.DESISTENCIA: "bg-zinc-100 text-zinc-600 ring-zinc-200",
        }
        return mapa.get(self.status, "bg-slate-100 text-slate-700 ring-slate-200")
