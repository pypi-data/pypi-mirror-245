import itertools
import pytest
import re
import string
import time

from pyssword import pyssword as m
from pyssword import util as u


@pytest.mark.parametrize('option', ['-h', '--help'])
def test_run_help(cli_invoker, option):
    result = cli_invoker(m.run, option)
    assert result.exit_code == 0
    assert result.output.startswith('Usage: run <options> <size>')


@pytest.mark.parametrize('option', ['-v', '--version'])
def test_run_version(cli_invoker, option):
    result = cli_invoker(m.run, option)
    assert result.exit_code == 0
    assert re.search(r'version (\d\.?){3}(\.dev\d+)?$', result.output.strip(), re.IGNORECASE)


@pytest.mark.parametrize('common', ['--show --time 0.3'])
@pytest.mark.parametrize('size', [
    *[pytest.param(i, marks=pytest.mark.xfail) for i in range(0, 10)],
    *range(10, 21),
])
def test_run_size(cli_invoker, common, size):
    result = cli_invoker(m.run, f'{common} {size}')
    assert result.exit_code == 0
    assert len(result.output.strip()) == size


@pytest.mark.parametrize('common', ['--show --time 0.3'])
@pytest.mark.parametrize('size', range(10, 30))
@pytest.mark.parametrize('option,alphabet_type', itertools.chain(
    # options with full punctuation
    list(itertools.product(
        [''],
        ['full']
    )),
    # options with digits
    list(itertools.product(
        ['-d', '--digits'],
        ['digits']
    )),
    # options with small punctuation
    list(itertools.product(
        ['-s', '--small'],
        ['small']
    )),
    # options with nopunctuation
    list(itertools.product(
        ['-n', '--nopunctuation'],
        ['nopunctuation']
    )),
    # options with small and nopunctuation
    list(itertools.product(
        itertools.product(
            ['-s', '--small'],
            ['-n', '--nopunctuation']
        ),
        ['nopunctuation']
    )),
    # options with digits, small and nopunctuation
    list(itertools.product(
        itertools.product(
            ['-d', '--digits'],
            ['-s', '--small'],
            ['-n', '--nopunctuation']
        ),
        ['digits']
    )),
))
def test_run_mixed_options(cli_invoker, common, option, alphabet_type, size):
    alphabet          = m.ALPHABET[alphabet_type]
    negative_alphabet = ''.join([c for c in string.printable if c not in alphabet])

    option = ' '.join(option) if isinstance(option, (list, tuple, set)) else option
    result = cli_invoker(m.run, f'{common} {option} {size}')
    output = result.output.strip()

    assert result.exit_code == 0
    assert len(output) == size

    assert not any(c not in alphabet for c in output), f"Invalid punctuations --> {tuple(c for c in output if c not in alphabet)} in {output}"
    assert not any(c in negative_alphabet for c in output), f"Invalid punctuations --> {tuple(c for c in output if c in negative_alphabet)} in {output}"


@pytest.mark.parametrize('common', ['--show --time 0.3'])
@pytest.mark.parametrize('size', range(10, 30))
@pytest.mark.parametrize('qty', [
    *[pytest.param(i, marks=pytest.mark.xfail) for i in range(-2, 1)],
    *range(1, 11),
])
@pytest.mark.parametrize('batch', ['-b', '--batch'])
def test_run_batch(cli_invoker, common, batch, qty, size):
    result = cli_invoker(m.run, f'{common} {batch} {qty} {size}')
    output = result.output.split()

    assert result.exit_code == 0
    assert len(output) == qty

    for item in output:
        assert len(item.strip()) == size


@pytest.mark.slow
@pytest.mark.parametrize('common', ['--time 0.1'])
@pytest.mark.parametrize('qty', [
    *[pytest.param(i, marks=pytest.mark.xfail) for i in range(-2, 1)],
    *range(1, 11),
])
@pytest.mark.parametrize('batch', ['--batch'])
@pytest.mark.parametrize('size', range(10, 30))
@pytest.mark.parametrize('show', ['-p', '--show'])
def test_run_show(cli_invoker, common, batch, qty, show, size):
    result = cli_invoker(m.run, f'{common} {batch} {qty} {show} {size}')
    output = result.output.split()

    assert result.exit_code == 0
    assert len(output) == qty
    assert sorted(output) == sorted(u.get_from_clipboard().split())

    for item in output:
        assert len(item.strip()) == size

    time.sleep(0.15)


@pytest.mark.slow
@pytest.mark.parametrize('common', ['--time 0.1'])
@pytest.mark.parametrize('qty', [
    *[pytest.param(i, marks=pytest.mark.xfail) for i in range(-2, 1)],
    *range(1, 11),
])
@pytest.mark.parametrize('batch', ['--batch'])
@pytest.mark.parametrize('size', range(10, 30))
@pytest.mark.parametrize('hide', ['-P', '--hide'])
def test_run_hide(cli_invoker, common, batch, qty, hide, size):
    result = cli_invoker(m.run, f'{common} {batch} {qty} {hide} {size}')
    output = result.output.split()

    assert result.exit_code == 0
    assert len(output) == 0

    for item in u.get_from_clipboard().split():
        assert len(item.strip()) == size

    time.sleep(0.13)


@pytest.mark.slow
@pytest.mark.parametrize('common', ['--show'])
@pytest.mark.parametrize('size', range(10, 30, 7))
@pytest.mark.parametrize('duration', [
    *[pytest.param(i/10.0, marks=pytest.mark.xfail) for i in range(-10, 1, 1)],
    *[i/10.0 for i in range(1, 10, 1)],
    *range(1, 11, 4),
])
@pytest.mark.parametrize('clip_time', ['-t', '--time'])
def test_run_clipboard_time_duration(cli_invoker, common, clip_time, duration, size):
    result = cli_invoker(m.run, f'{common} {clip_time} {duration} {size}')
    output = result.output.split()

    assert result.exit_code == 0
    assert len(output) == 1

    delta = 0.03

    time.sleep(duration - delta)

    assert sorted(output) == sorted(u.get_from_clipboard().split())

    for item in u.get_from_clipboard().split():
        assert len(item.strip()) == size

    time.sleep(delta)

    for item in u.get_from_clipboard().split():
        assert len(item.strip()) == 0
