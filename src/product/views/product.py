from django.views import generic
from django.views.generic import ListView
from django.shortcuts import render

from product.models import Variant
from product.models import Product
from product.models import ProductVariantPrice

from product.forms import ProductForm


class BaseProductview(generic.View):
    form_class = ProductForm
    model = ProductVariantPrice
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
    paginate_by = 2

    def get_queryset(self):
        filter_string = {}
        print("Products filter request: ", self.request.GET)

        for key in self.request.GET:
            if key != 'page' and self.request.GET.get(key):
                sql_key = key + '__icontains'
                filter_string[sql_key] = self.request.GET.get(key)
        print("Filter string\n", str(filter_string))
        queryset = Product.objects.filter(**filter_string).prefetch_related('productvariantprice_set__product_variant_one', 'productvariantprice_set__product_variant_two', 'productvariantprice_set__product_variant_three')
        return queryset
        # filter_string = {}
        # print("Products filter request: ",self.request.GET)

        # for key in self.request.GET:
        #     if key!='page' and self.request.GET.get(key):
        #         sql_key = key+'__icontains'
        #         filter_string[sql_key] = self.request.GET.get(key)
        # print("Filter string\n",**filter_string)
        # return Product.objects.filter(**filter_string)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_string = {}
        for key in self.request.GET:
            if key != 'page' and self.request.GET.get(key):
                sql_key = key + '__icontains'
                filter_string[sql_key] = self.request.GET.get(key)
        products = Product.objects.filter(**filter_string).prefetch_related('productvariantprice_set__product_variant_one', 'productvariantprice_set__product_variant_two', 'productvariantprice_set__product_variant_three')
        variants = Variant.objects.filter(active=True).values('id', 'title')

        context['product'] = True
        page_number = int(self.request.GET.get('page', 0))
        context['products'] = products[page_number * self.paginate_by:(page_number + 1) * self.paginate_by]
        context['variants'] = list(variants.all())
        context['request'] = ''
        if self.request.GET:
            context['request'] = self.request.GET.get('title', '')
        return context
        # context = super().get_context_data(**kwargs)
        # products = Product.objects.all().prefetch_related('productvariantprice_set__product_variant_one', 'productvariantprice_set__product_variant_two', 'productvariantprice_set__product_variant_three')
        # variants = Variant.objects.filter(active=True).values('id', 'title')

        # context['product'] = True
        # context['products'] = products
        # context['variants'] = list(variants.all())
        # context['request'] = ''
        # if self.request.GET:
        #     context['request'] = self.request.GET.get('title', '')
        # return context
        # print("Get Context data: here")
        # context = super().get_context_data(**kwargs)
        # variants = Variant.objects.filter(active=True).values('id', 'title')

        # context['product'] = True
        # context['variants'] = list(variants.all())
        # context['request'] = ''
        # if self.request.GET:
        #     context['request'] = self.request.GET.get('title', '')
        # print("Product context['request'] = ", context['request'])
        # return context
