from django.urls import path
from .views import *


urlpatterns = [
    path('stores/',
         StoreViewSet.as_view({'get': 'list', 'post':'create'},
                             name='stores')),
    path('stores/<store_id>/',
         StoreViewSet.as_view({'patch': 'partial_update',
                               'put': 'update', 'get': 'retrieve',
                              'delete':'destroy'}, name='stores')),
    path('report/',
         OrderViewSet.as_view({'get': 'list'},
                             name='report')),
]