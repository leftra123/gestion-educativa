from django import forms
from django.core.exceptions import ValidationError
from itertools import cycle
import re
from .models import (
    Establecimiento,
    Persona,
    Documento,
    Docente,
    DocenteEstablecimiento,
    Bienio,
    Curso,
    Asistente,
    AsistenteEstablecimiento,
)


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = [
            "nombre",
            "rut",
            "id_extranjero",
            "apellido_paterno",
            "apellido_materno",
            "fecha_nacimiento",
            "direccion",
            "telefono",
            "email",
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "rut": forms.TextInput(attrs={"class": "form-control"}),
            "id_extranjero": forms.TextInput(attrs={"class": "form-control"}),
            "apellido_paterno": forms.TextInput(attrs={"class": "form-control"}),
            "apellido_materno": forms.TextInput(attrs={"class": "form-control"}),
            "fecha_nacimiento": forms.DateInput(attrs={"class": "form-control"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def clean_rut(self):
        rut = self.cleaned_data.get("rut")
        if rut and not validar_rut(rut):
            raise forms.ValidationError("El RUT ingresado no es válido.")
        return rut

    def clean_telefono(self):
        telefono = self.cleaned_data.get("telefono")
        if telefono and not validar_telefono(telefono):
            raise forms.ValidationError("El número de teléfono ingresado no es válido.")
        return telefono

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and not validar_email(email):
            raise forms.ValidationError("El correo electrónico ingresado no es válido.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        rut = cleaned_data.get("rut")
        id_extranjero = cleaned_data.get("id_extranjero")

        if not rut and not id_extranjero:
            raise forms.ValidationError("Debe ingresar RUT o ID Extranjero.")
        if rut and id_extranjero:
            raise forms.ValidationError(
                "Solo debe ingresar RUT o ID Extranjero, no ambos."
            )

        return cleaned_data


def validar_rut(value):
    rut_regex = re.compile(r"^\d{1,8}-[\dkK]{1}$")
    if not rut_regex.match(value):
        raise forms.ValidationError("RUT no válido. Ingrese RUT en formato XXXXXXXX-X.")

    rut, dv = value.split("-")
    rut = int(rut)
    total = 0
    reversed_digits = map(int, reversed(str(rut)))
    factors = cycle(range(2, 8))
    for digit, factor in zip(reversed_digits, factors):
        total += digit * factor
    res = 11 - total % 11
    if res == 11:
        dv_calc = "0"
    elif res == 10:
        dv_calc = "K"
    else:
        dv_calc = str(res)

    if dv.upper() != dv_calc:
        raise forms.ValidationError("RUT no válido. Dígito verificador incorrecto.")


def validar_telefono(telefono):
    # Asumiendo que el número de teléfono tiene 9 dígitos y comienza con 9
    telefono_regex = re.compile(r"^9\d{8}$")
    if not telefono_regex.match(telefono):
        raise forms.ValidationError("Número de teléfono no válido.")


def validar_email(email):
    # Usando el validador de correo electrónico incorporado en Django
    from django.core.validators import validate_email as django_validate_email

    try:
        django_validate_email(email)
    except ValidationError:
        raise forms.ValidationError("Correo electrónico no válido.")


class EstablecimientoForm(forms.ModelForm):
    class Meta:
        model = Establecimiento
        fields = ["RBD", "DV", "nombre", "encargado"]
        encargados = Persona.objects.filter(rol="docente_de_aula") # Filtra solo docentes de aula
        encargados_choices = [(encargado.id, encargado.nombre) for encargado in encargados]
        widgets = {
            "RBD": forms.NumberInput(attrs={"class": "form-control"}),
            "DV": forms.TextInput(attrs={"class": "form-control"}),
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "encargado": forms.Select(choices=encargados_choices, attrs={"class": "form-control"}),
        }



class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ["persona", "titulo", "archivo"]
        widgets = {
            "persona": forms.Select(attrs={"class": "form-control"}),
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "archivo": forms.FileInput(attrs={"class": "form-control"}),
        }


class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = [
            "nombre",
            "rut",
            "id_extranjero",
            "apellido_paterno",
            "apellido_materno",
            "fecha_nacimiento",
            "direccion",
            "telefono",
            "email",
            "rol",
            "tipo_contrato",
            "subvencion",
            "horas_tipo_contrato",
            "horas_subvencion_normal",
            "horas_subvencion_sep",
            "horas_subvencion_pie",
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "rut": forms.TextInput(attrs={"class": "form-control"}),
            "id_extranjero": forms.TextInput(attrs={"class": "form-control"}),
            "apellido_paterno": forms.TextInput(attrs={"class": "form-control"}),
            "apellido_materno": forms.TextInput(attrs={"class": "form-control"}),
            "fecha_nacimiento": forms.DateInput(attrs={"class": "form-control"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "rol": forms.TextInput(attrs={"class": "form-control"}),
            "tipo_contrato": forms.TextInput(attrs={"class": "form-control"}),
            "subvencion": forms.TextInput(attrs={"class": "form-control"}),
            "horas_tipo_contrato": forms.NumberInput(attrs={"class": "form-control"}),
            "horas_subvencion_normal": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "horas_subvencion_sep": forms.NumberInput(attrs={"class": "form-control"}),
            "horas_subvencion_pie": forms.NumberInput(attrs={"class": "form-control"}),
        }


class DocenteEstablecimientoForm(forms.ModelForm):
    class Meta:
        model = DocenteEstablecimiento
        fields = [
            "docente",
            "establecimiento",
            "horas_subvencion_normal",
            "horas_subvencion_sep",
            "horas_subvencion_pie",
            "horas_tipo_contrato",
            "fecha_inicio",
            "fecha_termino",
        ]
        widgets = {
            "docente": forms.Select(attrs={"class": "form-control"}),
            "establecimiento": forms.Select(attrs={"class": "form-control"}),
            "horas_subvencion_normal": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "horas_subvencion_sep": forms.NumberInput(attrs={"class": "form-control"}),
            "horas_subvencion_pie": forms.NumberInput(attrs={"class": "form-control"}),
            "horas_tipo_contrato": forms.NumberInput(attrs={"class": "form-control"}),
            "fecha_inicio": forms.DateInput(attrs={"class": "form-control"}),
            "fecha_termino": forms.DateInput(attrs={"class": "form-control"}),
        }


class BienioForm(forms.ModelForm):
    class Meta:
        model = Bienio
        fields = ["docente", "fecha_inicio", "fecha_fin", "horas_acumuladas"]
        widgets = {
            "docente": forms.Select(attrs={"class": "form-control"}),
            "fecha_inicio": forms.DateInput(attrs={"class": "form-control"}),
            "fecha_fin": forms.DateInput(attrs={"class": "form-control"}),
            "horas_acumuladas": forms.NumberInput(attrs={"class": "form-control"}),
        }


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = [
            "nombre",
            "establecimiento",
            "docente",
            "grado",
            "letra",
            "seccion",
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "establecimiento": forms.Select(attrs={"class": "form-control"}),
            "docente": forms.Select(attrs={"class": "form-control"}),
            "grado": forms.TextInput(attrs={"class": "form-control"}),
            "letra": forms.TextInput(attrs={"class": "form-control"}),
            "seccion": forms.TextInput(attrs={"class": "form-control"}),
        }


class AsistenteForm(forms.ModelForm):
    class Meta:
        model = Asistente
        fields = [
            "nombre",
            "rut",
            "id_extranjero",
            "apellido_paterno",
            "apellido_materno",
            "fecha_nacimiento",
            "direccion",
            "telefono",
            "email",
            "cargo",
            "horas_semanales",
            "fecha_contratacion",
            "tipo_contrato",
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "rut": forms.TextInput(attrs={"class": "form-control"}),
            "id_extranjero": forms.TextInput(attrs={"class": "form-control"}),
            "apellido_paterno": forms.TextInput(attrs={"class": "form-control"}),
            "apellido_materno": forms.TextInput(attrs={"class": "form-control"}),
            "fecha_nacimiento": forms.DateInput(attrs={"class": "form-control"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "cargo": forms.TextInput(attrs={"class": "form-control"}),
            "horas_semanales": forms.NumberInput(attrs={"class": "form-control"}),
            "fecha_contratacion": forms.DateInput(attrs={"class": "form-control"}),
            "tipo_contrato": forms.TextInput(attrs={"class": "form-control"}),
        }


class AsistenteEstablecimientoForm(forms.ModelForm):
    class Meta:
        model = AsistenteEstablecimiento
        fields = [
            "asistente",
            "establecimiento",
            "fecha_inicio",
            "fecha_termino",
        ]

    widgets = {
        "asistente": forms.Select(attrs={"class": "form-control"}),
        "establecimiento": forms.Select(attrs={"class": "form-control"}),
        "fecha_inicio": forms.DateInput(attrs={"class": "form-control"}),
        "fecha_termino": forms.DateInput(attrs={"class": "form-control"}),
    }
