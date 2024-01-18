from rest_framework import serializers

from .models import Products

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = '__all__'