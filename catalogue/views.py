from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
    permission_required,
)
from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_POST
from django.db.models import Q
from django.http import HttpResponse, Http404
from catalogue.models import Product, Category
from catalogue.utils import check_is_active


def product_list(request):
    context = dict()
    context["products"] = Product.objects.select_related("category").all()
    return render(request, "catalogue/product_list.html", context=context)


def product_detail(request, pk):
    product = Product.objects.filter(is_active=True).filter(Q(pk=pk) | Q(upc=pk))
    if product.exists():
        product = product.first()
        return render(
            request, "catalogue/product_detail.html", context={"product": product}
        )
    raise Http404


def category_products(request, pk):
    try:
        category = Category.objects.prefetch_related("products").get(pk=pk)
    except Category.DoesNotExist:
        return HttpResponse("Category does not exist")
    products = category.products.all()
    context = "\n".join([f"{product.title}, {product.upc}" for product in products])
    return HttpResponse(context)


def product_search(request):
    title = request.GET.get("q")
    products = Product.objects.actives(
        Q(title__icontains=title) | Q(category__name__icontains=title)
    )
    context = "\n".join([f"{product.title}, {product.upc}" for product in products])
    return HttpResponse(f"Search pages:\n{context}")


@login_required()
@require_http_methods(request_method_list=["GET"])
@user_passes_test(check_is_active)
@user_passes_test(lambda u: u.is_staff)
# @user_passes_test(lambda u: u.has_perm('transaction.Has_score_permission'))
@permission_required("transaction.Has_score_permission")
def user_profile(request):
    return HttpResponse(f"Hello {request.user.username}")


@login_required()
@require_POST
# @require_GET
@user_passes_test(lambda u: u.score > 20)
@user_passes_test(lambda u: u.age > 14)
def campaign(request):
    return HttpResponse(f"Hello {request.user.username}")
