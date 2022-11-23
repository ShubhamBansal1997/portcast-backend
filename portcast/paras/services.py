# Standard Library
import logging
import time
from typing import Dict, Optional, Tuple, Type

# Third Party Stuff
import requests
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db.models import QuerySet

from .models import Dictionary, Paragraph
from .utils import calculate_frequency, prepare_q_string, prepare_vector_string

logger = logging.getLogger(__name__)


def fetch_paragraph(para: int = 1, sentence: int = 50) -> Tuple[str, Optional[str]]:
    url = f"http://metaphorpsum.com/paragraphs/{para}/{sentence}"
    para_content, err = "", None
    try:
        data = requests.get(url)
        if data.status_code != 200:
            raise Exception("API Failed")
        para_content = data.text
    except Exception:
        err = "API Failed"
    finally:
        return para_content, err


def fetch_dictionary_data(word: str) -> Tuple[str, Dict, Optional[str], bool]:
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    word_info, err = {}, None
    retry = False
    try:
        data = requests.get(url)
        if data.status_code == 200:
            request_data = data.json()
            word_info = request_data[0]
        elif data.status_code == 429:
            time.sleep(10)
            retry = True
        else:
            err = "API Failed"
    except Exception:
        err = "API Failed"
    finally:
        return word, word_info, err, retry


def update_word_in_dictionary(word: str, frequency: int):
    from .tasks import update_words_in_dictionary_task

    obj, created = Dictionary.objects.get_or_create(word=word)
    if not created:
        obj.frequency = obj.frequency + frequency
        obj.save()
    else:
        obj.frequency = frequency
        obj.save()
        word, word_info, err, retry = fetch_dictionary_data(word)
        if retry:
            update_words_in_dictionary_task.delay((word, 0))
            return obj
        if not err:
            word_info["source_urls"] = word_info.get("sourceUrls", [])
            word_extra_keys = [
                "license",
                "phonetics",
                "meanings",
                "license",
                "source_urls",
            ]
            for key in word_extra_keys:
                setattr(obj, key, word_info.get(key, {}))
            obj.save()
    return obj


def get_top_records(
    model: Type[Dictionary] = Dictionary,
    top: bool = True,
    no_of_records: int = 10,
    order_by: str = "frequency",
) -> QuerySet[Dictionary]:
    if top:
        order_by = f"-{order_by}"
    data = model.objects.order_by(order_by)[:no_of_records]
    return data


def get_paragraph(
    para: int = 1, sentence: int = 50
) -> Tuple[Optional[Paragraph], Optional[str]]:
    from .tasks import update_words_in_dictionary_task

    para_content, err = fetch_paragraph(para, sentence)
    obj = None
    if not err:
        obj = Paragraph()
        obj.para_content = para_content
        obj.save()
        freq_list = calculate_frequency(para_content.lower())
        for word, frequency in freq_list:
            update_words_in_dictionary_task.delay((word, frequency))
        return obj, err
    return obj, err


def search_data(
    model: Type[Paragraph], search_query: str, search_key: str = "para_content"
) -> QuerySet[Paragraph]:
    clean_query = prepare_vector_string(search_query)
    query = SearchQuery(clean_query, search_type="raw")
    data = model.objects.annotate(search=SearchVector(search_key)).filter(search=query)
    return data


def search_data_basic(
    model: Type[Paragraph], search_query: str, search_key: str = "para_content"
) -> QuerySet[Paragraph]:
    q_strings = prepare_q_string(search_query, search_key)
    data = model.objects.filter(*q_strings)
    return data
