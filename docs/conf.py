# -*- coding: utf-8 -*-
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx',
              'sphinx.ext.todo', 'sphinx.ext.viewcode']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'Python Social Auth'
copyright = u'2012, Matías Aguirre'
exclude_patterns = ['_build']
pygments_style = 'sphinx'
html_theme = 'nature'
html_static_path = []
htmlhelp_basename = 'PythonSocialAuthdoc'
latex_documents = [
  ('index', 'PythonSocialAuth.tex', u'Python Social Auth Documentation',
   u'Matías Aguirre', 'manual'),
]
man_pages = [
    ('index', 'pythonsocialauth', u'Python Social Auth Documentation',
     [u'Matías Aguirre'], 1)
]
intersphinx_mapping = {'http://docs.python.org/': None}
