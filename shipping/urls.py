from django.urls import path


from shipping.views import AddressListView, AddressCreateView

urlpatterns = [
    path("list/", AddressListView.as_view(), name="address-list"),
    # path("create/", address_create, name="address-create"),
    path("create/", AddressCreateView.as_view(), name="address-create"),
]
