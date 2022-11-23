# Third Party Stuff
from rest_framework import serializers

# portcast Stuff
from portcast.paras.models import Dictionary, Paragraph


class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = "__all__"


class DictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = "__all__"


class SearchQuerySerializer(serializers.Serializer):
    search_query = serializers.CharField(
        required=True, allow_null=False, allow_blank=False
    )
