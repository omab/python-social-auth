from social.exceptions import InvalidEmail
from social.pipeline.partial import partial


@partial
def mail_validation(strategy, details, user=None, is_new=False,
                    *args, **kwargs):
    requires_validation = strategy.backend.REQUIRES_EMAIL_VALIDATION or \
                          strategy.setting('FORCE_EMAIL_VALIDATION', False)
    if requires_validation and details.get('email'):
        data = strategy.request_data()
        if 'verification_code' in data:
            strategy.session_pop('email_validation_address')
            if not strategy.validate_email(details['email'],
                                           data['verification_code']):
                raise InvalidEmail(strategy.backend)
        else:
            strategy.send_email_validation(details['email'])
            strategy.session_set('email_validation_address', details['email'])
            return strategy.redirect(strategy.setting('EMAIL_VALIDATION_URL'))
