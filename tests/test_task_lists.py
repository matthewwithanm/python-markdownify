import io

import pytest

from markdownify import markdownify
from markdownify.main import main


@pytest.mark.parametrize('space', ['', ' '])
def test_checked_and_unchecked_tasks(space):
    html = ('<ul><li><input type="checkbox" checked>' + space + 'Pay rent</li>'
            '<li><input type="checkbox">' + space + 'Renew passport</li></ul>')
    assert markdownify(html, task_lists=True) == (
        '* [x] Pay rent\n* [ ] Renew passport'
    )


def test_task_checkbox_with_label_markup_and_nested_list():
    html = ('<ol><li><label><input type="CHECKBOX" checked="false">'
            '<strong>Done</strong></label><ul><li><input type="checkbox">'
            'Child</li></ul></li></ol>')
    assert markdownify(html, task_lists=True) == (
        '1. [x] **Done**\n   * [ ] Child'
    )


def test_standalone_empty_task_keeps_state():
    assert markdownify('<ul><li><input type=checkbox></li></ul>', task_lists=True) == '* [ ]'


def test_task_option_defaults_to_disabled_and_respects_strip():
    html = '<ul><li><input type=checkbox checked> Done</li></ul>'
    assert markdownify(html) == '* Done'
    assert markdownify(html, task_lists=True, strip=['input']) == '* Done'


def test_other_inputs_and_non_list_checkboxes_are_unchanged():
    assert markdownify('<p><input type=checkbox checked>Text</p>', task_lists=True) == 'Text'
    assert markdownify('<ul><li><input type=text value=test>Text</li></ul>', task_lists=True) == '* Text'


def test_label_boundary_and_code_context():
    html = '<ul><li><label><input type=checkbox checked></label> Done</li></ul>'
    assert markdownify(html, task_lists=True) == '* [x] Done'
    html = '<ul><li><code><input type=checkbox>Code</code></li></ul>'
    assert markdownify(html, task_lists=True) == '* `Code`'


def test_task_lists_cli(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO('<ul><li><input type=checkbox>Task</li></ul>'))
    main(['--task-lists'])
    assert capsys.readouterr().out == '* [ ] Task\n'
