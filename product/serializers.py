from base.models import Product
from rest_framework import serializers

class GetAllProductSerializers(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'