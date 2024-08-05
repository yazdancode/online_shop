from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, FormView
from shipping.forms import ShippingAddressForm
from shipping.models import ShippingAddress


class CustomUserListView(ListView):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class AddressListView(CustomUserListView):
    model = ShippingAddress

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=object_list, **kwargs)
        context["extra_data"] = self.get_queryset().count()
        return context


@login_required
@require_http_methods(["GET", "POST"])
def address_create(request):
    if request.method == "POST":
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            # Ensure the address is linked to the current user
            instance.user = request.user
            instance.save()
            return redirect("address-list")
    else:
        form = ShippingAddressForm()
    return render(request, "shipping/create.html", {"form": form})


class AddressCreateView(FormView):
    form_class = ShippingAddressForm
    template_name = "shipping/create.html"
    success_url = reverse_lazy("address-list")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)
