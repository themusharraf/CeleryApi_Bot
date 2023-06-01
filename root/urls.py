from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from apps.views import ProductListCreateAPIView
from root.settings import MEDIA_ROOT, MEDIA_URL

schema_view = get_schema_view(
   openapi.Info(
      title="P8 gruppa API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
from django.utils.translation import gettext_lazy as _

urlpatterns = [
   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('admin/', admin.site.urls),
   path('', include('apps.urls')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path(_("product"), ProductListCreateAPIView.as_view()),
)