# Copyright 2023 Weavers @ Eternal Loom. All rights reserved.
#
# Use of this software is governed by the license that can be
# found in LICENSE file in the source repository.

# Basic logging setup
import logging

from rich.logging import RichHandler

logger = logging.getLogger()

# Setup setup formatter for logging
shell_handler = RichHandler(show_time=False, show_path=False)
shell_format = '%(message)s'
shell_formatter = logging.Formatter(shell_format)
shell_handler.setFormatter(shell_formatter)
logger.addHandler(shell_handler)
