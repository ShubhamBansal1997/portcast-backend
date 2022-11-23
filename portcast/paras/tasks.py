# Standard Library
from typing import Tuple

# Third Party Stuff
from celery import shared_task

from .services import update_word_in_dictionary


@shared_task()
def update_words_in_dictionary_task(data: Tuple[str, int]):
    word, frequency = data
    _ = update_word_in_dictionary(word, frequency)
