# Copyright 2023 Weavers @ Eternal Loom. All rights reserved.
#
# Use of this software is governed by the license that can be
# found in LICENSE file in the source repository.

from typer.testing import CliRunner

from smighty.app.cli.__main__ import app

runner = CliRunner()


def test_hello() -> None:
    # Without proper command
    result = runner.invoke(app, ['sam', '--city', 'sfo'])
    assert result.exit_code != 0
    result = runner.invoke(app, ['hello', 'sam', '--city', 'sfo'])
    assert result.exit_code == 0
    assert 'Sam' in result.output
    assert 'SFO' in result.output
    # Without optional city
    result = runner.invoke(app, ['hello', 'sam'])
    assert result.exit_code == 0
    assert 'Sam' in result.output
    assert 'SFO' not in result.output
    result = runner.invoke(app, [])
    assert result.exit_code != 0


def test_goodbye() -> None:
    result = runner.invoke(app, ['goodbye'])
    assert result.exit_code == 0
    assert 'Have a great day!' in result.output
    result = runner.invoke(app, [])
    assert result.exit_code != 0
