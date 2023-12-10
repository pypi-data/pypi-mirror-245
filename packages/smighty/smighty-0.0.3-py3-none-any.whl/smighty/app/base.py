# Copyright 2023 Weavers @ Eternal Loom. All rights reserved.
#
# Use of this software is governed by the license that can be
# found in LICENSE file in the source repository.

from abc import ABC, abstractmethod


# Base application class
class App(ABC):
    """Abstract base class for all applications"""

    def __init__(self) -> None:
        pass

    @abstractmethod
    def build(self) -> None:
        """Build the client"""
        pass

    @abstractmethod
    def run(self) -> None:
        """Run the client"""
        pass
