from io import StringIO

import pytest

from markdownify.main import main


@pytest.mark.parametrize('args, title, expected_title', [
    ([], '', ''),
    (['--default-title'], '', ' "https://example.com"'),
    ([], ' title="Example"', ' "Example"'),
    (['--default-title'], ' title="Example"', ' "Example"'),
])
def test_default_title(args, title, expected_title, monkeypatch, capsys):
    html = '<a href="https://example.com"%s>Example</a>' % title
    monkeypatch.setattr('sys.stdin', StringIO(html))
    main(args)
    assert capsys.readouterr().out == '[Example](https://example.com%s)\n' % expected_title
