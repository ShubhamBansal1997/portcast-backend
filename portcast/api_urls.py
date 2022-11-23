# Third Party Stuff
from rest_framework.routers import DefaultRouter

# portcast Stuff
from portcast.base.api.routers import SingletonRouter
from portcast.paras.api.views import ParagraphViewSet
from portcast.users.api import CurrentUserViewSet
from portcast.users.auth.api import AuthViewSet

default_router = DefaultRouter(trailing_slash=False)
singleton_router = SingletonRouter(trailing_slash=False)

# Register all the django rest framework viewsets below.
default_router.register("auth", AuthViewSet, basename="auth")
default_router.register("paragraph", ParagraphViewSet, basename="paragraph")
singleton_router.register("me", CurrentUserViewSet, basename="me")


# Combine urls from both default and singleton routers and expose as
# 'urlpatterns' which django can pick up from this module.
urlpatterns = default_router.urls + singleton_router.urls
