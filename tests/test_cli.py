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


@pytest.mark.parametrize('keywords', ('spider man', 'iron man', 'captain america'))
def test_cli_with_search_keywords(keywords, script_runner):
    with mock.patch.object(builtins, 'input', lambda _: 'q'):
        result = script_runner.run(f'opensubtitles-dl', keywords)
        assert result.success
        assert result.stdout.split('\n')[0].startswith(
            'Please select subtitle by id:')


@pytest.mark.parametrize('n', (5, 10, 20))
def test_cli_with_limit_flag(n, script_runner):
    with mock.patch.object(builtins, 'input', lambda _: 'q'):
        result = script_runner.run(
            f'opensubtitles-dl', f'-n {n}', 'spider man')
        assert result.success
        assert result.stdout.split('\n')[0].startswith(
            'Please select subtitle by id:')
        assert len(result.stdout.split('\n')) == n + 2


@pytest.mark.parametrize('l', ('chi', 'spn', 'eng', 'hin', 'jpn', 'kor'))
def test_cli_with_language_flag(l, script_runner):
    with mock.patch.object(builtins, 'input', lambda _: 'q'):
        result = script_runner.run(
            f'opensubtitles-dl', f'-l {l}', 'spider man')
        assert result.success
        assert result.stdout.split('\n')[0].startswith(
            'Please select subtitle by id:')
        entries = result.stdout.split('\n')[1:-1]
        if len(entries) >= 0:
            assert all([l in entry for entry in entries])
