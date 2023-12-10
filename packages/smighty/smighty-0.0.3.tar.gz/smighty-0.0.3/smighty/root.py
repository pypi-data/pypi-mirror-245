# Copyright 2023 Weavers @ Eternal Loom. All rights reserved.
#
# Use of this software is governed by the license that can be
# found in LICENSE file in the source repository.

"""Base configuration and definitions needed to start Smigty.
"""
import logging
from typing import Annotated

from pydantic import Field
from pydantic.functional_validators import BeforeValidator
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

from smighty.utils.validate import convert_log_level

ENV_FILE_NAME = '.env'


class RootConfig(BaseSettings):
    """Settings for the root level context (/) of Smighty"""

    # The port number for the API server.
    port: int = 8042

    # The log level for the API server.
    log_level: Annotated[
        int, Field(default=logging.INFO), BeforeValidator(convert_log_level)
    ]

    # Enable reading from .env file
    model_config = SettingsConfigDict(env_file=ENV_FILE_NAME, env_file_encoding='utf-8')


# Root configuration for Smighty setup
config = RootConfig()
