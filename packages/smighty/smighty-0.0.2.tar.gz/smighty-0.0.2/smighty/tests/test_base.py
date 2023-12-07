# Copyright 2023 Weavers @ Eternal Loom. All rights reserved.
#
# Use of this software is governed by the license that can be
# found in LICENSE file in the source repository.

import pytest

from smighty.app import BaseApp


class AppForTest(BaseApp):
    def __init__(self) -> None:
        super().__init__()

    def build(self) -> None:
        print('Test app built...')

    def run(self) -> None:
        print('Test app running...')


@pytest.fixture
def app_instance() -> AppForTest:
    return AppForTest()


def test_base_app(app_instance: AppForTest) -> None:
    assert app_instance is not None
    assert isinstance(app_instance, BaseApp)
    app_instance.build()
    app_instance.run()
