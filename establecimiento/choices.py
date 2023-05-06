# choices.py
from django.utils.translation import gettext_lazy as _

class RolChoices:
    DIRECTOR = 'director'
    DOCENTE_AULA = 'docente_aula'
    PROFESOR_ENCARGADO = 'profesor_encargado'
    INSPECTOR_GENERAL = 'inspector_general'
    JEFE_UTP = 'jefe_utp'
    APOYO_UTP = 'apoyo_utp'
    FONOAUDIOLOGO = 'fonoaudiologo'
    PSICOLOGO = 'psicologo'
    EDUCADORA_DIFERENCIAL = 'educadora_diferencial'
    TRABAJADOR_SOCIAL = 'trabajador_social'
    FACILITADOR_INTERCULTURAL = 'facilitador_intercultural'
    AUXILIAR_SERVICIO_MENOR = 'auxiliares_servicio_menor'
    PROFESOR_ESPECIALISTA = 'profesor_especialista'
    ADMINISTRATIVO = 'administrativo'

    CHOICES = [
        (DIRECTOR, _('Director')),
        (DOCENTE_AULA, _('Docente de Aula')),
        (PROFESOR_ENCARGADO, _('Profesor Encargado')),
        (INSPECTOR_GENERAL, _('Inspector General')),
        (JEFE_UTP, _('Jefe UTP')),
        (APOYO_UTP, _('Apoyo UTP')),
        (FONOAUDIOLOGO, _('Fonoaudiólogo')),
        (PSICOLOGO, _('Psicólogo')),
        (EDUCADORA_DIFERENCIAL, _('Educadora Diferencial')),
        (TRABAJADOR_SOCIAL, _('Trabajador Social')),
        (FACILITADOR_INTERCULTURAL, _('Facilitador Intercultural')),
        (AUXILIAR_SERVICIO_MENOR, _('Auxiliar de Servicio Menor')),
        (PROFESOR_ESPECIALISTA, _('Profesor Especialista')),
        (ADMINISTRATIVO, _('Administrativo')),
    ]

class TipoContratoChoices:
    TITULAR = 'titular'
    CONTRATA = 'contrata'

    CHOICES = [
        (TITULAR, _('Titular')),
        (CONTRATA, _('Contrata')),
    ]

class SubvencionChoices:
    NORMAL = 'normal'
    SEP = 'sep'
    PIE = 'pie'

    CHOICES = [
        (NORMAL, _('Normal')),
        (SEP, _('SEP')),
        (PIE, _('PIE')),
    ]

class EstadoDocumentoChoices:
    SI = 'si'
    NO = 'no'
    NA = 'na'

    CHOICES = [
        (SI, _('Sí')),
        (NO, _('No')),
        (NA, _('No Aplica')),
    ]
