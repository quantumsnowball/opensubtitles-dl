import pytest
import mock
import builtins


def test_cli_help(script_runner):
    result = script_runner.run('opensubtitles-dl', '--help')
    assert result.success
    assert result.stdout.split('\n')[0].startswith('Usage:')


def test_cli_no_args(script_runner):
    result = script_runner.run('opensubtitles-dl')
    assert result.success
    assert result.stdout.split('\n')[0].startswith('Usage:')


@pytest.mark.parametrize('keywords', [
    (kw, ) for kw in ('spider man', 'iron man', 'captain america')])
def test_cli_with_search_keywords(keywords, script_runner):
    with mock.patch.object(builtins, 'input', lambda _: 'q'):
        result = script_runner.run(f'opensubtitles-dl', keywords)
        assert result.success
        assert result.stdout.split('\n')[0].startswith(
            'Please select subtitle by id:')


@pytest.mark.parametrize('n', [n for n in (5, 10, 20)])
def test_cli_with_n_limit(n, script_runner):
    with mock.patch.object(builtins, 'input', lambda _: 'q'):
        result = script_runner.run(
            f'opensubtitles-dl', f'-n {n}', 'spider man')
        assert result.success
        assert result.stdout.split('\n')[0].startswith(
            'Please select subtitle by id:')
        assert len(result.stdout.split('\n')) == n + 2
