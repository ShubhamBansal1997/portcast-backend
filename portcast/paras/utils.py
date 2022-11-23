# Standard Library
import re
from collections import Counter
from functools import reduce
from typing import Any, List, Tuple

# Third Party Stuff
from django.db.models import Q


def extract_words(para_content: str) -> List[str]:
    return re.findall("[a-zA-Z]+", para_content)


def calculate_frequency(para_content: str) -> List[Tuple[str, int]]:
    clean_para_content = extract_words(para_content)
    return list(Counter(clean_para_content).items())


def ireplace(old: str, new: str, text: str) -> str:
    idx = 0
    while idx < len(text):
        index_l = text.lower().find(old.lower(), idx)
        if index_l == -1:
            return text
        text = text[:index_l] + new + text[index_l + len(old) :]
        idx = index_l + len(new)
    return text


def clean_search_query(query: str) -> str:
    cleaned_query = ireplace(" and ", " & ", query)
    cleaned_query = ireplace(" or ", " | ", cleaned_query)
    return cleaned_query


def prepare_q_string(search_query: str, key: str) -> List[Any]:
    clean_query = clean_search_query(search_query)
    return [
        reduce(lambda x, y: x | y, block)
        for block in [
            [
                Q(**{f"{key}__icontains": or_block.strip()})
                for or_block in and_block.strip().split("|")
            ]
            for and_block in clean_query.split("&")
        ]
    ]


def prepare_vector_string(search_query: str) -> str:
    clean_query = clean_search_query(search_query)
    return " & ".join(
        [
            " | ".join(
                [
                    " <-> ".join(block.split(" "))
                    if len(block.split(" ")) > 1
                    else block
                    for block in single_block
                ]
            )
            for single_block in [
                [or_block.strip() for or_block in and_block.strip().split("|")]
                for and_block in clean_query.split("&")
            ]
        ]
    )
