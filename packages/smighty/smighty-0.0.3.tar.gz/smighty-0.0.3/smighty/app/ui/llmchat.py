# Copyright 2023 Weavers @ Eternal Loom. All rights reserved.
#
# Use of this software is governed by the license that can be
# found in LICENSE file in the source repository.

import gradio as gr  # type: ignore

from smighty.app import BaseApp
from smighty.app.consts import WIP_MARKDOWN


# Chat UI implementation integrated with LLMs
class ChatUI(BaseApp):
    """Chat UI integrated with Large Language Models."""

    def __init__(self) -> None:
        self._client = self._build()

    def build(self) -> None:
        """Build the chat interface"""
        if self._client is None:
            self._client = self._build()

    def run(self) -> None:
        """Launch the chat interface"""
        self._client.launch()  # type: ignore

    def _build(self) -> gr.Blocks:
        """Build a chat interface and return the UI component"""
        with gr.Blocks() as client:
            wip_message = gr.Markdown(f'{WIP_MARKDOWN}')

        return client


# Launch the chat interface
def launch() -> None:
    """Launch the chat interface"""
    ChatUI().run()


if __name__ == '__main__':
    ChatUI().run()
