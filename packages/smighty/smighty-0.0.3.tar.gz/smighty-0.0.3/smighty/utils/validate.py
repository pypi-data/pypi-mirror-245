# Copyright 2023 Weavers @ Eternal Loom. All rights reserved.
#
# Use of this software is governed by the license that can be
# found in LICENSE file in the source repository.

"""Validation related utilities.
"""
import logging


def convert_log_level(log_level: str) -> int:
    """Convert a log level string to a log level integer.

    Args:
        log_level (str): The log level string to convert.

    Returns:
        int: The log level integer.
    """
    try:
        level_int_value = int(log_level)
    except ValueError:
        level_int_value = getattr(logging, log_level.upper(), logging.INFO)

    return level_int_value
