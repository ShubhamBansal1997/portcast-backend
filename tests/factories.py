"""
Helpers to create dynamic model instances for testing purposes.

Usages:
>>> from tests import factories as f
>>>
>>> user = f.create_user(first_name="Robert", last_name="Downey")  # creates single instance of user
>>> users = f.create_user(n=5, is_active=False)  # creates 5 instances of user

There is a bit of magic going on behind the scenes with `G` method from https://django-dynamic-fixture.readthedocs.io/
"""

# Third Party Stuff
from django.apps import apps
from django.conf import settings
from django_dynamic_fixture import G

# portcast Stuff
from portcast.paras.models import Dictionary, Paragraph


def create_user(**kwargs):
    """Create an user along with their dependencies."""
    User = apps.get_model(settings.AUTH_USER_MODEL)
    user = G(User, **kwargs)
    user.set_password(kwargs.get("password", "test"))
    user.save()
    return user


def create_dictionary(**kwargs):
    """Create a word in the dictionary table."""
    word = G(Dictionary, **kwargs)
    word.save()
    return word


def create_paragraph(**kwargs):
    """Create a paragraph in the paragraph table"""
    paragraph = G(Paragraph, **kwargs)
    paragraph.save()
    return paragraph
