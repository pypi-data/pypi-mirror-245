# Copyright 2023 Weavers @ Eternal Loom. All rights reserved.
#
# Use of this software is governed by the license that can be
# found in LICENSE file in the source repository.

import importlib

import smighty.app.cli.welcome as app

# import smighty.app.chat as chat


def test_app_run() -> None:
    app.Welcome().run()


def test_app_build() -> None:
    app.Welcome().build()


def test_app_launch() -> None:
    app.launch()


def test_app_get_message() -> None:
    app.get_message()


def test_import() -> None:
    module = importlib.import_module('smighty.app.cli.welcome')
    assert module is not None
    # importlib.import_module("smighty.app.chat")


def test_module() -> None:
    import smighty.app.cli.welcome as app

    app.Welcome().run()
