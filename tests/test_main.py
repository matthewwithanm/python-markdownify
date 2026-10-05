from io import StringIO
import sys

from markdownify.main import main


def test_cli_stdin_default_and_flag(monkeypatch, capfd):
    html = '<a href="https://example.com">Example</a>'

    monkeypatch.setattr(sys, 'stdin', StringIO(html))
    main([])
    assert capfd.readouterr().out == '[Example](https://example.com)\n'

    monkeypatch.setattr(sys, 'stdin', StringIO(html))
    main(['--default-title'])
    assert capfd.readouterr().out == '[Example](https://example.com "https://example.com")\n'


def test_cli_named_file_and_explicit_title(tmp_path, monkeypatch, capfd):
    source = tmp_path / 'input.html'
    source.write_text(
        '<a href="https://example.com" title="Custom">Example</a>',
        encoding='utf-8',
    )

    main([str(source)])
    assert capfd.readouterr().out == '[Example](https://example.com "Custom")\n'

    main(['--default-title', str(source)])
    assert capfd.readouterr().out == '[Example](https://example.com "Custom")\n'


def test_cli_autolinks_option_is_unchanged(monkeypatch, capfd):
    html = '<a href="https://example.com">https://example.com</a>'

    monkeypatch.setattr(sys, 'stdin', StringIO(html))
    main(['-a'])
    assert capfd.readouterr().out == '<https://example.com>\n'

    monkeypatch.setattr(sys, 'stdin', StringIO(html))
    main(['-a', '--default-title'])
    assert capfd.readouterr().out == '[https://example.com](https://example.com "https://example.com")\n'
