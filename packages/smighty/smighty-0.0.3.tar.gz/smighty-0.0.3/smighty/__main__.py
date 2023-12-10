# Copyright 2023 Weavers @ Eternal Loom. All rights reserved.
#
# Use of this software is governed by the license that can be
# found in LICENSE file in the source repository.

# Create the Smighty Agent Server (Sasy) that will host a set
# of converwsational agents.

# Start the Smighty Agent Server (sasy)
# This preferably the only place where we have a cold start


import logging

import typer
import uvicorn

import smighty.root as root
from smighty.app import sasy

logger = logging.getLogger()


def start(
    port: int = root.config.port,
    log_level: int = root.config.log_level,
) -> None:
    """
    Start the Smighty API server.

    Args:
        port (int): The port number for the API server.
        log_level (str): The log level for the API server.

    Returns:
        None
    """

    logger.setLevel(log_level)
    logger.info(f'Starting Smighty API server on port {port}')
    uvicorn.run(sasy, port=port, log_level=log_level)


if __name__ == '__main__':
    typer.run(start)
