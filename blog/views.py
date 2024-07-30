from django.http import HttpResponse


def post_list(request, year=None, month=None):
    if year is not None:
        return HttpResponse(f"Post list archive for {year} and {month}")
    if year is not None:
        return HttpResponse(f"Post list archive for {year}")
    return HttpResponse("<h1>H1 tag</h1><br><h2>H2 tag</h2>")


def categories_list(request):
    return HttpResponse("Category list page")


def post_detail(request, post_slug):
    return HttpResponse(f"Post detail {post_slug}")


def custom_post_detail(request):
    return HttpResponse(f"Custom Post detail")
