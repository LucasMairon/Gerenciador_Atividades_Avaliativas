from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

period_validator = RegexValidator(
    r'(^(19|20)\d{2}\.[123]$)',
    _('Invalid period, make sure that the value is valid')
)
