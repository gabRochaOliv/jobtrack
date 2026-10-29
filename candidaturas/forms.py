from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Candidatura


BASE_INPUT = (
    "mt-1 block w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm "
    "text-slate-900 shadow-sm placeholder-slate-400 "
    "focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-200"
)


class CandidaturaForm(forms.ModelForm):
    class Meta:
        model = Candidatura
        fields = [
            "empresa",
            "cargo",
            "salario",
            "modalidade",
            "link",
            "data_candidatura",
            "status",
            "observacoes",
        ]
        widgets = {
            "empresa": forms.TextInput(attrs={"placeholder": "Ex.: Nubank"}),
            "cargo": forms.TextInput(attrs={"placeholder": "Ex.: Desenvolvedor Backend"}),
            "salario": forms.NumberInput(attrs={"step": "0.01", "placeholder": "4500.00"}),
            "link": forms.TextInput(attrs={"placeholder": "Cole aqui o link da vaga ou qualquer referência"}),
            "data_candidatura": forms.DateInput(attrs={"type": "date"}),
            "observacoes": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Anotações sobre a vaga, contatos, etapas..."}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{classes} {BASE_INPUT}".strip()


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{classes} {BASE_INPUT}".strip()


class LoginStyledForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{classes} {BASE_INPUT}".strip()
