from django.urls import path
from . import views

# urlpatterns = [
#     path('collections/', views.collection_list, name='collection_list'),
#     path('collections/<int:pk>/', views.collection_detail, name='collection_detail'),
#     path('products/', views.product_list, name='product_list'),
#     path('products/<int:pk>/', views.product_detail, name='product_detail'),
# ]
# PUT
# CRUD - create read update delete

from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers

# router = DefaultRouter()
router = routers.DefaultRouter()

router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('order', views.OrderViewSet, basename='orders')
# router.register('reviews', views.ReviewViewSet, basename='reviews')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')
# print(router.urls)
# urlpatterns = [
#     path('collections/', views.CollectionList.as_view(), name='collection_list'),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection_detail'),
#     path('products/', views.ProductList.as_view(), name='product_list'),
#     path('products/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
# ]

urlpatterns = router.urls + products_router.urls + carts_router.urls