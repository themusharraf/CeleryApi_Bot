from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer
from rest_framework.fields import CharField, FileField, ImageField
from rest_framework.serializers import ListSerializer, ModelSerializer

from apps.models import (District, New, Product, Region, ResponsiblePerson,
                         UseFulInfo)


class NewListModelSerializer(ModelSerializer):
    class Meta:
        model = New
        fields = ('id', 'title', 'view_count', 'created_at')


class RegionListModelSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class UseFulInfoListModelSerializer(ModelSerializer):
    class Meta:
        model = UseFulInfo
        fields = ('id', 'image', 'number_download', 'title', 'file')


class NewDetailModelSerializer(ModelSerializer):
    class Meta:
        model = New
        fields = ('id', 'title', 'view_count', 'description', 'created_at')


class DistrictModelSerializer(ModelSerializer):
    class Meta:
        model = District
        exclude = ('id', 'region')

    def to_representation(self, instance: District):
        _repr = super().to_representation(instance)
        _repr['full_name'] = instance.responsibleperson.full_name
        _repr['phone'] = instance.responsibleperson.phone
        return _repr


class DistrictResponsiblePersonModelSerializer(ModelSerializer):
    districts = DistrictModelSerializer(many=True, required=False)

    class Meta:
        model = Region
        exclude = ('id',)


class ResponsiblePersonModelSerializer(ModelSerializer):
    class Meta:
        model = ResponsiblePerson
        fields = ('id', 'full_name', 'phone', 'district')


class RegionModelSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


# # class ProductModelSerializer(ModelSerializer):
#
# from django.utils.translation import get_language_from_request
#
#
# class TranslatedSerializerMixin:
#     """
#     Mixin for selecting only requested translation with django-parler-rest
#     """
#
#     def to_representation(self, instance):
#         inst_rep = super().to_representation(instance)
#         request = self.context.get('request')
#         lang_code = get_language_from_request(request)
#         result = {}
#         for field_name, field in self.get_fields().items():
#             # add normal field to resulting representation
#             if field_name is not 'translations':
#                 field_value = inst_rep.pop(field_name)
#                 result.update({field_name: field_value})
#             if field_name is 'translations':
#                 translations = inst_rep.pop(field_name)
#                 if lang_code not in translations:
#                     # use fallback setting in PARLER_LANGUAGES
#                     parler_default_settings = settings.PARLER_LANGUAGES['default']
#                     if 'fallback' in parler_default_settings:
#                         lang_code = parler_default_settings.get('fallback')
#                     if 'fallbacks' in parler_default_settings:
#                         lang_code = parler_default_settings.get('fallbacks')[0]
#                 for lang, translation_fields in translations.items():
#                     if lang == lang_code:
#                         trans_rep = translation_fields.copy()  # make copy to use pop() from
#                         for trans_field_name, trans_field in translation_fields.items():
#                             field_value = trans_rep.pop(trans_field_name)
#                             result.update({trans_field_name: field_value})
#         return result


class ProductTranslatableModelSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Product)

    class Meta:
        model = Product
        fields = ('translations',)
