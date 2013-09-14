from django.shortcuts import redirect

from social.pipeline.partial import partial


@partial
def require_email(strategy, details, *args, **kwargs):
    print "REQUIRE EMAIL 0"
    if not details.get('email'):
        print "REQUIRE EMAIL 1: no email"
        if strategy.session_get('saved_email'):
            print "REQUIRE EMAIL 2: got email:", \
                  strategy.session_get('saved_email')
            details['email'] = strategy.session_pop('saved_email')
        else:
            print "REQUIRE EMAIL 3: redirect"
            return redirect('require_email')
    print "DETAILS:", details
