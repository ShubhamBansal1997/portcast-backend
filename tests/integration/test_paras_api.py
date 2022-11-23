# Standard Library
import json

# Third Party Stuff
import pytest
from django.urls import reverse

# portcast Stuff
from tests import factories as f

pytestmark = pytest.mark.django_db


def test_get_paragraph_api_success(client, settings, mocker):
    url = reverse("paragraph-get")
    para_content = "This is a para content"
    mock_fetch_paragraph = mocker.patch("portcast.paras.services.fetch_paragraph")
    mock_fetch_paragraph.return_value = (para_content, None)
    response = client.get(url)

    # assert response is None
    assert response.status_code == 200
    assert mock_fetch_paragraph.call_count == 1
    expected_keys = ["created_at", "id", "para_content", "modified_at"]
    assert set(expected_keys).issubset(response.data.keys())
    assert response.data["para_content"] == para_content


def test_get_paragraph_api_failure(client, settings, mocker):
    url = reverse("paragraph-get")
    para_content = ""
    mock_fetch_paragraph = mocker.patch("portcast.paras.services.fetch_paragraph")
    mock_fetch_paragraph.return_value = (para_content, "API Failed")
    response = client.get(url)

    # assert response is None
    assert response.status_code == 503
    assert mock_fetch_paragraph.call_count == 1
    assert response.data is None


def test_dictionary_paragraph_api(client):
    url = reverse("paragraph-dictionary")
    word_data = ["word1", "word2"]
    _ = f.create_dictionary(word=word_data[0])
    _ = f.create_dictionary(word=word_data[1])
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2
    expected_keys = [
        "id",
        "created_at",
        "modified_at",
        "word",
        "frequency",
        "phonetics",
        "meanings",
        "license",
        "source_urls",
    ]
    assert set(expected_keys).issubset(response.data[0].keys())
    assert set(expected_keys).issubset(response.data[1].keys())
    assert response.data[0]["word"] in word_data
    assert response.data[1]["word"] in word_data


@pytest.mark.parametrize("search_route", ["search", "searchv1"])
def test_search_paragraph_api_fail_blank(search_route, client):
    print(search_route)
    url = reverse(f"paragraph-{search_route}")
    data = {"search_query": ""}
    response = client.json.post(url, json.dumps(data))
    assert response.status_code == 400
    errors = response.data["errors"]
    assert errors[0]["field"] == "search_query"
    assert errors[0]["message"] == "This field may not be blank."
    assert response.data["error_type"] == "ValidationError"


@pytest.mark.parametrize("search_route", ["search", "searchv1"])
def test_search_paragraph_api_fail_null(search_route, client):
    url = reverse(f"paragraph-{search_route}")
    data = {}
    response = client.json.post(url, json.dumps(data))
    assert response.status_code == 400
    errors = response.data["errors"]
    assert errors[0]["field"] == "search_query"
    assert errors[0]["message"] == "This field is required."
    assert response.data["error_type"] == "ValidationError"


def test_searchv1_paragraph_success(client):
    url = reverse("paragraph-searchv1")
    _ = f.create_paragraph(para_content="This is a paragraph")
    second_word = f.create_paragraph(para_content="This is not a paragraph")
    data = {"search_query": "is or this ANd not"}
    response = client.json.post(url, json.dumps(data))
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["para_content"] == second_word.para_content
    assert response.data[0]["id"] == str(second_word.id)


def test_search_paragraph_success(client):
    url = reverse("paragraph-search")
    _ = f.create_paragraph(para_content="This is a paragraph")
    _ = f.create_paragraph(para_content="This is not a paragraph")
    data = {"search_query": "is or this ANd not"}
    response = client.json.post(url, json.dumps(data))
    assert response.status_code == 200
    assert len(response.data) == 0
