from django.urls import path
from catalogue.views import product_list, product_detail


urlpatterns = [
    path("product/list/", product_list, name="product-list"),
    path("product/detail/<int:pk>/", product_detail, name="product-detail"),
]
