from django.views import generic
from django.views.generic import ListView
from django.shortcuts import render

from product.models import Variant
from product.models import Product

from product.forms import ProductForm


class BaseProductview(generic.View):
    form_class = ProductForm
    model = Product
    template_name = '/products/create.html'
    success_url = '/product/products'


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

class ListProducts(BaseProductview, ListView):
    template_name = 'products/list.html'
    paginated_by = 10

    def get_queryset(self):
        filter_string = {}
        print("Products filter request: ",self.request.GET)

        for key in self.request.GET:
            if self.request.GET.get(key):
                sql_key = key+'__icontains'
                filter_string[sql_key] = self.request.GET.get(key)
        print("Filter string\n",**filter_string)
        return Product.objects.filter(**filter_string)
    
    def get_context_data(self, **kwargs):
        print("Get Context data: here")
        context = super().get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')

        context['product'] = True
        context['variants'] = list(variants.all())
        context['request'] = ''
        if self.request.GET:
            context['request'] = self.request.GET['title']
        print("Product context['request'] = ", context['request'])
        return context
