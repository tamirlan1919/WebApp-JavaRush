from django.shortcuts import render
from django.db.models import QuerySet, Avg
from .models import Product, Category
from django.views.generic import ListView, DetailView
from orders.models import OrderItem



class ProductListView(ListView):
    model = Product
    template_name = 'products/catalog.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self) -> QuerySet:
        qs = Product.objects.filter(is_active=True).select_related('category')

        # Filter by category if provided
        category_slug = self.request.GET.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(name__icontains=query) | qs.filter(description__icontains=query)

        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)

        sort = self.request.GET.get('sort', '-created_at')

        sort_map = {
            'price_asc': 'price',
            'price_desc': '-price',
            'new': '-created_at',
        }

        qs = qs.order_by(sort_map.get(sort, '-created_at'))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(parent=None).prefetch_related('children')
        context['current_category'] = self.request.GET.get('category', '')
        context['current_sort'] = self.request.GET.get('sort', 'new')
        context['current_q'] = self.request.GET.get('q', '')
        return context




class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).select_related('category')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        context['reviews'] = product.reviews.select_related('user').order_by('-created_at')

        avg = product.reviews.aggregate(Avg('rating'))['rating__avg']
        context['average_rating'] = round(avg, 1) if avg else None

        if self.request.user.is_authenticated:
            if OrderItem.objects.filter(product=product, order__user=self.request.user, order__status='completed').exists():
                context['can_review'] = True
            if product.reviews.filter(user=self.request.user).exists():
                context['user_review'] = product.reviews.get(user=self.request.user)

        return context





