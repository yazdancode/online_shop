from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from blog.models import Post, Blog


def post_list(request, year=None, month=None):
    if year is not None:
        return HttpResponse(f"Post list archive for {year} and {month}")
    if year is not None:
        return HttpResponse(f"Post list archive for {year}")
    return HttpResponse("<h1>H1 tag</h1><br><h2>H2 tag</h2>")


class BlogPostListView(ListView):
    model = Post


def categories_list(request):
    return HttpResponse("Category list page")


def post_detail(request, post_slug):
    return HttpResponse(f"Post detail {post_slug}")


class BlogPostDetailView(ListView):
    model = Blog


def custom_post_detail(request):
    return HttpResponse(f"Custom Post detail")


class CustomTemplateView(TemplateView):
    pass
