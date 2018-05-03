# -*- coding: utf-8 -*-
#
# City Energy Analyst documentation build configuration file, created by
# sphinx-quickstart on Tue Jan 31 15:57:58 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from mock import Mock as MagicMock
import cea

sys.path.insert(0, os.path.abspath('..'))



# mock out some imports so we don't have conflicts on the readthedocs server...
class Mock(MagicMock):
    @classmethod
    def __getattr__(cls, name):
            return MagicMock()


MOCK_MODULES = ['pythonocc',
                'SALib', 'SALib.analyze', 'SALib.analyze', 'SALib.sample', 'SALib.sample.saltelli',
                'SALib.sample.morris',
                'deap', 'descartes', 'doit',
                'ephem', 'fiona', 'geopandas', 'lxml', 'pandas', 'plotly', 'plotly.offline', 'plotly.graph_objs',
                'pycollada', 'pyproj', 'pysal', 'pyshp',
                'scikit-learn', 'shapely', 'simpledbf', 'xlrd', 'networkx', 'pyliburo', 'pyliburo.py3dmodel', 'pyliburo.py3dmodel.fetch', 'pyliburo.py3dmodel.construct', 'timezonefinder', 'astral',
                'cvxopt', 'xlwt', 'python-dateutil',
                'pyliburo.py3dmodel.calculate', 'pyliburo.py3dmodel.modify', 'pyliburo.pycitygml',
                'pyliburo.gml3dmodel', 'pyliburo.shp2citygml', 'pyliburo.py2radiance',
                'pandas.util', 'pandas.util.testing',
                ]

sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.todo',
              'sphinx.ext.coverage',
              'sphinx.ext.mathjax',
              'sphinx.ext.viewcode',
              'sphinx.ext.graphviz',
              'sphinx.ext.intersphinx',
              # 'sphinx.ext.githubpages',
              ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'City Energy Analyst'
copyright = u'2017, Architecture and Building Systems'
author = u'Architecture and Building Systems'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = cea.__version__
# The full version, including alpha/beta/rc tags.
release = cea.__version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store',
                    'modules/cea.CH','modules/cea.databases*','modules/uncertainty*',
                    'modules/cea.analysis.sensitivity.sensitivity_optimization.rst',  # TODO: remove when fixed
                    'modules/cea.optimization.*',  # TODO: remove when fixed
                    ]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# this should make the style the blue read-the-docs style
# html_theme = "sphinx_rtd_theme"
# html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
modindex_common_prefix = ['cea.']

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static', 'demand']


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'CityEnergyAnalystdoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'CityEnergyAnalyst.tex', u'City Energy Analyst Documentation',
     u'Architecture and Building Systems', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'cityenergyanalyst', u'City Energy Analyst Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'CityEnergyAnalyst', u'City Energy Analyst Documentation',
     author, 'CityEnergyAnalyst', 'One line description of project.',
     'Miscellaneous'),
]


intersphinx_mapping = {'python': ('https://docs.python.org/2.7', None)}



# ## Add documentation for python special methods

autodoc_default_flags = ['members', 'private-members', 'special-members',
                         #'undoc-members',
                         'show-inheritance']

def autodoc_skip_member(app, what, name, obj, skip, options):
        exclusions = ('__weakref__',  # special-members
                  '__doc__', '__module__', '__dict__',  # undoc-members
                  )
        exclude = name in exclusions
        if name == name in exclusions:
            return skip or exclude
        else:
            return False

def setup(app):
    app.connect('autodoc-skip-member', autodoc_skip_member)









# def run_apidoc(_):
# 	from sphinx.apidoc import main
# 	import os
# 	import sys
# 	sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# 	cur_dir = os.path.abspath(os.path.dirname(__file__))
# 	module = os.path.join(cur_dir,"../","cea")
# 	main(['sphinx-apidoc -e', ' -o ', cur_dir,' ', module, '--force'])
#
# def setup(app):
# 	app.connect('builder-inited', run_apidoc)
