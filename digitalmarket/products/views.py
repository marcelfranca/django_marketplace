from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
# from django.http import Http404
# Create your views here.

from .forms import ProductAddForm, ProductModelForm
from .models import Product


class ProductListView(ListView):
    model = Product
    # template_name = 'list_view.html'

    # def get_context_data(self, object_list=None, **kwargs):
    #   context = super(ProductListView, self).get_context_data(**kwargs)
    #   print(context)
    #    context["queryset"] = self.get_queryset()
    #    return context

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(**kwargs)
        # qs = qs.filter(title__icontains="Product")
        return qs


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
    template = "form.html"
    context = {
        "form": form,
        "submit_btn": "Create Product"
    }
    return render(request, template, context)


def update_view(request, object_id):
    # 1 item
    product = get_object_or_404(Product, id=object_id)
    form = ProductModelForm(request.POST or None, instance=product)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
    template = "form.html"
    context = {
        "object": product,
        "form": form,
        "submit_btn": "Update Product"
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


