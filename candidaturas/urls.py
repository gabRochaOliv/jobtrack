from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("candidaturas/", views.lista, name="lista"),
    path("candidaturas/nova/", views.nova, name="nova"),
    path("candidaturas/<int:pk>/", views.detalhe, name="detalhe"),
    path("candidaturas/<int:pk>/editar/", views.editar, name="editar"),
    path("candidaturas/<int:pk>/excluir/", views.excluir, name="excluir"),
]
