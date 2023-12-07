# Copyright 2023 Weavers @ Eternal Loom. All rights reserved.
#
# Use of this software is governed by the license that can be
# found in LICENSE file in the source repository.

# Build a chat interface using gradio

import gradio as gr  # type: ignore
import random
import time
from typing import TypeAlias, Generator

# Type aliases to handle Gradio types
TextAndHistoryUpdates: TypeAlias = tuple[
    str, list[list[str | None] | tuple[str | None] | tuple[str, str]]
]
ChatHistory: TypeAlias = list[list[str | None] | tuple[str | None] | tuple[str, str]]

BOT_MOCK_MESSAGES: list[str] = [
    'Hello, what can I do for you?',
    "There are so many answers to questions in life. I don't know any of them.",
    'Another day, another question. Shall we try another line of work?',
]

OUTPUT_DELAY: float = 0.05


def launch() -> None:
    """The user interface for a simple chat client"""

    with gr.Blocks() as client:
        # Build UI components that form the chat interface
        chatbot = gr.Chatbot(label='Message Thread')
        user_input = gr.Textbox(label='What do you want to do today?')
        clear_button = gr.Button('Clear')

        # Handle user input
        def handle_user_input(
            input_text: str, chat_history: ChatHistory
        ) -> TextAndHistoryUpdates:
            """Callback function for handling user input"""
            # Reset the input text
            text_update = ''
            # and update the history with the user text. None to inform
            # that this update has no bot respnse.
            history_update = chat_history + [[input_text, None]]
            return text_update, history_update

        # Handle chatbot response
        def handle_chatbot_response(
            chat_history: ChatHistory,
        ) -> Generator[ChatHistory, None, None]:
            """Callback function for handling chatbot response"""
            # Select a random response
            bot_message = random.choice(BOT_MOCK_MESSAGES)
            # Update the last message in the history with the bot response

            match chat_history[-1]:
                case list():
                    chat_history[-1][1] = ''
                case tuple():
                    # We are not using tuple format
                    raise ValueError('Unexpected chat history format')

            for character in bot_message:
                # Ignore types, we already ensured that it is not None
                chat_history[-1][1] += character  # type: ignore
                time.sleep(OUTPUT_DELAY)
                yield chat_history

        # Map handlers to events

        # On submit event of user input text field, handle user input
        user_input.submit(  # type: ignore
            fn=handle_user_input,
            inputs=[user_input, chatbot],
            outputs=[user_input, chatbot],
            queue=False,
        ).then(
            # Once we handled user input, handle chatbot response
            handle_chatbot_response,
            inputs=[chatbot],
            outputs=[chatbot],
        )

        # On click of the clear button, clear user input field and chat history
        clear_button.click(  # type: ignore
            fn=lambda: None,
            inputs=None,
            outputs=[chatbot],
            queue=False,
        )

    # By default this is launched on [link](http://localhost:7860)
    client.queue()
    client.launch()  # type: ignore
