from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse


def send_validation(strategy, backend, code):
    url = '{0}?verification_code={1}'.format(
        reverse('social:complete', args=(backend.name,)),
        code.code
    )
    url = strategy.request.build_absolute_uri(url)
    send_mail('Validate your account', 'Validate your account {0}'.format(url),
              settings.EMAIL_FROM, [code.email], fail_silently=False)
