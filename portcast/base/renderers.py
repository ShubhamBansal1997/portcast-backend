# Third Party Stuff
from rest_framework.renderers import JSONRenderer


class PortcastApiRenderer(JSONRenderer):
    media_type = "application/vnd.portcast+json"
