from django.urls import path, include
from rest_framework.routers import DefaultRouter

from common.views.dicts import PositionView


app_name = 'common'

router = DefaultRouter()

router.register(r'dicts/positions', PositionView, 'positions')

urlpatterns = [

]
urlpatterns += path('organizations/', include(router.urls)),