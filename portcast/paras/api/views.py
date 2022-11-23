# Third Party Stuff
# approval Stuff
# Third Party Stuff
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

# portcast Stuff
from portcast.base.api.mixins import MultipleSerializerMixin
from portcast.paras.models import Paragraph
from portcast.paras.services import (
    get_paragraph,
    get_top_records,
    search_data,
    search_data_basic,
)

from .serializers import (
    DictionarySerializer,
    ParagraphSerializer,
    SearchQuerySerializer,
)


class ParagraphViewSet(MultipleSerializerMixin, viewsets.GenericViewSet):
    serializer_class = ParagraphSerializer
    queryset = Paragraph.objects.all()
    serializer_classes = {
        "dictionary": DictionarySerializer,
        "search": SearchQuerySerializer,
        "searchv1": SearchQuerySerializer,
    }
    permission_classes = [AllowAny]

    @action(methods=["GET"], detail=False)
    def get(self, request: Request) -> Response:
        data, err = get_paragraph()
        if err:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        serializer = self.serializer_class(data)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(methods=["GET"], detail=False)
    def dictionary(self, request: Request) -> Response:
        data = get_top_records()
        serializer = self.get_serializer(data, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(methods=["POST"], detail=False)
    def search(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = search_data(Paragraph, **serializer.validated_data)
        serializer = self.serializer_class(data, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(methods=["POST"], detail=False)
    def searchv1(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = search_data_basic(Paragraph, **serializer.validated_data)
        serializer = self.serializer_class(data, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
