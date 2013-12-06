Mozilla Persona
===============

Support for `Mozilla Persona`_ is possible by posting the ``assertion`` code to
``/complete/persona/`` URL.

The setup doesn't need any setting, just the usual `Mozilla Persona`_
javascript include in your document and the needed mechanism to trigger the
POST to `python-social-auth`_::

    <!-- Include BrowserID JavaScript -->
    <script src="https://login.persona.org/include.js" type="text/javascript"></script>

    <!-- Define a form to send the POST data -->
    <form method="post" action="/complete/persona/">
        <input type="hidden" name="assertion" value="" />
        <a rel="nofollow" id="persona" href="#">Mozilla Persona</a>
    </form>

    <!-- Setup click handler that retieves Persona assertion code and sends POST data -->
    <script type="text/javascript">
        $(function () {
            $('#persona').click(function (e) {
                e.preventDefault();
                var self = $(this);

                navigator.id.get(function (assertion) {
                    if (assertion) {
                        self.parent('form')
                                .find('input[type=hidden]')
                                    .attr('value', assertion)
                                    .end()
                                .submit();
                    } else {
                        alert('Some error occurred');
                    }
                });
            });
        });
    </script>

.. _python-social-auth: https://github.com/omab/python-social-auth
.. _Mozilla Persona: http://www.mozilla.org/persona/
