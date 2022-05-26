def test_cli_help(script_runner):
    result = script_runner.run('opensubtitles-dl', '--help')
    assert result.success
    assert result.stdout.split('\n')[0].startswith('Usage:')


def test_cli_no_args(script_runner):
    result = script_runner.run('opensubtitles-dl')
    assert result.success
    assert result.stdout.split('\n')[0].startswith('Usage:')
