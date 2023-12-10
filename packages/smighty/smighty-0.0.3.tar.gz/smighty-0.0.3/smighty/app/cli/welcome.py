# Copyright 2023 Weavers @ Eternal Loom. All rights reserved.
#
# Use of this software is governed by the license that can be
# found in LICENSE file in the source repository.

from smighty.app import BaseApp

WELCOME_MESSAGE = 'Welcome to Smighty World!'


class Welcome(BaseApp):
    """A test welcome cli app"""

    def __init__(self) -> None:
        super().__init__()

    def build(self) -> None:
        return

    def run(self) -> None:
        print(WELCOME_MESSAGE)


# Launch the welcome apps
def launch() -> None:
    """Launch the chat interface"""
    Welcome().run()


# Just a test function to return the welcome message
def get_message() -> str | None:
    return WELCOME_MESSAGE


if __name__ == '__main__':
    launch()
