from drf_spectacular.utils import extend_schema_view, extend_schema

from .mixins import ListViewSet
from common.models import Position
from common.serializers.dicts import PositionListSerializer


@extend_schema_view(
    list=extend_schema(summary='Список должностей', tags=['Словари']),
)
class PositionView(ListViewSet):
    queryset = Position.objects.filter(is_active=True)
    serializer_class = PositionListSerializer


