# Copyright 2023 Weavers @ Eternal Loom. All rights reserved.
#
# Use of this software is governed by the license that can be
# found in LICENSE file in the source repository.

# Start a local terminal client

# This is the startup script for Smighty CLI client.
# Expected Use:
# ```
# python -m smighty.app.cli [--remote URL]
# ```
# This will start a terminal client. The client operates in
# two modes, local or remote.
#
# If no options are specified, the client will start a local
# environment and help setup, manage and use Smighty locally.
#
# If the `--remote` option is specified, it will connect to
# the remote Smighty API server and support use of Smighty.

from typing import Optional

import typer

app = typer.Typer()


@app.command()
def hello(name: str, city: Optional[str] = None) -> None:
    print(f'Hello, {name.capitalize()}!')
    if city is not None:
        print(f'Welcome to {city.upper()}!')


@app.command()
def goodbye() -> None:
    print('Have a great day!')


if __name__ == '__main__':
    app(['hello', 'sam', '--city', 'sfo'])
    app(['goodbye'])
