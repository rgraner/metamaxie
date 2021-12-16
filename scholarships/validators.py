from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_ronin(value, length=46):
    if str(value)[:6]!='ronin:':
        raise ValidationError(
            _("ronin address needs to start with the word 'ronin:'"),
            params={'value': value},
        )
    if len(str(value))<length and str(value)[:6]=='ronin:':
        raise ValidationError(
            _('ronin address is not correct'),
            params={'value': value},
        )

    if str(value)[6:8]=='0x':
        raise ValidationError(
            _('please remove 0x after ronin:'),
            params={'value': value},
        )


