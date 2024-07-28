from django.db.models import Q
from django.http import HttpResponse
from catalogue.models import Product, Category, ProductType, Brand


def product_list(request):
    products = Product.objects.select_related("category").all()
    context = "\n".join(
        [
            f"{product.title}, {product.upc}, {product.category.name}"
            for product in products
        ]
    )
    return HttpResponse(context)


def product_detail(request, pk):
    product = Product.objects.filter(is_active=True).filter(Q(pk=pk) | Q(upc=pk))
    if product.exists():
        product = product.first()
        return HttpResponse(f"title:{product.title}")
    return HttpResponse("Product does not exist")


def category_products(request, pk):
    try:
        category = Category.objects.prefetch_related("products").get(pk=pk)
    except Category.DoesNotExist:
        return HttpResponse("Category does not exist")
    products = category.products.all()
    product_ids = [1, 2, 3]
    products = Product.objects.filter(id__in=product_ids)
    context = "\n".join([f"{product.title}, {product.upc}" for product in products])
    return HttpResponse(context)


def product_search(request):
    title = request.GET.get("q")
    products = Product.objects.actives(
        title__icontains=title,
        category__name__icontains=title,
    )
    # products = (
    #     Product.objects.filter(is_active=True)
    #     .filter(title__icontains=title)
    #     .filter(category__name__icontains=title)
    #     .distinct()
    #     .filter(category__is_active=True)
    )
    context = "\n".join([f"{product.title}, {product.upc}" for product in products])
    return HttpResponse(f"Search pages:\n{context}")
