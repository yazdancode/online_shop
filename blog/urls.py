from django.urls import path, register_converter, re_path
from blog.views import post_list, categories_list, post_detail, custom_post_detail
from blog.utils import FourDigitYear


register_converter(FourDigitYear, "fourdigit")

urlpatterns = [
    path("list/", post_list, name="post_list"),
    path("detail/hello/", custom_post_detail, name="custom_post_detail"),
    path("detail/<slug:post_slug>/", post_detail, name="post_detail"),
    path("categories/list/", categories_list, name="categories_list"),
    path("archive/<fourdigit:year>/", post_list, name="archive_year"),
    path("archive/<int:year>/<int:month>/", post_list, name="archive_year_month"),
    
    re_path(r"^detail/(?P<post_slug>[\w-]+)/$", post_detail, name="post_detail_re"),
    re_path(r"^archive/(?P<year>[0-9]{2,4})/$", post_list, name="archive_year_re"),
    re_path(r"^archive/(?P<code>[0-9]{4,6})/$", post_list, name="archive_code"),
]
