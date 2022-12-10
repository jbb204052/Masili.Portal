from django.conf.urls.static import static
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include  # add this
import notifications.urls

from core import settings

urlpatterns = [
                  path('admin/', admin.site.urls),          # Django admin route
                  path("", include("apps.authentication.urls")), # Auth routes - login / register

                  # ADD NEW Routes HERE

                  # Leave `Home.Urls` as last the last line
                  path("", include("apps.home.urls")),
                  path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
                  path('tinymce/', include('tinymce.urls')),
                  # path(r'^calendar/', include('calendarium.urls')),
              ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
