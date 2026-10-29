from collections import OrderedDict
from datetime import date

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CandidaturaForm, SignupForm
from .models import Candidatura


def _is_htmx(request):
    return request.headers.get("HX-Request") == "true"


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bem-vindo(a), {user.username}! Sua conta foi criada.")
            return redirect("dashboard")
    else:
        form = SignupForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def dashboard(request):
    qs = Candidatura.objects.filter(usuario=request.user)
    total = qs.count()

    status_counts = OrderedDict(
        (label, 0) for _, label in Candidatura.Status.choices
    )
    status_raw = {s["status"]: s["count"] for s in qs.values("status").annotate(count=Count("id"))}
    for value, label in Candidatura.Status.choices:
        status_counts[label] = status_raw.get(value, 0)

    por_mes_qs = (
        qs.annotate(mes=TruncMonth("data_candidatura"))
        .values("mes")
        .annotate(count=Count("id"))
        .order_by("mes")
    )
    meses_labels = []
    meses_data = []
    nomes_meses = {
        1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
        7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez",
    }
    for row in por_mes_qs:
        m = row["mes"]
        if m is None:
            continue
        meses_labels.append(f"{nomes_meses[m.month]}/{str(m.year)[-2:]}")
        meses_data.append(row["count"])

    recentes = qs.order_by("-criado_em")[:5]

    ativos = sum(
        v for k, v in status_raw.items()
        if k in (Candidatura.Status.CANDIDATADO, Candidatura.Status.EM_ANALISE, Candidatura.Status.ENTREVISTA)
    )
    aprovados = status_raw.get(Candidatura.Status.APROVADO, 0)
    taxa_entrevista = 0
    if total:
        em_entrevista_ou_adiante = sum(
            v for k, v in status_raw.items()
            if k in (Candidatura.Status.ENTREVISTA, Candidatura.Status.APROVADO)
        )
        taxa_entrevista = round(100 * em_entrevista_ou_adiante / total)

    context = {
        "total": total,
        "ativos": ativos,
        "aprovados": aprovados,
        "taxa_entrevista": taxa_entrevista,
        "status_counts": status_counts,
        "recentes": recentes,
        "chart_status_labels": list(status_counts.keys()),
        "chart_status_data": list(status_counts.values()),
        "chart_meses_labels": meses_labels,
        "chart_meses_data": meses_data,
    }
    return render(request, "candidaturas/dashboard.html", context)


@login_required
def lista(request):
    qs = Candidatura.objects.filter(usuario=request.user)
    q = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    modalidade = request.GET.get("modalidade", "").strip()

    if q:
        qs = qs.filter(Q(empresa__icontains=q) | Q(cargo__icontains=q))
    if status:
        qs = qs.filter(status=status)
    if modalidade:
        qs = qs.filter(modalidade=modalidade)

    context = {
        "candidaturas": qs,
        "q": q,
        "status_atual": status,
        "modalidade_atual": modalidade,
        "status_choices": Candidatura.Status.choices,
        "modalidade_choices": Candidatura.Modalidade.choices,
        "total_filtrado": qs.count(),
    }
    if _is_htmx(request):
        return render(request, "candidaturas/_tabela.html", context)
    return render(request, "candidaturas/lista.html", context)


@login_required
def nova(request):
    initial = {"data_candidatura": date.today().isoformat()}
    if request.method == "POST":
        form = CandidaturaForm(request.POST)
        if form.is_valid():
            candidatura = form.save(commit=False)
            candidatura.usuario = request.user
            candidatura.save()
            messages.success(request, "Candidatura cadastrada com sucesso!")
            return redirect("lista")
    else:
        form = CandidaturaForm(initial=initial)
    return render(
        request,
        "candidaturas/form.html",
        {"form": form, "titulo": "Nova candidatura", "modo": "nova"},
    )


@login_required
def editar(request, pk):
    candidatura = get_object_or_404(Candidatura, pk=pk, usuario=request.user)
    if request.method == "POST":
        form = CandidaturaForm(request.POST, instance=candidatura)
        if form.is_valid():
            form.save()
            messages.success(request, "Candidatura atualizada.")
            return redirect("detalhe", pk=candidatura.pk)
    else:
        form = CandidaturaForm(instance=candidatura)
    return render(
        request,
        "candidaturas/form.html",
        {"form": form, "titulo": "Editar candidatura", "modo": "editar", "candidatura": candidatura},
    )


@login_required
def detalhe(request, pk):
    candidatura = get_object_or_404(Candidatura, pk=pk, usuario=request.user)
    return render(request, "candidaturas/detalhe.html", {"candidatura": candidatura})


@login_required
def excluir(request, pk):
    candidatura = get_object_or_404(Candidatura, pk=pk, usuario=request.user)
    if request.method == "POST":
        candidatura.delete()
        if _is_htmx(request):
            return HttpResponse("")
        messages.success(request, "Candidatura excluída.")
        return redirect("lista")
    return render(
        request,
        "candidaturas/confirmar_exclusao.html",
        {"candidatura": candidatura},
    )
