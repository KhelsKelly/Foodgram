from recipes.models import Ingredient
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['title', 'dimension']
        read_only_fields = ['title', 'dimension']
