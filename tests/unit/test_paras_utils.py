# Third Party Stuff
from django.db.models import Q

# portcast Stuff
from portcast.paras.utils import (
    calculate_frequency,
    clean_search_query,
    extract_words,
    ireplace,
    prepare_q_string,
)


def test_extract_words():
    para_content = "This is a sample para content, para four"
    expected_value = ["This", "is", "a", "sample", "para", "content", "para", "four"]
    assert extract_words(para_content) == expected_value


def test_calculate_frequency():
    para_content = "this is a word word is a a"
    expected_value = [("this", 1), ("is", 2), ("a", 3), ("word", 2)]
    actual_value = calculate_frequency(para_content)
    assert len(actual_value) == len(expected_value)
    difference = set(actual_value) ^ set(expected_value)
    assert not difference


def test_ireplace():
    input_values = (" AnD ", " & ", "one And two and five")
    expected_output = "one & two & five"
    actual_output = ireplace(*input_values)
    assert actual_output == expected_output


def test_clear_query():
    input_value = "one And two and five OR six And nine AND that"
    expected_output = "one & two & five | six & nine & that"
    actual_output = clean_search_query(input_value)
    assert actual_output == expected_output


def test_prepare_q_string():
    input_value = ("one & two | five", "search_key")
    expected_output = [
        *[Q(search_key__icontains="one")],
        *[Q(search_key__icontains="two") | Q(search_key__icontains="five")],
    ]
    actual_output = prepare_q_string(*input_value)
    assert len(expected_output) == len(actual_output)
    difference = set(expected_output) ^ set(actual_output)
    assert not difference
