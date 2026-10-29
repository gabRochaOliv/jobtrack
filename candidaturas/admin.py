from django.contrib import admin

from .models import Candidatura


@admin.register(Candidatura)
class CandidaturaAdmin(admin.ModelAdmin):
    list_display = ("empresa", "cargo", "status", "modalidade", "data_candidatura", "usuario")
    list_filter = ("status", "modalidade", "data_candidatura")
    search_fields = ("empresa", "cargo", "observacoes")
    date_hierarchy = "data_candidatura"
