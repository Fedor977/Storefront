from django.shortcuts import render, get_object_or_404
from .models import Product, Collection, Review
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer
from rest_framework import status
from django.db.models import Count


# collections/


# api_view - декоратор над функцией для отображения, дающий возможность указать допустимые методы запросы
# PATCH
# HEADERS

# GET, POST, PUT, DELETE

# /products

@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(products_count=Count('product')).all()
        serializer = CollectionSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = Collection.objects.annotate(products_count=Count('product')).get(pk=pk)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.product_set.count() > 0:
            return Response({'error': 'Нельзя удалить категорию, так как у нее есть продукт'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def product_list(request):
    # вывести все товары из БД
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()  # QuerySet
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=201)  # created
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# pip install -r requirements.txt


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if product.orderitem_set.count() > 0:
            return Response({'error': 'Нельзя удалить продукт, так как он есть в заказе'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.views import APIView


class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.select_related('collection').all()  # QuerySet
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get(self, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    def put(self, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitem_set.count() > 0:
            return Response({'error': 'Нельзя удалить продукт, так как он есть в заказе'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(APIView):
    def get(self, request):
        queryset = Collection.objects.annotate(products_count=Count('product')).all()
        serializer = CollectionSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = CollectionSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionDetail(APIView):
    def get(self, request, pk):
        collection = Collection.objects.annotate(products_count=Count('product')).get(pk=pk)
        serializer = CollectionSerializer(collection, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        collection = Collection.objects.annotate(products_count=Count('product')).get(pk=pk)
        serializer = CollectionSerializer(collection, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        collection = Collection.objects.annotate(products_count=Count('product')).get(pk=pk)
        if collection.product_set.count() > 0:
            return Response({'error': 'Нельзя удалить категорию, так как у нее есть продукт'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework import generics, mixins


class ProductList(generics.ListCreateAPIView):
    # def get_queryset(self): метод для получения всех элементов продуктов
    #     products = Product.objects.select_related('collection').all() обращаемся к модельке продукта Product
    #     менеджуеру объекта objects  забераем связанные элементы select_related и указываем 'collection'
    # забераем забираем вообще все элементы
    #     return products
    #
    # def get_serializer_class(self): отдает ссылку на класс сериалайзера
    #     return ProductSerializer тут отдаем сериалайзер

    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    # def get_serializer_context(self):
    #     return {'request': self.request}


class CollectionList(generics.ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count('product')).all()
    serializer_class = CollectionSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        # print(args, kwargs)
        # product = get_object_or_404(Product, pk=kwargs.get('pk'))
        if product.orderitem_set.count() > 0:
            return Response({'error': 'Нельзя удалить продукт, так как он есть в заказе'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count=Count('product')).all()
    serializer_class = CollectionSerializer

    def delete(self, request, *args, **kwargs):
        collection = self.get_object()
        if collection.product_set.count() > 0:
            return Response({'error': 'Нельзя удалить категорию, так как у нее есть продукт'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.viewsets import ModelViewSet
from .filters import ProductFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import DefaultPagination


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    pagination_class = DefaultPagination

    def get_queryset(self):
        queryset = Product.objects.all()
        collection_id = dict(self.request.query_params).get('collection_id')
        if collection_id is not None:
            queryset = queryset.filter(collection_id=collection_id[0])
        return queryset

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.orderitem_set.count() > 0:
            return Response({'error': 'Нельзя удалить продукт, так как он есть в заказе'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        collection = self.get_object()
        if collection.product_set.count() > 0:
            return Response({'error': 'Нельзя удалить категорию, так как у нее есть продукт'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product': self.kwargs['product_pk']}


from rest_framework.mixins import RetrieveModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from .serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from .models import Cart, CartItem


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}


# af632a52-99f9-417d-b57c-c7a8823e242a

from .serializers import CustomerSerializer, OrderSerializer, OrderItemSerializer, UpdateOrderSerializer, \
    CreateOrderSerializer
from .models import Customer, Order, OrderItem
from .permissions import IsAdminOrReadOnly, ViewCustomerHistoryPermissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermissions])
    def history(self, request, pk):
        return Response('ok')

    # права доступа permission_classes

    @action(detail=True, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        try:
            customer = Customer.objects.get(user_id=request.user.pk)
        except:
            customer, created = Customer.objects.get_or_create(
                user_id=request.user.id
            )

        # получи либо создай get_or_create

        if request.method == 'GET':
            serializer = CustomerSerializer(Customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(Customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data,
            context={'user_id': self.request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()

        customer_id = Customer.objects.only('id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


from .serializers import ProductImageSerializer
from .models import ProductImage


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
