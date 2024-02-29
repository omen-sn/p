from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from rest_framework import viewsets, permissions, filters
from .models import Product, Category, TagProduct, ProductDetail
from .permissions import CustomPermission, IsOwnerOrAdmin, IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import CategorySerializer, ProductSerializer, TagProductSerializer, ProductDetailSerializer

# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'category__name']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TagProductViewSet(viewsets.ModelViewSet):
    queryset = TagProduct.objects.all()
    serializer_class = TagProductSerializer
    permission_classes = [IsAdminOrReadOnly]

class ProductDetailViewSet(viewsets.ModelViewSet):
    queryset = ProductDetail.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


###########is used for the frontend, as I have not yet had time to rewrite it for api use################
menu = [
    {'title': 'About', 'url_name': 'about'},
    {'title': 'Add Article', 'url_name': 'add_page'},
    {'title': 'Contact', 'url_name': 'contact'},
    {'title': 'Login', 'url_name': 'login'}
]

def index(request):
    products = Product.published.all().select_related('category').prefetch_related('tags')
    data = {
        'title': "Welcome to StoreHouse!",
        'menu': menu,
        'products': products,
        'cat_selected': 0,
    }
    return render(request, 'stockcontrol/index.html', data)

def about(request):
    data = {
        'menu': menu,
    }
    return render(request, 'stockcontrol/about.html', data)

def add_article(request):
    return render(request, 'base.html')

def contact(request):
    return render(request, 'base.html')

def login_view(request):
    return render(request, 'base.html')

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    products = Product.published.filter(category_id=category.pk).select_related('category').prefetch_related('tags')

    data = {
        'title': "Categories",
        'menu': menu,
        'products': products,
        'cat_selected': category.pk,
    }
    return render(request, 'stockcontrol/index.html', data)

def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    data = {
        'menu': menu,
        'product': product,
        'cat_selected': None,
    }
    return render(request, 'stockcontrol/product_detail.html', data)


def show_tag_product(request, tag_slug):
    tag = get_object_or_404(TagProduct, slug=tag_slug)
    products = tag.tags.filter(is_published=Product.Status.PUBLISHED).select_related('category').prefetch_related('tags')

    data = {
        'title': f"Tag: #{tag.tag}",
        'menu': menu,
        'products': products,
        'cat_selected': None,
    }

    return render(request, 'stockcontrol/index.html', context=data)

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</p>")
