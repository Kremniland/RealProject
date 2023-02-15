from django.contrib.auth import get_user_model

from .mixins import ExtendedModelSerializer
from common.models import Position


User = get_user_model()


class PositionListSerializer(ExtendedModelSerializer):

    class Meta:
        model = Position
        fields = (
            'code',
            'name',
        )

