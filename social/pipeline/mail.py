from social.exceptions import InvalidEmail
from social.pipeline.partial import partial


@partial
def mail_validation(backend, details, is_new=False, *args, **kwargs):
    requires_validation = backend.REQUIRES_EMAIL_VALIDATION or \
                          backend.setting('FORCE_EMAIL_VALIDATION', False)
    send_validation = details.get('email') and \
                      (is_new or backend.setting('PASSWORDLESS', False))
    if requires_validation and send_validation:
        data = backend.strategy.request_data()
        if 'verification_code' in data:
            backend.strategy.session_pop('email_validation_address')
            if not backend.strategy.validate_email(details['email'],
                                           data['verification_code']):
                raise InvalidEmail(backend)
        else:
            backend.strategy.send_email_validation(backend, details['email'])
            backend.strategy.session_set('email_validation_address',
                                         details['email'])
            return backend.strategy.redirect(
                backend.strategy.setting('EMAIL_VALIDATION_URL')
            )
