from django.shortcuts import render, get_object_or_404
# from django.http import Http404
# Create your views here.

from .forms import ProductAddForm, ProductModelForm
from .models import Product


def create_view(request):
    # FORM
    form = ProductModelForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.sale_price = instance.price
        form.save()

    # if request.method == 'POST':
    #     print(request.POST)
    # if form.is_valid():
    #     data = form.cleaned_data
    #     title = data.get("title")
    #     description = data.get("description")
    #     price = data.get("price")
    #     new_obj = Product()
    #     new_obj.title = title
    #     new_obj.description = description
    #     new_obj.price = price
    #     new_obj.save()
    template = "create_view.html"
    context = {
        "form": form,
    }
    return render(request, template, context)


def detail_slug_view(request, slug=None):
    product = get_object_or_404(Product, slug=slug)
    template = "detail_view.html"
    context = {
        "object": product
    }
    return render(request, template, context)


def detail_view(request, object_id):
    # 1 item
    product = get_object_or_404(Product, id=object_id)
    template = "detail_view.html"
    context = {
        "object": product
    }
    return render(request, template, context)


def list_view(request):
    # list of items
    print(request)
    queryset = Product.objects.all()
    template = "list_view.html"
    context = {
        "queryset": queryset
    }
    return render(request, template, context)
