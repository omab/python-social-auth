Beginners Guide
===============

This is an attempt to bring together a number of concepts in python-social-auth
(psa) so that you will understand how it fits into your system. This definitely
has a Django flavor to it (because that's how I learned it).

Understanding PSA URLs
-----------------------

If you have not seen namespaced URLs before, you are about to be introduced.
When you add the PSA entry to your urls.py, it looks like this::

    url(r'', include('social.apps.django_app.urls', namespace='social'))

that "namespace" part on the end is what keeps the names in the PSA-world from
colliding with the names in your app, or other 3rd-party apps.  So your login
link will look like this::

    <a href="{% url 'social:begin' 'provider-name' %}">Login</a>

(See how "social" in the URL mapping matches the value of "namespace" in the
urls.py entry?)

Understanding Backends
----------------------

PSA implements a lot of backends.  Find the entry in the docs for your backend,
and if it's there, follow the steps to enable it, which come down to

1) Set up SOCIAL_AUTH_{backend} variables in settings.py.  (The
   settings vary, based on the backends)

2) Adding your backend to AUTHENTICATION_BACKENDS in settings.py.

If you need to implement a different backend (for instance, let's say you
want to use Intuit's OpenID), you can subclass the nearest one and override
the "name" attribute::

    from social.backends.open_id import OpenIDAuth
    class IntuitOpenID(OpenIDAuth):
        name = 'intuit'

And then add your new backend to AUTHENTICATION_BACKENDS in settings.py.

A couple notes about the pipeline:

The standard pipeline does not log the user in until after the pipeline has
completed.  So if you get a value in the user key of the accumulative
dictionary, that implies that the user was logged in when the process started.

Understanding the Pipeline
--------------------------

Reversing a URL like ``{% url 'social:begin' 'github' %}`` will give you a url
like::

    http://example.com/login/github

And clicking on that link will cause the "pipeline" to be started. The pipeline
is a list of functions that build up data about the user as we go through the
steps of the authentication process.  (If you really want to understand the
pipeline, look at the source in ``social/backends/base.py``, and see the
``run_pipeline()`` function in ``BaseAuth``.)

The design contract for each function in the pipeline is:

1) The pipeline starts with a four-item dictionary (the accumulative dictionary)
   which is updated with the results of each function in the pipeline. The
   initial four values are:
       'strategy' : contains a strategy object
       'backend' : contains the backend being used during this pipeline run
       'request' : contains a dictionary of the request keys. Note to Django
                   users -- this is not an HttpRequest object, it is actually
                   the results of ``request.REQUEST``.
       'details' : which is an empty dict.

2) If the function returns a dictionary or something False-ish, add the contents
   of the dictionary to an accumulative dictionary (called ``out`` in
   ``run_pipeline``), and call the next step in the pipeline with the
   accumulative dictionary.

3) If something else is returned (for example, a subclass of ``HttpResponse``),
   then return that to the browser.

4) If the pipeline completes, *THEN* the user is authenticated (logged in). So
   if you are finding an authenticated user object while the pipeline is
   running, that means that the user was logged in when the pipeline started.

There is one pipeline for your site as a whole -- if you have backend-specific
logic, you have to make your pipeline steps smart enough to skip the step if it
is not relevant.  This is as simple as::

    def my_custom_step(strategy, backend, request, details, *args, **kwargs):
        if backend_name != 'my_custom_backend':
            return
        # otherwise, do the special steps for your custom backend

Interrupting the Pipeline (and communicating with views)
---------------------------------------------------------

Let's say you want to add a custom step in the pipeline -- you want the user
to establish a password so that they can come directly to your site in the
future.  We can do that with the @partial decorator, which tells the pipeline
to keep track of where it is so that it can be restarted.

The first thing we need to do is set up a way for our views to communicate with
the pipeline. That is done by adding a value to the settings file to tell
us which values should be passed back and forth between the Django session
and the pipeline::

    SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['local_password',]

In our pipeline code, we would have::

    from django.shortcuts import redirect
    from django.contrib.auth.models import User
    from social.pipeline.partial import partial

    # partial says "we may interrupt, but we will come back here again"
    @partial
    def collect_password(strategy, backend, request, details, *args, **kwargs):
        # request['local_password'] is set by the pipeline infrastructure
        # because it exists in FIELDS_STORED_IN_SESSION
        if not request.get('local_password', None):

            # if we return something besides a dict or None, then that is
            # returned to the user -- in this case we will redirect to a
            # view that can be used to get a password
            return redirect("myapp.views.collect_password")

        # grab the user object from the database (remember that they may
        # not be logged in yet) and set their password.  (Assumes that the
        # email address was captured in an earlier step.)
        user = User.objects.get(email=kwargs['email'])
        user.set_password(request['local_password'])
        user.save()

        # continue the pipeline
        return

In our view code, we would have something like::

    class PasswordForm(forms.Form):
        secret_word = forms.CharField(max_length=10)

    def get_user_password(request):
        if request.method == 'POST':
            form = PasswordForm(request.POST)
            if form.is_valid():
                # because of FIELDS_STORED_IN_SESSION, this will get copied
                # to the request dictionary when the pipeline is resumed
                request.session['local_password'] = form.cleaned_data['secret_word']

                # once we have the password stashed in the session, we can
                # tell the pipeline to resume by using the "complete" endpoint
                return redirect(reverse('social:complete', args=("backend_name,")))
        else:
            form = PasswordForm()

        return render(request, "password_form.html")

Note that the ``social:complete`` will re-enter the pipeline with the same
function that interrupted it (in this case, collect_password).
