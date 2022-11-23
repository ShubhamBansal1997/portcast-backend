# Standard Library
from unittest.mock import MagicMock

# Third Party Stuff
import pytest

# portcast Stuff
from portcast.paras.services import (
    fetch_dictionary_data,
    fetch_paragraph,
    get_paragraph,
    update_word_in_dictionary,
)

# from portcast.paras.models import Dictionary
from tests import factories as f

pytestmark = pytest.mark.django_db


def test_get_paragraph_success(settings, mocker):
    para_content = "This is para content"
    mock_fetch_paragraph = mocker.patch("portcast.paras.services.fetch_paragraph")
    mock_fetch_paragraph.return_value = (para_content, None)
    no_of_paras = 1
    no_of_sentences = 50
    fetch_paragraph_input = (no_of_paras, no_of_sentences)
    obj, err = get_paragraph(no_of_paras, no_of_sentences)
    args, _ = mock_fetch_paragraph.call_args
    assert args == fetch_paragraph_input
    assert obj.para_content == para_content
    assert err is None
    assert mock_fetch_paragraph.call_count == 1


def test_update_word_in_dictionary_already_created(settings, mocker):
    word = "the"
    frequency = 10
    dictionary = f.create_dictionary(word=word, frequency=frequency)
    mock_update_words_in_dictionary_task = mocker.patch(
        "portcast.paras.tasks.update_words_in_dictionary_task.delay"
    )
    mock_fetch_dictionary_data = mocker.patch(
        "portcast.paras.services.fetch_dictionary_data"
    )
    updated_dictionary = update_word_in_dictionary(word, frequency)
    assert mock_update_words_in_dictionary_task.call_count == 0
    assert mock_fetch_dictionary_data.call_count == 0
    assert dictionary.word == updated_dictionary.word
    assert dictionary.frequency + frequency == updated_dictionary.frequency


def test_update_word_in_dictionary_new_word_success(settings, mocker):
    word = "word"
    frequency = 10
    mock_update_words_in_dictionary_task = mocker.patch(
        "portcast.paras.tasks.update_words_in_dictionary_task.delay"
    )
    mock_fetch_dictionary_data = mocker.patch(
        "portcast.paras.services.fetch_dictionary_data"
    )
    mock_fetch_dictionary_data.return_value = (word, {}, None, False)
    dictionary = update_word_in_dictionary(word, frequency)
    args, _ = mock_fetch_dictionary_data.call_args
    assert mock_update_words_in_dictionary_task.call_count == 0
    assert mock_fetch_dictionary_data.call_count == 1
    assert dictionary.word == word
    assert dictionary.frequency == frequency
    assert args == (word,)


def test_update_word_in_dictionary_new_word_retry(settings, mocker):
    word = "word"
    frequency = 10
    mock_update_words_in_dictionary_task = mocker.patch(
        "portcast.paras.tasks.update_words_in_dictionary_task.delay"
    )
    mock_fetch_dictionary_data = mocker.patch(
        "portcast.paras.services.fetch_dictionary_data"
    )
    mock_fetch_dictionary_data.return_value = (word, {}, None, True)
    dictionary = update_word_in_dictionary(word, frequency)
    args, _ = mock_fetch_dictionary_data.call_args
    arg, _ = mock_update_words_in_dictionary_task.call_args
    assert mock_update_words_in_dictionary_task.call_count == 1
    assert mock_fetch_dictionary_data.call_count == 1
    assert dictionary.word == word
    assert dictionary.frequency == frequency
    assert args == (word,)
    assert arg[0] == (word, 0)


def test_get_paragraph_failure(settings, mocker):
    para_content = ""
    mock_fetch_paragraph = mocker.patch("portcast.paras.services.fetch_paragraph")
    mock_fetch_paragraph.return_value = (para_content, "API Failed")
    no_of_paras = 1
    no_of_sentences = 50
    fetch_paragraph_input = (no_of_paras, no_of_sentences)
    obj, err = get_paragraph(no_of_paras, no_of_sentences)
    args, _ = mock_fetch_paragraph.call_args
    assert args == fetch_paragraph_input
    assert obj is None
    assert err == "API Failed"
    assert mock_fetch_paragraph.call_count == 1


def test_fetch_paragraph_success(settings, mocker):
    expected_para_content = "This is para content"
    mock_request = mocker.patch("portcast.paras.services.requests")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_request.text = expected_para_content
    mock_request.get.return_value = mock_response
    actual_para_content, err = fetch_paragraph()
    assert expected_para_content == expected_para_content
    assert err is None


def test_fetch_paragraph_failure(settings, mocker):
    mock_request = mocker.patch("portcast.paras.services.requests")
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_request.text = "API Failed"
    mock_request.get.return_value = mock_response
    actual_para_content, err = fetch_paragraph()
    assert actual_para_content == ""
    assert err == "API Failed"


def test_fetch_dictionary_data_404(settings, mocker):
    expected_word = "is"
    mock_request = mocker.patch("portcast.paras.services.requests")
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_request.get.return_value = mock_response
    actual_word, word_info, err, retry = fetch_dictionary_data(expected_word)
    assert actual_word == expected_word
    assert word_info == {}
    assert err == "API Failed"
    assert retry is False


def test_fetch_dictionary_data_429(settings, mocker):
    expected_word = "is"
    mock_request = mocker.patch("portcast.paras.services.requests")
    mock_time = mocker.patch("portcast.paras.services.time")
    mock_time.sleep.return_value = None
    mock_response = MagicMock()
    mock_response.status_code = 429
    mock_request.get.return_value = mock_response
    actual_word, word_info, err, retry = fetch_dictionary_data(expected_word)
    assert actual_word == expected_word
    assert word_info == {}
    assert err is None
    assert retry is True


def test_fetch_dictionary_data_not_200(settings, mocker):
    expected_word = "is"
    mock_request = mocker.patch("portcast.paras.services.requests")
    mock_response = MagicMock()
    mock_response.status_code = 300
    mock_request.get.return_value = mock_response
    actual_word, word_info, err, retry = fetch_dictionary_data(expected_word)
    assert actual_word == expected_word
    assert word_info == {}
    assert err == "API Failed"
    assert retry is False


def test_fetch_dictionary_data_200_without_data(settings, mocker):
    expected_word = "is"
    mock_request = mocker.patch("portcast.paras.services.requests")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    mock_request.get.return_value = mock_response
    actual_word, word_info, err, retry = fetch_dictionary_data(expected_word)
    assert actual_word == expected_word
    assert word_info == {}
    assert err == "API Failed"
    assert retry is False


def test_fetch_dictionary_data_200_with_data(settings, mocker):
    expected_word = "is"
    mock_request = mocker.patch("portcast.paras.services.requests")
    mock_response = MagicMock()
    mock_response.status_code = 200
    expected_word_info = {"sourceUrls": ["test"]}
    mock_response.json.return_value = [expected_word_info]
    mock_request.get.return_value = mock_response
    actual_word, word_info, err, retry = fetch_dictionary_data(expected_word)
    assert actual_word == expected_word
    assert word_info == expected_word_info
    assert err is None
    assert retry is False
