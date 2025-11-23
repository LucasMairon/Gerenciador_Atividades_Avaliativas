from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

personal_email_validator = RegexValidator(
    r"(^[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,}$)",
    _('Invalid email, follow the standart: email@host.extensions')
)

institutional_email_validator = RegexValidator(
    r"(^[\w.%+-]+@(?!gmail\.com|hotmail\.com|outlook\.com|yahoo\.com)[\w.-]+\.[a-zA-Z]{2,}$)",
    _('Invalid institutional email, make sure you have spelled it correctly')
)

name_validator = RegexValidator(
    r"(^[a-zA-ZÀ-ú ]+$)",
    _('Invalid name, use just letters')
)

password_validator = RegexValidator(
    r"(^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$)",
    _('Senha incorreta. Verifique se a senha informada segue todos os requisitos de segurança.')
)
