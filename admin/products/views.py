from random import choice
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import ProductSerializer
from .models import Product, User
from django.http import HttpResponse
from .producer import publish_to_main

# Simple view to return 'hello world'
def index(request):
    return HttpResponse('hello world')

# ViewSet for handling CRUD operations on the Product model
class ProductViewSet(viewsets.ViewSet):
    # Retrieve a list of all products
    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    # Create a new product
    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            publish_to_main('product_created', serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Retrieve details of a specific product
    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)
        return Response(serializer.data)

    # Update a specific product
    def update(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            publish_to_main('product_updated', serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete a specific product
    def delete(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        publish_to_main('product_deleted', pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

# APIView to retrieve a random User ID
class UserAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        user = choice(users)
        return Response({'id': user.id})
