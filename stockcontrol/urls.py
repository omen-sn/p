from django.urls import path, re_path, register_converter, include
from rest_framework.routers import DefaultRouter
from . import views
from . import converters


router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'tags', views.TagProductViewSet)
router.register(r'product-detail', views.ProductDetailViewSet)

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('add-article/', views.add_article, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('product/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('tag/<slug:tag_slug>/', views.show_tag_product, name='tag'),

    # Маршрути DRF API
    path('api/', include(router.urls)),
]