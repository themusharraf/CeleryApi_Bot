from ckeditor.fields import RichTextField
from django.db import models
from django.db.models import (CASCADE, CharField, DateTimeField, FileField,
                              ForeignKey, ImageField, IntegerField, Model,
                              OneToOneField)
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields


class UseFulInfo(Model):
    title = CharField(max_length=255)
    image = ImageField(upload_to='images/usefullinfo/')
    number_download = IntegerField(default=0)
    file = FileField(upload_to='images/usefullinfo/')


class New(Model):
    title = CharField(max_length=255)
    image = ImageField(upload_to='images/new/')
    view_count = IntegerField(default=0)
    description = RichTextField(blank=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)


class Region(Model):
    name = CharField(max_length=255)


class District(Model):
    name = CharField(max_length=255)
    region = ForeignKey('apps.Region', CASCADE, 'districts')


class ResponsiblePerson(Model):
    full_name = CharField(max_length=255)
    phone = CharField(max_length=500)
    district = OneToOneField('apps.District', CASCADE)


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=CharField(_("Name"), max_length=200, null=True, blank=True)
    )


class Product(TranslatableModel):
    price = IntegerField(default=0)
    translations = TranslatedFields(
        name=CharField(_("Name"), max_length=200, null=True, blank=True)
    )
    category = ForeignKey('apps.Category', CASCADE)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


class ProductImage(Model):
    image = ImageField(upload_to='product/images')
    product = ForeignKey('apps.Product', CASCADE)


'''

[
    {
        "name": "Toshkent",
        "districts":[
            {
                "name": "Yunusobod tumani",
                "full_name": "Бакиров Тимур Жолдасбаевич",
                "phone": "612227089"
            }
        ]
    }
]

 {
    "districts": [
      {
        "name": "yunusobod tumani",
        "full_name": "Раимов Акбар Абдурашитович",
        "phone": "755921629"
      },
      {
        "name": "CHilonzor tumani",
        "full_name": "Tohirjon 123",
        "phone": "12372615"
      }
    ],
    "name": "toshkent"
  },
'''
