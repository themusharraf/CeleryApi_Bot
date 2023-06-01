# from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView, \
#     RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
#
# from apps.models import New
# from apps.serializers import NewModelSerializer
#
#
# # CREATE
# class NewCreateAPIView(CreateAPIView):
#     serializer_class = NewModelSerializer
#
#
# # READ
# class NewListAPIView(ListAPIView):
#     queryset = New.objects.all()
#     serializer_class = NewModelSerializer
#
#
# # UPDATE
# class NewUpdateAPIView(UpdateAPIView):
#     queryset = New.objects.all()
#     serializer_class = NewModelSerializer
#
#
# # DELETE
# class NewDestroyAPIView(DestroyAPIView):
#     queryset = New.objects.all()
#     serializer_class = NewModelSerializer
#
#
# class NewRetrieveAPIView(RetrieveAPIView):
#     queryset = New.objects.all()
#     serializer_class = NewModelSerializer
#
#
# class NewRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = New.objects.all()
#     serializer_class = NewModelSerializer
#
#
# class NewListCreateAPIView(ListCreateAPIView):
#     queryset = New.objects.all()
#     serializer_class = NewModelSerializer
#
from django.db.models import F
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.models import (New, Product, ProductImage, Region, ResponsiblePerson,
                         UseFulInfo)
from apps.pagination import StandardResultsSetPagination
from apps.serializers import (DistrictResponsiblePersonModelSerializer,
                              NewDetailModelSerializer, NewListModelSerializer,
                              ProductTranslatableModelSerializer, RegionListModelSerializer,
                              ResponsiblePersonModelSerializer,
                              UseFulInfoListModelSerializer, RegionModelSerializer)
from apps.throttle import CustomUserRateThrottle
from faker import Faker
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import redirect

'''

v1 (id, name, description, price)
v2 (id, name, price)
# v2 (id, name, description, price)

'''
from root.tasks import notify_telegram_group


class BaseAPIView(GenericAPIView):
    serializer_class = NewListModelSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [CustomUserRateThrottle]

    def get(self, request, *args, **kwargs):
        notify_telegram_group.delay()
        return Response({'msg': 'hello world'})


class UseFulModelVUseFulInfo(ModelViewSet):
    queryset = UseFulInfo.objects.all()
    serializer_class = UseFulInfoListModelSerializer

    @action(methods=['GET'], detail=False)
    def counter(self, request, pk=None):
        if file_id := request.GET.get('file_id'):
            UseFulInfo.objects.filter(id=file_id).update(number_download=F('number_download') + 1)
            return Response()
        return Response('Not Found', status=404)


class RegionModelViewSet(ModelViewSet):
    queryset = Region.objects.order_by('id')
    serializer_class = RegionListModelSerializer


class RegionCreateAPIView(ListCreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionModelSerializer
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(tags=["Add Category"])
    def post(self, request, *args, **kwargs):
        fake = Faker()
        objects = (Region(name=fake.name()) for _ in range(500000))
        Region.objects.bulk_create(objects)
        response = super().post(request, *args, **kwargs)
        return response


class NewModelViewSet(ModelViewSet):
    queryset = New.objects.all()
    serializer_class = NewListModelSerializer

    def retrieve(self, request, *args, **kwargs):
        self.get_queryset()
        instance = self.get_object()
        instance.view_count += 1
        instance.save()
        serializer = NewDetailModelSerializer(instance)
        return Response(serializer.data)

    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         return NewDetailModelSerializer
    #     return NewListModelSerializer

    # @action(methods=['GET'], detail=False, url_path='botirjonni-urli')
    # def report(self, request, pk=None):
    #     return Response({'status': 'OK'})
    #


# class UserListAPIView(ListAPIView, GenericViewSet):
#     queryset = New.objects.all()
#     serializer_class = NewModelSerializer
#
#     def list(self, request, *args, **kwargs):
#         '''
#         nimadir yozamiz
#         user likni olish uchun
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         '''
#         return super().list(request, *args, **kwargs)
#
#     @action(methods=['GET'], detail=True, url_path='product', url_name='12321')
#     def report(self, request, id=None):
#         return Response({'status': id})


class ResponsePersonModelViewSet(ModelViewSet):
    queryset = ResponsiblePerson.objects.all()
    serializer_class = ResponsiblePersonModelSerializer

    @action(methods=['GET'], detail=False, queryset=Region.objects.all(),
            serializer_class=DistrictResponsiblePersonModelSerializer)
    def person(self, request, pk=None):
        queryset = self.get_queryset()
        serializered_data = self.serializer_class(queryset, many=True)
        return Response(serializered_data.data)


from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

images_params = openapi.Parameter('images', openapi.IN_FORM, description="test manual param", type=openapi.TYPE_ARRAY,
                                  items=openapi.Items(type=openapi.TYPE_FILE),
                                  required=True)


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    parser_classes = MultiPartParser, FormParser
    serializer_class = ProductTranslatableModelSerializer

    # permission_classes = IsAuthenticated,

    @swagger_auto_schema(tags=["Authors"], manual_parameters=[images_params])
    def post(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')
        response = super().post(request, *args, **kwargs)
        images_list = []
        for image in images:
            images_list.append(ProductImage(image=image, product_id=response.data['id']))
        ProductImage.objects.bulk_create(images_list)
        return response
