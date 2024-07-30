from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
    path("catalogue/", include("catalogue.urls")),
    # path("accounts/", include("django.contrib.auth.urls"))
]
