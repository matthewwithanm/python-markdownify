|build| |version| |license| |downloads|

.. |build| image:: https://img.shields.io/github/workflow/status/matthewwithanm/python-markdownify/Python%20application/develop
    :alt: GitHub Workflow Status
    :target: https://github.com/matthewwithanm/python-markdownify/actions?query=workflow%3A%22Python+application%22

.. |version| image:: https://img.shields.io/pypi/v/markdownify
    :alt: Pypi version
    :target: https://pypi.org/project/markdownify/

.. |license| image:: https://img.shields.io/pypi/l/markdownify
    :alt: License
    :target: https://github.com/matthewwithanm/python-markdownify/blob/develop/LICENSE

.. |downloads| image:: https://pepy.tech/badge/markdownify
    :alt: Pypi Downloads
    :target: https://pepy.tech/project/markdownify

Installation
============

``pip install markdownify``


Usage
=====

Convert some HTML to Markdown:

.. code:: python

    from markdownify import markdownify as md
    md('<b>Yay</b> <a href="http://github.com">GitHub</a>')  # > '**Yay** [GitHub](http://github.com)'

Specify tags to exclude (blacklist):

.. code:: python

    from markdownify import markdownify as md
    md('<b>Yay</b> <a href="http://github.com">GitHub</a>', strip=['a'])  # > '**Yay** GitHub'

\...or specify the tags you want to include (whitelist):

.. code:: python

    from markdownify import markdownify as md
    md('<b>Yay</b> <a href="http://github.com">GitHub</a>', convert=['b'])  # > '**Yay** GitHub'


Options
=======

Markdownify supports the following options:

strip
  A list of tags to strip (blacklist). This option can't be used with the
  ``convert`` option.

convert
  A list of tags to convert (whitelist). This option can't be used with the
  ``strip`` option.

autolinks
  A boolean indicating whether the "automatic link" style should be used when
  a ``a`` tag's contents match its href. Defaults to ``True``

heading_style
  Defines how headings should be converted. Accepted values are ``ATX``,
  ``ATX_CLOSED``, ``SETEXT``, and ``UNDERLINED`` (which is an alias for
  ``SETEXT``). Defaults to ``UNDERLINED``.

bullets
  An iterable (string, list, or tuple) of bullet styles to be used. If the
  iterable only contains one item, it will be used regardless of how deeply
  lists are nested. Otherwise, the bullet will alternate based on nesting
  level. Defaults to ``'*+-'``.

strong_em_symbol
  In markdown, both ``*`` and ``_`` are used to encode **strong** or
  *emphasized* texts. Either of these symbols can be chosen by the options
  ``ASTERISK`` (default) or ``UNDERSCORE`` respectively.

newline_style
  Defines the style of marking linebreaks (``<br>``) in markdown. The default
  value ``SPACES`` of this option will adopt the usual two spaces and a newline,
  while ``BACKSLASH`` will convert a linebreak to ``\\n`` (a backslash an a
  newline). While the latter convention is non-standard, it is commonly
  preferred and supported by a lot of interpreters.

Options may be specified as kwargs to the ``markdownify`` function, or as a
nested ``Options`` class in ``MarkdownConverter`` subclasses.


Development
===========

To run tests:

``python setup.py test``

To lint:

``python setup.py lint``
