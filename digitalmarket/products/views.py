from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.http import Http404
from django.urls import reverse
from django.db.models import Q
# Create your views here.

from digitalmarket.mixins import MultiSlugMixin, SubmitBtnMixin, LoginRequiredMixin, StaffRequiredMixin

from .forms import ProductAddForm, ProductModelForm
from .models import Product
from .mixins import ProductManagerMixin


class ProductCreateView(LoginRequiredMixin, SubmitBtnMixin, CreateView):
    model = Product
    template_name = "form.html"
    form_class = ProductModelForm
    # success_url = "/products/list/"
    submit_btn = "Add Product"

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        valid_data = super(ProductCreateView, self).form_valid(form)
        form.instance.managers.add(user)
        return valid_data

    def get_success_url(self):
        return reverse("product_list_view")


class ProductUpdateView(ProductManagerMixin, SubmitBtnMixin, MultiSlugMixin, UpdateView):
    model = Product
    template_name = "form.html"
    form_class = ProductModelForm
    success_url = "/products/list/"
    submit_btn = "UpdateProduct"


class ProductDetailView(DetailView):
    model = Product


class ProductListView(ListView):
    model = Product

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(**kwargs)
        query = self.request.GET.get("q")
        qs = qs.filter(Q(title__icontains=query) |
                       Q(description__icontains=query)
                       ).order_by("title")
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


