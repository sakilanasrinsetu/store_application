from django.shortcuts import render
from utils.custom_viewset import CustomViewSet

from .serializers import StoreSerializer
from store.models import Store
from utils.response_wrapper import ResponseWrapper
from utils.custom_pagination import CustomPagination
from store.filters import StoreFilter
from store.orderings import StoreOrdering
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers, filters

from actstream import action
from actstream.models import Action

import requests



# Create your views here.


class StoreViewSet(CustomViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    lookup_field = store_id = 'pk'
    pagination_class = CustomPagination

    filter_backends = (
        DjangoFilterBackend,
        StoreOrdering,
    )
    filterset_class = StoreFilter

    # filterset_fields = (
    #     "name",
    #     "slug",
    #     "type",
    #     "address",
    #     "primary_phone",
    #     "secondary_phone",
    #     "map_link",
    #     "opening_time",
    #     "closing_time",
    #     "shown_in_website",
    #     "is_active",
    #     "created_at",
    #     "updated_at",
    # )

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        serializer_class = self.get_serializer_class()
        # ....***.... Pagination ....***....
        page_qs = self.paginate_queryset(qs)
        serializer = serializer_class(instance=page_qs, many=True)
        paginated_data = self.get_paginated_response(serializer.data)

        return ResponseWrapper(data=paginated_data.data, msg='Success')

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
         
        if serializer.is_valid():
            opening_time = serializer.validated_data.get("opening_time")
            closing_time = serializer.validated_data.get("closing_time")
            
            if opening_time >= closing_time:
                return ResponseWrapper(
                    error_code=400, 
                    error_msg="Closing Time Must Be Less Than Opening Time"
                )
            
            qs = serializer.save()

            if qs:
                public_ip = None
                response = requests.get('https://api.ipify.org?format=json')
                if response.status_code == 200:
                    data = response.json()
                    public_ip = data['ip']
                    
                action.send(qs, verb=f"{public_ip}", action_object=qs, target=qs, description=f"Method: {request.method} URL-{request.build_absolute_uri()} \n\n Request Body is- \n {request.data} \n\n Response Body is- {serializer.data} \n\n Request from {public_ip}", url=request.path)

                # action.send(qs, verb=qs.name,
                #         action_object=qs, target=qs.slug, request_body=request.data, url=request.path)


            return ResponseWrapper(data=serializer.data, msg='created')
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)

    def retrieve(self, request, store_id, *args, **kwargs):
        qs = Store.objects.filter(id =  store_id).last()
        if not qs:
            return ResponseWrapper(
                error_code=404, 
                error_msg="Store Not Found")
        serializer = self.serializer_class(qs)

        if qs:
            public_ip = None
            response = requests.get('https://api.ipify.org?format=json')
            if response.status_code == 200:
                data = response.json()
                public_ip = data['ip']
                
            action.send(qs, verb=f"{public_ip}", action_object=qs, target=qs, description=f"Method: {request.method} URL-{request.build_absolute_uri()} \n\n Request Body is- \n {request.data} \n\n Response Body is- {serializer.data} \n\n Request from {public_ip}", url=request.path)
            
        return ResponseWrapper(data=serializer.data,
                               msg="Success")
    
    # ..........***.......... Update ..........***..........
    
    def update(self, request,store_id, **kwargs):
        qs = Store.objects.filter(pk=store_id).last()
        if not qs:
            return ResponseWrapper(
                error_code=404,
                error_msg="Store Not Found")
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)

        if serializer.is_valid():
            opening_time = serializer.validated_data.get("opening_time")
            closing_time = serializer.validated_data.get("closing_time")

            if opening_time >= closing_time:
                return ResponseWrapper(
                    error_code=400,
                    error_msg="Closing Time Must Be Less Than Opening Time"
                )

            qs = serializer.update(instance=qs, validated_data=serializer.validated_data)
            serializer = self.serializer_class(instance=qs)
            return ResponseWrapper(data=serializer.data)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
    
    # ..........***.......... Partial Update ..........***..........
    
    def partial_update(self, request,store_id,  **kwargs):
        qs = Store.objects.filter(pk=store_id).last()
        if not qs:
            return ResponseWrapper(
                error_code=404,
                error_msg="Store Not Found")

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        if serializer.is_valid():

            opening_time = serializer.validated_data.get("opening_time", qs.opening_time)
            closing_time = serializer.validated_data.get("closing_time", qs.closing_time)

            if opening_time >= closing_time:
                return ResponseWrapper(
                    error_code=400,
                    error_msg="Closing Time Must Be Less Than Opening Time"
                )

            qs = serializer.update(instance=qs,
                                   validated_data=serializer.validated_data)
            serializer = self.serializer_class(instance=qs)
            return ResponseWrapper(data=serializer.data)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)

    def destroy(self, request,store_id, **kwargs):
        qs = Store.objects.filter(pk=store_id).last()

        if not qs:
            return ResponseWrapper(
                error_code=400,
                error_msg="Store Not Found")

        qs.delete()
        return ResponseWrapper(status=200, msg='deleted')