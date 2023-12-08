"""
Demo code for question answering using GPT-3.
"""
import os

import openai

from yival.logger.token_logger import TokenLogger
from yival.schemas.experiment_config import MultimodalOutput
from yival.states.experiment_state import ExperimentState
from yival.wrappers.string_wrapper import StringWrapper


def qa(question: str, state: ExperimentState) -> MultimodalOutput:
    """
    Demo code for question answering using GPT-3.
    """
    logger = TokenLogger()
    logger.reset()
    # Ensure you have your OpenAI API key set up
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Create a chat message sequence
    prompt = str(StringWrapper("", name="qa", state=state))
    messages = [{
        "role":
        "system",
        "content":
        "You are a helpful assistant that will answer the question with only option."
    }, {
        "role": "user",
        "content": f'{question} ' + prompt
    }]
    # Use the chat-based completion
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, temperature=0
    )

    # Extract the assistant's message (translated text) from the response
    answer = MultimodalOutput(
        text_output=response['choices'][0]['message']['content'],
    )
    token_usage = response['usage']['total_tokens']
    logger.log(token_usage)

    return answer
