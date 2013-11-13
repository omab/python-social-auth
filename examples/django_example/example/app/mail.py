from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse


def send_validation(strategy, code):
    url = reverse('social:complete', args=(strategy.backend.name,)) + \
            '?verification_code=' + code.code
    send_mail('Validate your account',
              'Validate your account {0}'.format(url),
              settings.EMAIL_FROM,
              [code.email],
              fail_silently=False)
