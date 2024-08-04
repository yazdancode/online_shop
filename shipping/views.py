from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from shipping.forms import ShippingAddressForm


def address_list(request):
    pass


@login_required
@require_http_methods(request_method_list=["GET", "POST"])
def address_create(request):
    if request.method == "POST":
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            form.save()
    else:
         form = ShippingAddressForm()
    return render(request, "shipping/create.html", {"form": form})
